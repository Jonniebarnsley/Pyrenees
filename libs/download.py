import os
import ssl
import aiohttp
import asyncio
import pyesgf.search
from itertools import product

import nest_asyncio
nest_asyncio.apply()

def generate_dataset_local_path(
            dataset: pyesgf.search.results.DatasetResult, 
            home_path: str
    ):
    '''
    Takes pyesgf dataset object and returns a path object for that dataset were it stored locally, format:
        $DATA_HOME/project/domain/variable/experiment/gcm/rcm
    '''
    id, data_node = dataset.dataset_id.split('|')
    project, product, domain, institute, gcm, experiment, ensemble, rcm, downscaling, frequency, variable, version = id.split('.')

    path = os.path.join(home_path, project, domain, variable, experiment, ensemble, gcm, rcm)

    return path

async def download_file(
            session: aiohttp.ClientSession, 
            file: pyesgf.search.results.FileResult, 
            local_directory: str,
            sslcontext: ssl.SSLContext
    ):
    '''
    Coroutine which takes a aiohttp client session and pyesgf file object and downloads it to a local directory
    '''
    url = file.download_url
    if 'HadREM3-GA7-05' in url:
        url.replace('v20201111', 'latest') # hack to avoid http error

    filename = file.filename
    filepath = os.path.join(local_directory, filename)

    # if file already exists, skip it
    if os.path.isfile(filepath):
        return

    # open client session
    async with session.request('get', url, ssl=sslcontext) as response:
        
        temp_filepath = filepath+'.inprogress' # temporary filename whilst downloading
        chunk_size = 2048
        with open(temp_filepath, 'wb') as local_file:
            async for chunk in response.content.iter_chunked(chunk_size):
                local_file.write(chunk)
            os.rename(temp_filepath, filepath) # remove .inprogress suffix when finished

async def download_multiple(
            loop: asyncio.unix_events._UnixSelectorEventLoop, 
            files: pyesgf.search.results.ResultSet, 
            local_directory: str
    ):
    '''
    Coroutine that takes ayncio loop object and pyesgf files object and asynchronously downloads them to
    a local directory. 
    '''
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_file(session, file, local_directory) for file in files]
        await asyncio.gather(*tasks)

def remove_incomplete_files(directory):
    '''
    removes any files in a certain directory with the '.inprogress' suffix
    '''
    filenames = os.listdir(directory)
    incomplete = [os.path.join(directory, filename) for filename in filenames if '.inprogress' in filename]
    for file in incomplete:
        os.remove(file)
    if not os.listdir(directory): # if directory empty
        os.rmdir(directory)

def download_dataset(
            dataset: pyesgf.search.results.DatasetResult, 
            local_path: str,
            verbose: bool = False
    ):
    '''
    Takes pyesgf dataset object, creates local directory for dataset to be stored, extracts file objects
    then asynchronously downloads all files.
    '''
    # create all appripriate directories if they do not already exist
    directory = generate_dataset_local_path(dataset, local_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # extract files
    files = dataset.file_context().search(ignore_facet_check=True)

    # create loop for asynchronous downloads
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(download_multiple(loop, files, directory))
        verbose and print('---> done!')
        return True
    except Exception as err:
        verbose and print('\n\tencountered an error:', repr(err))
        remove_incomplete_files(directory)
        return False

def download_ensemble(
            context: pyesgf.search.context.DatasetSearchContext,
            local_path: str,
            verbose: bool = False
            
    ):
    ''' 
    Takes a pyesgf context object and downloads all available datasets that satisfy the constraints of
    that context. Datasets are downloaded one by one, but files within each dataset are downloaded
    asynchronously.
    '''
    # get all matching datasets for context
    results = context.search()

    # initialise outputs
    successfully_downloaded = set()
    encountered_errors = set()


    for i, dataset in enumerate(results):
        verbose and print('downloading {} of {}: {}'.format(i+1, len(results), dataset.dataset_id), end=' ')

        try:
            success = download_dataset(dataset, local_path, verbose) # True if all files downloaded successfully
            if success:
                successfully_downloaded.add(dataset.dataset_id)
            else:
                encountered_errors.add('\t'+dataset.dataset_id)
        except KeyboardInterrupt:
            directory = generate_dataset_local_path(dataset, local_path)
            remove_incomplete_files(directory)
            break

    print('\nsuccessfully downloaded {} of {} datasets'.format(len(successfully_downloaded), len(results)))
    if encountered_errors:
        print('the following datasets were not downloaded due to encountering errors during the process:')
        print(*encountered_errors, sep='\n')

    return {
        'success': successfully_downloaded,
        'errors': encountered_errors
    }

def make_multiple_queries(queries: dict):
    '''
    Takes a queries dictionary with ESGF facets as keys and lists of strings as values.
    Prints a table of all configurations of query and the number of datasets that match.
    Returns a dictionary of contexts for each configuration.
    Has the structure -> dict[config] = context
    '''
    headers = queries.keys()
    values = queries.values()
    h = len(headers)
    contexts = {}

    print('querying ESGF...')
    print('found the following datasets matching your queries:\n')

    # print table
    print(('{:<14} '*h).format(*headers), 'hit_count')
    for config in product(*values):
        query = {key: value for key, value in zip(headers, config)}
        context = conn.new_context(**query, facets=headers)
        contexts[config] = context
        hit_count = context.hit_count
        print(('{:<14} '*h).format(*config), hit_count)

    return contexts

def download_multiple_ensembles(queries:dict, verbose:bool=False):
    '''
    Takes a queries dictionary in the same form as make_multiple_queries. Carries out said queries
    and then requests confirmation from the user to proceed. Following confirmation, continues to
    download each ensemble one by one
    '''
    contexts = make_multiple_queries(queries)
    successfully_downloaded = set()
    encountered_errors = set()

    print('querying ESGF...')
    print('found the following datasets matching your queries:\n')

    response = input('proceed? (y/n)')
    if response != 'y':
        return

    for config in contexts:

        print('\ndownloading next config:', *config)
        context = contexts[config]
        downloads = download_ensemble(context, verbose)
        for dataset in downloads:
            successfully_downloaded |= dataset['success']
            encountered_errors |= dataset['errors']

    print('\nall downloads now complete. successfully downloaded {} out of {} datasets.'.format(
                len(successfully_downloaded),
                len(successfully_downloaded)+len(encountered_errors)
    ))
    print('a full list of datasets omitted due to errors is available below:\n')
    print(*encountered_errors, sep='\n')
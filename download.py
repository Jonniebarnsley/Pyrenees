import os
import ssl
import libs.downloader as dl
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection

queries = {
    'project': ['CORDEX'],
    'domain': ['EUR-11'],
    'experiment': ['historical', 'rcp26', 'rcp85'],
    'variable': ['tas', 'pr'],
    'time_frequency': ['mon'],
    'ensemble': ['r1i1p1']
}

# ensure the following are saved as environment variables
USERNAME = os.environ['ESGF_USERNAME']
PASSWORD = os.environ['ESGF_PASSWORD']
DATA_PATH = os.environ['DATA_HOME']

conn = SearchConnection('http://esgf-data.dkrz.de/esg-search', distrib=True)

myproxy_host = 'esgf-data.dkrz.de'

lm = LogonManager()
lm.logon(username=USERNAME, password=PASSWORD, hostname=myproxy_host)

sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
sslcontext.load_verify_locations(capath=lm.esgf_certs_dir)
sslcontext.load_cert_chain(lm.esgf_credentials)

dl.download_multiple_ensembles(queries, conn, sslcontext, DATA_PATH)

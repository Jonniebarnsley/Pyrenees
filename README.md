# Climate modelling workshops

Hi and welcome back to everybody's favourite field trip activity – modelling! Today we're looking at climate models, that is mathematical models designed to represent aspects of the Earth's climate. Climate models come in all shapes and sizes, from very basic [box-models](https://en.wikipedia.org/wiki/Climate_model#Box_models) to sophisticated [General Circulation Models](https://en.wikipedia.org/wiki/General_circulation_model) (GCMs). The former can be run with a simple laptop, the latter are usually run on supercomputers such as NERC's very own [ARCHER2](https://www.archer2.ac.uk/). Unfortunately, I forgot to pack my supercomputer with me this week, so we're limited in how sophisticated we can get with this modelling exercise.

There are two workshops in this github repositry – which one most interests you most may depend on your personal area of research and your experience with the Python programming language. They are:

- `cordex_workshop.ipynb` - Pyrenees climate projections in CORDEX, the Coordinated Regional climate Downscaling Experiment
- `snowball_earth_workshop.ipynb` - Investigating the role of the ice-albedo feedback in glacial-interglacial cycles

The CORDEX workshop doesn't include any real modelling per se, but looks at data produced by one of the most sophisticated climate models out there. The snowball Earth workshop takes a much simpler model, but allows for some fun tweaking of parameters if you're at all familiar with Python. Ultimately, both can be clicked through without giving too much thought to the code and you may only be interested in the outputs and what they can tell us about climate change. I promise not to be disappointed (much) if you opt for this approach.

Both workshops can be run in a Binder we've prepared at this link: https://mybinder.org/v2/gh/Jonniebarnsley/Pyrenees/HEAD.

## CORDEX workshop

CORDEX is an internationally coordinated effort to produce high-resolution regional climate model data for several of the world's key regions. Boundary conditions for the regions are provided by an ensemble of GCMs, with high-resolution Regional Climate Models (RCMs) handling the dynamics within the region. The project has standardised a number of experiments for each GCM-RCM pair to run, including a historical run and one for each Representative Concentration Pathway (RCP). The full dataset can be browsed manually at https://esgf-data.dkrz.de/search/cordex-dkrz/. For the Pyrenees, the region of interest has the code 'EUR-11'.

This practical 

### Instructions

No downloads or installations are required to run this practical. All the notebooks, data, and software is available in a binder, which can be accessed at https://mybinder.org/v2/gh/Jonniebarnsley/Pyrenees/HEAD.


Once you've accessed the binder, open the file `cordex_workshop.ipynb` and click through the jupyter notebook. If you're not familiar with python, there's no need to think too much about the code and what it's doing. Simply read through the comments explaining what is going on and have a look at the plots generated. However, do feel free to tweak aspects of the code if you'd like to explore what is possible with geospatial data.
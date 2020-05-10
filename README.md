# RemoveExternalDataSources.py

## Overview

This tool can be used to remove external dependencies from `.bacpac` database backups that were generated on MS Azure. External SQL tables and data sources are not compatible with local SQL instances, and therefore backups created with those features are incompatible with local development tools.

I often need to deploy such backups to test new features locally, and I didn't feel like manually scrubbing the XML for the errant elements each time, so this tool automates the process.

## Usage
### First time setup
1. Clone the repo
1. `python -m pip install lxml`
1. Run `python RemoveExternalDataSources.py` once to set up the requisite file structures

### Normal operation
1. Place your faulting `*.bacpac` in the `/in` folder
1. Run `python RemoveExternalDataSources.py`
1. If it completes without errors, your shiny clean `*_localsafe.bacpac` will be in the `/out` folder, and your original file will be copied to the `/processed` folder
1. SSMS will now be able to import the new `*_localsafe.bacpac` as a data-tier application

## Processes
1. Decompress `*.bacpac`
1. Remove `Type=SqlExternalDataSource` XML elements from `model.xml`
1. Remove `Type=SqlExternalTable` XML elements from `model.xml`
1. Recalculate and replace the SHA256 hash in `Origin.xml`
1. Recompress resulting files into new `*_localsafe.bacpac`

## Author
Riley Hunter

11/05/2020

https://github.com/RileyHunter/RemoveExternalDataSources

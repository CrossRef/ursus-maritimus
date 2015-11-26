# Ursus Maritimus

Example text and data mining application to demonstrate Crossref's Text and Data Mining API. It uses the Habanero Crossref client library.

## Requirements

PIP and virtualenv

 - `sudo apt-get install virtualenvwrapper`
 - `mkvirtualenv ursus-maritimus`
 - Log into the Crossref Clickthrough Service and get a token: https://apps.crossref.org/clickthrough/researchers/#/

## Installation

 - `workon ursis-maritimus`
 - `pip install -r requirements.txt`


## To run

1. Put your token in an environment variable called `TDM_TOKEN` e.g. `EXPORT TDM_TOKEN=60baeedb-ec5ce822-1222be6f-XXXXXXXX`.
2. Fetch the licenses that apply for your given query.
  
     `python run.py licenses`

3. Review the licenses in `licenses.txt`. Remove the ones you don't like.
4. Fetch the URLs

  `python run.py fetch`

5. Download URLs
  `./download.sh`

Output will be in `result/<date>`. This also contains a copy of the URLs file.
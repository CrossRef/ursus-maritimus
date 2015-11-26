import itertools
import sys
from habanero import Crossref

cr = Crossref()

SEARCH_TERM = "ursus maritimus"
LICENSES_FILE = "licenses.txt"
URLS_FILE = "urls.txt"
CONTENT_TYPES = set(['text/plain', 'unspecified'])

def search(offset=0, limit=200):
  query = cr.works(query=SEARCH_TERM, filter={"has_full_text": True, "has_license":True})
  return query

def get_agreed_licenses():
  "Fetch the list of licenses that have been agreed to in licenses file."
  licenses = []
  try:
    with open(LICENSES_FILE, "r") as licenses_file:
      licenses = [license.strip() for license in licenses_file.readlines()]
  except IOError:
    # Ignore if file doesn't exist.
    pass
  return set(licenses)


def update_licenses_for_query():
  "Update the licenses file with the licenses that apply to the works retrieved by the query."
  query = search()
  all_licenses_all_items = [[license['URL'] for license in item['license']] for item in query.items()]

  distinct_licenses = set(itertools.chain.from_iterable(all_licenses_all_items))

  # Merge with already agreed licenses and update file.
  already_agreed_licenses = get_agreed_licenses()

  all_licenses = already_agreed_licenses.union(distinct_licenses)

  with open(LICENSES_FILE, "w") as licenses_file:
    for license in all_licenses:
      licenses_file.write(license)
      licenses_file.write("\n")

def fetch_urls_for_query():
  "Retrieve the urls of works that conform to the query and have the right license, store in urls file."
  agreed_licenses = get_agreed_licenses()

  with open(URLS_FILE, "w") as urls_file:
    
    query = search()
    
    page_size = query.items_per_page()
    pages = xrange(0, query.total_results(), page_size)

    for offset in pages:
      print("Fetch offset %d, items %d" % (offset,  page_size))
      query = search(offset=offset, limit=page_size)


      for work in query.items():
        doi = work['DOI']
        licenses = set([license['URL'] for license in work['license']])
        
        if licenses.intersection(agreed_licenses):
          urls =  [link['URL'] for link in work['link'] if link['content-type'] in CONTENT_TYPES]

          if len(urls) == 0:
            available_content_types =  [link['content-type'] for link in work['link']]            
            print "Couldn't find any suitable content types for %s only found %s" % (doi, available_content_types)

          for url in urls:
            urls_file.write(url)
            urls_file.write("\n")
         
        else:
          print("License not allowed for " + doi + " : " + licenses)



def main(commands):
  if len(commands) != 1:
    print("Please run with 'licenses' or 'fetch' argument")
    exit()

  command = commands[0]

  if command == "licenses":
    update_licenses_for_query()
  elif command == "fetch":
    fetch_urls_for_query()
  else:
    print("Please run with 'licenses' or 'fetch' argument")

if __name__ == "__main__":
    main(sys.argv[1:])
"""Pull data from https://www.congress.gov/members and build a graph
   linking bills to sponsors / co-sponsers. Write this out as an xml file
   to be interpreted elsewhere
"""

import os
import sys
from bs4 import BeautifulSoup

#file = open("members", "r")
#html_doc = file.read()

soup = BeautifulSoup(open("members"), 'html.parser')

# collect all the representatives + urls
house = soup.find(id="members-representatives")

# collect all the senators + urls
senate = soup.find(id="members-senators")
for s in senate.find_all("option"):
    senator_name = s.string
    senator_url = s['value']

    print senator_name
    print senator_url

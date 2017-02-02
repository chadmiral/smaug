"""
Pull data from the web about our congress and write it to a format
we can interpret and visualize elsewhere
"""

import os
import sys
import json

propublica_url = "https://api.propublica.org/congress/v1/"
data_path = "data/"
current_congress = 115

# retrieve api key from text file
def get_api_key():
    f = open("propublica_key.txt", "r")
    key = f.read()
    return key

def get_senate_nominations(api_key):
    cmd_line = "curl \"" + propublica_url
    cmd_line += str(current_congress)
    cmd_line += "/nominations.json\" -H \"X-API-Key: " + api_key + "\""
    cmd_line += " > " + data_path + "/" + str(current_congress) + "/senate_nominations.json"

    print cmd_line
    os.system(cmd_line)

def get_chamber_data(api_key, chamber):

    # retrieve list of all representatives in JSON format
    base_cmd_line = "curl \"" + propublica_url
    base_cmd_line += str(current_congress)
    base_cmd_line += "/" + chamber

    suffix = " -H \"X-API-Key: " + api_key + "\""

    members_cmd_line = base_cmd_line + "/members.json\" " + suffix
    members_cmd_line += " > " + data_path + str(current_congress) + "/" + chamber + ".json"
    print members_cmd_line
    os.system(members_cmd_line)

    bills_cmd_line = base_cmd_line + "/bills/introduced.json\" " + suffix
    bills_cmd_line += " > " + data_path + str(current_congress) + "/" + chamber + "/bills_new.json"
    print bills_cmd_line
    os.system(bills_cmd_line)

def get_individual_bills(api_key, chamber):
    f = open("data/" + str(current_congress) + "/" + chamber + "/bills_new.json")
    json_data = json.loads(f.read())
    #print json_data['results'][0]['bills'][0]['title']

    for bill in json_data['results'][0]['bills']:
        cmd_line = "curl \"" + bill['bill_uri']
        cmd_line += "\" -H \"X-API-Key: " + api_key + "\""
        cmd_line += " > data/" + str(current_congress) + "/" + chamber + "/bills/" + bill['number'] + ".json"

        #pulls bill data
        print cmd_line
        os.system(cmd_line)

        #get cosponsors via another query
        url = os.path.splitext(bill['bill_uri'])[0] #chop off ".json"
        cmd_line = "curl \"" + url + "/cosponsors.json"
        cmd_line += "\" -H \"X-API-Key: " + api_key + "\""
        cmd_line += " > data/" + str(current_congress) + "/" + chamber + "/bills/" + bill['number'] + "_sponsors.json"
        print cmd_line
        os.system(cmd_line)

def get_committees(api_key, chamber):
    #curl "https://api.propublica.org/congress/v1/113/house/committees.json"
  #-H "X-API-Key: PROPUBLICA_API_KEY"
  cmd_line = "curl \"" + propublica_url
  cmd_line += str(current_congress)
  cmd_line += "/" + chamber + "/"
  cmd_line += "committees.json\" -H \"X-API-Key: " + api_key + "\""
  cmd_line += " > " + data_path + str(current_congress) + "/" + chamber
  cmd_line += "/committees.json"

  print cmd_line
  os.system(cmd_line)

def main():
    api_key = get_api_key()
    get_chamber_data(api_key, "house")
    get_chamber_data(api_key, "senate")
    get_senate_nominations(api_key)
    get_individual_bills(api_key, "house")
    get_individual_bills(api_key, "senate")
    get_committees(api_key, "house")
    get_committees(api_key, "senate")

main()






"""BeautifulSoup version
import urllib
from bs4 import BeautifulSoup



def retrieve_senator(name, url):
    print name
    fname = "temp_senator.html"
    os.system("wget " + url + " -O " + fname)
    senator = BeautifulSoup(open(fname), 'html.parser')
    #for b in senator.find()
    #print url


# retrieve html from congress website
# for some reason this triggers the server to put up an "access denied" page
#urllib.urlretrieve ("https://www.congress.gov/members", "members.html")
os.system("wget https://www.congress.gov/members -O temp.html")

soup = BeautifulSoup(open("temp.html"), 'html.parser')

# collect all the representatives + urls
house = soup.find(id="members-representatives")

# collect all the senators + urls
senate = soup.find(id="members-senators")
for s in senate.find_all("option"):
    #TODO: filter out inactive senators
    print s['']
    retrieve_senator(s.string, s['value'])
"""

"""
Pull data from the web about our congress and write it to a format
we can interpret and visualize elsewhere
"""

import os
import sys
import json
import requests

Propublica_url = "https://api.propublica.org/"
Congress_url = "congress/v1/"
Finance_url = "campaign-finance/v1/"
data_path = "data/"
curl_options = " --create-dirs -o "
current_congress = 115

Congress_api_key = ""
Finance_api_key = ""

# retrieve api key from text file
def load_api_key(fname):
    f = open(fname, "r")
    key = f.readline()
    return key.strip()

def build_curl_command(url, options, outfile, api_key):
    cmd_line = "curl \"" + url
    cmd_line += "\" -H \"X-API-Key: " + api_key
    cmd_line += "\"" + options + outfile
    return cmd_line

def build_congress_url(suffix):
    return (Propublica_url + Congress_url + str(current_congress) + suffix)

def build_finance_url(year, suffix):
    url = Propublica_url + Finance_url + str(year) + suffix
    #url += "/candidates/search.json?query=" + candidate_name
    return url

def get_senate_nominations():
    outfile = data_path + str(current_congress) + "/senate_nominations.json"
    url = build_congress_url("/nominations.json")
    cmd_line = build_curl_command(url, curl_options, outfile, Congress_api_key)

    print(cmd_line)
    os.system(cmd_line)

def get_chamber_members(chamber):
    url = build_congress_url("/" + chamber + "/members.json")

    h = { 'X-API-KEY' : Congress_api_key }
    r = requests.get(url, headers=h)
    return r.json()

def get_chamber_data(chamber):

    # retrieve list of all representatives in JSON format
    base_cmd_line = "curl \"" + Propublica_url + Congress_url
    base_cmd_line += str(current_congress)
    base_cmd_line += "/" + chamber

    suffix = " -H \"X-API-Key: " + Congress_api_key + "\""

    members_cmd_line = base_cmd_line + "/members.json\" " + suffix

    target_filename = data_path + str(current_congress) + "/" + chamber + ".json"

    members_cmd_line += curl_options + target_filename#+ data_path + str(current_congress) + "/" + chamber + ".json"
    print(members_cmd_line)
    os.system(members_cmd_line)

    bills_cmd_line = base_cmd_line + "/bills/introduced.json\" " + suffix
    bills_cmd_line += curl_options + data_path + str(current_congress) + "/" + chamber + "/bills_new.json"
    print(bills_cmd_line)
    os.system(bills_cmd_line)

def get_member_details(chamber, json_data):
    target_data_path = data_path + str(current_congress) + "/" + chamber + "/members/"

    for p in json_data['results'][0]['members']:
        url = Propublica_url + Congress_url + "members/" + p['id'] + ".json"
        out_file = target_data_path + p['id'] + ".json"
        cmd_line = build_curl_command(url, curl_options, out_file, Congress_api_key)
        print(cmd_line)
        os.system(cmd_line)

def get_most_recent_bill_number(chamber):
    url = build_congress_url("/" + chamber + "/bills/introduced.json")

    h = { 'X-API-KEY' : Congress_api_key }
    r = requests.get(url, headers=h)

    max_bill_num = 0
    for b in r.json()['results'][0]['bills']:
        max_bill_num = max(max_bill_num, int(b['number'].split('.')[-1]))

    return max_bill_num


def get_bill_range(chamber, lo, hi):
    chamber_prefix = { 'house' : 'hr', 'senate' : 's' }

    for bill_number in range(lo, hi + 1):
        bill_number_name = chamber_prefix[chamber] + str(bill_number)
        url = build_congress_url("/bills/" + bill_number_name + ".json")
        outfile = data_path + str(current_congress) + "/" + chamber + "/bills/" + bill_number_name + ".json"
        cmd_line = build_curl_command(url, curl_options, outfile, Congress_api_key)
        print(cmd_line)
        os.system(cmd_line)

def get_individual_bills(chamber):
    f = open("data/" + str(current_congress) + "/" + chamber + "/bills_new.json")
    json_data = json.loads(f.read())
    #print json_data['results'][0]['bills'][0]['title']

    for bill in json_data['results'][0]['bills']:
        cmd_line = "curl \"" + bill['bill_uri']
        cmd_line += "\" -H \"X-API-Key: " + Congress_api_key + "\""
        cmd_line += curl_options + data_path + str(current_congress) + "/" + chamber + "/bills/" + bill['number'] + ".json"

        #pulls bill data
        print(cmd_line)
        os.system(cmd_line)

        #get cosponsors via another query
        url = os.path.splitext(bill['bill_uri'])[0] #chop off ".json"
        cmd_line = "curl \"" + url + "/cosponsors.json"
        cmd_line += "\" -H \"X-API-Key: " + Congress_api_key + "\""

        target_filename = data_path + str(current_congress) + "/" + chamber + "/bills/" + bill['number'] + "_sponsors.json"
        cmd_line += curl_options + target_filename
        print(cmd_line)
        os.system(cmd_line)

def get_committees(chamber):
  cmd_line = "curl \"" + Propublica_url + Congress_url
  cmd_line += str(current_congress)
  cmd_line += "/" + chamber + "/"
  cmd_line += "committees.json\" -H \"X-API-Key: " + Congress_api_key + "\""

  target_filename = data_path + str(current_congress) + "/" + chamber + "/committees.json"
  cmd_line += curl_options + target_filename

  print(cmd_line)
  os.system(cmd_line)

def get_finance_data_by_state(state, year):
    outfile = state + "_" + str(year) + "_finance.json"
    url = build_finance_url(year, "/races/" + state + ".json")
    cmd_line = build_curl_command(url, curl_options, outfile, Finance_api_key)

    print(cmd_line)
    os.system(cmd_line)

#def get_state_by_candidate(last_name, first_name):

#def get_finance_data_by_name(last_name, first_name, year):
    #first, determine the state

#def get_fec_id_by_name(last_name, first_name):
    #name -> state -> query finance data by state

def main():
    global Congress_api_key
    global Finance_api_key
    Congress_api_key = load_api_key("congress_key.txt")
    Finance_api_key = load_api_key("finance_key.txt")

    global House_members
    global Senate_members
    #House_members = get_chamber_members("house")
    #Senate_members = get_chamber_members("senate")

    get_most_recent_bill_number("house")

    #get_chamber_data("house")
    #get_chamber_data("senate")
    #get_senate_nominations()
    #get_individual_bills("house")
    #get_individual_bills("senate")
    #get_committees("house")
    #get_committees("senate")
    #get_member_details("house", House_members)
    #get_member_details("senate", Senate_members)

    #get_finance_data_by_state("WI", 2014)

    latest_house_bill = get_most_recent_bill_number("house")
    get_bill_range("house", latest_house_bill - 40, latest_house_bill)
    latest_senate_bill = get_most_recent_bill_number("senate")
    get_bill_range("senate", latest_senate_bill - 40, latest_senate_bill)

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

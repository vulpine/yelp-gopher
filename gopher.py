#!/usr/bin/python

# YelpGopher - Hackathon 14.0
# Lawrence Matthews, 24/07/2014

import socket
import SocketServer
import string

import yelp

GOPHER_PORT = 70
CRLF = "\r\n"
hostname = "localhost"


countries = {
  'UK': {
    'london': 'London',
    'bristol': 'Bristol',
  },
  'USA': {
    'sf': 'San Francisco',
    'nyc': 'New York',
  },
  'Germany': {
    'berlin': 'Berlin',
    'munich': 'Munich',
  }
}

def country_list():
  return countries.keys()

def city_list():
  cities = dict()
  for country, local_cities in countries.items():
    for city, name in local_cities.items():
      cities[city] = name
  return cities

def lookup_city(directory):
  # There should be a more clever way of looking this up.
  return city_list()[directory]

def build_gopher_link(itemtype, name, target, host=hostname, port=GOPHER_PORT):
  link = "{0}{1}\t{2}\t{3}\t{4}{5}".format(itemtype,name,target,host,port,CRLF)
  return link

def show_directory_listing(directory):
  city = lookup_city(directory)
  response  = build_gopher_link("i","Welcome to Yelp!","","error.host","1")
  response += build_gopher_link("i","This is Yelp {0}".format(city),"","error.host","1")
  response += build_gopher_link("7","Search Yelp {0}".format(city),"/{0}/search".format(directory))
  response += build_gopher_link("i","Other Yelps:","","error.host","1")
  for key in city_list():
    response += build_gopher_link("1","Yelp {0}".format(city_list()[key]),"/{0}".format(key))
  response += build_gopher_link("h","About Yelp (HTTP)","URL:http://www.yelp.com/about","www.yelp.com","80")
  return response

class GopherTCPHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    # Listen for comms
    request = self.request.recv(1024).rstrip()
    request = string.lower(request)

    response = ""

    if request == "" or request == ("/"):
      # We default to SF
      response = show_directory_listing("sf")
    else:
      # Some other city
      request = request.rstrip()
      split_request = request.split('/')
      city = split_request[1]
      response = show_directory_listing(city)
      # Regrettably, we must handle two different delimiters for search terms
      if len(split_request) == 3:
        if "?" in split_request[2]:
          search_terms = split_request[2].split('?')[1]
        if "\t" in split_request[2]:
          search_terms = split_request[2].split('\t')[1]
        results_json = yelp.yelp_search(search_terms, city)
        response = yelp.render_results(results_json)
    print response
    self.request.sendall(response.encode("utf-8"))

def start_server():
  server = SocketServer.TCPServer(("", GOPHER_PORT), GopherTCPHandler)
  server.serve_forever()

print "YelpGopher listening on {0} port {1}".format(hostname, GOPHER_PORT)
start_server()

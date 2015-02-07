#!/usr/bin/python

# YelpGopher - Hackathon 14.0
# Lawrence Matthews, 24/07/2014
#
# Methods for querying the Yelp v2 API.
#
# Some of this liberally borrowed from the sample code
# available at https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py

import json
import sys
import urllib
import urllib2

import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search'
LORD_BUSINESS_PATH = '/v2/business'
DEBUG = True

# This is my API key. There are many others like it...
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
TOKEN = ''
TOKEN_SECRET = ''
OAUTH_SIGNATURE_METHOD = 'hmac-sha1'

def yelp_request(host, path, url_params=None):
    """Query the v2 API.

    Args:
      host (str): The domain host of the API.
      path (str): The path of the API after the domain.
      url_params (dict): The parameters of the request. 
    Returns:
      dict: The JSON response from the request.
    """

    url_params = url_params or {}
    if DEBUG:
      sys.stderr.write('DEBUG: URL parameters are {0}\n'.format(url_params))
    encoded_params = urllib.urlencode(url_params)

    url = 'http://{0}{1}?{2}'.format(host, path, encoded_params)

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    if DEBUG:
      sys.stderr.write('DEBUG: Querying {0}...\n'.format(url))

    try:
      conn = urllib2.urlopen(signed_url, None)
    except urllib2.HTTPError, error:
        print "HTTP Error occurred: ", error.read()
        sys.exit(1)
    response = json.loads(conn.read())
    conn.close()

    return response

def yelp_search(term, location):
    """Query the Search API by a search term and location.

    Args:
      term (str): The search term passed to the API.
      location (str): The search location passed to the API.

    Returns:
      dict: The JSON response from the request.
    """
    url_params = {
        'term': term,
        'location': location,
        'limit': SEARCH_LIMIT,
        'fmode': '1',
    }

    return yelp_request(API_HOST, SEARCH_PATH, url_params=url_params)

def format_results(results):
    """Return a nicely-formatted set of search results.

    Args:
      results (dict): The business for which we want information about.

    Returns:
      formatted_results (str): The results, formatted with labels.
    """
    is_claimed = results['is_claimed']
    name =  results['name']
    rating = results['rating']
    url = results['url']
    is_open = False if results['is_closed'] == "False" else True
    phone  = results.get('display_phone',"None available")
    if 'snippet_text' in results:
      snippet_text  = results['snippet_text']
    else:
      snippet_text  = "No review snippet available."
    location  = results['location']
    city = location['city']
    address = ', '.join(location['display_address'])
    postcode = location['postal_code']
    country = location['country_code']

    formatted_results = ""
    formatted_results += u"iName: {0}\t\terror.host\t1\n".format(name)
    formatted_results += "iRating: {0}\t\terror.host\t1\n".format(rating)
    formatted_results += "iPhone: {0}\t\terror.host\t1\n".format(phone)
    formatted_results += u"iAddress: {0}\t\terror.host\t1\n".format(address)
    formatted_results += u"iReview: {0}\t\terror.host\t1\n".format(snippet_text)
    formatted_results += "iOpen: {0}\t\terror.host\t1\n".format(is_open)
    formatted_results += "i \t\terror.host\t1\n"
    return formatted_results

def render_results(json):
    output = ""
    for business in json['businesses']:
      output += format_results(business)
    return output

if __name__ == "__main__":
  sys.exit(0)

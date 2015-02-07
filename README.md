yelp-gopher
===========

This is a Gopher server which will let you search for businesses using the Yelp API (http://www.yelp.com/developers). It's written in Python, primarily as an exercise in learning Python, and as a good excuse to play around with Yelp's API for Hackathon.


Getting started
===============

Put your API keys in yelp.py:

    # This is my API key. There are many others like it...
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    TOKEN = ''
    TOKEN_SECRET = ''

Start the server by running gopher.py as superuser. If it succeeds, it will output:
    YelpGopher listening on localhost port 70

You can then go to gopher://localhost:70 and you should see a Gophersite load.


Using the server
================

Choose the city you wish to search by choosing the link from the Gophersite, or by browsing to gopher://SERVER/1/CITY. Server will be the hostname the server is running on, and city is defined in gopher.py:

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

To get to New York, visit gopher://SERVER/1/nyc. (Feel free to add your own preferred cities here to customise your YelpGopher experience.)

Enter search terms into the search element ("Search Yelp New York") and YelpGopher will query the API and return the top three results.


Contact
=======

Email me at lmatthew@yelp.com or find me on Twitter as @lejmatthews. Patches always welcome!

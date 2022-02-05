"""pings the endpoint to run the data scraper"""
import requests

requests.get('https://car-park-when-sg.herokuapp.com/data/scrape/')

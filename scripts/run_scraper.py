"""pings the endpoint to run the data scraper"""
import requests
import os
import dotenv

dotenv.load_dotenv()
requests.post(os.environ.get("SCRAPER_ENDPOINT"))

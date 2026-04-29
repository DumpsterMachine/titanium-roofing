import json
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# This script assumes 'service-account.json' is present in the titanium-roofing directory.
def ping_url(url):
    try:
        # In a real environment, you need the service account JSON key file at this path.
        if not os.path.exists('/Users/mattai/.openclaw/workspace/titanium-roofing/service-account.json'):
            return "Service Account JSON file missing. Please add it to your titanium-roofing directory."
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            '/Users/mattai/.openclaw/workspace/titanium-roofing/service-account.json', 
            ['https://www.googleapis.com/auth/indexing']
        )
        
        # Build the service
        http = creds.authorize(httplib2.Http())
        service = googleapiclient.discovery.build('indexing', 'v3', http=http)
        
        # Send the ping
        body = {'url': url, 'type': 'URL_UPDATED'}
        response = service.urlNotifications().publish(body=body).execute()
        return response
    except Exception as e:
        return str(e)

import os
# We will ping the root and the locations index as a proof of concept.
urls_to_ping = [
    "https://www.titaniumroofingllc.com/",
    "https://www.titaniumroofingllc.com/locations",
    "https://www.titaniumroofingllc.com/locations/riverview"
]

for url in urls_to_ping:
    print(f"Pinging {url}: {ping_url(url)}")

import requests
from time import sleep
#from requests.exceptions import HTTPError
#from requests.exceptions import JSONDecodeError
#from requests.exceptions import ConnectionError

URL = "https://api.mg-rast.org/metadata/export/mgp385"
#URL = "https://www.google.com/search?q=london"
#response = ses.get("https://api.mg-rast.org/1/profile/mgm4472361.3?source=RefSeq")

class Data_pull:
    
    def __init__(self):
        self.response = None
        self.pulled_data = None

    def pull_study_metadata(self, url):
        self.url = url
        try:
            #ses = requests.session()
            with requests.session() as ses:
                try:
                    self.response = ses.get(self.url, timeout=120)
                except requests.exceptions.Timeout as e:
                    print(f"TimeoutError: The connection timed out \n {e} \n")
                    raise
        
            if self.response.status_code == requests.codes.ok:
                print(f"Good request for url: {self.url}.\n")
        
            try:
                self.response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"HTTPError: {self.response.text} \n {e} \n")
                raise
                #raise HTTPError(e, response.text)
    
            try:
                self.pulled_data = self.response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"JSONDecodeError: The file must be JSON. \n {e} \n")
                raise
        
   
        except requests.exceptions.ConnectionError as e:
        #except requests.exceptions.ConnectionError:
            #time.sleep(5)
            #continue
            print(f"ConnectionError: Connection refused, try it again later. \n {e} \n")
            raise
            #raise requests.exceptions.ConnectionError(e, "Connection refused")
            #response.status_code = "Connection refused"
        return self.pulled_data

data_pull = Data_pull() 
#meta_data = data_pull.pull_study_metadata("https://api.mg-rast.org/metadata/export/mgp385")
#meta_data = data_pull.pull_study_metadata("https://api.mg-rast.org/metadata/view/env_package")
meta_data = data_pull.pull_study_metadata("https://api.mg-rast.org/project?limit=20&order=id&verbosity=full")

#print(type(meta_data.keys))
#print(meta_data.keys())
print(meta_data)

'''
In case the JSON decoding fails, r.json() raises an exception. For example, if 
the response gets a 204 (No Content), or if the response contains invalid JSON, 
attempting r.json() raises requests.exceptions.JSONDecodeError.
'''


'''
raceback (most recent call last):
  File "<stdin>", line 1, in <module>
requests.exceptions.Timeout: HTTPConnectionPool(host='github.com', port=80): 
Request timed out. (timeout=0.001)
'''

'''
Errors and Exceptions
In the event of a network problem (e.g. DNS failure, refused connection, etc), 
Requests will raise a ConnectionError exception.

Response.raise_for_status() will raise an HTTPError if the HTTP request returned 
an unsuccessful status code.

If a request times out, a Timeout exception is raised.

If a request exceeds the configured number of maximum redirections,
 a TooManyRedirects exception is raised.

All exceptions that Requests explicitly raises inherit from 
requests.exceptions.RequestException.
'''

#print(response.json())
#response.text
#print(type(response.text))
#print(response.text)
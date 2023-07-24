#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 08:12:08 2023

@author: adamveszpremi
"""

import requests
from requests.adapters import HTTPAdapter, Retry ###

'''
This class is used to pull data from the MG-RAST API using an URL. 
It also raises errors if something goes wrong.
'''
class Connector:
    
    def __init__(self):
        self.response = None
        self.retry = None
        self.adapter = None
        self.pulled_data = None
    
    def set_adapter(self, assign):
        self.adapter = assign
    
    def set_retry(self, assign):
        self.retry = assign
    
    def pull_data(self, url):
        self.url = url
        try:
            with requests.session() as ses:
                try:
                    self.set_retry(Retry(connect = 3, backoff_factor = 1)) ###
                    self.set_adapter(HTTPAdapter(max_retries = self.retry)) ###
                    ses.mount('http://', self.adapter) ###
                    ses.mount('https://', self.adapter) ###
                    self.response = ses.get(self.url, timeout=300)
                except requests.exceptions.Timeout as e:
                    print(f"TimeoutError: The connection timed out \n {e} \n")
                    raise
        
            if self.response.status_code == requests.codes.ok:
                print(f"Successful request for the following URL:\n{self.url}.")
        
            try:
                self.response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"HTTPError: {self.response.text} \n {e} \n")
                raise
    
            try:
                self.pulled_data = self.response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"JSONDecodeError: The file must be a complete JSON. Try it again. \n {e} \n")
                raise
        
   
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError: Connection refused, try it again later. \n {e} \n")
            raise

        return self.pulled_data

'''

SSLEOFError: EOF occurred in violation of protocol (_ssl.c:1129)

MaxRetryError: HTTPSConnectionPool(host='api.mg-rast.org', port=443): 
Max retries exceeded with url: /metadata/view/seq_meth (Caused by 
SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))

SSLError: HTTPSConnectionPool(host='api.mg-rast.org', port=443):
Max retries exceeded with url: /metadata/view/seq_meth (Caused by 
SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))
'''

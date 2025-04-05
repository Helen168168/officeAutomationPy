'''
    封装requests库
'''

import requests
import logging
import json

class Request:
    def __init__(self, url='', method='GET',  headers=None, data=None, params=None, timeout=1000):
        self.url = url
        self.method = method
        self.headers = headers if headers else {}
        self.data = data
        self.params = params
        self.timeout = timeout

    def send(self):
        try:
            if self.method == 'GET':
                response = requests.get(self.url, headers=self.headers, params=self.params, timeout=self.timeout)
            elif self.method == 'POST':
                response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data), timeout=self.timeout)
            elif self.method == 'PATCH':
                response = requests.patch(self.url, headers=self.headers, data=json.dumps(self.data), timeout=self.timeout)
            elif self.method == 'PUT':
                response = requests.put(self.url, headers=self.headers, data=json.dumps(self.data),
                                        timeout=self.timeout)
            elif self.method == 'DELETE':
                response = requests.delete(self.url, headers=self.headers, timeout=self.timeout)
            else:
                raise ValueError("Unsupported HTTP method: {}".format(self.method))

            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return e
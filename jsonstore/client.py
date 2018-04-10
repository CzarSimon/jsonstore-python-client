import json
import requests
from requests.exceptions import RequestException


DEFAULT_TIMEOUT_SECONDS = 5


class JsonstoreError(Exception):
    '''Exception for errors occuring in calls to Jsonstore'''
    pass


class Client(object):
    '''Http client for the www.jsonstore.io API

    Attributes:
        __base_url Base url for jsonstore, inculding a user token.
        __headers  Request headers to include in all requests to jsonstore.
    '''
    def __init__(self, token):
        self.__base_url = f'https://www.jsonstore.io/{token}'
        self.__headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }

    def get(self, key, timeout=DEFAULT_TIMEOUT_SECONDS):
        '''Get gets value from jsonstore.

        :param key: Name of key to a resource
        :param timeout: Timeout of the request in seconds
        :return: Response result as a dictionary
        '''
        url = self.__create_url(key)
        try:
            resp = requests.get(url, headers=self.__headers)
            json_resp = self.__check_response(resp)
            return json_resp['result']
        except (RequestException, ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    def post(self, key, data, timeout=DEFAULT_TIMEOUT_SECONDS):
        '''Saves data in jsonstore under a key.

        :param key: Name of key to a resource
        :param data: Data to store in jsonstore
        :param timeout: Timeout of the request in seconds
        '''
        url = self.__create_url(key)
        json_data = json.dumps(data)
        try:
            resp = requests.post(url, data=json_data,
                                 headers=self.__headers, timeout=timeout)
            self.__check_response(resp)
        except (RequestException, ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    def put(self, key, data, timeout=DEFAULT_TIMEOUT_SECONDS):
        '''Updates data in jsonstore under a key.

        :param key: Name of key to a resource
        :param data: Updated data in jsonstore
        :param timeout: Timeout of the request in seconds
        '''
        url = self.__create_url(key)
        json_data = json.dumps(data)
        try:
            resp = requests.put(url, data=json_data,
                                headers=self.__headers, timeout=timeout)
            self.__check_response(resp)
        except (RequestException, ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    def delete(self, key, timeout=DEFAULT_TIMEOUT_SECONDS):
        '''Deletes data in jsonstore under a key.

        :param key: Name of key to a resource
        :param timeout: Timeout of the request in seconds
        '''
        url = self.__create_url(key)
        try:
            resp = requests.delete(url, headers=self.__headers,
                                   timeout=timeout)
            self.__check_response(resp)
        except (RequestException, ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    def __check_response(self, response):
        '''Checks if a response is successfull raises a JsonstoreError if not.

        :param response: Response to check
        :return: Desarialized json response
        '''
        if not isinstance(response, requests.Response):
            raise TypeError('Unexpected type {}'.format(type(response)))
        response.raise_for_status()
        resp = response.json()
        if 'ok' not in resp or not resp['ok']:
            raise JsonstoreError('Call to jsonstore failed')
        return resp

    def __create_url(self, key):
        '''Creates url for a given key.

        :param key: Key to append to the base url
        :return: URL to resource
        '''
        return '{}/{}'.format(self.__base_url, key)

from BeautifulSoup import BeautifulSoup
import urllib3
import json
import requests

class WebserviceTools:

    def __init__(self):
        self.soup = None
        return

    def getPageAsBeautifulSoup(self, url):
        req = urllib3.PoolManager()
        resp = req.request('GET', url)
        self.soup = BeautifulSoup(resp.data)
        return self.soup

    def getJsonResponse(self, url, params):
        """
        THROWS AN EXCEPTION IF THE RESPONSE WE GET BACK IS NOT JSON!
        :param url: The url before the ? in an API
        :param params: A dictionary representing the parameters in an API request
        :return: the response from the server in JSON format.
        """
        response = requests.get(url, params=params)
        return response.json()

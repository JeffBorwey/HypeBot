from BeautifulSoup import BeautifulSoup
import urllib3

class BeautifulSoupUtils:

    def __init__(self):
        self.soup = None
        return

    def getPage(self, url):
        req = urllib3.PoolManager()
        resp = req.request('GET', url)
        self.soup = BeautifulSoup(resp.data)
        return self.soup


import requests 
from bs4 import BeautifulSoup




class TTP:
    def __init__(self, src_url, prefix=''):
        self.src_url = src_url 
        self.prefix = prefix
        self.urls=[]


    def scrape(self):
        r = requests.get(self.src_url)
        soup = BeautifulSoup(r.content, "html.parser")

        for chunk in soup.find_all("ul", {"class":"toc chapters"}):
            for link in chunk.find_all("li"):
                if(link.a):
                    self.urls.append(self.prefix+link.a.get("href"))

        return self.urls


class JTP:
    def __init__(self, src_url, prefix=''):
        self.src_url = src_url 
        self.prefix = prefix
        self.urls=[]


    def scrape(self):
        r = requests.get(self.src_url)
        soup = BeautifulSoup(r.content, "html.parser")

        for chunk in soup.find_all("div", {"class":"leftmenu"}):
            for link in chunk.find_all("a"):
                self.urls.append(self.prefix+link.get("href"))

        return self.urls


class GFG:
    def __init__(self, src_url, prefix=''):
        self.src_url = src_url 
        self.prefix = prefix
        self.urls=[]


    def scrape(self):
        r = requests.get(self.src_url)
        soup = BeautifulSoup(r.content, "html.parser")

        for chunk in soup.find_all("ol"):
            for link in chunk.find_all("li"):
                self.urls.append(self.prefix+link.a.get("href"))

        return self.urls
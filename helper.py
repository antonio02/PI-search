import re

from requests import Session
import requests
from bs4 import BeautifulSoup


class Url:

    def __init__(self, url):
        self.url = url
        self.soup = None

    def inicializar(self):
        if self.soup is None:
            self.soup = BeautifulSoup(requests.get(self.url, timeout= 1).text, 'html.parser')

    def procurar_palavra(self, keyword):
        self.inicializar()

        body = self.soup.body

        # remove os javascript e css
        for script in body(["script", "style"]):
            script.decompose()

        encontradas = re.findall('\w*.{0,10}' + keyword + '.{0,10}\w*', body.text, re.IGNORECASE)

        return encontradas

    def pegar_links(self):
        self.inicializar()

        a = self.soup.find_all("a")
        links = []

        for link in a:
            try:
                if (str(link['href']).startswith("http")):
                    links.append(link["href"])
            except:
                pass

        return links


    def getUrl(self):
        return self.url



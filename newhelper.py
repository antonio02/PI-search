from bs4 import BeautifulSoup
from tornado import ioloop, curl_httpclient, httpclient
import re


class Url:

    def __init__(self, response, url:str):
        self.url = url
        self.soup = BeautifulSoup(response, 'html.parser')
        self.encontradas = None
        self.links = None
        self.last_keyword = None

    def procurar_palavra(self, keyword):


        if self.encontradas is not None and self.last_keyword == keyword:
            return self.encontradas

        self.last_keyword = keyword
        body = self.soup

        # remove os javascript e css
        for script in body(["script", "style"]):
            script.decompose()

        encontradas = re.findall('\w*.{0,10}' + keyword + '.{0,10}\w*', body.text, re.IGNORECASE)

        self.encontradas = encontradas

        return encontradas

    def pegar_links(self):

        if self.links is not None:
            return self.links

        a = self.soup.find_all("a")
        links = []

        for link in a:
            try:
                if (str(link['href']).startswith("http")):
                    links.append(link["href"])

                elif str(link['href']).startswith("/"):
                    new_link = self.url[0:len(self.url)-1]
                    new_link = new_link + link["href"]
                    links.append(new_link)

            except:
                pass

        self.links = links

        return links

    def getUrl(self):
        return self.url

class Camadas:

    def __init__(self, profundidade, url_inicial, finish_callback):

        self.finish_callback = finish_callback
        self.source_Url = re.findall("://[\w.]+/?", url_inicial)[0]
        self.profundidade = profundidade
        self.camadas = []
        self.salvas = []
        self.camada_atual = []
        self.links_atuais = []
        self.qtd_url_atual = 0
        self.profundidade_restante = profundidade
        self.start(url_inicial)

    def instanciar(self, response: httpclient.HTTPResponse):



        if response is not None:
            if response.code == 200:
                if response.body is not None:
                    self.camada_atual.append(Url(str(response.body), response.effective_url))

        self.qtd_url_atual -= 1
        if self.qtd_url_atual == 0:
            self.camadas.append(self.camada_atual.copy())
            self.camada_atual.clear()
            self.links_atuais.clear()

            if self.profundidade_restante != 0:
                self.continuar()
                self.profundidade_restante -= 1

            else:
                ioloop.IOLoop.instance().stop()
                self.finish_callback(self)


    def start(self, url_inicial):

        http_client = curl_httpclient.CurlAsyncHTTPClient()

        self.qtd_url_atual = 1
        self.salvas.append(url_inicial)
        http_client.fetch(url_inicial, self.instanciar, method='GET')

        ioloop.IOLoop.instance().start()

    def continuar(self):

        http_client = curl_httpclient.CurlAsyncHTTPClient()

        for lista in self.camadas[len(self.camadas) -1]:
            for url in lista.pegar_links():
                if url not in self.salvas and self.source_Url in url:
                    self.links_atuais.append(url)
                    self.salvas.append(url)

        self.qtd_url_atual = len(self.links_atuais)

        for link in self.links_atuais:
            http_client.fetch(httpclient.HTTPRequest(link, connect_timeout=5, request_timeout=5, method="GET"), self.instanciar)


    def get_camadas(self):

        return self.camadas

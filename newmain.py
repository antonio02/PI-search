from newhelper import Url, Camadas

def main():

    url = input("URL: ").strip()
    keyword = input("KEYWORD : ").strip()
    profundidade = int(input("PROFUNDIDADE: ").strip())
    finalizar = Finalizar(profundidade, keyword)
    camadas = Camadas(profundidade, url, finalizar.on_finish)



class Finalizar:

    def __init__(self, profundidade, keyword):
        self.profundidade = profundidade
        self.keyword = keyword

    def on_finish(self, camadas:Camadas):
        encontradas = camadas.get_camadas()[self.profundidade]

        ordenada = sorted(encontradas, key=lambda x:len(x.procurar_palavra(self.keyword)), reverse=True)

        print("\n----------------Resultados----------------")

        for url in ordenada:
            if len(url.procurar_palavra(self.keyword)) > 1:
                print(url.getUrl(), "\nQuantidade: ", len(url.procurar_palavra(self.keyword)), "\n")


if __name__ == '__main__':
    main()
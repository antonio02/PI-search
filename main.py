from helper import Url

import time


def main():
    url = Url("http://www.ifpi.edu.br/")

    keyword = input("KEYWORD : ")

    # camadas = int(input("Camada desejada: "))

    printar(explorador_camadas(url, 2), keyword)

    print("teste", len(url.pegar_links()))

    # for palavra in url.procurar_palavra(keyword):
    #     print(palavra)


def explorador_camadas(url, camada):
    profundidade = camada

    camadas = [[url]]

    exploradas = []

    # if profundidade == 0:
    # 	return camadas

    for i in range(0, profundidade):
        urls = []

        for url in camadas[i]:
            try:
                links = url.pegar_links()
                exploradas.append(url.getUrl())
                print(url.getUrl())

                for link in links:
                    if link not in exploradas:
                        new_link = Url(link)
                        urls.append(new_link)
                        exploradas.append(new_link.getUrl())

            except:
                print("deu erro")

        camadas.append(urls)

    return camadas


def printar(camadas, keyword):
    for i in range(len(camadas)):
        for url in camadas[i]:
            print(len(camadas[i]))
            try:
                pass
            # print(url.getUrl(), "\ncamada: ", i, " Quantidades encontradas: " , len(url.procurar_palavra(keyword)))
            except:
                print("erro na palavra")


if __name__ == '__main__':
    main()

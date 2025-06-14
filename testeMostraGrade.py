################################################################
###               M O S T R A   G R A D E                    ###
################################################################
### Neste teste, mostra uma garde centralizada na janela com ###
### N linhas e M colunas, permitindo a configuração da cor   ###
### de preenchimento da célula, bem como quais arestas       ###
### devem ser mostradas. Desta forma, pode-se "escavar"      ###
### caminhos entre as células.                               ###
################################################################
### Prof. Filipo Mor, FILIPOMOR.COM                          ###
################################################################

import pygame
import sys
from enum import Enum

class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita

class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corLinha):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corLinha = corLinha

    def corPreenchimento(self):
        return self.corPreenchimento

    def arestasFechadas(self):
        return self.arestasFechadas

    def desenhar(self, tela, x, y, aresta):
        # x : coluna
        # y : linha

        # calcula as posicoes de desenho das linhas de cada aresta
        arSuperiorIni = (x,y)
        arSuperiorFim = (x+aresta,y)
        arInferiorIni = (x,y+aresta)
        arInferiorFim = (x+aresta,y+aresta)
        arEsquerdaIni = (x,y)
        arEsquerdaFim = (x,y+aresta)
        arDireitaIni  = (x+aresta,y)
        arDireitaFim  = (x+aresta,y+aresta)

        # preenche a célula com a cor definida
        pygame.draw.rect(tela, self.corPreenchimento, (x,y,aresta,aresta))
        # linha superior
        if(self.arestasFechadas.superior):
            pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        # linha inferior
        if(self.arestasFechadas.inferior):
            pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        # linha esquerda
        if(self.arestasFechadas.esquerda):
            pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        # linha direita
        if(self.arestasFechadas.direita):
            pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)

###
### desenha uma malha (grade) na janela informada
###
def desenhar_grade(tela, x, y, aresta, qtLinhas, qtColunas, matriz):
    for linha in range(qtLinhas):
        for coluna in range(qtColunas):
            matriz[linha][coluna].desenhar(tela, x + coluna * aresta, y + linha * aresta, aresta)


def GeraMatriz(qtLinhas, qtColunas, valorPadrao):
    matriz = []
    for i in range(qtLinhas):
        linha = []
        for j in range(qtColunas):
            linha.append(valorPadrao)
        matriz.append(linha)
    return matriz


def main():
    pygame.init()

    ### definição das cores
    azul     = ( 50, 50,  255)
    preto    = (  0,   0,   0)
    branco   = (255, 255, 255)
    vermelho = (255,   0,   0)
    cinza    = (128, 128, 128)

    # Dimensões da janela
    [largura, altura] = [600, 300]

    ### Dimensões da malha (matriz NxM)
    N = 3  # número de linhas
    M = 3  # número de colunas
    aresta = 50 # dimensão dos lados das células

    celulaPadrao = Celula(ArestasFechadas(1,1,1,1), preto, vermelho)
    matriz = GeraMatriz(N, M, celulaPadrao)
    matriz[0][0] = Celula(ArestasFechadas(0,0,0,0), azul, branco)
    matriz[0][2] = Celula(ArestasFechadas(0, 0, 0, 0), cinza, azul)
    matriz[1][1] = Celula(ArestasFechadas(0, 0, 0, 0), azul, branco)
    matriz[1][0] = Celula(ArestasFechadas(0, 0, 0, 0), branco, vermelho)
    matriz[2][2] = Celula(ArestasFechadas(0, 0, 0, 0), azul, preto)

    # Cria a janela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Malha')

    ###
    ### Loop principal
    ###
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ### preenche a tela com a cor branca
        tela.fill(branco)

        ### centraliza a grade na janela
        [linha, coluna] = ((tela.get_width()  - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)
        desenhar_grade(tela, linha, coluna, aresta, N, M, matriz)

        ### atualiza a tela
        pygame.display.flip()


if __name__ == '__main__':
    main()
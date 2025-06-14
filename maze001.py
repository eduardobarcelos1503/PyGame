################################################################
###                 M O S T R A   M A Z E                    ###
################################################################
### Neste teste, mostra o labirinto gerado pelo algoritmo de ###
### Aldous-Broder                                            ###
################################################################
### Prof. Filipo Mor, FILIPOMOR.COM                          ###
################################################################

import pygame
import sys
import copy
import random
from random import randint


class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita


class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corVisitada, corLinha, corAberta, visitada, aberta):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corVisitada = corVisitada
        self.corLinha = corLinha
        self.corAberta = corAberta
        self.visited = visitada
        self.aberta = aberta

    def get_corPreenchimento(self):
        return self.corPreenchimento

    def get_arestasFechadas(self):
        return self.arestasFechadas

    def is_visited(self):
        return self.visited

    def desenhar(self, tela, x, y, aresta):
        # x : coluna
        # y : linha

        # calcula as posicoes de desenho das linhas de cada aresta
        arSuperiorIni = (x, y)
        arSuperiorFim = (x + aresta, y)
        arInferiorIni = (x, y + aresta)
        arInferiorFim = (x + aresta, y + aresta)
        arEsquerdaIni = (x, y)
        arEsquerdaFim = (x, y + aresta)
        arDireitaIni = (x + aresta, y)
        arDireitaFim = (x + aresta, y + aresta)

        # preenche a célula com a cor definida
        if (self.aberta):
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)

        '''
        # linha superior
        if (self.arestasFechadas.superior):
            pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        # linha inferior
        if (self.arestasFechadas.inferior):
            pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        # linha esquerda
        if (self.arestasFechadas.esquerda):
            pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        # linha direita
        if (self.arestasFechadas.direita):
            pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)
        '''
        '''
        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)
        '''


class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        # self.visitados = []

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while (encontrou == False):
            linhaVizinha = linhaCelulaAtual + randint(-1, 1)
            colunaVizinha = colunaCelulaAtual + randint(-1, 1)
            if (
                    linhaVizinha >= 0 and linhaVizinha < self.qtLinhas and colunaVizinha >= 0 and colunaVizinha < self.qtColunas):
                encontrou = True

        return linhaVizinha, colunaVizinha

    def GeraLabirinto(self):

        self.resetaLabirinto()

        unvisitedCells = self.qtLinhas * self.qtColunas
        currentCellLine, currentCellColumn, neighCellLine, neighCellColumn = -1, -1, -1, -1

        # sorteia uma célula qualquer
        currentCellLine = randint(0, self.qtLinhas - 1)
        currentCellColumn = randint(0, self.qtColunas - 1)

        while (unvisitedCells > 0):

            # Sorteia um vizinho qualquer da célula atual
            neighCellLine, neighCellColumn = self.SorteiaCelulaVizinha(currentCellLine, currentCellColumn)

            if (self.matriz[neighCellLine][neighCellColumn].visited == False):
                # incluir aqui a rotina paar abrir uma passagem. Por enquanto, apenas pinta a célula
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].visited = True
                '''
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].aberta     = True
                self.matriz[neighCellLine][neighCellColumn].visited    = True
                self.matriz[neighCellLine][neighCellColumn].corPreenchimento = (0, 255, 0)
                '''
                unvisitedCells -= 1
                # cont += 1

            currentCellLine, currentCellColumn = neighCellLine, neighCellColumn


class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value

    def __aslist__(self):
        return self.matriz

    def GeraMatriz(self):
        matriz = []
        for i in range(self.qtLinhas):
            linha = []
            for j in range(self.qtColunas):
                #newCell = copy.deepcopy(self.celulaPadrao)
                linha.append(copy.deepcopy(self.celulaPadrao))
            matriz.append(linha)
        return matriz

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)


def main():
    pygame.init()

    ### definição das cores
    azul = (50, 50, 255)
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    vermelho = (255, 0, 0)
    cinza = (128, 128, 128)

    # Dimensões da janela
    [largura, altura] = [600, 300]

    ### Dimensões da malha (matriz NxM)
    N = 20  # número de linhas
    M = 20  # número de colunas
    aresta = 10  # dimensão dos lados das células

    # cores: preenchimento - visitada - linha - aberta
    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, branco,False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()

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
        [linha, coluna] = ((tela.get_width() - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)
        # desenhar_grade(tela, linha, coluna, aresta, N, M, matriz)
        labirinto.matriz.DesenhaLabirinto(tela, linha, coluna)

        ### atualiza a tela
        pygame.display.flip()


if __name__ == '__main__':
    main()

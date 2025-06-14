import pygame
import sys


###
### desenha uma malha (grade) na janela informada
###
def desenhar_grade(tela, x, y, aresta, qtLinhas, qtColunas, corLinha, corPreenchimento):
    for linha in range(qtLinhas):
        for coluna in range(qtColunas):
            rect = pygame.Rect(x + coluna * aresta, y + linha * aresta, aresta, aresta)
            pygame.draw.rect(tela, corPreenchimento, rect)
            pygame.draw.rect(tela, corLinha, rect, 1)  # Desenha um retângulo com espessura de linha de 1 pixel



def main():
    pygame.init()

    ### definição das cores
    azul   = ( 50, 50,  255)
    preto  = (  0,   0,   0)
    branco = (255, 255, 255)

    # Dimensões da janela
    [largura, altura] = [600, 300]

    ### Dimensões da malha (matriz NxM)
    N = 3  # número de linhas
    M = 3  # número de colunas
    aresta = 50 # dimensão dos lados das células

    # Cria a janela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Malha')

    # Loop principal do jogo
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ### preenche a tela com a cor branca
        tela.fill(branco)

        ### centraliza a grade na janela
        [x, y] = ((tela.get_width()  - (M * aresta)) // 2,
                  (tela.get_height() - (N * aresta)) // 2)
        desenhar_grade(tela, x, y, aresta, N, M, preto, azul)

        ### atualiza a tela
        pygame.display.flip()


if __name__ == '__main__':
    main()
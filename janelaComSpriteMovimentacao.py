###
### Exploracao da biblioteca PyGame
###
### Prof. Filipo Novo Mor
###
import pygame
import sys

# Inicializa o pygame
pygame.init()

# Define as dimensões da janela
largura, altura = 300, 200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Janela com Botão")

# Define as cores
branco = (255, 255, 255)
cinza = (200, 200, 200)
preto = (0, 0, 0)

# Carrega a sprite sheet do personagem
sprite_sheet = pygame.image.load("Attack.png").convert_alpha()
num_quadros = 8  # Número de quadros na sprite sheet

# Ajuste para os tamanhos corretos
quadro_largura = sprite_sheet.get_width() // num_quadros  # Largura de cada quadro
quadro_altura = sprite_sheet.get_height()  # Altura total da sprite sheet

# Extraí os quadros na linha correta
quadros = [sprite_sheet.subsurface((i * quadro_largura, 52, quadro_largura, quadro_altura - 52)) for i in range(num_quadros)]

# Função para desenhar o botão
def desenha_botao(tela, cor, pos, tamanho, texto):
    fonte = pygame.font.Font(None, 36)
    pygame.draw.rect(tela, cor, (pos[0], pos[1], tamanho[0], tamanho[1]))
    texto_surface = fonte.render(texto, True, preto)
    texto_rect = texto_surface.get_rect(center=(pos[0] + tamanho[0] // 2, pos[1] + tamanho[1] // 2))
    tela.blit(texto_surface, texto_rect)

# Dimensões do botão
largura_botao, altura_botao = 100, 50

# Posição do botão no canto inferior direito
x_botao = largura - largura_botao - 10
y_botao = altura - altura_botao - 10

# Variáveis de animação
indice_quadro = 0
tempo_animacao = 200  # Tempo a cada quadro em milissegundos (ajustável)
cronometro = 0
ultimo_tempo = pygame.time.get_ticks()

# Posição inicial do sprite
pos_x = 10  # Posição inicial do sprite no eixo X
pos_y = 10  # Posição inicial do sprite no eixo Y
movimento = 1  # Ajuste para que a movimentação seja mais suave

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao.collidepoint(evento.pos):
                rodando = False

    # Captura os eventos de tecla
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        pos_x += movimento  # Movimento para a direita
    if teclas[pygame.K_LEFT]:
        pos_x -= movimento  # Movimento para a esquerda

    # Mantém o sprite dentro da janela
    if pos_x < 0:
        pos_x = 0
    elif pos_x > largura - quadro_largura:
        pos_x = largura - quadro_largura

    # Calcula o tempo passado desde o último quadro
    agora = pygame.time.get_ticks()
    if agora - ultimo_tempo > tempo_animacao:
        indice_quadro = (indice_quadro + 1) % num_quadros
        ultimo_tempo = agora  # Atualiza o último tempo

    # Preenche o fundo de branco
    tela.fill(branco)

    # Desenha a animação do personagem na posição atual
    tela.blit(quadros[indice_quadro], (pos_x, pos_y))

    # Desenha o botão
    botao = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)
    desenha_botao(tela, cinza, botao.topleft, botao.size, "Sair")

    # Atualiza a tela
    pygame.display.flip()

# Encerra o pygame
pygame.quit()
sys.exit()

##########################################################
####        N A V I O    C A T A    M O E D A S       ####
##########################################################
#### Prof. Filipo Novo Mor - filipomor.com            ####
#### github.com\ProfessorFilipo                       ####
##########################################################
import pygame
import random
import sys

pygame.init()

# Sons
som_aviso = pygame.mixer.Sound(r"CatchTheCoin\Assets\Audio\notificacao.mp3")
som_beep = pygame.mixer.Sound(r"CatchTheCoin\Assets\Audio\beep.mp3")

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Navio Cata Moedas!!!")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
MOEDA_TAMANHO = (32, 32)

# Imagens
background_img = pygame.image.load(r'CatchTheCoin\Assets\PNG\ambiente3.png').convert()
background_img = pygame.transform.smoothscale(background_img, (800, 600))
barco_sprite_img = pygame.image.load(r'CatchTheCoin\Assets\PNG\boat01.png').convert_alpha()
barco_sprite_img = pygame.transform.smoothscale(barco_sprite_img, (64, 64))
sea_sprite = pygame.image.load(r'CatchTheCoin\Assets\PNG\chao.png').convert()
sea_sprite = pygame.transform.smoothscale(sea_sprite, (WIDTH, sea_sprite.get_height()))
sea_rect = sea_sprite.get_rect(topleft=(0, HEIGHT - sea_sprite.get_height()))

# Brocolis
brocolis_img = pygame.image.load(r'CatchTheCoin\Assets\Inimigos\brocolis.png').convert_alpha()
brocolis_img = pygame.transform.smoothscale(brocolis_img, (32, 32))

# Função para dificuldade
def configurar_dificuldade(nivel):
    if nivel == 1:
        return 5, 2, 3
    elif nivel == 2:
        return 5, 3, 4
    elif nivel == 3:
        return 5, 4, 6
    else:
        return 15, 2, 3

def load_animation_frames(prefix, total_frames=2, tamanho=MOEDA_TAMANHO):
    frames = []
    for i in range(1, total_frames + 1):
        filename = f'{prefix}_{i}.png'
        image = pygame.image.load(filename).convert_alpha()
        image = pygame.transform.smoothscale(image, tamanho)
        frames.append(image)
    return frames

ouro_frames = load_animation_frames(r"CatchTheCoin\Assets\PNG\Gold\hamburguer")
prata_frames = load_animation_frames(r"CatchTheCoin\Assets\PNG\Silver\batata")
bronze_frames = load_animation_frames(r"CatchTheCoin\Assets\PNG\Bronze\refri")
VALOR_MOEDAS = {'ouro': 5, 'prata': 3, 'bronze': 1}

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        self.frames = {'ouro': ouro_frames, 'prata': prata_frames, 'bronze': bronze_frames}[tipo]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.uniform(2, 5)
        self.animation_speed = 0.2
        self.frame_counter = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-50, -10)
            self.speed = random.uniform(2, 5)
        self.frame_counter += self.animation_speed
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class Barco(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = barco_sprite_img
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 70))
        self.speed = 8
        self.carga = 0
        self.max_carga = 100

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

    def voltar_ao_porto(self):
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 100)
        self.carga = 0

class Brocolis(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = brocolis_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.uniform(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.uniform(2, 4)

def fim_de_jogo():
    texto = FONT.render("FIM DE JOGO! Brócolis acertou 3 vezes!", True, (255, 0, 0))
    screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

# Variáveis iniciais
nivel = 1
qtd_moedas, v_min, v_max = configurar_dificuldade(nivel)
moedas = pygame.sprite.Group()
for _ in range(qtd_moedas):
    tipo = random.choice(['ouro', 'prata', 'bronze'])
    x = random.randint(0, WIDTH - 20)
    y = random.randint(-100, -10)
    moedas.add(Moeda(x, y, tipo))

barco = Barco()

brocolis = pygame.sprite.Group()
for _ in range(2):
    x = random.randint(0, WIDTH - 32)
    y = random.randint(-200, -50)
    brocolis.add(Brocolis(x, y))

acertos_brocolis = 0
MAX_ACERTOS = 3
em_descarga = False
tempo_descarga = 0
pontos = 0

# Loop principal
going = True
while going:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False

    keys = pygame.key.get_pressed()

    if not em_descarga and barco.carga >= barco.max_carga:
        som_aviso.play()
        moedas_no_ceu = [m for m in moedas if m.rect.y < HEIGHT / 2]
        for m in moedas_no_ceu:
            moedas.remove(m)
            pontos = max(0, pontos - 1)
        em_descarga = True
        tempo_descarga = pygame.time.get_ticks()

    if em_descarga:
        barco.voltar_ao_porto()
        if pygame.time.get_ticks() - tempo_descarga > 2000:
            barco.carga = 0
            em_descarga = False
        continue

    barco.update(keys)
    moedas.update()
    brocolis.update()

    colisoes = pygame.sprite.spritecollide(barco, moedas, True)
    for moeda in colisoes:
        barco.carga += VALOR_MOEDAS[moeda.tipo]
        som_beep.play()
        pontos += 1

    while len(moedas) < qtd_moedas:
        tipo = random.choice(['ouro', 'prata', 'bronze'])
        x = random.randint(0, WIDTH - 20)
        y = random.randint(-100, -10)
        moedas.add(Moeda(x, y, tipo))

    colisoes_brocolis = pygame.sprite.spritecollide(barco, brocolis, True)
    for _ in colisoes_brocolis:
        acertos_brocolis += 1
        if acertos_brocolis >= MAX_ACERTOS:
            fim_de_jogo()
        else:
            x = random.randint(0, WIDTH - 32)
            y = random.randint(-100, -40)
            brocolis.add(Brocolis(x, y))

    # Desenho
    screen.blit(background_img, (0, 0))
    score_text = f"Pontos: {pontos}"
    screen.blit(FONT.render(score_text, True, (255, 255, 255)), (10, 80))
    screen.blit(FONT.render(f"Moedas: {barco.carga}\{barco.max_carga}", True, (255, 255, 255)), (10, 10))
    screen.blit(FONT.render(f"Nível: {nivel}", True, (255, 255, 255)), (10, 50))
    screen.blit(FONT.render(f"Erros (Brócolis): {acertos_brocolis}/{MAX_ACERTOS}", True, (255, 100, 100)), (10, 110))

    moedas.draw(screen)
    brocolis.draw(screen)
    screen.blit(sea_sprite, sea_rect)
    screen.blit(barco.image, barco.rect)

    if barco.carga >= barco.max_carga:
        nivel = min(3, nivel + 1)
        qtd_moedas, v_min, v_max = configurar_dificuldade(nivel)

    pygame.display.flip()

pygame.quit()
sys.exit()

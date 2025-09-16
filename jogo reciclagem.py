import pygame
import random

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Reciclagem")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)     # Vidro
AZUL = (0, 0, 200)      # Papel
VERMELHO = (200, 0, 0)  # Plástico
AMARELO = (255, 215, 0) # Metal

# Player
player = pygame.Rect(400, 500, 50, 50)
velocidade = 5

# Tipos de lixo
tipos_lixo = ["vidro", "metal", "papel", "plastico"]
cores_lixo = {"vidro": VERDE, "papel": AZUL, "plastico": VERMELHO, "metal": AMARELO}

lixos = []
for _ in range(5):
    tipo = random.choice(tipos_lixo)
    rect = pygame.Rect(random.randint(50, 750), random.randint(50, 300), 30, 30)
    lixos.append({"tipo": tipo, "rect": rect})

# Lixeiras (na parte de baixo da tela)
lixeiras = {
    "vidro": pygame.Rect(100, 550, 60, 40),
    "metal": pygame.Rect(250, 550, 60, 40),
    "papel": pygame.Rect(400, 550, 60, 40),
    "plastico": pygame.Rect(550, 550, 60, 40),
}

cores_lixeiras = {"vidro": VERDE, "papel": AZUL, "plastico": VERMELHO, "metal": AMARELO}

# Estado do jogo
lixo_coletado = None
pontos = 0
font = pygame.font.SysFont(None, 36)

# Loop principal
rodando = True
while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimentação (setas e WASD)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        player.x -= velocidade
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        player.x += velocidade
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        player.y -= velocidade
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        player.y += velocidade

    # Colisão com lixo
    if not lixo_coletado:
        for l in lixos:
            if player.colliderect(l["rect"]):
                lixo_coletado = l
                lixos.remove(l)
                break

    # Soltar lixo na lixeira
    if lixo_coletado:
        texto = font.render(f"Lixo: {lixo_coletado['tipo']}", True, PRETO)
        tela.blit(texto, (10, 10))

        for tipo, lixeira in lixeiras.items():
            if player.colliderect(lixeira):
                if tipo == lixo_coletado["tipo"]:
                    pontos += 10
                    print("Acertou!")
                else:
                    pontos -= 5
                    print("Errou!")
                lixo_coletado = None
                break

    # Desenhar player (preto pra destacar)
    pygame.draw.rect(tela, PRETO, player)

    # Desenhar lixos
    for l in lixos:
        pygame.draw.rect(tela, cores_lixo[l["tipo"]], l["rect"])

    # Desenhar lixeiras
    for tipo, lixeira in lixeiras.items():
        pygame.draw.rect(tela, cores_lixeiras[tipo], lixeira)
        texto = font.render(tipo, True, BRANCO)
        tela.blit(texto, (lixeira.x, lixeira.y - 25))

    # Pontuação
    pontos_texto = font.render(f"Pontos: {pontos}", True, PRETO)
    tela.blit(pontos_texto, (600, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

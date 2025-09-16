import pygame
import random
# Sprite da lixeira de vidro para o player
SPRITE_LIXEIRA_VIDRO = pygame.transform.scale(pygame.image.load('assets/lixeira_vidro.png'), (40, 40))
# Sprites dos lixos
SPRITE_LIXOS = {
    "papel": pygame.transform.scale(pygame.image.load('assets/papel_papel.png'), (30, 30)),
    "lata": pygame.transform.scale(pygame.image.load('assets/lata_metal.png'), (30, 30)),
    "vidro": pygame.transform.scale(pygame.image.load('assets/copo_vrido.png'), (30, 30)),
    "plastico": pygame.transform.scale(pygame.image.load('assets/garrafa_plastico.png'), (30, 30)),
}
# Carrega sprites
SPRITE_CRAB = pygame.image.load('assets/player_crab.png')
SPRITE_CRAB = pygame.transform.scale(SPRITE_CRAB, (50, 50))

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
player_pos = [400, 500]
player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
velocidade = 5

# Tipos de lixo
lixos = []
tipos_lixo = ["papel", "lata", "vidro", "plastico"]

# Spawner vertical de lixos
lixos = []
for _ in range(5):
    tipo = random.choice(tipos_lixo)
    x = random.randint(50, 750)
    y = random.randint(-150, -30)
    rect = pygame.Rect(x, y, 30, 30)
    lixos.append({"tipo": tipo, "rect": rect, "vel": random.randint(2, 4)})

# Lixeiras (na parte de baixo da tela)
lixeiras = {
    "vidro": pygame.Rect(100, 550, 60, 40),
    "metal": pygame.Rect(250, 550, 60, 40),
    "papel": pygame.Rect(400, 550, 60, 40),
    "plastico": pygame.Rect(550, 550, 60, 40),
}

cores_lixeiras = {"vidro": VERDE, "papel": AZUL, "plastico": VERMELHO, "metal": AMARELO}

# Estado do jogo
vidas = 3
lixo_coletado = None
pontos = 0
font = pygame.font.SysFont(None, 36)
game_over = False

# Loop principal
rodando = True
while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimentação (apenas horizontal - esquerda e direita)
    if not game_over:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            player_pos[0] -= velocidade
            # Limitar movimento para não sair da tela
            if player_pos[0] < 0:
                player_pos[0] = 0
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            player_pos[0] += velocidade
            # Limitar movimento para não sair da tela
            if player_pos[0] > LARGURA - 50:
                player_pos[0] = LARGURA - 50
        player_rect.x, player_rect.y = player_pos[0], player_pos[1]

    # Atualiza posição dos lixos (descendo verticalmente)
    if not game_over:
        for l in lixos:
            l["rect"].y += l["vel"]
        # Remove lixos que saem da tela
        lixos = [l for l in lixos if l["rect"].y < ALTURA]
        # Spawna novos lixos se menos de 5 na tela
        while len(lixos) < 5:
            tipo = random.choice(tipos_lixo)
            x = random.randint(50, 750)
            y = random.randint(-150, -30)
            rect = pygame.Rect(x, y, 30, 30)
            lixos.append({"tipo": tipo, "rect": rect, "vel": random.randint(2, 4)})

        # Colisão com lixo
        if not lixo_coletado:
            for l in lixos:
                if player_rect.colliderect(l["rect"]):
                    lixo_coletado = l
                    lixos.remove(l)
                    break

    # Soltar lixo na lixeira
    if lixo_coletado:
        texto = font.render(f"Lixo: {lixo_coletado['tipo']}", True, PRETO)
        tela.blit(texto, (10, 10))

        # Colisão com player segurando lixeira de vidro
        # Para testes, só existe a lixeira de vidro
        lixeira_vidro_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
        if player_rect.colliderect(lixeira_vidro_rect):
            if lixo_coletado["tipo"] == "vidro":
                pontos += 5
            else:
                # Evitar pontos negativos
                if pontos >= 5:
                    pontos -= 5
                vidas -= 1
                # Verificar game over
                if vidas <= 0:
                    game_over = True
            lixo_coletado = None

    # Desenhar player (sprite de caranguejo) segurando lixeira de vidro
    if not game_over:
        tela.blit(SPRITE_CRAB, (player_pos[0], player_pos[1]))
        # Centralizar lixeira nas "mãos" do caranguejo, mais acima
        lixeira_x = player_pos[0] + (SPRITE_CRAB.get_width() // 2) - (SPRITE_LIXEIRA_VIDRO.get_width() // 2)
        lixeira_y = player_pos[1] - 20
        tela.blit(SPRITE_LIXEIRA_VIDRO, (lixeira_x, lixeira_y))

        # Desenhar lixos (sprites)
        for l in lixos:
            tela.blit(SPRITE_LIXOS[l["tipo"]], (l["rect"].x, l["rect"].y))
    else:
        # Tela de Game Over
        game_over_texto = pygame.font.SysFont(None, 72).render("GAME OVER", True, PRETO)
        restart_texto = font.render("Pressione R para reiniciar", True, PRETO)
        tela.blit(game_over_texto, (LARGURA//2 - 150, ALTURA//2 - 50))
        tela.blit(restart_texto, (LARGURA//2 - 120, ALTURA//2 + 20))
        
        # Reiniciar com R
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            game_over = False
            vidas = 3
            pontos = 0
            lixo_coletado = None
            lixos.clear()
            for _ in range(5):
                tipo = random.choice(tipos_lixo)
                x = random.randint(50, 750)
                y = random.randint(-150, -30)
                rect = pygame.Rect(x, y, 30, 30)
                lixos.append({"tipo": tipo, "rect": rect, "vel": random.randint(2, 4)})

    # (Removido: não desenhar lixeiras nem textos)

    # Pontuação e vidas
    pontos_texto = font.render(f"Pontos: {pontos}", True, PRETO)
    vidas_texto = font.render(f"Vidas: {vidas}", True, PRETO)
    tela.blit(pontos_texto, (600, 10))
    tela.blit(vidas_texto, (600, 40))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

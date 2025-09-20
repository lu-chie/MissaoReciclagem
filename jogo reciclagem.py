import pygame
import random

# Inicialização do Pygame e mixer de som
pygame.init()
pygame.mixer.init()

# Carregar sons
try:
    som_acerto = pygame.mixer.Sound('assets/coin_pickup.wav')
    som_erro = pygame.mixer.Sound('assets/error_sound.wav')
    som_click = pygame.mixer.Sound('assets/button_click.wav')
    som_acerto.set_volume(0.7)  # Ajustar volume (0.0 a 1.0)
    som_erro.set_volume(0.7)
    som_click.set_volume(0.5)
    
    # Música de fundo
    pygame.mixer.music.load('assets/background_birds.wav')
    pygame.mixer.music.set_volume(0.3)  # Volume baixo para não competir com efeitos
    pygame.mixer.music.play(-1)  # Loop infinito
    
except pygame.error as e:
    print(f"Erro ao carregar sons: {e}")
    som_acerto = som_erro = som_click = None
# Sprites das lixeiras para o player
SPRITE_LIXEIRAS = {
    "vidro": pygame.transform.scale(pygame.image.load('assets/lixeira_vidro.png'), (40, 40)),
    "plastico": pygame.transform.scale(pygame.image.load('assets/lixeira_plastico.png'), (40, 40)),
    "metal": pygame.transform.scale(pygame.image.load('assets/lixeira_metal.png'), (40, 40)),
    "papel": pygame.transform.scale(pygame.image.load('assets/lixeira_papel.png'), (40, 40)),
}
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
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Reciclagem")

# Background de praia
try:
    BACKGROUND_BEACH = pygame.image.load('assets/beach_background.jpg')
    BACKGROUND_BEACH = pygame.transform.scale(BACKGROUND_BEACH, (LARGURA, ALTURA))
except pygame.error as e:
    print(f"Erro ao carregar background: {e}")
    BACKGROUND_BEACH = None

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)     # Vidro
AZUL = (0, 0, 200)      # Papel
VERMELHO = (200, 0, 0)  # Plástico
AMARELO = (255, 215, 0) # Metal
CINZA_CLARO = (230, 230, 230)
CINZA_ESCURO = (100, 100, 100)

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
    lixos.append({"tipo": tipo, "rect": rect, "vel": 1})

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
lixeira_atual = "vidro"  # Lixeira que o player está segurando
tipos_lixeira = ["plastico", "vidro", "metal", "papel"]  # Ordem para as teclas 1-4

# Sistema de dificuldade
lixos_coletados = 0
velocidade_base = 1
velocidade_maxima = 6
incremento_velocidade = 0.2

# Sistema de classificação
def get_classificacao(pontos):
    if pontos >= 100:
        return "MESTRE DA RECICLAGEM", VERDE
    elif pontos >= 80:
        return "EXPERT AMBIENTAL", AZUL
    elif pontos >= 60:
        return "PROTETOR VERDE", AMARELO
    elif pontos >= 40:
        return "CONSCIENTE", VERMELHO
    elif pontos >= 20:
        return "APRENDIZ", CINZA_ESCURO
    else:
        return "INICIANTE", PRETO

# Loop principal
rodando = True
while rodando:
    # Desenhar background de praia ou cor sólida
    if BACKGROUND_BEACH:
        tela.blit(BACKGROUND_BEACH, (0, 0))
    else:
        tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Troca de lixeira com teclas 1-4 ou Q/E
        if evento.type == pygame.KEYDOWN and not game_over:
            if evento.key == pygame.K_1:
                lixeira_atual = tipos_lixeira[0]  # plastico
                if som_click: som_click.play()
            elif evento.key == pygame.K_2:
                lixeira_atual = tipos_lixeira[1]  # vidro
                if som_click: som_click.play()
            elif evento.key == pygame.K_3:
                lixeira_atual = tipos_lixeira[2]  # metal
                if som_click: som_click.play()
            elif evento.key == pygame.K_4:
                lixeira_atual = tipos_lixeira[3]  # papel
                if som_click: som_click.play()
            elif evento.key == pygame.K_q:
                # Ciclar para trás
                idx = tipos_lixeira.index(lixeira_atual)
                lixeira_atual = tipos_lixeira[(idx - 1) % len(tipos_lixeira)]
                if som_click: som_click.play()
            elif evento.key == pygame.K_e:
                # Ciclar para frente
                idx = tipos_lixeira.index(lixeira_atual)
                lixeira_atual = tipos_lixeira[(idx + 1) % len(tipos_lixeira)]
                if som_click: som_click.play()

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
            # Velocidade progressiva baseada em lixos coletados
            vel_atual = max(velocidade_base, min(velocidade_maxima, velocidade_base + (lixos_coletados * incremento_velocidade)))
            lixos.append({"tipo": tipo, "rect": rect, "vel": vel_atual})

        # Colisão com lixo
        if not lixo_coletado:
            for l in lixos:
                if player_rect.colliderect(l["rect"]):
                    lixo_coletado = l
                    lixos.remove(l)
                    break

    # Soltar lixo na lixeira
    if lixo_coletado:
        # Mostrar lixo coletado no HUD superior
        pygame.draw.rect(tela, AMARELO, (400, 90, 150, 30))
        pygame.draw.rect(tela, PRETO, (400, 90, 150, 30), 2)
        texto = font.render(f"COLETADO: {lixo_coletado['tipo'].upper()}", True, PRETO)
        tela.blit(texto, (405, 95))

        # Colisão com player segurando lixeira selecionada
        lixeira_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
        if player_rect.colliderect(lixeira_rect):
            # Verificar se o tipo do lixo corresponde ao tipo da lixeira atual
            if (lixo_coletado["tipo"] == "lata" and lixeira_atual == "metal") or \
               (lixo_coletado["tipo"] == lixeira_atual):
                pontos += 5
                lixos_coletados += 1  # Incrementar contador para dificuldade
                if som_acerto: som_acerto.play()  # Som de acerto
            else:
                # Evitar pontos negativos
                if pontos >= 5:
                    pontos -= 5
                vidas -= 1
                if som_erro: som_erro.play()  # Som de erro
                # Verificar game over
                if vidas <= 0:
                    game_over = True
            lixo_coletado = None

    # Desenhar player (sprite de caranguejo) segurando lixeira selecionada
    if not game_over:
        tela.blit(SPRITE_CRAB, (player_pos[0], player_pos[1]))
        # Centralizar lixeira atual nas "mãos" do caranguejo, mais acima
        sprite_lixeira_atual = SPRITE_LIXEIRAS[lixeira_atual]
        lixeira_x = player_pos[0] + (SPRITE_CRAB.get_width() // 2) - (sprite_lixeira_atual.get_width() // 2)
        lixeira_y = player_pos[1] - 20
        tela.blit(sprite_lixeira_atual, (lixeira_x, lixeira_y))

        # Desenhar lixos (sprites)
        for l in lixos:
            tela.blit(SPRITE_LIXOS[l["tipo"]], (l["rect"].x, l["rect"].y))
    else:
        # Tela de Game Over com classificação
        classificacao, cor_classificacao = get_classificacao(pontos)
        
        game_over_texto = pygame.font.SysFont(None, 72).render("GAME OVER", True, PRETO)
        pontos_final_texto = pygame.font.SysFont(None, 48).render(f"PONTOS FINAIS: {pontos}", True, PRETO)
        classificacao_texto = pygame.font.SysFont(None, 36).render(f"CLASSIFICAÇÃO: {classificacao}", True, cor_classificacao)
        lixos_coletados_texto = font.render(f"Lixos coletados corretamente: {lixos_coletados}", True, PRETO)
        restart_texto = font.render("Pressione R para reiniciar", True, PRETO)
        
        tela.blit(game_over_texto, (LARGURA//2 - 150, ALTURA//2 - 100))
        tela.blit(pontos_final_texto, (LARGURA//2 - 150, ALTURA//2 - 50))
        tela.blit(classificacao_texto, (LARGURA//2 - 180, ALTURA//2 - 10))
        tela.blit(lixos_coletados_texto, (LARGURA//2 - 150, ALTURA//2 + 20))
        tela.blit(restart_texto, (LARGURA//2 - 120, ALTURA//2 + 50))
        
        # Reiniciar com R
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            game_over = False
            vidas = 3
            pontos = 0
            lixo_coletado = None
            lixeira_atual = "vidro"  # Reset para lixeira inicial
            lixos_coletados = 0  # Reset contador de dificuldade
            lixos.clear()
            for _ in range(5):
                tipo = random.choice(tipos_lixo)
                x = random.randint(50, 750)
                y = random.randint(-150, -30)
                rect = pygame.Rect(x, y, 30, 30)
                lixos.append({"tipo": tipo, "rect": rect, "vel": velocidade_base})

    # (Removido: não desenhar lixeiras nem textos)

    # HUD Melhorado
    # Painel superior com fundo
    pygame.draw.rect(tela, CINZA_CLARO, (0, 0, LARGURA, 80))
    pygame.draw.rect(tela, CINZA_ESCURO, (0, 0, LARGURA, 80), 2)
    
    # Pontuação com ícone
    font_grande = pygame.font.SysFont(None, 48)
    font_media = pygame.font.SysFont(None, 32)
    font_pequena = pygame.font.SysFont(None, 24)
    
    pontos_texto = font_grande.render(f"PONTOS: {pontos}", True, PRETO)
    tela.blit(pontos_texto, (20, 15))
    
    # Vidas com corações
    vidas_texto = font_media.render("VIDAS:", True, PRETO)
    tela.blit(vidas_texto, (300, 25))
    for i in range(vidas):
        pygame.draw.circle(tela, VERMELHO, (380 + i * 25, 35), 8)
    
    # Lixeira atual com sprite pequeno
    lixeira_texto = font_media.render("LIXEIRA:", True, PRETO)
    tela.blit(lixeira_texto, (450, 25))
    sprite_mini = pygame.transform.scale(SPRITE_LIXEIRAS[lixeira_atual], (25, 25))
    tela.blit(sprite_mini, (550, 25))
    lixeira_nome = font_pequena.render(lixeira_atual.upper(), True, PRETO)
    tela.blit(lixeira_nome, (580, 30))
    
    # Dificuldade e velocidade atual
    velocidade_atual = max(velocidade_base, min(velocidade_maxima, velocidade_base + (lixos_coletados * incremento_velocidade)))
    dificuldade_texto = font_pequena.render(f"COLETADOS: {lixos_coletados} | VEL: {velocidade_atual:.1f}", True, PRETO)
    tela.blit(dificuldade_texto, (20, 55))
    
    # Classificação atual
    classificacao_atual, cor_class = get_classificacao(pontos)
    class_texto = font_pequena.render(f"NÍVEL: {classificacao_atual}", True, cor_class)
    tela.blit(class_texto, (450, 55))
    
    # Controles no canto inferior esquerdo
    if not game_over:
        controles_texto1 = font_pequena.render("CONTROLES:", True, PRETO)
        controles_texto2 = font_pequena.render("1-4: Selecionar lixeira", True, PRETO)
        controles_texto3 = font_pequena.render("Q/E: Alternar", True, PRETO)
        controles_texto4 = font_pequena.render("A/D: Mover", True, PRETO)
        
        tela.blit(controles_texto1, (10, ALTURA - 90))
        tela.blit(controles_texto2, (10, ALTURA - 70))
        tela.blit(controles_texto3, (10, ALTURA - 50))
        tela.blit(controles_texto4, (10, ALTURA - 30))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Parar música ao sair
pygame.mixer.music.stop()
pygame.quit()

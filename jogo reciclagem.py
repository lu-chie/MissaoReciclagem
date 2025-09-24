import pygame
import random
import json
import time

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

# Background animado - Sistema de ciclo dia/noite
class AnimatedBackground:
    def __init__(self):
        try:
            # Carregar sprite sheet
            self.sprite_sheet = pygame.image.load('assets/Background.png')
            
            # Definir frames baseado no JSON fornecido
            self.frames = {
                # Dia (0-4)
                'day': [
                    (0, 0, 304, 256),      # Frame 0
                    (304, 0, 304, 256),    # Frame 1  
                    (608, 0, 304, 256),    # Frame 2
                    (0, 0, 304, 256),      # Frame 3 (repetição do 0)
                    (912, 0, 304, 256),    # Frame 4
                ],
                # Entardecer/Amanhecer (5-9)
                'dawn_dusk': [
                    (0, 256, 304, 256),    # Frame 5
                    (304, 256, 304, 256),  # Frame 6
                    (608, 256, 304, 256),  # Frame 7
                    (0, 256, 304, 256),    # Frame 8 (repetição do 5)
                    (912, 256, 304, 256),  # Frame 9
                ],
                # Noite (10-14)
                'night': [
                    (0, 512, 304, 256),    # Frame 10
                    (304, 512, 304, 256),  # Frame 11
                    (608, 512, 304, 256),  # Frame 12
                    (0, 512, 304, 256),    # Frame 13 (repetição do 10)
                    (912, 512, 304, 256),  # Frame 14
                ]
            }
            
            # Estado da animação
            self.current_period = 'day'  # 'day', 'dawn_dusk', 'night'
            self.frame_index = 0
            self.animation_timer = 0
            self.frame_duration = 200  # ms por frame
            self.period_duration = 30000  # 30 segundos por período
            self.period_timer = 0
            
        except pygame.error as e:
            print(f"Erro ao carregar background animado: {e}")
            self.sprite_sheet = None
    
    def update(self, dt):
        if not self.sprite_sheet:
            return
            
        # Atualizar timer do período
        self.period_timer += dt
        if self.period_timer >= self.period_duration:
            self.period_timer = 0
            # Ciclar através dos períodos
            periods = ['day', 'dawn_dusk', 'night']
            current_idx = periods.index(self.current_period)
            self.current_period = periods[(current_idx + 1) % len(periods)]
            self.frame_index = 0
        
        # Atualizar animação do frame atual
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.current_period])
    
    def draw(self, screen):
        if not self.sprite_sheet:
            screen.fill((135, 206, 235))  # Azul céu como fallback
            return
            
        # Obter frame atual
        frame_rect = self.frames[self.current_period][self.frame_index]
        frame_surface = self.sprite_sheet.subsurface(frame_rect)
        
        # Escalar para tamanho da tela
        scaled_frame = pygame.transform.scale(frame_surface, (LARGURA, ALTURA))
        screen.blit(scaled_frame, (0, 0))
    
    def get_period_info(self):
        periods_pt = {
            'day': 'DIA',
            'dawn_dusk': 'ENTARDECER',
            'night': 'NOITE'
        }
        progress = (self.period_timer / self.period_duration) * 100
        return periods_pt[self.current_period], progress

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

# Instanciar background animado
animated_background = AnimatedBackground()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)     # Vidro
AZUL = (0, 0, 200)      # Papel
VERMELHO = (200, 0, 0)  # Plástico
AMARELO = (255, 215, 0) # Metal
CINZA_CLARO = (230, 230, 230)
CINZA_ESCURO = (100, 100, 100)

# Player - Velocidade aumentada de 5 para 8
player_pos = [400, 500]
player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
velocidade = 8  # Aumentado para acompanhar melhor os lixos

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

# Estado do jogo - Vidas aumentadas de 3 para 5
vidas = 5  # Aumentado para 5 vidas
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

# Clock para controle de FPS e delta time
clock = pygame.time.Clock()

# Loop principal
rodando = True
while rodando:
    # Delta time para animações
    dt = clock.tick(60)
    
    # Atualizar background animado
    animated_background.update(dt)
    
    # Desenhar background animado
    animated_background.draw(tela)

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
        # Lista para armazenar lixos que caíram no chão
        lixos_caidos = []
        
        for l in lixos:
            l["rect"].y += l["vel"]
            # Verificar se o lixo caiu no chão (passou da tela)
            if l["rect"].y >= ALTURA:
                lixos_caidos.append(l)
        
        # Processar lixos que caíram no chão - jogador perde vida
        if lixos_caidos:
            vidas -= len(lixos_caidos)  # Perder 1 vida por lixo que caiu
            if som_erro: som_erro.play()  # Som de erro
            # Verificar game over
            if vidas <= 0:
                game_over = True
        
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
            vidas = 5  # Reset para 5 vidas
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

    # HUD Melhorado
    # Painel superior com fundo semi-transparente
    hud_surface = pygame.Surface((LARGURA, 120))
    hud_surface.set_alpha(180)  # Semi-transparência
    hud_surface.fill(CINZA_CLARO)
    tela.blit(hud_surface, (0, 0))
    pygame.draw.rect(tela, CINZA_ESCURO, (0, 0, LARGURA, 120), 2)
    
    # Pontuação com ícone
    font_grande = pygame.font.SysFont(None, 48)
    font_media = pygame.font.SysFont(None, 32)
    font_pequena = pygame.font.SysFont(None, 24)
    
    pontos_texto = font_grande.render(f"PONTOS: {pontos}", True, PRETO)
    tela.blit(pontos_texto, (20, 15))
    
    # Vidas com corações (agora até 5)
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
    
    # Sistema de período do dia
    periodo_nome, periodo_progresso = animated_background.get_period_info()
    periodo_texto = font_media.render(f"PERÍODO: {periodo_nome}", True, PRETO)
    tela.blit(periodo_texto, (20, 55))
    
    # Barra de progresso do período
    barra_rect = pygame.Rect(200, 65, 100, 10)
    pygame.draw.rect(tela, CINZA_ESCURO, barra_rect)
    progresso_width = int((periodo_progresso / 100) * 100)
    progresso_rect = pygame.Rect(200, 65, progresso_width, 10)
    # Cor da barra baseada no período
    cor_periodo = AMARELO if periodo_nome == 'DIA' else (255, 165, 0) if periodo_nome == 'ENTARDECER' else AZUL
    pygame.draw.rect(tela, cor_periodo, progresso_rect)
    
    # Dificuldade e velocidade atual
    velocidade_atual = max(velocidade_base, min(velocidade_maxima, velocidade_base + (lixos_coletados * incremento_velocidade)))
    dificuldade_texto = font_pequena.render(f"COLETADOS: {lixos_coletados} | VEL: {velocidade_atual:.1f}", True, PRETO)
    tela.blit(dificuldade_texto, (320, 80))
    
    # Classificação atual
    classificacao_atual, cor_class = get_classificacao(pontos)
    class_texto = font_pequena.render(f"NÍVEL: {classificacao_atual}", True, cor_class)
    tela.blit(class_texto, (450, 95))
    
    # Controles no canto inferior esquerdo
    if not game_over:
        controles_texto1 = font_pequena.render("CONTROLES:", True, BRANCO)
        controles_texto2 = font_pequena.render("1-4: Selecionar lixeira", True, BRANCO)
        controles_texto3 = font_pequena.render("Q/E: Alternar", True, BRANCO)
        controles_texto4 = font_pequena.render("A/D: Mover", True, BRANCO)
        controles_texto5 = font_pequena.render("⚠️ Lixos no chão = -1 VIDA", True, VERMELHO)
        
        tela.blit(controles_texto1, (10, ALTURA - 110))
        tela.blit(controles_texto2, (10, ALTURA - 90))
        tela.blit(controles_texto3, (10, ALTURA - 70))
        tela.blit(controles_texto4, (10, ALTURA - 50))
        tela.blit(controles_texto5, (10, ALTURA - 30))

    pygame.display.flip()

# Parar música ao sair
pygame.mixer.music.stop()
pygame.quit()

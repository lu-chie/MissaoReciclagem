
# MissaoReciclagem

## Descrição do Jogo

MissaoReciclagem é um arcade educativo desenvolvido em **Pygame**, com foco em ensinar conceitos de reciclagem de forma lúdica. O jogador controla um personagem que se movimenta horizontalmente pela tela (esquerda e direita) e carrega uma lixeira seletiva. O objetivo é coletar corretamente os resíduos que caem do topo da tela, alternando o tipo de lixeira conforme o lixo.

## Mecânicas Principais

- **Movimento:** O personagem se desloca para a esquerda/direita usando as teclas direcionais (setas ou A/D).
- **Troca de lixeira:** Teclas específicas alternam entre os tipos de lixeiras (vidro, metal, papel, plástico, orgânico).
- **Queda de resíduos:** Objetos de diferentes tipos caem aleatoriamente do topo da tela.
- **Pontuação:** Pontos ao reciclar corretamente, penalidade ao errar (perda de pontos e vidas).
- **Progressão:** A velocidade de queda dos resíduos aumenta gradualmente, tornando o jogo mais desafiador.

## Visão Geral

- **Tipo:** Arcade educativo 2D
- **Engine:** Pygame
- **Plataformas alvo:** PC (Windows/Linux), Web (HTML5 opcional via conversão)

**Pitch:** Controle um personagem que se move na horizontal e alterna a lixeira ativa (vidro, metal, papel, orgânico, plástico) para coletar corretamente os resíduos que caem. Aprenda reciclagem brincando, com dificuldade progressiva e feedbacks claros.

## Objetivos

1. Promover conscientização sobre reciclagem e preservação ambiental por meio de uma experiência lúdica e acessível.
2. Ensinar a separar resíduos por tipo e reforçar hábitos sustentáveis com reforço positivo.
3. Medir aprendizado via acertos/erros e níveis de proficiência. Entregar build estável, performática e de fácil distribuição.

## Público-Alvo

Crianças e adolescentes (7–15 anos), professores e famílias buscando apoio didático em educação ambiental. Linguagem simples, visual colorido, sessões de 3–5 min.

## Loop de Jogo

1. Spawner cria resíduos com tipo e posição X aleatórios.
2. Jogador posiciona-se sob o resíduo e alterna a lixeira correta.
3. Checagem de colisão: se tipo == lixeira ativa → acerto; senão → erro.
4. Ajuste de score/vida/combo; HUD é atualizado.
5. A cada intervalo, aumenta a dificuldade.
6. Fim: acabou o tempo ou zerou vidas → tela de resultado (Game Over).


import pygame
import sys
import random
import os

# ----------------- CONFIGURAÇÕES GLOBAIS -----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

FPS_INICIAL = 5           # Velocidade inicial (frames por segundo)
SPEED_INCREASE_SCORE = 5  # A cada 5 pontos, a velocidade aumenta
FPS_INCREMENT = 1

# Temas disponíveis: define fundo e cor do texto
temas = {
    "verde": {
        "fundo": (0, 128, 0),
        "texto": (255, 255, 255)
    },
    "preto": {
        "fundo": (0, 0, 0),
        "texto": (255, 255, 255)
    },
    "branco": {
        "fundo": (255, 255, 255),
        "texto": (0, 0, 0)
    }
}
lista_temas = list(temas.keys())
tema_selecionado = lista_temas[0]  # Tema padrão

ARQUIVO_RECORDS = "records.txt"

# Inicializa o Pygame e configura a tela
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jogo da Cobrinha')
clock = pygame.time.Clock()

# Fontes para textos
font_menu = pygame.font.SysFont("arial", 30)
font_texto = pygame.font.SysFont("arial", 25)
font_mensagem = pygame.font.SysFont("arial", 35)

# ----------------- CARREGAMENTO DOS SPRITES -----------------
# Sprite da maçã
apple_img = pygame.image.load("assets/apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (BLOCK_SIZE, BLOCK_SIZE))

# Sprites da cabeça
head_up_img = pygame.image.load("assets/head_up.png").convert_alpha()
head_down_img = pygame.image.load("assets/head_down.png").convert_alpha()
head_left_img = pygame.image.load("assets/head_left.png").convert_alpha()
head_right_img = pygame.image.load("assets/head_right.png").convert_alpha()
head_up_img = pygame.transform.scale(head_up_img, (BLOCK_SIZE, BLOCK_SIZE))
head_down_img = pygame.transform.scale(head_down_img, (BLOCK_SIZE, BLOCK_SIZE))
head_left_img = pygame.transform.scale(head_left_img, (BLOCK_SIZE, BLOCK_SIZE))
head_right_img = pygame.transform.scale(head_right_img, (BLOCK_SIZE, BLOCK_SIZE))

# Sprites da cauda
tail_up_img = pygame.image.load("assets/tail_up.png").convert_alpha()
tail_down_img = pygame.image.load("assets/tail_down.png").convert_alpha()
tail_left_img = pygame.image.load("assets/tail_left.png").convert_alpha()
tail_right_img = pygame.image.load("assets/tail_right.png").convert_alpha()
tail_up_img = pygame.transform.scale(tail_up_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_down_img = pygame.transform.scale(tail_down_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_left_img = pygame.transform.scale(tail_left_img, (BLOCK_SIZE, BLOCK_SIZE))
tail_right_img = pygame.transform.scale(tail_right_img, (BLOCK_SIZE, BLOCK_SIZE))

# Sprites do corpo
body_horizontal_img = pygame.image.load("assets/body_horizontal.png").convert_alpha()
body_vertical_img = pygame.image.load("assets/body_vertical.png").convert_alpha()
body_topleft_img = pygame.image.load("assets/body_topleft.png").convert_alpha()
body_topright_img = pygame.image.load("assets/body_topright.png").convert_alpha()
body_bottomleft_img = pygame.image.load("assets/body_bottomleft.png").convert_alpha()
body_bottomright_img = pygame.image.load("assets/body_bottomright.png").convert_alpha()
body_horizontal_img = pygame.transform.scale(body_horizontal_img, (BLOCK_SIZE, BLOCK_SIZE))
body_vertical_img = pygame.transform.scale(body_vertical_img, (BLOCK_SIZE, BLOCK_SIZE))
body_topleft_img = pygame.transform.scale(body_topleft_img, (BLOCK_SIZE, BLOCK_SIZE))
body_topright_img = pygame.transform.scale(body_topright_img, (BLOCK_SIZE, BLOCK_SIZE))
body_bottomleft_img = pygame.transform.scale(body_bottomleft_img, (BLOCK_SIZE, BLOCK_SIZE))
body_bottomright_img = pygame.transform.scale(body_bottomright_img, (BLOCK_SIZE, BLOCK_SIZE))

# ----------------- CLASSE SCORE MANAGER -----------------
class ScoreManager:
    """Gerencia o salvamento e carregamento dos melhores scores."""
    @staticmethod
    def load_scores():
        if not os.path.exists(ARQUIVO_RECORDS):
            return []
        try:
            with open(ARQUIVO_RECORDS, "r") as f:
                linhas = f.readlines()
            scores = [int(linha.strip()) for linha in linhas if linha.strip().isdigit()]
        except Exception as e:
            print("Erro ao carregar records:", e)
            scores = []
        return scores

    @staticmethod
    def save_score(score):
        scores = ScoreManager.load_scores()
        scores.append(score)
        scores = sorted(scores, reverse=True)[:5]
        try:
            with open(ARQUIVO_RECORDS, "w") as f:
                for s in scores:
                    f.write(str(s) + "\n")
        except Exception as e:
            print("Erro ao salvar records:", e)
        return scores

# ----------------- CLASSE DA COBRA -----------------
class Cobra:
    """Gerencia a lógica e o desenho da cobra utilizando sprites."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.lista = []  # Lista de segmentos; cada segmento é uma lista [x, y]
        self.tamanho = 1

    def mover(self):
        """Atualiza a posição e a lista de segmentos da cobra."""
        self.x += self.dx
        self.y += self.dy
        self.lista.append([self.x, self.y])
        if len(self.lista) > self.tamanho:
            self.lista.pop(0)

    def desenhar(self, surface):
        """
        Desenha a cobra utilizando sprites.
        Se a cobra possui menos de 2 segmentos, desenha apenas a cabeça.
        """
        if len(self.lista) < 2:
            head_img = self._escolher_imagem_cabeca()
            surface.blit(head_img, (self.x, self.y))
            return

        # Desenha a cabeça (último segmento da lista)
        head_img = self._escolher_imagem_cabeca()
        surface.blit(head_img, (self.lista[-1][0], self.lista[-1][1]))

        # Desenha a cauda (primeiro segmento)
        tail_pos = self.lista[0]
        segundo = self.lista[1]
        tail_img = self._escolher_imagem_cauda(tail_pos, segundo)
        surface.blit(tail_img, (tail_pos[0], tail_pos[1]))

        # Desenha os segmentos intermediários do corpo
        for i in range(1, len(self.lista) - 1):
            prev = self.lista[i - 1]
            curr = self.lista[i]
            next_seg = self.lista[i + 1]
            body_img = self._escolher_imagem_corpo(prev, curr, next_seg)
            surface.blit(body_img, (curr[0], curr[1]))

    def _escolher_imagem_cabeca(self):
        """Seleciona a imagem da cabeça de acordo com a direção atual."""
        if self.dx > 0:
            return head_right_img
        elif self.dx < 0:
            return head_left_img
        elif self.dy > 0:
            return head_down_img
        elif self.dy < 0:
            return head_up_img
        else:
            return head_right_img

    def _escolher_imagem_cauda(self, tail, next_seg):
        """Seleciona a imagem da cauda com base na direção do segundo segmento."""
        vx = next_seg[0] - tail[0]
        vy = next_seg[1] - tail[1]
        if vx > 0:
            return tail_left_img
        elif vx < 0:
            return tail_right_img
        elif vy > 0:
            return tail_up_img
        elif vy < 0:
            return tail_down_img
        else:
            return tail_right_img

    def _escolher_imagem_corpo(self, prev, curr, next_seg):
        """
        Seleciona a imagem do corpo.
        Se o segmento é reto (horizontal ou vertical), utiliza a imagem correspondente;
        caso contrário, utiliza uma imagem de curva de acordo com as direções.
        Nesta versão, as imagens das curvas foram invertidas.
        """
        vx1 = curr[0] - prev[0]
        vy1 = curr[1] - prev[1]
        vx2 = next_seg[0] - curr[0]
        vy2 = next_seg[1] - curr[1]

        # Reto horizontal ou vertical
        if vx1 == vx2 or vy1 == vy2:
            if vx1 != 0:
                return body_horizontal_img
            else:
                return body_vertical_img
        else:
            # Inversão: trocamos as imagens de curva
            if (vx1 > 0 and vy2 > 0) or (vy1 > 0 and vx2 > 0):
                return body_topright_img  # invertido de body_topleft_img
            elif (vx1 > 0 and vy2 < 0) or (vy1 < 0 and vx2 > 0):
                return body_bottomright_img  # invertido de body_bottomleft_img
            elif (vx1 < 0 and vy2 > 0) or (vy1 > 0 and vx2 < 0):
                return body_topleft_img  # invertido de body_topright_img
            elif (vx1 < 0 and vy2 < 0) or (vy1 < 0 and vx2 < 0):
                return body_bottomleft_img  # invertido de body_bottomright_img
            else:
                return body_horizontal_img

# ----------------- FUNÇÕES AUXILIARES -----------------
def draw_text(text, font, color, surface, x, y):
    """Desenha um texto na tela na posição (x, y)."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

def show_message_center(msg, color):
    """Exibe uma mensagem centralizada na tela."""
    text_surface = font_mensagem.render(msg, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text_surface, text_rect)

# ----------------- TELAS DO JOGO -----------------
def main_menu():
    """Menu principal com as opções: Jogar, Instruções, Configurações e Sair."""
    ativo = True
    while ativo:
        screen.fill(temas[tema_selecionado]["fundo"])
        draw_text("JOGO DA COBRINHA", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 4, 100)
        draw_text("1 - Jogar", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 200)
        draw_text("I - Instruções", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 250)
        draw_text("S - Configurações", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 300)
        draw_text("Q - Sair", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 350)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choose_mode()
                elif event.key == pygame.K_i:
                    instructions_screen()
                elif event.key == pygame.K_s:
                    settings_screen()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def instructions_screen():
    """Tela de instruções do jogo."""
    ativo = True
    while ativo:
        screen.fill(temas[tema_selecionado]["fundo"])
        draw_text("Instruções:", font_menu, temas[tema_selecionado]["texto"], screen, 50, 50)
        draw_text("- Use as setas para mover a cobra.", font_texto, temas[tema_selecionado]["texto"], screen, 50, 100)
        draw_text("- Coma a maçã para ganhar pontos.", font_texto, temas[tema_selecionado]["texto"], screen, 50, 140)
        draw_text("- Evite bater nas paredes, em si mesmo ou, no modo Desafio, nos obstáculos.", font_texto, temas[tema_selecionado]["texto"], screen, 50, 180)
        draw_text("Pressione B para voltar ao menu.", font_texto, temas[tema_selecionado]["texto"], screen, 50, 240)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                ativo = False

def settings_screen():
    """
    Tela de configurações para:
      - Trocar o tema (ciclando entre as opções disponíveis)
      - Voltar ao menu principal
    """
    global tema_selecionado
    ativo = True
    indice_tema = lista_temas.index(tema_selecionado)
    while ativo:
        screen.fill(temas[tema_selecionado]["fundo"])
        draw_text("Configurações", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 50)
        draw_text("T - Trocar Tema (Atual: {})".format(tema_selecionado), font_texto, temas[tema_selecionado]["texto"], screen, 50, 150)
        draw_text("B - Voltar ao Menu", font_texto, temas[tema_selecionado]["texto"], screen, 50, 250)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    indice_tema = (indice_tema + 1) % len(lista_temas)
                    tema_selecionado = lista_temas[indice_tema]
                elif event.key == pygame.K_b:
                    ativo = False

def choose_mode():
    """Tela para selecionar o modo de jogo: Clássico ou Desafio."""
    ativo = True
    while ativo:
        screen.fill(temas[tema_selecionado]["fundo"])
        draw_text("Selecione o Modo de Jogo", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 5, 100)
        draw_text("1 - Modo Clássico", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 200)
        draw_text("2 - Modo Desafio", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 250)
        draw_text("B - Voltar ao Menu", font_menu, temas[tema_selecionado]["texto"], screen, SCREEN_WIDTH / 3, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(mode="classico")
                elif event.key == pygame.K_2:
                    game_loop(mode="desafio")
                elif event.key == pygame.K_b:
                    ativo = False

# ----------------- CLASSE DO JOGO -----------------
class Game:
    """
    Gerencia o loop principal do jogo.
    mode:
      - "classico": jogo sem obstáculos permanentes.
      - "desafio": a cada maçã consumida, um obstáculo é adicionado.
    """
    def __init__(self, mode="classico"):
        self.mode = mode
        self.fps = FPS_INICIAL
        self.score = 0
        self.apple_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.apple_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.obstacles = []
        self.cobra = Cobra(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.game_active = True

    def processar_eventos(self):
        """Processa os eventos de teclado para controlar a cobra."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.cobra.dx == 0:
                    self.cobra.dx = -BLOCK_SIZE
                    self.cobra.dy = 0
                elif event.key == pygame.K_RIGHT and self.cobra.dx == 0:
                    self.cobra.dx = BLOCK_SIZE
                    self.cobra.dy = 0
                elif event.key == pygame.K_UP and self.cobra.dy == 0:
                    self.cobra.dy = -BLOCK_SIZE
                    self.cobra.dx = 0
                elif event.key == pygame.K_DOWN and self.cobra.dy == 0:
                    self.cobra.dy = BLOCK_SIZE
                    self.cobra.dx = 0

    def atualizar(self):
        """Atualiza a lógica do jogo (movimentação, colisões e pontuação)."""
        self.cobra.mover()

        # Colisão com as bordas
        if (self.cobra.x >= SCREEN_WIDTH or self.cobra.x < 0 or
            self.cobra.y >= SCREEN_HEIGHT or self.cobra.y < 0):
            self.game_active = False

        # Colisão com o próprio corpo
        for segmento in self.cobra.lista[:-1]:
            if segmento == [self.cobra.x, self.cobra.y]:
                self.game_active = False

        # No modo Desafio, verifica colisão com obstáculos
        if self.mode == "desafio":
            for obs in self.obstacles:
                if self.cobra.x == obs[0] and self.cobra.y == obs[1]:
                    self.game_active = False

        # Verifica se a cobra comeu a maçã
        if self.cobra.x == self.apple_x and self.cobra.y == self.apple_y:
            self.apple_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.apple_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.cobra.tamanho += 1
            self.score += 1

            # No modo Desafio, adiciona um obstáculo a cada maçã consumida
            if self.mode == "desafio":
                new_obs = [round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                           round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE]
                self.obstacles.append(new_obs)

            if self.score % SPEED_INCREASE_SCORE == 0:
                self.fps += FPS_INCREMENT

    def desenhar(self):
        """Desenha os elementos do jogo na tela."""
        screen.fill(temas[tema_selecionado]["fundo"])
        # Desenha a maçã utilizando sprite
        screen.blit(apple_img, (self.apple_x, self.apple_y))
        # Se estiver no modo Desafio, desenha os obstáculos (como retângulos simples)
        if self.mode == "desafio":
            for obs in self.obstacles:
                pygame.draw.rect(screen, temas[tema_selecionado]["texto"], [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
        # Desenha a cobra com sprites
        self.cobra.desenhar(screen)
        # Exibe o placar no canto superior direito
        score_text = font_texto.render("Pontuação: " + str(self.score), True, temas[tema_selecionado]["texto"])
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_text, score_rect)
        pygame.display.update()

    def loop(self):
        """Loop principal do jogo."""
        while self.game_active:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            clock.tick(self.fps)
        records = ScoreManager.save_score(self.score)
        game_over_screen(self.score, records, self.mode)

# ----------------- TELA DE GAME OVER -----------------
def game_over_screen(score, records, mode):
    """Exibe a tela de Game Over com o score atual e os melhores records."""
    ativo = True
    while ativo:
        screen.fill(temas[tema_selecionado]["fundo"])
        show_message_center("Game Over! Pressione C para jogar novamente ou Q para sair", temas[tema_selecionado]["texto"])
        draw_text("Seu Score: " + str(score), font_texto, temas[tema_selecionado]["texto"], screen, 50, SCREEN_HEIGHT / 2 + 50)
        draw_text("Melhores Records:", font_texto, temas[tema_selecionado]["texto"], screen, 50, SCREEN_HEIGHT / 2 + 90)
        for i, r in enumerate(records):
            draw_text("{}. {}".format(i+1, r), font_texto, temas[tema_selecionado]["texto"], screen, 50, SCREEN_HEIGHT / 2 + 120 + i * 30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    if mode == "classico":
                        game_loop(mode="classico")
                    else:
                        game_loop(mode="desafio")
                    ativo = False

# ----------------- FUNÇÃO PARA INICIAR O GAME LOOP -----------------
def game_loop(mode="classico"):
    jogo = Game(mode)
    jogo.loop()

# ----------------- EXECUÇÃO DO JOGO -----------------
if __name__ == "__main__":
    main_menu()

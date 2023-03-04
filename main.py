import pygame
from abc import abstractmethod, ABCMeta
from random import choice

pygame.init()

COMPRIMENTO_TELA = 1280
LARGURA_TELA = 720

CIMA_Player1 = pygame.K_w
BAIXO_Player1 = pygame.K_s

CIMA_Player2 = pygame.K_UP
BAIXO_Player2 = pygame.K_DOWN

PAUSADO = 0
JOGANDO = 1


AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)

tela = pygame.display.set_mode((COMPRIMENTO_TELA, LARGURA_TELA))
fonte = pygame.font.SysFont("arial", 40, False, False)

class ElementoDoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass
    @abstractmethod
    def calcular_regra(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Bola(ElementoDoJogo):
    def __init__(self, x, y, tamanho, cor):
        self.posicaoX = x
        self.posicaoY = y
        self.raio = tamanho
        self.cor = cor
        self.VELOCIDADE = 1
        self.velocidadeX = 1
        self.velocidadeY = 0

    def pintar(self, tela):
        pygame.draw.circle(tela, self.cor, (self.posicaoX-10, self.posicaoY), self.raio, 0)

    def processar_eventos(self, eventos):
        pass

    def calcular_regra(self):
        self.posicaoX += self.velocidadeX
        self.posicaoY += self.velocidadeY

    def escolher_direcao(self):
        escolha = choice((1, 2, 3))
        if escolha == 1:
            self.velocidadeY = self.VELOCIDADE

        elif escolha == 2:
            self.velocidadeY = -self.VELOCIDADE

        else:
            self.velocidadeY = 0


class Cenario(ElementoDoJogo):
    def __init__(self, obj_bola):
        self.bola = obj_bola
        self.lista_objetos = [obj_bola]
        self.comprimento = 20
        self.estado = PAUSADO
        self.player1_pontos = 0
        self.player2_pontos = 0
        self.batida = 0


    def adicionar_jogador(self, obj_jogador):
        self.lista_objetos.extend(obj_jogador)

    def calcular_regra(self):
        if self.estado == JOGANDO:
            self.calcular_regra_jogando()
        elif self.estado == PAUSADO:
            self.calcular_regra_pausado()

    def calcular_regra_pausado(self) :
        pass

    def calcular_regra_jogando(self):
        if (self.batida==5):
            self.batida = 0
            self.bola.VELOCIDADE += 1
        for movivel in self.lista_objetos:
            if (isinstance(movivel, Jogador_Humano)):
                ## testa hitbox na direita
                if self.bola.posicaoX + self.bola.raio == movivel.posicaoX+movivel.comprimento:
                    if movivel.posicaoY + movivel.altura >= self.bola.posicaoY + self.bola.raio >= movivel.posicaoY or\
                            movivel.posicaoY + movivel.altura >= self.bola.posicaoY - self.bola.raio >= movivel.posicaoY:
                        bola.velocidadeX = -1
                        bola.escolher_direcao()
                        self.batida += 1

                ## Testa hitbox na esquerda
                elif self.bola.posicaoX - self.bola.raio == movivel.posicaoX + movivel.comprimento:
                    if movivel.posicaoY + movivel.altura >= self.bola.posicaoY + self.bola.raio >= movivel.posicaoY or \
                            movivel.posicaoY + movivel.altura >= self.bola.posicaoY - self.bola.raio >= movivel.posicaoY:
                        bola.velocidadeX = 1
                        bola.escolher_direcao()
                        self.batida += 1

            if (isinstance(movivel, Bola)):

                if movivel.posicaoY<=0:## Testa se a bola bateu no teto
                    movivel.velocidadeY = movivel.VELOCIDADE
                    self.batida += 1
                elif movivel.posicaoY >= LARGURA_TELA: ## Testa se a bola bateu no chao
                    movivel.velocidadeY = -movivel.VELOCIDADE
                    self.batida += 1
                if movivel.posicaoX < 0 or movivel.posicaoX > COMPRIMENTO_TELA: ## testa se a bola passou por um dos lados
                    self.bola.VELOCIDADE = 1
                    self.batida = 0
                    if movivel.posicaoX <= 0:
                        movivel.velocidadeX = 1
                        self.player2_pontos += 1
                    elif movivel.posicaoX >= COMPRIMENTO_TELA:
                        movivel.velocidadeX = -1
                        self.player1_pontos += 1
                    movivel.posicaoX, movivel.posicaoY = COMPRIMENTO_TELA//2-self.comprimento, LARGURA_TELA//2
                    movivel.velocidadeY = 0

            movivel.calcular_regra()

    def processar_eventos(self, eventos):
        for e in eventos :
            if e.type == pygame.QUIT :
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if self.estado == PAUSADO:
                        self.estado = JOGANDO
                    else:
                        self.estado = PAUSADO

    def pintar(self, tela):
        if self.estado == JOGANDO:
            self.pintar_jogando(tela)
        else:
            self.pintar_pausado(tela)

    def pintar_pausado(self, tela):
        imagem_pausado = fonte.render("PAUSADO", True, AZUL, 0)
        tela.blit(imagem_pausado, (COMPRIMENTO_TELA//10, LARGURA_TELA-100))
        self.pintar_jogando(tela)


    def pintar_jogando(self, tela):
        self.player1_placar = f"Player 1: {self.player1_pontos}"
        self.player2_placar = f"Player 2: {self.player2_pontos}"
        imagem_player1 = fonte.render(self.player1_placar, True, CINZA, PRETO)
        imagem_player2 = fonte.render(self.player2_placar, True, CINZA, PRETO)
        pygame.draw.rect(tela, CINZA, (COMPRIMENTO_TELA//2-self.comprimento, 0, self.comprimento, LARGURA_TELA), 0)
        tela.blit(imagem_player1, (COMPRIMENTO_TELA//3 - COMPRIMENTO_TELA//10, 20))
        tela.blit(imagem_player2, (COMPRIMENTO_TELA //2 + COMPRIMENTO_TELA//10, 20))
        for movivel in self.lista_objetos:
            movivel.pintar(tela)

class Jogador_Humano(ElementoDoJogo):

    numero_jogador = 1
    def __init__(self, x, y, comprimento, largura):
        self.jogador = Jogador_Humano.numero_jogador
        self.velocidadeY = 0
        self.posicaoX = x
        self.posicaoY = y
        self.comprimento = comprimento
        self.altura = largura
        self.cor = AMARELO
        Jogador_Humano.numero_jogador += 1

    def pintar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.posicaoX, self.posicaoY, self.comprimento, self.altura), 0)


    def calcular_regra(self):
        self.posicaoY += self.velocidadeY
        if self.posicaoY + self.altura >= LARGURA_TELA or self.posicaoY<=0:
            self.posicaoY -= self.velocidadeY

    def processar_eventos(self, eventos):
        for e in eventos:
            if self.jogador == 1:
                if e.type == pygame.KEYDOWN:
                    if e.key == CIMA_Player1:
                        self.velocidadeY = -1
                    elif e.key == BAIXO_Player1:
                        self.velocidadeY = 1
                elif e.type == pygame.KEYUP:
                    if e.key == CIMA_Player1:
                        self.velocidadeY = 0
                    elif e.key == BAIXO_Player1:
                        self.velocidadeY = 0
            else:
                if e.type == pygame.KEYDOWN:
                    if e.key == CIMA_Player2:
                        self.velocidadeY = -1
                    elif e.key == BAIXO_Player2:
                        self.velocidadeY = 1
                elif e.type == pygame.KEYUP:
                    if e.key == CIMA_Player2:
                        self.velocidadeY = 0
                    elif e.key == BAIXO_Player2:
                        self.velocidadeY = 0

if __name__ == "__main__":
    comprimento_comum = COMPRIMENTO_TELA//30
    altura_comum = LARGURA_TELA//40
    jogador_um = Jogador_Humano(0, LARGURA_TELA//2, comprimento_comum // 2, altura_comum * 5)
    jogador_dois = Jogador_Humano(COMPRIMENTO_TELA - comprimento_comum//2, LARGURA_TELA//2, comprimento_comum//2, altura_comum * 5)
    bola = Bola(COMPRIMENTO_TELA//2, LARGURA_TELA//2, 20, AMARELO)
    cenario = Cenario(bola)
    cenario.adicionar_jogador([jogador_um, jogador_dois])


    while True:

        #Calcular Regras do jogo
        cenario.calcular_regra()
        print(cenario.batida)

        #Pintar tela
        tela.fill(PRETO)
        cenario.pintar(tela)
        pygame.display.update()



        ##Processar Eventos
        eventos = pygame.event.get()
        jogador_um.processar_eventos(eventos)
        jogador_dois.processar_eventos(eventos)
        cenario.processar_eventos(eventos)


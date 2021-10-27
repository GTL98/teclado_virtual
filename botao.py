import cv2


class Botao:
    def __init__(self, posicao, texto, tamanho=[85, 85]):
        self.posicao = posicao
        self.texto = texto
        self.tamanho = tamanho
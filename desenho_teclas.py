import cv2
import cvzone
import numpy as np

def desenhar_teclas_opacas(imagem, lista_botoes):
    for botao in lista_botoes:
        x, y = botao.posicao
        largura, altura = botao.tamanho
        cvzone.cornerRect(imagem, (x, y, largura, altura), 20, rt=0)
        cv2.rectangle(imagem, botao.posicao, (x+largura, y+altura), (255, 0, 255), cv2.FILLED)
        cv2.putText(imagem, botao.texto, (x+15, y+65),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    
    return imagem


def desenhar_teclas_transparentes(imagem, lista_botoes):
    imagem_nova = np.zeros_like(imagem, np.uint8)
    for botao in lista_botoes:
        x, y = botao.posicao
        largura, altura = botao.tamanho
        cvzone.cornerRect(imagem_nova, (x, y, largura, altura), 20, rt=0)
        cv2.rectangle(imagem_nova, botao.posicao, (x+largura, y+altura), (255, 0, 255), cv2.FILLED)
        cv2.putText(imagem_nova, botao.texto, (x+15, y+65),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        
        saida = imagem.copy()
        alfa = 0.5
        mascara = imagem_nova.astype(bool)
        saida[mascara] = cv2.addWeighted(imagem, alfa, imagem_nova, 1 - alfa, 0)[mascara]
        
    return saida

# 1. Importar as bibliotecas
import cv2
from botao import Botao
from pynput.keyboard import Controller
from cvzone.HandTrackingModule import HandDetector
from desenho_teclas import desenhar_teclas_opacas, desenhar_teclas_transparentes

# 2. Carregar o módulo de detecção
detector = HandDetector(maxHands=1, detectionCon=0.8, minTrackCon=0.8)

# 3. Definir o tamanho da tela
largura_tela = 1280
altura_tela = 720

# 4. Letras do teclado
teclas = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
         ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':'],
         ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', ' ']]

# 5. Definir o teclado
teclado = Controller()
ativo = 0  # se 0, escreve na tela de captura, se 1 escreve em qualquer lugar que desejar

# 6. Definir o texto que será mostrado na tela
texto_final = ''

# 7. Carregar o módulo do desenhos dos botões
lista_botoes = []
for linha in range(len(teclas)):
    for x, tecla in enumerate(teclas[linha]):
        lista_botoes.append(Botao([100*x+50, 50+linha*100], tecla))

# 8. Definir a transparência
transparencia = 0  # por algum motivo (acretido ser o poder de processamento), usar transparência cai muito o FPS

# 9. Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, largura_tela)
cap.set(4, altura_tela)

while True:
    # Detectar as mãos
    _, imagem = cap.read()
    imagem = cv2.flip(imagem, 1)
    maos, imagem = detector.findHands(imagem, flipType=False)

    # Desenhar os botões na tela
    if transparencia == 0:
        imagem = desenhar_teclas_opacas(imagem, lista_botoes)
    elif transparencia == 1:
        imagem = desenhar_teclas_transparentes(imagem, lista_botoes)

    if maos:
        lista_landmark = maos[0]['lmList']
        cursor = lista_landmark[8]  # ponta do dedo indicador
        for botao in lista_botoes:
            x, y = botao.posicao
            largura_botao, altura_botao = botao.tamanho
            
            # Verifcar em qual botão o indicador está
            if x < cursor[0] < x + largura_botao and y < cursor[1] < y + altura_botao:
                cv2.rectangle(imagem, (x - 5, y - 5), (x+largura_botao+5, y+altura_botao+5), (175, 0, 175), cv2.FILLED)
                cv2.putText(imagem, botao.texto, (x+15, y+65),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                comprimento, info = detector.findDistance(lista_landmark[8], lista_landmark[12])
                
                # Veficar se foi clicado o botão
                if comprimento < 30:
                    if ativo == 1:
                        teclado.press(botao.texto)
                    cv2.rectangle(imagem, botao.posicao, (x+largura_botao, y+altura_botao), (0, 255, 0), cv2.FILLED)
                    cv2.putText(imagem, botao.texto, (x+15, y+65),
                                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                    texto_final += botao.texto
                    cv2.waitKey(150)
                    
    if ativo == 0:
        # Fazer o lugar de onde será mostrado o texto
        cv2.rectangle(imagem, (50, 500), (700, 600), (255, 255, 255), cv2.FILLED)
        cv2.putText(imagem, texto_final, (60, 575),
                    cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            
    # Mostrar a imagem na tela
    cv2.imshow('Teclado Virtual', imagem)
    
    # Terminar o loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
        
# 10. Fechar a tela de captura
cap.release()
cv2.destroyAllWindows()
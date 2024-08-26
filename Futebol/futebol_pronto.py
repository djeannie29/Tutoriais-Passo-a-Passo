import cv2
import sys
from random import randint

# Abrir o vídeo
cap = cv2.VideoCapture("C:/futebol/futebol2.mp4")

ok, frame = cap.read()
if not ok:
    print("Não foi possível ler o arquivo")
    sys.exit(1)

bboxes = []
colors = []

# Adicionar instrução no frame
instructions = "Desenhe uma caixa sobre o objeto a ser rastreado, em seguida clique em Enter e na letra X"
cv2.putText(frame, instructions, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow('Tracker', frame)
cv2.waitKey(2000)  # Mostra a instrução por 2 segundos

# Selecionar as caixas delimitadoras
while True:
    bbox = cv2.selectROI('Tracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    print("Pressione X para sair ou qualquer outra tecla para continuar a selecionar o próximo objeto")
    k = cv2.waitKey(0) & 0XFF
    if k == 120:  # X para sair
        break

# Se a versão do OpenCV for menor que 4.5, usar o módulo legacy
tracker = cv2.legacy.TrackerCSRT_create()
multitracker = cv2.legacy.MultiTracker_create()

# Adicionar as caixas delimitadoras ao rastreador
for bbox in bboxes:
    multitracker.add(tracker, frame, bbox)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    # Atualizar o rastreador
    ok, boxes = multitracker.update(frame)

    # Desenhar as caixas delimitadoras e coordenadas na imagem
    for i, newbox in enumerate(boxes):
        (x, y, w, h) = [int(v) for v in newbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), colors[i], 2)
        # Adicionar o texto com as coordenadas
        coords_text = f"x: {x}, y: {y}, w: {w}, h: {h}"
        cv2.putText(frame, coords_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[i], 1)

    # Adicionar mensagens informativas na tela na parte superior
    instructions = "Pressione 'ESC' para sair do rastreamento."
    cv2.putText(frame, instructions, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Exibir a imagem com as caixas delimitadoras, coordenadas e mensagens
    cv2.imshow('MultiTracker', frame)

    # Verificar tecla pressionada para sair
    if cv2.waitKey(1) & 0XFF == 27:  # ESC para sair
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

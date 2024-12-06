import cv2

# Caminho para o vídeo
video_path = 'Projeto.mov'
cap = cv2.VideoCapture(video_path)

# Lista para armazenar posições das vagas de estacionamento
parking_positions = [
    (550, 450, 190, 110),  # Vaga 8
    (550, 600, 190, 110),  # Vaga 9
    (550, 500, 190, 120),  # Vaga 10
    (1050, 450, 190, 110),  # Vaga 8
    (1050, 600, 190, 110),  # Vaga 9
    (1050, 500, 190, 120),  # Vaga 10
]


# Função para detectar se uma vaga está ocupada com base nos contornos
def is_occupied(roi):
    # Converter a ROI para escala de cinza
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Aplicar um limiar para binarizar a imagem
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Encontrar contornos na imagem binária
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos pequenos, que provavelmente são ruídos
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # Se houver contornos significativos, consideramos a vaga ocupada
    return len(contours) > 0


# Processar o vídeo e contar vagas
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    occupied_count = 0
    free_count = 0

    for position in parking_positions:
        # Extrair a região de interesse (ROI) para cada vaga
        x, y, w, h = position
        roi = frame[y:y + h, x:x + w]

        # Determinar se a vaga está ocupada
        if is_occupied(roi):
            occupied_count += 1
            color = (0, 0, 255)  # Vermelho para ocupado
        else:
            free_count += 1
            color = (0, 255, 0)  # Verde para livre

        # Desenhar retângulo ao redor da vaga
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Mostrar contagem no frame
    cv2.putText(frame, f'Ocupadas: {occupied_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Livres: {free_count}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exibir frame
    cv2.imshow("Estacionamento", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.getWindowProperty('Estacionamento', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()

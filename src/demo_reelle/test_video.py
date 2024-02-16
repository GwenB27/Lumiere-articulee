import cv2
import numpy as np
import matplotlib.pyplot as plt

video_device_index = 0

cap = cv2.VideoCapture(video_device_index)

if not cap.isOpened():
    print("Impossible d'ouvrir la caméra")
    exit()

frame_count = 0
qr_count = 0

start_time = cv2.getTickCount()

plt.ion()  # Activer le mode interactif pour afficher les images en temps réel
fig, ax = plt.subplots()


def update_display(image):
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.01)

def close_display():
    plt.ioff()
    plt.close()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erreur lors de la lecture de la trame.")
        break

    frame_count += 1
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)

    if points is not None:
        qr_count += len(points)
        

        for i, point_set in enumerate(points):
            
            print("QR Code", i + 1, "points:", point_set)

            # Convertir tous les points en entiers 32 bits signés
            point_set = np.int32(point_set)

            # Utiliser le polygone des points convertis pour polylines
            cv2.polylines(frame, [point_set], isClosed=True, color=(0, 255, 0), thickness=2)

            # Votre code de calcul de distance et d'autres traitements ici
            # Calculer le centre moyen des QR codes détectés
            if len(point_set) >= 2:
                x_bleu2 =0
                y_bleu2 = 0 
                print("points : ", point_set)
                x_values = [point[0] for point in point_set]
                y_values = [point[1] for point in point_set]

                # on cherche le centre du QR code et on l'affiche
                x_weight = sum(point[0] for point in point_set) / len(point_set)
                y_weight = sum(point[1] for point in point_set) / len(point_set)
                print(" poid des x et y :", x_weight, " et ", y_weight)

                # Ajouter un point bleu au niveau des coordonnées x_weight et y_weight
                cv2.circle(frame, (int(x_weight), int(y_weight)), 5, (255, 0, 0), -1)

                if i == 0 :
                    x_bleu = int(x_weight)
                    y_bleu = int(y_weight)
                
                else: 
                    x_bleu2 = int(x_weight)
                    y_bleu2 = int(y_weight)
                    # Calculer le milieu entre les deux points bleus
                    distance_x = (x_bleu+x_bleu2 )/2
                    distance_y = (y_bleu+y_bleu2 )/2
                    print(" Coordonees point rouge :", distance_x, " , ", distance_y)
                    center_red = (int(distance_x), int(distance_y))

                    # Ajouter un point rouge au centre équidistant des points bleus
                    cv2.circle(frame, center_red, 5, (0, 0, 255), -1)

                

        # Afficher la trame avec les codes QR dessinés
        update_display(frame)

    # Afficher le nombre de codes QR détectés toutes les 5 secondes
    # if frame_count == 5:
    #     end_time = cv2.getTickCount()
    #     elapsed_time = (end_time - start_time) / cv2.getTickFrequency()
    #     actual_fps = frame_count / elapsed_time
    #     print(f"Nombre de codes QR détectés : {qr_count}")
    #     print(f"FPS de la caméra (calculé) : {actual_fps}")
    #     frame_count = 0
    #     qr_count = 0
    #     start_time = cv2.getTickCount()


# Libérer la capture et fermer la fenêtre d'affichage
cap.release()
close_display()

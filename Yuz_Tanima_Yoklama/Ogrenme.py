# Ogrenme.py
# Created/Modified files during execution:
#  - trainer/trainer.yml

import cv2
import numpy as np
import os
from PIL import Image

def getImagesAndLabels(path):
    # resimler ve etiketler için boş listeler
    faceSamples = []
    ids = []

    # path içindeki dosyaları listele
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]

    for imagePath in imagePaths:
        # Görüntüyü gri formatta aç
        pil_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(pil_img, 'uint8')

        # Dosya adından ID bilgisi çekme (ör: face_1_ali_veli_1.jpg -> ID = 1)
        filename = os.path.split(imagePath)[-1]
        # Örnek dosya adı yüzünden ID'yi parse etme (face_<id>_...)
        # Burada dosya adını '_' ile ayırıp 1. indexi ID olarak alalım.
        try:
            id_str = filename.split('_')[1]
            face_id = int(id_str)
        except:
            face_id = 0  # parse edilemezse 0

        faceSamples.append(img_numpy)
        ids.append(face_id)

    return faceSamples, ids

def main():
    path = 'yuzler'
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    print("\n[INFO] Yüzleri ve ID'leri alıyorum. Lütfen bekleyin...")
    faces, ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    # trainer klasörü yoksa oluştur
    if not os.path.exists('trainer'):
        os.makedirs('trainer')

    # Eğitilen modeli kaydet
    recognizer.write('trainer/trainer.yml')

    print(f"\n[INFO] {len(np.unique(ids))} farklı ID için yüz eğitimi tamamlandı.")

if __name__ == "__main__":
    main()
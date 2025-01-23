# Tanima.py
# Created/Modified files during execution:
#  - sinif_listesi.xls (okuma-yazma yapar, ancak mevcut satırları korur.)
#  - Yoklamaya dair ek kayıtlar (örnek bir CSV ya da Xls dosyası yazabilirsiniz.)

import cv2
import xlrd
from xlwt import Workbook, easyxf
import os
import numpy as np
from datetime import datetime

def load_excel_data(excel_file):
    """
    Excel dosyasını okuyarak
    ID -> (Ad, Soyad, Sinif) bilgisini
    bir sözlük (dict) olarak döndürür.
    """
    if not os.path.exists(excel_file):
        print(f"{excel_file} bulunamadı. Lütfen dosya oluşturun veya düzenleyin.")
        return {}

    book = xlrd.open_workbook(excel_file)
    sheet = book.sheet_by_index(0)

    # Excel'de ilk satırı (Numara, Ad, Soyad, Sinif) başlık olarak kabul edelim
    # ID (Numara) -> (Ad, Soyad, Sinif)
    data_dict = {}
    for rowx in range(1, sheet.nrows):  # ilk satırı atla
        row = sheet.row_values(rowx)
        try:
            numara = int(row[0])
            ad = str(row[1])
            soyad = str(row[2])
            sinif = str(row[3])
            data_dict[numara] = (ad, soyad, sinif)
        except:
            continue
    return data_dict

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Daha önce eğitilmiş modeli yükle
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')

    # Excel dosyası
    excel_file = 'sinif_listesi.xls'
    id_info_dict = load_excel_data(excel_file)

    # Kamera aç
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    print("\n[INFO] Tanıma modu aktif. 'q' tuşu ile çıkabilirsiniz.")

    while True:
        ret, img = cam.read()
        if not ret:
            print("Kamera okunamadı, çıkılıyor...")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(50, 50)
        )

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            # Tanıma yap
            id_, confidence = recognizer.predict(roi_gray)

            # confidence değeri 100'e ne kadar yakınsa o kadar az güven demektir
            # pratikte 0-100 arası (bazı durumlarda 0-50 iyi, 50-100 kötü tanıma vb.)
            if confidence < 60:
                # Excel'den ID bilgilerini çek
                if id_ in id_info_dict:
                    ad, soyad, sinif = id_info_dict[id_]
                    text = f"{id_} {ad} {soyad} - {sinif}"
                else:
                    text = f"ID {id_} (Excel Kaydı Yok)"
            else:
                text = "Bilinmeyen"

            # Dikdörtgen çizin
            color = (0, 255, 0) if "Bilinmeyen" not in text else (0, 0, 255)
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow('Yuz Tanima', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
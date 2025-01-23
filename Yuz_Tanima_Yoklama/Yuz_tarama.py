# Created/Modified files during execution:
#  - yuzler/...
#  - sinif_listesi.xls

import cv2
import os
import xlrd
import xlwt

def add_entry_to_excel(excel_file, numara, ad, soyad, sinif):
    """
    sinif_listesi.xls dosyasına yeni bir öğrenci kaydı (Numara, Ad, Soyad, Sinif) ekler.
    Eğer dosya yoksa başlık satırıyla birlikte yeni bir dosya oluşturur.
    Varsa, mevcut verileri korur ve yeni satırın sonuna ekler.
    """

    if not os.path.exists(excel_file):
        # Eğer dosya yoksa => başlık satırlı, tek satırlık örnek Excel oluştur
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Sheet1")
        # Başlıklar
        sheet.write(0, 0, "Numara")
        sheet.write(0, 1, "Ad")
        sheet.write(0, 2, "Soyad")
        sheet.write(0, 3, "Sinif")
        # İlk veriyi yaz
        sheet.write(1, 0, numara)
        sheet.write(1, 1, ad)
        sheet.write(1, 2, soyad)
        sheet.write(1, 3, sinif)

        workbook.save(excel_file)
        print(f"{excel_file} oluşturuldu ve ilk kayıt eklendi.")
    else:
        # Mevcut dosyayı oku
        book = xlrd.open_workbook(excel_file)
        sheet = book.sheet_by_index(0)
        
        # Mevcut satır sayısı
        row_count = sheet.nrows  
        
        # Tüm veriyi hafızaya kopyalayacağız
        all_data = []
        for rx in range(row_count):
            row_values = sheet.row_values(rx)
            all_data.append(row_values)
        
        # row_count satır var, biz yeni veriyi row_count konumuna ekleyeceğiz
        
        # xlwt ile yeni bir workbook oluştur
        workbook = xlwt.Workbook()
        new_sheet = workbook.add_sheet("Sheet1")
        
        # Önce var olan satırları kopyala
        for r in range(row_count):
            row_values = all_data[r]
            for c, val in enumerate(row_values):
                new_sheet.write(r, c, val)
        
        # Yeni veriyi ekle (numara, ad, soyad, sinif)
        new_sheet.write(row_count, 0, numara)
        new_sheet.write(row_count, 1, ad)
        new_sheet.write(row_count, 2, soyad)
        new_sheet.write(row_count, 3, sinif)
        
        # Kaydet
        workbook.save(excel_file)
        print(f"{excel_file} dosyasına yeni kayit eklendi: {numara}, {ad}, {soyad}, {sinif}")

def main():
    """
    Kameradan 30 adet yüz görüntüsü alarak
    'yuzler' klasörüne kaydeder ve
    sinif_listesi.xls dosyasına da ID, Ad, Soyad, Sinif bilgisini ekler.
    """
    # Haar Cascade yüz algılama için hazır xml dosyası (OpenCV ile geliyor)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Kişi bilgilerini kullanıcıdan al
    face_id = input("Kayıt için bir yüz ID numarası (örn: 1) giriniz: ")
    ad = input("Kişinin Adı: ")
    soyad = input("Kişinin Soyadı: ")
    sinif = input("Kişinin Sınıfı: ")

    # Excel'e bu kaydı ekleyelim (ID=Numara varsayımıyla)
    excel_file = 'sinif_listesi.xls'
    try:
        add_entry_to_excel(excel_file, int(face_id), ad, soyad, sinif)
    except ValueError:
        # face_id int'e çevrilemezse, 0 veya -1 gibi bir değer kullanın
        add_entry_to_excel(excel_file, 0, ad, soyad, sinif)

    # Kaydedilecek yüzler klasörü yoksa oluştur
    if not os.path.exists('yuzler'):
        os.makedirs('yuzler')

    # Kamera başlat
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Genişlik
    cam.set(4, 480)  # Yükseklik

    print("\n[INFO] Kamerayı açtım, yüz yakalamak için bekliyorum...")

    count = 0  # kaç fotoğraf çektiğimizi sayacağız

    while True:
        ret, img = cam.read()
        if not ret:
            print("[ERR] Kamera okunamadı, çıkılıyor...")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(50, 50)
        )

        for (x, y, w, h) in faces:
            # Yüz için dikdörtgen çiz
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Yüz bölgesini kırp, kaydet
            face_img = gray[y:y+h, x:x+w]
            count += 1

            # yüzler klasörüne kaydet (ID, Ad, Soyad gibi ek bilgiler dosya adında tutulabilir)
            file_name = f"yuzler/face_{face_id}_{ad}_{soyad}_{str(count)}.jpg"
            cv2.imwrite(file_name, face_img)

            cv2.putText(img, f"Kaydediliyor {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Yuz Tarama', img)

        # 30 fotoğraf çekince otomatik çık ya da 'q' tuşuna basınca çık
        if (count >= 30) or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    print("\n[INFO] Program sonlandırılıyor. Yüz kayıtları tamam.")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
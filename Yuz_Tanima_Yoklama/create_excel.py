import xlwt

def create_excel_file(file_name="sinif_listesi.xls"):
    # Yeni bir çalışma kitabı (workbook) oluştur
    workbook = xlwt.Workbook()

    # Bir sayfa ekle (varsayılan adı "Sheet1")
    sheet = workbook.add_sheet("Sheet1")

    # İlk satıra (index 0) sütun başlıklarını yazalım:
    sheet.write(0, 0, "Numara")
    sheet.write(0, 1, "Ad")
    sheet.write(0, 2, "Soyad")
    sheet.write(0, 3, "Sinif")

    # Örnek veri satırı ekleyelim (index 1):
    sheet.write(1, 0, 1)           # Numara
    sheet.write(1, 1, "Ali")      # Ad
    sheet.write(1, 2, "Yılmaz")   # Soyad
    sheet.write(1, 3, "10-A")     # Sinif

    # İsterseniz ek satırlar eklemeye devam edebilirsiniz
    # sheet.write(2, 0, 2)
    # sheet.write(2, 1, "Ayşe")
    # sheet.write(2, 2, "Demir")
    # sheet.write(2, 3, "10-B")

    # Çalışma kitabını kaydet
    workbook.save(file_name)
    print(f"'{file_name}' başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_excel_file("sinif_listesi.xls")
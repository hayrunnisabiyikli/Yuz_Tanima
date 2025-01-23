# Yüz Tanıma ve Sınıf Yönetim Sistemi

Bu proje, yüz tanıma teknolojisini kullanarak bir sınıf yönetim sistemi oluşturmayı amaçlar. Sistem, öğrencilerin yüzlerini tanıyarak kimlik bilgilerini ekrana yansıtır ve sınıf listesiyle entegre bir şekilde çalışır. Proje, üç ana Python dosyasından oluşur: `yuz_tarama.py`, `ogrenme.py` ve `tanima.py`.

## Çalışma Akışı

1. **`yuz_tarama.py`**:

   - Kullanıcıdan ID, ad, soyad ve sınıf bilgileri alınır.
   - Kameradan 30 adet yüz görüntüsü yakalanır ve `yuzler` klasörüne kaydedilir.
   - Kullanıcının bilgileri `sinif_listesi.xls` dosyasına eklenir.
2. **`ogrenme.py`**:

   - `yuzler` klasöründeki yüz görüntüleri ve ID bilgileri kullanılarak LBPH algoritması ile yüz tanıma modeli eğitilir.
   - Eğitilen model `trainer/trainer.yml` dosyasına kaydedilir.
3. **`tanima.py`**:

   - Eğitilen model kullanılarak kameradan alınan görüntülerdeki yüzler tanınır.
   - Tanınan yüzlerin bilgileri `sinif_listesi.xls` dosyasından alınır ve ekranda gösterilir.

---

## Proje Dosyaları

### 1. `yuz_tarama.py`

Bu dosya, yeni bir kişinin yüzünü kaydetmek ve bilgilerini sınıf listesine eklemek için kullanılır.

#### İşlevler:

- Kullanıcıdan ID, ad, soyad ve sınıf bilgilerini alır.
- Kameradan 30 adet yüz görüntüsü yakalar ve `yuzler` klasörüne kaydeder.
- Kullanıcının bilgilerini `sinif_listesi.xls` dosyasına ekler.

#### Kullanım:

1. `yuz_tarama.py` dosyasını çalıştırın.
2. İstenilen bilgileri girin ve yüz kaydını tamamlayın.

---

### 2. `ogrenme.py`

Bu dosya, yüz tanıma modelini eğitmek için kullanılır.

#### İşlevler:

- `yuzler` klasöründeki yüz görüntülerini ve ID bilgilerini alır.
- LBPH algoritması ile yüz tanıma modelini eğitir.
- Eğitilen modeli `trainer/trainer.yml` dosyasına kaydeder.

#### Kullanım:

1. `yuz_tarama.py` ile yüz görüntülerini kaydedin.
2. `ogrenme.py` dosyasını çalıştırarak modeli eğitin.

---

### 3. `tanima.py`

Bu dosya, kameradan alınan görüntülerdeki yüzleri tanımak için kullanılır.

#### İşlevler:

- Eğitilen modeli (`trainer/trainer.yml`) kullanarak yüz tanıma yapar.
- Tanınan yüzlerin bilgilerini `sinif_listesi.xls` dosyasından alır.
- Tanınan yüzleri ekranda gösterir ve kimlik bilgilerini görüntüler.

#### Kullanım:

1. `ogrenme.py` ile modeli eğitin.
2. `tanima.py` dosyasını çalıştırarak yüz tanıma işlemini başlatın.

---

## Gereksinimler

- Python 3.x
- OpenCV
- NumPy
- xlrd
- xlwt
- PIL (Pillow)

### Kurulum

1. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install opencv-python numpy xlrd xlwt pillow
   ```

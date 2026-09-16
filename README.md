# Webcam AR Yapboz 🧩

Bu proje, bilgisayarınızın web kamerasını ve el hareketlerinizi kullanarak gerçek zamanlı bir yapboz (puzzle) oyununa dönüşür. Klavyeye veya fareye ihtiyacınız yoktur; her şeyi tamamen el hareketlerinizle kontrol edersiniz!

## 🌟 Özellikler
* **El İşaretleriyle Kontrol:** Oyun tamamen OpenCV ve MediaPipe kullanılarak el takibi (hand tracking) ile çalışır.
* **Kendi Yapbozunu Yarat:** Kamerada iki elinle bir dikdörtgen çerçeve çizerek ortamdaki herhangi bir nesneyi veya kendini yapboza dönüştürebilirsin.
* **Sürükle & Bırak:** Baş ve işaret parmağını birleştirerek (çimdik hareketi) yapboz parçalarını tutup yerlerini değiştirebilirsin.
* **Akıllı Sıfırlama:** Oyunu baştan başlatmak veya yeni bir fotoğraf çekmek istersen sadece elini yumruk yapman yeterli.

## 🛠️ Kurulum

Bilgisayarınızda Python yüklü olmalıdır. Proje dizininde terminali açıp aşağıdaki adımları izleyin:

1. Gerekli kütüphaneleri yükleyin:
```bash
pip3 install -r requirements.txt
```

*(Not: Eğer Mac cihazınızda MediaPipe ile ilgili çökme hatası alırsanız, `pip3 install mediapipe==0.10.9` komutuyla stabil sürümü yükleyebilirsiniz).*

2. Oyunu başlatın:
```bash
python3 main.py
```

## 🎮 Nasıl Oynanır?

Oyun iki aşamadan oluşur:

### 1. Aşama: Fotoğraf Çekme (Çerçeveleme)
* İki elinizi kameraya gösterin. Sağ ve sol **işaret parmaklarınızın uçları** çerçevenin köşelerini belirler (ekranda sarı bir kutu göreceksiniz).
* Çerçeveyi ayarladıktan sonra, pozisyonu bozmadan **her iki elinizle aynı anda "Çimdik"** (baş parmak ile işaret parmağını birleştirme) yapın.
* Fotoğraf çekilecek ve 16 parçalı karışık bir yapboz halinde karşınıza gelecektir.

### 2. Aşama: Bulmacayı Çözme
* Ekranda tek elinizi kullanmanız yeterlidir. İşaret parmağınızın ucu fareniz (imleç) gibi çalışır.
* Yanlış yerdeki bir parçanın üstüne gelin, **"Çimdik"** yapıp basılı tutarak parçayı istediğiniz yere sürükleyin ve çimdiği bırakın.
* Tüm parçalar doğru sıraya geldiğinde oyunu kazanırsınız!

### 🔄 Başa Sarma
Oyundan sıkıldıysanız veya fotoğrafı yanlış çektiyseniz, kameraya karşı elinizi **Yumruk** yapın. Bu hareket mevcut yapbozu iptal edip en başa (fotoğraf çekme aşamasına) dönmenizi sağlar.

## 💻 Kullanılan Teknolojiler
* **Python 3**
* **OpenCV** (Görüntü işleme ve arayüz çizimleri)
* **MediaPipe** (Yapay zeka destekli el ve eklem takibi)

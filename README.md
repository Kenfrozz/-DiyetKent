# DiyetKent - Google Sheets ile Masaüstü Uygulama
DiyetKent, Google Sheets veritabanını kullanarak verileri yönetmek üzere tasarlanmış, PyQt5 tabanlı bir masaüstü uygulamasıdır. Bu uygulama, kullanıcılara verileri görüntüleme, düzenleme ve silme yetenekleri sunar.
---

## Özellikler
- **Google Sheets entegrasyonu**: Dinamik veri alma ve güncelleme.
- **PyQt5 arayüzü**: Kullanış odaklı masaüstü uygulama.
- **Veri düzenleme**: Seçilen satırları düzenleyebilme.
- **Veri silme**: Satır bazında veri silme işlemleri.
- **Asenkron işlem desteği**: Hızlı ve kesintisiz veri yükleme.

---

## Gereksinimler
- **Python**: 3.7 veya daha üstü
- **Google Sheets API**: Yetkilendirilmiş bir servis hesabı (Service Account)

---

## Kurulum

### 1. Projeyi Klonlayın
Projeyi yerel bilgisayarınıza klonlayın veya ZIP formatında indirin:
```bash
git clone https://github.com/kullaniciadi/DiyetKent.git
cd DiyetKent
```

### 2. Gerekli Kütüpaneleri Yükleyin
Python kütüpanelerini **requirements.txt** dosyasından yükleyin:
```bash
pip install -r requirements.txt
```

### 3. Google Sheets API Yapılandırması
1. [Google Cloud Console](https://console.cloud.google.com/) üzerinden bir proje oluşturun.
2. "Service Account" oluşturun ve JSON kimlik dosyasını indirin.
3. Bu dosyayı proje dizinine **credentials.json** adıyla yerleştirin.
4. Google Sheets belgesini oluşturun ve Service Account e-posta adresini paylaşım izinlerine ekleyin.

---

## Kullanım

### Uygulamayı Başlatma
Uygulamayı aşağıdaki komutla başlatın:
```bash
python main.py
```

### Uygulama Penceresi
- **Veri Tablosu**: Google Sheets'ten yüklenen verileri görüntüleyin.
- **Düzenle ve Sil**: Her satır için ilgili düğmeler kullanılabilir.

---

## Ekran Görüntüleri
- **Ana Tablo Görüntüsü**: Veriler görüntülenir ve satır işlemleri yapılabilir.
- **Düzenleme Diyaloğu**: Seçilen satırları düzenlemek için pop-up pencere.

---

## Teknik Detaylar

### Kullanılan Teknolojiler
- **Python**: Ana programlama dili.
- **PyQt5**: Masaüstü uygulama arayüzü için.
- **gspread**: Google Sheets API entegrasyonu.
- **google-auth**: Yetkilendirme işlemleri için.

### Dosya Yapısı
- `main.py`: Ana uygulama dosyası.
- `credentials.json`: Google Sheets API yetkilendirme dosyası.
- `requirements.txt`: Gerekli Python kütüpanelerini listeleyen dosya.

---

## Geliştirici Notları
- **Genişletilebilirlik**: Daha fazla özellik eklemek üzere uygulama modülerı ayrılarak yapılandırılmıştır.
- **Hata Ayıklama**: Uygulama hata mesajlarıyla birlikte kullanıcı dostu uyarılar göstermektedir.


---

## Lisans
Bu proje, MIT lisansı altında sunulmaktadır. Daha fazla bilgi için `LICENSE` dosyasını inceleyebilirsiniz.


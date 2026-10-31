# 🏥 SağlıkNet - Hasta Kayıt ve Yönetim Sistemi

Python ve Tkinter kullanılarak geliştirilmiş, modern arayüze sahip, SQLite veritabanı destekli masaüstü **Hasta Kayıt ve Takip Uygulaması**.

---

## 🌟 Özellikler

1. **Hasta Kayıt (Ekleme)**:
   - T.C. Kimlik Numarası (11 haneli sayı kontrolü ve mükerrer kayıt engelleme)
   - Ad ve Soyad
   - Cinsiyet ve Kan Grubu seçimi
   - Doğum Tarihi / Yaş bilgisi
   - İletişim Telefonu
   - Poliklinik / Tıbbi Bölüm seçimi (14+ poliklinik seçeneği)
   - Hasta Şikayeti / Ön Muayene & Doktor Notları

2. **Dinamik Tablo & Listeleme**:
   - Modern `ttk.Treeview` tablo tasarımı ve alternatif satır renklendirmesi (Zebra striping)
   - Çift tıklama ile hastanın detaylı tıbbi dosyasını açma
   - Tek tıklama ile hasta bilgilerini anında düzenleme formuna aktarma

3. **Anlık Arama & Poliklinik Filtreleme**:
   - Klavyeden yazıldığı anda canlı filtreleme (T.C. Kimlik No, İsim veya Soyisme göre)
   - Bölümlere / Polikliniklere göre tek tıkla filtreleme

4. **Hasta Bilgilerini Güncelleme & Güvenli Silme**:
   - Mevcut hastanın iletişim veya tıbbi bilgilerini kolayca düzenleme
   - Onay pencereli güvenli kayıt silme mekanizması

5. **📋 Detaylı Hasta Kartı (Modal Pencere)**:
   - Hastanın tüm kişisel ve iletişim bilgilerini, başvurduğu polikliniği ve uzun klinik şikayet metnini kart şeklinde görüntüleme

6. **📊 Poliklinik & Kayıt İstatistikleri**:
   - Toplam hasta sayısı, polikliniklere göre hasta dağılımı ve yüzdelik oranları gösteren istatistik paneli

7. **📥 Excel / CSV Dışa Aktarma**:
   - Sistemdeki tüm veya filtrelenmiş hasta kayıtlarını Türkçe karakter uyumlu (`UTF-8 with BOM`) olarak tek tıkla Excel/CSV formatında kaydetme

---

## 🛠️ Gereksinimler & Kurulum

Bu uygulama Python'ın standart kütüphaneleri (`tkinter`, `sqlite3`, `csv`) ile geliştirilmiştir. Ekstra hiçbir dış kütüphane (`pip install`) gerektirmez.

- **Python 3.8+** (Bilgisayarınızda yüklü olması yeterlidir)

---

## 🚀 Uygulamayı Çalıştırma

Terminal veya Komut Satırında (PowerShell / CMD) proje dizinine gelip şu komutu çalıştırın:

```bash
python main.py
```

Uygulama ilk kez açıldığında örnek birkaç hasta kaydı ile birlikte otomatik olarak `hasta_kayit.db` dosyasını oluşturacaktır.

---

## 📁 Proje Dosya Yapısı

```
yapayzeka/
│
├── main.py          # Modern Tkinter kullanıcı arayüzü ve olay yönetimi
├── database.py      # SQLite veritabanı CRUD işlemleri ve sorgular
├── hasta_kayit.db   # SQLite yerel veritabanı dosyası (otomatik oluşturulur)
└── README.md        # Proje tanıtım ve kullanım kılavuzu
```


# 🎯 Kariyer ve Vizyon Asistanı (YKS & Kariyer Rehberlik Platformu)

12. Sınıf YKS adayları ve kariyerini şekillendirmek isteyen öğrenciler için geliştirilmiş, statik listeler yerine tamamen dinamik bir koçluk mantığıyla çalışan **Yapay Zekâ ve Test Destekli Kariyer Planlama Platformu**.

---

## 🚀 Projenin Amacı ve Özellikleri

Bu sistem, öğrencilerin lise son sınıftaki sınav stresini azaltmak ve onlara kendi potansiyellerine uygun geleceğin en vizyoner mesleklerini tanıtmak amacıyla tasarlanmıştır:
- **Envanter ve Analiz:** Öğrencinin verdiği yanıtları analiz ederek en uygun kariyer alanını belirler.
- **Dinamik Kıyaslama Matrisi:** Seçilen alandaki gözde mesleklerin avantajlarını, dezavantajlarını ve maaş potansiyellerini listeler.
- **Rol Simülasyonu:** Mesleklerin eğitim süreçleri, günlük çalışma tempoları ve zorluklarını gözler önüne serer.
- **Akıllı YKS & Gelişim Yol Haritası:** Tıklanan herhangi bir meslek için arka plandaki akıllı motor sayesinde **YKS Puan Türü, Hedef Sıralama, Ağırlık Verilmesi Gereken Dersler ve Çalışma Stratejisi** üretir.
- **Kişiselleştirilmiş Haftalık Ders Çalışma Programı:** Öğrencinin alanına özel (Sayısal, Eşit Ağırlık, Sözel) haftalık YKS kamp programı sunar.

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, Flask, Jinja2
- **Veritabanı Entegrasyonu:** Oracle Database (`oracle-26ai`)
- **Frontend:** HTML5, CSS3, Modern Responsive Tasarım

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda (Ubuntu/Linux/Windows) çalıştırmak için şu adımları izleyin:

1. **Projeyi Klonlayın veya İndirin:**
   ```bash
   git clone [https://github.com/marfusha1986/kariyer-vizyon-asistani.git](https://github.com/marfusha1986/kariyer-vizyon-asistani.git)
   cd kariyer-vizyon-asistani

Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin:

Bash
python3 -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
Gerekli Kütüphaneleri Yükleyin:

Bash
pip install -r requirements.txt
Uygulamayı Başlatın:

Bash
python app.py
Tarayıcınızda Açın:
Tarayıcınıza http://127.0.0.1:5000 adresini yazarak platformu kullanmaya başlayabilirsiniz.

📂 Proje Mimarisi
Plaintext
kariyer-vizyon-asistani/
│
├── app.py                 # Ana Flask uygulama ve akıllı yönlendirme motoru
├── requirements.txt       # Proje bağımlılıkları
├── README.md              # Proje dokümantasyonu
├── static/                # CSS ve statik varlıklar
│   └── css/
│       └── style.css
└── templates/             # HTML şablonları
    ├── index.html
    ├── test.html
    ├── sonuclar.html
    ├── karsilastirma.html
    ├── simulasyon.html
    ├── yol_haritasi.html
    ├── ders_programi.html
    └── bitti.html
💡 Geliştirici Notu
Bu sistem; 12. sınıf öğrencilerinin sadece sınav odaklı değil, geleceğin teknolojilerini ve mesleklerini kavrayarak bilinçli bir kariyer vizyonu çizmeleri için sevgiyle kodlanmıştır. Başarılar dileriz! ✨


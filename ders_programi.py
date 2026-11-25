def _g(gun, odak, detay):
    return {
        'gun': gun,
        'odak': odak,
        'detay': detay,
    }


DERS_PROGRAMLARI = {
    'SAYISAL': {
        'temel': {
            'program_adi': 'Sayısal Temel Kurma ve Eksik Yakalama Programı',
            'gunler': [
                _g('Pazartesi', 'Temel Matematik & Okuma Alışkanlığı', '45 dk dört işlem, oran-orantı ve denklem temelleri; 25 dk kısa paragraf okuma ve anlam çıkarma.'),
                _g('Salı', 'Temel Fen Kavramları & Dil Bilgisi', '45 dk kuvvet-hareket veya madde yapısı temel kavramları; 30 dk cümle öğeleri ve yazım/noktalama pratiği.'),
                _g('Çarşamba', 'Problem Kurma & Temel Sayılar', '45 dk problemleri cümle cümle denkleme çevirme alıştırması; 25 dk yanlış yapılan soruları tekrar çözme.'),
                _g('Perşembe', 'Temel Geometri & Biyoloji Kavramları', '45 dk doğru, açı ve üçgen temel özellikleri; 30 dk hücre ve canlıların temel özellikleri kavram haritası.'),
                _g('Cuma', 'Eksik Defteri ve Hafta Özeti', 'Hafta boyunca takıldığın 5-10 temel konuyu işaretleme, kısa not çıkarma ve zorlamayan temel soru denemesi.'),
                _g('Cumartesi', 'Kısa Süreli Temel Tarama', '60-75 dk temel düzey karma soru taraması; ardından süre baskısı olmadan nereden puan kaçtığını bulma.'),
                _g('Pazar', 'Hafif Tekrar ve Dinlenme', '30 dk haftalık notlara göz atma; günün geri kalanında tamamen dinlenme ve zihin boşaltma.'),
            ],
        },
        'gelisen': {
            'program_adi': 'Sayısal Gelişim ve Kademeli Yükseliş Programı',
            'gunler': [
                _g('Pazartesi', 'TYT Matematik & Paragraf Rutini', '75 dk TYT Matematik konu + soru çözümü (problemler/fonksiyonlar); 30 dk paragraf.'),
                _g('Salı', 'Fizik & Türkçe', '60 dk temel-orta düzey Fizik konu ve soru; 45 dk TYT Türkçe dil bilgisi ve paragraf.'),
                _g('Çarşamba', 'Matematik & Kimya', '75 dk Matematik soru bankası pratiği; 45 dk Kimya temel kavramlar ve tepkime/çözelti çalışmaları.'),
                _g('Perşembe', 'Biyoloji & Geometri', '60 dk Biyoloji sistemler/genetik konu ve test; 45 dk Geometri üçgenler/çokgenler uygulaması.'),
                _g('Cuma', 'Eksik Kapatma & Yanlış Analizi', 'Haftadaki yanlış soruların yeniden çözümü, eksik kalan alt başlıkların tamamlanması.'),
                _g('Cumartesi', 'TYT Deneme & Analiz', '135 dk TYT deneme provası; ardından yanlış ve boş soruların konu bazlı listelenmesi.'),
                _g('Pazar', 'Kademeli AYT Geçişi & Dinlenme', '60 dk AYT Matematik/Fen temel konularına ısınma; akşam dinlenme ve haftalık plan.'),
            ],
        },
        'zirve': {
            'program_adi': 'Sayısal YKS Zirve Hazırlık Programı',
            'gunler': [
                _g('Pazartesi', 'TYT-AYT Matematik', 'Sabah 2 saat AYT Matematik (Türev/İntegral/Trigonometri), Akşam 1.5 saat TYT Matematik branş denemesi ve paragraf.'),
                _g('Salı', 'Fizik & Türkçe', 'Sabah AYT Fizik (Mekanik/Elektrik), Öğleden sonra TYT Türkçe (Dil Bilgisi ve Paragraf kampı).'),
                _g('Çarşamba', 'Matematik & Kimya', 'Sabah AYT Matematik soru bankası çözümü, Akşam AYT Kimya (Organik Kimya ağırlıklı çalışma).'),
                _g('Perşembe', 'Biyoloji & Geometri', 'Sabah AYT Biyoloji (Sistemler ve Genetik), Akşam Geometri (Üçgenler ve Çember kampı).'),
                _g('Cuma', 'Genel Tekrar & Deneme', 'Haftalık işlenen konuların fasikül taramaları, yanlış yapılan soruların analizi ve defter notu çıkarılması.'),
                _g('Cumartesi', 'TYT Genel Deneme', 'Sabah tam zamanlı TYT Deneme Sınavı (Süre tutarak), Öğleden sonra detaylı deneme analizi ve eksik kapatma.'),
                _g('Pazar', 'AYT Branş Denemeleri & Dinlenme', 'Sabah AYT Matematik/Fen branş denemesi, Akşam ise zihni dinlendirme ve gelecek haftanın planlaması.'),
            ],
        },
    },
    'ESIT_AGIRLIK': {
        'temel': {
            'program_adi': 'Eşit Ağırlık Temel Kurma ve Eksik Yakalama Programı',
            'gunler': [
                _g('Pazartesi', 'Temel Matematik & Okuma Anlama', '45 dk temel sayılar, kesir ve denklem kurma; 30 dk paragraf okuma ve ana fikir bulma.'),
                _g('Salı', 'Edebiyat Kavramları & Tarih Temeli', '45 dk söz sanatları, türler ve okuma metinleri; 30 dk tarihsel olay-neden-sonuç ilişkisi.'),
                _g('Çarşamba', 'Problem Pratiği & Harita Okuma', '45 dk günlük hayat problemleri; 30 dk Türkiye ve dünya haritasında yer/iklim/nüfus okuma.'),
                _g('Perşembe', 'Okuma-Yazma & Felsefe/Sosyal Kavramlar', '45 dk metin özetleme ve paragraf soruları; 30 dk temel felsefe ve sosyal kavramlar.'),
                _g('Cuma', 'Eksik Bulma ve Tekrar', 'Haftanın en zorlayıcı 2 konusunu seçip kısa tekrar ve temel soru çözümü.'),
                _g('Cumartesi', 'Kısa Deneme ve Hata Ayıklama', '75 dk temel soru taraması; dikkat hatası mı konu eksiği mi olduğunu ayırma.'),
                _g('Pazar', 'Hafif Tekrar ve Dinlenme', '30 dk kısa not tekrarı; kalan zamanda dinlenme.'),
            ],
        },
        'gelisen': {
            'program_adi': 'Eşit Ağırlık Gelişim Programı',
            'gunler': [
                _g('Pazartesi', 'TYT Matematik & Paragraf', '75 dk Matematik (temel konular ve problemler); 30 dk TYT Türkçe/paragraf.'),
                _g('Salı', 'Edebiyat & Tarih', '60 dk Türk Dili ve Edebiyatı konu ve soru; 45 dk Tarih konu ve test.'),
                _g('Çarşamba', 'Matematik & Coğrafya', '75 dk Matematik soru çözümü; 45 dk Coğrafya harita ve beşeri konular.'),
                _g('Perşembe', 'Edebiyat & Felsefe Grubu', '60 dk Edebiyat dönem/eser çalışmaları ve test; 45 dk Felsefe/Din tekrar ve soru.'),
                _g('Cuma', 'Yanlış Analizi ve Eksik Kapatma', 'Çözülemeyen soruların incelenmesi ve zayıf konuların tamamlanması.'),
                _g('Cumartesi', 'TYT Deneme Sınavı', '135 dk TYT denemesi ve öğleden sonra net/eksik analizi.'),
                _g('Pazar', 'AYT EA Geçiş & Dinlenme', '60 dk AYT Matematik/Edebiyat-Sosyal temel soruları; akşam dinlenme.'),
            ],
        },
        'zirve': {
            'program_adi': 'EŞİT AĞIRLIK (EA) Zirve Hazırlık Programı',
            'gunler': [
                _g('Pazartesi', 'AYT Matematik & Paragraf', 'Sabah 2 saat AYT Matematik (Fonksiyonlar, Polinomlar), Akşam TYT Paragraf ve Türkçe denemesi.'),
                _g('Salı', 'Edebiyat & Tarih', 'Sabah AYT Türk Dili ve Edebiyatı (Cumhuriyet Dönemi / Divan Edebiyatı), Akşam Tarih-1 çalışması.'),
                _g('Çarşamba', 'Matematik & Coğrafya', 'Sabah AYT Matematik problem kampı, Akşam Coğrafya-1 harita ve beşeri sistemler analizi.'),
                _g('Perşembe', 'Edebiyat & Felsefe Grubu', 'Sabah Edebiyat yazar-eser ezberleri ve soru çözümü, Akşam Felsefe ve Din Kültürü tekrarları.'),
                _g('Cuma', 'Analiz & Soru Çözümü', 'Haftalık çözülemeyen soruların hocalarla çözdürülmesi ve eksik konuların taranması.'),
                _g('Cumartesi', 'TYT Genel Deneme', 'Sabah gerçek sınav provası niteliğinde TYT Denemesi, Öğleden sonra detaylı analiz.'),
                _g('Pazar', 'AYT Deneme & Motivasyon', 'Sabah AYT Eşit Ağırlık Deneme Sınavı, Akşam hafif okumalar ve dinlenme.'),
            ],
        },
    },
    'SOZEL_GENEL': {
        'temel': {
            'program_adi': 'Sözel ve Genel Temel Kurma Programı',
            'gunler': [
                _g('Pazartesi', 'Okuma Anlama & Sözcük/Dil Temeli', '45 dk düzenli okuma ve paragraf anlama; 30 dk temel dil bilgisi kuralları.'),
                _g('Salı', 'Tarih Temeli & Kronoloji', '45 dk olayların kronolojik sıralaması ve neden-sonuç ilişkisi; 25 dk temel soru.'),
                _g('Çarşamba', 'Coğrafya Harita & Felsefe Temeli', '45 dk harita/mekân okuma; 30 dk temel felsefi kavramlar.'),
                _g('Perşembe', 'Edebiyat Metin Okuma & Kısa Test', '45 dk metin inceleme ve temel edebiyat soruları; 25 dk yanlış kontrolü.'),
                _g('Cuma', 'Eksik Bulma ve Özet', 'Haftada en çok zorlayan konunun kısa özeti ve temel soru tekrarı.'),
                _g('Cumartesi', 'Kısa Tarama ve Analiz', '60-75 dk karma sözel/genel soru taraması ve eksik konu listesi.'),
                _g('Pazar', 'Hafif Okuma ve Dinlenme', '30 dk keyifli okuma/tekrar; günün geri kalanında dinlenme.'),
            ],
        },
        'gelisen': {
            'program_adi': 'Sözel ve Genel Gelişim Programı',
            'gunler': [
                _g('Pazartesi', 'Edebiyat & Türkçe', '60 dk Edebiyat konu ve soru; 45 dk TYT Türkçe/paragraf çalışması.'),
                _g('Salı', 'Tarih & Coğrafya', '60 dk Tarih konu ve soru; 45 dk Coğrafya konu ve harita pratiği.'),
                _g('Çarşamba', 'Felsefe & Sosyal Bilimler', '60 dk Felsefe grubu konu ve kavramlar; 45 dk sosyal bilimler testleri.'),
                _g('Perşembe', 'Edebiyat Soru Pratiği', '75 dk Edebiyat soru çözümü ve yanlış analizi.'),
                _g('Cuma', 'Eksik Kapatma & Tekrar', 'Haftalık eksik konuların tamamlanması ve not düzenleme.'),
                _g('Cumartesi', 'TYT Deneme Sınavı', '135 dk TYT denemesi ve öğleden sonra eksik analizi.'),
                _g('Pazar', 'Sözel Pratik & Dinlenme', '60 dk AYT Sözel sorularına geçiş; akşam dinlenme.'),
            ],
        },
        'zirve': {
            'program_adi': 'SÖZEL / GENEL YKS Başarı Programı',
            'gunler': [
                _g('Pazartesi', 'Edebiyat & Türkçe', 'Sabah AYT Edebiyat detaylı konu çalışması, Akşam TYT Türkçe paragraf rutini.'),
                _g('Salı', 'Tarih & Coğrafya', 'Sabah AYT Tarih (İnkılap ve Dünya Tarihi), Akşam Coğrafya genel tekrarı.'),
                _g('Çarşamba', 'Felsefe & Yabancı Dil / Sosyal', 'Sabah Felsefe grubu kavram haritaları, Akşam sosyal bilimler soru çözümleri.'),
                _g('Perşembe', 'Edebiyat Soru Kampı', 'Edebiyat soru bankası üzerinden en az 150 soru ve yanlış analizi.'),
                _g('Cuma', 'Genel Tekrar', 'Haftalık notların baştan sona gözden geçirilmesi.'),
                _g('Cumartesi', 'TYT Deneme Sınavı', 'Sabah 135 dakika TYT Denemesi ve öğleden sonra analiz.'),
                _g('Pazar', 'Sözel Deneme & Dinlenme', 'Sabah AYT Sözel branş denemesi, akşam dinlenme.'),
            ],
        },
    },
}


def _grup_sec(alan):
    if 'Teknik' in alan or 'Mühendislik' in alan or 'Sağlık' in alan:
        return 'SAYISAL'
    if 'Ekonomi' in alan or 'Yönetim' in alan or 'Sosyal' in alan:
        return 'ESIT_AGIRLIK'
    return 'SOZEL_GENEL'


def seviye_belirle(seviye_param=None, puan=None):
    if seviye_param in ('temel', 'gelisen', 'zirve'):
        return seviye_param
    if puan is not None:
        try:
            puan_val = float(puan)
            if puan_val < 45:
                return 'temel'
            if puan_val < 75:
                return 'gelisen'
            return 'zirve'
        except (TypeError, ValueError):
            pass
    return 'gelisen'


def program_getir(alan, seviye_param=None, puan=None):
    grup = _grup_sec(alan or '')
    seviye = seviye_belirle(seviye_param, puan)
    paket = DERS_PROGRAMLARI[grup][seviye]
    return seviye, paket['program_adi'], paket['gunler']
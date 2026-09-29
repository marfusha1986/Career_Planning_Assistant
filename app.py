from flask import Flask,render_template,request,redirect,url_for
from database import get_db_connection


app = Flask(__name__)

def safe_int(value,default=0):
    try:
        return(value) if value else default
    except(TypeError,ValueError):
        return default

@app.route('/')
def index():
    #Anasayfa : 10 modüllü kariyer asistanı dashboardu
    return render_template('index.html')

@app.route('/test',methods=['GET','POST'])
def ilgi_testi():
    #Akıllı ilgi ve yetenek analizi
    if request.method == 'POST':
        
        #Kullanıcı test yanıtları burda işlenecek
        q1_score = int(request.form.get('q1'))
        q2_score = int(request.form.get('q2'))

        #q1:Analitik sayısal eğilim
        #q2:Sosyal Sözel eğilim
        toplam_puan = q1_score + q2_score
        print(f"Alınan Test Puanları -> Soru 1: {q1_score}, Soru 2: {q2_score}, Toplam: {toplam_puan}")
        return redirect(url_for('sonuclar',puan=toplam_puan))
    
    return render_template('test.html')

@app.route('/sonuclar')
def sonuclar():
    #Eşleştirme ve rapor ekranı
    secilen_maddeler = request.args.getlist('maddeler')

    #Kategorilere göre sayaç başlatalım
    puanlar = {
        "sayisal":0,
        "sozel":0,
        "esit":0,
        "saglik":0,
        "sanat":0,
        "sosyal":0
    }

    #Gelen maddeleri öneklerine göre sayıyoruz
    for madde in secilen_maddeler:
        kategori = madde.split("_")[0]
        if kategori in puanlar:
            puanlar[kategori] += 1


    #En çok puan alan kategoriyi buluyoruz
    en_yuksek_kategori = max(puanlar,key=puanlar.get)
    toplam_isaretlenen = len(secilen_maddeler)

    #Kategoriye göre dinamik sonuç metini
    sonuc_bilgileri = { 
        'sayisal': {
            'alan': "Teknik, Mühendislik ve Yapay Zekâ",
            'aciklama': "Analitik düşünme, kodlama, sistem kurma ve teknik problemleri çözme konularında çok yüksek bir potansiyele adaysın. Yazılım mühendisliği ve ileri teknoloji alanları senin için biçilmiş kaftan!"
        },
        'sozel': {
            'alan': "Sözel, Dil ve Medya Yönetimi",
            'aciklama': "Güçlü ifade kabiliyetin, dil öğrenme becerin ve edebi/fikri yönün sayesinde kitleleri etkileyebileceğin, yazarlık, medya veya uluslararası iletişim alanlarında parlayabilirsin."
        },
        'esit': {
            'alan': "Ekonomi, Yönetim ve Sosyal Bilimler",
            'aciklama': "Strateji kurma, bütçe yönetimi, liderlik ve analitik karar alma becerilerin yüksek. İşletme, iktisat ve yönetim bilişim sistemleri senin için ideal."
        },
        'saglik': {
            'alan': "Sağlık ve Canlı Bilimleri",
            'aciklama': "Canlıların yapısına olan meraktan, insanlara yardım etme isteğinden ve doğa bilimlerine olan duyarlılığından ötürü sağlık, tıp destek teknolojileri ve biyoloji alanlarında harika işler çıkarabilirsin."
        },
        'sanat': {
            'alan': "Tasarım, Mimari ve Sanat",
            'aciklama': "Görsel estetiğe verdiğin önem, el becerin ve yaratıcı bakış açınla mimariden dijital tasarıma, sanattan zanaatın inceliklerine kadar estetiğin olduğu her yerde başarılı olursun."
        },
        'sosyal': {
            'alan': "Sosyoloji, Hukuk ve Araştırma",
            'aciklama': "İnsan davranışlarını inceleme, toplumsal sorunlara çözüm arama ve adalet duygusu gerektiren alanlarda (hukuk, psikoloji, sosyal araştırmalar) derinleşme potansiyelin çok yüksek."
        }
    }
    
    secilen_sonuc = sonuc_bilgileri.get(en_yuksek_kategori, {
        'alan': "Çok Yönlü Kariyer Potansiyeli",
        'aciklama': "Farklı alanlarda dengeli ilgi alanlarına sahipsin. Kendi tutkularını harmanlayarak interdisipliner bir kariyer yolu çizebilirsin."
    })

    # 1. VERİTABANI KAYIT İŞLEMİ
    try:
        # Oracle bağlantı bilgileri (kendi kullanıcı adı ve şifrene göre düzenleyebilirsin)
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO kariyer_sonuclari 
            (toplam_puan, en_yuksek_alan, sayisal_puan, sozel_puan, esit_puan, saglik_puan, sanat_puan, sosyal_puan) 
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """
        
        cursor.execute(sql, (
            toplam_isaretlenen, 
            secilen_sonuc['alan'], 
            puanlar['sayisal'], 
            puanlar['sozel'], 
            puanlar['esit'], 
            puanlar['saglik'], 
            puanlar['sanat'], 
            puanlar['sosyal']
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Test sonucu Oracle veritabanına başarıyla kaydedildi!")
        
    except Exception as e:
        print(f"❌ Veritabanı kayıt hatası: {e}")

    return render_template('sonuclar.html', 
                           puan=toplam_isaretlenen, 
                           alan=secilen_sonuc['alan'], 
                           aciklama=secilen_sonuc['aciklama'],
                           puanlar=puanlar)

    
@app.route('/gelecek-meslekleri')
def gelecek_meslekleri():
    # Kullanıcının en son hangi alanda öne çıktığını query string veya session'dan alabiliriz. 
    # Şimdilik örnek olarak parametre veya varsayılan bir alan kullanalım:
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    
    # Alanlara göre geleceğin meslek havuzu (Yapay Zekâ ve 2026+ Trendleri)
    gelecek_trendleri = {
        'Teknik, Mühendislik ve Yapay Zekâ': [
            {"meslek": "Yapay Zekâ Etiği ve Güvenliği Uzmanı", "aciklama": "Yapay zekâ modellerinin tarafsızlığını, güvenliğini ve etik kurallara uygunluğunu denetler."},
            {"meslek": "Kuantum Yazılım Mühendisi", "aciklama": "Kuantum bilgisayarları için algoritma ve yazılım altyapısı geliştirir."},
            {"meslek": "Otonom Sistemler Filo Mimarı", "aciklama": "İnsansız hava/kara araçlarının trafik ve operasyon yönetim ağını tasarlar."}
        ],
        'Sözel, Dil ve Medya Yönetimi': [
            {"meslek": "AI Destekli İçerik Küratörü", "aciklama": "Yapay zekâ tarafından üretilen metin ve medyaları marka diline ve insan duygusuna uyarlar."},
            {"meslek": "Dijital İtibar ve Kriz Mimarı", "aciklama": "Metaverse ve küresel ağlarda kurumların ve kişilerin dijital kimliklerini yönetir."},
            {"meslek": "Kültürlerarası Yapay Zekâ Dil Uzmanı", "aciklama": "LLM'lerin yerel kültürel kodları ve lehçeleri kusursuz anlamasını sağlar."}
        ],
        'Ekonomi, Yönetim ve Sosyal Bilimler': [
            {"meslek": "Algoritmik Ticaret ve Risk Analisti", "aciklama": "Yapay zekâ destekli finansal piyasa algoritmalarını denetler ve strateji kurar."},
            {"meslek": "Dijital Dönüşüm ve Çevik Lider", "aciklama": "Geleneksel şirketlerin yapay zekâ odaklı otonom yapılara evrilmesini yönetir."},
            {"meslek": "Sürdürülebilir Ekonomi Stratejisti", "aciklama": "Yeşil enerji ve karbon ayak izi odaklı finansal modeller geliştirir."}
        ],
        'Sağlık ve Canlı Bilimleri': [
            {"meslek": "Kişiselleştirilmiş Genomik Danışmanı", "aciklama": "Bireylerin DNA haritasına göre yaşam ve tedavi planı oluşturur."},
            {"meslek": "Biyonik Organ Entegrasyon Uzmanı", "aciklama": "Yapay organların sinir sistemiyle uyumlu çalışmasını koordine eder."},
            {"meslek": "Tele-Sağlık Sistemleri Mimarı", "aciklama": "Uzaktan ameliyat ve yapay zekâ destekli erken teşhis ağlarını kurar."}
        ],
        'Tasarım, Mimari ve Sanat': [
            {"meslek": "Metaverse Deneyim (UX) Mimarı", "aciklama": "Sanal evrenlerde estetik, akıcı ve insan odaklı yaşam alanları tasarlar."},
            {"meslek": "AI Sanat Direktörü", "aciklama": "Üretken yapay zekâ araçlarıyla (Midjourney/Sora vb.) sinema ve reklam estetiğini yönlendirir."},
            {"meslek": "Eko-Mimari ve Akıllı Malzeme Tasarımcısı", "aciklama": "Doğayla uyumlu, kendi kendini onaran akıllı binalar ve malzemeler tasarlar."}
        ],
        'Sosyoloji, Hukuk ve Araştırma': [
            {"meslek": "Yapay Zekâ ve Robot Hukuku Uzmanı", "aciklama": "Otonom araçların veya yapay zekâ kararlarının hukuki sorumluluklarını düzenler."},
            {"meslek": "Dijital Sosyolog", "aciklama": "Sanal toplulukların, yapay zekâ entegrasyonunun insan psikolojisi üzerindeki etkilerini inceler."},
            {"meslek": "Küresel Risk ve Kriz Araştırmacısı", "aciklama": "Yapay zekâ çağında toplumsal ve jeopolitik kırılma noktalarını analiz eder."}
        ]
    }
    
    # Seçilen alana ait meslekleri al, yoksa varsayılan teknik alanı getir
    meslekler_listesi = gelecek_trendleri.get(alan, gelecek_trendleri['Teknik, Mühendislik ve Yapay Zekâ'])

    return render_template('gelecek_meslekleri.html', alan=alan, meslekler=meslekler_listesi)

@app.route('/karsilastirma')
def karsilastirma():
    aktif_kriter = request.args.get('kriter', 'tumu')
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    
    # Her alan için 10'ar adet vizyoner meslek ve detayları
    karsilastirma_semasi = {
        'Teknik, Mühendislik ve Yapay Zekâ': {
            'brans_adi': 'Teknik, Mühendislik ve Yapay Zekâ',
            'meslekler': [
                {
                    'ad': 'Yapay Zekâ Mühendisi',
                    'avantaj': 'Küresel ölçekte yüksek maaş, uzaktan (remote) çalışma ve geleceğin en gözde sektörü.',
                    'dezavantaj': 'Sürekli güncel kalma baskısı; her gün yeni bir model çıkar.',
                    'zorluk': 'İleri düzey matematik, istatistik ve karmaşık kodlama hatalarını çözmek.',
                    'calisma_ortami': 'Teknoloji ofisleri, yazılım geliştirme stüdyoları veya evden esnek çalışma.',
                    'maas': 'Çok Yüksek (Dolar/Euro bazlı küresel standartlar).',
                    'yetenek_uyumu': 'Analitik zekâ, mantıksal kurgu ve ileri düzey kodlama disiplini.'
                },
                {
                    'ad': 'Kıdemli Full-Stack Geliştirici',
                    'avantaj': 'Uçtan uca bir sistemin hem arayüzünü hem veritabanını kurabilmenin yarattığı yaratıcı tatmin.',
                    'dezavantaj': 'Müşteri taleplerinin sürekli değişmesi ve sıkı teslim tarihlerine sıkışmak.',
                    'zorluk': 'Farklı teknolojileri birbiriyle entegre etmek ve sistem güvenliğini sağlamak.',
                    'calisma_ortami': 'Yazılım ajansları ve teknoloji şirketleri.',
                    'maas': 'Yüksek (Tecrübe arttıkça hızla katlanır).',
                    'yetenek_uyumu': 'Problem çözme becerisi, sabır ve çok yönlü öğrenme yeteneği.'
                },
                {
                    'ad': 'Kuantum Yazılım Mühendisi',
                    'avantaj': 'Geleneksel bilgisayarların çözemediği devasa problemleri çözen geleceğin öncü teknolojisinde yer almak.',
                    'dezavantaj': 'Alanın henüz çok yeni olması ve kaynak/dokümantasyon eksikliği.',
                    'zorluk': 'Kuantum mekaniği mantığıyla yazılım algoritmaları kurgulamak.',
                    'calisma_ortami': 'İleri teknoloji Ar-Ge merkezleri ve kuantum laboratuvarları.',
                    'maas': 'Çok Yüksek.',
                    'yetenek_uyumu': 'İleri fizik merakı, soyut düşünme ve üst düzey matematik.'
                },
                {
                    'ad': 'Otonom Sistemler Filo Mimarı',
                    'avantaj': 'İnsansız hava, kara ve deniz araçlarının yapay zekâ ağlarını yöneten kritik bir rolde olmak.',
                    'dezavantaj': 'Sistem hatasının fiziksel dünyada büyük riskler doğurabilmesi (yüksek sorumluluk).',
                    'zorluk': 'Anlık veri akışında sıfır hata toleransıyla karar mekanizmaları kurmak.',
                    'calisma_ortami': 'Otonom araç geliştirme merkezleri ve teknoparklar.',
                    'maas': 'Yüksek.',
                    'yetenek_uyumu': 'Sistem mühendisliği, algoritmik mantık ve kriz yönetimi.'
                },
                {
                    'ad': 'Veri Bilimci ve Büyük Veri Analisti',
                    'avantaj': 'Yüz binlerce karmaşık verinin içindeki gizli trendleri ortaya çıkararak şirketlere stratejik yön vermek.',
                    'dezavantaj': 'Veri temizleme (data cleaning) gibi zaman alan ve yorucu süreçler.',
                    'zorluk': 'Gürültülü verilerden anlamlı ve doğru sonuçlar türetebilmek.',
                    'calisma_ortami': 'Kurumsal şirketlerin veri analitiği departmanları.',
                    'maas': 'Yüksek.',
                    'yetenek_uyumu': 'İstatistik bilgisi, SQL/Python hâkimiyeti ve analitik bakış açısı.'
                },
                {
                    'ad': 'Siber Güvenlik Uzmanı / Etik Hacker',
                    'avantaj': 'Asla talebi azalmayacak, dijital dünyayı koruyan "kalkan" görevi gören saygın ve dinamik bir alan.',
                    'dezavantaj': 'Siber saldırıların 7/24 olabilmesi nedeniyle nöbetli veya stresli çalışma saatleri.',
                    'zorluk': 'Saldırganların zihnini okuyarak sistemdeki en küçük açığı onlardan önce bulmak.',
                    'calisma_ortami': 'Güvenlik operasyon merkezleri (SOC) ve kurumsal ofisler.',
                    'maas': 'Yüksek.',
                    'yetenek_uyumu': 'Şüpheci ve analitik yaklaşım, ağ protokolleri bilgisi ve sabır.'
                },
                {
                    'ad': 'Bulut Bilişim (Cloud) Mimarı',
                    'avantaj': 'Dünyanın dört bir yanındaki sistemlerin bulutta kesintisiz ve güvenli çalışmasını koordine etmek.',
                    'dezavantaj': 'Sistem kesintilerinde (down time) gece yarısı bile müdahale etme zorunluluğu.',
                    'zorluk': 'Milyonlarca kullanıcının aynı anda eriştiği devasa altyapıları ölçeklemek.',
                    'calisma_ortami': 'Bulut servis sağlayıcıları ve büyük ölçekli teknoloji firmaları.',
                    'maas': 'Çok Yüksek.',
                    'yetenek_uyumu': 'Altyapı bilgisi, ağ yönetimi ve sistem optimizasyon yeteneği.'
                },
                {
                    'ad': 'Blockchain ve Akıllı Sözleşme Geliştiricisi',
                    'avantaj': 'Merkeziyetsiz finans ve güvenli dijital mülkiyet sistemlerinin mimarı olmak.',
                    'dezavantaj': 'Blokzincir kodlarındaki en ufak hatanın geri döndürülemez finansal kayıplara yol açabilmesi.',
                    'zorluk': 'Hatasız ve yüzde yüz güvenli akıllı sözleşmeler (smart contracts) yazmak.',
                    'calisma_ortami': 'Web3 projeleri, kripto varlık ve finans teknolojisi firmaları.',
                    'maas': 'Çok Yüksek.',
                    'yetenek_uyumu': 'Kriptografi merakı, titizlik ve ileri düzey programlama.'
                },
                {
                    'ad': 'Robotik Süreç Otomasyonu (RPA) Uzmanı',
                    'avantaj': 'Şirketlerin rutin, sıkıcı ve manuel işlerini robot yazılımlara devrederek verimliliği uçurmak.',
                    'dezavantaj': 'İş süreçlerindeki sürekli değişimlerin otomasyon kodlarını eskitmesi.',
                    'zorluk': 'Farklı kurumsal yazılımları birbiriyle konuşturacak akışlar tasarlamak.',
                    'calisma_ortami': 'Kurumsal şirketlerin dijital dönüşüm birimleri.',
                    'maas': 'İyi - Yüksek.',
                    'yetenek_uyumu': 'Süreç analizi, iş zekâsı ve pratik kodlama becerisi.'
                },
                {
                    'ad': 'Yapay Zekâ Etiği ve Güvenliği Denetçisi',
                    'avantaj': 'Yapay zekâ modellerinin tarafsız, insan haklarına uygun ve adil çalışmasını sağlayarak geleceği şekillendirmek.',
                    'dezavantaj': 'Henüz oturmamış yasal çerçeveler ve etik ikilemlerle boğuşmak.',
                    'zorluk': 'Algoritmik önyargıları tespit edip ortadan kaldırmak.',
                    'calisma_ortami': 'Denetim firmaları, teknoloji devlerinin etik kurulları ve araştırma merkezleri.',
                    'maas': 'Yüksek.',
                    'yetenek_uyumu': 'Felsefe/etik bilinci, teknoloji merakı ve analitik eleştiri.'
                }
            ]
        },
        'Sözel, Dil dan Medya Yönetimi': {
            'brans_adi': 'Sözel, Dil ve Medya Yönetimi',
            'meslekler': [
                {'ad': 'Küresel Marka İletişim Direktörü', 'avantaj': 'Kitleleri yönlendirme gücü.', 'dezavantaj': '7/24 ulaşıda olma.', 'zorluk': 'Kriz yönetimi.', 'calisma_ortami': 'Global ajanslar.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Hitabet.'},
                {'ad': 'AI Metin ve Medya Stratejisti', 'avantaj': 'Yapay zekâyla hızlı üretim.', 'dezavantaj': 'Özgünlük baskısı.', 'zorluk': 'Metne insan ruhu katmak.', 'calisma_ortami': 'Medya ajansları.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Yaratıcı yazarlık.'},
                {'ad': 'Dijital İtibar ve Kriz Mimarı', 'avantaj': 'Krizleri avantaja çevirme tatmini.', 'dezavantaj': 'Sürekli stres.', 'zorluk': 'Anlık kararlar.', 'calisma_ortami': 'Kurumsal plazalar.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Soğukkanlılık.'},
                {'ad': 'Kültürlerarası Yapay Zekâ Dil Uzmanı', 'avantaj': 'Yazılımların dünyaya açılmasını sağlamak.', 'dezavantaj': 'Lehçe çeşitliliği.', 'zorluk': 'Yerel kültürel kodları kodlamak.', 'calisma_ortami': 'Teknoloji devleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Çoklu dil hâkimiyeti.'},
                {'ad': 'Podcast ve Sesli Medya Yapımcısı', 'avantaj': 'Büyüyen sesli pazarda trend belirleyici olmak.', 'dezavantaj': 'Dinleyici sadakati sağlama zorluğu.', 'zorluk': 'Özgün ses ve kurgu dili yakalamak.', 'calisma_ortami': 'Stüdyolar.', 'maas': 'Orta.', 'yetenek_uyumu': 'İşitsel estetik.'},
                {'ad': 'Senarist ve Dijital Hikâye Anlatıcısı', 'avantaj': 'Kendi dünyanı milyonlara izletme imkânı.', 'dezavantaj': 'Yaratıcı tıkanıklıklar.', 'zorluk': 'Sürükleyici kurgu kurmak.', 'calisma_ortami': 'Prodüksiyon şirketleri.', 'maas': 'Değişken.', 'yetenek_uyumu': 'Hayal gücü.'},
                {'ad': 'Uluslararası Basın Sözcüsü', 'avantaj': 'Devletleri veya büyük kurumları temsil etme prestiji.', 'dezavantaj': 'Hatasız konuşma baskısı.', 'zorluk': 'Basın mensuplarının zor sorularını ustaca yanıtlamak.', 'calisma_ortami': 'Kurumsal merkezler.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Güçlü diksiyon.'},
                {'ad': 'Sosyal Medya Algoritma Uzmanı', 'avantaj': 'İçeriklerin milyonlara ulaşmasını sağlayan formülü çözmek.', 'dezavantaj': 'Algoritmaların sürekli değişmesi.', 'zorluk': 'Hızla güncellenen trendlere adapte olmak.', 'calisma_ortami': 'Ajanslar.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Veri okuma.'},
                {'ad': 'Kurumsal Yayıncılık Editörü', 'avantaj': 'Nitelikli yayınlar ortaya koyma.', 'dezavantaj': 'Yoğun okuma ve düzelti mesaisi.', 'zorluk': 'Yazım standartlarını kusursuz korumak.', 'calisma_ortami': 'Yayınevleri.', 'maas': 'Orta.', 'yetenek_uyumu': 'Dil bilgisi.'},
                {'ad': 'Dijital Eğitim İçeriği Tasarımcısı', 'avantaj': 'İnsanların yeni beceriler kazanmasına öncülük etmek.', 'dezavantaj': 'Pedagojik ve teknik uyumu yakalamak.', 'zorluk': 'Sıkıcı konuları eğlenceli hale getirmek.', 'calisma_ortami': 'EdTech firmaları.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Eğiticilik.'}
            ]
        },
        'Ekonomi, Yönetim ve Sosyal Bilimler': {
            'brans_adi': 'Ekonomi, Yönetim ve Sosyal Bilimler',
            'meslekler': [
                {'ad': 'Finansal Teknoloji Stratejisti', 'avantaj': 'Geleceğin para sistemine yön verme.', 'dezavantaj': 'Piyasa stresi.', 'zorluk': 'Regülasyonları okumak.', 'calisma_ortami': 'Fintech merkezleri.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Sayısal mantık.'},
                {'ad': 'Kıdemli Yönetim Danışmanı', 'avantaj': 'Dev şirketleri yönetme vizyonu.', 'dezavantaj': 'Yoğun seyahat.', 'zorluk': 'Krizdeki şirketi kurtarmak.', 'calisma_ortami': 'Danışmanlık firmaları.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Liderlik.'},
                {'ad': 'Algoritmik Ticaret Uzmanı', 'avantaj': 'Yapay zekâ ile finansal piyasalarda operasyon.', 'dezavantaj': 'Anlık riskler.', 'zorluk': 'Algoritma hatalarını önlemek.', 'calisma_ortami': 'Yatırım fonları.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Matematik.'},
                {'ad': 'Sürdürülebilirlik ve Yeşil Ekonomi Uzmanı', 'avantaj': 'Geleceğin doğa dostu ekonomisini inşa etmek.', 'dezavantaj': 'Yeni bir alan olduğu için standartların oturmamış olması.', 'zorluk': 'Karbon ayak izini optimize eden modeller kurmak.', 'calisma_ortami': 'Kurumsal plazalar.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Çevre bilinci ve analiz.'},
                {'ad': 'Girişim Sermayesi (Venture Capital) Yöneticisi', 'avantaj': 'Parlak fikirleri erken aşamada keşfedip büyütmek.', 'dezavantaj': 'Yatırım yapılan girişimlerin batma riski.', 'zorluk': 'Doğru projeyi seçebilmek.', 'calisma_ortami': 'Yatırım ofisleri.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Öngörü ve vizyon.'},
                {'ad': 'Küresel Tedarik Zinciri Direktörü', 'avantaj': 'Uluslararası ticaretin devasa akışını yönetmek.', 'dezavantaj': 'Krizlerde (pandemi, savaş vb.) yaşanan tıkalı ağlar.', 'zorluk': 'Lojistik maliyetlerini minimize etmek.', 'calisma_ortami': 'Lojistik merkezleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Operasyonel zekâ.'},
                {'ad': 'İnsan Kaynakları ve Yetenek Mimarı', 'avantaj': 'Şirketlerin en değerli varlığı olan insanı doğru konuma getirmek.', 'dezavantaj': 'Çalışan uyuşmazlıkları ve krizleri yönetmek.', 'zorluk': 'Doğru yeteneği şirkete bağlamak.', 'calisma_ortami': 'İK departmanları.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Empati ve insan yönetimi.'},
                {'ad': 'Uluslararası Pazarlama Stratejisti', 'avantaj': 'Farklı kültürlerde ürünleri parlatmak.', 'dezavantaj': 'Kültürel uyumsuzluk riski.', 'zorluk': 'Yerel pazarları analiz etmek.', 'calisma_ortami': 'Global markalar.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Pazarlama zekâsı.'},
                {'ad': 'Risk Yönetimi ve Uyum Uzmanı', 'avantaj': 'Şirketleri olası yasal ve finansal felaketlerden korumak.', 'dezavantaj': 'Sürekli kural ve denetim odaklı sıkı çalışma.', 'zorluk': 'Gizli riskleri önceden görmek.', 'calisma_ortami': 'Banka ve holdingler.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Detaycılık.'},
                {'ad': 'Vergi ve Mali Hukuk Danışmanı', 'avantaj': 'Şirketlerin mali yapısını yasal çerçevede en karlı hale getirmek.', 'dezavantaj': 'Sürekli değişen karmaşık vergi kanunları.', 'zorluk': 'Mevzuat değişikliklerine anında adapte olmak.', 'calisma_ortami': 'Mali müşavirlik ofisleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Mevzuat hâkimiyeti.'}
            ]
        },
        'Sağlık ve Canlı Bilimleri': {
            'brans_adi': 'Sağlık ve Canlı Bilimleri',
            'meslekler': [
                {
                    'ad': 'Kişiselleştirilmiş Genomik Danışmanı',
                    'avantaj': 'Bireylerin DNA haritasına özel yaşam ve tedavi planı oluşturarak tıp dünyasında çığır açmak.',
                    'dezavantaj': 'Genetik verilerin mahremiyeti ve etik tartışmalarla uğraşmak.',
                    'zorluk': 'Karmaşık DNA dizilimlerini anlaşılır sağlık tavsiyelerine dönüştürmek.',
                    'calisma_ortami': 'Genetik laboratuvarları ve özel tıp merkezleri.',
                    'maas': 'Yüksek.',
                    'yetenek_uyumu': 'Genetik bilimi merakı ve birebir danışmanlık yeteneği.'
                },
                {
                    'ad': 'Biyonik Organ Entegrasyon Uzmanı',
                    'avantaj': 'Yapay organların insan sinir sistemiyle kusursuz uyum içinde çalışmasını sağlayarak hayat kurtarmak.',
                    'dezavantaj': 'Yüksek teknoloji entegrasyonunda yaşanan biyolojik reddedilme riskleri.',
                    'zorluk': 'Nörolojik sinyallerle mekanik organları senkronize etmek.',
                    'calisma_ortami': 'İleri teknoloji hastaneler ve biyomedikal laboratuvarlar.',
                    'maas': 'Çok Yüksek.',
                    'yetenek_uyumu': 'Biyomedikal mühendisliği ve tıp entegrasyon bilgisi.'
                },
                {
                    'ad': 'Tele-Sağlık Sistemleri Mimarı',
                    'avantaj': 'Uzaktan ameliyat ve yapay zekâ destekli erken teşhis ağlarını kurarak coğrafi sınırları ortadan kaldırmak.',
                    'dezavantaj': 'Ağ kesintisi veya teknolojik arızalarda yaşanabilecek kritik riskler.',
                    'zorluk': 'Sıfır gecikmeli (zero-latency) uzaktan cerrahi ağları tasarlamak.',
                    'calisma_ortami': 'Sağlık teknolojisi firmaları ve akıllı hastaneler.',
                    'maas': 'Yüksek.',
                    'yetenek_uyumu': 'Ağ teknolojileri ve sağlık sistemleri bilgisi.'
                },
                {'ad': 'Biyoteknoloji Uzmanı', 'avantaj': 'Tıbbi keşiflerde yer almak.', 'dezavantaj': 'Sabır gerektiren laboratuvarlar.', 'zorluk': 'Genetik anomalileri çözmek.', 'calisma_ortami': 'Ar-Ge merkezleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Titizlik.'},
                {'ad': 'Robotik Cerrahi Uzmanı', 'avantaj': 'En modern ameliyat sistemlerini kullanmak.', 'dezavantaj': 'Yüksek stres.', 'zorluk': 'Kritik operasyon saniyeleri.', 'calisma_ortami': 'Modern hastaneler.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Soğukkanlılık.'},
                {'ad': 'Nöroteknoloji ve Beyin-Bilgisayar Arayüz Uzmanı', 'avantaj': 'Zihin gücüyle çalışan cihazların geliştirilmesine öncülük etmek.', 'dezavantaj': 'İnsan beyninin karmaşık yapısının henüz tam çözülememiş olması.', 'zorluk': 'Nöron sinyallerini dijital komutlara çevirmek.', 'calisma_ortami': 'Nöroloji laboratuvarları.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Nöroloji ve yazılım entegrasyonu.'},
                {'ad': 'Yapay Organ ve Doku Mühendisi', 'avantaj': 'Laboratuvar ortamında suni organ üretme devriminin bir parçası olmak.', 'dezavantaj': 'Hücre kültürlerinin yaşatılmasındaki yüksek hassasiyet zorlukları.', 'zorluk': 'Damar ağı oluşturulabilen dokular üretmek.', 'calisma_ortami': 'Biyomühendislik merkezleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Hücre biyolojisi.'},
                {'ad': 'Tıbbi Yapay Zekâ Teşhis Uzmanı', 'avantaj': 'Görüntüleme ve tahlil verilerini AI ile milisaniyede analiz etmek.', 'dezavantaj': 'Yapay zekâ yanılmalarında hukuki sorumluluk.', 'zorluk': 'Algoritmaların hata payını sıfıra indirmek.', 'calisma_ortami': 'Tıp merkezleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Tıbbi veri analizi.'},
                {'ad': 'Nanotıp ve Akıllı İlaç Tasarımcısı', 'avantaj': 'Hastalık hücrelerini doğrudan hedef alan akıllı moleküller üretmek.', 'dezavantaj': 'Uzun klinik test ve onay süreçleri.', 'zorluk': 'Nano-robotların vücuttaki hareketini yönlendirmek.', 'calisma_ortami': 'İlaç Ar-Ge laboratuvarları.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Kimya ve nanoteknoloji.'},
                {'ad': 'Epidemiyoloji ve Küresel Sağlık Analisti', 'avantaj': 'Salgın hastalıkları önceden tahmin edip dünyayı korumak.', 'dezavantaj': 'Kriz anlarında yaşanan yoğun baskı.', 'zorluk': 'Devasa demografik sağlık verilerini modellemek.', 'calisma_ortami': 'Sağlık örgütleri ve enstitüler.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'İstatistik ve biyoloji.'}
            ]
        },
        'Tasarım, Mimari ve Sanat': {
            'brans_adi': 'Tasarım, Mimari ve Sanat',
            'meslekler': [
                {'ad': 'Metaverse / UX Deneyim Mimarı', 'avantaj': 'Sanal evrenleri tasarlamak.', 'dezavantaj': 'Teknolojinin hızlı değişimi.', 'zorluk': 'Akış kurgulamak.', 'calisma_ortami': 'Teknoloji stüdyoları.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Görsel zekâ.'},
                {'ad': 'Üst Düzey AI Sanat Direktörü', 'avantaj': 'Yapay zekâ ile dev projeler yönetmek.', 'dezavantaj': 'Müşteri beklentileri.', 'zorluk': 'Özgün konsept seçmek.', 'calisma_ortami': 'Ajanslar.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Estetik.'},
                {'ad': 'Eko-Mimari ve Akıllı Malzeme Tasarımcısı', 'avantaj': 'Doğayla uyumlu akıllı binalar inşa etmek.', 'dezavantaj': 'Pahalı ve yeni teknolojiler.', 'zorluk': 'Sürdürülebilir malzeme üretmek.', 'calisma_ortami': 'Mimarlık ofisleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Çevre ve tasarım.'},
                {'ad': 'Sanal Gerçeklik (VR) Çevre Tasarımcısı', 'avantaj': 'İnsanların içinde yaşayabileceği 3D dünyalar yaratmak.', 'dezavantaj': 'Donanım kısıtlamaları.', 'zorluk': 'Yüksek kaliteli gerçekçi dokular üretmek.', 'calisma_ortami': 'Oyun ve simülasyon firmaları.', 'maas': 'Yüksek.', 'yetenek_uyumu': '3D modelleme.'},
                {'ad': 'Dijital Moda ve Avatar Stilisti', 'avantaj': 'Metaverse ve oyunlar için dijital kıyafetler tasarlamak.', 'dezavantaj': 'Fiziki moda kadar kabul görmesinin zaman alması.', 'zorluk': 'Kumaş simülasyonlarını gerçeğe yakın kodlamak.', 'calisma_ortami': 'Moda teknoloji stüdyoları.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Moda ve 3D tasarım.'},
                {'ad': 'Akıllı Ürün ve Endüstriyel Tasarımcı', 'avantaj': 'Geleceğin ev aletlerini ve cihazlarını tasarlamak.', 'dezavantaj': 'Üretim maliyetleri dengesi.', 'zorluk': 'Ergonomi ile estetiği buluşturmak.', 'calisma_ortami': 'Endüstriyel atölyeler.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Form ve malzeme bilgisi.'},
                {'ad': 'Oyun Deneyimi (Game UX) Tasarımcısı', 'avantaj': 'Milyonların oynadığı oyunlarda kusursuz menü ve akışlar kurmak.', 'dezavantaj': 'Oyuncu geri bildirimleriyle gelen baskı.', 'zorluk': 'Karmaşık oyun arayüzlerini basit kılmak.', 'calisma_ortami': 'Oyun stüdyoları.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Oyun kültürü ve psikoloji.'},
                {'ad': 'Kapsamlı Marka Kimliği Tasarımcısı', 'avantaj': 'Şirketlerin yüzünü ve ruhunu sıfırdan yaratmak.', 'dezavantaj': 'Önyargılı müşteri revizyonları.', 'zorluk': 'Markanın ruhunu tek bir logoda özetlemek.', 'calisma_ortami': 'Tasarım ajansları.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Grafik sanatlar.'},
                {'ad': 'Dijital Sergi ve Müze Küratörü', 'avantaj': 'Sanatı dijital dünyada kitlelerle buluşturmak.', 'dezavantaj': 'Dijital telif ve güvenlik sorunları.', 'zorluk': 'Hikâye akışı kurmak.', 'calisma_ortami': 'Kültür merkezleri.', 'maas': 'Orta.', 'yetenek_uyumu': 'Sanat tarihi.'},
                {'ad': 'Akustik ve Ses Manzarası Tasarımcısı', 'avantaj': 'Mekânların ve dijital oyunların ses dünyasını inşa etmek.', 'dezavantaj': 'İnce akustik hesaplamalardaki zorluklar.', 'zorluk': 'Mükemmel ses yalıtımı ve yankı dengesi.', 'calisma_ortami': 'Akustik stüdyolar.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Müzik ve fizik.'}
            ]
        },
        'Sosyoloji, Hukuk ve Araştırma': {
            'brans_adi': 'Sosyoloji, Hukuk ve Araştırma',
            'meslekler': [
                {'ad': 'Bilişim ve Yapay Zekâ Hukuku Uzmanı', 'avantaj': 'Yeni dijital dünyanın kurallarını yazmak.', 'dezavantaj': 'Sürekli değişen yasalar.', 'zorluk': 'Yapay zekâ suçlarını savunmak.', 'calisma_ortami': 'Hukuk büroları.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Keskin mantık.'},
                {'ad': 'Dijital Sosyolog & Araştırmacı', 'avantaj': 'Algoritmaların toplum üzerindeki etkisini incelemek.', 'dezavantaj': 'Bütçe bulma zorluğu.', 'zorluk': 'Dezenformasyon ağlarını çözmek.', 'calisma_ortami': 'Enstitüler.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Gözlem yeteneği.'},
                {'ad': 'Kripto Varlık ve Blokzincir Hukukçusu', 'avantaj': 'Kripto varlık davalarında öncü uzman olmak.', 'dezavantaj': 'Belirsiz yasal boşluklar.', 'zorluk': 'Sınır ötesi dijital suçları takip etmek.', 'calisma_ortami': 'Global hukuk ofisleri.', 'maas': 'Çok Yüksek.', 'yetenek_uyumu': 'Finans ve hukuk.'},
                {'ad': 'Uluslararası İnsan Hakları ve Teknoloji Savunucusu', 'avantaj': 'Dijital çağda bireylerin haklarını korumak.', 'dezavantaj': 'Büyük teknoloji devleriyle mücadele stresi.', 'zorluk': 'Güçlü lobileri aşmak.', 'calisma_ortami': 'STK ve uluslararası mahkemeler.', 'maas': 'Orta-Yüksek.', 'yetenek_uyumu': 'Adalet duygusu.'},
                {'ad': 'Yapay Zekâ ve Veri Etiği Danışmanı', 'avantaj': 'Şirketlerin veri politikalarının etik olup olmadığını denetlemek.', 'dezavantaj': 'Şirket çıkarları ile etik değerler arasında kalmak.', 'zorluk': 'Şeffaf algoritma ilkeleri yazmak.', 'calisma_ortami': 'Danışmanlık firmaları.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Etik ve hukuk.'},
                {'ad': 'Dijital Suçlar ve Siber Soruşturma Uzmanı', 'avantaj': 'Siber suçluların dijital izlerini sürerek adalete teslim etmek.', 'dezavantaj': 'Tehlikeli siber çetelerle sanal temas.', 'zorluk': 'Usta korsanların sildiğiz izleri kurtarmak.', 'calisma_ortami': 'Adli bilişim birimleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Adli bilişim.'},
                {'ad': 'Fikri Mülkiyet ve Patent Vekili', 'avantaj': 'İcatların ve yaratıcı fikirlerin yasal haklarını korumak.', 'dezavantaj': 'Yoğun teknik inceleme dosyaları.', 'zorluk': 'Patent hırsızlığı davalarını kanıtlamak.', 'calisma_ortami': 'Patent ofisleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Detaycı inceleme.'},
                {'ad': 'Kritik Altyapılar Güvenlik Politikası Uzmanı', 'avantaj': 'Ülke geneli enerji ve su gibi kritik sistemleri korumak.', 'dezavantaj': 'Ulusal güvenlik seviyesinde yüksek stres.', 'zorluk': 'Gelişmiş sızma senaryolarına karşı önlem almak.', 'calisma_ortami': 'Kamu ve stratejik merkezler.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Stratejik güvenlik.'},
                {'ad': 'Yeni Medya ve İletişim Hukukçusu', 'avantaj': 'Sosyal medya suçları ve telif davalarında uzmanlaşmak.', 'dezavantaj': 'Her gün yeni bir dijital davanın türemesi.', 'zorluk': 'İnternetteki kişilik hakları ihlallerini durdurmak.', 'calisma_ortami': 'Özel hukuk büroları.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Medya hukuku.'},
                {'ad': 'Küresel Jeopolitik Risk Analisti', 'avantaj': 'Dünya genelindeki siyasi ve ekonomik kırılmaları önceden görmek.', 'dezavantaj': 'Sürekli kriz senaryoları üretmek.', 'zorluk': 'Karmaşık jeopolitik verileri doğru okumak.', 'calisma_ortami': 'Strateji merkezleri.', 'maas': 'Yüksek.', 'yetenek_uyumu': 'Tarih ve siyaset bilimi.'}
            ]
        }
    }
    
    secilen_veri = karsilastirma_semasi.get(alan, karsilastirma_semasi['Teknik, Mühendislik ve Yapay Zekâ'])

    return render_template('karsilastirma.html', veri=secilen_veri, alan=alan, aktif_kriter=aktif_kriter)

@app.route('/rol-simulasyonu')
def rol_simulasyonu():
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    
    # Karşılaştırma matrisindeki ilk 10 meslekle yüzde yüz uyumlu simülasyon havuzu
    simulasyon_verileri = {
        'Teknik, Mühendislik ve Yapay Zekâ': {
            'brans_adi': 'Teknik, Mühendislik ve Yapay Zekâ',
            'meslekler': [
                {
                    'ad': 'Yapay Zekâ Mühendisi',
                    'ikon': '🤖',
                    'egitim_zorluklari': 'Üniversitede ileri düzey lineer cebir, çok değişkenli kalkülüs, olasılık ve istatistik derslerini aşmak gerekir. Mezuniyet sonrasında ise her hafta çıkan yeni derin öğrenme modellerini ve akademik makaleleri takip etmek başlı başına zihinsel bir maratondur.',
                    'is_temposu': 'Yoğun tempoludur. Sabah sprint toplantılarıyla başlar; günün büyük kısmı kod yazarak, veri setlerini temizleyerek ve başarısız model eğitimlerini (training) debug ederek ekrana bakarak geçer.'
                },
                {
                    'ad': 'Kıdemli Full-Stack Geliştirici',
                    'ikon': '💻',
                    'egitim_zorluklari': 'Temel programlama mantığını kaptıktan sonra front-end, back-end, veritabanı ve sunucu yönetimi gibi çok farklı teknolojileri aynı anda kafada oturtmak ilk başta zorlar.',
                    'is_temposu': 'Hızlı ve streslidir. Müşteri taleplerinin aniden değişmesi, sıkı teslim tarihleri (deadline) ve sistem kesintilerine (down time) anında müdahale etme baskısı vardır.'
                },
                {
                    'ad': 'Kuantum Yazılım Mühendisi',
                    'ikon': '⚛️️',
                    'egitim_zorluklari': 'Klasik fizik mantığını tamamen unutup kuantum mekaniği (süperpozisyon, dolanıklık) kurallarıyla algoritma yazmayı öğrenmek zihni en çok zorlayan süreçtir. Kaynak sayısı çok azdır.',
                    'is_temposu': 'Ar-Ge odaklı ve zihinsel olarak çok yorucudur. Günün büyük kısmı soyut devre simülasyonları ve teorik matematiksel hesaplamalarla geçer.'
                },
                {
                    'ad': 'Otonom Sistemler Filo Mimarı',
                    'ikon': '🛸',
                    'egitim_zorluklari': 'Mekatronik ve yazılımı harmanlamak gereklidir. Hem donanım (sensörler, devreler) hem de yazılım (ROS, algoritmalar) tarafında aynı anda uzmanlaşmak uzun yıllar ister.',
                    'is_temposu': 'Yüksek sorumluluk gerektirir. Yazdığınız kodun fiziksel dünyada (araçlar, drone\'lar) hata yapma lüksü yoktur; anlık veri akışı sürekli kontrol edilir.'
                },
                {
                    'ad': 'Veri Bilimci ve Büyük Veri Analisti',
                    'ikon': '📊',
                    'egitim_zorluklari': 'İstatistik teorisini ezberlemek yetmez; o teoriyi milyonlarca satırlık dağınık ve kirli veriye uygulama becerisi kazanmak ciddi pratik ister.',
                    'is_temposu': 'Orta-Yoğun tempoludur. Zamanın büyük bölümü veriyi ayıklamakla geçer; ardından yönetim için sunumlar ve stratejik raporlar hazırlanır.'
                },
                {
                    'ad': 'Siber Güvenlik Uzmanı / Etik Hacker',
                    'ikon': '🛡️',
                    'egitim_zorluklari': 'Ağ protokollerini, işletim sistemlerinin zayıf yönlerini ve hacker bakış açısını kazanmak için sürekli sistemleri kırma (lab ortamında) çalışmaları yapmak şarttır.',
                    'is_temposu': 'Kriz odaklıdır. Sistemlerde bir zafiyet çıktığında veya saldırı hissedildiğinde mesai saati kavramı biter; gece yarısı bile müdahale etmek gerekebilir.'
                },
                {
                    'ad': 'Bulut Bilişim (Cloud) Mimarı',
                    'ikon': '☁️',
                    'egitim_zorluklari': 'Devasa sunucu altyapılarını, ağ güvenlik duvarlarını ve maliyet optimizasyonunu teorik olarak öğrenmek yetmez, binlerce dolarlık bulut bütçelerini yönetme stresi yaşanır.',
                    'is_temposu': 'Sürekli uyanık olmayı gerektirir. Milyonlarca kişinin kullandığı bir sistemde gece patlayan bir sunucu arızasına anında remote bağlanıp çözüm üretmek zorundasındır.'
                },
                {
                    'ad': 'Blockchain ve Akıllı Sözleşme Geliştiricisi',
                    'ikon': '⛓️',
                    'egitim_zorluklari': 'Yazdığınız akıllı sözleşmenin blokzincire bir kez yüklendikten sonra asla değiştirilememesi (ve milyar dolarlık açık barındırabilmesi) korkusuyla hatasız kodlama disiplini edinmek en büyük zorluktur.',
                    'is_temposu': 'Titiz ve dikkatli bir tempodur. Kodlar defalarca güvenlik testlerinden (audit) geçirilir; en ufak bir hata milyonluk kayıplara yol açabilir.'
                },
                {
                    'ad': 'Robotik Süreç Otomasyonu (RPA) Uzmanı',
                    'ikon': '⚙️',
                    'egitim_zorluklari': 'Farklı kurumsal yazılımların (SAP vb.) arkasındaki mantığı kavrayıp onları robotik akışlarla konuşturacak pratik mantığı oturtmak zaman alır.',
                    'is_temposu': 'Dengeli bir temposu vardır. Şirketlerin rutin iş süreçleri analiz edilir ve botların hatasız çalışıp çalışmadığı takip edilir.'
                },
                {
                    'ad': 'Yapay Zekâ Etiği ve Güvenliği Denetçisi',
                    'ikon': '⚖️',
                    'egitim_zorluklari': 'Hem hukuk/felsefe (etik, insan hakları) hem de teknik (yapay zekâ nasıl karar verir) altyapısını aynı kafada harmanlamak nadir bulunan bir eğitim süreci gerektirir.',
                    'is_temposu': 'Toplantı ve analiz ağırlıklıdır. Şirketlerin yapay zekâ modellerinin taraflı olup olmadığını denetlemek için kurullarla sürekli müzakere edilir.'
                }
            ]
        },
        'Sözel, Dil ve Medya Yönetimi': {
            'brans_adi': 'Sözel, Dil ve Medya Yönetimi',
            'meslekler': [
                {'ad': 'Küresel Marka İletişim Direktörü', 'ikon': '📢', 'egitim_zorluklari': 'İletişim fakültesi teoriktir; asıl zorluk küresel pazarları, kriz anı reflekslerini ve insan psikolojisini sahada, yıllar içinde öğrenmektir.', 'is_temposu': '7/24 ulaşıda olma gerektiren, yoğun toplantı ve seyahatlerle geçen stresli bir tempodur.'},
                {'ad': 'AI Metin ve Medya Stratejisti', 'ikon': '✍️️', 'egitim_zorluklari': 'Hem yaratıcı yazarlık yeteneğine sahip olmak hem de yapay zekâ metin araçlarını (LLM) bir ustalıkla yönlendirecek prompt mühendisliğini öğrenmek gerekir.', 'is_temposu': 'Hızlı ve tempoludur. Sürekli içerik üretimi, trend takibi ve yapay zekâ çıktılarını insan dokunuşuyla revize etme işi gün boyu sürer.'},
                {'ad': 'Dijital İtibar ve Kriz Mimarı', 'ikon': '🚨', 'egitim_zorluklari': 'Kriz anında soğukkanlı kalabilme refleksini geliştirmek okulda öğretelecek bir şey değildir; tecrübe ister.', 'is_temposu': 'Beklenmeyen anlarda patlayan krizlerle şekillenen, anlık karar almayı gerektiren yüksek stresli bir tempodur.'},
                {'ad': 'Kültürlerarası Yapay Zekâ Dil Uzmanı', 'ikon': '🌍', 'egitim_zorluklari': 'Birden fazla dile anadil düzeyinde hâkim olmak yetmez; o dillerin argo, yerel kültür ve deyim kodlarını yapay zekâya öğretecek dilbilim altyapısı gerekir.', 'is_temposu': 'Analitik ve odaklanma gerektiren, dil veri setleri üzerinde geçen düzenli bir çalışma temposu vardır.'},
                {'ad': 'Podcast ve Sesli Medya Yapımcısı', 'ikon': '🎙️', 'egitim_zorluklari': 'Ses estetiğini, miksaj ve kurgu tekniklerini öğrenmek ve kitleleri sesle bağlayacak özgün konseptler üretmek sabır ister.', 'is_temposu': 'Stüdyo kayıtları, konuk ayarlama ve uzun saatler süren ses kurgusu (editing) seanslarıyla geçer.'},
                {'ad': 'Senarist ve Dijital Hikâye Anlatıcısı', 'ikon': '🎬', 'egitim_zorluklari': 'Yaratıcı tıkanıklıkları aşmak, diyalogları doğal kılmak ve sürekli reddedilen senaryolara rağmen yazma disiplinini korumak en büyük zihinsel zorluktur.', 'is_temposu': 'Esnek ama yoğun bir kapanış temposudur. Ekran karşısında saatlerce kurgu kurarak ve sahne tasarlayarak geçer.'},
                {'ad': 'Uluslararası Basın Sözcüsü', 'ikon': '🎙️', 'egitim_zorluklari': 'Kameralar önünde kusursuz diksiyonla konuşmak, zor ve provokatif soruları ustaca savuşturabilmek ciddi bir stres yönetimi eğitimi gerektirir.', 'is_temposu': 'Gündem odaklıdır. Basın bültenleri, brifingler ve canlı yayın hazırlıklarıyla tempolu geçer.'},
                {'ad': 'Sosyal Medya Algoritma Uzmanı', 'ikon': '📈', 'egitim_zorluklari': 'Platformların her ay değiştiren gizli algoritmalarını ve veri analitiği araçlarını sürekli takip etmek teknik bir disiplin ister.', 'is_temposu': 'Anlık veri takibi gerektirir. Kampanya metrikleri sürekli izlenir ve optimize edilir.'},
                {'ad': 'Kurumsal Yayıncılık Editörü', 'ikon': '📚', 'egitim_zorluklari': 'Binlerce sayfalık metinleri hatasız okumak, yazım kurallarını kusursuz bilmek ve yazar kaprislerini yönetmek sabır ister.', 'is_temposu': 'Masa başı ve detay odaklıdır; uzun okuma ve düzelti mesaisi gerektirir.'},
                {'ad': 'Dijital Eğitim İçeriği Tasarımcısı', 'ikon': '🎓', 'egitim_zorluklari': 'Sıkıcı ve teknik bir bilgiyi, ekrandan izleyen öğrencinin sıkılmayacağı interaktif bir eğitime dönüştürecek pedagojik formasyonu kurmak.', 'is_temposu': 'Modül kurgusu ve test tasarımlarıyla geçen düzenli bir ofis temposudur.'}
            ]
        },
        'Ekonomi, Yönetim ve Sosyal Bilimler': {
            'brans_adi': 'Ekonomi, Yönetim ve Sosyal Bilimler',
            'meslekler': [
                {'ad': 'Finansal Teknoloji Stratejisti', 'ikon': '💳', 'egitim_zorluklari': 'Hem finans/ekonomi teorisini hem de yazılım/ödeme sistemlerinin teknik altyapısını aynı anda kavramak zorludur.', 'is_temposu': 'Piyasa açılış saatlerine endeksli, yüksek finansal risk sorumluluğu taşıyan tempolu bir iştir.'},
                {'ad': 'Kıdemli Yönetim Danışmanı', 'ikon': '👔', 'egitim_zorluklari': 'Prestijli bir MBA eğitimi ve farklı sektörlerin işleyişini hızla kavrayıp analiz edebilme yeteneği şarttır.', 'is_temposu': 'Yoğun seyahat trafiği, üst düzey yöneticilerle art arda yapılan toplantılar ve sunum hazırlıklarıyla geçer.'},
                {'ad': 'Algoritmik Ticaret Uzmanı', 'ikon': '📈', 'egitim_zorluklari': 'İleri düzey matematik, finans ve kodlamayı harmanlayıp borsada para kazandıran algoritmalar kurmak yüksek risk taşır.', 'is_temposu': 'Anlık piyasa dalgalanmalarını takip eden, hata kabul etmeyen stresli bir tempodur.'},
                {'ad': 'Sürdürülebilirlik ve Yeşil Ekonomi Uzmanı', 'ikon': '🌱', 'egitim_zorluklari': 'Yeni kuralları, karbon ayak izi hesaplama standartlarını ve uluslararası yeşil mutabakat yasalarını öğrenmek.', 'is_temposu': 'Raporlama, veri modelleme ve şirket içi yeşil dönüşüm toplantılarıyla geçer.'},
                {'ad': 'Girişim Sermayesi (VC) Yöneticisi', 'ikon': '💡', 'egitim_zorluklari': 'Binlerce başarısız fikir arasından milyar dolar yapacak tek girişimi önceden koklayıp bulabilme vizyonu kazanmak tecrübe ister.', 'is_temposu': 'Girişim sunumları (pitch), networking etkinlikleri ve fizibilite incelemeleriyle koşturmacalıdır.'},
                {'ad': 'Küresel Tedarik Zinciri Direktörü', 'ikon': '🚢', 'egitim_zorluklari': 'Lojistik ağlarındaki küresel aksaklıkları (savaş, kriz, pandemi) önceden öngörüp alternatif rotalar çizebilmek.', 'is_temposu': 'Sevkiyat takipleri, depo optimizasyonu ve kriz anlarında anlık telefon trafiğiyle doludur.'},
                {'ad': 'İnsan Kaynakları ve Yetenek Mimarı', 'ikon': '👥', 'egitim_zorluklari': 'İnsan psikolojisini ve kurumsal çatışmaları objektif yönetebilmek, zorlu mülakat dinamiklerini yönetmek.', 'is_temposu': 'Gün boyu süren yetenek mülakatları ve şirket içi denge toplantılarıyla geçer.'},
                {'ad': 'Uluslararası Pazarlama Stratejisti', 'ikon': '🎯', 'egitim_zorluklari': 'Farklı ülkelerin kültürlerini, yasalarını ve tüketici alışkanlıklarını hatasız analiz etmek.', 'is_temposu': 'Pazar araştırmaları ve global kampanya kurgularının yapıldığı yaratıcı ve tempolu bir iştir.'},
                {'ad': 'Risk Yönetimi ve Uyum Uzmanı', 'ikon': '📑', 'egitim_zorluklari': 'Şirketleri batırabilecek yasal ve finansal riskleri binlerce sayfalık mevzuat arasından sıyırıp bulmak.', 'is_temposu': 'Sıkı yasal denetimler ve detaylı risk raporlamalarıyla geçen masa başı temposu.'},
                {'ad': 'Veri ve Mali Hukuk Danışmanı', 'ikon': '💼', 'egitim_zorluklari': 'Sürekli değişen karmaşık vergi yasalarını hatasız takip etmek ve ezberlemek.', 'is_temposu': 'Mali tabloların incelenmesi ve müvekkil danışmanlık görüşmeleriyle geçer.'}
            ]
        },
        'Sağlık ve Canlı Bilimleri': {
            'brans_adi': 'Sağlık ve Canlı Bilimleri',
            'meslekler': [
                {
                    'ad': 'Kişiselleştirilmiş Genomik Danışmanı',
                    'ikon': '🧬',
                    'egitim_zorluklari': 'Moleküler biyoloji, genetik, tıp ve biyoenformatik temellerini birleştirmek; DNA dizilimlerindeki en minik anomalileri okuyabilmek uzun ve ağır bir akademik eğitim gerektirir.',
                    'is_temposu': 'Yoğun konsantrasyon gerektirir. Genetik analiz raporları incelenir ve hastalarla birebir hassas danışmanlık seansları yürütülür.'
                },
                {
                    'ad': 'Biyonik Organ Entegrasyon Uzmanı',
                    'ikon': '🦾',
                    'egitim_zorluklari': 'Biyomedikal mühendisliği ile insan sinir sisteminin biyolojisini aynı anda çözmek, yapay organların doku reddi riskini hesaplamak çok ileri düzey Ar-Ge çalışması ister.',
                    'is_temposu': 'Hassas ve teknoloji odaklıdır. Laboratuvar simülasyonları ve cerrahi ekiplerle ortak entegrasyon testleri yapılır.'
                },
                {
                    'ad': 'Tele-Sağlık Sistemleri Mimarı',
                    'ikon': '📡',
                    'egitim_zorluklari': 'Hem tıbbi cihazların çalışma mantığını hem de sıfır gecikmeli (zero-latency) kritik ağ mimarilerini tasarlayacak teknik donanıma sahip olmak.',
                    'is_temposu': 'Ağ testleri, akıllı hastane yazılımlarının entegrasyonu ve sistem güvenlik denetimleriyle geçen tempolu bir iştir.'
                },
                {'ad': 'Biyoteknoloji Uzmanı', 'ikon': '🧫', 'egitim_zorluklari': 'Steril laboratuvar disiplini, başarısız geçen yüzlerce deneyin yarattığı psikolojik yorgunluk ve sabır.', 'is_temposu': 'Hücre kültürü çalışmaları ve titiz laboratuvar deneyleriyle geçen sakin ama dikkatli bir tempo.'},
                {'ad': 'Robotik Cerrahi Asistan / Uzmanı', 'ikon': '🏥', 'egitim_zorluklari': 'Tıp fakültesi ve cerrahi ihtisasının getirdiği yıllarca süren nöbetli, uykusuz ve aşırı stresli eğitim süreci.', 'is_temposu': 'Ağır ve yüksek streslidir. Ameliyathanede saniyelerin kritik olduğu robotik operasyonlar yönetilir.'},
                {'ad': 'Nöroteknoloji ve Beyin-Bilgisayar Arayüz Uzmanı', 'ikon': '🧠', 'egitim_zorluklari': 'İnsan beyninin nöron ağlarını ve sinyallerini dijital koda çevirecek karmaşık sinyal işleme matematiğini öğrenmek.', 'is_temposu': 'EEG veri analizi ve cihaz kalibrasyon testleriyle geçen ileri teknoloji temposu.'},
                {'ad': 'Yapay Organ ve Doku Mühendisi', 'ikon': '🫀', 'egitim_zorluklari': 'Laboratuvarda canlı doku iskeleleri kurmak ve hücrelerin ölmeden yaşamasını sağlamak aşırı hassasiyet ister.', 'is_temposu': 'Biyoreaktör takipleri ve doku üretim aşamalarının izlendiği titiz bir laboratuvar temposu.'},
                {'ad': 'Tıbbi Yapay Zekâ Teşhis Uzmanı', 'ikon': '💻', 'egitim_zorluklari': 'Tıp bilimiyle yapay zekâ görüntü işleme algoritmalarını harmanlayacak yazılım ve tıp bilgisini birleştirmek.', 'is_temposu': 'Medikal görüntü analizi ve AI model doğrulama testleriyle geçen ekran başı temposu.'},
                {'ad': 'Nanotıp ve Akıllı İlaç Tasarımcısı', 'ikon': '💊', 'egitim_zorluklari': 'Atomik ve moleküler düzeyde kimya bilmek, nano robotların vücuttaki hareketini modellemek.', 'is_temposu': 'Moleküler modelleme ve sentez testlerinin yapıldığı Ar-Ge laboratuvarı temposu.'},
                {'ad': 'Epidemiyoloji ve Küresel Sağlık Analisti', 'ikon': '🦠', 'egitim_zorluklari': 'İleri istatistik modelleriyle salgın hastalıkların yayılımını matematiksel olarak modellemek.', 'is_temposu': 'Demografik sağlık verilerinin incelendiği ve kriz senaryolarının üretildiği analitik bir tempo.'}
            ]
        },
        'Tasarım, Mimari ve Sanat': {
            'brans_adi': 'Tasarım, Mimari ve Sanat',
            'meslekler': [
                {'ad': 'Metaverse / UX Deneyim Mimarı', 'ikon': '🥽', 'egitim_zorluklari': 'Sürekli değişen 3D render motorlarını (Unreal/Blender) ve insan psikolojisini (UX) aynı anda öğrenmek.', 'is_temposu': '3D wireframe tasarımları ve kullanıcı deneyimi testleriyle geçen yaratıcı ve tempolu bir iş.'},
                {'ad': 'Üst Düzey AI Sanat Direktörü', 'ikon': '🎨', 'egitim_zorluklari': 'Klasik sanat eğitimini, renk/kompozisyon bilgisini yapay zekâ prompt araçlarıyla harmanlama ustalığı.', 'is_temposu': 'Görsel üretim süreçleri ve reklam konsept seçimleriyle geçen yaratıcı tempo.'},
                {'ad': 'Eko-Mimari ve Akıllı Malzeme Tasarımcısı', 'ikon': '🌿', 'egitim_zorluklari': 'Mimari tasarımla doğa dostu, kendi kendini onaran akıllı yapı malzemelerinin kimyasını öğrenmek.', 'is_temposu': 'Çevreci yapı tasarımı ve malzeme test raporlarının incelendiği ofis/atölye temposu.'},
                {'ad': 'Sanal Gerçeklik (VR) Çevre Tasarımcısı', 'ikon': '🌐', 'egitim_zorluklari': '3D modelleme yazılımlarında yüksek kaliteli gerçekçi dokular üretirken donanım optimizasyonunu tutturmak.', 'is_temposu': 'Unreal Engine ve VR gözlük testleriyle geçen stüdyo temposu.'},
                {'ad': 'Dijital Moda ve Avatar Stilisti', 'ikon': '👗', 'egitim_zorluklari': 'Klasik moda tasarımının ötesine geçip kumaşların fiziksel simülasyonlarını 3D kodlamayı öğrenmek.', 'is_temposu': 'Marvelous Designer ve avatar giydirme süreçleriyle geçen dijital moda temposu.'},
                {'ad': 'Akıllı Ürün ve Endüstriyel Tasarımcı', 'ikon': '⌚', 'egitim_zorluklari': 'Ergonomi, estetik ve seri üretim maliyetleri dengesini CAD programlarında hatasız kurmak.', 'is_temposu': 'CAD modelleme ve prototip incelemeleriyle geçen tasarım atölyesi temposu.'},
                {'ad': 'Oyun Deneyimi (Game UX) Tasarımcısı', 'ikon': '🎮', 'egitim_zorluklari': 'Oyuncunun psikolojisini okuyup karmaşık oyun menülerini tamamen sezgisel ve akıcı kılmak.', 'is_temposu': 'Oyun akış şemaları ve oyuncu test geri bildirimlerinin analiz edildiği tempolu bir stüdyo ortamı.'},
                {'ad': 'Kapsamlı Marka Kimliği Tasarımcısı', 'ikon': '✒️', 'egitim_zorluklari': 'Şirketlerin ruhunu tek bir logoda özetlemek ve sürekli değişen müşteri revizyon kaprisleriyle başa çıkmak.', 'is_temposu': 'Logo tasarımları ve marka kılavuzu hazırlıklarıyla geçen ajans temposu.'},
                {'ad': 'Dijital Sergi ve Müze Küratörü', 'ikon': '🏛️', 'egitim_zorluklari': 'Sanat tarihi birikimini dijital sergi salonları ve sanal gerçeklik altyapısıyla harmanlamak.', 'is_temposu': 'Sergi konsept kurgusu ve sanal galeri turlarının yönetildiği kültür-sanat temposu.'},
                {'ad': 'Akustik ve Ses Manzarası Tasarımcısı', 'ikon': '🎵', 'egitim_zorluklari': 'Fiziksel ses dalgaları hesaplamalarını ve dijital ses işleme yazılımlarını kusursuz bilmek.', 'is_temposu': 'Ses yalıtım simülasyonları ve oyun/mekân ses tasarımı yapılan akustik stüdyo temposu.'}
            ]
        },
        'Sosyoloji, Hukuk ve Araştırma': {
            'brans_adi': 'Sosyoloji, Hukuk ve Araştırma',
            'meslekler': [
                {'ad': 'Bilişim ve Yapay Zekâ Hukuku Uzmanı', 'ikon': '⚖️', 'egitim_zorluklari': 'Hukuk fakültesini bitirdikten sonra yazılım mimarilerini, algoritmaları ve sürekli değişen teknoloji yasalarını ezberlemek gerekir.', 'is_temposu': 'Yoğun mevzuat takibi, sözleşme incelemeleri ve mahkeme/müvekkil görüşmeleriyle geçen tempolu bir hukuk bürosu temposu.'},
                {'ad': 'Dijital Sosyolog & Araştırmacı', 'ikon': '🔍', 'egitim_zorluklari': 'Sosyoloji teorilerini internetin devasa veri akışı (big data) ve sosyal medya algoritmalarıyla okumayı öğrenmek.', 'is_temposu': 'Sosyal medya topluluk analizi ve akademik rapor yazımıyla geçen akademik/araştırma temposu.'},
                {'ad': 'Kripto Varlık ve Blokzincir Hukukçusu', 'ikon': '🪙', 'egitim_zorluklari': 'Merkeziyetsiz finans dünyasının henuz oturmamış yasal boşluklarını ve sınır ötesi dijital suçları takip etmek.', 'is_temposu': 'Kripto varlık düzenleme incelemeleri ve danışmanlık görüşmeleriyle koşturmacalıdır.'},
                {'ad': 'Uluslararası İnsan Hakları ve Teknoloji Savunucusu', 'ikon': '🛡️', 'egitim_zorluklari': 'Küresel teknoloji devlerinin devasa lobilerine karşı dijital hakları koruyacak hukuki argümanlar üretmek.', 'is_temposu': 'Dijital hak ihlalleri raporlamaları ve STK koordinasyon toplantılarıyla geçer.'},
                {'ad': 'Yapay Zekâ ve Veri Etiği Danışmanı', 'ikon': '📜', 'egitim_zorluklari': 'Felsefe/etik ile teknik yapay zekâ kararlarını buluşturacak tarafsız denetim mekanizmaları kurmak.', 'is_temposu': 'Şirketlerin veri politikası denetimleri ve etik kurul toplantılarıyla geçer.'},
                {'ad': 'Dijital Suçlar ve Siber Soruşturma Uzmanı', 'ikon': '🕵️‍♂️', 'egitim_zorluklari': 'Siber suçluların internette bıraktığı gizli dijital izleri, logları ve silinmiş verileri adli bilişim teknikleriyle geri getirmek.', 'is_temposu': 'Adli bilişim incelemeleri ve siber soruşturma dosyalarının hazırlandığı dikkatli bir tempo.'},
                {'ad': 'Fikri Mülkiyet ve Patent Vekili', 'ikon': '📝', 'egitim_zorluklari': 'Mühendislik icatlarını ve teknik patent dosyalarını inceleyip hukuki olarak koruma altına almak.', 'is_temposu': 'Patent başvuru incelemeleri ve marka ihlal davalarının takip edildiği ofis temposu.'},
                {'ad': 'Kritik Altyapılar Güvenlik Politikası Uzmanı', 'ikon': '⚡', 'egitim_zorluklari': 'Ülke genelindeki enerji ve su gibi kritik sistemlerin siber güvenlik açıklarını stratejik düzeyde analiz etmek.', 'is_temposu': 'Stratejik risk değerlendirmeleri ve kamu-özel sektör brifingleriyle geçen kritik bir tempo.'},
                {'ad': 'Yeni Medya ve İletişim Hukukçusu', 'ikon': '📱', 'egitim_zorluklari': 'İnternet üzerindeki kişilik hakları ihlallerini, telif ve erişim engeli süreçlerini yönetmek.', 'is_temposu': 'Sosyal medya erişim engeli dosyaları ve dava takiplerinin yapıldığı yoğun tempo.'},
                {'ad': 'Küresel Jeopolitik Risk Analisti', 'ikon': '🌐', 'egitim_zorluklari': 'Dünya genelindeki siyasi ve ekonomik kırılmaları doğru okuyacak tarih ve dış politika birikimi.', 'is_temposu': 'Küresel bülten taramaları ve risk senaryo raporlarının üretildiği analitik bir tempo.'}
            ]
        }
    }
    
    secilen_veri = simulasyon_verileri.get(alan, simulasyon_verileri['Teknik, Mühendislik ve Yapay Zekâ'])

    return render_template('rol-simulasyonu.html', simulasyonlar=secilen_veri, alan=alan)

@app.route('/yol-haritasi')
def yol_haritasi():
    meslek_adi = request.args.get('meslek', 'Hedef Meslek')
    alan = request.args.get('alan', 'Kariyer Alanı')
    
    # 1. Meslek adını ve alanı küçük harfe çevirerek analiz kelimeleri çıkaralım
    ad_kucuk = meslek_adi.lower()
    alan_kucuk = alan.lower()
    
    # 2. Akıllı Sıralama ve Puan Belirleme Motoru (Her mesleğe göre esner)
    if any(k in ad_kucuk for k in ['uzman', 'mühendis', 'cerrah', 'mimar', 'direktör', 'stratejist', 'analist', 'lider']):
        if any(k in alan_kucuk for k in ['teknik', 'mühendislik', 'sağlık', 'canlı']):
            siralama = 'İlk 5.000 - 20.000 arası'
            puan = '490 - 540 Puan aralığı'
        else:
            siralama = 'İlk 10.000 - 30.000 arası'
            puan = '440 - 490 Puan aralığı'
    elif any(k in ad_kucuk for k in ['asistan', 'geliştirici', 'programcı', 'uzman yardımcısı', 'operatör']):
        siralama = 'İlk 25.000 - 60.000 arası'
        puan = '400 - 460 Puan aralığı'
    else:
        # Tamamen bilinmeyen veya özgün bir meslek gelse bile akıllı bant aralığı
        siralama = 'İlk 15.000 - 50.000 arası (Rekabetçi Sektör)'
        puan = '420 - 500 Puan aralığı'

    # 3. Alanına ve meslek adına göre akıllı ders tavsiyesi türetme
    if 'teknik' in alan_kucuk or 'mühendis' in alan_kucuk or 'yapay zekâ' in alan_kucuk:
        puan_turu = 'SAYISAL (SAY)'
        tavsiye_dersler = 'TYT-AYT Matematik, Geometri, Fizik ve analitik problem çözme becerileri.'
    elif 'sağlık' in alan_kucuk or 'canlı' in alan_kucuk:
        puan_turu = 'SAYISAL (SAY)'
        tavsiye_dersler = 'TYT-AYT Matematik, Biyoloji (Kalıtım ve Sistemler) ve Kimya.'
    elif 'ekonomi' in alan_kucuk or 'yönetim' in alan_kucuk or 'sosyal' in alan_kucuk:
        puan_turu = 'EŞİT AĞIRLIK (EA)'
        tavsiye_dersler = 'TYT-AYT Matematik ve Türkçe (Türk Dili ve Edebiyatı).'
    elif 'sözel' in alan_kucuk or 'medya' in alan_kucuk:
        puan_turu = 'SÖZEL (SÖZ) / DİL'
        tavsiye_dersler = 'Türk Dili ve Edebiyatı, Tarih, Coğrafya ve Sosyal Bilimler.'
    else:
        puan_turu = 'SAYISAL / EŞİT AĞIRLIK (Alan Esnek)'
        tavsiye_dersler = 'TYT temel matematik ve Türkçe netlerini tavan yapacak soru kampları.'

    # 4. Dinamik olarak hazırlanan kusursuz rehber
    harita = {
        'puan_turu': puan_turu,
        'taban_siralamasi': siralama,
        'son_yil_puan': puan,
        'agirlik_verilmesi_gereken_dersler': tavsiye_dersler,
        'nasil_calisilmali': f"'{meslek_adi}' hedefine ulaşmak için lise son sınıfta sadece konu çalışmak yetmez. Haftalık deneme analizleri yaparak yanlış yaptığın soru tipleri üzerine gitmeli, bu mesleğin gerektirdiği pratik yetkinlikleri şimdiden araştırmalısın.",
        'kazananlarin_zorlandigi_noktalar': f"Geçen sene bu alandaki vizyoner rollere yerleşen öğrenciler, ilk dönem lise ezber sisteminden çıkıp üniversite düzeyindeki analitik ve pratik tempo uyum sürecinde en çok zaman yönetimi ve istikrar konularında zorlandıklarını belirtiyorlar."
    }

    return render_template('yol-haritasi.html', meslek_adi=meslek_adi, alan=alan, harita=harita)

@app.route('/ders_programi')
def ders_programi():
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    meslek = request.args.get('meslek', 'Hedef Meslek')
    
    # Alana göre haftalık ders çalışma programı stratejisi ve dağılımı
    if 'Teknik' in alan or 'Mühendislik' in alan or 'Sağlık' in alan:
        program_adi = "SAYISAL YKS Zirve Hazırlık Programı"
        gunler = [
            {'gun': 'Pazartesi', 'odak': 'TYT-AYT Matematik', 'detay': 'Sabah 2 saat AYT Matematik (Türev/İntegral/Trigonometri), Akşam 1.5 saat TYT Matematik Branş Denemesi ve Paragraf.'},
            {'gun': 'Salı', 'odak': 'Fizik & Türkçe', 'detay': 'Sabah AYT Fizik (Mekanik/Elektrik), Öğleden sonra TYT Türkçe (Dil Bilgisi ve Paragraf kampı).'},
            {'gun': 'Çarşamba', 'odak': 'Matematik & Kimya', 'detay': 'Sabah AYT Matematik soru bankası çözümü, Akşam AYT Kimya (Organik Kimya ağırlıklı çalışma).'},
            {'gun': 'Perşembe', 'odak': 'Biyoloji & Geometri', 'detay': 'Sabah AYT Biyoloji (Sistemler ve Genetik), Akşam Geometri (Üçgenler ve Çember kampı).'},
            {'gun': 'Cuma', 'odak': 'Genel Tekrar & Deneme', 'detay': 'Haftalık işlenen konuların fasikül taramaları, yanlış yapılan soruların analizi ve defterenotu çıkarılması.'},
            {'gun': 'Cumartesi', 'odak': 'TYT Genel Deneme', 'detay': 'Sabah tam zamanlı TYT Deneme Sınavı (Süre tutarak), Öğleden sonra detaylı deneme analizi ve eksik kapatma.'},
            {'gun': 'Pazar', 'odak': 'AYT Branş Denemeleri & Dinlenme', 'detay': 'Sabah AYT Matematik/Fen branş denemesi, Akşam ise zihni dinlendirme ve gelecek haftanın planlaması.'}
        ]
    elif 'Ekonomi' in alan or 'Yönetim' in alan or 'Sosyal' in alan:
        program_adi = "EŞİT AĞIRLIK (EA) Zirve Hazırlık Programı"
        gunler = [
            {'gun': 'Pazartesi', 'odak': 'AYT Matematik & Paragraf', 'detay': 'Sabah 2 saat AYT Matematik (Fonksiyonlar, Polinomlar), Akşam TYT Paragraf ve Türkçe denemesi.'},
            {'gun': 'Salı', 'odak': 'Edebiyat & Tarih', 'detay': 'Sabah AYT Türk Dili ve Edebiyatı (Cumhuriyet Dönemi / Divan Edebiyatı), Akşam Tarih-1 çalışması.'},
            {'gun': 'Çarşamba', 'odak': 'Matematik & Coğrafya', 'detay': 'Sabah AYT Matematik problem kampı, Akşam Coğrafya-1 harita ve beşeri sistemler analizi.'},
            {'gun': 'Perşembe', 'odak': 'Edebiyat & Felsefe Grubu', 'detay': 'Sabah Edebiyat yazar-eser ezberleri ve soru çözümü, Akşam Felsefe ve Din Kültürü tekrarları.'},
            {'gun': 'Cuma', 'odak': 'Analiz & Soru Çözümü', 'detay': 'Haftalık çözülemeyen soruların hocalarla çözdürülmesi ve eksik konuların taranması.'},
            {'gun': 'Cumartesi', 'odak': 'TYT Genel Deneme', 'detay': 'Sabah gerçek sınav provası niteliğinde TYT Denemesi, Öğleden sonra detaylı analiz.'},
            {'gun': 'Pazar', 'odak': 'AYT Deneme & Motivasyon', 'detay': 'Sabah AYT Eşit Ağırlık Deneme Sınavı, Akşam hafif okumalar ve dinlenme.'}
        ]
    else:
        program_adi = "SÖZEL / GENEL YKS Başarı Programı"
        gunler = [
            {'gun': 'Pazartesi', 'odak': 'Edebiyat & Türkçe', 'detay': 'Sabah AYT Edebiyat detaylı konu çalışması, Akşam TYT Türkçe paragraf rutini.'},
            {'gun': 'Salı', 'odak': 'Tarih & Coğrafya', 'detay': 'Sabah AYT Tarih (İnkılap ve Dünya Tarihi), Akşam Coğrafya genel tekrarı.'},
            {'gun': 'Çarşamba', 'odak': 'Felsefe & Yabancı Dil / Sosyal', 'detay': 'Sabah Felsefe grubu kavram haritaları, Akşam sosyal bilimler soru çözümleri.'},
            {'gun': 'Perşembe', 'odak': 'Edebiyat Soru Kampı', 'detay': 'Edebiyat soru bankası üzerinden en az 150 soru ve yanlış analizi.'},
            {'gun': 'Cuma', 'odak': 'Genel Tekrar', 'detay': 'Haftalık notların baştan sona gözden geçirilmesi.'},
            {'gun': 'Cumartesi', 'odak': 'TYT Deneme Sınavı', 'detay': 'Sabah 135 dakika TYT Denemesi ve öğleden sonra analiz.'},
            {'gun': 'Pazar', 'odak': 'Sözel Deneme & Dinlenme', 'detay': 'Sabah AYT Sözel branş denemesi, akşam dinlenme.'}
        ]

    return render_template('ders_programi.html', program_adi=program_adi, gunler=gunler, alan=alan, meslek=meslek)

@app.route('/bitti')
def bitti():
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    return render_template('bitti.html', alan=alan)

if __name__ == '__main__':
    app.run(debug=True,port=5000)


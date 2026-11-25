from unittest import result

from flask import Flask,render_template,request,redirect,url_for
from database import get_db_connection
import traceback
from simulasyon_katalogu import SIMULASYON_VERILERI
from karsilastirma_katalogu import KARSILASTIRMA_SEMASI
from gelecek_katalogu import GELECEK_TRENDLERI
from ders_programi import program_getir
app = Flask(__name__)
@app.route('/')
def giris():
    return render_template('exam_score.html')

def safe_int(value,default=0):
    try:
        return(value) if value else default
    except(TypeError,ValueError):
        return default

@app.route('/ana-sayfa')
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

    aktif_ogrenci_id = 1  # form veya session'dan gelen ogrenci_id
    test_sonucu_kaydet(
        ogrenci_id=aktif_ogrenci_id,
        puanlar=puanlar,
        toplam_isaretlenen=toplam_isaretlenen,
        ilgi_kariyeri=secilen_sonuc['alan']
    )

    return render_template('sonuclar.html', 
                           puan=toplam_isaretlenen, 
                           alan=secilen_sonuc['alan'], 
                           aciklama=secilen_sonuc['aciklama'],
                           puanlar=puanlar)

def test_sonucu_kaydet(ogrenci_id,puanlar,toplam_isaretlenen,ilgi_kariyeri):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        ##İlgili rehber bilgisini ogrenci_id üzerinden getir
        cursor.execute("""
            SELECT FIRST_NAME,LAST_NAME from "C##CAREER_PLANNING_ASSISTANT".USERS
                WHERE OGRENCI_ID = :1
        """,(ogrenci_id,))
        rehber_row = cursor.fetchone()
        rehber_bilgi = f"{rehber_row[0]} {rehber_row[1] or ' '}".strip() if rehber_row else "Rehber atanmamış"

        #Test sonuclarını dogrudan ogrenci_user_db'ye gonder
        insert_res_sql = """
                INSERT INTO "C##CAREER_PLANNING_ASSISTANT".USER_TEST_RESULTS
                    (OGRENCI_ID,CATEGORY_NAME,SCORE_PERCENTAGE,ILGI_KARIYERI)
                    VALUES (:1, :2, :3, :4)
                """
        kayitlar = [
            (
                ogrenci_id,
                kat,round((puan_degeri / toplam_isaretlenen) * 100,2) if toplam_isaretlenen > 0 else 0.0,
                ilgi_kariyeri
            )
            for kat, puan_degeri in puanlar.items()
        ]
        cursor.executemany(insert_res_sql,kayitlar)

        connection.commit()
        cursor.close()
        connection.close()
        print(f"✅ Öğrenci ID {ogrenci_id} (Rehber: {rehber_bilgi}) için sonuçlar kaydedildi.")

    except Exception as e:
        print(f"❌ Kayıt hatası: {e}")
        traceback.print_exc()



def _float_veya_none(val):
    if val is None or str(val).strip() == '':
        return None
    try:
        return float(val)
    except ValueError:
        return None

def exam_score_kaydet(ogrenci_id,sinav_turu,deneme_adi,tyt_net=None,ayt_net=None,obp_puani=None,lgs_puani=None,yuzdelik_dilim=None,zayif_dersler=None,exam_year=2026):
    connection=get_db_connection()
    cursor = connection.cursor()

    calc_score = None
    if sinav_turu == 'YKS':
        t = tyt_net or 0.0
        a = ayt_net or 0.0
        o = obp_puani or 0.0
        #Yaklaşık YKS yerleştirme puani simulasyonu(500+OBP)
        calc_score = round(100+(t*1.35) + (a*2.95)+(o*0.6),3)

    insert_sql = """
        INSERT INTO "C##CAREER_PLANNING_ASSISTANT".exam_scores
            (ogrenci_id,sinav_turu,deneme_adi,tyt_net,ayt_net,obp_puani,calculated_palcement_score,lgs_puani,yuzdelik_dilim,zayif_dersler,exam_year)
            VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)
    """
    cursor.execute(
        insert_sql,
        (int(ogrenci_id),sinav_turu,deneme_adi,tyt_net,ayt_net,obp_puani,calc_score,lgs_puani,yuzdelik_dilim,zayif_dersler,int(exam_year))
    )
    connection.commit()
    cursor.close()
    connection.close()

def _denemeleri_getir(ogrenci_id):
    connecion = get_db_connection()
    cursor = connecion.cursor()
    cursor.execute(
        """
            SELECT sinav_turu,deneme_adi,tyt_net,ayt_net,calculated_placement_score,lgs_puani,yuzdelik_dilim,zayif_dersler
            FROM "C##CAREER_PLANNING_ASSISTANT".exam_scores
                WHERE ogrenci_id = :1
                ORDER BY score_id DESC
        """,
        (int(ogrenci_id),)
    )
    rows = cursor.fetchall()
    cursor.close()
    connecion.close()
    return rows

@app.route('/exam_scores',methods=['GET','POST'])
def exam_scores_sayfasi():
    ogrenci_id = int(request.args.get('ogrenci_id') or request.form.get('ogrenci_id') or 1)
    mesaj = None

    if request.method == 'POST':
        sinav_turu = request.form.get('sinav_turu','YKS')
        deneme_adi = request.form.get('deneme_adi','').strip()
        exam_year = request.form.get('exam_year') or 2026
        zayif_dersler = request.form.get('zayif_dersler','').strip() or None

        tyt_net = _float_veya_none(request.form.get('tyt_net'))
        ayt_net = _float_veya_none(request.form.get('ayt_net'))
        obp_puani = _float_veya_none(request.form.get('obp_puani'))
        lgs_puani = _float_veya_none(request.form.get('lgs_puani'))
        yuzdelik_dilim = _float_veya_none(request.form.get('yuzdelik_dilim'))

        if deneme_adi:
            try:
                exam_score_kaydet(
                    ogrenci_id=ogrenci_id,
                    sinav_turu=sinav_turu,
                    deneme_adi=deneme_adi,
                    tyt_net=tyt_net,
                    ayt_net=ayt_net,
                    obp_puani=obp_puani,
                    lgs_puani=lgs_puani,
                    yuzdelik_dilim=yuzdelik_dilim,
                    zayif_dersler=zayif_dersler,
                    exam_year=exam_year
                )
                mesaj = f"✅ {sinav_turu} deneme sonucu başarıyla kaydedildi!"

            except Exception as e:
                print(f"❌ Deneme kayıt hatası: {e}")
                traceback.print_exc()
                mesaj = f"Kayıt sırasında hata oluştu: {e}"

    denemeler = _denemeleri_getir(ogrenci_id)
    return render_template(
        'exam_score.html',
        ogrenci_id=ogrenci_id,
        denemeler=denemeler,
        mesaj=mesaj)


@app.route('/gelecek-meslekleri')
def gelecek_meslekleri():
    # Kullanıcının en son hangi alanda öne çıktığını query string veya session'dan alabiliriz.
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    varsayilan_alan = 'Teknik,ühendislik ve Yapay Zeka'

    # Seçilen alana ait meslekleri al, yoksa varsayılan teknik alanı getir
    meslekler_listesi = GELECEK_TRENDLERI.get(alan) or GELECEK_TRENDLERI[varsayilan_alan]

    return render_template('gelecek_meslekleri.html',
                           alan=alan,
                           meslekler=meslekler_listesi)

@app.route('/karsilastirma')
def karsilastirma():
    aktif_kriter = request.args.get('kriter', 'tumu')
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    varsayilan_alan = 'Teknik,Mühendislik ve Yapay Zeka'

    secilen_veri = KARSILASTIRMA_SEMASI.get(alan) or KARSILASTIRMA_SEMASI[varsayilan_alan]

    return render_template(
        'karsilastirma.html',
        veri=secilen_veri,
        alan=alan,
        aktif_kriter=aktif_kriter)

@app.route('/rol-simulasyonu')
def rol_simulasyonu():
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    varsayilan_alan = 'Teknik,Mühendislik ve Yapay Zeka'
    secilen_meslek_adi = request.args.get('meslek')
    
    # Karşılaştırma matrisindeki ilk 10 meslekle yüzde yüz uyumlu simülasyon havuzu
    secilen_veri = SIMULASYON_VERILERI.get(alan) or SIMULASYON_VERILERI[varsayilan_alan]


    meslekler = secilen_veri.get('meslekler',[])
    secilen_meslek = next(
        (m for m in meslekler if m['ad'] == secilen_meslek_adi),
        meslekler[0] if meslekler else {}
    )

    aktif_ogrenci_id = int(request.args.get('ogrenci_id') or 1)
    dept_id = secilen_veri.get('brans_adi',alan)
    time_slot = request.args.get('time_slot') or 'Genel Oturum'
    task_description = secilen_meslek.get('egitim_zorlukları') or f"{dept_id} simulasyonu"
    outcome_summary = secilen_meslek.get('is_temposu')

    role_simulations_kaydet(
        ogrenci_id=aktif_ogrenci_id,
        dept_id=dept_id,
        time_slot=time_slot,
        task_description=task_description[:500],
        outcome_summary=outcome_summary[:500] if outcome_summary else None
    )

    return render_template(
        'rol-simulasyonu.html',
                           simulasyonlar=secilen_veri,
                           alan=alan,
                           secilen_meslek=secilen_meslek)

def role_simulations_kaydet(ogrenci_id,dept_id,time_slot,task_description,outcome_summary=None):
    try:
        connection=get_db_connection()
        cursor = connection.cursor()

        insert_sim_sql = """
            INSERT INTO "C##CAREER_PLANNING_ASSISTANT".role_simulations
            (ogrenci_id,dept_id,time_slot,task_description,outcome_summary)
                VALUES(:1,:2,:3,:4,:5)
        """
        cursor.execute(
            insert_sim_sql,
            (int(ogrenci_id), str(dept_id)[:100], str(time_slot)[:50], str(task_description)[:500],
             str(outcome_summary)[:500] if outcome_summary else None)
        )

        connection.commit()
        print(f"✅ Öğrenci ID {ogrenci_id} için simülasyon kaydedildi ({dept_id}).")
        return True

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"❌ Simülasyon kayıt hatası: {e}")
        traceback.print_exc()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


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


def _son_test_puani_getir(ogrenci_id):
    if not ogrenci_id:
        return None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT score_percentage
            FROM "C##CAREER_PLANNING_ASSISTANT".user_test_results
                WHERE ogrenci_id = :1
                ORDER BY created_at DESC,result_id DESC
                FETCH FIRST 1 ROWS ONLY
            """,
            (int(ogrenci_id),)
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row[0] if row else None
    except Exception as e:
        print(f"⚠️ Test puanı okunamadı: {e}")
        return None
@app.route('/ders_programi')
def ders_programi():
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    meslek = request.args.get('meslek', 'Hedef Meslek')
    seviye_param = request.args.get('seviye')
    ogrenci_id = request.args.get('ogrenci_id')

    puan = _son_test_puani_getir(ogrenci_id) if not seviye_param else None
    aktif_seviye,program_adi,gunler = program_getir(
        alan = alan,
        seviye_param = seviye_param,
        puan=puan
    )


    return render_template(
        'ders_programi.html',
                           program_adi=program_adi,
                           gunler=gunler,
                           alan=alan, meslek=meslek)

@app.route('/bitti')
def bitti():
    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    return render_template('bitti.html', alan=alan)

def skill_gaps_birlesik_kaydet(ogrenci_id, alan_adi, test_puani):
    """
    Son deneme sonucu (exam_scores) ile test puani (user_test_results)
    birleştirilince skill_gaps kaydeder.
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT sinav_turu, tyt_net, ayt_net, obp_puani, calculated_placement_score,
                   lgs_puani, yuzdelik_dilim, zayif_dersler
            FROM "C##CAREER_PLANNING_ASSISTANT".exam_scores
            WHERE ogrenci_id = :1
            ORDER BY score_id DESC
            FETCH FIRST 1 ROWS ONLY
            """,
            (int(ogrenci_id),)
        )
        son_deneme = cursor.fetchone()

        test_skoru = max(0.0, min(100.0, float(test_puani or 0.0)))
        deneme_skoru_100 = test_skoru
        sinav_etiketi = "YKS"
        zayif_dersler = None

        if son_deneme:
            (
                sinav_turu,
                tyt_net,
                ayt_net,
                obp_puani,
                calc_score,
                lgs_puani,
                yuzdelik_dilim,
                zayif_dersler,
            ) = son_deneme
            sinav_etiketi = (sinav_turu or "YKS").upper()

            if sinav_etiketi == "LGS":
                if lgs_puani is not None:
                    deneme_skoru_100 = max(0.0, min(100.0, ((float(lgs_puani) - 100.0) / 400.0) * 100.0))
                elif yuzdelik_dilim is not None:
                    deneme_skoru_100 = max(0.0, min(100.0, 100.0 - float(yuzdelik_dilim)))
            else:
                # YKS tarafı
                if calc_score is not None:
                    deneme_skoru_100 = max(0.0, min(100.0, ((float(calc_score) - 100.0) / 400.0) * 100.0))
                else:
                    t_norm = min(1.0, max(0.0, float(tyt_net or 0.0) / 120.0)) * 55.0
                    a_norm = min(1.0, max(0.0, float(ayt_net or 0.0) / 80.0)) * 35.0
                    o_norm = min(1.0, max(0.0, max(0.0, float(obp_puani or 50.0) - 50.0) / 50.0)) * 10.0
                    deneme_skoru_100 = round(t_norm + a_norm + o_norm, 2)

        birlesik_skor = round((deneme_skoru_100 * 0.5) + (test_skoru * 0.5), 2)

        if birlesik_skor < 45:
            potansiyel = "Temel / Gelişime Açık"
        elif birlesik_skor < 75:
            potansiyel = "Orta - Güçlenen"
        else:
            potansiyel = "Yüksek Potansiyel"

        eksik_ozet = (
            zayif_dersler.strip()
            if zayif_dersler and zayif_dersler.strip()
            else (
                "TYT/AYT temel konular ve süre yönetimi"
                if sinav_etiketi == "YKS"
                else f"{alan_adi} temel kavram ve uygulama pratiği"
            )
        )

        if sinav_etiketi == "YKS":
            eksik_beceri = f"[YKS] {eksik_ozet} - Konu kavrama, branş neti ve AYT geçiş dengesi"
            edinim_yolu = (
                f"1) YKS denemesindeki {eksik_ozet} eksiklerini kısa konu tekrarı ve temel soru bankasıyla kapat; "
                f"2) {alan_adi} alanında düzenli TYT/AYT deneme analizi ve yanlış defteriyle birleşik puanını kademeli artır."
            )
        elif sinav_etiketi == "LGS":
            eksik_beceri = f"[LGS] {eksik_ozet} — Okuduğunu anlama, yeni nesil muhakeme ve zaman yönetimi"
            edinim_yolu = (
                f"1) LGS denemesindeki {eksik_ozet} başlıklarında temel kavram ve adım adım soru çözümü yap; "
                f"2) {alan_adi} ve sınav pratiğinde süre tutarak deneme çözüp yanlışlarını konu bazlı işle."
            )
        else:
            eksik_beceri = f"{eksik_ozet} — Temel kavram kavrama, uygulama ve düzenli tekrar"
            edinim_yolu = (
                f"1) {eksik_ozet} tarafındaki eksikleri kısa tekrar ve temel sorularla tamamla; "
                f"2) {alan_adi} alanında düzenli pratik ve analizle ilerle."
            )

        cursor.execute(
            """
            INSERT INTO "C##CAREER_PLANNING_ASSISTANT".skill_gaps
            (ogrenci_id, alan_adi, potansiyel_seviye, birlesik_skor, eksik_beceri, edinim_yolu)
            VALUES (:1, :2, :3, :4, :5, :6)
            """,
            (
                int(ogrenci_id),
                alan_adi,
                potansiyel,
                birlesik_skor,
                eksik_beceri[:250],
                edinim_yolu[:500],
            ),
        )
        connection.commit()
        print(
            f"✅ skill_gaps kaydedildi ({sinav_etiketi}) -> Öğrenci: {ogrenci_id}, Skor: {birlesik_skor}, Potansiyel: {potansiyel}"
        )
        return birlesik_skor, potansiyel

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"❌ skill_gaps kayıt hatası: {e}")
        traceback.print_exc()
        return None, None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def _skill_gaps_getir(ogrenci_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT gap_id, alan_adi, potansiyel_seviye, birlesik_skor, eksik_beceri, edinim_yolu, created_at
        FROM "C##CAREER_PLANNING_ASSISTANT".skill_gaps
        WHERE ogrenci_id = :1
        ORDER BY gap_id DESC
        """,
        (int(ogrenci_id),)
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


@app.route('/skill-gaps')
def skill_gaps_sayfasi():
    raw_id = request.args.get('ogrenci_id')
    try:
        ogrenci_id = int(raw_id) if raw_id and str(raw_id).strip() else 1
    except ValueError:
        ogrenci_id = 1

    alan = request.args.get('alan', 'Teknik, Mühendislik ve Yapay Zekâ')
    kayitlar = _skill_gaps_getir(ogrenci_id)

    # Sayfa ilk açıldığında kayıt yoksa mevcut son test/deneme verisiyle bir analiz üret
    if not kayitlar:
        son_puan = _son_test_puani_getir(ogrenci_id)
        if son_puan is not None:
            skill_gaps_birlesik_kaydet(
                ogrenci_id=ogrenci_id,
                alan_adi=alan,
                test_puani=son_puan
            )
            kayitlar = _skill_gaps_getir(ogrenci_id)

    return render_template(
        'skill_gaps.html',
        ogrenci_id=ogrenci_id,
        alan=alan,
        kayitlar=kayitlar
    )

if __name__ == '__main__':
    app.run(debug=True,port=5000)


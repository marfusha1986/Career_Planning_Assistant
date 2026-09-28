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
    #URL'den gelen puanı yakala
    puan = request.args.get('puan',0)
    return render_template('sonuclar.html',puan=puan)

@app.route('/gelecek-meslekleri')
def gelecek_meslekleri():
    conn= get_db_connection()
    cursor=conn.cursor()

    #Trend skoruna göre yüksekten en düşüğe sıralayalım
    cursor.execute("SELECT dept_name, dept_type, future_trend_score, salary_potential FROM C##CAREER_PLANNING_ASSISTANT.departments ORDER BY future_trend_score DESC")
    meslekler = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('gelecek_meslekleri.html',meslekler=meslekler)

if __name__ == '__main__':
    app.run(debug=True,port=5000)


import oracledb

def get_db_connection():
    try:
        #Oracle veritabanı bağlantı bilgileri
        connection = oracledb.connect(
            user="c##career_planning_assistant",
            password="Oracle1234",
            dsn="localhost:1521/FREE"
        )
        return connection
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None
import sqlite3
from contextlib import contextmanager
from datetime import datetime

class Database:
    def __init__(self, db_name="hasta_kayit.db"):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hastalar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tc_no TEXT UNIQUE NOT NULL,
                    ad TEXT NOT NULL,
                    soyad TEXT NOT NULL,
                    cinsiyet TEXT,
                    dogum_tarihi TEXT,
                    telefon TEXT,
                    kan_grubu TEXT,
                    poliklinik TEXT NOT NULL,
                    sikayet TEXT,
                    kayit_tarihi TEXT NOT NULL
                )
            """)
            conn.commit()
            
            # Eğer tablo boşsa örnek birkaç kayıt ekleyelim
            cursor.execute("SELECT COUNT(*) FROM hastalar")
            if cursor.fetchone()[0] == 0:
                ornek_hastalar = [
                    ("12345678901", "Ahmet", "Yılmaz", "Erkek", "1988-04-12", "0532 111 2233", "A Rh(+)", "Dahiliye (İç Hastalıkları)", "Son 3 gündür yüksek ateş, halsizlik ve mide bulantısı şikayeti var.", "2026-10-25 10:30"),
                    ("23456789012", "Ayşe", "Kaya", "Kadın", "1995-09-20", "0544 222 3344", "0 Rh(+)", "Göz Hastalıkları", "Uzağı görmede bulanıklık, göz kuruluğu ve baş ağrısı.", "2026-10-26 14:15"),
                    ("34567890123", "Mehmet", "Demir", "Erkek", "1976-12-05", "0555 333 4455", "B Rh(+)", "Kardiyoloji", "Göğüste sıkışma hissi, merdiven çıkarken nefes darlığı.", "2026-10-28 09:45"),
                    ("45678901234", "Fatma", "Çelik", "Kadın", "2001-07-18", "0505 444 5566", "AB Rh(-)", "Kulak Burun Boğaz (KBB)", "Boğaz ağrısı, yutkunma güçlüğü ve burun tıkanıklığı.", "2026-10-30 11:20"),
                    ("56789012345", "Can", "Öztürk", "Erkek", "1992-03-30", "0533 555 6677", "A Rh(-)", "Ortopedi ve Travmatoloji", "Sol dizde spor sonrası ağrı ve şişlik şikayeti.", "2026-10-31 08:50")
                ]
                cursor.executemany("""
                    INSERT INTO hastalar (tc_no, ad, soyad, cinsiyet, dogum_tarihi, telefon, kan_grubu, poliklinik, sikayet, kayit_tarihi)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, ornek_hastalar)
                conn.commit()

    def hasta_ekle(self, tc_no, ad, soyad, cinsiyet, dogum_tarihi, telefon, kan_grubu, poliklinik, sikayet):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            kayit_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute("""
                INSERT INTO hastalar (tc_no, ad, soyad, cinsiyet, dogum_tarihi, telefon, kan_grubu, poliklinik, sikayet, kayit_tarihi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (tc_no.strip(), ad.strip(), soyad.strip(), cinsiyet, dogum_tarihi.strip(), telefon.strip(), kan_grubu, poliklinik, sikayet.strip(), kayit_tarihi))
            conn.commit()
            return cursor.lastrowid

    def hasta_guncelle(self, hasta_id, tc_no, ad, soyad, cinsiyet, dogum_tarihi, telefon, kan_grubu, poliklinik, sikayet):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE hastalar 
                SET tc_no = ?, ad = ?, soyad = ?, cinsiyet = ?, dogum_tarihi = ?, telefon = ?, kan_grubu = ?, poliklinik = ?, sikayet = ?
                WHERE id = ?
            """, (tc_no.strip(), ad.strip(), soyad.strip(), cinsiyet, dogum_tarihi.strip(), telefon.strip(), kan_grubu, poliklinik, sikayet.strip(), hasta_id))
            conn.commit()
            return cursor.rowcount > 0

    def hasta_sil(self, hasta_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hastalar WHERE id = ?", (hasta_id,))
            conn.commit()
            return cursor.rowcount > 0

    def hasta_getir_by_id(self, hasta_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hastalar WHERE id = ?", (hasta_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def tc_var_mi(self, tc_no, haric_id=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if haric_id:
                cursor.execute("SELECT id FROM hastalar WHERE tc_no = ? AND id != ?", (tc_no.strip(), haric_id))
            else:
                cursor.execute("SELECT id FROM hastalar WHERE tc_no = ?", (tc_no.strip(),))
            return cursor.fetchone() is not None

    def hastalari_listele(self, arama_metni="", poliklinik="Tümü"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT id, tc_no, ad, soyad, cinsiyet, dogum_tarihi, telefon, kan_grubu, poliklinik, kayit_tarihi FROM hastalar WHERE 1=1"
            params = []

            if arama_metni:
                sql += " AND (tc_no LIKE ? OR ad LIKE ? OR soyad LIKE ? OR (ad || ' ' || soyad) LIKE ?)"
                arama_wildcard = f"%{arama_metni.strip()}%"
                params.extend([arama_wildcard, arama_wildcard, arama_wildcard, arama_wildcard])

            if poliklinik and poliklinik != "Tümü":
                sql += " AND poliklinik = ?"
                params.append(poliklinik)

            sql += " ORDER BY id DESC"
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    def istatistikleri_getir(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM hastalar")
            toplam_hasta = cursor.fetchone()[0]

            cursor.execute("SELECT poliklinik, COUNT(*) FROM hastalar GROUP BY poliklinik ORDER BY COUNT(*) DESC")
            poliklinik_dagilimi = cursor.fetchall()

            cursor.execute("SELECT cinsiyet, COUNT(*) FROM hastalar GROUP BY cinsiyet")
            cinsiyet_dagilimi = cursor.fetchall()

            return {
                "toplam_hasta": toplam_hasta,
                "poliklinik_dagilimi": poliklinik_dagilimi,
                "cinsiyet_dagilimi": cinsiyet_dagilimi
            }

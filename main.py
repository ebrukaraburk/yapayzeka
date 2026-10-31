import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
from database import Database

class HastaKayitUygulamasi:
    POLIKLINIKLER = [
        "Acil Servis",
        "Dahiliye (İç Hastalıkları)",
        "Kardiyoloji",
        "Göz Hastalıkları",
        "Kulak Burun Boğaz (KBB)",
        "Ortopedi ve Travmatoloji",
        "Nöroloji",
        "Genel Cerrahi",
        "Çocuk Sağlığı ve Hastalıkları",
        "Dermatoloji (Cildiye)",
        "Psikiyatri",
        "Üroloji",
        "Göğüs Hastalıkları",
        "Fizik Tedavi ve Rehabilitasyon"
    ]

    KAN_GRUPLARI = [
        "Seçiniz", "A Rh(+)", "A Rh(-)", "B Rh(+)", "B Rh(-)",
        "AB Rh(+)", "AB Rh(-)", "0 Rh(+)", "0 Rh(-)", "Bilinmiyor"
    ]

    CINSIYETLER = ["Seçiniz", "Erkek", "Kadın", "Belirtilmemiş"]

    def __init__(self, root):
        self.root = root
        self.root.title("SağlıkNet - Hasta Kayıt ve Yönetim Sistemi")
        self.root.geometry("1240x740")
        self.root.minsize(1050, 650)
        
        # Windows pencere simgesi için basit renk teması
        self.root.configure(bg="#f1f5f9")

        self.db = Database()
        self.secili_hasta_id = None

        self._stil_ayarla()
        self._arayuz_olustur()
        self.tabloyu_guncelle()

    def _stil_ayarla(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass

        # Renkler
        self.PRIMARY_COLOR = "#0284c7"      # Canlı Mavi
        self.PRIMARY_DARK = "#0369a1"
        self.SUCCESS_COLOR = "#16a34a"      # Yeşil
        self.SUCCESS_DARK = "#15803d"
        self.DANGER_COLOR = "#dc2626"       # Kırmızı
        self.DANGER_DARK = "#b91c1c"
        self.BG_MAIN = "#f1f5f9"
        self.CARD_BG = "#ffffff"
        self.TEXT_COLOR = "#1e293b"

        # Genel ttk Stilleri
        self.style.configure(".", background=self.BG_MAIN, foreground=self.TEXT_COLOR, font=("Segoe UI", 10))
        self.style.configure("Card.TFrame", background=self.CARD_BG, relief="flat")
        
        # Etiketler
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#ffffff", background="#1e3a8a")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground="#93c5fd", background="#1e3a8a")
        self.style.configure("CardTitle.TLabel", font=("Segoe UI", 12, "bold"), foreground="#0f172a", background=self.CARD_BG)
        self.style.configure("FormLabel.TLabel", font=("Segoe UI", 9, "bold"), foreground="#334155", background=self.CARD_BG)
        self.style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#475569", background="#e2e8f0")

        # Buton Stilleri
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.PRIMARY_COLOR, foreground="#ffffff", borderwidth=0, padding=6)
        self.style.map("Primary.TButton", background=[("active", self.PRIMARY_DARK), ("pressed", "#075985")])

        self.style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background=self.SUCCESS_COLOR, foreground="#ffffff", borderwidth=0, padding=6)
        self.style.map("Success.TButton", background=[("active", self.SUCCESS_DARK), ("pressed", "#14532d")])

        self.style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background=self.DANGER_COLOR, foreground="#ffffff", borderwidth=0, padding=6)
        self.style.map("Danger.TButton", background=[("active", self.DANGER_DARK), ("pressed", "#991b1b")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 9), background="#e2e8f0", foreground="#1e293b", padding=5)
        self.style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

        # Treeview (Tablo) Stilleri
        self.style.configure("Custom.Treeview", 
                             font=("Segoe UI", 9), 
                             rowheight=28, 
                             background="#ffffff", 
                             fieldbackground="#ffffff",
                             foreground="#1e293b",
                             borderwidth=0)
        self.style.configure("Custom.Treeview.Heading", 
                             font=("Segoe UI", 10, "bold"), 
                             background="#e2e8f0", 
                             foreground="#1e293b",
                             relief="flat",
                             padding=5)
        self.style.map("Custom.Treeview.Heading", background=[("active", "#cbd5e1")])
        self.style.map("Custom.Treeview", background=[("selected", "#bae6fd")], foreground=[("selected", "#0c4a6e")])

    def _arayuz_olustur(self):
        # 1. ÜST BAŞLIK BANDI
        header_frame = tk.Frame(self.root, bg="#1e3a8a", height=70)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg="#1e3a8a")
        header_content.pack(fill="both", expand=True, padx=25, pady=10)

        title_box = tk.Frame(header_content, bg="#1e3a8a")
        title_box.pack(side="left", fill="y")
        
        lbl_title = ttk.Label(title_box, text="🏥 SağlıkNet Hasta Kayıt & Yönetim Sistemi", style="Header.TLabel")
        lbl_title.pack(anchor="w")
        lbl_subtitle = ttk.Label(title_box, text="Poliklinik Randevu, Hasta Dosyası ve Takip Paneli", style="SubHeader.TLabel")
        lbl_subtitle.pack(anchor="w")

        # Sağ üst hızlı bilgi
        info_box = tk.Frame(header_content, bg="#1e3a8a")
        info_box.pack(side="right", fill="y")
        self.lbl_canli_saat = tk.Label(info_box, text=datetime.now().strftime("%d.%m.%Y"), font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#2563eb", padx=12, pady=5)
        self.lbl_canli_saat.pack(anchor="e")

        # 2. ANA İÇERİK ALANI (Sol Form, Sağ Liste)
        main_body = tk.Frame(self.root, bg=self.BG_MAIN)
        main_body.pack(fill="both", expand=True, padx=15, pady=15)

        # ---------------- SOL TARAF: HASTA KAYIT VE DÜZENLEME FORMU ----------------
        left_container = tk.Frame(main_body, bg=self.CARD_BG, width=380, highlightthickness=1, highlightbackground="#cbd5e1")
        left_container.pack(side="left", fill="y", padx=(0, 15))
        left_container.pack_propagate(False)

        # Form Başlığı
        form_header = tk.Frame(left_container, bg="#f8fafc", height=45)
        form_header.pack(fill="x", side="top")
        form_header.pack_propagate(False)

        self.lbl_form_baslik = tk.Label(form_header, text="📋 Hasta Bilgileri Girişi", font=("Segoe UI", 11, "bold"), fg="#0f172a", bg="#f8fafc")
        self.lbl_form_baslik.pack(side="left", padx=15, pady=10)

        # Düzenleme modu uyarısı rozeti
        self.badge_duzenleme = tk.Label(form_header, text="DÜZENLEME MODU", font=("Segoe UI", 8, "bold"), bg="#fef08a", fg="#854d0e", padx=6, pady=2)

        # Form Alanları İçin Kaydırılabilir / Düzenli Frame
        form_frame = tk.Frame(left_container, bg=self.CARD_BG, padx=15, pady=10)
        form_frame.pack(fill="both", expand=True)

        row_idx = 0

        # TC Kimlik No
        ttk.Label(form_frame, text="T.C. Kimlik No *", style="FormLabel.TLabel").grid(row=row_idx, column=0, sticky="w", pady=(2, 2))
        row_idx += 1
        self.ent_tc = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.ent_tc.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row_idx += 1

        # Ad ve Soyad (Yan Yana)
        ad_soyad_frame = tk.Frame(form_frame, bg=self.CARD_BG)
        ad_soyad_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Ad
        f_ad = tk.Frame(ad_soyad_frame, bg=self.CARD_BG)
        f_ad.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(f_ad, text="Adı *", style="FormLabel.TLabel").pack(anchor="w")
        self.ent_ad = ttk.Entry(f_ad, font=("Segoe UI", 10))
        self.ent_ad.pack(fill="x", pady=(2, 0))

        # Soyad
        f_soyad = tk.Frame(ad_soyad_frame, bg=self.CARD_BG)
        f_soyad.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ttk.Label(f_soyad, text="Soyadı *", style="FormLabel.TLabel").pack(anchor="w")
        self.ent_soyad = ttk.Entry(f_soyad, font=("Segoe UI", 10))
        self.ent_soyad.pack(fill="x", pady=(2, 0))
        row_idx += 1

        # Cinsiyet ve Kan Grubu (Yan Yana)
        cin_kan_frame = tk.Frame(form_frame, bg=self.CARD_BG)
        cin_kan_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        f_cin = tk.Frame(cin_kan_frame, bg=self.CARD_BG)
        f_cin.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(f_cin, text="Cinsiyet", style="FormLabel.TLabel").pack(anchor="w")
        self.cmb_cinsiyet = ttk.Combobox(f_cin, values=self.CINSIYETLER, state="readonly", font=("Segoe UI", 9))
        self.cmb_cinsiyet.current(0)
        self.cmb_cinsiyet.pack(fill="x", pady=(2, 0))

        f_kan = tk.Frame(cin_kan_frame, bg=self.CARD_BG)
        f_kan.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ttk.Label(f_kan, text="Kan Grubu", style="FormLabel.TLabel").pack(anchor="w")
        self.cmb_kan = ttk.Combobox(f_kan, values=self.KAN_GRUPLARI, state="readonly", font=("Segoe UI", 9))
        self.cmb_kan.current(0)
        self.cmb_kan.pack(fill="x", pady=(2, 0))
        row_idx += 1

        # Doğum Tarihi & Telefon (Yan Yana)
        dt_tel_frame = tk.Frame(form_frame, bg=self.CARD_BG)
        dt_tel_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        f_dt = tk.Frame(dt_tel_frame, bg=self.CARD_BG)
        f_dt.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(f_dt, text="Doğum Tarihi (Yıl/Yaş)", style="FormLabel.TLabel").pack(anchor="w")
        self.ent_dt = ttk.Entry(f_dt, font=("Segoe UI", 10))
        self.ent_dt.insert(0, "1990-01-01")
        self.ent_dt.pack(fill="x", pady=(2, 0))

        f_tel = tk.Frame(dt_tel_frame, bg=self.CARD_BG)
        f_tel.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ttk.Label(f_tel, text="Telefon", style="FormLabel.TLabel").pack(anchor="w")
        self.ent_tel = ttk.Entry(f_tel, font=("Segoe UI", 10))
        self.ent_tel.insert(0, "05")
        self.ent_tel.pack(fill="x", pady=(2, 0))
        row_idx += 1

        # Poliklinik Seçimi
        ttk.Label(form_frame, text="Poliklinik / Bölüm *", style="FormLabel.TLabel").grid(row=row_idx, column=0, sticky="w", pady=(2, 2))
        row_idx += 1
        self.cmb_poliklinik = ttk.Combobox(form_frame, values=self.POLIKLINIKLER, state="readonly", font=("Segoe UI", 10))
        self.cmb_poliklinik.current(1)
        self.cmb_poliklinik.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row_idx += 1

        # Şikayet ve Klinik Notlar
        ttk.Label(form_frame, text="Şikayet / Muayene Ön Notu", style="FormLabel.TLabel").grid(row=row_idx, column=0, sticky="w", pady=(2, 2))
        row_idx += 1
        self.txt_sikayet = tk.Text(form_frame, height=5, font=("Segoe UI", 9), relief="solid", borderwidth=1, bg="#ffffff", fg="#1e293b", wrap="word")
        self.txt_sikayet.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        row_idx += 1

        form_frame.columnconfigure(0, weight=1)

        # Butonlar Kutusu
        btn_box = tk.Frame(left_container, bg=self.CARD_BG, padx=15, pady=10)
        btn_box.pack(side="bottom", fill="x")

        self.btn_kaydet = ttk.Button(btn_box, text="💾 Yeni Hasta Kaydet", style="Success.TButton", command=self.hasta_kaydet)
        self.btn_kaydet.pack(fill="x", pady=(0, 6))

        self.btn_guncelle = ttk.Button(btn_box, text="✏️ Seçili Hastayı Güncelle", style="Primary.TButton", command=self.hasta_guncelle)
        # Varsayılanda güncelleme butonu inaktif
        self.btn_guncelle.pack(fill="x", pady=(0, 6))

        self.btn_temizle = ttk.Button(btn_box, text="🧹 Formu Temizle", style="Secondary.TButton", command=self.formu_temizle)
        self.btn_temizle.pack(fill="x")

        # ---------------- SAĞ TARAF: ARAMA, FİLTRE VE HASTA LİSTESİ ----------------
        right_container = tk.Frame(main_body, bg=self.CARD_BG, highlightthickness=1, highlightbackground="#cbd5e1")
        right_container.pack(side="right", fill="both", expand=True)

        # ARAMA VE ARAÇ ÇUBUĞU (Toolbar)
        toolbar = tk.Frame(right_container, bg="#f8fafc", padx=15, pady=12)
        toolbar.pack(side="top", fill="x")

        # Arama Kutusu
        tk.Label(toolbar, text="🔍 Hızlı Arama:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#475569").pack(side="left", padx=(0, 5))
        self.ent_arama = ttk.Entry(toolbar, font=("Segoe UI", 10), width=22)
        self.ent_arama.pack(side="left", padx=(0, 12))
        self.ent_arama.bind("<KeyRelease>", lambda event: self.tabloyu_guncelle())

        # Poliklinik Filtresi
        tk.Label(toolbar, text="Bölüm:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#475569").pack(side="left", padx=(0, 5))
        self.cmb_filtre_poli = ttk.Combobox(toolbar, values=["Tümü"] + self.POLIKLINIKLER, state="readonly", font=("Segoe UI", 9), width=20)
        self.cmb_filtre_poli.current(0)
        self.cmb_filtre_poli.pack(side="left", padx=(0, 10))
        self.cmb_filtre_poli.bind("<<ComboboxSelected>>", lambda event: self.tabloyu_guncelle())

        # Temizle Butonu
        btn_filtre_temizle = ttk.Button(toolbar, text="Filtreyi Sıfırla", style="Secondary.TButton", command=self.filtreyi_sifirla)
        btn_filtre_temizle.pack(side="left", padx=(0, 10))

        # Sağ Taraf Aksiyon Butonları (İstatistik & Dışa Aktar)
        btn_export = ttk.Button(toolbar, text="📥 Excel / CSV Aktar", style="Secondary.TButton", command=self.csv_aktar)
        btn_export.pack(side="right", padx=(5, 0))

        btn_istatistik = ttk.Button(toolbar, text="📊 İstatistikler", style="Secondary.TButton", command=self.istatistik_penceresi_ac)
        btn_istatistik.pack(side="right", padx=(5, 0))

        # TABLO (TREEVIEW) VE SCROLLBAR
        table_frame = tk.Frame(right_container, bg=self.CARD_BG)
        table_frame.pack(fill="both", expand=True, padx=12, pady=10)

        columns = ("id", "tc_no", "ad_soyad", "cinsiyet", "telefon", "kan_grubu", "poliklinik", "kayit_tarihi")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview", selectmode="browse")

        # Başlık ve Genişlik Tanımları
        self.tree.heading("id", text="ID")
        self.tree.heading("tc_no", text="T.C. Kimlik No")
        self.tree.heading("ad_soyad", text="Hasta Adı Soyadı")
        self.tree.heading("cinsiyet", text="Cinsiyet")
        self.tree.heading("telefon", text="Telefon")
        self.tree.heading("kan_grubu", text="Kan Grubu")
        self.tree.heading("poliklinik", text="Poliklinik")
        self.tree.heading("kayit_tarihi", text="Kayıt Tarihi")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("tc_no", width=110, anchor="center")
        self.tree.column("ad_soyad", width=160, anchor="w")
        self.tree.column("cinsiyet", width=80, anchor="center")
        self.tree.column("telefon", width=110, anchor="center")
        self.tree.column("kan_grubu", width=85, anchor="center")
        self.tree.column("poliklinik", width=170, anchor="w")
        self.tree.column("kayit_tarihi", width=120, anchor="center")

        # Scrollbarlar
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Tablo Çizgili Satır Efekti (Zebra striping)
        self.tree.tag_configure("oddrow", background="#f8fafc")
        self.tree.tag_configure("evenrow", background="#ffffff")

        # Eventler: Tek tıkla formu doldur, çift tıkla detay kartı aç
        self.tree.bind("<<TreeviewSelect>>", self.tablodan_secildi)
        self.tree.bind("<Double-1>", lambda event: self.detay_karti_ac())

        # ALT AKSİYON ÇUBUĞU VE DURUM
        bottom_bar = tk.Frame(right_container, bg="#f8fafc", height=45, padx=15, pady=8)
        bottom_bar.pack(side="bottom", fill="x")

        self.lbl_sayac = tk.Label(bottom_bar, text="Kayıtlar yükleniyor...", font=("Segoe UI", 9), fg="#475569", bg="#f8fafc")
        self.lbl_sayac.pack(side="left")

        # Alt Sağ Butonlar
        btn_sil = ttk.Button(bottom_bar, text="🗑️ Seçili Hastayı Sil", style="Danger.TButton", command=self.hasta_sil)
        btn_sil.pack(side="right", padx=(5, 0))

        btn_detay = ttk.Button(bottom_bar, text="🔍 Hasta Kartını Görüntüle", style="Primary.TButton", command=self.detay_karti_ac)
        btn_detay.pack(side="right", padx=(5, 0))

    def tabloyu_guncelle(self):
        """Veritabanındaki hastaları arama ve filtreye göre Treeview'a doldurur"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        arama_metni = self.ent_arama.get().strip()
        secili_poli = self.cmb_filtre_poli.get()

        hastalar = self.db.hastalari_listele(arama_metni=arama_metni, poliklinik=secili_poli)

        for idx, hasta in enumerate(hastalar):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            ad_soyad = f"{hasta['ad']} {hasta['soyad']}"
            self.tree.insert("", "end", iid=str(hasta["id"]), values=(
                hasta["id"],
                hasta["tc_no"],
                ad_soyad,
                hasta["cinsiyet"] or "-",
                hasta["telefon"] or "-",
                hasta["kan_grubu"] or "-",
                hasta["poliklinik"],
                hasta["kayit_tarihi"]
            ), tags=(tag,))

        # Durum sayacı güncelle
        toplam_ist = self.db.istatistikleri_getir()["toplam_hasta"]
        self.lbl_sayac.config(text=f"Listelenen: {len(hastalar)} hasta  |  Sistemdeki Toplam: {toplam_ist} hasta")

    def formu_temizle(self):
        """Formdaki tüm alanları temizler ve yeni kayıt moduna döner"""
        self.secili_hasta_id = None
        self.ent_tc.delete(0, tk.END)
        self.ent_ad.delete(0, tk.END)
        self.ent_soyad.delete(0, tk.END)
        self.cmb_cinsiyet.current(0)
        self.cmb_kan.current(0)
        self.ent_dt.delete(0, tk.END)
        self.ent_dt.insert(0, "1990-01-01")
        self.ent_tel.delete(0, tk.END)
        self.ent_tel.insert(0, "05")
        self.cmb_poliklinik.current(1)
        self.txt_sikayet.delete("1.0", tk.END)

        # Mod etiketini ve butonları sıfırla
        self.lbl_form_baslik.config(text="📋 Hasta Bilgileri Girişi")
        self.badge_duzenleme.pack_forget()
        self.btn_kaydet.config(state="normal")
        self.tree.selection_remove(self.tree.selection())

    def tablodan_secildi(self, event):
        """Tablodan bir hasta seçildiğinde verileri forma aktarır"""
        secilenler = self.tree.selection()
        if not secilenler:
            return

        hasta_id = int(secilenler[0])
        hasta = self.db.hasta_getir_by_id(hasta_id)
        if not hasta:
            return

        self.secili_hasta_id = hasta_id
        
        # Alanları doldur
        self.ent_tc.delete(0, tk.END)
        self.ent_tc.insert(0, hasta["tc_no"])

        self.ent_ad.delete(0, tk.END)
        self.ent_ad.insert(0, hasta["ad"])

        self.ent_soyad.delete(0, tk.END)
        self.ent_soyad.insert(0, hasta["soyad"])

        if hasta["cinsiyet"] in self.CINSIYETLER:
            self.cmb_cinsiyet.set(hasta["cinsiyet"])
        else:
            self.cmb_cinsiyet.current(0)

        if hasta["kan_grubu"] in self.KAN_GRUPLARI:
            self.cmb_kan.set(hasta["kan_grubu"])
        else:
            self.cmb_kan.current(0)

        self.ent_dt.delete(0, tk.END)
        self.ent_dt.insert(0, hasta["dogum_tarihi"] or "")

        self.ent_tel.delete(0, tk.END)
        self.ent_tel.insert(0, hasta["telefon"] or "")

        if hasta["poliklinik"] in self.POLIKLINIKLER:
            self.cmb_poliklinik.set(hasta["poliklinik"])

        self.txt_sikayet.delete("1.0", tk.END)
        if hasta["sikayet"]:
            self.txt_sikayet.insert("1.0", hasta["sikayet"])

        # Düzenleme modu bildirimini göster
        self.lbl_form_baslik.config(text=f"✏️ Hasta Düzenleme (ID: {hasta_id})")
        self.badge_duzenleme.pack(side="right", padx=10, pady=10)

    def _form_verilerini_dogrula(self):
        """Formdaki verilerin geçerliliğini denetler"""
        tc = self.ent_tc.get().strip()
        ad = self.ent_ad.get().strip()
        soyad = self.ent_soyad.get().strip()
        cinsiyet = self.cmb_cinsiyet.get()
        kan_grubu = self.cmb_kan.get()
        dogum_tarihi = self.ent_dt.get().strip()
        telefon = self.ent_tel.get().strip()
        poliklinik = self.cmb_poliklinik.get()
        sikayet = self.txt_sikayet.get("1.0", tk.END).strip()

        if not tc or not ad or not soyad or not poliklinik:
            messagebox.showwarning("Eksik Bilgi", "Lütfen T.C. Kimlik No, Ad, Soyad ve Poliklinik alanlarını doldurunuz!")
            return None

        if len(tc) != 11 or not tc.isdigit():
            messagebox.showwarning("Geçersiz T.C. No", "T.C. Kimlik Numarası 11 haneli rakamlardan oluşmalıdır!")
            return None

        if cinsiyet == "Seçiniz":
            cinsiyet = "Belirtilmemiş"
        if kan_grubu == "Seçiniz":
            kan_grubu = "Bilinmiyor"

        return {
            "tc": tc,
            "ad": ad,
            "soyad": soyad,
            "cinsiyet": cinsiyet,
            "kan_grubu": kan_grubu,
            "dogum_tarihi": dogum_tarihi,
            "telefon": telefon,
            "poliklinik": poliklinik,
            "sikayet": sikayet
        }

    def hasta_kaydet(self):
        """Yeni bir hastayı veritabanına kaydeder"""
        veri = self._form_verilerini_dogrula()
        if not veri:
            return

        if self.db.tc_var_mi(veri["tc"]):
            messagebox.showerror("Hata", f"{veri['tc']} T.C. Kimlik numaralı hasta sistemde zaten kayıtlı!")
            return

        try:
            self.db.hasta_ekle(
                tc_no=veri["tc"],
                ad=veri["ad"],
                soyad=veri["soyad"],
                cinsiyet=veri["cinsiyet"],
                dogum_tarihi=veri["dogum_tarihi"],
                telefon=veri["telefon"],
                kan_grubu=veri["kan_grubu"],
                poliklinik=veri["poliklinik"],
                sikayet=veri["sikayet"]
            )
            messagebox.showinfo("Başarılı", f"{veri['ad']} {veri['soyad']} adlı hasta başarıyla kaydedildi.")
            self.formu_temizle()
            self.tabloyu_guncelle()
        except Exception as e:
            messagebox.showerror("Kayıt Hatası", f"Hasta kaydedilirken hata oluştu:\n{e}")

    def hasta_guncelle(self):
        """Seçili hastanın bilgilerini günceller"""
        if not self.secili_hasta_id:
            messagebox.showwarning("Seçim Yapılmadı", "Lütfen önce tablodan güncellemek istediğiniz hastayı seçiniz.")
            return

        veri = self._form_verilerini_dogrula()
        if not veri:
            return

        if self.db.tc_var_mi(veri["tc"], haric_id=self.secili_hasta_id):
            messagebox.showerror("Hata", f"{veri['tc']} T.C. Kimlik numarası başka bir hastaya aittir!")
            return

        onay = messagebox.askyesno("Güncelleme Onayı", f"{veri['ad']} {veri['soyad']} adlı hastanın bilgilerini güncellemek istiyor musunuz?")
        if not onay:
            return

        try:
            self.db.hasta_guncelle(
                hasta_id=self.secili_hasta_id,
                tc_no=veri["tc"],
                ad=veri["ad"],
                soyad=veri["soyad"],
                cinsiyet=veri["cinsiyet"],
                dogum_tarihi=veri["dogum_tarihi"],
                telefon=veri["telefon"],
                kan_grubu=veri["kan_grubu"],
                poliklinik=veri["poliklinik"],
                sikayet=veri["sikayet"]
            )
            messagebox.showinfo("Başarılı", "Hasta bilgileri başarıyla güncellendi.")
            self.formu_temizle()
            self.tabloyu_guncelle()
        except Exception as e:
            messagebox.showerror("Güncelleme Hatası", f"Güncelleme yapılırken hata oluştu:\n{e}")

    def hasta_sil(self):
        """Seçili hastayı sistemden siler"""
        secilenler = self.tree.selection()
        if not secilenler:
            messagebox.showwarning("Seçim Yapılmadı", "Lütfen silmek istediğiniz hastayı tablodan seçiniz.")
            return

        hasta_id = int(secilenler[0])
        hasta = self.db.hasta_getir_by_id(hasta_id)
        if not hasta:
            return

        onay = messagebox.askyesno(
            "Silme Onayı",
            f"DİKKAT: {hasta['ad']} {hasta['soyad']} (TC: {hasta['tc_no']}) isimli hastayı ve tıbbi kaydını kalıcı olarak silmek istediğinizden emin misiniz?",
            icon="warning"
        )
        if not onay:
            return

        try:
            self.db.hasta_sil(hasta_id)
            messagebox.showinfo("Silindi", "Hasta kaydı başarıyla silindi.")
            self.formu_temizle()
            self.tabloyu_guncelle()
        except Exception as e:
            messagebox.showerror("Silme Hatası", f"Kayıt silinirken hata oluştu:\n{e}")

    def filtreyi_sifirla(self):
        """Arama kutusunu ve poliklinik filtresini sıfırlar"""
        self.ent_arama.delete(0, tk.END)
        self.cmb_filtre_poli.current(0)
        self.tabloyu_guncelle()

    def detay_karti_ac(self):
        """Seçili hastanın tüm detaylarını ve şikayet geçmişini gösteren pop-up pencere"""
        secilenler = self.tree.selection()
        if not secilenler:
            messagebox.showwarning("Seçim Yapılmadı", "Lütfen detayını görmek istediğiniz hastayı tablodan seçiniz.")
            return

        hasta_id = int(secilenler[0])
        hasta = self.db.hasta_getir_by_id(hasta_id)
        if not hasta:
            return

        modal = tk.Toplevel(self.root)
        modal.title(f"Hasta Dosyası - {hasta['ad']} {hasta['soyad']}")
        modal.geometry("550x520")
        modal.resizable(False, False)
        modal.configure(bg="#f8fafc")
        modal.grab_set()  # Modal odak

        # Kart Başlığı
        m_head = tk.Frame(modal, bg="#1e3a8a", padx=20, pady=15)
        m_head.pack(fill="x")
        tk.Label(m_head, text=f"🩺 {hasta['ad']} {hasta['soyad']}", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1e3a8a").pack(anchor="w")
        tk.Label(m_head, text=f"T.C. Kimlik: {hasta['tc_no']}  |  Kayıt Tarihi: {hasta['kayit_tarihi']}", font=("Segoe UI", 9), fg="#93c5fd", bg="#1e3a8a").pack(anchor="w", pady=(3, 0))

        # Kart İçeriği
        content_frame = tk.Frame(modal, bg="#f8fafc", padx=25, pady=15)
        content_frame.pack(fill="both", expand=True)

        bilgiler = [
            ("🏥 Başvurduğu Bölüm / Poliklinik:", hasta["poliklinik"]),
            ("🩸 Kan Grubu:", hasta["kan_grubu"] or "Bilinmiyor"),
            ("👤 Cinsiyet:", hasta["cinsiyet"] or "Belirtilmemiş"),
            ("📅 Doğum Tarihi / Yaş:", hasta["dogum_tarihi"] or "-"),
            ("📞 İletişim Telefonu:", hasta["telefon"] or "-"),
        ]

        for lbl, val in bilgiler:
            row = tk.Frame(content_frame, bg="#f8fafc")
            row.pack(fill="x", pady=4)
            tk.Label(row, text=lbl, font=("Segoe UI", 9, "bold"), fg="#475569", bg="#f8fafc", width=30, anchor="w").pack(side="left")
            tk.Label(row, text=str(val), font=("Segoe UI", 9), fg="#0f172a", bg="#f8fafc", anchor="w").pack(side="left", fill="x", expand=True)

        # Şikayet ve Klinik Açıklama Kutusu
        tk.Label(content_frame, text="📝 Hastanın Şikayeti ve Klinik Notları:", font=("Segoe UI", 9, "bold"), fg="#1e293b", bg="#f8fafc").pack(anchor="w", pady=(12, 4))
        
        txt_box = tk.Text(content_frame, height=7, font=("Segoe UI", 9), bg="#ffffff", fg="#1e293b", relief="solid", borderwidth=1, wrap="word", padx=8, pady=8)
        txt_box.pack(fill="both", expand=True)
        txt_box.insert("1.0", hasta["sikayet"] if hasta["sikayet"] else "Bu hasta için kayıtlı şikayet veya doktor notu bulunmamaktadır.")
        txt_box.config(state="disabled")

        # Kapat Butonu
        btn_kapat = ttk.Button(modal, text="Kapat", style="Secondary.TButton", command=modal.destroy)
        btn_kapat.pack(side="bottom", pady=12)

    def istatistik_penceresi_ac(self):
        """Poliklinik ve hasta kayıt istatistiklerini gösteren pencere"""
        ist = self.db.istatistikleri_getir()

        modal = tk.Toplevel(self.root)
        modal.title("Poliklinik ve Hasta İstatistikleri")
        modal.geometry("500x480")
        modal.resizable(False, False)
        modal.configure(bg="#f8fafc")
        modal.grab_set()

        head = tk.Frame(modal, bg="#0284c7", padx=20, pady=15)
        head.pack(fill="x")
        tk.Label(head, text="📊 Sistem İstatistik Özeti", font=("Segoe UI", 13, "bold"), fg="#ffffff", bg="#0284c7").pack(anchor="w")

        body = tk.Frame(modal, bg="#f8fafc", padx=20, pady=15)
        body.pack(fill="both", expand=True)

        # Toplam Kartı
        toplam_card = tk.Frame(body, bg="#e0f2fe", padx=15, pady=10, relief="flat", highlightbackground="#bae6fd", highlightthickness=1)
        toplam_card.pack(fill="x", pady=(0, 15))
        tk.Label(toplam_card, text=f"Toplam Kayıtlı Hasta Sayısı:  {ist['toplam_hasta']}", font=("Segoe UI", 12, "bold"), fg="#0369a1", bg="#e0f2fe").pack(side="left")

        # Poliklinik Dağılımı
        tk.Label(body, text="Bölümlere Göre Hasta Dağılımı:", font=("Segoe UI", 10, "bold"), fg="#1e293b", bg="#f8fafc").pack(anchor="w", pady=(0, 5))
        
        list_frame = tk.Frame(body, bg="#ffffff", relief="solid", borderwidth=1)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        v_scroll = ttk.Scrollbar(list_frame)
        v_scroll.pack(side="right", fill="y")

        lb = tk.Listbox(list_frame, font=("Segoe UI", 9), yscrollcommand=v_scroll.set, relief="flat", bg="#ffffff", selectmode="none")
        lb.pack(fill="both", expand=True, padx=5, pady=5)
        v_scroll.config(command=lb.yview)

        for poli, sayi in ist["poliklinik_dagilimi"]:
            yuzde = (sayi / ist["toplam_hasta"] * 100) if ist["toplam_hasta"] > 0 else 0
            lb.insert(tk.END, f"  • {poli:<35}: {sayi} hasta (%{yuzde:.1f})")

        ttk.Button(modal, text="Tamam", style="Primary.TButton", command=modal.destroy).pack(pady=(0, 12))

    def csv_aktar(self):
        """Kayıtlı hastaları UTF-8 BOM ile Excel uyumlu CSV olarak dışa aktarır"""
        hastalar = self.db.hastalari_listele(arama_metni=self.ent_arama.get().strip(), poliklinik=self.cmb_filtre_poli.get())
        if not hastalar:
            messagebox.showwarning("Kayıt Yok", "Dışa aktarılacak hasta kaydı bulunamadı.")
            return

        dosya_yolu = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Dosyası (Excel Uyumlu)", "*.csv"), ("Tüm Dosyalar", "*.*")],
            title="Hasta Listesini Kaydet",
            initialfile=f"Hasta_Listesi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        )
        if not dosya_yolu:
            return

        try:
            # utf-8-sig Türkçe karakterlerin Excel'de bozulmadan açılmasını sağlar
            with open(dosya_yolu, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=";")
                # Başlıklar
                writer.writerow(["ID", "TC Kimlik No", "Ad", "Soyad", "Cinsiyet", "Doğum Tarihi", "Telefon", "Kan Grubu", "Poliklinik", "Kayıt Tarihi", "Şikayet"])
                
                # Her hastanın tam detayını çekip yazalım
                for h in hastalar:
                    tam_hasta = self.db.hasta_getir_by_id(h["id"])
                    writer.writerow([
                        tam_hasta["id"],
                        tam_hasta["tc_no"],
                        tam_hasta["ad"],
                        tam_hasta["soyad"],
                        tam_hasta["cinsiyet"],
                        tam_hasta["dogum_tarihi"],
                        tam_hasta["telefon"],
                        tam_hasta["kan_grubu"],
                        tam_hasta["poliklinik"],
                        tam_hasta["kayit_tarihi"],
                        tam_hasta["sikayet"].replace("\n", " ") if tam_hasta["sikayet"] else ""
                    ])

            messagebox.showinfo("Başarılı", f"{len(hastalar)} adet hasta kaydı başarıyla aktarıldı:\n{os.path.basename(dosya_yolu)}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata oluştu:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HastaKayitUygulamasi(root)
    root.mainloop()


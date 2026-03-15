"""
run_seeder.py — Jalankan SQL seeder profesi tanpa psql
Cukup: python run_seeder.py

Requires: pip install psycopg2-binary
"""
import os, sys

DB_HOST = "103.171.84.248"
DB_PORT = 5433
DB_USER = "postgres"
DB_PASS = "password"
DB_NAME = "rextra"

# ── MAPPING DARI DB AKTUAL ────────────────────────────────────────────────────
# profession_main_categories
CAT = {
    "TECHNOLOGY": 1,
    "CREATIVE":   2,
    "BUSINESS":   3,
    "SOCIAL":     4,
    "SCIENCE":    5,
}
# profession_sub_categories
SUB = {
    "SOFTWARE_DEV":  1,
    "DATA_SCIENCE":  2,
    "DEVOPS":        3,
    "CYBERSECURITY": 4,
    "UI_UX":         5,
    "CONTENT":       6,
    "PRODUCT":       7,
    "MARKETING":     8,
    "EDUCATION":     9,
    "RESEARCH":      10,
}

# ── 50 PROFESI ────────────────────────────────────────────────────────────────
# Format: (slug, name, main_cat_key, sub_cat_key, riasec_code, about, riasec_desc)
PROFESSIONS = [
    # ── BATCH 01: Backend & Cloud ─────────────────────────────────────────────
    ("backend-engineer",              "Backend Engineer",
     "TECHNOLOGY", "SOFTWARE_DEV", "RI",
     "Backend Engineer membangun dan memelihara sistem sisi server — API, logika bisnis, database, dan integrasi layanan. Mereka adalah fondasi teknis yang memungkinkan produk digital berjalan cepat, aman, dan scalable.",
     "Tipe RI cocok: menggabungkan pekerjaan hands-on teknis (R) dengan analisis mendalam arsitektur sistem (I)."),

    ("cloud-infrastructure-engineer", "Cloud Infrastructure Engineer",
     "TECHNOLOGY", "DEVOPS", "R",
     "Cloud Infrastructure Engineer mengelola seluruh lapisan infrastruktur cloud — compute, storage, networking, dan security. Mereka memastikan sistem produksi reliabel, efisien biaya, dan siap scale.",
     "Tipe R cocok: sangat hands-on mengelola server dan sistem cloud meskipun secara virtual."),

    ("devops-platform-engineer",      "DevOps Platform Engineer",
     "TECHNOLOGY", "DEVOPS", "RC",
     "DevOps Platform Engineer membangun CI/CD pipeline, developer tooling, dan standar deployment agar setiap rilis ke produksi aman dan konsisten.",
     "Tipe RC cocok: implementasi teknis hands-on (R) dipadukan penerapan standar prosedur deployment yang ketat (C)."),

    ("backend-systems-architect",     "Backend Systems Architect",
     "TECHNOLOGY", "SOFTWARE_DEV", "IR",
     "Backend Systems Architect merancang arsitektur sistem backend yang kompleks — menentukan bagaimana service berkomunikasi, data mengalir, dan sistem tetap resilient di skala besar.",
     "Tipe IR cocok: investigasi mendalam trade-off teknis (I) sekaligus implementasi nyata arsitektur (R)."),

    ("site-reliability-engineer",     "Site Reliability Engineer",
     "TECHNOLOGY", "DEVOPS", "RI",
     "Site Reliability Engineer menggabungkan software engineering dengan operasi sistem untuk memastikan produk berjalan reliabel di skala besar. Mereka mendefinisikan SLO, error budget, dan membangun sistem self-healing.",
     "Tipe RI cocok: pekerjaan hands-on engineering (R) plus investigasi mendalam pola kegagalan sistem (I)."),

    ("web-backend-developer",         "Web Backend Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "RI",
     "Web Backend Developer membangun logika server-side untuk aplikasi web — dari autentikasi hingga integrasi payment gateway. Bekerja erat dengan frontend untuk memastikan API mudah dikonsumsi.",
     "Tipe RI cocok: implementasi teknis nyata (R) plus berpikir analitis alur data dan keamanan (I)."),

    ("mobile-android-developer",      "Mobile Android Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "R",
     "Mobile Android Developer membangun aplikasi native Android menggunakan Kotlin dan Jetpack Compose, memastikan aplikasi berjalan mulus di ratusan jenis perangkat.",
     "Tipe R cocok: sangat hands-on coding, debugging di device nyata, optimasi performa fisik."),

    ("mobile-ios-developer",          "Mobile iOS Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "R",
     "Mobile iOS Developer membangun aplikasi native iOS menggunakan Swift dan SwiftUI di ekosistem Apple dengan standar kualitas tinggi.",
     "Tipe R cocok: pengembangan iOS sangat teknis dan hands-on dari coding Swift hingga profiling di Xcode."),

    ("flutter-mobile-developer",      "Flutter Mobile Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "RI",
     "Flutter Mobile Developer membangun aplikasi cross-platform menggunakan Flutter dan Dart yang berjalan di Android, iOS, dan Web dari satu codebase.",
     "Tipe RI cocok: hands-on engineering Flutter (R) plus investigasi performa rendering dan state management (I)."),

    ("security-engineer",             "Security Engineer",
     "TECHNOLOGY", "CYBERSECURITY", "IR",
     "Security Engineer melindungi sistem dan data dari ancaman siber melalui penetration testing, security review kode, dan membangun tooling deteksi insiden.",
     "Tipe IR cocok: investigasi mendalam celah keamanan (I) plus implementasi teknis sistem pertahanan (R)."),

    # ── BATCH 02: Frontend & Data ─────────────────────────────────────────────
    ("frontend-engineer",             "Frontend Engineer",
     "TECHNOLOGY", "SOFTWARE_DEV", "RI",
     "Frontend Engineer membangun antarmuka aplikasi web yang performant, aksesibel, dan mudah digunakan. Mereka menerjemahkan mockup menjadi komponen interaktif yang berjalan mulus di semua browser.",
     "Tipe RI cocok: implementasi kode hands-on (R) plus analisis performa rendering dan optimasi (I)."),

    ("creative-frontend-developer",   "Creative Frontend Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "AR",
     "Creative Frontend Developer membangun pengalaman web yang memukau secara visual — animasi kompleks, micro-interaction halus, dan efek visual yang membuat produk terasa hidup.",
     "Tipe AR cocok: ekspresi kreatif dan sense estetika (A) dipadukan implementasi teknis kode yang presisi (R)."),

    ("data-engineer",                 "Data Engineer",
     "TECHNOLOGY", "DATA_SCIENCE", "IR",
     "Data Engineer membangun dan memelihara pipeline data yang mengalirkan data dari berbagai sumber ke data warehouse. Mereka adalah fondasi ekosistem data perusahaan.",
     "Tipe IR cocok: investigasi kualitas dan aliran data (I) plus implementasi pipeline hands-on (R)."),

    ("data-analytics-engineer",       "Data Analytics Engineer",
     "SCIENCE", "DATA_SCIENCE", "I",
     "Data Analytics Engineer membangun data model, dashboard, dan self-serve analytics agar tim bisnis bisa mengambil keputusan berbasis data secara mandiri.",
     "Tipe I cocok: peran ini tentang investigasi — menggali data, menemukan pola, mengubah angka jadi insight actionable."),

    ("machine-learning-engineer",     "Machine Learning Engineer",
     "SCIENCE", "DATA_SCIENCE", "I",
     "Machine Learning Engineer mengembangkan, melatih, dan men-deploy model ML ke produksi, menjembatani gap antara data scientist dan engineering team.",
     "Tipe I cocok: eksperimentasi ilmiah — merumuskan hipotesis, menguji model, menganalisis hasil, iterasi."),

    ("ai-llm-engineer",               "AI/LLM Engineer",
     "TECHNOLOGY", "DATA_SCIENCE", "IA",
     "AI/LLM Engineer membangun produk berbasis Large Language Model — dari RAG pipeline, fine-tuning, hingga AI agent yang menyelesaikan task kompleks secara otonom.",
     "Tipe IA cocok: investigasi mendalam cara kerja model (I) plus kreativitas merancang sistem output berkualitas (A)."),

    ("data-scientist",                "Data Scientist",
     "SCIENCE", "DATA_SCIENCE", "I",
     "Data Scientist menggunakan metode statistik dan ML untuk menjawab pertanyaan bisnis kompleks, membangun model prediktif, dan mengkomunikasikan temuan kepada stakeholder.",
     "Tipe I cocok: penelitian berbasis data — merumuskan hipotesis, eksperimen, menarik kesimpulan statistik valid."),

    ("database-reliability-engineer", "Database Reliability Engineer",
     "TECHNOLOGY", "DATA_SCIENCE", "CI",
     "Database Reliability Engineer memastikan database produksi berjalan dengan performa optimal, ketersediaan tinggi, dan disaster recovery yang solid dari gigabyte hingga petabyte.",
     "Tipe CI cocok: kepatuhan prosedur ketat (C) plus investigasi mendalam saat terjadi performance issue (I)."),

    ("software-qa-engineer",          "Software QA Engineer",
     "TECHNOLOGY", "SOFTWARE_DEV", "C",
     "Software QA Engineer memastikan produk digital bebas dari bug melalui strategi testing, automation test, dan menjadi gatekeeper kualitas di setiap siklus development.",
     "Tipe C cocok: pendekatan sistematis, terstruktur, dan berorientasi prosedur dalam memastikan kualitas."),

    ("full-stack-developer",          "Full Stack Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "RI",
     "Full Stack Developer menangani pengembangan dari backend hingga frontend — dari database hingga browser. Sangat efektif di startup yang butuh developer yang bisa bergerak cepat di semua lapisan.",
     "Tipe RI cocok: hands-on di dua sisi teknis (R) plus berpikir analitis integrasi backend-frontend (I)."),

    # ── BATCH 03: Design & Product ────────────────────────────────────────────
    ("product-uiux-designer",         "Product UI/UX Designer",
     "CREATIVE", "UI_UX", "A",
     "Product UI/UX Designer merancang antarmuka dan pengalaman pengguna digital yang intuitif, konsisten, dan menyenangkan melalui riset, wireframe, dan prototype.",
     "Tipe A cocok: pekerjaan kreatif yang membutuhkan sense estetika tajam dan ekspresi visual orisinal."),

    ("ux-researcher",                 "UX Researcher",
     "CREATIVE", "RESEARCH", "IA",
     "UX Researcher menggali pemahaman mendalam tentang pengguna — siapa mereka, apa yang dibutuhkan, dan bagaimana mereka berinteraksi dengan produk — untuk mendasari keputusan desain.",
     "Tipe IA cocok: investigasi ilmiah perilaku manusia (I) plus mengkomunikasikan temuan secara persuasif (A)."),

    ("visual-brand-designer",         "Visual & Brand Designer",
     "CREATIVE", "UI_UX", "A",
     "Visual & Brand Designer membangun identitas visual yang kuat dan konsisten — dari logo dan color palette hingga ilustrasi dan marketing assets.",
     "Tipe A cocok: peran kreatif murni yang bergantung ekspresi visual, sense estetika, dan bercerita melalui gambar."),

    ("digital-motion-designer",       "Digital Motion Designer",
     "CREATIVE", "CONTENT", "AI",
     "Digital Motion Designer menciptakan animasi, motion graphics, dan video pendek yang menghidupkan brand dan cerita melalui gerakan yang purposeful.",
     "Tipe AI cocok: ekspresi kreatif kuat (A) plus pemahaman teknis prinsip animasi dan timing (I)."),

    ("ux-writer-content-designer",    "UX Writer / Content Designer",
     "CREATIVE", "CONTENT", "AI",
     "UX Writer merancang teks dalam produk digital — button label, error message, onboarding flow — memastikan setiap kata membantu pengguna mencapai tujuannya.",
     "Tipe AI cocok: keahlian menulis empatik (A) plus investigasi perilaku pengguna dan konteks penggunaan (I)."),

    ("digital-product-manager",       "Digital Product Manager",
     "BUSINESS", "PRODUCT", "E",
     "Digital Product Manager mendefinisikan visi, strategi, dan roadmap produk digital, menjadi titik temu antara engineering, design, dan bisnis.",
     "Tipe E cocok: memimpin tanpa otoritas formal, mempengaruhi keputusan, mengadvokasi visi kepada stakeholder."),

    ("product-growth-manager",        "Product Growth Manager",
     "BUSINESS", "PRODUCT", "EC",
     "Product Growth Manager fokus pada satu hal: membuat produk tumbuh melalui eksperimen, optimasi funnel, dan growth loop yang membuat pengguna baru datang dan pengguna lama kembali.",
     "Tipe EC cocok: ambisi eksekusi (E) plus pendekatan sistematis dan data-driven (C)."),

    ("technical-product-manager",     "Technical Product Manager",
     "BUSINESS", "PRODUCT", "EI",
     "Technical Product Manager mengelola produk teknis — platform, API, developer tools — dengan pemahaman engineering yang dalam untuk keputusan yang mempertimbangkan kompleksitas implementasi.",
     "Tipe EI cocok: memimpin tim (E) plus menginvestigasi kedalaman teknis produk (I)."),

    ("edtech-learning-designer",      "EdTech Learning Designer",
     "SOCIAL", "EDUCATION", "SA",
     "EdTech Learning Designer merancang pengalaman belajar digital yang efektif dan engaging dengan menggabungkan prinsip pedagogi, instructional design, dan UX.",
     "Tipe SA cocok: kepedulian mendalam pengembangan orang lain (S) plus kreativitas merancang pengalaman belajar (A)."),

    ("product-operations-manager",    "Product Operations Manager",
     "BUSINESS", "PRODUCT", "CE",
     "Product Operations Manager memastikan mesin product development berjalan efisien — dari ritme sprint, tooling, dokumentasi, hingga proses pengambilan keputusan lintas tim.",
     "Tipe CE cocok: kecintaan sistem dan prosedur (C) plus proaktif menyelesaikan hambatan operasional (E)."),

    # ── BATCH 04: Marketing, DevRel, Business ─────────────────────────────────
    ("technical-developer-advocate",  "Technical Developer Advocate",
     "TECHNOLOGY", "SOFTWARE_DEV", "S",
     "Technical Developer Advocate menjadi jembatan antara perusahaan teknologi dengan komunitas developer melalui konten teknis, workshop, dan kehadiran aktif di komunitas.",
     "Tipe S cocok: membangun hubungan, membantu developer sukses, menciptakan komunitas di sekitar produk."),

    ("technical-documentation-engineer", "Technical Documentation Engineer",
     "TECHNOLOGY", "CONTENT", "CE",
     "Technical Documentation Engineer membuat dokumentasi API, tutorial, dan developer guide yang memungkinkan pengguna memahami produk secara mandiri.",
     "Tipe CE cocok: ketelitian dan struktur informasi (C) plus inisiatif mendokumentasikan pengetahuan tersebar (E)."),

    ("digital-marketing-manager",     "Digital Marketing Manager",
     "BUSINESS", "MARKETING", "ES",
     "Digital Marketing Manager merancang dan mengeksekusi strategi marketing digital multi-channel — SEO, content, paid ads, email — untuk mencapai target bisnis.",
     "Tipe ES cocok: ambisi growth (E) plus memahami psikologi dan perilaku audiens (S)."),

    ("seo-content-strategist",        "SEO & Content Strategist",
     "BUSINESS", "MARKETING", "IA",
     "SEO & Content Strategist membangun kehadiran organik produk digital melalui konten berkualitas tinggi yang menggabungkan analisis keyword dan kemampuan storytelling.",
     "Tipe IA cocok: investigasi data keyword (I) plus kreativitas menciptakan konten yang menarik (A)."),

    ("growth-marketing-analyst",      "Growth Marketing Analyst",
     "SCIENCE", "RESEARCH", "IC",
     "Growth Marketing Analyst menganalisis data marketing untuk menemukan peluang pertumbuhan, membangun attribution model, dan mengoptimalkan pengeluaran marketing.",
     "Tipe IC cocok: investigasi mendalam data (I) plus kecermatan membangun model yang akurat (C)."),

    ("technology-sales-engineer",     "Technology Sales Engineer",
     "BUSINESS", "PRODUCT", "EC",
     "Technology Sales Engineer menggabungkan keahlian teknis dengan kemampuan penjualan untuk memenangkan deal enterprise melalui demo, PoC, dan technical objection handling.",
     "Tipe EC cocok: drive komersial untuk closing (E) plus keteraturan teknis mendokumentasikan solusi (C)."),

    ("tech-startup-founder-cto",      "Tech Startup Founder / CTO",
     "BUSINESS", "PRODUCT", "ES",
     "Tech Startup Founder atau CTO memimpin visi teknis startup dari ideasi hingga scale, bertanggung jawab atas arsitektur, tim engineering, dan keputusan produk.",
     "Tipe ES cocok: jiwa entrepreneurial di tengah ketidakpastian (E) plus kemampuan membangun tim (S)."),

    ("business-development-manager-tech", "Business Development Manager (Tech)",
     "BUSINESS", "PRODUCT", "E",
     "Business Development Manager membangun kemitraan strategis yang mempercepat pertumbuhan, dari integrasi API partner hingga deal distribusi enterprise.",
     "Tipe E cocok: memimpin negosiasi, mengidentifikasi peluang, menggerakkan deal yang mengubah trajectory bisnis."),

    ("technical-project-manager",     "Technical Project Manager",
     "BUSINESS", "PRODUCT", "SE",
     "Technical Project Manager memastikan proyek teknologi selesai tepat waktu, sesuai scope, dan dalam budget dengan mengelola dependency dan menghilangkan blocker.",
     "Tipe SE cocok: membangun kepercayaan lintas tim (S) plus proaktif dan berorientasi hasil eksekusi (E)."),

    ("security-operations-analyst",   "Security Operations Analyst",
     "TECHNOLOGY", "CYBERSECURITY", "CR",
     "Security Operations Analyst memantau, mendeteksi, dan merespons ancaman keamanan secara real-time dari SOC sebagai garda depan pertahanan siber.",
     "Tipe CR cocok: prosedur sangat terstruktur (C) plus respons teknis nyata terhadap ancaman (R)."),

    # ── BATCH 05: Finance, People, Ops, Emerging ─────────────────────────────
    ("startup-finance-manager",       "Startup Finance Manager",
     "BUSINESS", "PRODUCT", "CE",
     "Startup Finance Manager mengelola kesehatan finansial startup — cash flow, financial modeling, fundraising prep — membantu founder membuat keputusan berbasis angka.",
     "Tipe CE cocok: ketelitian dan kepatuhan prosedur keuangan (C) plus inisiatif mendorong keputusan finansial optimal (E)."),

    ("people-culture-manager",        "People & Culture Manager",
     "SOCIAL", "EDUCATION", "SE",
     "People & Culture Manager memastikan perusahaan punya orang yang tepat di posisi tepat dengan budaya kerja yang mendukung pertumbuhan dan kontribusi maksimal.",
     "Tipe SE cocok: empati dan orientasi pengembangan manusia (S) plus inisiatif membangun sistem organisasi (E)."),

    ("tech-talent-recruiter",         "Tech Talent Recruiter",
     "SOCIAL", "EDUCATION", "ES",
     "Tech Talent Recruiter spesialisasi mencari dan menarik engineer dan profesional teknologi terbaik dengan memahami technical stack dan ekosistem developer.",
     "Tipe ES cocok: drive memenuhi hiring target (E) plus membangun hubungan dengan kandidat (S)."),

    ("customer-success-manager-tech", "Customer Success Manager (Tech)",
     "BUSINESS", "PRODUCT", "SE",
     "Customer Success Manager memastikan pelanggan mendapatkan value maksimal dari produk melalui onboarding, adoption, dan renewal management.",
     "Tipe SE cocok: empatis membantu pelanggan sukses (S) plus proaktif mengidentifikasi peluang ekspansi (E)."),

    ("digital-operations-manager",    "Digital Operations Manager",
     "BUSINESS", "PRODUCT", "EC",
     "Digital Operations Manager memastikan mesin operasional perusahaan digital berjalan efisien melalui optimasi proses, tooling, dan otomasi.",
     "Tipe EC cocok: drive mengoptimalkan operasi (E) plus kecermatan membangun sistem dan prosedur (C)."),

    ("game-developer",                "Game Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "RI",
     "Game Developer membangun pengalaman interaktif menggunakan Unity atau Unreal, menggabungkan programming, fisika, dan desain untuk menciptakan dunia digital yang menarik.",
     "Tipe RI cocok: implementasi teknis hands-on (R) plus investigasi game mechanics dan physics simulation (I)."),

    ("web3-blockchain-developer",     "Web3 / Blockchain Developer",
     "TECHNOLOGY", "SOFTWARE_DEV", "IR",
     "Web3 / Blockchain Developer membangun smart contract dan dApp di atas blockchain, berada di frontier teknologi yang mendefinisikan ulang kepemilikan digital.",
     "Tipe IR cocok: investigasi kriptografi dan konsensus mekanisme (I) plus implementasi teknis smart contract (R)."),

    ("iot-embedded-systems-engineer", "IoT / Embedded Systems Engineer",
     "TECHNOLOGY", "SOFTWARE_DEV", "R",
     "IoT / Embedded Systems Engineer mengembangkan firmware untuk perangkat fisik yang terhubung internet, bekerja di boundary antara hardware dan software.",
     "Tipe R cocok: bekerja langsung dengan hardware fisik, testing di perangkat nyata, optimasi resource terbatas."),

    ("network-engineer",              "Network Engineer",
     "TECHNOLOGY", "DEVOPS", "RC",
     "Network Engineer merancang dan memelihara infrastruktur jaringan — dari jaringan kantor dan data center hingga SD-WAN dan cloud networking.",
     "Tipe RC cocok: konfigurasi jaringan hands-on (R) plus penerapan standar dan prosedur jaringan ketat (C)."),

    ("product-data-analyst",          "Product Data Analyst",
     "SCIENCE", "DATA_SCIENCE", "IC",
     "Product Data Analyst menganalisis perilaku pengguna di produk digital untuk membantu tim produk membuat keputusan berbasis data yang lebih baik.",
     "Tipe IC cocok: investigasi mendalam data pengguna (I) plus kecermatan membangun analisis yang akurat (C)."),
]

def main():
    try:
        import psycopg2
    except ImportError:
        print("[ERROR] pip install psycopg2-binary")
        sys.exit(1)

    print("=" * 60)
    print(f"  KENALI DIRI — Seeder 50 Profesi Digital")
    print(f"  Host: {DB_HOST}:{DB_PORT}  DB: {DB_NAME}")
    print("=" * 60)

    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
    conn.autocommit = False
    cur = conn.cursor()
    print("[OK] Koneksi berhasil.\n")

    inserted = 0
    skipped  = 0

    for prof in PROFESSIONS:
        slug, name, main_key, sub_key, riasec_code, about, riasec_desc = prof
        main_id = CAT[main_key]
        sub_id  = SUB[sub_key]

        # Resolve riasec_code_id
        cur.execute("SELECT id FROM riasec_codes WHERE riasec_code = %s", (riasec_code,))
        row = cur.fetchone()
        if not row:
            print(f"[WARN] riasec_code '{riasec_code}' tidak ditemukan, skip: {slug}")
            skipped += 1
            continue
        riasec_id = row[0]

        cur.execute("""
            INSERT INTO professions
              (slug, name, main_category_id, sub_category_id, riasec_code_id,
               about_description, riasec_description, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (slug) DO NOTHING
        """, (slug, name, main_id, sub_id, riasec_id, about, riasec_desc))

        if cur.rowcount > 0:
            inserted += 1
            print(f"  [INSERT] {name}")
        else:
            skipped += 1
            print(f"  [SKIP]   {name} (sudah ada)")

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n{'='*60}")
    print(f"  Selesai! Insert: {inserted}  Skip: {skipped}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
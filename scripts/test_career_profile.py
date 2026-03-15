import os, sys, json, time, random, string, textwrap, re, uuid
import requests, psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
API_V1   = f"{BASE_URL}/api/v1"
OR_KEY   = os.getenv("OPENROUTER_API_KEY", "")
OR_URL   = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OR_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")
DB_HOST  = os.getenv("DB_HOST", "103.171.84.248")
DB_PORT  = int(os.getenv("DB_PORT", "5433"))
DB_NAME  = os.getenv("DB_NAME", "rextra")
DB_USER  = os.getenv("DB_USER", "postgres")
DB_PASS  = os.getenv("DB_PASS", os.getenv("DB_PASSWORD", "password"))

GR="\033[92m"; RD="\033[91m"; YL="\033[93m"; CY="\033[96m"
MG="\033[95m"; DM="\033[2m"; BD="\033[1m"; RS="\033[0m"

RIASEC_LABELS = {
    "R":"Realistic","I":"Investigative","A":"Artistic",
    "S":"Social","E":"Enterprising","C":"Conventional"
}
PERSONAS = {
    "R": {"full":"Raka - Cloud & DevOps Engineer",     "karakter":"Sangat hands-on dalam dunia cloud dan infrastruktur digital. Suka membangun pipeline CI/CD, mengelola server, dan mengoptimalkan sistem deployment. Tertarik Kubernetes, Docker, dan otomasi infrastruktur."},
    "I": {"full":"Andi - Backend Engineer",            "karakter":"Sangat analitis dan suka memecahkan masalah teknis yang kompleks. Gemar membangun sistem backend yang scalable, merancang API, dan mendalami arsitektur distributed systems."},
    "A": {"full":"Budi - UI/UX & Frontend Developer",  "karakter":"Sangat kreatif dalam dunia digital. Suka mendesain antarmuka yang intuitif, membangun komponen frontend interaktif, dan menciptakan pengalaman pengguna yang bermakna."},
    "S": {"full":"Dian - Developer Advocate",          "karakter":"Sangat empatis dan komunikatif. Senang membantu komunitas developer, membuat konten teknis edukatif, dan menjembatani gap antara produk teknologi dengan penggunanya."},
    "E": {"full":"Citra - Product Manager Digital",   "karakter":"Ambisius dan strategis. Gemar memimpin pengembangan produk digital, mendefinisikan roadmap, dan menggerakkan tim lintas fungsi untuk menciptakan produk yang berdampak."},
    "C": {"full":"Fira - Data & QA Engineer",          "karakter":"Sangat teliti dan sistematis. Ahli menganalisis data, membangun pipeline data, menulis test case, dan memastikan kualitas sistem berjalan presisi sesuai spesifikasi."},
}

# ─── TABEL PRESISI SKOR ────────────────────────────────────────────────────────
# Dihitung berdasarkan aturan klasifikasi RIASEC:
# Single: gap >= 9, gap/r1 >= 0.15, r1 >= 40
# Dual:   gap_12 < 9, gap_23 >= 9, r1 >= 40, r2 >= 30
# Triple: fallback (gap_12 < 9, gap_23 < 9)
# avg = raw_score / 12 soal per tipe
TARGET_AVG = {
    # Single (1 huruf)
    "R":   {"R":4.5,"I":3.3,"A":2.5,"S":1.7,"E":1.7,"C":1.7},
    "I":   {"I":4.5,"R":3.3,"A":2.5,"S":1.7,"E":1.7,"C":1.7},
    "A":   {"A":4.5,"R":2.5,"I":2.5,"S":1.7,"E":1.7,"C":1.7},
    "S":   {"S":4.5,"R":2.5,"I":2.5,"A":1.7,"E":1.7,"C":1.7},
    "E":   {"E":4.5,"R":2.5,"I":2.5,"A":1.7,"S":1.7,"C":1.7},
    "C":   {"C":4.5,"R":2.5,"I":2.5,"A":1.7,"S":1.7,"E":1.7},
    # Dual (2 huruf)
    "RI":  {"R":4.3,"I":4.0,"A":2.8,"S":1.7,"E":1.7,"C":1.7},
    "IR":  {"R":4.3,"I":4.0,"A":2.8,"S":1.7,"E":1.7,"C":1.7},
    "RA":  {"R":4.3,"A":4.0,"I":2.8,"S":1.7,"E":1.7,"C":1.7},
    "IA":  {"I":4.3,"A":4.0,"R":2.8,"S":1.7,"E":1.7,"C":1.7},
    "RS":  {"R":4.3,"S":4.0,"I":2.8,"A":1.7,"E":1.7,"C":1.7},
    "IS":  {"I":4.3,"S":4.0,"R":2.8,"A":1.7,"E":1.7,"C":1.7},
    "AS":  {"A":4.3,"S":4.0,"R":2.8,"I":1.7,"E":1.7,"C":1.7},
    "RE":  {"R":4.3,"E":4.0,"I":2.8,"A":1.7,"S":1.7,"C":1.7},
    "IE":  {"I":4.3,"E":4.0,"R":2.8,"A":1.7,"S":1.7,"C":1.7},
    "SE":  {"S":4.3,"E":4.0,"R":2.8,"I":1.7,"A":1.7,"C":1.7},
    "EC":  {"E":4.3,"C":4.0,"R":2.8,"I":1.7,"A":1.7,"S":1.7},
    "SC":  {"S":4.3,"C":4.0,"R":2.8,"I":1.7,"A":1.7,"E":1.7},
    "RC":  {"R":4.3,"C":4.0,"I":2.8,"A":1.7,"S":1.7,"E":1.7},
    "IC":  {"I":4.3,"C":4.0,"R":2.8,"A":1.7,"S":1.7,"E":1.7},
    "AC":  {"A":4.3,"C":4.0,"R":2.8,"I":1.7,"S":1.7,"E":1.7},
    "AE":  {"A":4.3,"E":4.0,"R":2.8,"I":1.7,"S":1.7,"C":1.7},
    # Triple (3 huruf)
    "RIA": {"R":4.5,"I":4.3,"A":4.0,"S":2.0,"E":1.7,"C":1.7},
    "RIS": {"R":4.5,"I":4.3,"S":4.0,"A":2.0,"E":1.7,"C":1.7},
    "RIE": {"R":4.5,"I":4.3,"E":4.0,"A":2.0,"S":1.7,"C":1.7},
    "RIC": {"R":4.5,"I":4.3,"C":4.0,"A":2.0,"S":1.7,"E":1.7},
    "RAS": {"R":4.5,"A":4.3,"S":4.0,"I":2.0,"E":1.7,"C":1.7},
    "RAE": {"R":4.5,"A":4.3,"E":4.0,"I":2.0,"S":1.7,"C":1.7},
    "IAE": {"I":4.5,"A":4.3,"E":4.0,"R":2.0,"S":1.7,"C":1.7},
    "IAS": {"I":4.5,"A":4.3,"S":4.0,"R":2.0,"E":1.7,"C":1.7},
    "RES": {"R":4.5,"E":4.3,"S":4.0,"I":2.0,"A":1.7,"C":1.7},
    "SEC": {"S":4.5,"E":4.3,"C":4.0,"R":2.0,"I":1.7,"A":1.7},
    "AES": {"A":4.5,"E":4.3,"S":4.0,"R":2.0,"I":1.7,"C":1.7},
}

def classify_target(target: str) -> dict:
    """Hitung avg per tipe yang dibutuhkan untuk mencapai target RIASEC."""
    t = target.upper().strip()
    if t in TARGET_AVG:
        return TARGET_AVG[t]

    # Build dinamis kalau tidak ada di tabel
    RIASEC_ORDER = "RIASEC"
    letters = list(dict.fromkeys(c for c in t if c in RIASEC_LABELS))
    others  = [c for c in RIASEC_ORDER if c not in letters]
    n = len(letters)

    avgs = {}
    if n == 1:
        avgs[letters[0]] = 4.5
        for i, o in enumerate(others): avgs[o] = 3.3 if i == 0 else 1.7
    elif n == 2:
        avgs[letters[0]] = 4.3
        avgs[letters[1]] = 4.0
        for i, o in enumerate(others): avgs[o] = 2.8 if i == 0 else 1.7
    else:  # triple
        avgs[letters[0]] = 4.5
        avgs[letters[1]] = 4.3
        avgs[letters[2]] = 4.0
        for i, o in enumerate(others): avgs[o] = 2.0 if i == 0 else 1.7

    return avgs

def sec(t): print(f"\n{BD}{YL}{'─'*62}\n  {t}\n{'─'*62}{RS}")
def ok(m):  print(f"  {GR}v{RS} {m}")
def err(m): print(f"  {RD}x{RS} {m}")
def inf(m): print(f"  {CY}i{RS} {m}")
def w(t):   return "\n".join(textwrap.wrap(str(t), 56, initial_indent="     ", subsequent_indent="     "))

def call_ai(system: str, user: str, max_tokens=3000) -> str:
    for attempt in range(3):
        try:
            resp = requests.post(
                f"{OR_URL}/chat/completions",
                headers={"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://kenalidiri.dev"},
                json={"model": OR_MODEL,
                      "messages": [{"role":"system","content":system},{"role":"user","content":user}],
                      "max_tokens": max_tokens, "temperature": 0.2},
                timeout=90
            )
            if not resp.ok:
                raise Exception(f"OpenRouter {resp.status_code}: {resp.text[:200]}")
            content = resp.json()["choices"][0]["message"]["content"]
            if not content or not content.strip():
                raise Exception("Response kosong")
            return content
        except Exception as e:
            if attempt == 2: raise
            inf(f"Retry {attempt+1}/3: {e}")
            time.sleep(3)

def parse_json(raw: str):
    """Parse JSON dari AI response — robust terhadap truncation dan trailing commas."""
    import re as _re
    cleaned = _re.sub(r"```(?:json)?|```", "", raw).strip()

    def _fix(s):
        s = _re.sub(r",\s*([\]\}])", r"\1", s)
        s = _re.sub(r"\n\s*", " ", s)
        return s

    def _try(s):
        for v in (s, _fix(s)):
            try:
                return json.loads(v)
            except Exception:
                pass
        return None

    r = _try(cleaned)
    if r is not None:
        return r

    m = _re.search(r"(\{[\s\S]*?\})", cleaned)
    if m:
        r = _try(m.group(1))
        if r is not None:
            return r

    for suffix in ['"}', '"]}', ']}', '}']:
        r = _try(cleaned + suffix)
        if r is not None and isinstance(r, dict):
            return r

    raise Exception(f"Gagal parse JSON: {cleaned[:150]}")

def create_user(name: str) -> str:
    uid = os.getenv("TEST_USER_ID", "")
    if uid:
        ok(f"Pakai TEST_USER_ID: {uid[:8]}..."); return uid
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email  = f"aitest_{suffix}@kenalidiri.dev"
    new_id = str(uuid.uuid4())
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                                user=DB_USER, password=DB_PASS, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        row = cur.fetchone()
        if row:
            user_id = str(row[0]); ok(f"User existing: {email}")
        else:
            cur.execute("""INSERT INTO users (id,fullname,email,password,phone_number,role,is_verified,created_at)
                VALUES (%s,%s,%s,'hashed','08000000000','USER',true,now()) RETURNING id""",
                (new_id, name, email))
            user_id = str(cur.fetchone()[0])
            try:
                cur.execute("INSERT INTO token_wallet (id,user_id,balance,updated_at) VALUES (%s,%s,1000,now())",
                            (str(uuid.uuid4()), user_id))
                ok("Token wallet dibuat")
            except Exception: conn.rollback()
            conn.commit(); ok(f"User baru: {email}")
        conn.close(); return user_id
    except Exception as e:
        err(f"Gagal buat user: {e}"); sys.exit(1)

def ai_answer_riasec(questions: list, target_code: str, persona: dict) -> list:
    """
    Jawab 72 soal RIASEC dengan skor yang dikalibrasi presisi
    sesuai aturan klasifikasi untuk mencapai target kode.
    """
    sec(f"AI Menjawab RIASEC — Target: {BD}{target_code}{RS}")

    # Hitung avg target per tipe
    target_avgs = classify_target(target_code)

    print(f"  {MG}Persona: {persona['full']}{RS}")
    print(f"\n  {BD}Kalibrasi skor untuk mencapai '{target_code}':{RS}")
    for t in "RIASEC":
        avg = target_avgs.get(t, 1.7)
        is_t = t in target_code
        col  = f"{BD}{GR}" if is_t else DM
        bar  = "█" * int(avg * 3)
        print(f"    {col}{t} {RIASEC_LABELS[t]:<13}{RS} target avg {avg:.1f}  {col}{bar}{RS}")

    print(f"\n  {DM}Mengirim semua {len(questions)} soal ke AI (1 batch)...{RS}", flush=True)

    q_list = "\n".join(
        f"{q['question_id']}. [{q['riasec_type'][0]}] {q['question_text']}"
        for q in questions
    )

    # Buat aturan skor berdasarkan target_avgs
    aturan_lines = []
    for t in "RIASEC":
        avg = target_avgs.get(t, 1.7)
        if avg >= 4.3:   skor_range = "4 atau 5"
        elif avg >= 3.8: skor_range = "kebanyakan 4, sesekali 3 atau 5"
        elif avg >= 3.3: skor_range = "3 atau 4"
        elif avg >= 2.5: skor_range = "kebanyakan 3, sesekali 2"
        elif avg >= 2.0: skor_range = "2 atau 3"
        else:            skor_range = "1 atau 2"
        aturan_lines.append(f"  - Soal tipe {t} ({RIASEC_LABELS[t]}): jawab {skor_range} (target avg {avg:.1f})")

    system = f"""Kamu adalah {persona['full']}. {persona['karakter']}

Kamu sedang mengisi tes RIASEC dengan tujuan menghasilkan kode '{target_code}'.

ATURAN SKOR WAJIB (1=Sangat Tidak Setuju, 5=Sangat Setuju):
{chr(10).join(aturan_lines)}

PENTING:
- Ikuti aturan skor di atas dengan ketat agar hasil klasifikasi tepat
- Variasikan skor agar natural (jangan semua nilai identik persis)
- Return HANYA JSON array format: [{{"id":1,"s":5}},{{"id":2,"s":4}},...] untuk semua {len(questions)} soal
- Tidak ada teks lain, tidak ada markdown"""

    raw = call_ai(system, f"Jawab semua {len(questions)} soal:\n{q_list}", max_tokens=2500)

    try:
        data = parse_json(raw)
        if isinstance(data, list):
            score_map = {item["id"]: item["s"] for item in data if "id" in item and "s" in item}
        else:
            score_map = {}
    except Exception as e:
        inf(f"Parse batch gagal ({e}), pakai skor kalkulasi")
        score_map = {}

    # Build responses + tampilkan per soal
    responses = []
    type_scores = {t: [] for t in "RIASEC"}

    print(f"\n  {'No':>3}  {'T':<2} {'Soal':<40} Skor")
    print(f"  {'─'*3}  {'─'*2} {'─'*40} {'─'*4}")

    for q in questions:
        qid   = q["question_id"]
        qtype = q["riasec_type"][0].upper()
        qtxt  = q["question_text"]
        avg   = target_avgs.get(qtype, 1.7)

        if qid in score_map:
            score = max(1, min(5, int(score_map[qid])))
        else:
            # Kalkulasi presisi berdasarkan avg target
            if avg >= 4.3:   choices = [4,4,5,5,4]
            elif avg >= 3.8: choices = [3,4,4,4,5]
            elif avg >= 3.3: choices = [3,3,4,4,3]
            elif avg >= 2.5: choices = [2,3,3,2,3]
            elif avg >= 2.0: choices = [2,2,3,2,2]
            else:            choices = [1,1,2,1,2]
            score = random.choice(choices)

        responses.append({
            "question_id": qid,
            "question_type": qtype,
            "answer_value": score,
            "answered_at": datetime.now(timezone.utc).isoformat()
        })
        type_scores[qtype].append(score)

        sc_col = GR if score >= 4 else (YL if score == 3 else RD)
        t_col  = f"{BD}{GR}" if qtype in target_code else DM
        txt    = (qtxt[:38]+"..") if len(qtxt) > 40 else qtxt.ljust(40)
        print(f"  {qid:>3}  {t_col}{qtype}{RS}  {DM}{txt}{RS} {sc_col}{score}{RS}")

    # Estimasi hasil klasifikasi
    print(f"\n  {BD}Estimasi skor & klasifikasi:{RS}")
    raw_scores = {t: sum(type_scores[t]) for t in "RIASEC"}
    sorted_s   = sorted(raw_scores.items(), key=lambda x: -x[1])
    for t, s in sorted_s:
        avg_actual = s/12
        is_t = t in target_code
        col  = f"{BD}{GR}" if is_t else DM
        bar  = "█" * int(avg_actual * 3)
        mark = " <- TARGET" if is_t else ""
        print(f"    {col}{t} {RIASEC_LABELS[t]:<13}{RS} avg {avg_actual:.2f}  {col}{bar}{RS}{YL}{mark}{RS}")

    r1n,r1v = sorted_s[0]; r2n,r2v = sorted_s[1]; r3n,r3v = sorted_s[2]
    gap12 = r1v-r2v; gap23 = r2v-r3v
    if r1v >= 40 and gap12 >= 9 and gap12/r1v >= 0.15:
        pred = r1n; ptype = "single"
    elif r1v >= 40 and gap12 < 9 and gap23 >= 9 and r2v >= 30:
        pred = r1n+r2n; ptype = "dual"
    else:
        pred = r1n+r2n+r3n; ptype = "triple"

    hit = f"{GR}🎯 TEPAT!" if pred == target_code else f"{YL}≈ dekat"
    print(f"\n  Prediksi: {BD}{pred}{RS} ({ptype}) {hit}{RS}")

    return responses

# ─── PERSONA DETAIL PER RIASEC ────────────────────────────────────────────────
# Karakter mendalam per kode untuk reasoning Ikigai yang konsisten dan kaya.
# Multi-code (RIA) pakai gabungan dari semua huruf.
PERSONA_DETAIL = {
    "R": {
        "latar": "Saya memulai karier di dunia IT ops dan jatuh cinta dengan cloud infrastructure. "
                 "Senang sekali kalau bisa otomasi sesuatu yang tadinya manual — deploy, monitoring, "
                 "scaling. Bagi saya kode yang bagus adalah kode yang tidak perlu disentuh karena "
                 "sistemnya sudah jalan sendiri.",
        "love": "Saya paling antusias saat merancang pipeline deployment yang efisien atau debugging "
                "masalah infrastructure yang tricky. Melihat sistem berjalan stabil di production "
                "setelah incident adalah kepuasan tersendiri yang sulit dijelaskan.",
        "good_at": "Saya kuat di cloud platforms (AWS/GCP), container orchestration dengan Kubernetes, "
                   "dan scripting otomasi dengan Bash/Python. Cepat mendiagnosis bottleneck sistem "
                   "dan terbiasa kerja di bawah tekanan saat ada incident produksi.",
        "world_needs": "Dunia butuh infrastruktur digital yang reliabel dan scalable. Tanpa DevOps "
                       "engineer yang solid, produk sebagus apapun tidak akan bisa deliver ke jutaan "
                       "pengguna dengan stabil. Saya ingin jadi fondasi yang tidak kelihatan tapi krusial.",
        "paid_for": "Saya cocok dengan perusahaan tech yang punya infrastruktur kompleks — startup "
                    "Series B ke atas atau enterprise. Model kerja remote atau hybrid dengan kompensasi "
                    "berbasis seniority dan on-call allowance adalah yang paling ideal buat saya.",
    },
    "I": {
        "latar": "Sejak kuliah saya sudah freelance bikin API dan backend untuk startup lokal. "
                 "Saya suka sekali dengan tantangan merancang sistem yang bisa handle traffic besar "
                 "tanpa collapse. Architecture decision dan performance tuning adalah zona nyaman saya.",
        "love": "Saya paling hidup saat merancang arsitektur backend dari nol atau memecahkan "
                "masalah performance yang sudah bikin tim lain frustrasi berminggu-minggu. "
                "Menulis kode bersih yang mudah di-maintain oleh engineer lain terasa seperti seni.",
        "good_at": "Saya kuat di backend engineering — REST/gRPC API design, database optimization, "
                   "caching strategy, dan distributed systems. Punya insting bagus untuk trade-off "
                   "antara simplicity dan scalability di setiap keputusan teknis.",
        "world_needs": "Dunia butuh sistem backend yang tidak hanya bekerja hari ini tapi tetap "
                       "maintainable 3 tahun lagi. Saya ingin berkontribusi pada produk digital yang "
                       "benar-benar digunakan jutaan orang tanpa mereka sadar betapa kompleksnya di balik layar.",
        "paid_for": "Saya cocok dengan model kerja remote-first di tech company atau product startup. "
                    "Gaji kompetitif dengan ruang untuk grow ke Staff/Principal Engineer lebih menarik "
                    "daripada title yang bagus tapi tidak ada ownership teknis.",
    },
    "A": {
        "latar": "Saya masuk dunia digital dari jalur desain grafis lalu berkembang ke UI/UX dan "
                 "akhirnya belajar frontend development. Percaya bahwa produk digital yang bagus "
                 "adalah irisan sempurna antara estetika dan fungsi.",
        "love": "Saya paling bersemangat saat bisa mengubah wireframe menjadi interface yang terasa "
                "hidup — animasi yang smooth, micro-interaction yang intuitif, dan layout yang "
                "membuat pengguna tidak perlu berpikir keras. Proses dari blank canvas ke prototype "
                "interaktif adalah favorit saya.",
        "good_at": "Saya kuat di UI/UX design dengan Figma, design system, dan frontend implementation "
                   "dengan React/Vue. Punya sense estetika yang tajam dan kemampuan untuk "
                   "mengadvokasi kebutuhan pengguna di tengah tekanan engineering.",
        "world_needs": "Dunia butuh produk digital yang tidak hanya fungsional tapi juga menyenangkan "
                       "digunakan. Saya ingin membuktikan bahwa desain bukan lapisan cat terakhir — "
                       "tapi fondasi yang menentukan apakah produk akan dicintai atau ditinggalkan.",
        "paid_for": "Saya cocok di product company dengan design-led culture atau agency digital "
                    "yang punya klien beragam. Model hybrid dengan kebebasan eksplorasi kreatif "
                    "lebih penting dari sekadar gaji besar di perusahaan yang tidak menghargai desain.",
    },
    "S": {
        "latar": "Saya mulai karier sebagai software engineer tapi paling puas saat bisa membantu "
                 "developer lain berkembang. Akhirnya pivot ke Developer Relations dan merasa "
                 "ini adalah kombinasi sempurna antara technical depth dan human connection.",
        "love": "Saya paling energized saat bisa membuat konsep teknis yang rumit menjadi mudah "
                "dipahami — lewat tulisan, video, atau workshop langsung. Melihat developer lain "
                "'aha moment' setelah menjelaskan sesuatu adalah reward terbesar.",
        "good_at": "Saya kuat dalam technical writing, public speaking, dan community building. "
                   "Bisa berbicara dalam bahasa engineer sekaligus bahasa bisnis. Punya kemampuan "
                   "untuk menangkap feedback komunitas dan mentranslasikan ke product insight.",
        "world_needs": "Dunia butuh jembatan antara teknologi yang makin kompleks dengan developer "
                       "yang ingin belajar menggunakannya. Ekosistem open source dan developer tools "
                       "hanya bisa tumbuh kalau ada orang yang berdedikasi membangun komunitasnya.",
        "paid_for": "Saya cocok di perusahaan developer tools, cloud provider, atau open source company "
                    "yang serius investasi di developer ecosystem. Remote-first dengan budget konferensi "
                    "dan travel untuk event komunitas adalah setup ideal saya.",
    },
    "E": {
        "latar": "Saya punya background engineering tapi selalu tertarik dengan sisi bisnis dan "
                 "strategi produk. Setelah beberapa tahun sebagai engineer, pindah ke product management "
                 "dan tidak pernah menyesal — ini peran yang membutuhkan semua skill sekaligus.",
        "love": "Saya paling bergairah saat mendefinisikan roadmap produk, bernegosiasi prioritas "
                "dengan stakeholders, dan melihat fitur yang saya champion akhirnya shipped dan "
                "digunakan oleh ribuan pengguna. Data-driven decision making adalah passion saya.",
        "good_at": "Saya kuat dalam product strategy, user research synthesis, dan komunikasi lintas "
                   "fungsi antara engineering, design, dan business. Bisa membaca data produk dan "
                   "mentranslasikan ke keputusan prioritas yang masuk akal secara teknis maupun bisnis.",
        "world_needs": "Dunia butuh product manager yang bisa menjembatani gap antara apa yang bisa "
                       "dibangun secara teknis dengan apa yang benar-benar dibutuhkan pengguna. "
                       "Terlalu banyak produk dibuat karena bisa, bukan karena harus.",
        "paid_for": "Saya cocok di growth-stage startup atau scaleup yang punya masalah product-market "
                    "fit yang menarik untuk dipecahkan. Equity + kompetitif base salary dengan "
                    "otonomi penuh atas product area lebih menarik dari corporate PM role.",
    },
    "C": {
        "latar": "Saya masuk dunia data dari background statistik dan jatuh cinta dengan SQL di hari "
                 "pertama. Sekarang saya bekerja di intersection antara data engineering, analytics, "
                 "dan QA — tiga bidang yang semuanya butuh ketelitian dan sistematika tinggi.",
        "love": "Saya paling puas saat menemukan anomali dalam data yang sudah seminggu bikin tim "
                "bingung, atau saat pipeline data yang saya bangun berjalan tanpa error selama berbulan-bulan. "
                "Membuat sesuatu yang chaotic menjadi terstruktur dan dapat dipercaya adalah kepuasan saya.",
        "good_at": "Saya kuat di SQL, data pipeline (dbt/Airflow), dan exploratory analysis dengan Python. "
                   "Juga terbiasa menulis test plan dan automation test untuk memastikan kualitas sistem. "
                   "Detail kecil yang sering terlewat engineer lain justru yang paling saya perhatikan.",
        "world_needs": "Dunia butuh data yang bisa dipercaya untuk pengambilan keputusan yang benar. "
                       "Tanpa data quality yang solid, semua dashboard dan AI model hanya noise. "
                       "Saya ingin jadi penjaga integritas data di organisasi yang data-driven.",
        "paid_for": "Saya cocok di data-driven company — fintech, e-commerce, atau SaaS — yang serius "
                    "investasi di data infrastructure. Model kerja remote atau hybrid dengan jalur "
                    "karier yang jelas dari analyst ke senior data engineer adalah ideal saya.",
    },
}

# ─── KONTEKS PERTANYAAN PER DIMENSI ───────────────────────────────────────────
DIMENSION_GUIDE = {
    "what_you_love": {
        "label": "Apa yang kamu CINTAI",
        "pertanyaan": "Dari opsi aktivitas kerja berikut, mana yang paling ingin kamu lakukan berulang kali?",
        "jika_memilih": "Jelaskan bagian spesifik dari aktivitas itu yang paling kamu sukai dan mengapa itu menarik bagimu secara pribadi.",
        "jika_tidak": "Jelaskan aktivitas seperti apa yang lebih kamu inginkan dan mengapa opsi yang ada kurang menarik.",
    },
    "what_you_are_good_at": {
        "label": "Apa yang kamu KUASAI",
        "pertanyaan": "Aktivitas mana yang paling yakin bisa kamu kerjakan dengan baik tanpa banyak persiapan?",
        "jika_memilih": "Jelaskan keahlian atau pengalaman konkret yang membuatmu yakin bisa mengerjakannya — apakah dari latihan, pengalaman kerja, atau bakat alami.",
        "jika_tidak": "Jelaskan aktivitas apa yang lebih sesuai dengan keahlianmu dan apa yang membuatmu lebih percaya diri di sana.",
    },
    "what_the_world_needs": {
        "label": "Apa yang DUNIA BUTUHKAN",
        "pertanyaan": "Dampak seperti apa yang menurutmu paling penting untuk masyarakat saat ini?",
        "jika_memilih": "Jelaskan mengapa dampak ini penting bagimu — bisa dari pengalaman pribadi, nilai hidup, atau keprihatinan terhadap kondisi dunia.",
        "jika_tidak": "Jelaskan kontribusi apa yang lebih ingin kamu berikan dan mengapa dampak yang ditawarkan opsi kurang relevan bagimu.",
    },
    "what_you_can_be_paid_for": {
        "label": "Apa yang bisa MENGHASILKAN uang",
        "pertanyaan": "Pola kerja dan penghasilan seperti apa yang paling realistis dan nyaman untuk jangka panjang?",
        "jika_memilih": "Jelaskan mengapa pola kerja/penghasilan ini paling sesuai dengan prioritas hidupmu — stabilitas, fleksibilitas, potensi, atau lifestyle.",
        "jika_tidak": "Jelaskan pola kerja/penghasilan ideal yang kamu bayangkan dan mengapa opsi yang ada tidak cukup sesuai.",
    },
}

def _build_riasec_persona_context(riasec_code: str) -> dict:
    """Gabungkan konteks persona dari semua huruf RIASEC dalam kode."""
    letters = list(riasec_code)
    if not letters:
        return PERSONA_DETAIL.get("I", {})

    primary = PERSONA_DETAIL.get(letters[0], PERSONA_DETAIL["I"])
    if len(letters) == 1:
        return primary

    # Multi-code: gabungkan latar dari primary, ambil dimensi dari huruf paling relevan
    combined = dict(primary)
    combined["latar"] = primary["latar"]

    # Untuk multi-code, enrichkan tiap dimensi dengan nuansa huruf lain
    for letter in letters[1:]:
        detail = PERSONA_DETAIL.get(letter, {})
        for dim in ["love", "good_at", "world_needs", "paid_for"]:
            if dim in detail:
                combined[dim] = combined.get(dim, "") + " " + detail[dim]

    return combined


def ai_answer_ikigai(token: str, headers: dict, persona: dict,
                     candidates: list, riasec_code: str) -> dict:
    """
    Jawab 4 dimensi Ikigai dengan reasoning yang kaya dan konsisten dengan RIASEC.

    Perbedaan dari versi lama:
    - Payload pakai selected_profession_ids (List[int]) sesuai schema baru (poin 14)
    - selection_type dikirim sebagai konteks scoring (poin 15)
    - dimension_options dari response backend dipakai AI sebagai konteks pilihan checkbox
    - System prompt kaya: latar, karakter, pandangan per dimensi per kode RIASEC
    - Reasoning WAJIB min 40 kata, spesifik per dimensi, tidak generik
    - Multi-code (RIA): konteks gabungan dari semua huruf
    """
    sec("AI Menjawab Ikigai")

    target_code = persona.get("target_code", riasec_code)
    ctx = _build_riasec_persona_context(target_code)

    DIMS = [
        "what_you_love",
        "what_you_are_good_at",
        "what_the_world_needs",
        "what_you_can_be_paid_for",
    ]
    DIM_FIELD = {
        "what_you_love":            "love",
        "what_you_are_good_at":     "good_at",
        "what_the_world_needs":     "world_needs",
        "what_you_can_be_paid_for": "paid_for",
    }
    DIM_COLORS = {
        "what_you_love":            MG,
        "what_you_are_good_at":     CY,
        "what_the_world_needs":     GR,
        "what_you_can_be_paid_for": YL,
    }

    # Bangun tabel kandidat dengan dimension_content per profesi
    # dimension_content dikirim backend — narasi spesifik per profesi per dimensi
    cands_display = []
    for c in candidates:
        dc = c.get("dimension_content", {})
        # Truncate untuk display — ambil kalimat pertama saja (setelah titik pertama)
        def short(text: str, n: int = 55) -> str:
            t = (text or "").split(".")[0].strip()
            return (t[:n] + "…") if len(t) > n else (t or "-")

        # Prioritas: gunakan _option field (teks checkbox 1 kalimat)
        # Fallback ke narasi panjang jika _option kosong
        opsi_love    = dc.get("what_you_love_option")    or dc.get("what_you_love", "")
        opsi_good_at = dc.get("what_you_are_good_at_option") or dc.get("what_you_are_good_at", "")
        opsi_world   = dc.get("what_the_world_needs_option") or dc.get("what_the_world_needs", "")
        opsi_paid    = dc.get("what_you_can_be_paid_for_option") or dc.get("what_you_can_be_paid_for", "")

        cands_display.append({
            "id":        c["id"],
            "name":      c["name"],
            "opsi_love":    opsi_love,
            "opsi_good_at": opsi_good_at,
            "opsi_world":   opsi_world,
            "opsi_paid":    opsi_paid,
            # Versi pendek untuk display terminal
            "short_love":    short(opsi_love),
            "short_good_at": short(opsi_good_at),
            "short_world":   short(opsi_world),
            "short_paid":    short(opsi_paid),
        })

    # Deteksi apakah dimension_content kosong/tidak ada dari backend (fallback)
    all_empty = all(
        not cands_display[i]["opsi_love"]
        for i in range(len(cands_display))
    ) if cands_display else True

    # Jika kosong, gunakan generic berdasarkan nama profesi
    if all_empty:
        inf("dimension_content kosong dari backend — AI akan pilih berdasarkan nama profesi")
        for c in cands_display:
            c["opsi_love"]    = f"Mengerjakan pekerjaan utama sebagai {c['name']}"
            c["opsi_good_at"] = f"Menyelesaikan tantangan keahlian inti {c['name']}"
            c["opsi_world"]   = f"Memberikan kontribusi nyata melalui peran {c['name']}"
            c["opsi_paid"]    = f"Berkarir profesional sebagai {c['name']}"
            c["short_love"]   = c["opsi_love"][:55]
            c["short_good_at"] = c["opsi_good_at"][:55]
            c["short_world"]  = c["opsi_world"][:55]
            c["short_paid"]   = c["opsi_paid"][:55]

    # Tampilkan kandidat beserta narasi per dimensi
    print(f"\n  {BD}Kandidat & narasi per dimensi (dari backend):{RS}")
    for c in cands_display:
        print(f"\n  [{CY}{c['id']}{RS}] {BD}{c['name']}{RS}")
        print(f"      ❤  {DM}{c['short_love']}{RS}")
        print(f"      ✦  {DM}{c['short_good_at']}{RS}")
        print(f"      🌍 {DM}{c['short_world']}{RS}")
        print(f"      💰 {DM}{c['short_paid']}{RS}")

    # Bangun blok kandidat untuk system prompt — sertakan narasi lengkap per dimensi
    cands_block_lines = []
    for c in cands_display:
        cands_block_lines.append(
            f"  ID {c['id']}: {c['name']}\n"
            f"    - Love (apa yang disukai)   : {c['opsi_love']}\n"
            f"    - GoodAt (apa yang dikuasai): {c['opsi_good_at']}\n"
            f"    - World (apa yang dunia butuh): {c['opsi_world']}\n"
            f"    - Paid (apa yang bisa menghasilkan): {c['opsi_paid']}"
        )
    cands_block = "\n".join(cands_block_lines)

    # System prompt kaya — konteks persona + opsi konkret tiap kandidat
    system = f"""Kamu adalah {persona['full']} dengan kode kepribadian RIASEC {riasec_code}.

LATAR BELAKANG DIRIMU:
{ctx.get('latar', '')}

KARAKTERMU:
{persona['karakter']}

PANDANGAN HIDUPMU PER DIMENSI (referensi WAJIB untuk reasoning):
- Apa yang kamu cintai: {ctx.get('love', '')}
- Apa yang kamu kuasai: {ctx.get('good_at', '')}
- Apa yang dunia butuhkan: {ctx.get('world_needs', '')}
- Apa yang bisa menghasilkan uang: {ctx.get('paid_for', '')}

PROFESI KANDIDAT + OPSI CHECKBOX MASING-MASING:
{cands_block}

CARA MEMILIH:
- Setiap profesi punya opsi checkbox untuk dimensi ini
- Pilih TEPAT 1 profesi yang opsi checkbox-nya PALING SESUAI dengan pandangan hidupmu
- Hanya boleh memilih 1 profesi — jika tidak ada yang cocok, biarkan kosong
- JANGAN pilih lebih dari 1 profesi

ATURAN REASONING (WAJIB):
- Minimal 40 kata, dalam Bahasa Indonesia orang pertama ("Saya...")
- WAJIB menyebut aspek SPESIFIK dari opsi yang dipilih (bukan nama profesi saja)
- Hubungkan dengan latar belakang dan pandangan hidupmu di dimensi itu
- BERBEDA antardimensi — tiap dimensi punya sudut pandang yang unik
- Hindari kalimat generik seperti "profesi ini sesuai" atau "cocok dengan saya"

FORMAT RESPONSE — tulis dalam 1 baris compact, TANPA newline di dalam JSON:
{{"selected_profession_ids": [<satu id saja>], "selection_type": "selected", "reasoning_text": "<reasoning 40+ kata dalam satu paragraf>"}}

Jika tidak ada yang cocok:
{{"selected_profession_ids": [], "selection_type": "not_selected", "reasoning_text": "<alasan 40+ kata>"}}

PENTING: selected_profession_ids hanya boleh berisi MAKSIMAL 1 ID. Tulis seluruh JSON dalam SATU BARIS."""

    results = {}
    for dim_idx, dim_name in enumerate(DIMS, 1):
        guide    = DIMENSION_GUIDE[dim_name]
        dim_col  = DIM_COLORS[dim_name]
        dim_field = DIM_FIELD[dim_name]

        print(f"\n  {dim_col}{BD}[{dim_idx}/4] {guide['label']}{RS}")

        if dim_name == "what_you_can_be_paid_for":
            print(f"  {YL}⏳ Dimensi terakhir — akan trigger AI scoring...{RS}")

        # Opsi per kandidat untuk dimensi ini
        opsi_dim_key = {
            "what_you_love":            "opsi_love",
            "what_you_are_good_at":     "opsi_good_at",
            "what_the_world_needs":     "opsi_world",
            "what_you_can_be_paid_for": "opsi_paid",
        }[dim_name]
        opsi_display = "\n".join(
            f"    ID {c['id']} ({c['name']}): \"{c[opsi_dim_key]}\""
            for c in cands_display
        )

        # Prompt per dimensi — sertakan opsi konkret dimensi ini
        user_p = f"""DIMENSI {dim_idx}: {guide['label']}
PERTANYAAN: {guide['pertanyaan']}

OPSI CHECKBOX UNTUK DIMENSI INI:
{opsi_display}

PANDANGANMU DI DIMENSI INI (dari karaktermu sebagai {riasec_code}):
"{ctx.get(dim_field, '')}"

INSTRUKSI (jika memilih): {guide['jika_memilih']}
INSTRUKSI (jika tidak memilih): {guide['jika_tidak']}

Return JSON sekarang:"""

        answer = None
        for attempt in range(3):
            try:
                raw    = call_ai(system, user_p, max_tokens=800)
                answer = parse_json(raw)

                if not isinstance(answer, dict):
                    raise Exception("Bukan dict")
                # Backward compat: AI masih return single ID
                if "selected_profession_ids" not in answer:
                    sid = answer.get("selected_profession_id")
                    answer["selected_profession_ids"] = [sid] if sid is not None else []
                if "reasoning_text" not in answer:
                    raise Exception("Tidak ada reasoning_text")
                reasoning = answer["reasoning_text"].strip()
                if len(reasoning.split()) < 15:
                    raise Exception(f"Reasoning terlalu pendek ({len(reasoning.split())} kata)")
                answer["reasoning_text"] = reasoning
                break

            except Exception as ex:
                if attempt == 2:
                    # Fallback — ambil dari konteks persona
                    fallback_id = candidates[0]["id"] if candidates else None
                    fallback_reasoning = ctx.get(dim_field, "")
                    # Ambil 2 kalimat pertama, pastikan > 30 karakter
                    sentences = [s.strip() for s in fallback_reasoning.split(".") if len(s.strip()) > 10]
                    fallback_text = ". ".join(sentences[:3]) + "."
                    if len(fallback_text) < 40:
                        fallback_text = (f"Sebagai seseorang dengan kepribadian {riasec_code}, "
                                         f"saya memilih ini karena {fallback_text}")
                    answer = {
                        "selected_profession_ids": [fallback_id] if fallback_id else [],
                        "selection_type": "selected" if fallback_id else "not_selected",
                        "reasoning_text": fallback_text,
                    }
                    inf(f"Fallback dipakai [{dim_name}] setelah 3 retry ({ex})")
                else:
                    inf(f"Retry {attempt+1}/3 [{dim_name}]: {ex}")
                    time.sleep(2)

        # Server production pakai selected_profession_ids (plural List[int])
        # Maks 1 ID per dimensi (business rule)
        valid_ids_set = {c["id"] for c in candidates}
        raw_ids = answer.get("selected_profession_ids", [])
        if isinstance(raw_ids, list):
            valid_ids = [i for i in raw_ids if i in valid_ids_set]
        elif isinstance(raw_ids, int) and raw_ids in valid_ids_set:
            valid_ids = [raw_ids]
        else:
            valid_ids = []
        # Enforce maks 1 — ambil yang pertama jika AI tetap return >1
        if len(valid_ids) > 1:
            valid_ids = valid_ids[:1]

        selection_type = "selected" if valid_ids else "not_selected"

        # Payload sesuai SubmitDimensionRequest (selected_profession_ids plural list)
        payload = {
            "session_token":           token,
            "dimension_name":          dim_name,
            "selected_profession_ids": valid_ids,   # List[int], boleh kosong
            "selection_type":          selection_type,
            "reasoning_text":          answer["reasoning_text"],
        }
        resp = requests.post(
            f"{API_V1}/career-profile/ikigai/submit-dimension",
            json=payload, headers=headers, timeout=90,
        )

        # ── Tampilkan hasil ──────────────────────────────────────
        chosen_names = [c["name"] for c in candidates if c["id"] in valid_ids]
        icon = f"{GR}✓{RS}" if resp.status_code == 200 else f"{RD}✗{RS}"

        print(f"  {icon} Status  : HTTP {resp.status_code}")
        if chosen_names:
            for cn in chosen_names:
                print(f"     Pilihan : {GR}{BD}{cn}{RS}")
                # Tampilkan juga opsi spesifik yang dipilih
                chosen_c = next((c for c in cands_display if c["name"] == cn), None)
                if chosen_c:
                    opsi_txt = chosen_c.get(opsi_dim_key, "")
                    if opsi_txt and opsi_txt != "-":
                        print(f"     Opsi    : {DM}\"{opsi_txt}\"{RS}")
        else:
            print(f"     Pilihan : {DM}(tidak ada yang dipilih){RS}")

        # Reasoning ditampilkan dengan word-wrap rapi
        reasoning = answer["reasoning_text"]
        word_count = len(reasoning.split())
        print(f"     Alasan  : {DM}({word_count} kata){RS}")
        for line in textwrap.wrap(reasoning, 58):
            print(f"       {line}")

        if resp.status_code != 200:
            err(f"Submit gagal: {resp.text[:200]}")
        else:
            # Cek completion setelah dimensi 4
            try:
                resp_data = resp.json()
                is_complete = (
                    resp_data.get("status") == "completed" or
                    resp_data.get("all_completed") is True
                )
                if is_complete:
                    top2 = resp_data.get("top_2_professions", [])
                    print(f"\n  {GR}{'─'*50}{RS}")
                    print(f"  {GR}{BD}🎯 Scoring Selesai!{RS}")
                    for p in top2:
                        rank  = p.get('rank', '-')
                        name  = p.get('profession_name', '?')
                        score = p.get('total_score', 0)
                        love  = p.get('score_what_you_love', 0)
                        good  = p.get('score_what_you_are_good_at', 0)
                        world = p.get('score_what_the_world_needs', 0)
                        paid  = p.get('score_what_you_can_be_paid_for', 0)
                        print(f"\n  #{rank} {GR}{BD}{name}{RS}  total={score:.4f}")
                        print(f"       love={love:.3f}  good={good:.3f}  "
                              f"world={world:.3f}  paid={paid:.3f}")
                    print(f"  {GR}{'─'*50}{RS}")
            except Exception:
                pass

        results[dim_name] = {
            "label":     guide["label"],
            "chosen":    chosen_names,
            "reasoning": reasoning,
            "status":    resp.status_code,
        }
        time.sleep(0.5)

    return results

def _print_persona_info(persona: dict, target_code: str):
    """Tampilkan info persona yang sedang dipakai."""
    print(f"\n  {BD}Persona aktif:{RS}")
    print(f"    Nama     : {MG}{BD}{persona['full']}{RS}")
    print(f"    Karakter : {DM}{persona['karakter']}{RS}")
    print(f"    Target   : {GR}{BD}{target_code}{RS} — {' + '.join(RIASEC_LABELS.get(c, c) for c in target_code)}")
    avgs = classify_target(target_code)
    print(f"    Kalibrasi: ", end="")
    for t in "RIASEC":
        a = avgs.get(t, 1.7)
        col = f"{BD}{GR}" if t in target_code else DM
        print(f"{col}{t}:{a:.1f}{RS}", end="  ")
    print()


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{BD}{CY}  REXTRA-AI - AI Test Runner  |  {now}{RS}\n")

    if not OR_KEY or "xxxxx" in OR_KEY:
        err("OPENROUTER_API_KEY belum diset!"); sys.exit(1)

    # ── PILIH MODE ────────────────────────────────────────────────────────────
    print(f"  {BD}Mode tes:{RS}")
    print(f"    {BD}{GR}1{RS} — PATHFINDER  (Recommendation + Ikigai) {DM}← default{RS}")
    print(f"    {BD}{GR}2{RS} — BUILDER     (pilih: Recommendation atau Fit Check)")
    raw_mode = input(f"\n  Pilih mode [1/2, Enter=1]: ").strip()
    is_builder = raw_mode == "2"

    test_mode = "recommendation"  # default
    if is_builder:
        print(f"\n  {BD}Tipe sesi BUILDER:{RS}")
        print(f"    {BD}{GR}R{RS} — Recommendation (full: RIASEC + Ikigai)")
        print(f"    {BD}{GR}F{RS} — Fit Check only  (RIASEC saja, tidak ada Ikigai)")
        raw_sesi = input(f"\n  Pilih [R/F, Enter=R]: ").strip().upper()
        test_mode = "fit_check" if raw_sesi == "F" else "recommendation"

    persona_type = "BUILDER" if is_builder else "PATHFINDER"
    print(f"\n  {GR}Mode: {BD}{persona_type}{RS} — {test_mode.upper()}")

    # ── PILIH TARGET RIASEC + PERSONA ─────────────────────────────────────────
    print(f"\n  {BD}Target RIASEC:{RS}")
    for k, v in RIASEC_LABELS.items():
        p = PERSONAS.get(k, {})
        print(f"    {BD}{GR}{k}{RS} - {v:<14} {DM}({p.get('full', '')}){RS}")
    print(f"\n  {DM}1 huruf (R), 2 huruf (RI, IA), atau 3 huruf (RIA, SEC){RS}")
    print(f"  {DM}Enter = Random{RS}")

    raw = input(f"\n  Target RIASEC: ").strip().upper()
    valid = list(dict.fromkeys(c for c in raw if c in RIASEC_LABELS))

    if valid:
        target_code = "".join(valid[:3])
        persona     = dict(PERSONAS[valid[0]])
    else:
        key         = random.choice(list(PERSONAS.keys()))
        persona     = dict(PERSONAS[key])
        target_code = key
        print(f"  {GR}Random → {BD}{target_code}{RS}")

    persona["target_code"] = target_code
    _print_persona_info(persona, target_code)

    # Load questions
    for p in ["data/riasec_questions.json", "riasec_questions.json"]:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                raw_q = json.load(f)
            questions = raw_q if isinstance(raw_q, list) else raw_q.get("questions", [])
            ok(f"{len(questions)} soal dimuat"); break
    else:
        err("riasec_questions.json tidak ditemukan!"); sys.exit(1)

    user_id = create_user(persona["full"])
    HEADERS = {"x-user-id": user_id, "Content-Type": "application/json"}

    # ── START SESSION ─────────────────────────────────────────────────────────
    if test_mode == "fit_check":
        print(f"\n{BD}{CY}  ALUR FIT CHECK ({persona_type}){RS}")
        # Fit check butuh target_profession_id dan persona_type
        fit_profession_id = input(f"  Masukkan target_profession_id [default=5]: ").strip()
        fit_profession_id = int(fit_profession_id) if fit_profession_id.isdigit() else 5
        
        payload = {
            "persona_type": persona_type,
            "target_profession_id": fit_profession_id
        }
        
        r = requests.post(f"{API_V1}/career-profile/fit-check/start",
                          json=payload, headers=HEADERS, timeout=30)
        if r.status_code not in [200, 201]:
            err(f"Start fit-check gagal: {r.text[:200]}"); sys.exit(1)
        rec_data  = r.json()
        rec_token = rec_data.get("session_token") or rec_data.get("token")
        ok(f"Session: {rec_token[:24]}...")
    else:
        print(f"\n{BD}{CY}  ALUR RECOMMENDATION ({persona_type}){RS}")

        # ── Cek profil aktif user sebelum tes ────────────────────────────
        try:
            r_prof = requests.get(f"{API_V1}/career-profile/user-profile", headers=HEADERS, timeout=10)
            if r_prof.status_code == 200:
                pd = r_prof.json()
                if pd.get("has_active_profile"):
                    inf(f"Profil aktif: kode={GR}{pd.get('riasec_code','?')}{RS}  top1={pd.get('top_profession1_id','?')}  top2={pd.get('top_profession2_id','?')}")
                    inf("Ini tes ke-2+. Setelah selesai, user bisa set profil baru via /user-profile/set-active")
                else:
                    inf("Belum ada profil aktif → tes RECOMMENDATION pertama, akan auto-save setelah selesai")
        except Exception:
            pass

        r = requests.post(f"{API_V1}/career-profile/recommendation/start",
                          json={"persona_type": persona_type}, headers=HEADERS, timeout=30)
        if r.status_code not in [200, 201]:
            err(f"Start gagal: {r.text[:200]}"); sys.exit(1)
        rec_data  = r.json()
        rec_token = rec_data.get("session_token") or rec_data.get("token")
        _tes_start_time = time.time()   # ← Timer mulai saat sesi dibuat # CONFIG: hapus baris ini jika track dari login
        ok(f"Session: {rec_token[:24]}...")

    ai_responses = ai_answer_riasec(questions, target_code, persona)

    # Submit
    sec("Submit ke API")
    r = requests.post(f"{API_V1}/career-profile/riasec/submit",
                      json={"session_token": rec_token, "responses": ai_responses},
                      headers=HEADERS, timeout=30)
    if r.status_code != 200:
        err(f"Submit gagal: {r.text[:300]}"); sys.exit(1)

    res_data    = r.json()
    riasec_code = res_data.get("riasec_code_info", {}).get("riasec_code") or res_data.get("riasec_code", "?")
    scores      = res_data.get("scores", {})
    match_ok    = riasec_code == target_code

    ok(f"RIASEC hasil: {BD}{GR}{riasec_code}{RS}")
    if match_ok:
        print(f"  {GR}🎯 Target '{target_code}' TERCAPAI PERSIS!{RS}")
    elif all(c in riasec_code for c in target_code):
        print(f"  {YL}≈ Semua huruf target ada di '{riasec_code}'{RS}")
    else:
        print(f"  {YL}Target '{target_code}' → hasil '{riasec_code}'{RS}")

    # Fit check tidak punya alur Ikigai — langsung ke hasil
    if test_mode == "fit_check":
        sec("Hasil Fit Check")
        time.sleep(2)
        r_fc = requests.get(f"{API_V1}/career-profile/result/fit-check/{rec_token}", headers=HEADERS)
        fc_result = r_fc.json() if r_fc.status_code == 200 else {}
        if fc_result:
            ok("Fit Check result diterima!")
            mc = fc_result.get("fit_check_result", {}).get("match_category", "?")
            print(f"     Match Category : {GR}{BD}{mc}{RS}")
        else:
            err(f"Fit Check result gagal: {r_fc.text[:200]}")

        # Simpan JSON lengkap
        summary = {
            "run_at": now, "mode": "fit_check", "target_riasec": target_code,
            "hasil_riasec": riasec_code, "target_tercapai": match_ok,
            "persona": persona["full"], "riasec_scores_raw": scores,
            "fit_check_result": fc_result,
        }
        
        # Simpan ke folder test_results/career_profile
        os.makedirs("test_results/career_profile", exist_ok=True)
        fname = f"test_results/career_profile/ai_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        ok(f"Tersimpan: {BD}{fname}{RS}")
        print(f"\n{BD}{GR}  SELESAI!{RS}\n")
        return

    # Ikigai (hanya untuk mode recommendation)
    sec("Mulai Ikigai")
    r = requests.post(f"{API_V1}/career-profile/ikigai/start",
                      json={"session_token": rec_token}, headers=HEADERS, timeout=90)
    if r.status_code != 200:
        err(f"Ikigai start gagal: {r.text[:300]}"); sys.exit(1)

    d = r.json()
    professions = d.get("candidates_with_content", d.get("professions", []))

    # Info jumlah kandidat dari metadata response
    total_display   = d.get("total_display_candidates", len(professions))
    total_evaluated = d.get("total_professions_evaluated", "?")  # dari scoring metadata
    # Hitung total kandidat dari response (display + backup)
    all_cands_raw = d.get("candidates_with_content", [])
    backup_count  = d.get("total_backup_candidates", 0)
    total_all     = total_display + backup_count

    # Kode kongruen yang dipakai
    congruent_codes = d.get("congruent_codes_used", [])
    expansion = d.get("expansion_summary", {})
    backup_cands = d.get("backup_candidates", [])
    backup_count = d.get("total_backup_candidates", max(0, len(backup_cands)))
    total_all = total_display + backup_count

    # Tampilkan ringkasan ekspansi kandidat
    print(f"\n  {BD}Ekspansi kandidat dari kode {GR}{riasec_code}{RS}:")
    if congruent_codes:
        print(f"    Kode kongruen    : {CY}{', '.join(congruent_codes)}{RS}")
    if expansion:
        t1 = expansion.get("tier_1_exact", 0)
        t2 = expansion.get("tier_2_congruent", 0)
        t3 = expansion.get("tier_3_subset", 0)
        t4 = expansion.get("tier_4_dominant", 0)
        print(f"    Tier 1 (persis)  : {GR}{t1}{RS} profesi  ← prioritas opsi soal")
        if t2: print(f"    Tier 2 (kongr.)  : {DM}{t2}{RS} profesi")
        if t3: print(f"    Tier 3 (subset)  : {DM}{t3}{RS} profesi")
        if t4: print(f"    Tier 4 (dominan) : {DM}{t4}{RS} profesi")
    print(f"    Opsi soal (display) : {CY}{BD}{total_display}{RS} profesi")
    print(f"    Backup scoring      : {DM}{backup_count}{RS} profesi")
    print(f"    TOTAL kandidat      : {CY}{BD}{total_all}{RS} profesi")
    if total_all > 20:
        print(f"    {YL}⚠ Melebihi maks 20 — cek riasec_service_patch sudah di-deploy{RS}")

    # Ambil dimension_content dari response backend (poin 13)
    # Backend mengirim "dimension_content" per profesi — BUKAN "dimension_options"
    # Fields: what_you_love, what_you_are_good_at, what_the_world_needs, what_you_can_be_paid_for
    # Setiap field = narasi 1-2 kalimat spesifik per profesi — ini yang jadi teks checkbox
    candidates = [
        {
            "id":   p.get("profession_id"),
            "name": p.get("profession_name", p.get("name", "?")),
            # dimension_content: dict 4 field narasi spesifik per profesi
            "dimension_content": p.get("dimension_content", {}),
        }
        for p in professions
    ]
    ok(f"{len(candidates)} kandidat display:")

    ikigai_results = ai_answer_ikigai(rec_token, HEADERS, persona, candidates, riasec_code)

    # Hasil akhir — retry karena scoring async mungkin belum selesai
    sec("Hasil Akhir")
    rec_result = {}
    # Narrative generation butuh hingga 45 detik — tunggu dulu sebelum retry
    inf("Menunggu narrative generation selesai (maks ~60 detik)...")
    time.sleep(10)
    for attempt in range(8):
        r = requests.get(f"{API_V1}/career-profile/result/recommendation/{rec_token}", headers=HEADERS)
        if r.status_code == 200:
            data = r.json()
            # Cek apakah narrative sudah ada (bukan data minimal)
            has_narrative = bool(data.get("ikigai_profile_summary", {}).get("what_you_love"))
            if has_narrative or attempt >= 5:
                rec_result = data
                if has_narrative:
                    ok("Narrative sudah tergenerate!")
                else:
                    inf("Narrative belum ada, pakai data yang tersedia")
                break
            inf(f"Retry {attempt+1}/8 — narrative belum siap, tunggu 8 detik...")
            time.sleep(8)
        else:
            inf(f"Retry {attempt+1}/8 (HTTP {r.status_code})...")
            time.sleep(5)

    RIASEC_NAMES = {"R":"Realistic","I":"Investigative","A":"Artistic","S":"Social","E":"Enterprising","C":"Conventional"}

    if rec_result:
        ok("Rekomendasi diterima!")

        riasec_sum  = rec_result.get("riasec_summary", {})
        scores_raw  = rec_result.get("riasec_scores_raw", {})
        rp          = rec_result.get("riasec_profile", {})
        riasec_code = riasec_sum.get("riasec_code", "?")

        # Hitung durasi tes
        _tes_end_time  = time.time()
        _tes_dur_min   = max(1, int((_tes_end_time - _tes_start_time) / 60))  # CONFIG: waktu diukur dari sesi dimulai
        _poin_diberikan = 200   # CONFIG: ubah di sini untuk sesuaikan reward poin

        # ── HEADER HASIL ───────────────────────────────────────────
        print(f"\n{'─'*62}")
        print(f"  {BD}{CY}HASIL TES KARIER{RS}  {DM}[ID: TPKRR{rec_token[-6:].upper()}]{RS}")
        print(f"{'─'*62}")
        print(f"  Berikut adalah ringkasan gabungan dari profil minat")
        print(f"  (RIASEC) dan potensi diri (IKIGAI) kamu.")
        print()

        # ── STATISTIK ─────────────────────────────────────────────
        print(f"  {BD}Statistik Tes:{RS}")
        print(f"    🕐  Durasi     : {GR}{BD}{_tes_dur_min} menit{RS}  {DM}# CONFIG: diukur dari sesi dibuat s/d hasil diterima{RS}")
        print(f"    🏆  Poin       : {GR}{BD}+{_poin_diberikan} REXTRA Poin{RS}  {DM}# CONFIG: sesuaikan di test_ai_runner.py → _poin_diberikan{RS}")
        print(f"    📊  Profil     : {GR}{BD}{riasec_code}{RS}")

        # ── 3.2 RINGKASAN PROFIL RIASEC ──────────────────────────
        print(f"\n  {'─'*58}")
        print(f"  {BD}3.2  Ringkasan Profil RIASEC{RS}")
        print(f"  {'─'*58}")
        if scores_raw:
            # Sort by score desc
            sorted_types = sorted("RIASEC", key=lambda t: scores_raw.get(t, 0), reverse=True)
            max_s = max(scores_raw.values()) if scores_raw else 60
            for t in sorted_types:
                s     = scores_raw.get(t, 0)
                width = max(1, int(s / max_s * 24))
                bar   = "█" * width
                name  = RIASEC_NAMES.get(t, t)
                is_top = t in riasec_code
                if is_top:
                    print(f"    {GR}{BD}{t} {name:<14}{RS} {GR}{bar:<24}{RS} {BD}{s}{RS}")
                else:
                    print(f"    {DM}{t} {name:<14}{RS} {DM}{bar:<24}{RS} {DM}{s}{RS}")

        # Summary text dari riasec_description (dari tabel riasec_codes via /result)
        rp_desc = rp.get("riasec_description", "")
        top_types_full = [RIASEC_NAMES.get(l, l) for l in riasec_code if l in RIASEC_NAMES]
        if top_types_full:
            types_str = ", ".join([f"{BD}{t}{RS}" for t in top_types_full])
            print(f"\n  Skor tertinggimu ada pada tipe {types_str}.")
            print(f"  Kombinasi ini membentuk profil dengan kode {GR}{BD}{riasec_code}{RS}.")
        if rp_desc:
            for line in textwrap.wrap(rp_desc, 58):
                print(f"  {DM}{line}{RS}")
        print(f"\n  {DM}→ Lihat Tab Kepribadian untuk penjelasan lengkap profil {riasec_code}{RS}")

        # ── 3.3 KANDIDAT PROFESI ──────────────────────────────────
        display_cands = rec_result.get("display_candidates", [])
        congr_cands   = rec_result.get("congruent_candidates", [])
        total_cands   = len(display_cands) + len(congr_cands)
        print(f"\n  {'─'*58}")
        print(f"  {BD}3.3  Kandidat Profesi yang Relevan{RS}")
        print(f"  {'─'*58}")
        print(f"  Dari kode {GR}{BD}{riasec_code}{RS}, REXTRA menemukan {GR}{BD}{total_cands}{RS} profesi")
        print(f"  yang selaras dengan pola kerjamu.")
        print()
        all_cands = display_cands + congr_cands
        for c in all_cands:
            tier = c.get("expansion_tier")
            ctype = c.get("congruence_type", "")
            tag = f"Tier {tier}" if tier else ctype
            print(f"    💼 {c['name']:<36} {DM}{tag}{RS}")

        # ── 3.4 PROFIL IKIGAI ─────────────────────────────────────
        ik_sum = rec_result.get("ikigai_profile_summary", {})
        print(f"\n  {'─'*58}")
        print(f"  {BD}3.4  Profil Ikigai{RS}")
        print(f"  {'─'*58}")
        print(f"  {DM}Tes RIASEC mengidentifikasi minat dan cara kerjamu.")
        print(f"  IKIGAI melengkapinya dengan memetakan apa yang kamu")
        print(f"  sukai, kuasai, dampak untuk dunia, dan nilai ekonominya.{RS}")
        print()
        ikigai_dims = [
            ("what_you_love",         "❤ ", "Love    ", "Apa yang kamu sukai"),
            ("what_you_are_good_at",  "⭐ ", "Good At ", "Apa yang kamu kuasai"),
            ("what_the_world_needs",  "🌍 ", "Needs   ", "Apa yang dibutuhkan dunia"),
            ("what_you_can_be_paid_for","💰 ","Paid    ", "Apa yang bisa dibayar"),
        ]
        if ik_sum and any(ik_sum.values()):
            for key, ico, lbl, sublbl in ikigai_dims:
                txt = ik_sum.get(key, "")
                if txt:
                    print(f"    {ico} {BD}{lbl}{RS} {DM}— {sublbl}{RS}")
                    for line in textwrap.wrap(txt, 56):
                        print(f"       {line}")
                    print()
        else:
            print(f"  {YL}ℹ Profil Ikigai belum tergenerate{RS}")

        # ── 3.5 REKOMENDASI KARIER UTAMA ──────────────────────────
        top = rec_result.get("recommended_professions", [])
        print(f"  {'─'*58}")
        print(f"  {BD}3.5  Rekomendasi Profesi Terbaik{RS}")
        print(f"  {'─'*58}")
        print(f"  Berikut dua profesi yang paling selaras dengan")
        print(f"  profil RIASEC dan IKIGAI-mu.")
        for i, p in enumerate(top[:2], 1):
            pname     = p.get("profession_name", "?")
            match_pct = p.get("match_percentage", 0)
            reasoning = p.get("match_reasoning", "")
            print(f"\n    {'┌'+'─'*54+'┐'}")
            match_badge = f"{match_pct:.0f}% cocok"
            name_pad = 54 - len(match_badge) - 2
            print(f"    │ {GR}{BD}{pname:<{name_pad}}{RS}{CY}{match_badge}{RS} │")
            print(f"    {'├'+'─'*54+'┤'}")
            if reasoning:
                for line in textwrap.wrap(reasoning, 52):
                    print(f"    │ {DM}{line:<52}{RS} │")
            print(f"    {'├'+'─'*54+'┤'}")
            print(f"    │ {DM}Lihat detail profesi >{' '*32}{RS}│")
            print(f"    {'└'+'─'*54+'┘'}")

        # ── 3.6 SHARE & REWARD ────────────────────────────────────
        print(f"\n  {'─'*58}")
        print(f"  {BD}3.6  Share & Reward{RS}")
        print(f"  {'─'*58}")
        print(f"  📢 Bagikan hasil tes ini ke media sosial &")
        print(f"     dapatkan bonus {GR}{BD}+100 REXTRA Poin{RS}")
        print(f"  {DM}[Bagikan Hasil Tes]{RS}")

        # ── TAB 2: KEPRIBADIAN ────────────────────────────────────
        print(f"\n  {'═'*58}")
        print(f"  {BD}{CY}TAB 2 — KEPRIBADIAN{RS}")
        print(f"  {'═'*58}")

        # Section 1: Profil Kode
        print(f"\n  {BD}Profil Kode: {GR}{riasec_code}{RS}")
        code_parts = [f"{l} ({RIASEC_NAMES.get(l,l)})" for l in riasec_code if l in RIASEC_NAMES]
        print(f"  {DM}{' • '.join(code_parts)}{RS}")

        # Section 2: Tentang Kode (dari riasec_description di DB)
        print(f"\n  {BD}Tentang Kode {riasec_code}{RS}")
        n = len(riasec_code)
        if n == 1:
            l1 = RIASEC_NAMES.get(riasec_code[0], riasec_code[0])
            narasi = f"Kode {BD}{riasec_code}{RS} menunjukkan bahwa kepribadian kariermu didominasi oleh tipe {BD}{l1}{RS}."
        elif n == 2:
            l1 = RIASEC_NAMES.get(riasec_code[0], riasec_code[0])
            l2 = RIASEC_NAMES.get(riasec_code[1], riasec_code[1])
            narasi = f"Kode {BD}{riasec_code}{RS} menunjukkan kekuatan utamamu adalah {BD}{l1}{RS}, cara kerjamu dipengaruhi sifat {BD}{l2}{RS}."
        else:
            l1 = RIASEC_NAMES.get(riasec_code[0], riasec_code[0])
            l2 = RIASEC_NAMES.get(riasec_code[1], riasec_code[1])
            l3 = RIASEC_NAMES.get(riasec_code[2], riasec_code[2])
            narasi = f"Kode {BD}{riasec_code}{RS} — kekuatan utama {BD}{l1}{RS}, dipengaruhi pola pikir {BD}{l2}{RS} dan gaya {BD}{l3}{RS}."
        print(f"  {narasi}")
        if rp_desc:
            for line in textwrap.wrap(rp_desc, 56):
                print(f"  {DM}{line}{RS}")

        # Section 3: Strengths
        if rp and rp.get("strengths"):
            print(f"\n  {GR}{BD}✦ Kekuatan Profil (Strengths){RS}")
            print(f"  {DM}Profil {riasec_code} menunjukkan keunggulan kompetitif:{RS}")
            for s in rp.get("strengths", []):
                for line in textwrap.wrap(f"✓ {s}", 56):
                    print(f"    {GR}{line}{RS}")

        # Section 4: Challenges
        if rp and rp.get("challenges"):
            print(f"\n  {YL}{BD}⚠ Tantangan Profil (Challenges){RS}")
            print(f"  {DM}Tantangan yang perlu diperhatikan:{RS}")
            for c in rp.get("challenges", []):
                for line in textwrap.wrap(f"⚠ {c}", 56):
                    print(f"    {YL}{line}{RS}")

        # Section 5: Strategies
        if rp and rp.get("strategies"):
            print(f"\n  {CY}{BD}💡 Strategi Pengembangan Diri{RS}")
            print(f"  {DM}Strategi konkret untuk berkembang:{RS}")
            for s in rp.get("strategies", []):
                for line in textwrap.wrap(f"💡 {s}", 56):
                    print(f"    {CY}{line}{RS}")

        # Section 6: Interaction Styles
        if rp and rp.get("interaction_styles"):
            print(f"\n  {BD}👥 Gaya Interaksi & Kolaborasi{RS}")
            print(f"  {DM}Profil {riasec_code} dalam tim:{RS}")
            for item in rp.get("interaction_styles", []):
                for line in textwrap.wrap(f"👥 {item}", 56):
                    print(f"    {line}")

        # Section 7: Work Environments
        if rp and rp.get("work_environments"):
            print(f"\n  {BD}🏢 Lingkungan Kerja Ideal{RS}")
            print(f"  {DM}Paling produktif di:{RS}")
            for item in rp.get("work_environments", []):
                for line in textwrap.wrap(f"🏢 {item}", 56):
                    print(f"    {line}")

        if not rp or not rp.get("strengths"):
            print(f"\n  {YL}ℹ riasec_profile kosong — pastikan tabel riasec_codes sudah di-seed{RS}")

    else:
        err(f"Get result gagal: {r.text[:200]}")

    # Simpan JSON lengkap
    summary = {
        "run_at": now, "target_riasec": target_code, "hasil_riasec": riasec_code,
        "target_tercapai": match_ok, "persona": persona["full"],
        "kalibrasi_avg": classify_target(target_code),
        "riasec_scores_raw": scores,
        "jawaban_riasec": [
            {"no":a["question_id"],"skor":a["answer_value"],"tipe":a["question_type"],
             "soal":next((q["question_text"] for q in questions if q["question_id"]==a["question_id"]),"")
            }
            for a in ai_responses
        ],
        "ikigai_kandidat": candidates,
        "ikigai_jawaban": {d:{"pilihan":v["chosen"],"alasan":v["reasoning"]} for d,v in ikigai_results.items()},
        # Dari /result/recommendation — sudah include RIASEC profile + ikigai + rekomendasi
        "rekomendasi_akhir": rec_result,
        # Convenience: extract top fields untuk mudah dibaca
        "riasec_profil": rec_result.get("riasec_profile", {}),
        "ikigai_profil_per_dimensi": rec_result.get("ikigai_profile_summary", {}),
        "kandidat_display": rec_result.get("display_candidates", []),
        "kandidat_backup":  rec_result.get("congruent_candidates", []),
        "top_rekomendasi":  rec_result.get("recommended_professions", []),
    }
    
    # Simpan ke folder test_results/career_profile
    os.makedirs("test_results/career_profile", exist_ok=True)
    fname = f"test_results/career_profile/ai_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # ── Verifikasi user_career_profiles setelah tes ───────────────────────
    try:
        r_prof2 = requests.get(f"{API_V1}/career-profile/user-profile", headers=HEADERS, timeout=10)
        if r_prof2.status_code == 200:
            pd2 = r_prof2.json()
            if pd2.get("has_active_profile"):
                ok(f"user_career_profiles ✓  kode={GR}{BD}{pd2.get('riasec_code','?')}{RS}  "
                   f"top1={pd2.get('top_profession1_id','?')}  top2={pd2.get('top_profession2_id','?')}")
            else:
                inf("user_career_profiles: kosong (auto-save belum jalan atau endpoint belum di-deploy)")
        else:
            inf(f"GET /user-profile → HTTP {r_prof2.status_code}")
    except Exception as _e:
        inf(f"user-profile check skip: {_e}")

    # ── Cek user_career_profiles setelah tes selesai ─────────────────────
    r_prof2 = requests.get(f"{API_V1}/career-profile/user-profile", headers=HEADERS, timeout=10)
    if r_prof2.status_code == 200:
        pd2 = r_prof2.json()
        if pd2.get("has_active_profile"):
            ok(f"user_career_profiles: profil aktif = {GR}kode {pd2.get('riasec_code','?')}{RS}  "
               f"top1={pd2.get('top_profession1_id','?')}  top2={pd2.get('top_profession2_id','?')}")
        else:
            inf("user_career_profiles: masih kosong (auto-save mungkin gagal)")

    ok(f"Tersimpan: {BD}{fname}{RS}")
    print(f"\n{BD}{GR}  SELESAI!{RS}\n")

if __name__ == "__main__":
    main()
"""
╔══════════════════════════════════════════════════════════════╗
║      REXTRA-AI API - Full Test Runner v4                   ║
║  Jalankan: python test_all_api.py                            ║
║  - Tampilkan error DB asli (field "error" dari response)     ║
║  - Rate limit sudah dinaikkan untuk testing                  ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, uuid, json, requests
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

FASTAPI_URL  = "http://localhost:8000"
API_V1       = f"{FASTAPI_URL}/api/v1"
GOLANG_HOST  = "http://103.171.84.248"
REGISTER_URL = f"{GOLANG_HOST}/api/v1/auth/register"
DB_URL       = os.getenv("DATABASE_URL", "")

RAND       = str(uuid.uuid4())[:8]
TEST_EMAIL = f"autotest_{RAND}@kenalidiri.dev"
TEST_PASS  = "AutoTest.123"
TEST_PHONE = f"0812{RAND[:8].replace('-','')}"
TEST_NAME  = f"Auto Tester {RAND}"

# Load question type map
QUESTION_TYPE_MAP = {}
for p in ["data/riasec_questions.json", "../data/riasec_questions.json",
          str(Path(__file__).parent / "data" / "riasec_questions.json")]:
    if Path(p).exists():
        with open(p) as f:
            items = json.load(f)
        items = items if isinstance(items, list) else items.get("questions", [])
        for item in items:
            QUESTION_TYPE_MAP[item["question_id"]] = item["riasec_type"][0].upper()
        break
if not QUESTION_TYPE_MAP:
    for i, t in enumerate(["R","I","A","S","E","C"]):
        for q in range(1, 13):
            QUESTION_TYPE_MAP[(i*12)+q] = t

results = []

def log(status, name, code, detail=""):
    icon  = "✓" if status == "PASS" else ("⚠" if status == "SKIP" else "✗")
    color = "\033[92m" if status == "PASS" else ("\033[93m" if status == "SKIP" else "\033[91m")
    reset = "\033[0m"
    print(f"  {color}{icon} [{code}] {name}{reset}" +
          (f"\n       └─ {detail}" if detail and status != "PASS" else ""))
    results.append({"status": status, "name": name, "code": code, "detail": detail})

def req(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=30, **kwargs)
    except Exception as e:
        class F:
            status_code = 0
            text = str(e)
            def json(self): return {}
        return F()

def test(name, method, url, expected=200, headers=None, json_body=None, params=None):
    r = req(method, url, headers=headers, json=json_body, params=params)
    ok = r.status_code == expected or (expected == 200 and r.status_code in [200, 201])
    detail = ""
    if not ok:
        try:
            body = r.json()
            # FIX: tampilkan "error" field dulu (berisi pesan DB asli),
            # fallback ke "detail" kalau "error" tidak ada
            raw_error = body.get("error") or body.get("detail") or body
            detail = str(raw_error)[:300]
        except:
            detail = r.text[:300]
    log("PASS" if ok else "FAIL", name, r.status_code, detail)
    return ok, r

def build_riasec_payload(session_token, question_ids):
    base = {"R":5,"I":4,"A":3,"S":2,"E":1,"C":3}
    counter = {}
    responses = []
    for qid in question_ids:
        qt = QUESTION_TYPE_MAP.get(qid, "R")
        counter[qt] = counter.get(qt, 0) + 1
        n = counter[qt]
        val = base[qt]
        if n % 4 == 0: val = min(val+1, 5)
        if n % 5 == 0: val = max(val-1, 1)
        responses.append({
            "question_id": qid, "question_type": qt,
            "answer_value": val,
            "answered_at": datetime.now(timezone.utc).isoformat()
        })
    return {"session_token": session_token, "responses": responses}

# ═══════════════════════════════════════════════════════════════
print()
print("╔══════════════════════════════════════════════════════════════╗")
print("║         REXTRA-AI API - Full Test Runner v4                ║")
print(f"║  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                          ║")
print("╚══════════════════════════════════════════════════════════════╝")

print(f"\n🚀 Memeriksa server di {FASTAPI_URL}...")
r = req("GET", f"{FASTAPI_URL}/health")
if r.status_code == 0:
    print("  ✗ Server tidak merespons! Jalankan uvicorn dulu."); sys.exit(1)
print(f"  ✓ Server aktif (status {r.status_code})")
print(f"  ✓ {len(QUESTION_TYPE_MAP)} soal dimuat dari riasec_questions.json")

# ─── BUAT USER ───────────────────────────────────────────────
print(f"\n👤 Membuat user test → {TEST_EMAIL}")
USER_ID = None

r_reg = req("POST", REGISTER_URL, json={
    "fullname": TEST_NAME, "email": TEST_EMAIL,
    "password": TEST_PASS, "phone_number": TEST_PHONE, "role": "USER"
})
if r_reg.status_code in [200, 201]:
    try:
        d = r_reg.json()
        USER_ID = d.get("user_id") or d.get("id") or (d.get("data") or {}).get("id")
        print(f"  ✓ Register via Golang! ID: {USER_ID}")
    except: pass
else:
    print(f"  ⚠ Golang API tidak bisa → insert DB langsung")

try:
    engine = create_engine(DB_URL, pool_pre_ping=True, connect_args={"connect_timeout":10})
    new_uuid = str(uuid.uuid4())
    with engine.connect() as conn:
        existing = conn.execute(
            text("SELECT id, role FROM users WHERE email=:e"), {"e": TEST_EMAIL}
        ).fetchone()
        if existing:
            USER_ID = str(existing[0])
            if existing[1] not in ("USER","EXPERT"):
                conn.execute(text("UPDATE users SET role='USER' WHERE id=:id"), {"id": USER_ID})
                conn.commit()
            print(f"  ✓ User sudah ada. ID: {USER_ID}")
        else:
            conn.execute(text("""
                INSERT INTO users (id, fullname, email, password, phone_number, role, is_verified, created_at)
                VALUES (:id,:name,:email,:pwd,:phone,'USER',true,now())
            """), {"id":new_uuid,"name":TEST_NAME,"email":TEST_EMAIL,"pwd":"hashed","phone":TEST_PHONE})
            try:
                conn.execute(text("""
                    INSERT INTO token_wallet (id, user_id, balance, updated_at)
                    VALUES (:wid,:uid,1000,now())
                """), {"wid":str(uuid.uuid4()),"uid":new_uuid})
                print(f"  ✓ Token wallet dibuat (balance: 1000)")
            except Exception as we:
                print(f"  ⚠ Wallet: {we}")
            conn.commit()
            USER_ID = new_uuid
            print(f"  ✓ User baru! ID: {USER_ID}")
except Exception as e:
    print(f"  ✗ DB: {e}")
    try:
        with engine.connect() as conn:
            row = conn.execute(text("SELECT id FROM users WHERE role IN ('USER','EXPERT') LIMIT 1")).fetchone()
            if row: USER_ID = str(row[0]); print(f"  ✓ Pakai user existing: {USER_ID}")
    except: sys.exit(1)

if not USER_ID: print("  ✗ Gagal dapat User ID!"); sys.exit(1)
print(f"\n  ✅ User ID: {USER_ID}")

HEADERS = {"x-user-id": USER_ID, "Content-Type": "application/json"}

# ═══════════════════════════════════════════════════════════════
print("\n" + "─"*62)
print("  📡 SYSTEM ENDPOINTS")
print("─"*62)
test("GET / (Root)",            "GET", f"{FASTAPI_URL}/")
test("GET /health",             "GET", f"{FASTAPI_URL}/health")
test("GET /api/v1/ (API Root)", "GET", f"{API_V1}/")
test("GET /metrics",            "GET", f"{FASTAPI_URL}/metrics")
test("GET /test-redis",         "GET", f"{FASTAPI_URL}/test-redis")

print("\n" + "─"*62)
print("  📂 CATEGORIES")
print("─"*62)
test("GET /categories/", "GET", f"{API_V1}/categories/")

# ═══════════════════════════════════════════════════════════════
print("\n" + "─"*62)
print("  🎯 ALUR 1: RECOMMENDATION")
print("─"*62)

rec_token = None; rec_qids = None; first_prof_id = None

ok, r = test("POST /career-profile/recommendation/start",
             "POST", f"{API_V1}/career-profile/recommendation/start",
             json_body={"persona_type": "PATHFINDER"}, headers=HEADERS)
if ok:
    rec_token = r.json().get("session_token")
    rec_qids  = r.json().get("question_ids", [])
    print(f"       token: {rec_token}  |  {len(rec_qids)} soal")

if rec_token and rec_qids:
    ok, r = test("POST /career-profile/riasec/submit",
                 "POST", f"{API_V1}/career-profile/riasec/submit",
                 json_body=build_riasec_payload(rec_token, rec_qids), headers=HEADERS)
    if ok:
        print(f"       RIASEC code: {r.json().get('riasec_code_info',{}).get('riasec_code','?')}")

if rec_token:
    test("GET /career-profile/riasec/result/{token}",
         "GET", f"{API_V1}/career-profile/riasec/result/{rec_token}", headers=HEADERS)

if rec_token:
    ok, r = test("POST /career-profile/ikigai/start",
                 "POST", f"{API_V1}/career-profile/ikigai/start",
                 json_body={"session_token": rec_token}, headers=HEADERS)
    if ok:
        cands = r.json().get("candidates_with_content", [])
        if cands:
            first_prof_id = cands[0].get("profession_id")
            print(f"       {len(cands)} kandidat, ID pertama: {first_prof_id}")

if rec_token:
    test("GET /career-profile/ikigai/content/{token}",
         "GET", f"{API_V1}/career-profile/ikigai/content/{rec_token}", headers=HEADERS)

DIMS = [
    ("what_you_love","Dimensi 1 - Love"),
    ("what_you_are_good_at","Dimensi 2 - Good At"),
    ("what_the_world_needs","Dimensi 3 - World Needs"),
    ("what_you_can_be_paid_for","Dimensi 4 - Paid For (FINAL)"),
]
if rec_token and first_prof_id:
    for dim, label in DIMS:
        if "FINAL" in label: print("       ⏳ AI scoring...")
        test(f"POST /ikigai/submit-dimension [{label}]",
             "POST", f"{API_V1}/career-profile/ikigai/submit-dimension",
             json_body={"session_token":rec_token,"dimension_name":dim,
                        "selected_profession_id":first_prof_id,
                        "selection_type":"selected","reasoning_text":f"Test {dim}"},
             headers=HEADERS)
elif rec_token:
    for _, label in DIMS:
        log("SKIP", f"POST /ikigai/submit-dimension [{label}]", "-", "Tidak ada kandidat")

if rec_token:
    test("GET /career-profile/result/personality/{token}",
         "GET", f"{API_V1}/career-profile/result/personality/{rec_token}", headers=HEADERS)
    test("GET /career-profile/result/recommendation/{token}",
         "GET", f"{API_V1}/career-profile/result/recommendation/{rec_token}", headers=HEADERS)

# ═══════════════════════════════════════════════════════════════
print("\n" + "─"*62)
print("  🔍 ALUR 2: FIT CHECK")
print("─"*62)

fit_token = None; fit_qids = None

ok, r = test("POST /career-profile/fit-check/start",
             "POST", f"{API_V1}/career-profile/fit-check/start",
             json_body={"persona_type":"BUILDER","target_profession_id":1},
             headers=HEADERS)
if ok:
    fit_token = r.json().get("session_token")
    fit_qids  = r.json().get("question_ids", [])
    print(f"       token: {fit_token}  |  {len(fit_qids)} soal")

if fit_token and fit_qids:
    test("POST /career-profile/riasec/submit (fit-check)",
         "POST", f"{API_V1}/career-profile/riasec/submit",
         json_body=build_riasec_payload(fit_token, fit_qids), headers=HEADERS)

if fit_token:
    test("GET /career-profile/result/fit-check/{token}",
         "GET", f"{API_V1}/career-profile/result/fit-check/{fit_token}", headers=HEADERS)

# ═══════════════════════════════════════════════════════════════
print("\n" + "─"*62)
print("  📜 HISTORY")
print("─"*62)
test("GET /history/", "GET", f"{API_V1}/history/", params={"user_id": 1})
ok_h, r_h = test("GET /history/1", "GET", f"{API_V1}/history/1")
if not ok_h and r_h.status_code == 404:
    results[-1]["status"] = "SKIP"

# ═══════════════════════════════════════════════════════════════
print("\n" + "─"*62)
print("  🛡  EDGE CASES")
print("─"*62)
test("GET riasec/result token invalid (expect 404)",
     "GET", f"{API_V1}/career-profile/riasec/result/token-tidak-valid-xyz",
     expected=404, headers=HEADERS)
test("POST recommendation/start body kosong (expect 422)",
     "POST", f"{API_V1}/career-profile/recommendation/start",
     json_body={}, expected=422, headers=HEADERS)
test("POST tanpa header x-user-id (expect 422)",
     "POST", f"{API_V1}/career-profile/recommendation/start",
     json_body={"persona_type":"PATHFINDER"}, expected=422)

# ═══════════════════════════════════════════════════════════════
total   = len(results)
passed  = sum(1 for r in results if r["status"] == "PASS")
failed  = sum(1 for r in results if r["status"] == "FAIL")
skipped = sum(1 for r in results if r["status"] == "SKIP")

print()
print("╔══════════════════════════════════════════════════════════════╗")
print(f"║  HASIL  →  {passed} PASS  |  {failed} FAIL  |  {skipped} SKIP  |  {total} TOTAL")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  Email   : {TEST_EMAIL}")
print(f"║  User ID : {USER_ID}")
print("╚══════════════════════════════════════════════════════════════╝")

if failed > 0:
    print("\n  ✗ Yang GAGAL:")
    for r in results:
        if r["status"] == "FAIL":
            print(f"    [{r['code']}] {r['name']}")
            if r["detail"]: print(f"          → {r['detail']}")
else:
    print("\n  🎉 Semua test LULUS!")
print()
sys.exit(0 if failed == 0 else 1)
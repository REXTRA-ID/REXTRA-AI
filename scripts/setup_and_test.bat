@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

:: ============================================================
::  REXTRA-AI API - Setup & Test Runner
::  Jalankan file ini dari root folder project (kenali-diri-main)
:: ============================================================

title REXTRA-AI - Setup & Test Runner

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║        REXTRA-AI API - SETUP ^& TEST RUNNER           ║
echo ║           FastAPI Career Profile System                  ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: ─────────────────────────────────────────────
:: KONFIGURASI — Sesuaikan dengan environment kamu
:: ─────────────────────────────────────────────
set BASE_URL=http://localhost:8000
set PYTHON=python
set PIP=pip

:: User UUID yang akan dipakai untuk header X-User-Id
:: Ganti dengan UUID user yang sudah ada di DB setelah seeder dijalankan
set TEST_USER_ID=00000000-0000-0000-0000-000000000001

:: Target profesi untuk FIT_CHECK test (sesuaikan dengan data di DB)
set TARGET_PROFESSION_ID=1

:: ─────────────────────────────────────────────
:: CEK PYTHON
:: ─────────────────────────────────────────────
echo [1/7] Memeriksa instalasi Python...
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan! Pastikan Python sudah diinstall dan ada di PATH.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('%PYTHON% --version 2^>^&1') do echo       ✓ %%v
echo.

:: ─────────────────────────────────────────────
:: CEK .ENV FILE
:: ─────────────────────────────────────────────
echo [2/7] Memeriksa file konfigurasi .env...
if not exist ".env" (
    echo [WARNING] File .env tidak ditemukan!
    echo           Membuat .env dari template default...
    echo.
    (
        echo APP_NAME="REXTRA-AI API"
        echo APP_VERSION="0.1.0"
        echo DATABASE_URL=postgresql://user:password@localhost:5432/features
        echo REDIS_URL=redis://localhost:6379/0
        echo CELERY_BROKER_URL=redis://localhost:6379/1
        echo OPENROUTER_API_KEY=sk-or-v1-xxxxx
        echo OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
        echo OPENROUTER_MODEL=google/gemini-3.0-flash
        echo AI_MAX_TOKENS=2000
        echo AI_TEMPERATURE=0.7
        echo SECRET_KEY=dev-secret-key-change-in-production
        echo SENTRY_DSN=
        echo LOG_LEVEL=INFO
    ) > .env
    echo [INFO] File .env dibuat. HARAP EDIT .env dengan konfigurasi DB dan API key yang benar!
    echo        Tekan Enter untuk melanjutkan setelah mengedit .env...
    pause
) else (
    echo       ✓ File .env ditemukan
)
echo.

:: ─────────────────────────────────────────────
:: INSTALL DEPENDENCIES
:: ─────────────────────────────────────────────
echo [3/7] Menginstall dependencies Python...
echo       Menjalankan: pip install -r requirements.txt
echo.
%PIP% install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Gagal menginstall dependencies!
    pause
    exit /b 1
)
echo.
echo       ✓ Semua dependencies berhasil diinstall
echo.

:: ─────────────────────────────────────────────
:: CEK KONEKSI DATABASE & REDIS
:: ─────────────────────────────────────────────
echo [4/7] Memeriksa koneksi database dan Redis...
%PYTHON% -c "
import sys
try:
    from app.core.config import settings
    from sqlalchemy import create_engine, text
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('  [OK] Database PostgreSQL terhubung:', settings.DATABASE_URL.split('@')[-1])
except Exception as e:
    print('  [FAIL] Database gagal terhubung:', str(e))
    sys.exit(1)
"
if errorlevel 1 (
    echo.
    echo [ERROR] Koneksi database gagal!
    echo         Pastikan PostgreSQL berjalan dan konfigurasi DATABASE_URL di .env sudah benar.
    pause
    exit /b 1
)

%PYTHON% -c "
import sys
try:
    from app.core.config import settings
    import redis
    r = redis.from_url(settings.REDIS_URL)
    r.ping()
    print('  [OK] Redis terhubung:', settings.REDIS_URL)
except Exception as e:
    print('  [WARN] Redis gagal terhubung:', str(e))
    print('         Beberapa fitur caching mungkin tidak berfungsi')
"
echo.

:: ─────────────────────────────────────────────
:: JALANKAN MIGRASI ALEMBIC
:: ─────────────────────────────────────────────
echo [5/7] Menjalankan migrasi database (Alembic)...
%PYTHON% -m alembic upgrade head
if errorlevel 1 (
    echo [WARNING] Migrasi Alembic gagal atau sudah up-to-date
    echo           Melanjutkan...
) else (
    echo       ✓ Migrasi database selesai
)
echo.

:: ─────────────────────────────────────────────
:: JALANKAN SERVER di background + tunggu siap
:: ─────────────────────────────────────────────
echo [6/7] Menjalankan server FastAPI...
echo       Server akan berjalan di: %BASE_URL%
echo.

:: Jalankan server di background window baru
start "REXTRA-AI API Server" cmd /k "%PYTHON% -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: Tunggu server siap (coba setiap 2 detik, max 30 detik)
echo       Menunggu server siap...
set /a WAIT_COUNT=0
:WAIT_LOOP
timeout /t 2 /nobreak >nul
%PYTHON% -c "import urllib.request; urllib.request.urlopen('%BASE_URL%/health')" >nul 2>&1
if errorlevel 1 (
    set /a WAIT_COUNT+=1
    if !WAIT_COUNT! lss 15 (
        echo       ... menunggu (!WAIT_COUNT!x)
        goto WAIT_LOOP
    )
    echo [ERROR] Server tidak merespons setelah 30 detik!
    pause
    exit /b 1
)
echo       ✓ Server siap di %BASE_URL%
echo.

:: ─────────────────────────────────────────────
:: JALANKAN API TESTS
:: ─────────────────────────────────────────────
echo [7/7] Menjalankan pengujian semua API endpoint...
echo ════════════════════════════════════════════════════════════
echo.

%PYTHON% -c "
import urllib.request
import urllib.error
import json
import sys
import time

BASE_URL = '%BASE_URL%'
USER_ID  = '%TEST_USER_ID%'
TARGET_PROFESSION_ID = %TARGET_PROFESSION_ID%

PASS = 0
FAIL = 0
SKIP = 0
session_token_recommendation = None
session_token_fitcheck = None
riasec_question_ids = []

def make_request(method, path, body=None, headers=None):
    url = BASE_URL + path
    default_headers = {
        'Content-Type': 'application/json',
        'x-user-id': USER_ID
    }
    if headers:
        default_headers.update(headers)

    data = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=data, headers=default_headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body_text = resp.read().decode('utf-8')
            return resp.status, json.loads(body_text) if body_text else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode('utf-8')
        try:
            return e.code, json.loads(body_text)
        except:
            return e.code, {'raw': body_text}
    except Exception as e:
        return 0, {'error': str(e)}

def test(name, method, path, body=None, expected_status=200, headers=None, save_token_key=None):
    global PASS, FAIL, SKIP, session_token_recommendation, session_token_fitcheck
    status, resp = make_request(method, path, body, headers)
    ok = (status == expected_status) or (expected_status == 200 and status in [200, 201])
    icon = '✓' if ok else '✗'
    color_ok = ok
    print(f'  {icon} [{status}] {name}')
    if not ok:
        detail = resp.get('detail', resp.get('error', str(resp))[:80])
        print(f'       └─ Expected {expected_status}, got {status}: {detail}')
        FAIL += 1
    else:
        PASS += 1
        if save_token_key and isinstance(resp, dict):
            token = resp.get('session_token') or resp.get(save_token_key)
            if token and save_token_key == 'recommendation':
                session_token_recommendation = token
            elif token and save_token_key == 'fitcheck':
                session_token_fitcheck = token
    return ok, resp

# ── SYSTEM ENDPOINTS ──────────────────────────────────────
print('── SYSTEM ENDPOINTS ─────────────────────────────────────')
test('GET / (Root)',            'GET', '/')
test('GET /health',             'GET', '/health')
test('GET /api/v1/ (API Root)', 'GET', '/api/v1/')
test('GET /test-redis',         'GET', '/test-redis')
test('GET /metrics',            'GET', '/metrics')
test('GET /docs (Swagger UI)',  'GET', '/docs')
print()

# ── CATEGORIES ────────────────────────────────────────────
print('── CATEGORIES ───────────────────────────────────────────')
test('GET /categories/ (list semua kategori)', 'GET', '/api/v1/categories/', expected_status=200)
print()

# ── SESSION: RECOMMENDATION ───────────────────────────────
print('── SESSION - RECOMMENDATION ─────────────────────────────')
ok, resp = test(
    'POST /career-profile/recommendation/start',
    'POST', '/api/v1/career-profile/recommendation/start',
    body={'persona_type': 'PATHFINDER'},
    expected_status=200,
    save_token_key='recommendation'
)
if ok and isinstance(resp, dict):
    session_token_recommendation = resp.get('session_token')
    print(f'       └─ Session token (recommendation): {session_token_recommendation}')

# ── SESSION: FIT CHECK ────────────────────────────────────
print()
print('── SESSION - FIT CHECK ──────────────────────────────────')
ok2, resp2 = test(
    'POST /career-profile/fit-check/start',
    'POST', '/api/v1/career-profile/fit-check/start',
    body={
        'persona_type': 'EXPLORER',
        'target_profession_id': TARGET_PROFESSION_ID
    },
    expected_status=200,
    save_token_key='fitcheck'
)
if ok2 and isinstance(resp2, dict):
    session_token_fitcheck = resp2.get('session_token')
    print(f'       └─ Session token (fitcheck): {session_token_fitcheck}')

# ── RIASEC ────────────────────────────────────────────────
print()
print('── RIASEC ───────────────────────────────────────────────')

# Submit RIASEC (recommendation session)
if session_token_recommendation:
    # Buat payload 72 jawaban dummy (12 soal x 6 tipe RIASEC)
    responses = [{'question_id': i, 'answer_value': (i % 5) + 1} for i in range(1, 73)]
    test(
        'POST /riasec/submit (recommendation session)',
        'POST', '/api/v1/career-profile/riasec/submit',
        body={
            'session_token': session_token_recommendation,
            'responses': responses
        },
        expected_status=200
    )
    test(
        'GET /riasec/result/{session_token} (recommendation)',
        'GET', f'/api/v1/career-profile/riasec/result/{session_token_recommendation}'
    )
else:
    print('  - [SKIP] Submit RIASEC recommendation — tidak ada session token')
    SKIP += 2

# Submit RIASEC (fitcheck session)
if session_token_fitcheck:
    responses = [{'question_id': i, 'answer_value': (i % 5) + 1} for i in range(1, 73)]
    test(
        'POST /riasec/submit (fitcheck session)',
        'POST', '/api/v1/career-profile/riasec/submit',
        body={
            'session_token': session_token_fitcheck,
            'responses': responses
        },
        expected_status=200
    )
else:
    print('  - [SKIP] Submit RIASEC fitcheck — tidak ada session token')
    SKIP += 1

# ── IKIGAI ────────────────────────────────────────────────
print()
print('── IKIGAI ───────────────────────────────────────────────')

if session_token_recommendation:
    ok3, resp3 = test(
        'POST /ikigai/start',
        'POST', '/api/v1/career-profile/ikigai/start',
        body={'session_token': session_token_recommendation},
        expected_status=200
    )
    test(
        'GET /ikigai/content/{session_token}',
        'GET', f'/api/v1/career-profile/ikigai/content/{session_token_recommendation}'
    )

    # Ambil candidate profession dari response start ikigai
    if ok3 and isinstance(resp3, dict):
        candidates = resp3.get('candidates', [])
        if candidates:
            first_prof_id = candidates[0].get('profession_id') or candidates[0].get('id', 1)
            dimensions = ['love', 'good_at', 'world_needs', 'paid_for']
            for dim in dimensions:
                test(
                    f'POST /ikigai/submit-dimension ({dim})',
                    'POST', '/api/v1/career-profile/ikigai/submit-dimension',
                    body={
                        'session_token': session_token_recommendation,
                        'dimension_name': dim,
                        'selected_profession_id': first_prof_id,
                        'selection_type': 'CLICK',
                        'reasoning_text': f'Test reasoning untuk dimensi {dim}'
                    },
                    expected_status=200
                )
        else:
            print('  - [SKIP] Submit Ikigai dimensions — tidak ada candidates dari response')
            SKIP += 4
    else:
        print('  - [SKIP] Submit Ikigai dimensions — ikigai/start gagal')
        SKIP += 4
else:
    print('  - [SKIP] Seluruh flow Ikigai — tidak ada session recommendation')
    SKIP += 6

# ── RESULT ────────────────────────────────────────────────
print()
print('── RESULT ENDPOINTS ─────────────────────────────────────')

if session_token_recommendation:
    test(
        'GET /result/personality/{session_token}',
        'GET', f'/api/v1/career-profile/result/personality/{session_token_recommendation}'
    )
    test(
        'GET /result/recommendation/{session_token}',
        'GET', f'/api/v1/career-profile/result/recommendation/{session_token_recommendation}'
    )
else:
    print('  - [SKIP] Result endpoints — tidak ada session recommendation')
    SKIP += 2

if session_token_fitcheck:
    test(
        'GET /result/fit-check/{session_token}',
        'GET', f'/api/v1/career-profile/result/fit-check/{session_token_fitcheck}'
    )
else:
    print('  - [SKIP] Result fit-check — tidak ada session fitcheck')
    SKIP += 1

# ── HISTORY ───────────────────────────────────────────────
print()
print('── HISTORY ──────────────────────────────────────────────')
test(
    'GET /history/ (user_id=1)',
    'GET', f'/api/v1/history/?user_id=1'
)
test(
    'GET /history/1 (detail)',
    'GET', '/api/v1/history/1',
    expected_status=200  # bisa 404 jika belum ada data
)

# ── EDGE CASES ────────────────────────────────────────────
print()
print('── EDGE CASES / VALIDASI ────────────────────────────────')
test('GET /health (no auth)', 'GET', '/health',
     headers={'x-user-id': None}, expected_status=200)
test('GET invalid session token', 'GET',
     '/api/v1/career-profile/riasec/result/invalid-token-xyz',
     expected_status=404)
test('POST start session tanpa body', 'POST',
     '/api/v1/career-profile/recommendation/start',
     body={}, expected_status=422)

# ── SUMMARY ───────────────────────────────────────────────
print()
print('════════════════════════════════════════════════════════════')
print(f'  HASIL PENGUJIAN: {PASS} PASS  |  {FAIL} FAIL  |  {SKIP} SKIP')
print('════════════════════════════════════════════════════════════')
if FAIL == 0:
    print('  ✓ Semua endpoint yang diuji berhasil!')
else:
    print(f'  ✗ {FAIL} endpoint gagal. Periksa log server untuk detail.')
print()
if FAIL > 0:
    sys.exit(1)
"

set TEST_EXIT=%errorlevel%

echo.
echo ════════════════════════════════════════════════════════════
if %TEST_EXIT% == 0 (
    echo  ✓ Semua test LULUS! API berjalan dengan baik.
) else (
    echo  ✗ Beberapa test GAGAL. Periksa output di atas untuk detail.
    echo    Tips: Pastikan DB sudah ada data seed dan .env dikonfigurasi benar.
)
echo ════════════════════════════════════════════════════════════
echo.
echo  Server FastAPI masih berjalan di window terpisah.
echo  Buka %BASE_URL%/docs untuk Swagger UI.
echo  Tutup window "REXTRA-AI API Server" untuk menghentikan server.
echo.
pause
endlocal

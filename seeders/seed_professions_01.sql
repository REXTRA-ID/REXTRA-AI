-- =============================================================================
-- SEEDER PROFESI DIGITAL — BATCH 01 (Profesi #1–10)
-- Kategori: Backend Engineering & Cloud/DevOps
-- Prasyarat: profession_main_category_seeder & profession_sub_category_seeder
--            sudah dijalankan. riasec_codes sudah ada.
-- Idempotent: pakai INSERT ... ON CONFLICT DO NOTHING
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 0. HELPER: ambil ID kategori & riasec yang dipakai di batch ini
-- -----------------------------------------------------------------------------
-- main_category : ENGINEERING
-- sub_categories: BACKEND, CLOUD, DEVOPS
-- riasec_codes  : RI, R, IR, RC, I

-- -----------------------------------------------------------------------------
-- 1. SKILLS — insert skill baru, skip kalau sudah ada
-- -----------------------------------------------------------------------------
INSERT INTO skills (slug, name, created_at, updated_at) VALUES
  ('python',              'Python',               NOW(), NOW()),
  ('golang',              'Golang',               NOW(), NOW()),
  ('nodejs',              'Node.js',              NOW(), NOW()),
  ('java-spring',         'Java Spring Boot',     NOW(), NOW()),
  ('postgresql',          'PostgreSQL',           NOW(), NOW()),
  ('mysql',               'MySQL',                NOW(), NOW()),
  ('redis',               'Redis',                NOW(), NOW()),
  ('rest-api-design',     'REST API Design',      NOW(), NOW()),
  ('grpc',                'gRPC',                 NOW(), NOW()),
  ('microservices',       'Microservices',        NOW(), NOW()),
  ('system-design',       'System Design',        NOW(), NOW()),
  ('docker',              'Docker',               NOW(), NOW()),
  ('kubernetes',          'Kubernetes',           NOW(), NOW()),
  ('terraform',           'Terraform',            NOW(), NOW()),
  ('aws',                 'AWS',                  NOW(), NOW()),
  ('gcp',                 'GCP',                  NOW(), NOW()),
  ('linux-administration','Linux Administration', NOW(), NOW()),
  ('ci-cd',               'CI/CD Pipeline',       NOW(), NOW()),
  ('bash-scripting',      'Bash Scripting',       NOW(), NOW()),
  ('monitoring-observability', 'Monitoring & Observability', NOW(), NOW()),
  ('message-queue',       'Message Queue (Kafka/RabbitMQ)', NOW(), NOW()),
  ('database-optimization','Database Optimization', NOW(), NOW()),
  ('git',                 'Git & Version Control', NOW(), NOW()),
  ('agile',               'Agile / Scrum',        NOW(), NOW()),
  ('code-review',         'Code Review',          NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. TOOLS
-- -----------------------------------------------------------------------------
INSERT INTO tools (slug, name, created_at, updated_at) VALUES
  ('vscode',          'VS Code',              NOW(), NOW()),
  ('postman',         'Postman',              NOW(), NOW()),
  ('datagrip',        'DataGrip',             NOW(), NOW()),
  ('intellij',        'IntelliJ IDEA',        NOW(), NOW()),
  ('github-actions',  'GitHub Actions',       NOW(), NOW()),
  ('gitlab-ci',       'GitLab CI',            NOW(), NOW()),
  ('jenkins',         'Jenkins',              NOW(), NOW()),
  ('aws-console',     'AWS Console',          NOW(), NOW()),
  ('gcp-console',     'GCP Console',          NOW(), NOW()),
  ('terraform-cloud', 'Terraform Cloud',      NOW(), NOW()),
  ('grafana',         'Grafana',              NOW(), NOW()),
  ('prometheus',      'Prometheus',           NOW(), NOW()),
  ('datadog',         'Datadog',              NOW(), NOW()),
  ('sentry',          'Sentry',               NOW(), NOW()),
  ('notion',          'Notion',               NOW(), NOW()),
  ('jira',            'Jira',                 NOW(), NOW()),
  ('confluence',      'Confluence',           NOW(), NOW()),
  ('slack',           'Slack',                NOW(), NOW()),
  ('pagerduty',       'PagerDuty',            NOW(), NOW()),
  ('k9s',             'k9s (Kubernetes CLI)', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 3. PROFESI #1–10
-- Menggunakan subquery untuk resolve FK (main_category, sub_category, riasec_code)
-- agar tidak hardcode ID yang berbeda-beda tiap environment.
-- -----------------------------------------------------------------------------

-- ── #1: Backend Engineer ─────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'backend-engineer',
    'Backend Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Backend Engineer membangun dan memelihara sistem sisi server — API, logika bisnis, database, dan integrasi layanan. Mereka adalah fondasi teknis yang memungkinkan produk digital berjalan cepat, aman, dan scalable untuk jutaan pengguna.',
    'Profesi ini cocok untuk tipe RI (Realistic-Investigative) karena menggabungkan pekerjaan hands-on teknis dengan analisis mendalam terhadap arsitektur dan performa sistem.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan membangun REST API atau gRPC service yang performant dan maintainable'),
  (2, 'Mendesain skema database dan mengoptimalkan query untuk performa tinggi'),
  (3, 'Mengimplementasikan logika bisnis yang kompleks dengan test coverage yang memadai'),
  (4, 'Mereview kode rekan tim dan memastikan standar arsitektur diterapkan konsisten'),
  (5, 'Mendiagnosis dan memperbaiki bug produksi termasuk memory leak dan race condition'),
  (6, 'Berkolaborasi dengan frontend engineer untuk mendefinisikan kontrak API')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('python','golang','postgresql','rest-api-design','microservices','system-design','redis','message-queue','database-optimization','git','agile','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('vscode','postman','datagrip','github-actions','sentry','jira','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Backend Engineer',    6000000,  12000000),
  (2, 'Mid Backend Engineer',      12000000,  22000000),
  (3, 'Senior Backend Engineer',   22000000,  40000000),
  (4, 'Staff/Principal Engineer',  40000000,  70000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Permintaan Backend Engineer di Indonesia tumbuh 35% YoY seiring ekspansi fintech dan e-commerce.'),
  (2, 'Golang dan Rust semakin populer sebagai alternatif Python/Java untuk sistem high-throughput.'),
  (3, 'Spesialisasi di distributed systems atau database internals membuka peluang kompensasi premium.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #2: Cloud Infrastructure Engineer ────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'cloud-infrastructure-engineer',
    'Cloud Infrastructure Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'CLOUD'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'R'),
    'Cloud Infrastructure Engineer mengelola dan mengoptimalkan seluruh lapisan infrastruktur cloud — dari compute dan storage hingga networking dan security. Mereka memastikan sistem produksi berjalan reliabel, efisien biaya, dan siap scale kapanpun dibutuhkan.',
    'Profesi ini cocok untuk tipe R (Realistic) karena pekerjaan sangat hands-on: mengelola server, jaringan, dan sistem nyata yang berjalan di cloud meskipun secara virtual.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan mengimplementasikan arsitektur cloud yang scalable dan cost-efficient'),
  (2, 'Mengelola infrastructure as code menggunakan Terraform atau Pulumi'),
  (3, 'Memantau kesehatan sistem dan merespons incident produksi dengan cepat'),
  (4, 'Mengoptimalkan biaya cloud melalui right-sizing dan reserved instance management'),
  (5, 'Mendesain disaster recovery plan dan menguji prosedur failover secara berkala'),
  (6, 'Memastikan kepatuhan keamanan cloud sesuai standar SOC2 atau ISO 27001')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'cloud-infrastructure-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('aws','gcp','terraform','kubernetes','docker','linux-administration','bash-scripting','monitoring-observability','ci-cd','python','system-design')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'cloud-infrastructure-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('aws-console','gcp-console','terraform-cloud','grafana','prometheus','datadog','pagerduty','k9s','github-actions','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'cloud-infrastructure-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Cloud Engineer',       7000000,  13000000),
  (2, 'Cloud Engineer',             13000000,  25000000),
  (3, 'Senior Cloud Engineer',      25000000,  45000000),
  (4, 'Cloud Architect',            45000000,  80000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'cloud-infrastructure-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Migrasi cloud di perusahaan enterprise Indonesia meningkat pesat pasca pandemi.'),
  (2, 'Sertifikasi AWS Solutions Architect dan GCP Professional Cloud Architect sangat dihargai.'),
  (3, 'FinOps (cloud cost optimization) menjadi spesialisasi baru yang dicari banyak perusahaan.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #3: DevOps Platform Engineer ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'devops-platform-engineer',
    'DevOps Platform Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'DEVOPS'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RC'),
    'DevOps Platform Engineer membangun dan memelihara platform internal yang memungkinkan tim engineering bekerja lebih cepat dan reliabel. Mereka mengelola CI/CD pipeline, developer tooling, dan standar deployment agar setiap rilis ke produksi aman dan konsisten.',
    'Profil RC (Realistic-Conventional) cocok karena pekerjaan ini menggabungkan implementasi teknis hands-on dengan penerapan standar dan prosedur yang ketat untuk deployment dan operasi sistem.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun dan mengoptimalkan CI/CD pipeline untuk ratusan service di monorepo atau microservices'),
  (2, 'Merancang internal developer platform yang mempercepat onboarding dan deployment tim engineering'),
  (3, 'Menstandarisasi container image, deployment manifest, dan runbook operasional'),
  (4, 'Mengelola secret management dan access control untuk environment produksi'),
  (5, 'Melakukan post-mortem setelah incident dan mengimplementasikan perbaikan sistemik'),
  (6, 'Berkolaborasi dengan security team untuk memastikan supply chain keamanan software')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'devops-platform-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('ci-cd','kubernetes','docker','terraform','bash-scripting','python','linux-administration','monitoring-observability','aws','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'devops-platform-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('github-actions','gitlab-ci','jenkins','grafana','prometheus','datadog','pagerduty','k9s','terraform-cloud','jira')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'devops-platform-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior DevOps Engineer',      7000000,  14000000),
  (2, 'DevOps Engineer',            14000000,  26000000),
  (3, 'Senior DevOps Engineer',     26000000,  45000000),
  (4, 'Platform Engineering Lead',  45000000,  75000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'devops-platform-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Platform Engineering menjadi tren besar di 2024–2025 seiring makin banyak perusahaan adopsi Internal Developer Platform.'),
  (2, 'GitOps dan ArgoCD semakin menjadi standar deployment di perusahaan yang serius dengan Kubernetes.'),
  (3, 'Kombinasi DevOps + Security (DevSecOps) menjadi diferensiasi utama yang dicari perusahaan fintech.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #4: Backend Systems Architect ────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'backend-systems-architect',
    'Backend Systems Architect',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IR'),
    'Backend Systems Architect merancang arsitektur sistem backend yang kompleks — menentukan bagaimana service berkomunikasi, data mengalir, dan sistem tetap resilient di skala besar. Mereka adalah technical leader yang keputusannya berdampak jangka panjang.',
    'Profil IR (Investigative-Realistic) cocok karena peran ini membutuhkan investigasi mendalam terhadap trade-off teknis sekaligus implementasi nyata dari arsitektur yang dirancang.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang arsitektur sistem untuk produk yang perlu scale ke puluhan juta pengguna'),
  (2, 'Mendefinisikan architectural decision record (ADR) dan memastikan adopsi oleh tim'),
  (3, 'Mengevaluasi dan memilih teknologi baru yang masuk dalam tech stack perusahaan'),
  (4, 'Melakukan architecture review dan mentoring senior engineer dalam keputusan desain'),
  (5, 'Merancang strategy untuk migrasi sistem legacy ke arsitektur modern'),
  (6, 'Berkolaborasi dengan CTO dan VP Engineering untuk menyelaraskan arsitektur dengan strategi bisnis')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-systems-architect')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('system-design','microservices','message-queue','grpc','rest-api-design','postgresql','redis','golang','python','monitoring-observability','database-optimization','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-systems-architect')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('datagrip','grafana','datadog','confluence','notion','jira','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-systems-architect')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Senior Backend Engineer',    22000000,  40000000),
  (2, 'Staff Engineer',             40000000,  65000000),
  (3, 'Principal Engineer',         65000000,  100000000),
  (4, 'Distinguished Engineer/CTO', 100000000, 200000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'backend-systems-architect')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Peran architect semakin dicari seiring perusahaan digital Indonesia tumbuh ke fase scaling.'),
  (2, 'Domain-Driven Design (DDD) dan Event Sourcing menjadi skill diferensiasi yang sangat dihargai.'),
  (3, 'Kandidat dengan pengalaman handle sistem >10 juta DAU sangat langka dan kompensasinya premium.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #5: Site Reliability Engineer (SRE) ──────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'site-reliability-engineer',
    'Site Reliability Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'DEVOPS'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Site Reliability Engineer (SRE) menggabungkan software engineering dengan operasi sistem untuk memastikan produk berjalan reliabel di skala besar. Mereka mendefinisikan SLO, mengelola error budget, dan membangun sistem yang self-healing.',
    'Profil RI cocok karena SRE melakukan pekerjaan hands-on engineering yang intens (Realistic) sekaligus investigasi mendalam terhadap pola kegagalan sistem dan cara pencegahannya (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mendefinisikan SLI, SLO, dan error budget untuk setiap critical service'),
  (2, 'Membangun sistem monitoring, alerting, dan auto-remediation untuk produksi'),
  (3, 'Melakukan chaos engineering untuk menemukan titik lemah sistem sebelum incident nyata'),
  (4, 'Menulis runbook dan memimpin incident response ketika terjadi outage produksi'),
  (5, 'Mengotomasi toil operasional yang berulang menggunakan scripting dan tooling internal'),
  (6, 'Berkolaborasi dengan tim engineering untuk mereview arsitektur dari perspektif reliability')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'site-reliability-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('monitoring-observability','kubernetes','python','bash-scripting','linux-administration','system-design','ci-cd','aws','gcp','golang','database-optimization')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'site-reliability-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('grafana','prometheus','datadog','pagerduty','k9s','aws-console','github-actions','sentry','slack','jira')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'site-reliability-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior SRE',      8000000,  15000000),
  (2, 'SRE',            15000000,  28000000),
  (3, 'Senior SRE',     28000000,  50000000),
  (4, 'SRE Tech Lead',  50000000,  80000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'site-reliability-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'SRE menjadi peran kritis di startup yang sudah memasuki fase growth dan tidak boleh down.'),
  (2, 'OpenTelemetry menjadi standar observability baru yang menggantikan solusi proprietary.'),
  (3, 'Pengalaman mengelola sistem dengan 99.99% SLA sangat dihargai di fintech dan healthtech.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #6: Web Backend Developer ────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'web-backend-developer',
    'Web Backend Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Web Backend Developer membangun logika server-side untuk aplikasi web — dari autentikasi dan otorisasi hingga integrasi payment gateway dan notifikasi. Mereka bekerja erat dengan frontend developer untuk memastikan API yang dihasilkan mudah dikonsumsi.',
    'Profil RI cocok karena developer backend web melakukan implementasi teknis nyata (Realistic) sekaligus perlu berpikir analitis dalam merancang alur data dan keamanan sistem (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun endpoint API yang aman, terdokumentasi, dan mudah dikonsumsi frontend'),
  (2, 'Mengimplementasikan sistem autentikasi dan otorisasi (OAuth2, JWT, RBAC)'),
  (3, 'Mengintegrasikan layanan pihak ketiga seperti payment gateway, email, dan SMS'),
  (4, 'Menulis unit test dan integration test untuk menjaga kualitas kode'),
  (5, 'Mengoptimalkan query database dan menerapkan caching untuk halaman yang berat'),
  (6, 'Mendokumentasikan API menggunakan OpenAPI/Swagger agar mudah digunakan tim frontend')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web-backend-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('nodejs','python','java-spring','postgresql','mysql','redis','rest-api-design','git','agile','code-review','database-optimization')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web-backend-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('vscode','postman','datagrip','github-actions','sentry','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web-backend-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Backend Developer',   5000000,  10000000),
  (2, 'Backend Developer',         10000000,  20000000),
  (3, 'Senior Backend Developer',  20000000,  35000000),
  (4, 'Lead Backend Developer',    35000000,  60000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web-backend-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Node.js dan Python (FastAPI/Django) mendominasi stack backend startup Indonesia saat ini.'),
  (2, 'Pemahaman keamanan aplikasi web (OWASP Top 10) menjadi differentiator penting.'),
  (3, 'Banyak perusahaan mencari backend developer yang juga bisa handle deployment dasar di cloud.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #7: Mobile Android Developer ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'mobile-android-developer',
    'Mobile Android Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'MOBILE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'R'),
    'Mobile Android Developer membangun aplikasi native Android menggunakan Kotlin dan Jetpack. Mereka memastikan aplikasi berjalan mulus di ratusan jenis perangkat Android, performant, dan memberikan pengalaman pengguna yang konsisten di berbagai ukuran layar.',
    'Profil R (Realistic) cocok karena pekerjaan ini sangat hands-on: coding, debugging di device nyata, mengoptimalkan performa yang terasa langsung oleh pengguna di perangkat fisik.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengembangkan fitur baru menggunakan Kotlin dan Android Jetpack Compose'),
  (2, 'Mengintegrasikan REST API backend dan mengelola state aplikasi dengan ViewModel/Flow'),
  (3, 'Mengoptimalkan performa aplikasi: startup time, rendering, dan memory usage'),
  (4, 'Menulis unit test dan UI test dengan JUnit dan Espresso'),
  (5, 'Memastikan kompatibilitas di berbagai versi Android dan ukuran layar'),
  (6, 'Berkolaborasi dengan designer untuk mengimplementasikan design system yang konsisten')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-android-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('rest-api-design','git','agile','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-android-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('github-actions','sentry','jira','slack','notion','intellij')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-android-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Android Developer',   5000000,  10000000),
  (2, 'Android Developer',         10000000,  20000000),
  (3, 'Senior Android Developer',  20000000,  35000000),
  (4, 'Lead Mobile Engineer',      35000000,  60000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-android-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Indonesia adalah salah satu pasar Android terbesar dunia — permintaan Android dev tetap tinggi.'),
  (2, 'Jetpack Compose semakin menggantikan XML layout sebagai standar UI development Android.'),
  (3, 'Pengalaman dengan deep link, push notification, dan payment SDK sangat dicari startup e-commerce.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #8: Mobile iOS Developer ──────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'mobile-ios-developer',
    'Mobile iOS Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'MOBILE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'R'),
    'Mobile iOS Developer membangun aplikasi native iOS menggunakan Swift dan SwiftUI. Mereka bekerja di ekosistem Apple yang ketat dengan standar kualitas tinggi, memastikan aplikasi berjalan optimal di iPhone dan iPad dengan pengalaman yang terasa premium.',
    'Profil R cocok karena pengembangan iOS sangat teknis dan hands-on — dari coding Swift hingga profiling di Xcode dan testing langsung di device fisik Apple.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengembangkan fitur baru menggunakan Swift dan SwiftUI atau UIKit'),
  (2, 'Mengintegrasikan API backend dengan URLSession atau Alamofire'),
  (3, 'Mengoptimalkan performa dan battery usage aplikasi menggunakan Xcode Instruments'),
  (4, 'Memastikan aplikasi memenuhi guideline App Store Review sebelum submission'),
  (5, 'Menulis unit test dan snapshot test dengan XCTest'),
  (6, 'Berkolaborasi dengan backend team untuk mendefinisikan kontrak API dan data model')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-ios-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('rest-api-design','git','agile','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-ios-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('github-actions','sentry','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-ios-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior iOS Developer',    6000000,  12000000),
  (2, 'iOS Developer',          12000000,  22000000),
  (3, 'Senior iOS Developer',   22000000,  38000000),
  (4, 'Lead Mobile Engineer',   38000000,  65000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'mobile-ios-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'iOS developer lebih langka dari Android di Indonesia — supply terbatas membuat kompensasi lebih tinggi.'),
  (2, 'SwiftUI dan Swift Concurrency (async/await) menjadi skill wajib untuk iOS developer modern.'),
  (3, 'Pengalaman implementasi Apple Pay, Sign in with Apple, dan HealthKit membuka peluang di fintech/healthtech.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #9: Flutter Mobile Developer ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'flutter-mobile-developer',
    'Flutter Mobile Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'MOBILE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Flutter Mobile Developer membangun aplikasi cross-platform menggunakan Flutter dan Dart yang berjalan di Android, iOS, dan Web dari satu codebase. Pilihan populer di startup yang ingin ship lebih cepat tanpa mengorbankan performa atau tampilan.',
    'Profil RI cocok karena Flutter dev perlu hands-on engineering yang kuat (Realistic) sekaligus investigasi performa rendering dan state management yang kompleks (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun UI responsif menggunakan Flutter Widget tree dan custom painter'),
  (2, 'Mengelola state aplikasi menggunakan BLoC, Riverpod, atau Provider'),
  (3, 'Mengintegrasikan native Android/iOS functionality melalui platform channel'),
  (4, 'Mengoptimalkan performa rendering dan ukuran bundle aplikasi'),
  (5, 'Menulis widget test dan integration test untuk alur kritis aplikasi'),
  (6, 'Berkolaborasi dengan designer untuk mengimplementasikan design token dan component library')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'flutter-mobile-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('rest-api-design','git','agile','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'flutter-mobile-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('vscode','github-actions','sentry','jira','slack','notion','firebase')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'flutter-mobile-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Flutter Developer',   5000000,  10000000),
  (2, 'Flutter Developer',         10000000,  20000000),
  (3, 'Senior Flutter Developer',  20000000,  35000000),
  (4, 'Lead Flutter Developer',    35000000,  55000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'flutter-mobile-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Flutter menjadi pilihan utama startup Indonesia yang ingin ship ke Android dan iOS sekaligus.'),
  (2, 'Flutter 3.x dengan Impeller rendering engine memberikan performa yang makin mendekati native.'),
  (3, 'Demand Flutter developer meningkat signifikan di e-commerce dan super app Indonesia.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #10: Security Engineer ────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'security-engineer',
    'Security Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'SECURITY'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IR'),
    'Security Engineer melindungi sistem dan data perusahaan dari ancaman siber. Mereka melakukan penetration testing, security review kode, dan membangun tooling untuk mendeteksi serta merespons insiden keamanan sebelum berdampak ke pengguna.',
    'Profil IR cocok karena security engineering membutuhkan investigasi mendalam (Investigative) terhadap celah keamanan sekaligus implementasi teknis nyata dari sistem pertahanan (Realistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Melakukan penetration testing dan vulnerability assessment pada aplikasi web dan mobile'),
  (2, 'Mereview kode dari perspektif keamanan dan mengidentifikasi potensi OWASP Top 10'),
  (3, 'Membangun dan mengelola SIEM untuk monitoring ancaman keamanan secara real-time'),
  (4, 'Merancang security architecture dan memastikan enkripsi data at-rest dan in-transit'),
  (5, 'Merespons dan memimpin investigasi insiden keamanan (security incident response)'),
  (6, 'Mengedukasi tim engineering tentang secure coding practices dan threat modeling')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('linux-administration','python','bash-scripting','aws','kubernetes','monitoring-observability','system-design','git')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('datadog','grafana','pagerduty','jira','slack','confluence')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Security Engineer',   7000000,  14000000),
  (2, 'Security Engineer',         14000000,  28000000),
  (3, 'Senior Security Engineer',  28000000,  50000000),
  (4, 'Security Architect/CISO',   50000000,  100000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Regulasi keamanan siber (PDPA) mendorong perusahaan Indonesia merekrut security engineer lebih agresif.'),
  (2, 'Sertifikasi OSCP, CEH, dan CISSP sangat meningkatkan nilai pasar security engineer.'),
  (3, 'Security engineer dengan spesialisasi cloud security (AWS Security Specialty) sangat langka dan bergaji premium.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

COMMIT;

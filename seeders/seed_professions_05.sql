-- =============================================================================
-- SEEDER PROFESI DIGITAL — BATCH 05 (Profesi #41–50)
-- Kategori: Finance Tech, People & Culture, Operations, Emerging Digital Roles
-- Prasyarat: batch 01-04 sudah dijalankan
-- Idempotent: pakai INSERT ... ON CONFLICT DO NOTHING
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. SKILLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO skills (slug, name, created_at, updated_at) VALUES
  ('financial-analysis',     'Financial Analysis',               NOW(), NOW()),
  ('startup-finance',        'Startup Finance & Unit Economics',  NOW(), NOW()),
  ('tax-compliance',         'Tax & Compliance',                 NOW(), NOW()),
  ('people-ops',             'People Operations',                NOW(), NOW()),
  ('talent-acquisition',     'Talent Acquisition',               NOW(), NOW()),
  ('employer-branding',      'Employer Branding',                NOW(), NOW()),
  ('performance-management', 'Performance Management',           NOW(), NOW()),
  ('learning-development',   'Learning & Development',           NOW(), NOW()),
  ('operations-management',  'Operations Management',            NOW(), NOW()),
  ('process-improvement',    'Process Improvement',              NOW(), NOW()),
  ('customer-success',       'Customer Success',                 NOW(), NOW()),
  ('onboarding-management',  'Onboarding Management',            NOW(), NOW()),
  ('game-development',       'Game Development',                 NOW(), NOW()),
  ('unity-unreal',           'Unity / Unreal Engine',            NOW(), NOW()),
  ('blockchain',             'Blockchain & Web3',                NOW(), NOW()),
  ('smart-contracts',        'Smart Contracts (Solidity)',        NOW(), NOW()),
  ('ar-vr-development',      'AR/VR Development',                NOW(), NOW()),
  ('iot-development',        'IoT Development',                  NOW(), NOW()),
  ('embedded-systems',       'Embedded Systems',                 NOW(), NOW()),
  ('network-engineering',    'Network Engineering',              NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. TOOLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO tools (slug, name, created_at, updated_at) VALUES
  ('quickbooks',    'QuickBooks',               NOW(), NOW()),
  ('xero',          'Xero',                     NOW(), NOW()),
  ('workday',       'Workday',                  NOW(), NOW()),
  ('bamboohr',      'BambooHR',                 NOW(), NOW()),
  ('greenhouse',    'Greenhouse',               NOW(), NOW()),
  ('lever',         'Lever',                    NOW(), NOW()),
  ('lattice',       'Lattice',                  NOW(), NOW()),
  ('culture-amp',   'Culture Amp',              NOW(), NOW()),
  ('zendesk',       'Zendesk',                  NOW(), NOW()),
  ('freshdesk',     'Freshdesk',                NOW(), NOW()),
  ('unity',         'Unity',                    NOW(), NOW()),
  ('unreal',        'Unreal Engine',            NOW(), NOW()),
  ('blender',       'Blender',                  NOW(), NOW()),
  ('hardhat',       'Hardhat',                  NOW(), NOW()),
  ('metamask',      'MetaMask',                 NOW(), NOW()),
  ('arduino',       'Arduino',                  NOW(), NOW()),
  ('raspberry-pi',  'Raspberry Pi',             NOW(), NOW()),
  ('wireshark',     'Wireshark',                NOW(), NOW()),
  ('cisco-packet',  'Cisco Packet Tracer',      NOW(), NOW()),
  ('retool',        'Retool',                   NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- PROFESI #41–50
-- -----------------------------------------------------------------------------

-- ── #41: Startup Finance Manager ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'startup-finance-manager', 'Startup Finance Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'FINANCE'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'CE'),
    'Startup Finance Manager mengelola kesehatan finansial perusahaan teknologi — dari cash flow, financial modeling, hingga persiapan fundraising. Mereka membantu founder membuat keputusan berbasis angka dan memastikan runway perusahaan cukup untuk mencapai milestone berikutnya.',
    'Profil CE cocok karena Finance Manager membutuhkan ketelitian dan kepatuhan prosedur (Conventional) sekaligus inisiatif untuk mendorong keputusan finansial yang mengoptimalkan pertumbuhan (Enterprising).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun dan memelihara financial model untuk proyeksi revenue, burn rate, dan runway'),
  (2, 'Mengelola cash flow dan memastikan likuiditas perusahaan cukup untuk operasional'),
  (3, 'Menyiapkan laporan keuangan bulanan untuk board dan investor'),
  (4, 'Berkolaborasi dengan founder untuk mempersiapkan data room fundraising'),
  (5, 'Mengelola kepatuhan pajak dan regulasi keuangan yang berlaku'),
  (6, 'Menganalisis unit economics produk dan memberikan rekomendasi optimasi')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'startup-finance-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('financial-analysis','startup-finance','financial-modeling','tax-compliance','sql-advanced','statistics','stakeholder-management')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'startup-finance-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('xero','quickbooks','notion','slack','pitch','bigquery','metabase','airtable','zoom')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'startup-finance-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Finance Analyst',7000000,14000000),(2,'Finance Manager',14000000,28000000),(3,'Senior Finance Manager',28000000,50000000),(4,'CFO / VP Finance',50000000,120000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'startup-finance-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Finance yang paham SaaS metrics (ARR, MRR, churn) sangat dicari startup Indonesia.'),(2,'Kemampuan membangun financial model di Excel/Google Sheets adalah baseline minimum.'),(3,'CFO dengan track record sukses fundraising Series A/B sangat bernilai di ekosistem startup.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #42: People & Culture Manager ────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'people-culture-manager', 'People & Culture Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'PEOPLE'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'SE'),
    'People & Culture Manager memastikan perusahaan teknologi punya orang-orang yang tepat, di posisi yang tepat, dengan budaya kerja yang mendukung mereka tumbuh dan berkontribusi maksimal. Mereka mengelola talent acquisition, performance management, dan employee experience.',
    'Profil SE cocok karena People Manager harus empatis dan berorientasi pada pengembangan manusia (Social) sekaligus punya inisiatif dalam membangun sistem dan program yang mendorong pertumbuhan organisasi (Enterprising).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan menjalankan proses rekrutmen yang efisien untuk peran teknis dan non-teknis'),
  (2, 'Membangun program onboarding yang memastikan karyawan baru produktif sejak hari pertama'),
  (3, 'Mengelola performance review cycle dan memastikan feedback yang konstruktif dan adil'),
  (4, 'Merancang program learning & development yang sesuai dengan kebutuhan tim'),
  (5, 'Membangun dan menjaga budaya perusahaan yang selaras dengan nilai-nilai organisasi'),
  (6, 'Menganalisis employee engagement data dan mengeksekusi program retensi talenta')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'people-culture-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('people-ops','talent-acquisition','employer-branding','performance-management','learning-development','stakeholder-management','agile','product-analytics')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'people-culture-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('workday','bamboohr','greenhouse','lever','lattice','culture-amp','notion','slack','zoom','airtable')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'people-culture-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'HR Generalist',6000000,12000000),(2,'People Manager',12000000,22000000),(3,'Senior People Manager',22000000,38000000),(4,'VP People / Chief People Officer',38000000,80000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'people-culture-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'People yang bisa recruit engineer dengan cepat adalah aset sangat berharga di startup.'),(2,'Data-driven HR (people analytics) menjadi tren besar — HR yang bisa baca data lebih efektif.'),(3,'Employer branding menjadi kompetitif — perusahaan yang punya culture kuat lebih mudah rekrut talenta top.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #43: Tech Talent Recruiter ────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'tech-talent-recruiter', 'Tech Talent Recruiter',
    (SELECT id FROM profession_main_categories WHERE code = 'PEOPLE'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'ES'),
    'Tech Talent Recruiter spesialisasi dalam mencari dan menarik engineer, data scientist, dan profesional teknologi terbaik. Mereka memahami technical stack, bisa mengevaluasi profil GitHub, dan tahu cara meyakinkan kandidat pasif untuk bergabung.',
    'Profil ES cocok karena Tech Recruiter harus punya drive tinggi untuk memenuhi hiring target (Enterprising) sekaligus kemampuan membangun hubungan dengan kandidat dan hiring manager (Social).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Melakukan sourcing kandidat teknis melalui LinkedIn, GitHub, dan komunitas developer'),
  (2, 'Melakukan screening awal untuk memvalidasi technical fit dan culture fit'),
  (3, 'Berkolaborasi dengan hiring manager untuk mendefinisikan job requirement yang tepat'),
  (4, 'Mengelola candidate pipeline dan memastikan candidate experience yang positif'),
  (5, 'Membangun talent pool untuk peran teknis yang sering dibutuhkan'),
  (6, 'Menganalisis recruitment metrics (time-to-hire, offer acceptance rate) untuk optimasi proses')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-talent-recruiter')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('talent-acquisition','employer-branding','stakeholder-management','public-speaking','community-building','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-talent-recruiter')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('greenhouse','lever','bamboohr','notion','slack','zoom','linkedin','airtable')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-talent-recruiter')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Tech Recruiter',6000000,12000000),(2,'Senior Tech Recruiter',12000000,22000000),(3,'Lead Tech Recruiter',22000000,35000000),(4,'Head of Talent Acquisition',35000000,65000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-talent-recruiter')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Tech recruiter yang bisa baca kode dan profile GitHub jauh lebih efektif dari recruiter generalis.'),(2,'Perang talenta engineering di Indonesia masih sangat ketat — recruiter yang cepat punya keunggulan.'),(3,'Recruiter yang membangun personal brand di komunitas tech mendapat akses ke kandidat pasif lebih mudah.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #44: Customer Success Manager (Tech) ─────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'customer-success-manager-tech', 'Customer Success Manager (Tech)',
    (SELECT id FROM profession_main_categories WHERE code = 'OPERATIONS'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'SE'),
    'Customer Success Manager di perusahaan teknologi memastikan pelanggan mendapatkan value maksimal dari produk. Mereka mengelola onboarding, adoption, dan renewal — dan menjadi suara pelanggan yang paling kuat di dalam perusahaan.',
    'Profil SE cocok karena CSM harus empatis dan berorientasi membantu pelanggan sukses (Social) sekaligus punya inisiatif proaktif dalam mengidentifikasi peluang upsell dan ekspansi (Enterprising).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengelola onboarding pelanggan baru agar bisa menggunakan produk secara efektif'),
  (2, 'Melakukan regular business review dengan pelanggan untuk memastikan value terealisasi'),
  (3, 'Mengidentifikasi tanda-tanda churn risk dan melakukan intervensi proaktif'),
  (4, 'Berkolaborasi dengan sales untuk mengidentifikasi peluang upsell dan cross-sell'),
  (5, 'Mengumpulkan feedback produk dari pelanggan dan menyampaikan ke tim produk'),
  (6, 'Membangun playbook onboarding dan success metric yang scalable untuk seluruh tim CSM')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'customer-success-manager-tech')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('customer-success','onboarding-management','stakeholder-management','product-analytics','sql-advanced','agile','public-speaking')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'customer-success-manager-tech')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('zendesk','freshdesk','hubspot','intercom','salesforce','notion','slack','zoom','amplitude','loom')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'customer-success-manager-tech')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Customer Success Associate',7000000,13000000),(2,'Customer Success Manager',13000000,24000000),(3,'Senior CSM',24000000,40000000),(4,'Head of Customer Success',40000000,75000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'customer-success-manager-tech')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Churn prevention menjadi prioritas utama SaaS Indonesia yang sudah melewati fase growth.'),(2,'CSM yang bisa analisis product usage data sendiri jauh lebih efektif dalam proactive outreach.'),(3,'PLG (Product-Led Growth) menciptakan peran CSM baru yang fokus pada digital-touch engagement.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #45: Digital Operations Manager ──────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'digital-operations-manager', 'Digital Operations Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'OPERATIONS'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'EC'),
    'Digital Operations Manager memastikan mesin operasional perusahaan digital berjalan efisien. Mereka mengoptimalkan proses bisnis, mengelola vendor dan tooling, dan memastikan setiap divisi punya sistem yang mendukung mereka bekerja dengan produktivitas maksimal.',
    'Profil EC cocok karena Ops Manager harus punya drive untuk mengeksekusi dan mengoptimalkan (Enterprising) sekaligus kecermatan dalam membangun dan menjaga sistem dan prosedur (Conventional).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Memetakan dan mengoptimalkan proses bisnis di seluruh divisi untuk menghilangkan inefisiensi'),
  (2, 'Mengelola stack tooling perusahaan dan memastikan integrasi antar sistem berjalan lancar'),
  (3, 'Membangun dashboard operasional untuk monitoring KPI real-time lintas departemen'),
  (4, 'Mengelola vendor dan kontrak layanan untuk memastikan nilai terbaik bagi perusahaan'),
  (5, 'Memimpin inisiatif otomasi proses untuk mengurangi manual work di seluruh tim'),
  (6, 'Berkolaborasi dengan leadership untuk merencanakan kapasitas dan sumber daya operasional')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-operations-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('operations-management','process-improvement','project-management','product-analytics','sql-advanced','stakeholder-management','agile','financial-modeling')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-operations-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('notion','jira','airtable','clickup','retool','metabase','slack','zoom','asana','coda')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-operations-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Operations Specialist',7000000,13000000),(2,'Operations Manager',13000000,25000000),(3,'Senior Operations Manager',25000000,42000000),(4,'VP Operations / COO',42000000,90000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-operations-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Ops yang bisa coding automation sederhana (Zapier, n8n, Python) sangat meningkatkan produktivitas.'),(2,'No-code dan low-code tools memperluas scope Ops Manager tanpa harus bergantung pada engineering.'),(3,'Ops Manager yang pernah scale perusahaan dari 50 ke 500 orang sangat dicari perusahaan growth stage.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #46: Game Developer ───────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'game-developer', 'Game Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'GAME'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Game Developer membangun pengalaman interaktif yang membuat jutaan orang terhibur dan terhubung. Dari game mobile casual hingga game PC multiplayer — mereka menggabungkan programming, fisika, dan desain untuk menciptakan dunia digital yang menarik.',
    'Profil RI cocok karena Game Developer melakukan implementasi teknis yang sangat hands-on (Realistic) sekaligus investigasi mendalam terhadap game mechanics, performa rendering, dan physics simulation (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengimplementasikan game mechanics, physics, dan AI behavior menggunakan Unity atau Unreal'),
  (2, 'Mengoptimalkan performa game: frame rate, memory, dan loading time di target platform'),
  (3, 'Berkolaborasi dengan game artist dan designer untuk mengintegrasikan aset visual dan audio'),
  (4, 'Membangun sistem backend untuk multiplayer, leaderboard, dan in-app purchase'),
  (5, 'Melakukan playtesting dan mengiterasi game feel berdasarkan feedback'),
  (6, 'Mengelola build pipeline dan submission ke App Store, Google Play, atau Steam')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'game-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('game-development','unity-unreal','python','git','agile','code-review','rest-api-design')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'game-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('unity','unreal','blender','vscode','github-actions','jira','slack','notion','sentry')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'game-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Junior Game Developer',5000000,10000000),(2,'Game Developer',10000000,20000000),(3,'Senior Game Developer',20000000,35000000),(4,'Lead Game Developer',35000000,60000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'game-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Industri game mobile Indonesia tumbuh pesat — Indonesia masuk top 5 pasar game mobile Asia.'),(2,'Hyper-casual game yang bisa develop cepat dan scale ads sangat diminati publisher global.'),(3,'Game developer yang bisa handle backend dan analytics sendiri sangat efisien untuk indie studio.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #47: Web3 / Blockchain Developer ─────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'web3-blockchain-developer', 'Web3 / Blockchain Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IR'),
    'Web3 / Blockchain Developer membangun aplikasi terdesentralisasi (dApp) dan smart contract di atas blockchain seperti Ethereum. Mereka berada di frontier teknologi yang sedang mendefinisikan ulang kepemilikan digital, keuangan terdesentralisasi, dan identitas online.',
    'Profil IR cocok karena Blockchain Developer perlu investigasi mendalam terhadap kriptografi dan konsensus mekanisme (Investigative) sekaligus implementasi teknis nyata dari smart contract dan protocol (Realistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Menulis dan mengaudit smart contract Solidity untuk protocol DeFi atau NFT marketplace'),
  (2, 'Membangun dApp frontend yang terintegrasi dengan wallet Web3 (MetaMask, WalletConnect)'),
  (3, 'Mengoptimalkan gas efficiency smart contract untuk mengurangi biaya transaksi pengguna'),
  (4, 'Melakukan security review dan formal verification smart contract sebelum deployment'),
  (5, 'Membangun indexer dan subgraph untuk query on-chain data secara efisien'),
  (6, 'Berkolaborasi dengan protocol designer untuk mengimplementasikan tokenomics dan governance')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web3-blockchain-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('blockchain','smart-contracts','python','nodejs','typescript','rest-api-design','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web3-blockchain-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('hardhat','metamask','vscode','github-actions','notion','slack','discord')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web3-blockchain-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Junior Web3 Developer',8000000,15000000),(2,'Web3 Developer',15000000,30000000),(3,'Senior Web3 Developer',30000000,60000000),(4,'Protocol Engineer / Lead',60000000,150000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'web3-blockchain-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Web3 developer sangat langka secara global — kompensasi bisa jauh di atas rata-rata industri.'),(2,'DeFi protocol dan NFT infrastructure terus mencari Solidity developer berpengalaman.'),(3,'Smart contract auditor adalah spesialisasi paling dicari dan bergaji tertinggi di ekosistem Web3.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #48: IoT / Embedded Systems Engineer ─────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'iot-embedded-systems-engineer', 'IoT / Embedded Systems Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'EMBEDDED'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'R'),
    'IoT / Embedded Systems Engineer mengembangkan software untuk perangkat fisik yang terhubung ke internet — dari sensor industri dan smart home device hingga wearable dan kendaraan otonom. Mereka bekerja di boundary antara hardware dan software.',
    'Profil R (Realistic) sangat cocok karena Embedded Engineer bekerja langsung dengan perangkat keras fisik, melakukan testing di hardware nyata, dan mengoptimalkan kode untuk resource yang sangat terbatas.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengembangkan firmware dan driver untuk mikrokontroler (STM32, ESP32, Arduino)'),
  (2, 'Mengintegrasikan sensor, aktuator, dan modul komunikasi ke dalam sistem embedded'),
  (3, 'Mengoptimalkan performa dan konsumsi daya untuk perangkat battery-powered'),
  (4, 'Membangun komunikasi IoT: MQTT, CoAP, dan integrasi dengan cloud platform'),
  (5, 'Melakukan debugging hardware menggunakan oscilloscope dan logic analyzer'),
  (6, 'Berkolaborasi dengan hardware engineer untuk memastikan integrasi PCB dan firmware')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'iot-embedded-systems-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('iot-development','embedded-systems','python','bash-scripting','linux-administration','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'iot-embedded-systems-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('arduino','raspberry-pi','vscode','github-actions','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'iot-embedded-systems-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Junior Embedded Engineer',6000000,12000000),(2,'Embedded Engineer',12000000,22000000),(3,'Senior Embedded Engineer',22000000,38000000),(4,'IoT Architect / Lead',38000000,65000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'iot-embedded-systems-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Industri manufaktur dan pertanian Indonesia mulai adopsi IoT — demand embedded engineer tumbuh.'),(2,'Embedded engineer yang juga bisa cloud backend (AWS IoT, GCP IoT Core) sangat bernilai.'),(3,'Smart city dan infrastruktur digital pemerintah membuka peluang besar untuk IoT engineer.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #49: Network Engineer ─────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'network-engineer', 'Network Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'NETWORK'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RC'),
    'Network Engineer merancang, membangun, dan memelihara infrastruktur jaringan yang menghubungkan semua sistem digital. Dari jaringan kantor dan data center hingga SD-WAN dan jaringan cloud — mereka memastikan konektivitas yang cepat, aman, dan reliabel.',
    'Profil RC cocok karena Network Engineer melakukan konfigurasi dan maintenance jaringan yang sangat hands-on (Realistic) sekaligus menerapkan standar dan prosedur jaringan yang ketat (Conventional).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang topologi jaringan yang scalable dan resilient untuk data center atau kantor'),
  (2, 'Mengkonfigurasi dan memelihara router, switch, dan firewall enterprise'),
  (3, 'Mengimplementasikan network security: VPN, IDS/IPS, dan segmentasi jaringan'),
  (4, 'Memantau performa jaringan dan mendiagnosis bottleneck atau koneksi yang tidak stabil'),
  (5, 'Mengelola migrasi ke SD-WAN atau jaringan cloud (AWS Direct Connect, GCP Interconnect)'),
  (6, 'Mendokumentasikan arsitektur jaringan dan mengelola IP addressing schema')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'network-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('network-engineering','linux-administration','bash-scripting','monitoring-observability','aws','python','git')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'network-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('wireshark','cisco-packet','grafana','prometheus','aws-console','jira','slack','confluence')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'network-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Junior Network Engineer',6000000,12000000),(2,'Network Engineer',12000000,22000000),(3,'Senior Network Engineer',22000000,38000000),(4,'Network Architect',38000000,70000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'network-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Transformasi digital perbankan dan telco Indonesia mendorong permintaan network engineer senior.'),(2,'Network engineer yang bisa handle cloud networking (AWS/GCP) lebih kompetitif dari yang hanya onsite.'),(3,'Sertifikasi CCNA, CCNP, dan AWS Advanced Networking masih sangat dihargai di industri.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #50: Product Data Analyst ─────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'product-data-analyst', 'Product Data Analyst',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'ANALYTICS'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IC'),
    'Product Data Analyst menganalisis perilaku pengguna di dalam produk digital untuk membantu tim produk dan bisnis membuat keputusan yang lebih baik. Mereka adalah jembatan antara data mentah dan insight yang dapat ditindaklanjuti oleh PM, designer, dan engineer.',
    'Profil IC cocok karena Product Analyst perlu investigasi mendalam ke dalam data pengguna (Investigative) sekaligus kecermatan dalam membangun analisis yang akurat dan reproducible (Conventional).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Menganalisis funnel pengguna untuk mengidentifikasi drop-off dan friction point di produk'),
  (2, 'Membangun dan memelihara dashboard produk yang digunakan PM secara harian'),
  (3, 'Merancang tracking plan dan memastikan implementasi analytics event yang benar'),
  (4, 'Melakukan analisis cohort untuk memahami retensi dan engagement pengguna dari waktu ke waktu'),
  (5, 'Mendukung product experiment dengan analisis statistik yang valid'),
  (6, 'Mempresentasikan insight kepada tim produk dan memberikan rekomendasi yang konkret')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-data-analyst')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('product-analytics','sql-advanced','statistics','ab-testing','data-visualization','python','agile','stakeholder-management')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-data-analyst')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('amplitude','mixpanel','bigquery','metabase','looker','jupyter','notion','slack','jira','fullstory')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-data-analyst')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Junior Product Analyst',6000000,12000000),(2,'Product Analyst',12000000,22000000),(3,'Senior Product Analyst',22000000,38000000),(4,'Lead Product Analyst',38000000,65000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-data-analyst')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Hampir setiap product company Indonesia kini punya atau butuh product analyst dedicated.'),(2,'Analyst yang bisa setup tracking sendiri di Amplitude/Segment tanpa bergantung engineering sangat produktif.'),(3,'Kombinasi SQL yang kuat dan kemampuan presentasi insight adalah skill yang paling dicari PM dari analyst.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

COMMIT;

-- =============================================================================
-- SEEDER PROFESI DIGITAL — BATCH 04 (Profesi #31–40)
-- Kategori: Marketing Digital, Developer Relations, Technical Writing, Business
-- Prasyarat: batch 01-03 sudah dijalankan
-- Idempotent: pakai INSERT ... ON CONFLICT DO NOTHING
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. SKILLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO skills (slug, name, created_at, updated_at) VALUES
  ('seo',                    'SEO',                              NOW(), NOW()),
  ('content-marketing',      'Content Marketing',                NOW(), NOW()),
  ('copywriting',            'Copywriting',                      NOW(), NOW()),
  ('social-media-marketing', 'Social Media Marketing',           NOW(), NOW()),
  ('email-marketing',        'Email Marketing',                  NOW(), NOW()),
  ('paid-ads',               'Paid Ads (Meta/Google)',           NOW(), NOW()),
  ('marketing-analytics',    'Marketing Analytics',              NOW(), NOW()),
  ('technical-writing',      'Technical Writing',                NOW(), NOW()),
  ('api-documentation',      'API Documentation',                NOW(), NOW()),
  ('public-speaking',        'Public Speaking',                  NOW(), NOW()),
  ('community-building',     'Community Building',               NOW(), NOW()),
  ('developer-relations',    'Developer Relations',              NOW(), NOW()),
  ('b2b-sales',              'B2B Sales',                        NOW(), NOW()),
  ('solution-selling',       'Solution Selling',                 NOW(), NOW()),
  ('crm-management',         'CRM Management',                   NOW(), NOW()),
  ('business-development',   'Business Development',             NOW(), NOW()),
  ('partnership-management', 'Partnership Management',           NOW(), NOW()),
  ('financial-modeling',     'Financial Modeling',               NOW(), NOW()),
  ('fundraising',            'Fundraising & Investor Relations', NOW(), NOW()),
  ('project-management',     'Project Management',               NOW(), NOW()),
  ('risk-management',        'Risk Management',                  NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. TOOLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO tools (slug, name, created_at, updated_at) VALUES
  ('semrush',     'SEMrush',              NOW(), NOW()),
  ('ahrefs',      'Ahrefs',               NOW(), NOW()),
  ('hubspot',     'HubSpot',              NOW(), NOW()),
  ('mailchimp',   'Mailchimp',            NOW(), NOW()),
  ('meta-ads',    'Meta Ads Manager',     NOW(), NOW()),
  ('google-ads',  'Google Ads',           NOW(), NOW()),
  ('buffer',      'Buffer',               NOW(), NOW()),
  ('readme-io',   'Readme.io',            NOW(), NOW()),
  ('gitbook',     'GitBook',              NOW(), NOW()),
  ('loom',        'Loom',                 NOW(), NOW()),
  ('streamyard',  'StreamYard',           NOW(), NOW()),
  ('discord',     'Discord',              NOW(), NOW()),
  ('salesforce',  'Salesforce',           NOW(), NOW()),
  ('pipedrive',   'Pipedrive',            NOW(), NOW()),
  ('apollo',      'Apollo.io',            NOW(), NOW()),
  ('zoom',        'Zoom',                 NOW(), NOW()),
  ('pitch',       'Pitch',                NOW(), NOW()),
  ('canva',       'Canva',                NOW(), NOW()),
  ('clickup',     'ClickUp',              NOW(), NOW()),
  ('asana',       'Asana',                NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- PROFESI #31–40
-- -----------------------------------------------------------------------------

-- ── #31: Technical Developer Advocate ────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'technical-developer-advocate', 'Technical Developer Advocate',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'S'),
    'Technical Developer Advocate menjadi jembatan antara perusahaan teknologi dengan komunitas developer. Mereka membuat developer jatuh cinta dengan produk melalui konten teknis, demo, workshop, dan kehadiran aktif di komunitas — sambil membawa feedback developer kembali ke tim produk.',
    'Profil S (Social) cocok karena Developer Advocate adalah tentang membangun hubungan, membantu developer sukses, dan menciptakan komunitas yang saling mendukung di sekitar produk teknologi.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membuat konten teknis: artikel, tutorial, video, dan sample code untuk membantu developer'),
  (2, 'Berbicara di konferensi dan meetup teknis untuk mempresentasikan produk dan use case'),
  (3, 'Membangun dan mengelola komunitas developer di Discord, forum, atau GitHub Discussions'),
  (4, 'Mengumpulkan feedback developer dan mengadvokasi kebutuhan mereka ke tim produk'),
  (5, 'Membuat dan memelihara dokumentasi, quickstart guide, dan contoh integrasi'),
  (6, 'Mengelola program early adopter dan beta tester untuk fitur baru')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-developer-advocate')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('developer-relations','technical-writing','public-speaking','community-building','python','rest-api-design','git','stakeholder-management')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-developer-advocate')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('readme-io','gitbook','discord','loom','streamyard','github-actions','notion','slack','vscode')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-developer-advocate')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Developer Advocate',10000000,20000000),(2,'Senior Developer Advocate',20000000,35000000),(3,'Staff Developer Advocate',35000000,55000000),(4,'Head of Developer Relations',55000000,90000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-developer-advocate')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Developer Relations menjadi investasi strategis perusahaan API-first dan cloud provider.'),(2,'DevRel yang punya personal brand kuat di komunitas developer Indonesia sangat langka.'),(3,'Kombinasi coding + komunikasi publik yang baik adalah kombinasi yang sangat jarang.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #32: Technical Documentation Engineer ────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'technical-documentation-engineer', 'Technical Documentation Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'CE'),
    'Technical Documentation Engineer membuat dokumentasi yang memungkinkan developer dan pengguna memahami produk teknologi secara mandiri. Dokumentasi yang baik adalah multiplier — satu artikel bisa menggantikan ribuan pertanyaan support.',
    'Profil CE cocok karena Technical Writer membutuhkan ketelitian dan struktur (Conventional) sekaligus inisiatif untuk mencari dan mendokumentasikan pengetahuan yang tersebar (Enterprising).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Menulis dan memelihara API reference documentation yang akurat dan mudah dipahami'),
  (2, 'Membuat getting started guide, tutorial, dan how-to artikel untuk berbagai level pengguna'),
  (3, 'Berkolaborasi dengan engineer untuk memastikan akurasi dokumentasi teknis'),
  (4, 'Mengelola dokumentasi menggunakan docs-as-code workflow (Markdown, Git, CI/CD)'),
  (5, 'Menganalisis feedback pengguna untuk menemukan gap dokumentasi'),
  (6, 'Membangun information architecture yang intuitif untuk developer portal')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-documentation-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('technical-writing','api-documentation','rest-api-design','git','python','ux-writing','stakeholder-management')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-documentation-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('readme-io','gitbook','notion','postman','github-actions','jira','slack','vscode','confluence')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-documentation-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Technical Writer',7000000,14000000),(2,'Senior Technical Writer',14000000,25000000),(3,'Docs Engineer',25000000,40000000),(4,'Head of Documentation',40000000,65000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-documentation-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Developer experience yang baik dimulai dari dokumentasi — makin banyak perusahaan sadari ini.'),(2,'Docs-as-code membuat technical writer makin overlap dengan software engineer.'),(3,'Technical writer yang bisa code dan test API sendiri jauh lebih dihargai.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #33: Digital Marketing Manager ───────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'digital-marketing-manager', 'Digital Marketing Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'MARKETING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'ES'),
    'Digital Marketing Manager merancang dan mengeksekusi strategi marketing digital yang mendorong awareness, akuisisi, dan retensi pengguna. Mereka mengelola seluruh channel digital — dari SEO dan content hingga paid ads dan email.',
    'Profil ES cocok karena Digital Marketing Manager harus punya ambisi growth (Enterprising) sekaligus kemampuan memahami psikologi audiens (Social).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang strategi marketing digital multi-channel yang terintegrasi'),
  (2, 'Mengelola campaign paid ads di Google, Meta, dan TikTok dengan efisiensi ROAS'),
  (3, 'Memimpin content strategy dan SEO untuk meningkatkan organic traffic'),
  (4, 'Menganalisis marketing funnel dan mengoptimalkan conversion di setiap tahap'),
  (5, 'Mengelola marketing budget dan alokasi ke channel paling efektif'),
  (6, 'Berkolaborasi dengan product dan sales untuk campaign go-to-market')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-marketing-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('seo','content-marketing','paid-ads','marketing-analytics','email-marketing','social-media-marketing','ab-testing','stakeholder-management','market-research')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-marketing-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('google-analytics','meta-ads','google-ads','semrush','hubspot','mailchimp','buffer','amplitude','notion','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-marketing-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Digital Marketing Specialist',6000000,12000000),(2,'Digital Marketing Manager',12000000,22000000),(3,'Senior Marketing Manager',22000000,38000000),(4,'VP Marketing',38000000,80000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-marketing-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Marketing yang data-driven menjadi standar — marketer yang tidak bisa baca data makin tersisih.'),(2,'TikTok Ads menjadi channel paling cepat tumbuh di Indonesia sejak 2023.'),(3,'Performance marketer yang bisa manage budget besar sangat langka dan bergaji premium.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #34: SEO & Content Strategist ────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'seo-content-strategist', 'SEO & Content Strategist',
    (SELECT id FROM profession_main_categories WHERE code = 'MARKETING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IA'),
    'SEO & Content Strategist membangun kehadiran organik produk digital melalui konten berkualitas tinggi. Mereka menggabungkan analisis data keyword, pemahaman algoritma Google, dan kemampuan storytelling untuk mendatangkan traffic yang tepat sasaran.',
    'Profil IA cocok karena SEO content strategist perlu investigasi data (Investigative) sekaligus kreativitas dalam menciptakan konten yang menarik (Artistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Melakukan keyword research dan gap analysis untuk menemukan peluang konten organik'),
  (2, 'Membuat content strategy dan editorial calendar selaras dengan funnel marketing'),
  (3, 'Mengoptimalkan on-page SEO: meta tag, heading structure, internal linking, dan schema'),
  (4, 'Menganalisis performa konten di Google Search Console'),
  (5, 'Membangun backlink strategy melalui digital PR dan content partnership'),
  (6, 'Berkolaborasi dengan tim produk untuk mengoptimalkan technical SEO di platform')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'seo-content-strategist')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('seo','content-marketing','copywriting','marketing-analytics','data-visualization','market-research','competitor-analysis')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'seo-content-strategist')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('semrush','ahrefs','google-analytics','notion','canva','buffer','jira','slack','notion-ai')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'seo-content-strategist')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'SEO Specialist',5000000,10000000),(2,'SEO & Content Strategist',10000000,20000000),(3,'Senior Content Strategist',20000000,35000000),(4,'Head of Content',35000000,60000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'seo-content-strategist')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'AI-generated content mengubah landscape SEO — strategist yang bisa direct AI lebih unggul.'),(2,'Technical SEO semakin krusial dan butuh kolaborasi dengan dev.'),(3,'SEO yang bisa analisis data sendiri tanpa bergantung tim data sangat dihargai.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #35: Growth Marketing Analyst ────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'growth-marketing-analyst', 'Growth Marketing Analyst',
    (SELECT id FROM profession_main_categories WHERE code = 'MARKETING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IC'),
    'Growth Marketing Analyst menganalisis data marketing untuk menemukan peluang pertumbuhan. Mereka mengukur efektivitas setiap channel, membangun attribution model, dan memberikan rekomendasi berbasis data untuk mengoptimalkan pengeluaran marketing.',
    'Profil IC cocok karena growth analyst membutuhkan investigasi mendalam ke dalam data (Investigative) sekaligus kecermatan dalam membangun model yang akurat (Conventional).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun marketing attribution model untuk mengukur kontribusi setiap channel'),
  (2, 'Menganalisis customer acquisition cost (CAC) dan lifetime value (LTV) per segmen'),
  (3, 'Membuat dashboard marketing performance untuk pengambilan keputusan CMO'),
  (4, 'Melakukan cohort analysis untuk memahami pola retensi pelanggan dari berbagai source'),
  (5, 'Menganalisis hasil A/B test campaign marketing secara statistik'),
  (6, 'Berkolaborasi dengan tim paid ads untuk mengoptimalkan bidding strategy berbasis data')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'growth-marketing-analyst')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('marketing-analytics','sql-advanced','statistics','ab-testing','data-visualization','python')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'growth-marketing-analyst')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('amplitude','mixpanel','google-analytics','bigquery','metabase','looker','notion','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'growth-marketing-analyst')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Marketing Analyst',7000000,13000000),(2,'Growth Marketing Analyst',13000000,23000000),(3,'Senior Growth Analyst',23000000,40000000),(4,'Head of Marketing Analytics',40000000,70000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'growth-marketing-analyst')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Multi-touch attribution menjadi tantangan besar seiring privacy changes iOS.'),(2,'Marketing analyst yang bisa SQL sendiri sangat produktif.'),(3,'Kemampuan predictive analytics untuk forecast campaign sangat dihargai.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #36: Technology Sales Engineer ───────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'technology-sales-engineer', 'Technology Sales Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'BUSINESS'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'EC'),
    'Technology Sales Engineer menggabungkan keahlian teknis dengan kemampuan penjualan untuk memenangkan deal enterprise. Mereka melakukan demo produk, menjawab technical objection, dan memastikan prospek yakin bahwa solusi teknis menjawab masalah mereka.',
    'Profil EC cocok karena Sales Engineer harus punya drive komersial untuk closing deal (Enterprising) sekaligus keteraturan teknis dalam mendokumentasikan solusi (Conventional).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Melakukan technical discovery untuk memahami pain point dan kebutuhan teknis prospek'),
  (2, 'Membangun dan mempresentasikan proof of concept yang relevan dengan use case klien'),
  (3, 'Menjawab Request for Proposal (RFP) dan technical security questionnaire dari enterprise'),
  (4, 'Berkolaborasi dengan account executive untuk strategi deal dan negosiasi teknis'),
  (5, 'Memberikan training produk kepada tim teknis klien pasca closing'),
  (6, 'Mengumpulkan feedback teknis dari prospek dan menyampaikannya ke tim produk')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technology-sales-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('b2b-sales','solution-selling','technical-writing','rest-api-design','public-speaking','stakeholder-management','python')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technology-sales-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('salesforce','hubspot','zoom','loom','pitch','postman','notion','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technology-sales-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Sales Engineer',10000000,20000000),(2,'Senior Sales Engineer',20000000,35000000),(3,'Principal Sales Engineer',35000000,60000000),(4,'Head of Solutions Engineering',60000000,100000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technology-sales-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'SaaS dan cloud adoption enterprise Indonesia mendorong permintaan sales engineer.'),(2,'Sales engineer yang bisa demo live coding sangat efektif memenangkan deal.'),(3,'OTE Sales Engineer bisa 2x gaji base — salah satu peran paling menguntungkan di tech.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #37: Tech Startup Founder / CTO ──────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'tech-startup-founder-cto', 'Tech Startup Founder / CTO',
    (SELECT id FROM profession_main_categories WHERE code = 'BUSINESS'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'ES'),
    'Tech Startup Founder atau CTO memimpin visi teknis dan strategi produk sebuah startup dari ideasi hingga scale. Mereka bertanggung jawab atas keputusan arsitektur, membangun tim engineering, dan memastikan produk bisa memenangkan pasar.',
    'Profil ES cocok karena founder/CTO harus punya jiwa entrepreneurial (Enterprising) sekaligus kemampuan membangun dan memimpin tim (Social).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mendefinisikan technical vision dan arsitektur produk untuk mendukung strategi bisnis'),
  (2, 'Merekrut, membangun, dan memimpin tim engineering dari ground up'),
  (3, 'Mengelola technical debt dan keseimbangan antara kecepatan dan kualitas'),
  (4, 'Mempresentasikan roadmap teknis kepada investor dan board'),
  (5, 'Membangun budaya engineering yang produktif dan high output'),
  (6, 'Berkolaborasi dengan co-founder untuk memastikan visi produk dan bisnis selaras')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-startup-founder-cto')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('system-design','product-strategy','stakeholder-management','fundraising','public-speaking','community-building','financial-modeling')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-startup-founder-cto')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('notion','jira','slack','pitch','zoom','github-actions','aws-console','figma','linear')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-startup-founder-cto')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Technical Co-Founder (Pre-seed)',0,30000000),(2,'CTO Seed Stage',20000000,60000000),(3,'CTO Series A/B',60000000,150000000),(4,'CTO Growth/Scale',150000000,500000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'tech-startup-founder-cto')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Ekosistem startup Indonesia terus tumbuh — founder teknis masih banyak dicari investor.'),(2,'CTO yang bisa scale tim dari 3 ke 50+ engineer adalah profil paling langka di Indonesia.'),(3,'Equity dapat menjadi kompensasi utama yang nilainya jauh melebihi gaji di startup yang sukses.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #38: Business Development Manager (Tech) ─────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'business-development-manager-tech', 'Business Development Manager (Tech)',
    (SELECT id FROM profession_main_categories WHERE code = 'BUSINESS'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'E'),
    'Business Development Manager di perusahaan teknologi membangun kemitraan strategis yang mempercepat pertumbuhan. Dari integrasi API dengan partner ekosistem hingga deal distribusi enterprise — mereka membuka pintu yang tidak bisa dibuka tim sales biasa.',
    'Profil E (Enterprising) cocok karena BizDev adalah tentang memimpin negosiasi, mengidentifikasi peluang, dan menggerakkan deal yang mengubah trajectory bisnis.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengidentifikasi dan mengevaluasi peluang kemitraan strategis yang menguntungkan kedua pihak'),
  (2, 'Memimpin negosiasi term sheet dan kontrak kemitraan dengan perusahaan mitra'),
  (3, 'Mengelola hubungan jangka panjang dengan partner dan memastikan mutual value terealisasi'),
  (4, 'Berkolaborasi dengan tim produk untuk mendefinisikan integrasi teknis yang dibutuhkan'),
  (5, 'Mempresentasikan peluang kemitraan kepada C-level dan board'),
  (6, 'Membangun pipeline partnership dan tracking progress menggunakan CRM')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'business-development-manager-tech')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('business-development','partnership-management','b2b-sales','stakeholder-management','public-speaking','market-research','competitor-analysis','financial-modeling')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'business-development-manager-tech')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('salesforce','hubspot','pipedrive','apollo','zoom','pitch','notion','slack','airtable')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'business-development-manager-tech')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'BizDev Associate',8000000,15000000),(2,'BizDev Manager',15000000,28000000),(3,'Senior BizDev Manager',28000000,50000000),(4,'VP Business Development',50000000,100000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'business-development-manager-tech')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Super app dan platform ekosistem mendorong permintaan BizDev yang bisa manage integrasi teknis.'),(2,'BizDev dengan network kuat di ekosistem fintech dan e-commerce Indonesia sangat bernilai.'),(3,'Kemampuan memahami technical integration membuat BizDev tech jauh lebih efektif.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #39: Technical Project Manager ───────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'technical-project-manager', 'Technical Project Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'PRODUCT'),
    (SELECT id FROM profession_sub_categories WHERE code = 'OPERATIONS'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'SE'),
    'Technical Project Manager memastikan proyek teknologi selesai tepat waktu, sesuai scope, dan dalam budget. Mereka mengelola dependency antar tim, menghilangkan blocker, dan menjaga semua stakeholder tetap aligned.',
    'Profil SE cocok karena Technical PM harus pandai membangun kepercayaan lintas tim (Social) sekaligus proaktif dan berorientasi hasil dalam mengeksekusi proyek (Enterprising).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membuat project plan, milestone, dan dependency map yang realistis'),
  (2, 'Memfasilitasi daily standup, sprint planning, dan retrospective'),
  (3, 'Mengidentifikasi dan mengelola risiko proyek sebelum menjadi blocking issue'),
  (4, 'Mengkomunikasikan status proyek kepada stakeholder secara transparan'),
  (5, 'Mengelola scope creep melalui proses change management yang ketat'),
  (6, 'Berkoordinasi dengan vendor dan tim eksternal yang terlibat dalam proyek')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-project-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('project-management','agile','stakeholder-management','risk-management','product-analytics','public-speaking')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-project-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('jira','linear','asana','clickup','notion','confluence','miro','slack','zoom')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-project-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'Project Coordinator',7000000,13000000),(2,'Technical PM',13000000,25000000),(3,'Senior Technical PM',25000000,42000000),(4,'Program Manager / Head',42000000,75000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-project-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'Technical PM dengan sertifikasi PMP atau Scrum Master lebih mudah masuk enterprise.'),(2,'PM yang bisa baca Jira dan tahu cara unblock engineering issue sangat efektif.'),(3,'Demand Technical PM meningkat di proyek transformasi digital perbankan dan BUMN Indonesia.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

-- ── #40: Security Operations Analyst ─────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (slug, name, main_category_id, sub_category_id, riasec_code_id, about_description, riasec_description, created_at, updated_at)
  SELECT 'security-operations-analyst', 'Security Operations Analyst',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'SECURITY'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'CR'),
    'Security Operations Analyst memantau, mendeteksi, dan merespons ancaman keamanan secara real-time dari Security Operations Center (SOC). Mereka adalah garda depan pertahanan siber yang memastikan tidak ada insiden keamanan yang lolos.',
    'Profil CR cocok karena SOC analyst bekerja dengan prosedur yang sangat terstruktur (Conventional) sambil melakukan respons teknis nyata terhadap ancaman (Realistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Memantau alert keamanan dari SIEM dan mengklasifikasikan severity setiap insiden'),
  (2, 'Melakukan investigasi forensik digital untuk mengidentifikasi root cause insiden'),
  (3, 'Menulis incident report dan mendokumentasikan timeline serangan'),
  (4, 'Melakukan threat hunting proaktif untuk menemukan indikator kompromi tersembunyi'),
  (5, 'Mengembangkan detection rule berdasarkan threat intelligence terbaru'),
  (6, 'Berkoordinasi dengan tim IT dan manajemen saat terjadi insiden keamanan besar')
) AS act(sort_order, description) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-operations-analyst')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('monitoring-observability','linux-administration','python','bash-scripting','technical-writing')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-operations-analyst')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('datadog','grafana','prometheus','pagerduty','jira','confluence','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-operations-analyst')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.so, NOW(), NOW() FROM p,
(VALUES (1,'SOC Analyst L1',6000000,12000000),(2,'SOC Analyst L2',12000000,22000000),(3,'Senior SOC Analyst',22000000,38000000),(4,'SOC Lead / CISO',38000000,80000000))
AS lv(so, level_name, sal_min, sal_max) ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'security-operations-analyst')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.d, mi.so, NOW(), NOW() FROM p,
(VALUES (1,'BSSN dan regulasi keamanan siber nasional mendorong pembentukan SOC di banyak institusi Indonesia.'),(2,'SOC analyst yang mahir threat hunting dengan MITRE ATT&CK framework sangat dicari.'),(3,'Sertifikasi CompTIA Security+, CEH, dan GCIH membuka peluang di perusahaan keamanan enterprise.'))
AS mi(so, d) ON CONFLICT DO NOTHING;

COMMIT;

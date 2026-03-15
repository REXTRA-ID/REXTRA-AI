-- =============================================================================
-- SEEDER PROFESI DIGITAL — BATCH 03 (Profesi #21–30)
-- Kategori: Design (UI/UX, Visual, Research), Product Management & Growth
-- Prasyarat: seed_professions_01.sql & seed_professions_02.sql sudah dijalankan
-- Idempotent: pakai INSERT ... ON CONFLICT DO NOTHING
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. SKILLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO skills (slug, name, created_at, updated_at) VALUES
  ('user-research',           'User Research',                NOW(), NOW()),
  ('usability-testing',       'Usability Testing',            NOW(), NOW()),
  ('wireframing-prototyping', 'Wireframing & Prototyping',    NOW(), NOW()),
  ('design-system',           'Design System',                NOW(), NOW()),
  ('interaction-design',      'Interaction Design',           NOW(), NOW()),
  ('visual-design',           'Visual Design',                NOW(), NOW()),
  ('motion-design',           'Motion Design',                NOW(), NOW()),
  ('brand-identity',          'Brand Identity Design',        NOW(), NOW()),
  ('typography',              'Typography',                   NOW(), NOW()),
  ('ux-writing',              'UX Writing',                   NOW(), NOW()),
  ('product-strategy',        'Product Strategy',             NOW(), NOW()),
  ('product-roadmap',         'Product Roadmap',              NOW(), NOW()),
  ('user-story',              'User Story Writing',           NOW(), NOW()),
  ('ab-testing',              'A/B Testing',                  NOW(), NOW()),
  ('growth-hacking',          'Growth Hacking',               NOW(), NOW()),
  ('conversion-optimization', 'Conversion Rate Optimization', NOW(), NOW()),
  ('product-analytics',       'Product Analytics',            NOW(), NOW()),
  ('stakeholder-management',  'Stakeholder Management',       NOW(), NOW()),
  ('market-research',         'Market Research',              NOW(), NOW()),
  ('competitor-analysis',     'Competitor Analysis',          NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. TOOLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO tools (slug, name, created_at, updated_at) VALUES
  ('miro',            'Miro',                     NOW(), NOW()),
  ('maze',            'Maze',                     NOW(), NOW()),
  ('hotjar',          'Hotjar',                   NOW(), NOW()),
  ('mixpanel',        'Mixpanel',                 NOW(), NOW()),
  ('productboard',    'Productboard',             NOW(), NOW()),
  ('linear',          'Linear',                   NOW(), NOW()),
  ('framer',          'Framer',                   NOW(), NOW()),
  ('adobe-xd',        'Adobe XD',                 NOW(), NOW()),
  ('illustrator',     'Adobe Illustrator',        NOW(), NOW()),
  ('photoshop',       'Adobe Photoshop',          NOW(), NOW()),
  ('after-effects',   'Adobe After Effects',      NOW(), NOW()),
  ('lottie',          'Lottie Files',             NOW(), NOW()),
  ('google-analytics','Google Analytics 4',       NOW(), NOW()),
  ('fullstory',       'FullStory',                NOW(), NOW()),
  ('dovetail',        'Dovetail',                 NOW(), NOW()),
  ('coda',            'Coda',                     NOW(), NOW()),
  ('airtable',        'Airtable',                 NOW(), NOW()),
  ('intercom',        'Intercom',                 NOW(), NOW()),
  ('typeform',        'Typeform',                 NOW(), NOW()),
  ('notion-ai',       'Notion AI',                NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 3. PROFESI #21–30
-- -----------------------------------------------------------------------------

-- ── #21: Product UI/UX Designer ──────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'product-uiux-designer',
    'Product UI/UX Designer',
    (SELECT id FROM profession_main_categories WHERE code = 'DESIGN'),
    (SELECT id FROM profession_sub_categories WHERE code = 'UI_UX'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'A'),
    'Product UI/UX Designer merancang antarmuka dan pengalaman pengguna untuk produk digital. Mereka menggabungkan riset pengguna, desain visual, dan prototipe interaktif untuk memastikan setiap touchpoint di produk terasa intuitif, konsisten, dan menyenangkan.',
    'Profil A (Artistic) sangat cocok karena UI/UX designer adalah pekerjaan kreatif yang membutuhkan sense estetika tajam, kemampuan berpikir desain yang kuat, dan ekspresi visual yang orisinal.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Melakukan user research melalui wawancara, survei, dan usability testing'),
  (2, 'Membuat wireframe, user flow, dan high-fidelity prototype di Figma'),
  (3, 'Membangun dan memelihara design system yang konsisten di seluruh produk'),
  (4, 'Berkolaborasi dengan engineer untuk memastikan implementasi sesuai desain'),
  (5, 'Melakukan design critique dan iterasi berdasarkan feedback pengguna dan data'),
  (6, 'Mendefinisikan design guidelines dan accessibility standard untuk produk')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-uiux-designer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('user-research','usability-testing','wireframing-prototyping','design-system','interaction-design','visual-design','accessibility','agile','stakeholder-management')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-uiux-designer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('figma','miro','maze','hotjar','dovetail','storybook','jira','slack','notion','amplitude')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-uiux-designer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior UI/UX Designer',   5000000,  10000000),
  (2, 'UI/UX Designer',         10000000,  20000000),
  (3, 'Senior UI/UX Designer',  20000000,  35000000),
  (4, 'Principal Designer',     35000000,  60000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-uiux-designer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Design thinking menjadi kompetensi inti yang diminta perusahaan di luar tech sekalipun.'),
  (2, 'AI-assisted design tools mengubah workflow — designer yang mahir Figma AI lebih produktif.'),
  (3, 'Senior designer yang bisa memimpin design system di skala enterprise sangat langka dan bergaji tinggi.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #22: UX Researcher ───────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'ux-researcher',
    'UX Researcher',
    (SELECT id FROM profession_main_categories WHERE code = 'DESIGN'),
    (SELECT id FROM profession_sub_categories WHERE code = 'RESEARCH'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IA'),
    'UX Researcher menggali pemahaman mendalam tentang pengguna — siapa mereka, apa yang mereka butuhkan, dan bagaimana mereka berinteraksi dengan produk. Insight mereka menjadi fondasi keputusan desain dan produk yang tepat sasaran.',
    'Profil IA (Investigative-Artistic) cocok karena UX researcher melakukan investigasi ilmiah (Investigative) untuk memahami perilaku manusia, lalu mengkomunikasikan temuannya dengan cara yang persuasif dan mudah dipahami (Artistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan menjalankan studi riset kualitatif (wawancara mendalam, focus group)'),
  (2, 'Menganalisis data perilaku pengguna dari Hotjar, FullStory, dan analytics platform'),
  (3, 'Melakukan usability testing dan mengidentifikasi pain point di alur pengguna'),
  (4, 'Menyusun research report dan mempresentasikan insight kepada tim produk dan bisnis'),
  (5, 'Membangun dan mengelola user panel untuk riset yang berkelanjutan'),
  (6, 'Berkolaborasi dengan designer untuk menerjemahkan insight riset ke keputusan desain')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-researcher')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('user-research','usability-testing','statistics','product-analytics','market-research','stakeholder-management','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-researcher')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('figma','miro','maze','hotjar','fullstory','dovetail','typeform','amplitude','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-researcher')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior UX Researcher',   6000000,  12000000),
  (2, 'UX Researcher',         12000000,  22000000),
  (3, 'Senior UX Researcher',  22000000,  38000000),
  (4, 'Principal Researcher',  38000000,  65000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-researcher')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'UX researcher masih sangat langka di Indonesia — banyak perusahaan baru membuka posisi ini.'),
  (2, 'Mixed methods (kualitatif + kuantitatif) menjadi ekspektasi standar UX researcher senior.'),
  (3, 'Perusahaan yang serius di design-led culture seperti Gojek dan Tokopedia investasi besar di research.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #23: Visual & Brand Designer ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'visual-brand-designer',
    'Visual & Brand Designer',
    (SELECT id FROM profession_main_categories WHERE code = 'DESIGN'),
    (SELECT id FROM profession_sub_categories WHERE code = 'VISUAL'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'A'),
    'Visual & Brand Designer membangun identitas visual yang kuat dan konsisten untuk produk dan perusahaan digital. Dari logo dan color palette hingga ilustrasi dan marketing assets — mereka memastikan brand berbicara dengan satu suara yang memorable.',
    'Profil A (Artistic) paling cocok karena ini adalah peran kreatif murni yang bergantung pada ekspresi visual, sense estetika yang kuat, dan kemampuan bercerita melalui gambar dan warna.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang brand identity: logo, color system, typography, dan brand guidelines'),
  (2, 'Membuat visual assets untuk campaign marketing digital dan social media'),
  (3, 'Mendesain ilustrasi dan icon set yang konsisten dengan brand personality'),
  (4, 'Berkolaborasi dengan marketing team untuk memastikan eksekusi visual on-brand'),
  (5, 'Membangun visual style guide yang bisa digunakan oleh tim secara mandiri'),
  (6, 'Melakukan visual QA sebelum assets dipublish ke channel digital')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'visual-brand-designer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('visual-design','brand-identity','typography','design-system','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'visual-brand-designer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('figma','illustrator','photoshop','after-effects','lottie','notion','slack','jira')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'visual-brand-designer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Visual Designer',   4500000,  9000000),
  (2, 'Visual Designer',          9000000, 18000000),
  (3, 'Senior Visual Designer',  18000000, 30000000),
  (4, 'Brand Design Lead',       30000000, 50000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'visual-brand-designer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Identitas visual yang kuat menjadi keunggulan kompetitif yang semakin diakui startup Indonesia.'),
  (2, 'Kemampuan motion design (After Effects + Lottie) menjadi nilai tambah besar untuk visual designer.'),
  (3, 'Brand designer dengan portfolio di e-commerce atau fintech sangat diminati agensi premium.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #24: Digital Motion Designer ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'digital-motion-designer',
    'Digital Motion Designer',
    (SELECT id FROM profession_main_categories WHERE code = 'DESIGN'),
    (SELECT id FROM profession_sub_categories WHERE code = 'VISUAL'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'AI'),
    'Digital Motion Designer menciptakan animasi, motion graphics, dan video pendek untuk platform digital. Dari onboarding animation di aplikasi mobile hingga explainer video produk — mereka menghidupkan brand dan cerita melalui gerakan yang purposeful.',
    'Profil AI (Artistic-Investigative) cocok karena motion designer membutuhkan ekspresi kreatif yang kuat (Artistic) sekaligus pemahaman teknis tentang prinsip animasi, timing, dan tools (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membuat UI animation dan micro-interaction menggunakan After Effects dan Lottie'),
  (2, 'Memproduksi explainer video dan motion infographic untuk kampanye marketing'),
  (3, 'Berkolaborasi dengan UI designer untuk mengimplementasikan motion language produk'),
  (4, 'Mengeksport animasi ke format yang optimal untuk web (Lottie JSON, WebM, GIF)'),
  (5, 'Membuat storyboard dan animatic sebelum produksi animasi penuh'),
  (6, 'Mengelola asset library animasi yang reusable untuk tim desain')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-motion-designer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('motion-design','visual-design','typography','brand-identity')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-motion-designer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('figma','after-effects','lottie','illustrator','photoshop','notion','slack','jira')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-motion-designer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Motion Designer',   5000000,  9000000),
  (2, 'Motion Designer',          9000000, 18000000),
  (3, 'Senior Motion Designer',  18000000, 32000000),
  (4, 'Motion Design Lead',      32000000, 55000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-motion-designer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Short-form video content mendorong permintaan motion designer yang bisa kerja cepat dan iteratif.'),
  (2, 'Motion designer yang bisa export ke Lottie untuk in-app animation punya nilai lebih tinggi.'),
  (3, 'AI video generation tools mengubah industri — motion designer yang bisa directnya lebih relevan.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #25: UX Writer / Content Designer ────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'ux-writer-content-designer',
    'UX Writer / Content Designer',
    (SELECT id FROM profession_main_categories WHERE code = 'DESIGN'),
    (SELECT id FROM profession_sub_categories WHERE code = 'CONTENT'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'AI'),
    'UX Writer / Content Designer merancang teks dalam produk digital — dari button label dan error message hingga onboarding flow dan empty state. Mereka memastikan setiap kata di produk membantu pengguna mencapai tujuannya dengan mudah dan percaya diri.',
    'Profil AI (Artistic-Investigative) cocok karena UX writing membutuhkan keahlian menulis yang ekspresif dan empatik (Artistic) sekaligus investigasi mendalam tentang perilaku pengguna dan konteks penggunaan (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Menulis dan menyempurnakan microcopy untuk semua touchpoint di produk digital'),
  (2, 'Membangun content guidelines dan tone of voice yang konsisten dengan brand'),
  (3, 'Berkolaborasi dengan designer untuk memastikan teks dan visual saling mendukung'),
  (4, 'Melakukan user testing untuk memvalidasi apakah teks mudah dipahami pengguna'),
  (5, 'Mengelola content inventory dan memastikan konsistensi terminologi di seluruh produk'),
  (6, 'Berkontribusi pada design system sebagai pemilik komponen teks dan pattern library')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-writer-content-designer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('ux-writing','user-research','usability-testing','design-system','accessibility','agile','stakeholder-management')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-writer-content-designer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('figma','miro','notion','dovetail','maze','jira','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-writer-content-designer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior UX Writer',        5000000,  10000000),
  (2, 'UX Writer',              10000000,  18000000),
  (3, 'Senior UX Writer',       18000000,  30000000),
  (4, 'Content Design Lead',    30000000,  50000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ux-writer-content-designer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'UX Writing baru mulai dikenal di Indonesia — masih sangat sedikit yang benar-benar specialist.'),
  (2, 'Perusahaan dengan multilingual product sangat membutuhkan UX writer yang paham lokalisasi.'),
  (3, 'UX writer yang bisa kerja dalam design system dan Figma component secara langsung sangat dihargai.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #26: Digital Product Manager ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'digital-product-manager',
    'Digital Product Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'PRODUCT'),
    (SELECT id FROM profession_sub_categories WHERE code = 'MANAGEMENT'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'E'),
    'Digital Product Manager mendefinisikan visi, strategi, dan roadmap produk digital. Mereka menjadi titik temu antara engineering, design, dan bisnis — memastikan tim membangun produk yang tepat, untuk pengguna yang tepat, pada waktu yang tepat.',
    'Profil E (Enterprising) sangat cocok karena PM digital harus memimpin tanpa otoritas formal, mempengaruhi keputusan lintas tim, dan mengadvokasi visi produk kepada berbagai stakeholder.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mendefinisikan product vision, strategy, dan OKR yang selaras dengan tujuan bisnis'),
  (2, 'Mengelola dan memprioritaskan product backlog berdasarkan value dan effort'),
  (3, 'Melakukan discovery dengan user research dan data untuk memvalidasi arah produk'),
  (4, 'Berkolaborasi dengan engineering dan design untuk memastikan eksekusi yang tepat'),
  (5, 'Mengkomunikasikan roadmap dan progress kepada stakeholder eksekutif secara berkala'),
  (6, 'Menganalisis metrik produk dan menentukan langkah iterasi berdasarkan data')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-product-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('product-strategy','product-roadmap','user-story','ab-testing','product-analytics','user-research','stakeholder-management','agile','market-research','competitor-analysis')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-product-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('productboard','linear','jira','miro','amplitude','mixpanel','figma','notion','slack','notion-ai')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-product-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Associate PM',          8000000,  15000000),
  (2, 'Product Manager',      15000000,  28000000),
  (3, 'Senior PM',            28000000,  50000000),
  (4, 'Director of Product',  50000000, 100000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'digital-product-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'PM dengan background teknis (ex-engineer) sangat dicari untuk memimpin produk B2D atau platform.'),
  (2, 'Kemampuan SQL untuk analisis data sendiri menjadi keunggulan kompetitif PM modern.'),
  (3, 'PM yang punya track record growth metric yang jelas lebih mudah naik ke level Director dan VP.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #27: Product Growth Manager ──────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'product-growth-manager',
    'Product Growth Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'PRODUCT'),
    (SELECT id FROM profession_sub_categories WHERE code = 'GROWTH'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'EC'),
    'Product Growth Manager fokus pada satu hal: membuat produk tumbuh. Mereka mengelola funnel akuisisi hingga retensi, merancang eksperimen, dan mengeksekusi growth loop yang membuat pengguna baru terus datang dan pengguna lama terus kembali.',
    'Profil EC (Enterprising-Conventional) cocok karena growth manager membutuhkan ambisi dan semangat untuk mengeksekusi (Enterprising) sekaligus pendekatan sistematis dan data-driven yang terstruktur (Conventional).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan menjalankan eksperimen growth (A/B test, multivariate test) secara sistematis'),
  (2, 'Menganalisis funnel konversi dan mengidentifikasi friction point yang menghambat aktivasi'),
  (3, 'Berkolaborasi dengan engineering untuk membangun fitur yang mendorong viral dan referral'),
  (4, 'Mengelola product onboarding agar pengguna baru mencapai AHA moment secepat mungkin'),
  (5, 'Memonitor North Star Metric dan leading indicator yang menunjukkan kesehatan growth'),
  (6, 'Berkoordinasi dengan marketing untuk mengoptimalkan paid dan organic acquisition channel')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-growth-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('growth-hacking','ab-testing','conversion-optimization','product-analytics','sql-advanced','user-research','stakeholder-management','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-growth-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('amplitude','mixpanel','google-analytics','hotjar','intercom','jira','notion','slack','airtable')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-growth-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Growth Analyst',          8000000,  14000000),
  (2, 'Growth PM',              14000000,  26000000),
  (3, 'Senior Growth PM',       26000000,  45000000),
  (4, 'Head of Growth',         45000000,  85000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-growth-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Growth PM menjadi peran kritis di startup yang sudah masuk fase scale-up post-PMF.'),
  (2, 'PLG (Product-Led Growth) strategy mendorong permintaan growth PM yang paham self-serve funnel.'),
  (3, 'Growth PM dengan track record meningkatkan activation rate atau retention di produk nyata sangat dicari.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #28: Technical Product Manager ───────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'technical-product-manager',
    'Technical Product Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'PRODUCT'),
    (SELECT id FROM profession_sub_categories WHERE code = 'MANAGEMENT'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'EI'),
    'Technical Product Manager mengelola produk yang sangat teknis — platform, API, developer tools, atau infrastruktur produk. Mereka membutuhkan pemahaman engineering yang dalam untuk berkomunikasi efektif dengan tim teknis dan mengambil keputusan yang mempertimbangkan kompleksitas implementasi.',
    'Profil EI (Enterprising-Investigative) cocok karena Technical PM harus memimpin dan mempengaruhi tim (Enterprising) sekaligus menginvestigasi dan memahami kedalaman teknis produk yang mereka kelola (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mendefinisikan roadmap untuk platform atau API yang digunakan developer internal/eksternal'),
  (2, 'Berkolaborasi langsung dengan arsitek dan senior engineer dalam keputusan teknis besar'),
  (3, 'Menulis PRD yang menyertakan spesifikasi teknis dan acceptance criteria yang detail'),
  (4, 'Mengelola trade-off antara technical debt, fitur baru, dan stabilitas sistem'),
  (5, 'Mengkomunikasikan kompleksitas teknis kepada stakeholder bisnis dengan cara yang mudah dipahami'),
  (6, 'Memimpin inisiatif platform migration atau refactoring besar lintas tim')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-product-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('product-strategy','product-roadmap','system-design','rest-api-design','product-analytics','stakeholder-management','agile','sql-advanced')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-product-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('jira','linear','notion','confluence','miro','postman','amplitude','slack','notion-ai')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-product-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Technical PM',           15000000,  30000000),
  (2, 'Senior Technical PM',   30000000,  55000000),
  (3, 'Group PM / Principal',  55000000,  90000000),
  (4, 'VP Product Technology', 90000000, 160000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'technical-product-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Technical PM dengan background engineering sangat dicari perusahaan yang membangun platform atau API produk.'),
  (2, 'Developer experience (DX) menjadi area produk baru yang butuh TPM yang paham kebutuhan developer.'),
  (3, 'TPM yang bisa baca kode dan review architecture document lebih efektif dari yang hanya bisa manage.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #29: EdTech Learning Designer ────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'edtech-learning-designer',
    'EdTech Learning Designer',
    (SELECT id FROM profession_main_categories WHERE code = 'PRODUCT'),
    (SELECT id FROM profession_sub_categories WHERE code = 'MANAGEMENT'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'SA'),
    'EdTech Learning Designer merancang pengalaman belajar digital yang efektif dan engaging. Mereka menggabungkan prinsip pedagogi, instructional design, dan UX untuk membangun kurikulum dan konten yang benar-benar membantu learner mencapai tujuan belajarnya.',
    'Profil SA (Social-Artistic) sangat cocok karena learning designer perlu kepedulian mendalam terhadap perkembangan orang lain (Social) sekaligus kreativitas dalam merancang pengalaman belajar yang menarik (Artistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang kurikulum pembelajaran digital berdasarkan learning objectives yang terukur'),
  (2, 'Membuat konten pembelajaran: video script, quiz interaktif, dan case study'),
  (3, 'Melakukan learner research untuk memahami kebutuhan dan pain point pengguna platform'),
  (4, 'Berkolaborasi dengan subject matter expert untuk memastikan akurasi dan relevansi konten'),
  (5, 'Menganalisis learning analytics untuk mengidentifikasi konten yang perlu diperbaiki'),
  (6, 'Mendesain assessment dan certification yang valid mengukur kompetensi learner')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'edtech-learning-designer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('user-research','product-analytics','wireframing-prototyping','ux-writing','stakeholder-management','agile','market-research')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'edtech-learning-designer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('figma','notion','miro','airtable','typeform','jira','slack','coda','notion-ai')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'edtech-learning-designer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Learning Designer',          7000000,  14000000),
  (2, 'Senior Learning Designer',  14000000,  26000000),
  (3, 'Lead Learning Designer',    26000000,  42000000),
  (4, 'Head of Learning Design',   42000000,  70000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'edtech-learning-designer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Edtech di Indonesia tumbuh masif pasca pandemi — Ruangguru, Skill Academy, dan Dicoding terus ekspansi.'),
  (2, 'AI-powered personalized learning menciptakan peluang baru untuk learning designer yang tech-savvy.'),
  (3, 'Kombinasi instructional design + data analytics menjadi keunggulan diferensiatif di industri ini.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #30: Product Operations Manager ──────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'product-operations-manager',
    'Product Operations Manager',
    (SELECT id FROM profession_main_categories WHERE code = 'PRODUCT'),
    (SELECT id FROM profession_sub_categories WHERE code = 'OPERATIONS'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'CE'),
    'Product Operations Manager memastikan mesin product development berjalan efisien — dari ritme sprint, tooling, dokumentasi, hingga proses pengambilan keputusan lintas tim. Mereka adalah enabler tersembunyi yang membuat PM lain bisa fokus pada hal yang paling penting.',
    'Profil CE (Conventional-Enterprising) cocok karena Product Ops membutuhkan kecintaan pada sistem dan prosedur yang terstruktur (Conventional) sekaligus proaktif dalam mengidentifikasi dan menyelesaikan hambatan operasional (Enterprising).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan mengoptimalkan proses product development agar lebih efisien dan konsisten'),
  (2, 'Mengelola tooling dan template yang digunakan seluruh tim PM'),
  (3, 'Membangun dan memelihara product wiki dan knowledge base yang dapat diandalkan'),
  (4, 'Menganalisis data velocity dan efisiensi tim untuk mengidentifikasi bottleneck'),
  (5, 'Memfasilitasi retrospective dan quarterly business review untuk continuous improvement'),
  (6, 'Menjadi jembatan komunikasi antara product team dengan stakeholder internal')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-operations-manager')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('product-analytics','stakeholder-management','agile','sql-advanced','product-roadmap')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-operations-manager')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('jira','linear','notion','confluence','airtable','coda','miro','slack','amplitude','notion-ai')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-operations-manager')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Product Ops Specialist',    8000000,  14000000),
  (2, 'Product Ops Manager',      14000000,  25000000),
  (3, 'Senior Product Ops',       25000000,  40000000),
  (4, 'Head of Product Ops',      40000000,  70000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'product-operations-manager')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Product Operations menjadi peran yang semakin dikenal seiring perusahaan tech Indonesia menjadi lebih mature.'),
  (2, 'AI tools untuk documentation dan process automation memperluas scope produktivitas Product Ops.'),
  (3, 'Product Ops yang bisa membangun culture of experimentation di tim product sangat dihargai leadership.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

COMMIT;

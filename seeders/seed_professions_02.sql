-- =============================================================================
-- SEEDER PROFESI DIGITAL — BATCH 02 (Profesi #11–20)
-- Kategori: Frontend Engineering, Data Engineering & AI/ML
-- Prasyarat: seed_professions_01.sql sudah dijalankan (skills & tools dasar sudah ada)
-- Idempotent: pakai INSERT ... ON CONFLICT DO NOTHING
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- 1. SKILLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO skills (slug, name, created_at, updated_at) VALUES
  ('react',                 'React',                    NOW(), NOW()),
  ('nextjs',                'Next.js',                  NOW(), NOW()),
  ('typescript',            'TypeScript',               NOW(), NOW()),
  ('vuejs',                 'Vue.js',                   NOW(), NOW()),
  ('css-tailwind',          'CSS & Tailwind',           NOW(), NOW()),
  ('web-performance',       'Web Performance Optimization', NOW(), NOW()),
  ('accessibility',         'Web Accessibility (WCAG)', NOW(), NOW()),
  ('graphql',               'GraphQL',                  NOW(), NOW()),
  ('sql-advanced',          'SQL Advanced',             NOW(), NOW()),
  ('data-warehousing',      'Data Warehousing',         NOW(), NOW()),
  ('etl-pipeline',          'ETL Pipeline',             NOW(), NOW()),
  ('spark',                 'Apache Spark',             NOW(), NOW()),
  ('kafka',                 'Apache Kafka',             NOW(), NOW()),
  ('dbt',                   'dbt (Data Build Tool)',    NOW(), NOW()),
  ('machine-learning',      'Machine Learning',         NOW(), NOW()),
  ('deep-learning',         'Deep Learning',            NOW(), NOW()),
  ('nlp',                   'Natural Language Processing', NOW(), NOW()),
  ('mlops',                 'MLOps',                    NOW(), NOW()),
  ('feature-engineering',   'Feature Engineering',      NOW(), NOW()),
  ('data-visualization',    'Data Visualization',       NOW(), NOW()),
  ('statistics',            'Statistics & Probability', NOW(), NOW()),
  ('pytorch',               'PyTorch',                  NOW(), NOW()),
  ('tensorflow',            'TensorFlow',               NOW(), NOW()),
  ('llm-fine-tuning',       'LLM Fine-tuning',          NOW(), NOW()),
  ('prompt-engineering',    'Prompt Engineering',       NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 2. TOOLS tambahan batch ini
-- -----------------------------------------------------------------------------
INSERT INTO tools (slug, name, created_at, updated_at) VALUES
  ('figma',           'Figma',                    NOW(), NOW()),
  ('storybook',       'Storybook',                NOW(), NOW()),
  ('chromatic',       'Chromatic',                NOW(), NOW()),
  ('webpack',         'Webpack/Vite',             NOW(), NOW()),
  ('vercel',          'Vercel',                   NOW(), NOW()),
  ('netlify',         'Netlify',                  NOW(), NOW()),
  ('bigquery',        'BigQuery',                 NOW(), NOW()),
  ('snowflake',       'Snowflake',                NOW(), NOW()),
  ('airflow',         'Apache Airflow',           NOW(), NOW()),
  ('dbt-cloud',       'dbt Cloud',                NOW(), NOW()),
  ('jupyter',         'Jupyter Notebook',         NOW(), NOW()),
  ('mlflow',          'MLflow',                   NOW(), NOW()),
  ('weights-biases',  'Weights & Biases',         NOW(), NOW()),
  ('huggingface',     'Hugging Face Hub',         NOW(), NOW()),
  ('colab',           'Google Colab',             NOW(), NOW()),
  ('looker',          'Looker / Looker Studio',   NOW(), NOW()),
  ('metabase',        'Metabase',                 NOW(), NOW()),
  ('tableau',         'Tableau',                  NOW(), NOW()),
  ('firebase',        'Firebase',                 NOW(), NOW()),
  ('amplitude',       'Amplitude',                NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 3. PROFESI #11–20
-- -----------------------------------------------------------------------------

-- ── #11: Frontend Engineer ───────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'frontend-engineer',
    'Frontend Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'FRONTEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Frontend Engineer membangun antarmuka aplikasi web yang performant, aksesibel, dan mudah digunakan. Mereka menjembatani gap antara desain dan engineering — menerjemahkan mockup menjadi komponen interaktif yang berjalan mulus di semua browser dan perangkat.',
    'Profil RI cocok karena frontend engineering membutuhkan implementasi kode yang hands-on (Realistic) sekaligus analisis performa rendering, accessibility, dan optimasi bundle yang mendalam (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun komponen UI reusable menggunakan React/Next.js dan TypeScript'),
  (2, 'Mengoptimalkan performa web: Core Web Vitals, code splitting, dan lazy loading'),
  (3, 'Memastikan aksesibilitas (WCAG 2.1) dan cross-browser compatibility'),
  (4, 'Berkolaborasi dengan designer untuk mengimplementasikan design system'),
  (5, 'Menulis unit test dan visual regression test menggunakan Jest dan Chromatic'),
  (6, 'Mengintegrasikan REST API atau GraphQL endpoint ke komponen frontend')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'frontend-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('react','nextjs','typescript','css-tailwind','web-performance','accessibility','graphql','rest-api-design','git','agile','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'frontend-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('vscode','figma','storybook','chromatic','webpack','vercel','github-actions','sentry','jira','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'frontend-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Frontend Engineer',   5000000,  10000000),
  (2, 'Frontend Engineer',         10000000,  20000000),
  (3, 'Senior Frontend Engineer',  20000000,  35000000),
  (4, 'Lead Frontend Engineer',    35000000,  60000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'frontend-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'React masih mendominasi ekosistem frontend Indonesia, diikuti Vue.js untuk proyek enterprise.'),
  (2, 'Server-side rendering dengan Next.js menjadi standar baru untuk produk yang butuh SEO.'),
  (3, 'Frontend engineer yang paham performance optimization dan Core Web Vitals sangat dicari e-commerce.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #12: Creative Frontend Developer ─────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'creative-frontend-developer',
    'Creative Frontend Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'FRONTEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'AR'),
    'Creative Frontend Developer membangun pengalaman web yang tidak hanya fungsional tapi juga memukau secara visual — animasi kompleks, micro-interaction yang halus, dan efek visual yang membuat produk terasa hidup. Mereka berada di irisan antara engineering dan seni digital.',
    'Profil AR (Artistic-Realistic) sangat cocok karena peran ini menggabungkan ekspresi kreatif dan sense estetika (Artistic) dengan implementasi teknis kode yang presisi dan hands-on (Realistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun animasi dan transisi UI yang smooth menggunakan Framer Motion atau GSAP'),
  (2, 'Mengimplementasikan visualisasi data interaktif menggunakan D3.js atau Three.js'),
  (3, 'Membangun design system dengan komponen yang konsisten dan terdokumentasi di Storybook'),
  (4, 'Berkolaborasi dengan motion designer untuk menerjemahkan animasi After Effects ke kode'),
  (5, 'Mengoptimalkan aset visual (SVG, WebP, font subsetting) untuk performa web'),
  (6, 'Membangun landing page dan marketing site yang conversion-optimized')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'creative-frontend-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('react','typescript','css-tailwind','web-performance','accessibility','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'creative-frontend-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('vscode','figma','storybook','webpack','vercel','netlify','github-actions','jira','slack')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'creative-frontend-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Creative Frontend Dev',   5000000,  10000000),
  (2, 'Creative Frontend Developer',   10000000,  22000000),
  (3, 'Senior Creative Frontend Dev',  22000000,  38000000),
  (4, 'Frontend Tech Lead',            38000000,  60000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'creative-frontend-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Web animation dan micro-interaction menjadi diferensiator kuat di tengah persaingan produk digital.'),
  (2, 'Three.js dan WebGL membuka peluang di industri gaming web dan visualisasi 3D produk.'),
  (3, 'Creative developer yang bisa handle Figma-to-code workflow sangat dicari agency digital premium.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #13: Data Engineer ────────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'data-engineer',
    'Data Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'INFRASTRUCTURE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IR'),
    'Data Engineer membangun dan memelihara pipeline data yang mengalirkan data dari berbagai sumber ke data warehouse untuk analisis. Mereka adalah "tukang ledeng" ekosistem data — tanpa pipeline yang handal, semua analitik dan AI tidak bisa berjalan.',
    'Profil IR cocok karena data engineering membutuhkan investigasi mendalam terhadap kualitas dan aliran data (Investigative) sekaligus implementasi pipeline yang hands-on dan teknis (Realistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun dan memelihara ELT/ETL pipeline menggunakan Airflow dan dbt'),
  (2, 'Merancang skema data warehouse yang efisien untuk analitik dan reporting'),
  (3, 'Memastikan kualitas data melalui data validation, testing, dan monitoring pipeline'),
  (4, 'Mengoptimalkan query BigQuery atau Snowflake untuk mengurangi biaya dan latency'),
  (5, 'Membangun data catalog dan dokumentasi lineage data untuk tim analytics'),
  (6, 'Berkolaborasi dengan data scientist untuk menyediakan feature store yang efisien')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('python','sql-advanced','data-warehousing','etl-pipeline','spark','kafka','dbt','postgresql','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('airflow','dbt-cloud','bigquery','snowflake','jupyter','github-actions','grafana','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Data Engineer',    7000000,  13000000),
  (2, 'Data Engineer',          13000000,  25000000),
  (3, 'Senior Data Engineer',   25000000,  45000000),
  (4, 'Staff Data Engineer',    45000000,  75000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Data Engineering menjadi bottleneck di banyak perusahaan — demand jauh melebihi supply.'),
  (2, 'dbt menjadi standar transformasi data modern yang menggeser stored procedures tradisional.'),
  (3, 'Lakehouse architecture (Delta Lake, Apache Iceberg) menjadi skill diferensiasi yang makin dicari.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #14: Data Analytics Engineer ─────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'data-analytics-engineer',
    'Data Analytics Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'ANALYTICS'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'I'),
    'Data Analytics Engineer berada di persimpangan antara data engineering dan business analytics — membangun data model, dashboard, dan self-serve analytics infrastructure agar tim bisnis bisa mengambil keputusan berbasis data tanpa bergantung pada engineer.',
    'Profil I (Investigative) sangat cocok karena analytics engineering adalah tentang investigasi: menggali data, menemukan pola tersembunyi, dan mengubah angka menjadi insight yang actionable.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun data model analitik menggunakan dbt untuk metrics yang konsisten'),
  (2, 'Membuat dan memelihara dashboard eksekutif di Looker, Metabase, atau Tableau'),
  (3, 'Melakukan ad-hoc analysis untuk menjawab pertanyaan bisnis yang kritis'),
  (4, 'Mendefinisikan dan memastikan konsistensi metrik bisnis di seluruh tim'),
  (5, 'Membangun self-serve analytics tooling agar tim non-teknis bisa eksplorasi data mandiri'),
  (6, 'Berkolaborasi dengan product dan marketing untuk mengidentifikasi leading indicator bisnis')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-analytics-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('sql-advanced','python','dbt','data-warehousing','data-visualization','statistics','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-analytics-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('dbt-cloud','bigquery','looker','metabase','tableau','jupyter','amplitude','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-analytics-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Analytics Engineer',   6000000,  12000000),
  (2, 'Analytics Engineer',         12000000,  22000000),
  (3, 'Senior Analytics Engineer',  22000000,  40000000),
  (4, 'Lead Analytics Engineer',    40000000,  65000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-analytics-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Analytics Engineering menjadi role baru yang populer seiring adopsi data mesh di perusahaan besar.'),
  (2, 'Kemampuan storytelling data dengan visualisasi yang baik menjadi skill yang sangat dihargai.'),
  (3, 'Perusahaan e-commerce dan fintech paling aktif merekrut analytics engineer di Indonesia.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #15: Machine Learning Engineer ───────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'machine-learning-engineer',
    'Machine Learning Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'AI'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'I'),
    'Machine Learning Engineer mengembangkan, melatih, dan men-deploy model ML ke produksi. Mereka menjembatani gap antara data scientist yang meneliti model dengan engineering team yang membutuhkan sistem yang reliabel dan scalable.',
    'Profil I (Investigative) sangat cocok karena ML engineering adalah tentang eksperimentasi ilmiah: merumuskan hipotesis, menguji model, menganalisis hasil, dan mengiterasi untuk menemukan solusi terbaik.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun dan melatih model machine learning untuk use case seperti rekomendasi dan fraud detection'),
  (2, 'Mengimplementasikan MLOps pipeline untuk training, evaluation, dan deployment model otomatis'),
  (3, 'Melakukan feature engineering dan feature selection untuk meningkatkan performa model'),
  (4, 'Monitoring model drift dan memastikan performa model tetap stabil di produksi'),
  (5, 'Berkolaborasi dengan data engineer untuk membangun feature store yang reusable'),
  (6, 'Melakukan A/B testing model dan menganalisis dampak bisnis dari setiap perubahan')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'machine-learning-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('python','machine-learning','deep-learning','feature-engineering','mlops','statistics','sql-advanced','pytorch','tensorflow','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'machine-learning-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('jupyter','mlflow','weights-biases','colab','bigquery','github-actions','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'machine-learning-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior ML Engineer',    8000000,  15000000),
  (2, 'ML Engineer',          15000000,  30000000),
  (3, 'Senior ML Engineer',   30000000,  55000000),
  (4, 'Staff ML Engineer',    55000000,  90000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'machine-learning-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Permintaan ML engineer melonjak signifikan seiring adopsi AI di fintech dan e-commerce Indonesia.'),
  (2, 'MLOps menjadi skill kritis yang membedakan ML engineer dari data scientist pure.'),
  (3, 'Spesialisasi di recommendation system atau fraud detection sangat bernilai di industri e-commerce.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #16: AI/LLM Engineer ─────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'ai-llm-engineer',
    'AI/LLM Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'AI'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'IA'),
    'AI/LLM Engineer membangun produk dan sistem berbasis Large Language Model — dari RAG pipeline, fine-tuning model, hingga AI agent yang bisa menyelesaikan task kompleks secara otonom. Mereka adalah arsitek dari gelombang AI yang sedang mengubah industri.',
    'Profil IA (Investigative-Artistic) cocok karena LLM engineering membutuhkan investigasi mendalam tentang cara kerja model (Investigative) sekaligus kreativitas dalam merancang prompt dan sistem yang menghasilkan output berkualitas (Artistic).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang dan mengimplementasikan RAG (Retrieval Augmented Generation) pipeline untuk knowledge base'),
  (2, 'Melakukan fine-tuning LLM open source (Llama, Mistral) untuk use case spesifik domain'),
  (3, 'Membangun AI agent yang bisa menggunakan tools dan menyelesaikan task multi-step'),
  (4, 'Mengoptimalkan prompt dan sistem prompt untuk konsistensi dan akurasi output AI'),
  (5, 'Evaluasi dan benchmarking model AI menggunakan metrik yang relevan dengan use case'),
  (6, 'Berkolaborasi dengan product team untuk mengintegrasikan AI ke dalam fitur produk')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ai-llm-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('python','nlp','deep-learning','llm-fine-tuning','prompt-engineering','machine-learning','pytorch','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ai-llm-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('jupyter','huggingface','weights-biases','colab','mlflow','github-actions','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ai-llm-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'AI Engineer',              12000000,  25000000),
  (2, 'Senior AI Engineer',       25000000,  50000000),
  (3, 'Staff AI Engineer',        50000000,  90000000),
  (4, 'Principal AI Architect',   90000000,  150000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'ai-llm-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'LLM engineer adalah salah satu profesi paling dicari dan paling langka di 2024–2025.'),
  (2, 'Pengalaman dengan vector database (Pinecone, Weaviate) dan RAG sangat diferensiating.'),
  (3, 'Perusahaan Indonesia mulai serius investasi di AI native product — pipeline talent sangat terbatas.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #17: Data Scientist ───────────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'data-scientist',
    'Data Scientist',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'SCIENCE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'I'),
    'Data Scientist menggunakan metode statistik dan machine learning untuk menjawab pertanyaan bisnis yang kompleks dari data. Mereka menggali insight tersembunyi, membangun model prediktif, dan mengkomunikasikan temuan kepada stakeholder non-teknis.',
    'Profil I (Investigative) sangat cocok karena data science adalah tentang penelitian berbasis data — merumuskan hipotesis, menguji dengan eksperimen, dan menarik kesimpulan yang valid secara statistik.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Melakukan eksplorasi dan analisis data untuk menemukan pola dan anomali yang actionable'),
  (2, 'Membangun model prediktif untuk use case seperti churn prediction dan demand forecasting'),
  (3, 'Merancang dan menganalisis hasil A/B experiment untuk pengambilan keputusan produk'),
  (4, 'Mengkomunikasikan insight dan rekomendasi kepada stakeholder bisnis secara visual'),
  (5, 'Berkolaborasi dengan data engineer untuk mendapatkan dataset yang berkualitas'),
  (6, 'Melakukan causal inference analysis untuk memahami hubungan sebab akibat dari intervensi')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-scientist')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('python','statistics','machine-learning','sql-advanced','feature-engineering','data-visualization','deep-learning','git')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-scientist')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('jupyter','colab','mlflow','bigquery','tableau','metabase','amplitude','jira','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-scientist')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Data Scientist',    7000000,  13000000),
  (2, 'Data Scientist',          13000000,  25000000),
  (3, 'Senior Data Scientist',   25000000,  45000000),
  (4, 'Principal Data Scientist',45000000,  80000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'data-scientist')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Data scientist yang bisa handle end-to-end dari analisis hingga deployment lebih dihargai.'),
  (2, 'Causal inference dan experimental design menjadi skill yang membedakan data scientist senior.'),
  (3, 'Sektor fintech dan healthtech di Indonesia paling banyak merekrut data scientist spesialis.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #18: Database Reliability Engineer ───────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'database-reliability-engineer',
    'Database Reliability Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'DATA'),
    (SELECT id FROM profession_sub_categories WHERE code = 'GOVERNANCE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'CI'),
    'Database Reliability Engineer memastikan database produksi berjalan dengan performa optimal, ketersediaan tinggi, dan disaster recovery yang solid. Mereka menangani skala database dari gigabyte hingga petabyte dan memastikan tidak ada data yang hilang.',
    'Profil CI (Conventional-Investigative) cocok karena DBA modern membutuhkan kepatuhan prosedur yang ketat (Conventional) sekaligus investigasi mendalam saat terjadi performance issue atau corruption (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Mengelola database cluster PostgreSQL/MySQL di produksi termasuk replication dan failover'),
  (2, 'Mengidentifikasi dan mengoptimalkan slow query yang berdampak ke performa produksi'),
  (3, 'Merancang dan menguji disaster recovery plan secara berkala'),
  (4, 'Mengelola database migration dengan zero downtime strategy'),
  (5, 'Monitoring database metrics dan menangani capacity planning untuk pertumbuhan data'),
  (6, 'Mendefinisikan standar database schema dan memastikan adopsi best practices oleh tim')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'database-reliability-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('postgresql','mysql','database-optimization','sql-advanced','redis','monitoring-observability','python','bash-scripting','linux-administration','git')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'database-reliability-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('datagrip','grafana','prometheus','datadog','pagerduty','aws-console','jira','slack','confluence')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'database-reliability-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior DBA/DBE',          7000000,  13000000),
  (2, 'Database Engineer',      13000000,  25000000),
  (3, 'Senior DBE',             25000000,  45000000),
  (4, 'Principal Database Arch',45000000,  75000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'database-reliability-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Perusahaan fintech sangat bergantung pada DRE karena konsistensi data adalah regulatory requirement.'),
  (2, 'PostgreSQL mendominasi stack data produksi startup Indonesia dan keahliannya sangat dicari.'),
  (3, 'Spesialisasi di NewSQL (CockroachDB, TiDB) untuk global scale menjadi niche yang menjanjikan.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #19: Software QA Engineer ─────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'software-qa-engineer',
    'Software QA Engineer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'QUALITY_ASSURANCE'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'C'),
    'Software QA Engineer memastikan produk digital bebas dari bug dan memenuhi standar kualitas sebelum sampai ke pengguna. Mereka merancang strategi testing, menulis automation test, dan menjadi gatekeeper kualitas di setiap siklus development.',
    'Profil C (Conventional) sangat cocok karena QA membutuhkan pendekatan yang sistematis, terstruktur, dan berorientasi pada prosedur — memastikan setiap skenario test dieksekusi dan setiap defect terdokumentasi dengan tepat.',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Merancang test plan dan test case yang komprehensif untuk fitur baru'),
  (2, 'Membangun dan memelihara automation test suite (API test, UI test, performance test)'),
  (3, 'Melakukan regression testing setiap sebelum release untuk memastikan tidak ada regresi'),
  (4, 'Berkolaborasi dengan developer untuk mendefinisikan acceptance criteria yang clear'),
  (5, 'Menganalisis test result dan memprioritaskan bug berdasarkan severity dan impact'),
  (6, 'Mengelola test documentation dan memastikan coverage setiap alur kritis terpenuhi')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'software-qa-engineer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('python','rest-api-design','sql-advanced','ci-cd','git','agile')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'software-qa-engineer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('postman','github-actions','sentry','jira','confluence','slack','notion')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'software-qa-engineer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior QA Engineer',   5000000,  10000000),
  (2, 'QA Engineer',         10000000,  18000000),
  (3, 'Senior QA Engineer',  18000000,  32000000),
  (4, 'QA Lead/Manager',     32000000,  55000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'software-qa-engineer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Shift-left testing dan QA sebagai bagian dari CI/CD menjadi standar di perusahaan digital mature.'),
  (2, 'QA engineer yang bisa code automation test (Playwright, Cypress) lebih dihargai dari manual QA.'),
  (3, 'Peran SDET (Software Development Engineer in Test) menjadi evolusi natural QA engineer di tech company.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

-- ── #20: Full Stack Developer ─────────────────────────────────────────────────
WITH ins AS (
  INSERT INTO professions (
    slug, name, main_category_id, sub_category_id, riasec_code_id,
    about_description, riasec_description, created_at, updated_at
  )
  SELECT
    'full-stack-developer',
    'Full Stack Developer',
    (SELECT id FROM profession_main_categories WHERE code = 'ENGINEERING'),
    (SELECT id FROM profession_sub_categories WHERE code = 'BACKEND'),
    (SELECT id FROM riasec_codes WHERE riasec_code = 'RI'),
    'Full Stack Developer menangani pengembangan dari sisi server (backend) hingga antarmuka pengguna (frontend) — dari database hingga browser. Sangat efektif di startup early-stage yang butuh developer yang bisa bergerak cepat di semua lapisan teknis.',
    'Profil RI cocok karena full stack developer melakukan pekerjaan hands-on di dua sisi teknis sekaligus (Realistic) dan perlu berpikir analitis tentang bagaimana backend dan frontend saling terhubung dengan efisien (Investigative).',
    NOW(), NOW()
  ON CONFLICT (slug) DO NOTHING
  RETURNING id
)
INSERT INTO profession_activities (profession_id, description, sort_order, created_at, updated_at)
SELECT id, act.description, act.sort_order, NOW(), NOW() FROM ins, (VALUES
  (1, 'Membangun fitur end-to-end dari API backend hingga komponen UI frontend'),
  (2, 'Mengelola database schema dan mengoptimalkan query untuk fitur yang sedang dibangun'),
  (3, 'Deploy dan maintain aplikasi di cloud platform seperti AWS atau Vercel'),
  (4, 'Melakukan code review lintas frontend dan backend untuk menjaga kualitas codebase'),
  (5, 'Berkolaborasi langsung dengan product dan designer tanpa lapisan perantara'),
  (6, 'Mengidentifikasi dan memperbaiki performance bottleneck di semua layer aplikasi')
) AS act(sort_order, description)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'full-stack-developer')
INSERT INTO profession_skill_rels (profession_id, skill_id, created_at, updated_at)
SELECT p.id, s.id, NOW(), NOW() FROM p, skills s
WHERE s.slug IN ('nodejs','react','typescript','postgresql','redis','rest-api-design','css-tailwind','git','agile','docker','code-review')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'full-stack-developer')
INSERT INTO profession_tool_rels (profession_id, tool_id, created_at, updated_at)
SELECT p.id, t.id, NOW(), NOW() FROM p, tools t
WHERE t.slug IN ('vscode','postman','datagrip','vercel','github-actions','sentry','jira','slack','notion','figma')
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'full-stack-developer')
INSERT INTO profession_career_paths (profession_id, level_name, estimated_salary_min, estimated_salary_max, sort_order, created_at, updated_at)
SELECT p.id, lv.level_name, lv.sal_min, lv.sal_max, lv.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Junior Full Stack Developer',   5000000,  10000000),
  (2, 'Full Stack Developer',         10000000,  20000000),
  (3, 'Senior Full Stack Developer',  20000000,  36000000),
  (4, 'Lead Full Stack Developer',    36000000,  58000000)
) AS lv(sort_order, level_name, sal_min, sal_max)
ON CONFLICT DO NOTHING;

WITH p AS (SELECT id FROM professions WHERE slug = 'full-stack-developer')
INSERT INTO profession_market_insights (profession_id, description, sort_order, created_at, updated_at)
SELECT p.id, mi.description, mi.sort_order, NOW(), NOW() FROM p, (VALUES
  (1, 'Full stack developer sangat dicari di startup seed-stage yang butuh kecepatan eksekusi.'),
  (2, 'T-shaped skill (satu spesialisasi dalam, selebihnya generalis) lebih dihargai dari yang serba tanggung.'),
  (3, 'Full stack developer yang bisa bootstrap produk sendiri dari nol sangat diminati co-founder teknis.')
) AS mi(sort_order, description)
ON CONFLICT DO NOTHING;

COMMIT;

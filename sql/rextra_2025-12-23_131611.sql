--
-- PostgreSQL database dump
--

\restrict ZPmMUNU8yqbDLaTpjK8PsWL91ImdviZZZahgQh7ypTxxbLFJFBc1CmpIXFP7EM2

-- Dumped from database version 16.10 (Debian 16.10-1.pgdg13+1)
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: career_recommendations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.career_recommendations (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    recommendations_data jsonb NOT NULL,
    top_profession1_id bigint,
    top_profession2_id bigint,
    generated_at timestamp with time zone DEFAULT now(),
    ai_model_used character varying(50) DEFAULT 'gemini-1.5-flash'::character varying NOT NULL
);


ALTER TABLE public.career_recommendations OWNER TO postgres;

--
-- Name: career_recommendations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.career_recommendations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.career_recommendations_id_seq OWNER TO postgres;

--
-- Name: career_recommendations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.career_recommendations_id_seq OWNED BY public.career_recommendations.id;


--
-- Name: careerprofile_test_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.careerprofile_test_sessions (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    session_token character varying(100) NOT NULL,
    status character varying(20) NOT NULL,
    started_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone,
    riasec_completed_at timestamp with time zone,
    ikigai_completed_at timestamp with time zone
);


ALTER TABLE public.careerprofile_test_sessions OWNER TO postgres;

--
-- Name: careerprofile_test_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.careerprofile_test_sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.careerprofile_test_sessions_id_seq OWNER TO postgres;

--
-- Name: careerprofile_test_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.careerprofile_test_sessions_id_seq OWNED BY public.careerprofile_test_sessions.id;


--
-- Name: ikigai_candidate_professions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ikigai_candidate_professions (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    candidates_data jsonb NOT NULL,
    total_candidates bigint NOT NULL,
    generation_strategy character varying(50) DEFAULT '4_tier_expansion'::character varying NOT NULL,
    max_candidates_limit bigint DEFAULT 15 NOT NULL,
    generated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.ikigai_candidate_professions OWNER TO postgres;

--
-- Name: ikigai_candidate_professions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ikigai_candidate_professions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ikigai_candidate_professions_id_seq OWNER TO postgres;

--
-- Name: ikigai_candidate_professions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ikigai_candidate_professions_id_seq OWNED BY public.ikigai_candidate_professions.id;


--
-- Name: ikigai_dimension_scores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ikigai_dimension_scores (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    scores_data jsonb NOT NULL,
    calculated_at timestamp with time zone DEFAULT now(),
    ai_model_used character varying(50) DEFAULT 'gemini-1.5-flash'::character varying NOT NULL,
    total_api_calls bigint DEFAULT 4
);


ALTER TABLE public.ikigai_dimension_scores OWNER TO postgres;

--
-- Name: ikigai_dimension_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ikigai_dimension_scores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ikigai_dimension_scores_id_seq OWNER TO postgres;

--
-- Name: ikigai_dimension_scores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ikigai_dimension_scores_id_seq OWNED BY public.ikigai_dimension_scores.id;


--
-- Name: ikigai_responses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ikigai_responses (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    dimension1_love jsonb NOT NULL,
    dimension2_good_at jsonb NOT NULL,
    dimension3_world_needs jsonb NOT NULL,
    dimension4_paid_for jsonb NOT NULL,
    completed boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone,
    CONSTRAINT valid_completion CHECK ((((completed = false) AND (completed_at IS NULL)) OR ((completed = true) AND (completed_at IS NOT NULL))))
);


ALTER TABLE public.ikigai_responses OWNER TO postgres;

--
-- Name: ikigai_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ikigai_responses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ikigai_responses_id_seq OWNER TO postgres;

--
-- Name: ikigai_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ikigai_responses_id_seq OWNED BY public.ikigai_responses.id;


--
-- Name: ikigai_total_scores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ikigai_total_scores (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    scores_data jsonb NOT NULL,
    top_profession1_id bigint,
    top_profession2_id bigint,
    calculated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.ikigai_total_scores OWNER TO postgres;

--
-- Name: ikigai_total_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ikigai_total_scores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ikigai_total_scores_id_seq OWNER TO postgres;

--
-- Name: ikigai_total_scores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ikigai_total_scores_id_seq OWNED BY public.ikigai_total_scores.id;


--
-- Name: kenalidiri_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kenalidiri_categories (
    id bigint NOT NULL,
    category_code character varying(50) NOT NULL,
    category_name character varying(255) NOT NULL,
    description text,
    detail_table_name character varying(100) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.kenalidiri_categories OWNER TO postgres;

--
-- Name: kenalidiri_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kenalidiri_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kenalidiri_categories_id_seq OWNER TO postgres;

--
-- Name: kenalidiri_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kenalidiri_categories_id_seq OWNED BY public.kenalidiri_categories.id;


--
-- Name: kenalidiri_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kenalidiri_history (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    test_category_id bigint NOT NULL,
    detail_session_id bigint NOT NULL,
    status character varying(20) NOT NULL,
    started_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone
);


ALTER TABLE public.kenalidiri_history OWNER TO postgres;

--
-- Name: kenalidiri_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kenalidiri_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kenalidiri_history_id_seq OWNER TO postgres;

--
-- Name: kenalidiri_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kenalidiri_history_id_seq OWNED BY public.kenalidiri_history.id;


--
-- Name: personas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.personas (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id text NOT NULL,
    institution text NOT NULL,
    study text NOT NULL,
    education_level text NOT NULL,
    graduation_year bigint NOT NULL,
    career_plan text NOT NULL,
    career_dreams text NOT NULL,
    portfolio boolean DEFAULT false NOT NULL,
    application boolean NOT NULL,
    status text NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.personas OWNER TO postgres;

--
-- Name: riasec; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.riasec (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    riasec_code text NOT NULL,
    r_description text,
    idescription text,
    a_description text,
    s_description text,
    e_description text,
    c_description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.riasec OWNER TO postgres;

--
-- Name: riasec_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.riasec_codes (
    id bigint NOT NULL,
    riasec_code character varying(3) NOT NULL,
    riasec_title character varying(255) NOT NULL,
    riasec_description text,
    strengths jsonb DEFAULT '[]'::jsonb NOT NULL,
    challenges jsonb DEFAULT '[]'::jsonb NOT NULL,
    strategies jsonb DEFAULT '[]'::jsonb NOT NULL,
    work_environments jsonb DEFAULT '[]'::jsonb NOT NULL,
    interaction_styles jsonb DEFAULT '[]'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.riasec_codes OWNER TO postgres;

--
-- Name: riasec_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.riasec_codes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.riasec_codes_id_seq OWNER TO postgres;

--
-- Name: riasec_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.riasec_codes_id_seq OWNED BY public.riasec_codes.id;


--
-- Name: riasec_question_sets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.riasec_question_sets (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    question_ids jsonb NOT NULL,
    generated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.riasec_question_sets OWNER TO postgres;

--
-- Name: riasec_question_sets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.riasec_question_sets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.riasec_question_sets_id_seq OWNER TO postgres;

--
-- Name: riasec_question_sets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.riasec_question_sets_id_seq OWNED BY public.riasec_question_sets.id;


--
-- Name: riasec_responses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.riasec_responses (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    responses_data jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.riasec_responses OWNER TO postgres;

--
-- Name: riasec_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.riasec_responses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.riasec_responses_id_seq OWNER TO postgres;

--
-- Name: riasec_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.riasec_responses_id_seq OWNED BY public.riasec_responses.id;


--
-- Name: riasec_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.riasec_results (
    id bigint NOT NULL,
    test_session_id bigint NOT NULL,
    score_r bigint NOT NULL,
    score_i bigint NOT NULL,
    score_a bigint NOT NULL,
    score_s bigint NOT NULL,
    score_e bigint NOT NULL,
    score_c bigint NOT NULL,
    riasec_code_id bigint NOT NULL,
    riasec_code_type character varying(20) NOT NULL,
    is_inconsistent_profile boolean DEFAULT false NOT NULL,
    calculated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.riasec_results OWNER TO postgres;

--
-- Name: riasec_results_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.riasec_results_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.riasec_results_id_seq OWNER TO postgres;

--
-- Name: riasec_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.riasec_results_id_seq OWNED BY public.riasec_results.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id text NOT NULL,
    token text NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    auth_provider text NOT NULL,
    device_info jsonb,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: user_ikigais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_ikigais (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    profile character varying(255) NOT NULL,
    chart_data jsonb NOT NULL,
    hash character varying(255) NOT NULL,
    results jsonb NOT NULL,
    riasec_explanations jsonb NOT NULL,
    riasec_map_full jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.user_ikigais OWNER TO postgres;

--
-- Name: user_riasecs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_riasecs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    profile text NOT NULL,
    normalized_scores jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.user_riasecs OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    profile_image_url text,
    fullname text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    phone_number text NOT NULL,
    role text DEFAULT 'USER'::text NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: career_recommendations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.career_recommendations ALTER COLUMN id SET DEFAULT nextval('public.career_recommendations_id_seq'::regclass);


--
-- Name: careerprofile_test_sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.careerprofile_test_sessions ALTER COLUMN id SET DEFAULT nextval('public.careerprofile_test_sessions_id_seq'::regclass);


--
-- Name: ikigai_candidate_professions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_candidate_professions ALTER COLUMN id SET DEFAULT nextval('public.ikigai_candidate_professions_id_seq'::regclass);


--
-- Name: ikigai_dimension_scores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_dimension_scores ALTER COLUMN id SET DEFAULT nextval('public.ikigai_dimension_scores_id_seq'::regclass);


--
-- Name: ikigai_responses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_responses ALTER COLUMN id SET DEFAULT nextval('public.ikigai_responses_id_seq'::regclass);


--
-- Name: ikigai_total_scores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_total_scores ALTER COLUMN id SET DEFAULT nextval('public.ikigai_total_scores_id_seq'::regclass);


--
-- Name: kenalidiri_categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kenalidiri_categories ALTER COLUMN id SET DEFAULT nextval('public.kenalidiri_categories_id_seq'::regclass);


--
-- Name: kenalidiri_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kenalidiri_history ALTER COLUMN id SET DEFAULT nextval('public.kenalidiri_history_id_seq'::regclass);


--
-- Name: riasec_codes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_codes ALTER COLUMN id SET DEFAULT nextval('public.riasec_codes_id_seq'::regclass);


--
-- Name: riasec_question_sets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_question_sets ALTER COLUMN id SET DEFAULT nextval('public.riasec_question_sets_id_seq'::regclass);


--
-- Name: riasec_responses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_responses ALTER COLUMN id SET DEFAULT nextval('public.riasec_responses_id_seq'::regclass);


--
-- Name: riasec_results id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_results ALTER COLUMN id SET DEFAULT nextval('public.riasec_results_id_seq'::regclass);


--
-- Data for Name: career_recommendations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.career_recommendations (id, test_session_id, recommendations_data, top_profession1_id, top_profession2_id, generated_at, ai_model_used) FROM stdin;
\.


--
-- Data for Name: careerprofile_test_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.careerprofile_test_sessions (id, user_id, session_token, status, started_at, completed_at, riasec_completed_at, ikigai_completed_at) FROM stdin;
\.


--
-- Data for Name: ikigai_candidate_professions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ikigai_candidate_professions (id, test_session_id, candidates_data, total_candidates, generation_strategy, max_candidates_limit, generated_at) FROM stdin;
\.


--
-- Data for Name: ikigai_dimension_scores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ikigai_dimension_scores (id, test_session_id, scores_data, calculated_at, ai_model_used, total_api_calls) FROM stdin;
\.


--
-- Data for Name: ikigai_responses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ikigai_responses (id, test_session_id, dimension1_love, dimension2_good_at, dimension3_world_needs, dimension4_paid_for, completed, created_at, completed_at) FROM stdin;
\.


--
-- Data for Name: ikigai_total_scores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ikigai_total_scores (id, test_session_id, scores_data, top_profession1_id, top_profession2_id, calculated_at) FROM stdin;
\.


--
-- Data for Name: kenalidiri_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kenalidiri_categories (id, category_code, category_name, description, detail_table_name, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: kenalidiri_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kenalidiri_history (id, user_id, test_category_id, detail_session_id, status, started_at, completed_at) FROM stdin;
\.


--
-- Data for Name: personas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.personas (id, user_id, institution, study, education_level, graduation_year, career_plan, career_dreams, portfolio, application, status, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: riasec; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.riasec (id, user_id, riasec_code, r_description, idescription, a_description, s_description, e_description, c_description, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: riasec_codes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.riasec_codes (id, riasec_code, riasec_title, riasec_description, strengths, challenges, strategies, work_environments, interaction_styles, created_at, updated_at) FROM stdin;
1	R	Realistic (R)	Profil Realistic menunjukkan bahwa kamu adalah tipe yang lebih nyaman dengan pekerjaan praktis dan konkret dibandingkan hal yang abstrak. Berdasarkan pengalaman saya sebagai praktisi psikologi industri dan organisasi, individu dengan profil ini biasanya sangat baik dalam pelaksanaan teknis dan implementasi. Kamu cenderung lebih menyukai pendekatan "langsung mengerjakan" daripada menghabiskan waktu berjam-jam dalam rapat perencanaan. Di kampus, kamu mungkin lebih menikmati praktikum atau kerja laboratorium dibanding kuliah teori murni. Kekuatan khas dari tipe Realistic adalah kemampuanmu dalam memecahkan masalah teknis secara sistematis.	["Pemecah masalah yang praktis: Kamu cenderung berpikir dalam pola \\"apa yang bisa saya lakukan sekarang\\" daripada hanya berteori tanpa tindakan", "Teliti dalam hal teknis: Ketika menangani peralatan, sistem, atau proses teknis, kamu secara natural memperhatikan detail penting", "Pembelajar mandiri: Kamu tidak membutuhkan pengawasan atau bimbingan terus-menerus", "Dapat diandalkan dalam eksekusi: Ketika kamu berkomitmen untuk menyelesaikan sesuatu, orang lain bisa mengandalkanmu"]	["Kurang sabar dengan diskusi abstrak: Pembahasan yang terlalu konseptual tanpa rencana aksi yang jelas bisa membuatmu frustrasi", "Kesulitan menjelaskan kepada orang awam: Menjelaskan hal teknis kepada orang yang tidak memiliki latar belakang sama adalah tantangan tersendiri", "Tidak nyaman dengan perubahan mendadak: Kamu cenderung lebih menyukai metode yang sudah terbukti berhasil"]	["Latih kemampuan menjelaskan: Berlatihlah menjelaskan hal teknis menggunakan analogi atau contoh sehari-hari", "Bangun kebiasaan dokumentasi: Biasakan untuk mendokumentasikan proses kerjamu", "Cari kolaborasi lintas bidang: Bekerjalah secara aktif dengan orang dari fungsi atau latar belakang berbeda"]	["Spesifikasi yang jelas: Kamu berkembang optimal ketika persyaratan kerja dan hasil yang diharapkan terdefinisi dengan baik", "Akses ke alat yang tepat: Memiliki alat yang tepat sangat penting untuk kualitas kerjamu", "Penilaian berbasis kinerja: Lingkungan kerja di mana penilaian didasarkan pada hasil kerja konkret"]	["Komunikasi langsung dan faktual: Dalam berkomunikasi, kamu cenderung langsung ke inti permasalahan", "Lebih suka mendemonstrasikan: Ketika menjelaskan sesuatu, kamu cenderung lebih suka menunjukkan langsung", "Nyaman dengan keheningan: Kamu merasa nyaman bekerja dalam suasana tenang"]	2025-12-23 06:15:22.16977+00	2025-12-23 06:15:22.16977+00
2	I	Investigative (I)	Tipe Investigative pada dasarnya adalah individu yang selalu bertanya "mengapa". Kamu tidak bisa puas hanya dengan pemahaman di permukaan. Individu dengan profil ini sering kali unggul dalam bidang yang memerlukan analisis mendalam dan pemikiran sistematis. Kamu mungkin adalah tipe orang yang benar-benar membaca jurnal penelitian untuk kesenangan pribadi, atau yang selalu penasaran dengan cara kerja sesuatu.	["Kemampuan analitis yang tinggi: Kamu bisa memproses informasi kompleks dan mengidentifikasi pola yang tidak langsung terlihat oleh orang lain", "Menguasai metodologi penelitian: Kamu nyaman dengan penyelidikan yang sistematis", "Berpikir kritis: Kamu tidak begitu saja menerima informasi yang diberikan", "Mampu mengintegrasikan konsep: Kamu terampil dalam menghubungkan ide dari berbagai bidang"]	["Terlalu banyak menganalisis: Terkadang kamu menghabiskan terlalu banyak waktu untuk menganalisis hingga terlambat mengambil tindakan", "Tidak sabar dengan pendekatan dangkal: Ketika orang lain mengambil jalan pintas, hal ini mengganggu kamu", "Kesenjangan dalam berkomunikasi: Penjelasanmu bisa menjadi terlalu teknis atau rinci"]	["Tetapkan batas waktu untuk analisis: Berikan dirimu tenggat waktu yang jelas untuk fase penelitian", "Latih pengambilan keputusan yang cukup baik: Kembangkan intuisi untuk mengetahui kapan informasi 70-80 persen sudah cukup", "Berkolaborasi dengan tipe pelaksana: Bermitra dengan orang yang cenderung langsung bertindak"]	["Otonomi intelektual: Kamu memerlukan kebebasan untuk mengejar penyelidikan dengan caramu sendiri", "Akses ke sumber informasi: Kamu memerlukan akses ke sumber daya untuk memenuhi kebutuhan risetmu", "Budaya yang menghargai kerja mendalam: Lingkungan yang memahami bahwa analisis berkualitas memerlukan waktu"]	["Komunikasi berbasis pertanyaan: Cara alami kamu berkomunikasi adalah dengan mengajukan pertanyaan", "Diskusi berbasis bukti: Kamu selalu membawa data dan rujukan penelitian untuk mendukung argumenmu", "Lebih suka komunikasi tertulis: Kamu sering merasa lebih nyaman dengan komunikasi tertulis"]	2025-12-23 06:15:22.174571+00	2025-12-23 06:15:22.174571+00
3	A	Artistic (A)	Profil Artistic menunjukkan bahwa kamu adalah seseorang yang melihat dunia melalui lensa kemungkinan dan orisinalitas. Kamu mungkin merasa terkekang ketika diminta untuk "ikuti saja format yang sudah ada". Tipe Artistic ini bukan hanya tentang seni visual, ini tentang pendekatan kreatif dan inovatif terhadap masalah di bidang apa pun.	["Pemikiran divergen: Ketika orang lain melihat satu solusi standar, kamu melihat berbagai kemungkinan alternatif", "Kepekaan estetika: Kamu memiliki kepekaan terhadap desain, komposisi, dan presentasi", "Nyaman dengan ketidakpastian: Kamu justru nyaman dengan masalah yang terbuka", "Motivasi dari dalam: Kamu didorong oleh kepuasan internal dari proses menciptakan sesuatu"]	["Mudah bosan dengan rutinitas: Tugas yang repetitif dan monoton dengan cepat menguras energi mentalmu", "Tekanan tenggat waktu: Proses kreatifmu mungkin tidak selalu sejalan dengan jadwal yang kaku", "Sensitif terhadap kritik: Umpan balik negatif bisa terasa sangat personal"]	["Ciptakan sistem untuk kreativitas: Strukturkan rutinitas kerjamu untuk melindungi waktu kreatif", "Minta umpan balik di tahap awal: Jangan menunggu sampai karya sudah hampir selesai untuk mendapatkan masukan", "Belajar menghargai batasan: Terkadang keterbatasan justru memaksa munculnya kreativitas yang lebih baik"]	["Jadwal yang fleksibel: Fleksibilitas untuk bekerja pada jam-jam puncak produktivitas kreatifmu sangat penting", "Ruang kerja yang menginspirasi: Lingkungan fisikmu sangat memengaruhi output", "Budaya yang mendukung eksperimen: Lingkungan yang memberikan ruang untuk mencoba-coba tanpa takut gagal"]	["Komunikasi yang ekspresif: Kamu menggunakan bahasa yang hidup, metafora, atau alat bantu visual", "Berpikir melalui cerita: Kamu lebih suka menyampaikan ide melalui narasi", "Menikmati sesi curah gagasan: Diskusi untuk menghasilkan ide secara kolaboratif memberimu energi"]	2025-12-23 06:15:22.18073+00	2025-12-23 06:15:22.18073+00
4	S	Social (S)	Profil Social menunjukkan bahwa kamu adalah seseorang yang mendapatkan makna dari dampak positif yang kamu berikan kepada orang lain. Tipe Social sering menjadi jangkar kecerdasan emosional dalam tim. Tipe Social adalah tentang koneksi, memahami bahwa kesuksesan profesional sangat terkait erat dengan kualitas hubungan antarmanusia.	["Empati yang tinggi: Kamu bisa membaca dinamika emosional yang mungkin terlewat oleh orang lain", "Jembatan komunikasi: Kamu terampil dalam memfasilitasi komunikasi antara orang atau kelompok yang berbeda", "Meningkatkan kohesi tim: Kehadiranmu sering meningkatkan semangat dan kekompakan tim", "Sabar dalam pengembangan: Kamu memiliki kesabaran untuk melihat orang berkembang"]	["Kelelahan emosional: Terus-menerus mengelola emosi orang lain bisa sangat menguras energi", "Kesulitan menghadapi konflik: Menghindari percakapan yang sulit demi menjaga harmoni bisa berdampak buruk", "Sulit mengatakan tidak: Menolak permintaan orang lain terasa seperti mengecewakan mereka"]	["Tetapkan batasan yang jelas: Tidak apa-apa untuk memiliki batasan", "Kembangkan ketegasan: Berlatih menyatakan kebutuhanmu sendiri dengan cara diplomatis", "Jadwalkan waktu untuk diri sendiri: Secara harfiah blokir waktu untuk mengisi ulang energi"]	["Budaya kolaboratif: Lingkungan yang menghargai kerja tim dan kesuksesan bersama", "Misi yang bermakna: Organisasi yang tujuannya mencakup dampak positif kepada masyarakat", "Kesempatan berinteraksi: Kamu membutuhkan kontak manusia secara regular"]	["Pendengar aktif: Kamu memberikan perhatian penuh dan menunjukkan ketertarikan yang tulus", "Pendekatan yang hangat: Gaya komunikasimu membuat orang merasa nyaman", "Membangun konsensus: Kamu sering bekerja untuk menemukan titik temu yang bisa diterima semua pihak"]	2025-12-23 06:15:22.185495+00	2025-12-23 06:15:22.185495+00
5	E	Enterprising (E)	Tipe Enterprising adalah tentang dorongan untuk mencapai sesuatu dan memberikan pengaruh. Individu dengan profil Enterprising memiliki energi yang tidak pernah berhenti untuk mewujudkan sesuatu. Tipe Enterprising bukan otomatis berarti otoriter, ini tentang memiliki visi dan mengambil inisiatif untuk merealisasikannya.	["Inisiatif kepemimpinan: Kamu tidak menunggu izin atau kondisi sempurna untuk bertindak", "Komunikasi yang persuasif: Kamu bisa mengartikulasikan visi dengan cara yang menarik", "Pemikiran strategis: Kamu berpikir tentang posisi, keunggulan kompetitif, dan tujuan jangka panjang", "Ketahanan mental: Kemunduran tidak menghentikanmu"]	["Tidak sabar dengan proses yang lambat: Birokrasi atau proses pembangunan konsensus yang panjang membuatmu frustrasi", "Terlalu blak-blakan: Fokusmu pada hasil bisa terkesan tidak sensitif", "Titik buta terhadap risiko: Kepercayaan diri pada keputusanmu bisa membuat kamu meremehkan risiko"]	["Kembangkan kesabaran: Kenali bahwa dukungan dari orang lain sering memerlukan proses", "Praktikkan kepemimpinan yang empatik: Seimbangkan fokus pada tugas dengan perhatian terhadap kebutuhan tim", "Belajar memberdayakan orang lain: Investasikan waktu dalam mengembangkan kemampuan orang lain"]	["Dinamika yang cepat: Lingkungan yang bergerak cepat dan melihat hasil secara konkret", "Budaya kewirausahaan: Organisasi yang menghargai inisiatif dan pengambilan risiko", "Metrik kinerja yang jelas: Mengetahui seperti apa kesuksesan itu dan bagaimana diukur"]	["Kehadiran yang percaya diri: Kamu memancarkan keyakinan yang membuat orang percaya", "Komunikasi langsung: Kamu menghargai efisiensi, tidak bertele-tele", "Energi yang memotivasi: Antusiasme kamu menular"]	2025-12-23 06:15:22.190443+00	2025-12-23 06:15:22.190443+00
6	C	Conventional (C)	Profil Conventional menandakan bahwa kamu berkembang dengan struktur, keteraturan, dan praktik yang sudah mapan. Tipe Conventional adalah tulang punggung yang memastikan operasional berjalan lancar. Tipe Conventional bukan tentang menjadi kaku atau tidak kreatif, ini tentang mengenali nilai dari sistem yang terbukti efektif.	["Keunggulan organisasional: Kamu menciptakan dan memelihara sistem yang meningkatkan efisiensi", "Perhatian pada detail: Kesalahan atau inkonsistensi yang terlewat oleh orang lain tertangkap olehmu", "Dapat diandalkan: Ketika kamu berkomitmen pada tenggat waktu, itu akan terjadi", "Dokumentasi proses: Kamu secara natural mendokumentasikan prosedur"]	["Resistensi terhadap perubahan: Sistem baru atau perubahan mendadak terasa tidak nyaman", "Perfeksionisme yang melumpuhkan: Mengejar kesempurnaan bisa menunda kemajuan", "Improvisasi terbatas: Ketika situasi memerlukan adaptasi cepat, kamu mungkin merasa kehilangan arah"]	["Praktikkan perubahan bertahap: Berlatihlah beradaptasi dengan perubahan kecil secara teratur", "Tetapkan standar yang cukup baik: Tidak semuanya memerlukan presisi maksimal", "Hargai pendekatan berbeda: Secara aktif cari perspektif dari tipe yang kurang terstruktur"]	["Struktur organisasi yang jelas: Mengetahui garis pelaporan dan tanggung jawab memberikan kenyamanan", "Lingkungan yang stabil: Prediktabilitas dalam operasi, minim kejutan", "Standar yang terdefinisi: Organisasi dengan tolok ukur kualitas yang jelas"]	["Formalitas profesional: Kamu lebih suka tingkat formalitas yang sesuai", "Dokumentasi tertulis: Kamu lebih suka mengkomunikasikan hal penting secara tertulis", "Rapat yang terstruktur: Diskusi yang dipandu agenda adalah preferensimu"]	2025-12-23 06:15:22.194912+00	2025-12-23 06:15:22.194912+00
7	RA	Realistic Artistic (RA)	Realistic dan Artistic adalah kombinasi menarik yang menggabungkan eksekusi praktis dengan visi kreatif. Kamu adalah tipe yang bisa membayangkan sesuatu yang original dan benar-benar membangunnya. Pikirkan desainer produk, arsitek, pengrajin, atau teknolog kreatif.	["Pembuatan prototipe kreatif: Kamu bisa dengan cepat menerjemahkan konsep kreatif menjadi prototipe nyata", "Keseimbangan estetika dan fungsional: Karyamu tidak hanya berfungsi tetapi juga terlihat tepat", "Kreativitas langsung: Berbeda dengan tipe Artistic murni, kamu benar-benar mewujudkan ide", "Pemecahan masalah dengan gaya: Kamu menemukan cara kreatif untuk memecahkan masalah praktis"]	["Frustrasi dengan murni estetis atau murni fungsional: Kamu menginginkan keduanya", "Kesulitan estimasi waktu: Proses kreatif memakan waktu yang tidak terduga", "Perfeksionisme dalam kerajinan: Standar kualitas yang tinggi bisa melumpuhkan"]	["Tetapkan batasan kreatif: Gunakan keterbatasan sebagai tantangan kreatif", "Pisahkan ideasi dari eksekusi: Miliki fase terpisah untuk curah gagasan", "Bangun portofolio: Dokumentasikan karyamu untuk menunjukkan kemampuan"]	["Ruang pembuat: Akses ke alat dan kebebasan kreatif", "Studio desain: Lingkungan yang menghargai bentuk dan fungsi", "Proses kreatif fleksibel: Ruang untuk eksperimen dalam batasan proyek"]	["Komunikasi visual: Penggunaan berat sketsa, prototipe, atau referensi visual", "Demonstrasi kemampuan: Lebih suka tunjukkan portofolio daripada penjelasan verbal", "Apresiasi untuk kerajinan: Menghormati keterampilan teknis dan kepekaan estetika"]	2025-12-23 06:15:22.198739+00	2025-12-23 06:15:22.198739+00
8	RC	Realistic Conventional (RC)	Realistic dan Conventional adalah kombinasi ideal untuk peran yang memerlukan presisi, keandalan, dan eksekusi sistematis. Kamu adalah spesialis teknis yang juga mencintai organisasi dan prosedur yang tepat. Pikirkan jaminan kualitas, spesialis dokumentasi teknis, atau administrator sistem.	["Pola pikir jaminan kualitas: Secara natural memeriksa dan memverifikasi pekerjaan teknis", "Dokumentasi proses: Unggul dalam membuat prosedur operasi standar", "Eksekusi konsisten: Karyamu memiliki variasi minimal dengan output kualitas yang dapat diandalkan", "Organisasi teknis: Bisa mengorganisir sistem atau informasi teknis yang kompleks"]	["Kekakuan dalam metode: Preferensi untuk prosedur yang teruji bisa menolak inovasi", "Perfeksionisme menunda: Ingin semuanya benar bisa memperlambat pengiriman", "Resistensi perubahan: Preferensi ganda untuk stabilitas bisa membuat adaptasi sulit"]	["Jadwalkan waktu inovasi: Sisihkan waktu khusus untuk menjelajahi metode baru", "Gunakan pola pikir kontrol versi: Perubahan oke sebagai peningkatan bertahap", "Bermitra dengan tipe fleksibel: Berkolaborasi dengan orang yang bisa mendorongmu keluar zona nyaman"]	["Lingkungan dengan prosedur jelas: Tempat di mana standar operasi sudah terdefinisi", "Peran jaminan kualitas: Posisi yang menghargai ketelitian dan konsistensi", "Tim teknis yang terorganisir: Kolega yang menghargai pendekatan sistematis"]	["Komunikasi terstruktur: Preferensi untuk format laporan yang konsisten", "Dokumentasi sebagai standar: Harapan bahwa semua proses terdokumentasi", "Pertemuan terjadwal: Lebih suka rapat dengan agenda yang jelas"]	2025-12-23 06:15:22.201846+00	2025-12-23 06:15:22.201846+00
9	RE	Realistic Enterprising (RE)	Realistic dan Enterprising menggabungkan kemampuan teknis dengan dorongan untuk mencapai dan memimpin. Kamu bukan hanya ahli teknis, kamu ingin menerapkan keterampilan teknis untuk kesuksesan bisnis atau kepemimpinan. Pikirkan pendiri teknis, manajer operasi, atau pemimpin proyek di bidang teknis.	["Kepemimpinan teknis: Bisa memimpin tim teknis dengan kredibel karena memahami pekerjaannya", "Eksekusi berbasis hasil: Fokus pada output praktis yang penting untuk tujuan bisnis", "Kepercayaan implementasi: Bersedia membuat keputusan dan mengeksekusi tanpa informasi sempurna", "Optimasi sumber daya: Praktis tentang sumber daya yang dibutuhkan"]	["Tidak sabar dengan kepemimpinan non-teknis: Frustrasi ketika orang non-teknis membuat keputusan teknis", "Terlalu percaya diri dalam kelayakan: Kadang meremehkan kompleksitas", "Kesulitan delegasi: Lebih suka melakukan sendiri"]	["Kembangkan kecerdasan bisnis: Pelajari aspek keuangan, pemasaran, atau strategis", "Praktikkan kepemimpinan inklusif: Kenali bahwa tidak semua orang perlu teknis untuk berkontribusi", "Bangun tim teknis: Investasi dalam merekrut dan mengembangkan orang"]	["Perusahaan teknis: Organisasi di mana keahlian teknis dihargai dalam kepemimpinan", "Budaya berorientasi hasil: Fokus pada pengiriman dan hasil", "Peluang kewirausahaan: Ruang untuk inisiatif dalam arah teknis dan bisnis"]	["Kepemimpinan teknis langsung: Instruksi jelas berdasarkan pemahaman praktis", "Rapat berorientasi aksi: Diskusi yang mengarah pada keputusan", "Komunikasi hasil: Membingkai update dalam hal apa yang telah dicapai"]	2025-12-23 06:15:22.205138+00	2025-12-23 06:15:22.205138+00
10	RI	Realistic Investigative (RI)	Kombinasi Realistic dan Investigative menciptakan tipe yang menggabungkan kemampuan praktis dengan pemikiran analitis. Ini adalah kombinasi langka yang sangat berharga di bidang teknis. Kamu bukan hanya bisa mengeksekusi, tetapi juga memahami teori di baliknya.	["Sintesis teknis dan analitis: Kamu bisa merancang eksperimen atau sistem dan juga mengimplementasikannya sendiri", "Diagnosis masalah: Kamu mendekati pemecahan masalah secara sistematis dengan membentuk hipotesis", "Penerjemahan penelitian: Kamu bisa mengambil konsep teoretis dan membangun aplikasi praktis", "Praktik berbasis bukti: Keputusanmu berdasarkan data dan pengujian"]	["Tidak sabar dengan teori murni atau eksekusi murni: Kamu frustrasi kalau terjebak hanya melakukan salah satu", "Komunikasi dengan orang non-teknis: Menjelaskan pekerjaanmu adalah tantangan ganda", "Perfeksionisme dalam metodologi: Menginginkan teori dan implementasi sempurna bisa memperlambatmu"]	["Cari peran yang hybrid: Cari posisi yang menggabungkan riset dengan implementasi", "Dokumentasikan alasanmu: Ketika mengimplementasikan, jelaskan mengapa", "Tetapkan tujuan iterasi: Rencanakan untuk beberapa versi"]	["Lingkungan riset dan pengembangan: Laboratorium atau tim inovasi", "Otonomi teknis: Kebebasan untuk merancang pendekatan dan mengeksekusinya", "Sumber daya untuk eksperimen: Akses ke alat, data, dan anggaran untuk menguji ide"]	["Tunjukkan dan jelaskan: Kamu lebih suka mendemonstrasikan sambil menjelaskan logikanya", "Menghargai dialog teknis: Menikmati diskusi yang menyeimbangkan teori dengan praktis", "Dokumentasi teknis tertulis: Preferensi kuat untuk dokumentasi yang detail"]	2025-12-23 06:15:22.20911+00	2025-12-23 06:15:22.20911+00
11	RS	Realistic Social (RS)	Kombinasi Realistic dan Social menciptakan individu yang praktis tetapi juga berorientasi pada orang. Kamu adalah penolong praktis yang lebih suka membantu orang lain melalui tindakan nyata daripada hanya dukungan emosional. Pikirkan terapis okupasi, pelatih, atau spesialis dukungan teknis.	["Bantuan terapan: Kamu memecahkan masalah orang melalui solusi praktis, bukan hanya simpati", "Instruktur yang sabar: Bisa mengajarkan keterampilan teknis dengan cara yang mudah diakses", "Implementasi tim: Baik dalam memimpin eksekusi dan memastikan semua orang termasuk", "Kolaborasi langsung: Lebih suka bekerja bersama orang daripada koordinasi murni"]	["Pekerjaan emosional kurang terlihat: Bantuan praktismu mungkin kurang terlihat dibanding dukungan emosional", "Menyeimbangkan tugas versus orang: Kadang terjebak antara menyelesaikan tugas dan mengurus tim", "Preferensi komunikasi: Lebih suka tunjukkan daripada berbicara"]	["Artikulasikan gaya dukunganmu: Bantu orang lain memahami bahwa caramu peduli adalah melalui tindakan", "Kembangkan pengecekan verbal: Latih bertanya \\"bagaimana kabarmu\\" di luar pertanyaan tugas", "Cari peran layanan: Cari karier yang menggabungkan keterampilan teknis dengan dampak pada orang"]	["Berorientasi layanan: Organisasi fokus pada membantu melalui solusi praktis", "Proyek berbasis tim: Lingkungan kerja kolaboratif", "Budaya pelatihan langsung: Di mana pengembangan keterampilan terjadi melalui melakukan bersama"]	["Dukungan berorientasi aksi: Respons alami kamu adalah \\"Biar saya bantu kamu dengan itu\\"", "Melakukan kolaboratif: Lebih suka bekerja bersama daripada diskusi murni", "Saran praktis: Ketika orang berbagi masalah, kamu menawarkan solusi konkret"]	2025-12-23 06:15:22.212359+00	2025-12-23 06:15:22.212359+00
12	IA	Investigative Artistic (IA)	Investigative dan Artistic menggabungkan riset mendalam dengan kreativitas. Kamu adalah pemikir yang tidak hanya ingin memahami dunia tetapi juga mengekspresikan pemahaman itu dengan cara yang unik dan inovatif. Pikirkan peneliti desain, ilmuwan yang juga seniman, atau inovator konseptual.	["Riset kreatif: Kamu mendekati pertanyaan riset dengan cara yang tidak konvensional", "Sintesis ide: Terampil dalam menghubungkan konsep dari bidang yang berbeda", "Komunikasi temuan yang menarik: Bisa menyajikan riset dengan cara yang menarik secara visual atau naratif", "Inovasi berbasis bukti: Kreativitasmu didasarkan pada pemahaman yang mendalam"]	["Ketegangan antara ketelitian dan kebebasan: Kadang standar riset bertentangan dengan eksplorasi kreatif", "Kesulitan menyederhanakan: Menjelaskan temuan kompleks dengan cara sederhana adalah tantangan", "Waktu untuk keduanya: Riset mendalam dan ekspresi kreatif keduanya memerlukan waktu"]	["Tentukan fase: Berikan waktu terpisah untuk riset murni dan eksplorasi kreatif", "Temukan medium yang tepat: Identifikasi cara mengekspresikan temuan yang cocok dengan kekuatanmu", "Cari audiens yang menghargai keduanya: Komunitas yang menghargai rigor dan kreativitas"]	["Institusi riset interdisipliner: Tempat yang menghargai pendekatan lintas bidang", "Laboratorium inovasi: Lingkungan yang mendorong eksperimen berbasis riset", "Media atau penerbitan khusus: Platform yang menyajikan riset dengan cara kreatif"]	["Presentasi yang visual dan substantif: Menggabungkan kedalaman dengan presentasi menarik", "Diskusi konseptual: Menikmati eksplorasi ide-ide besar", "Penulisan yang ekspresif: Mengkomunikasikan temuan dengan gaya personal"]	2025-12-23 06:15:22.215465+00	2025-12-23 06:15:22.215465+00
13	IC	Investigative Conventional (IC)	Investigative dan Conventional menggabungkan analisis mendalam dengan kecintaan pada sistem dan organisasi. Kamu adalah peneliti yang sangat metodis dan terorganisir. Pikirkan analis data, auditor, atau peneliti dengan fokus pada metodologi ketat.	["Metodologi yang ketat: Kamu merancang dan mengikuti protokol penelitian dengan teliti", "Dokumentasi komprehensif: Semua langkah riset terdokumentasi dengan baik", "Analisis yang dapat direplikasi: Pekerjaanmu bisa diverifikasi dan diulangi oleh orang lain", "Manajemen data yang sistematis: Terampil dalam mengorganisir dan memelihara dataset"]	["Fleksibilitas terbatas: Kadang terlalu terikat pada protokol yang sudah ditetapkan", "Kesulitan dengan ambiguitas: Lebih nyaman dengan pertanyaan riset yang terdefinisi dengan jelas", "Waktu untuk dokumentasi: Ketelitian dalam dokumentasi memakan waktu signifikan"]	["Bangun fleksibilitas terstruktur: Sisipkan titik evaluasi dalam protokol untuk memungkinkan penyesuaian", "Terima ketidakpastian sebagai bagian riset: Kenali bahwa beberapa ambiguitas adalah normal", "Efisiensikan dokumentasi: Kembangkan template dan sistem untuk mempercepat pencatatan"]	["Institusi riset dengan standar tinggi: Tempat yang menghargai metodologi ketat", "Analisis data: Peran yang memerlukan ketelitian dan organisasi", "Audit atau evaluasi: Posisi yang menilai kepatuhan terhadap standar"]	["Laporan terstruktur: Preferensi untuk format pelaporan yang konsisten", "Diskusi berbasis bukti: Komunikasi yang didukung data", "Dokumentasi sebagai prioritas: Harapan bahwa semua proses tercatat"]	2025-12-23 06:15:22.218096+00	2025-12-23 06:15:22.218096+00
14	IE	Investigative Enterprising (IE)	Investigative dan Enterprising menggabungkan analisis mendalam dengan dorongan untuk dampak dan kepemimpinan. Kamu adalah pemikir strategis yang menggunakan riset untuk menginformasikan keputusan dan mempengaruhi arah organisasi. Pikirkan konsultan strategi, analis investasi, atau pemimpin riset.	["Strategi berbasis bukti: Menggunakan data dan analisis untuk menginformasikan keputusan strategis", "Intelijen kompetitif: Terampil dalam menganalisis pasar, pesaing, tren untuk mengidentifikasi peluang", "Pola pikir ROI: Berpikir dalam hal pengembalian investasi", "Visi persuasif dengan data: Mempresentasikan arah strategis didukung bukti"]	["Analisis dapat memperlambat tindakan: Keinginan untuk data solid mungkin menunda keputusan", "Terlalu percaya diri dari data: Data memberikan rasa kepastian palsu", "Mengabaikan intuisi: Kadang pengenalan pola intuitif valid bahkan tanpa data"]	["Tetapkan ambang keputusan: Tentukan kapan data cukup untuk bergerak maju", "Integrasikan sinyal kualitatif: Pertimbangkan wawasan yang tidak mudah dikuantifikasi", "Bangun kredibilitas melalui hasil: Tunjukkan bahwa analisismu mengarah pada kesuksesan nyata"]	["Konsultasi strategi: Firma yang memerlukan analisis dan dampak klien", "Investasi atau modal ventura: Peran yang menganalisis peluang", "Kepemimpinan riset: Posisi yang mengarahkan agenda riset organisasi"]	["Presentasi berbasis data: Menyajikan rekomendasi dengan dukungan analisis", "Diskusi strategis: Menikmati eksplorasi arah dan implikasi", "Jaringan dengan pengambil keputusan: Membangun hubungan dengan orang berpengaruh"]	2025-12-23 06:15:22.222255+00	2025-12-23 06:15:22.222255+00
15	IR	Investigative Realistic (IR)	Investigative dan Realistic membalik RI, menempatkan keingintahuan analitis terlebih dahulu yang didukung kemampuan praktis. Kamu adalah peneliti yang juga bisa membangun dan menguji. Pikirkan ilmuwan eksperimental, insinyur riset, atau pengembang yang sangat analitis.	["Riset berbasis eksperimen: Tidak hanya berteori tetapi membangun dan menguji", "Implementasi teori: Mengambil konsep abstrak dan memvalidasinya dalam praktik", "Debug sistematis: Mendekati masalah teknis dengan metodologi riset", "Prototipe untuk pembuktian: Membangun untuk menguji hipotesis"]	["Terlalu banyak waktu di lab: Kadang terjebak dalam eksperimen tanpa akhir", "Perfeksionisme riset: Ingin hasil yang sempurna sebelum berbagi", "Komunikasi temuan: Menerjemahkan temuan teknis untuk audiens yang lebih luas"]	["Tetapkan milestone riset: Tentukan titik di mana akan berbagi temuan sementara", "Berkolaborasi dengan komunikator: Bermitra dengan orang yang terampil menyampaikan temuan", "Keseimbangan eksplorasi dengan pengiriman: Alokasikan waktu untuk riset terbuka dan proyek terfokus"]	["Laboratorium riset: Fasilitas dengan fokus eksperimental", "R&D di industri: Peran yang menggabungkan riset dengan pengembangan produk", "Startup teknologi mendalam: Perusahaan berbasis inovasi ilmiah"]	["Presentasi berbasis bukti: Menunjukkan data dan demonstrasi", "Diskusi teknis mendalam: Menikmati eksplorasi detail metodologi", "Dokumentasi eksperimental: Catatan menyeluruh tentang proses dan hasil"]	2025-12-23 06:15:22.224989+00	2025-12-23 06:15:22.224989+00
16	IS	Investigative Social (IS)	Investigative dan Social menggabungkan analisis mendalam dengan kepedulian terhadap orang. Kamu adalah peneliti yang fokus pada pemahaman dan membantu manusia. Pikirkan psikolog peneliti, antropolog, atau analis kebijakan sosial.	["Riset berpusat pada manusia: Menggunakan metodologi untuk memahami pengalaman dan kebutuhan orang", "Wawancara empatik: Terampil dalam mengumpulkan data dari orang dengan cara yang menghormati", "Terjemahan temuan untuk dampak: Mengkomunikasikan riset untuk membantu orang lain", "Kesadaran etis: Kepekaan kuat terhadap etika riset yang melibatkan manusia"]	["Kedekatan emosional dengan subjek: Kadang terlalu terlibat secara emosional", "Menyeimbangkan objektivitas dengan empati: Ketegangan antara jarak analitis dan koneksi manusia", "Frustrasi dengan laju perubahan: Ingin riset segera membantu orang"]	["Tetapkan batasan profesional: Jaga jarak yang sehat sambil tetap empatik", "Riset partisipatif: Libatkan komunitas dalam proses riset", "Komunikasi untuk tindakan: Fokuskan diseminasi pada rekomendasi yang dapat ditindaklanjuti"]	["Riset sosial: Institusi yang mempelajari manusia dan masyarakat", "Riset kebijakan: Organisasi yang menginformasikan kebijakan berbasis bukti", "Riset kesehatan: Studi yang fokus pada kesejahteraan pasien"]	["Profesionalisme hangat: Menyeimbangkan ketelitian dengan kepedulian", "Presentasi berbasis cerita: Menggunakan narasi untuk membuat temuan relatable", "Keterlibatan komunitas: Berbagi temuan dengan cara yang bermakna bagi mereka"]	2025-12-23 06:15:22.228503+00	2025-12-23 06:15:22.228503+00
42	RCE	Realistic Conventional Enterprising (RCE)	Kombinasi yang menggabungkan kemampuan teknis, organisasi, dan ambisi. Kamu adalah operator yang efisien dengan dorongan untuk sukses. Ideal untuk manajer produksi, supervisor teknis, atau pemilik bisnis berbasis kerajinan.	["Operasi yang efisien: Menjalankan produksi dengan optimasi maksimal", "Kepemimpinan teknis terstruktur: Memimpin dengan prosedur yang jelas", "Pertumbuhan sistematis: Mengembangkan bisnis melalui proses yang scalable", "Kontrol kualitas: Memastikan standar terpenuhi secara konsisten"]	["Terlalu fokus pada efisiensi: Bisa mengabaikan inovasi", "Tekanan produktivitas: Mendorong tim terlalu keras", "Resistensi terhadap perubahan: Investasi dalam sistem membuat sulit berubah"]	["Waktu untuk improvement: Sisihkan waktu untuk perbaikan proses", "Dengarkan tim: Operator punya insight untuk efisiensi", "Balance jangka panjang: Pertumbuhan berkelanjutan vs hasil cepat"]	["Manajemen produksi: Mengawasi operasi manufaktur", "Bisnis kerajinan: Memiliki workshop dengan karyawan", "Supervisor teknis: Memimpin tim operasional"]	["Komunikasi terstruktur: Briefing dan reporting yang jelas", "Metrik kinerja: Bicara dalam angka dan target", "Rapat produksi: Update reguler tentang output"]	2025-12-23 06:15:22.343055+00	2025-12-23 06:15:22.343055+00
17	AC	Artistic Conventional (AC)	Artistic dan Conventional menggabungkan kreativitas dengan kecintaan pada organisasi dan sistem. Kamu adalah kreator yang juga sangat terorganisir. Pikirkan desainer grafis dengan alur kerja yang ketat, editor dengan standar tinggi, atau manajer produksi kreatif.	["Proses kreatif yang terstruktur: Memiliki metodologi untuk menghasilkan karya berkualitas secara konsisten", "Manajemen proyek kreatif: Bisa mengelola kompleksitas produksi kreatif", "Standar kualitas: Mempertahankan standar tinggi dalam output kreatif", "Dokumentasi kreatif: Mendokumentasikan proses dan keputusan desain"]	["Ketegangan antara struktur dan spontanitas: Kebutuhan akan sistem bisa membatasi eksplorasi bebas", "Perfeksionisme ganda: Ingin karya yang kreatif sempurna DAN terorganisir sempurna", "Frustrasi dengan kekacauan kreatif: Proses kreatif orang lain yang tidak terstruktur bisa mengganggu"]	["Jadwalkan waktu eksplorasi bebas: Sisihkan waktu di mana tidak ada aturan", "Sistem fleksibel: Ciptakan kerangka yang memberikan struktur tetapi memungkinkan variasi", "Hargai proses berbeda: Kenali bahwa orang lain mungkin kreatif dengan cara yang kurang terorganisir"]	["Studio dengan sistem: Lingkungan kreatif yang juga terorganisir", "Produksi media: Peran yang mengelola proses kreatif yang kompleks", "Desain dengan metodologi: Praktik yang menghargai proses dan hasil"]	["Komunikasi terstruktur tentang kreativitas: Menjelaskan keputusan kreatif dengan logika yang jelas", "Dokumentasi visual: Menggunakan mood board, panduan gaya, dan referensi terorganisir", "Deadline sebagai motivasi: Menemukan struktur membantu kreativitas"]	2025-12-23 06:15:22.232034+00	2025-12-23 06:15:22.232034+00
18	AE	Artistic Enterprising (AE)	Artistic dan Enterprising menggabungkan kreativitas dengan ambisi dan kepemimpinan. Kamu adalah kreator yang juga ingin membuat dampak besar. Pikirkan pendiri agensi kreatif, seniman yang membangun merek, atau direktur kreatif dengan visi bisnis.	["Visi kreatif komersial: Bisa menciptakan karya yang menarik secara artistik dan sukses secara komersial", "Kepemimpinan kreatif: Menginspirasi dan memimpin tim kreatif", "Branding personal: Terampil dalam membangun dan mempromosikan identitas kreatif", "Negosiasi kreatif: Bisa menjual ide dan mengadvokasi visi"]	["Kompromi artistik: Kadang harus mengorbankan visi untuk kebutuhan komersial", "Beban kepemimpinan: Mengelola tim bisa menguras waktu untuk berkreasi sendiri", "Kritik sebagai serangan: Umpan balik bisnis bisa terasa seperti penolakan kreatif"]	["Definisikan batas kompromi: Tentukan aspek mana yang tidak bisa dikompromikan", "Delegasi operasional: Serahkan manajemen hari-ke-hari kepada orang lain", "Pisahkan identitas dari bisnis: Kenali bahwa penolakan bisnis bukan penolakan pribadi"]	["Industri kreatif: Media, periklanan, desain, atau hiburan", "Startup kreatif: Perusahaan yang dibangun di sekitar inovasi kreatif", "Galeri atau platform: Tempat yang menghubungkan seniman dengan pasar"]	["Pitch kreatif: Mempresentasikan ide dengan antusiasme dan strategi", "Jaringan industri: Membangun hubungan dengan pembuat keputusan kreatif", "Storytelling merek: Mengkomunikasikan visi dengan narasi yang menarik"]	2025-12-23 06:15:22.234931+00	2025-12-23 06:15:22.234931+00
19	AI	Artistic Investigative (AI)	Artistic dan Investigative membalik IA, menempatkan kreativitas terlebih dahulu yang didukung keingintahuan analitis. Kamu adalah kreator yang karyanya diinformasikan oleh riset dan pemahaman mendalam. Pikirkan desainer yang melakukan riset pengguna, penulis yang mendalami topik, atau seniman konseptual.	["Kreativitas yang terinformasi: Karyamu didasarkan pada riset dan pemahaman", "Konsep yang kuat: Ide di balik karya sama kuatnya dengan eksekusinya", "Eksplorasi topik mendalam: Tidak puas dengan pemahaman permukaan", "Inovasi berbasis insight: Kreativitas yang muncul dari pemahaman unik"]	["Riset tanpa akhir: Kadang terjebak dalam fase riset dan tidak pernah membuat", "Over-intellectualizing seni: Terlalu banyak berpikir bisa menghambat intuisi kreatif", "Komunikasi kompleksitas: Konsep yang dalam bisa sulit dijelaskan"]	["Tetapkan batas riset: Tentukan kapan riset cukup dan saatnya membuat", "Percaya intuisi kreatif: Izinkan keputusan yang tidak sepenuhnya rasional", "Layered communication: Siapkan penjelasan untuk berbagai tingkat pemahaman"]	["Desain berbasis riset: Studio yang menghargai insight sebagai fondasi", "Penulisan kreatif: Konteks di mana riset mendalam menginformasikan narasi", "Seni konseptual: Komunitas yang menghargai ide di balik karya"]	["Diskusi konseptual: Menikmati eksplorasi ide dan makna", "Presentasi berlapis: Menawarkan pengalaman permukaan dan kedalaman", "Referensi intelektual: Membawa konteks dan pengaruh ke dalam diskusi"]	2025-12-23 06:15:22.238514+00	2025-12-23 06:15:22.238514+00
20	AR	Artistic Realistic (AR)	Artistic dan Realistic membalik RA, menempatkan kreativitas terlebih dahulu yang didukung kemampuan praktis. Kamu adalah kreator yang juga bisa membangun. Pikirkan seniman yang bekerja dengan material, pembuat yang juga desainer, atau kreator yang menguasai medium teknis.	["Penguasaan medium: Memahami material dan teknik secara mendalam", "Kreativitas yang dapat diwujudkan: Ide-idemu bisa benar-benar dibuat", "Eksperimen material: Menjelajahi kemungkinan baru dengan medium yang dikuasai", "Kerajinan sebagai ekspresi: Kualitas teknis adalah bagian dari pesan artistik"]	["Keterbatasan medium: Visi kreatif kadang melebihi kemampuan teknis", "Waktu untuk penguasaan: Mempelajari teknik baru memakan waktu dari kreasi", "Perfeksionisme kerajinan: Standar tinggi bisa menghambat eksperimen"]	["Ekspansi bertahap: Perluas kemampuan teknis secara terencana", "Kolaborasi dengan spesialis: Bermitra dengan orang yang memiliki keterampilan yang kamu butuhkan", "Embrace imperfection: Terima bahwa tidak sempurna bisa jadi bagian dari karya"]	["Studio dengan workshop: Akses ke alat dan ruang untuk membuat", "Komunitas pembuat: Kolega yang menghargai kerajinan dan kreativitas", "Residensi artistik: Waktu dan ruang untuk eksplorasi"]	["Demonstrasi proses: Menunjukkan cara membuat sebagai bagian dari presentasi", "Apresiasi material: Membahas pilihan medium dan teknik", "Portofolio fisik: Preferensi untuk menunjukkan karya nyata"]	2025-12-23 06:15:22.241968+00	2025-12-23 06:15:22.241968+00
21	AS	Artistic Social (AS)	Artistic dan Social menggabungkan kreativitas dengan kepedulian terhadap orang. Kamu adalah kreator yang karyanya berfokus pada koneksi manusia. Pikirkan terapis seni, seniman komunitas, atau desainer yang berfokus pada pengalaman pengguna.	["Kreativitas relasional: Proses kreatifmu melibatkan dan melayani orang lain", "Fasilitasi ekspresi: Membantu orang lain mengekspresikan diri secara kreatif", "Seni yang menyembuhkan: Menggunakan kreativitas untuk kesejahteraan", "Desain empatik: Menciptakan dengan mempertimbangkan pengalaman pengguna"]	["Identitas artistik personal: Fokus pada orang lain bisa mengorbankan visi sendiri", "Batasan dalam berbagi: Sulit menentukan berapa banyak dari diri untuk dibagikan", "Mengukur dampak: Dampak sosial dari seni sulit dikuantifikasi"]	["Pertahankan praktik personal: Sisihkan waktu untuk karya yang hanya untukmu", "Dokumentasikan dampak: Kumpulkan testimoni dan cerita", "Komunitas praktisi: Terhubung dengan seniman lain yang bekerja dengan fokus sosial"]	["Terapi seni: Setting klinis atau pendidikan yang menggunakan kreativitas", "Seni komunitas: Program yang membawa seni ke masyarakat", "Desain berpusat manusia: Praktik yang mengutamakan pengalaman pengguna"]	["Menciptakan ruang aman: Membangun lingkungan di mana orang bisa rentan secara kreatif", "Afirmasi partisipasi: Menghargai semua upaya kreatif", "Pengalaman bersama: Menciptakan bersama versus mendemonstrasikan"]	2025-12-23 06:15:22.244742+00	2025-12-23 06:15:22.244742+00
22	SA	Social Artistic (SA)	Social dan Artistic membalik AS, menempatkan fokus orang terlebih dahulu yang didukung kreativitas. Kamu adalah orang yang membantu yang mengekspresikannya secara kreatif. Pikirkan terapis drama, fasilitator seni komunitas, atau pembuat cerita dampak sosial.	["Kreativitas fasilitatif: Menciptakan ruang di mana orang lain bisa mengekspresikan diri", "Penggunaan terapeutik seni: Memahami bagaimana ekspresi kreatif bisa menyembuhkan", "Proses kreatif inklusif: Membuat kreativitas dapat diakses semua orang", "Koneksi melalui cerita: Menggunakan narasi untuk membangun empati"]	["Identitas artistik personal: Fokus memfasilitasi orang lain bisa mengorbankan suara sendiri", "Batasan: Sulit menentukan apa yang dibagikan versus disimpan", "Mengukur dampak: Sulit mengukur dampak sosial intervensi kreatif"]	["Pertahankan praktik personal: Waktu untuk karya kreatif sendiri", "Dokumentasikan proses dan hasil: Kumpulkan bukti dampak", "Jaringan dengan praktisi: Terhubung dengan fasilitator seni lain"]	["Terapi atau pendidikan seni: Menggunakan seni untuk pengembangan atau penyembuhan", "Perusahaan sosial kreatif: Organisasi menggunakan kreativitas untuk misi sosial", "Pusat komunitas: Program seni melayani pengembangan komunitas"]	["Menciptakan ruang aman: Lingkungan di mana orang bisa rentan secara kreatif", "Afirmasi: Penguatan positif konsisten untuk upaya kreatif", "Menciptakan bersama: Preferensi untuk proses kolaboratif"]	2025-12-23 06:15:22.247318+00	2025-12-23 06:15:22.247318+00
23	SC	Social Conventional (SC)	Social dan Conventional menggabungkan orientasi orang dengan kecintaan pada struktur dan sistem. Kamu adalah pembantu yang bekerja dalam kerangka terorganisir. Pikirkan konselor sekolah, spesialis HR, atau administrator layanan sosial.	["Pengiriman dukungan sistematis: Menciptakan sistem yang memastikan orang mendapat bantuan secara konsisten", "Pencatatan untuk layanan: Dokumentasi untuk melacak kemajuan dan kontinuitas", "Kesadaran kebijakan: Mengetahui kebijakan dan regulasi relevan untuk advokasi", "Tindak lanjut yang dapat diandalkan: Orang dapat bergantung padamu untuk menyelesaikan"]	["Frustrasi oleh birokrasi: Birokrasi bisa terasa menghalangi bantuan", "Menyeimbangkan empati dengan protokol: Ketegangan antara hati dan aturan", "Keterbatasan sistem: Frustrasi ketika tidak bisa membantu karena kebijakan"]	["Bekerja untuk perubahan sistem: Advokasi untuk perbaikan kebijakan dari dalam", "Kembangkan solusi kreatif: Cara navigasi sistem demi keuntungan klien", "Supervisi profesional: Debriefing untuk memproses kasus menantang"]	["Agensi layanan sosial: Program dukungan terstruktur", "Administrasi kesehatan: Advokasi pasien, koordinasi perawatan", "Administrasi pendidikan: Konseling sekolah, layanan mahasiswa"]	["Empati profesional: Kehangatan dengan batasan yang sesuai", "Komunikasi proses yang jelas: Membantu orang memahami prosedur", "Pola pikir dokumentasi: Kecenderungan mendokumentasikan untuk akuntabilitas"]	2025-12-23 06:15:22.259792+00	2025-12-23 06:15:22.259792+00
24	SE	Social Enterprising (SE)	Social dan Enterprising menggabungkan keterampilan orang dengan ambisi untuk dampak sosial besar. Kamu adalah pemimpin yang ingin perubahan sistemik. Pikirkan pengusaha sosial, pemimpin organisasi nirlaba, atau investor dampak.	["Kepemimpinan berbasis misi: Menginspirasi dan memimpin tim di sekitar misi sosial", "Mobilisasi sumber daya: Terampil dalam penggalangan dana dan membangun kemitraan", "Pemikiran strategis untuk dampak: Mempertimbangkan sistem berkelanjutan dan skala", "Manajemen pemangku kepentingan: Menavigasi hubungan beragam dari penerima hingga donor"]	["Menyeimbangkan misi dengan keberlanjutan: Ketegangan antara membantu semua orang versus kelangsungan finansial", "Beban emosional skala: Melihat masalah sistemik bisa sangat memberatkan", "Keputusan sulit: Kadang harus membuat panggilan yang tampak bertentangan dengan membantu individu"]	["Definisikan teori perubahan: Jelas tentang bagaimana kerjamu menciptakan dampak", "Bangun tim kuat: Kelilingi diri dengan orang yang berbagi misi dengan keterampilan komplementer", "Perawatan diri: Tetapkan cakupan realistis untuk keberlanjutan jangka panjang"]	["Perusahaan sosial: Bisnis dengan misi sosial jelas", "Kepemimpinan organisasi nirlaba: Peran eksekutif dalam nirlaba atau yayasan", "Investasi dampak: Peran keuangan fokus pada pengembalian sosial"]	["Komunikasi inspirasional: Mengartikulasikan visi yang menggerakkan orang", "Pembangunan hubungan autentik: Kepedulian tulus melampaui hubungan transaksional", "Pengambilan keputusan inklusif: Melibatkan komunitas yang terpengaruh"]	2025-12-23 06:15:22.265243+00	2025-12-23 06:15:22.265243+00
25	SI	Social Investigative (SI)	Social dan Investigative menggabungkan kepedulian terhadap orang dengan analisis mendalam. Kamu adalah peneliti atau analis yang fokus pada kesejahteraan manusia. Pikirkan psikolog klinis, peneliti sosial, atau analis data nirlaba.	["Riset berpusat pada manusia: Merancang riset yang etis dan menghormati partisipan", "Menerjemahkan temuan untuk dampak: Mengkomunikasikan riset yang dapat ditindaklanjuti", "Wawancara empatik: Membangun hubungan dengan partisipan untuk data yang jujur", "Kesadaran etis: Kepekaan terhadap etika riset dan potensi bahaya"]	["Kedekatan emosional: Kadang terlalu dekat dengan subjek riset", "Frustrasi dengan laju riset: Riset membutuhkan waktu untuk diterjemahkan menjadi bantuan", "Menyeimbangkan ketelitian dengan relevansi: Ketegangan antara standar akademis dan kegunaan"]	["Libatkan praktisi: Terhubung dengan implementor untuk melihat dampak lebih cepat", "Riset berbasis komunitas: Libatkan komunitas dalam proses riset", "Ringkasan awam: Buat versi yang dapat diakses untuk audiens luas"]	["Riset terapan: Organisasi yang fokus pada riset untuk dampak sosial", "Riset kebijakan: Di mana riset menginformasikan kebijakan sosial", "Riset kesehatan: Studi dengan fokus pasien"]	["Profesionalisme hangat: Batasan profesional dengan kehangatan tulus", "Presentasi berbasis cerita: Menyertakan cerita untuk membuat temuan relatable", "Keterlibatan pemangku kepentingan: Melibatkan komunitas dalam diseminasi"]	2025-12-23 06:15:22.268434+00	2025-12-23 06:15:22.268434+00
26	SR	Social Realistic (SR)	Social dan Realistic membalik RS, menempatkan fokus orang terlebih dahulu yang didukung kemampuan praktis. Kamu adalah pembantu yang mengekspresikan kepedulian melalui tindakan praktis. Pikirkan terapis fisik, pelatih vokasional, atau spesialis dukungan teknis.	["Bantuan langsung yang terapan: Secara aktif melakukan hal untuk membantu orang memecahkan masalah", "Pengajar teknis yang sabar: Mengajarkan keterampilan dengan cara yang mendukung", "Empati praktis: Memahami kebutuhan orang dalam istilah konkret", "Pemecahan masalah kolaboratif: Bekerja dengan orang untuk mencari solusi"]	["Pekerjaan emosional kurang terlihat: Bantuan praktis mungkin kurang terlihat dibanding dukungan verbal", "Menyeimbangkan tugas versus orang: Ketegangan antara menyelesaikan dan mengurus", "Preferensi komunikasi: Lebih suka menunjukkan daripada berbicara"]	["Artikulasikan gaya dukungan: Bantu orang memahami bahwa caramu peduli adalah melalui tindakan", "Kembangkan pengecekan verbal: Latih bertanya tentang perasaan", "Cari peran layanan: Karier yang menggabungkan keterampilan teknis dengan dampak pada orang"]	["Layanan kesehatan atau rehabilitasi: Perawatan pasien praktis dan pemulihan", "Pelatihan atau pendidikan: Pengembangan keterampilan langsung", "Layanan komunitas: Bantuan praktis untuk masyarakat"]	["Komunikasi teknis yang hangat: Menjelaskan hal teknis dengan ramah dan sabar", "Dukungan berorientasi tindakan: Langsung memikirkan apa yang bisa dilakukan", "Tindak lanjut natural: Memeriksa kembali untuk memastikan solusi berhasil"]	2025-12-23 06:15:22.283231+00	2025-12-23 06:15:22.283231+00
27	EA	Enterprising Artistic (EA)	Enterprising dan Artistic menggabungkan ambisi dengan kreativitas. Kamu adalah pemimpin kreatif yang ingin sukses komersial melalui inovasi artistik. Pikirkan pendiri agensi kreatif, produser, atau pemimpin industri hiburan.	["Visi kreatif komersial: Menciptakan yang menarik secara artistik dan sukses secara bisnis", "Kepemimpinan industri kreatif: Mempengaruhi arah industri kreatif", "Branding dan positioning: Terampil dalam membangun identitas yang menonjol", "Negosiasi untuk kreatif: Mengadvokasi nilai karya kreatif"]	["Kompromi artistik: Kadang harus mengorbankan visi untuk kebutuhan pasar", "Fokus ganda: Mengelola bisnis sambil mempertahankan standar kreatif", "Kritik sebagai serangan: Umpan balik bisnis bisa terasa seperti penolakan kreatif"]	["Definisikan visi inti: Tentukan apa yang tidak bisa dikompromikan", "Delegasi operasional: Serahkan manajemen kepada orang lain", "Pisahkan identitas dari produk: Penolakan bisnis bukan penolakan pribadi"]	["Industri kreatif: Media, periklanan, desain, hiburan", "Kewirausahaan kreatif: Memulai bisnis berbasis kreativitas", "Kepemimpinan agensi: Mengarahkan tim dan klien kreatif"]	["Pitch yang menarik: Mempresentasikan ide dengan antusiasme dan strategi", "Jaringan industri: Membangun hubungan dengan pembuat keputusan", "Storytelling merek: Visi dikomunikasikan melalui narasi yang kuat"]	2025-12-23 06:15:22.29784+00	2025-12-23 06:15:22.29784+00
28	EC	Enterprising Conventional (EC)	Enterprising dan Conventional menggabungkan ambisi dengan kecintaan pada sistem dan efisiensi. Kamu adalah pemimpin yang berorientasi hasil dengan fondasi operasional yang kuat. Pikirkan CEO dengan fokus operasional, manajer umum, atau konsultan efisiensi.	["Kepemimpinan operasional: Memimpin dengan fokus pada sistem dan hasil", "Pertumbuhan terukur: Mengembangkan bisnis dengan metrik yang jelas", "Optimasi proses: Mengidentifikasi dan menghilangkan inefisiensi", "Akuntabilitas hasil: Membangun budaya di mana orang bertanggung jawab atas outcome"]	["Terlalu fokus pada efisiensi: Bisa mengabaikan inovasi atau kesejahteraan", "Resistensi terhadap perubahan besar: Investasi dalam sistem yang ada membuat sulit berubah", "Kekakuan: Proses yang ketat bisa membunuh kreativitas"]	["Alokasi untuk inovasi: Sisihkan sumber daya untuk eksperimen", "Dengarkan garis depan: Orang yang melakukan pekerjaan sering punya wawasan", "Seimbangkan efisiensi dengan fleksibilitas: Proses harus melayani tujuan, bukan sebaliknya"]	["Manajemen operasional: Peran yang mengawasi efisiensi dan hasil", "Konsultasi bisnis: Membantu organisasi meningkatkan kinerja", "Kepemimpinan korporat: Posisi eksekutif dengan fokus operasional"]	["Komunikasi berbasis metrik: Diskusi berpusat pada angka dan KPI", "Rapat terstruktur: Agenda jelas dengan item tindakan", "Akuntabilitas yang tegas: Ekspektasi jelas tentang tanggung jawab"]	2025-12-23 06:15:22.300993+00	2025-12-23 06:15:22.300993+00
29	EI	Enterprising Investigative (EI)	Enterprising dan Investigative membalik IE, memimpin dengan ambisi yang didukung analisis. Kamu adalah pemimpin strategis yang menggunakan data untuk keputusan. Pikirkan konsultan manajemen, direktur strategi, atau kapitalis ventura.	["Strategi berbasis bukti: Menggunakan data untuk keputusan strategis", "Intelijen kompetitif: Menganalisis pasar dan tren untuk peluang", "Pola pikir ROI: Berpikir dalam hal pengembalian investasi", "Visi persuasif dengan data: Mempresentasikan arah dengan bukti"]	["Analisis dapat memperlambat: Keinginan untuk data bisa menunda keputusan", "Terlalu percaya diri dari data: Data memberikan kepastian palsu", "Mengabaikan intuisi: Kadang pengenalan pola intuitif valid tanpa data"]	["Tetapkan ambang keputusan: Kapan data cukup untuk bergerak", "Integrasikan sinyal kualitatif: Pertimbangkan wawasan yang tidak mudah dikuantifikasi", "Validasi melalui hasil: Tunjukkan bahwa analisis mengarah pada kesuksesan"]	["Konsultasi strategi: Firma yang memerlukan analisis dan dampak klien", "Investasi: Peran yang menganalisis peluang", "Kepemimpinan strategi: Mengarahkan arah organisasi berdasarkan analisis"]	["Presentasi berbasis data: Rekomendasi dengan dukungan analisis", "Diskusi strategis: Eksplorasi arah dan implikasi", "Jaringan pengambil keputusan: Hubungan dengan orang berpengaruh"]	2025-12-23 06:15:22.304403+00	2025-12-23 06:15:22.304403+00
30	ER	Enterprising Realistic (ER)	Enterprising dan Realistic membalik RE, memimpin dengan ambisi yang didukung kemampuan teknis. Kamu adalah pemimpin yang mengerti pekerjaan teknis dan mendorong hasil. Pikirkan direktur operasi, manajer produksi, atau manajer proyek konstruksi.	["Manajemen fokus hasil: Mendorong hasil nyata, tidak tertarik pada aktivitas tanpa outcome", "Pengambilan keputusan praktis: Berdasarkan apa yang layak, bukan ideal teoretis", "Optimasi sumber daya: Mengidentifikasi dan menghilangkan inefisiensi", "Kepemimpinan teknis yang kredibel: Tim menghormati karena kamu tahu apa yang kamu minta"]	["Tidak sabar dengan kesempurnaan teknis: Lebih tertarik pada cukup baik dan maju", "Dapat mengabaikan kekhawatiran teknis: Percaya diri mungkin mengabaikan keberatan valid", "Frustrasi delegasi: Kadang frustrasi melihat orang lain melakukan berbeda"]	["Investasi dalam tim teknis: Rekrut orang kuat sehingga bisa fokus pada strategi", "Dengarkan tanda bahaya teknis: Ciptakan budaya di mana tim nyaman mengemukakan kekhawatiran", "Seimbangkan kecepatan dengan keberlanjutan: Jangan korbankan jangka panjang untuk kemenangan cepat"]	["Manufaktur atau produksi: Manajemen operasi", "Konstruksi atau teknik: Manajemen proyek", "Logistik: Mengelola sistem operasional kompleks"]	["Langsung dan berorientasi tindakan: Rapat mengarah pada keputusan", "Komunikasi fokus metrik: Bicara dalam angka dan tanggal pengiriman", "Budaya akuntabilitas: Jelas tentang siapa bertanggung jawab untuk apa"]	2025-12-23 06:15:22.30771+00	2025-12-23 06:15:22.30771+00
31	ES	Enterprising Social (ES)	Enterprising dan Social menggabungkan ambisi dengan kepedulian terhadap orang. Kamu adalah pemimpin yang ingin kesuksesan sambil membawa orang bersamamu. Pikinkan pemimpin tim yang inspirasional, manajer penjualan dengan fokus hubungan, atau pengusaha dengan misi.	["Kepemimpinan yang menginspirasi: Memotivasi orang untuk mencapai tujuan bersama", "Pembangunan tim: Membangun tim yang kuat dan kohesif", "Penjualan berbasis hubungan: Sukses melalui koneksi autentik", "Visi inklusif: Menyertakan orang dalam perjalanan menuju tujuan"]	["Konflik loyalitas: Ketegangan antara hasil dan kesejahteraan tim", "Keputusan sulit: Kadang harus membuat keputusan yang berdampak negatif pada individu", "Beban emosional kepemimpinan: Bertanggung jawab untuk kesuksesan dan kesejahteraan"]	["Komunikasi transparan: Jelaskan konteks dan alasan di balik keputusan sulit", "Dukungan transisi: Berikan dukungan maksimal untuk yang terdampak", "Delegasi dengan pengembangan: Berikan tanggung jawab sebagai peluang pertumbuhan"]	["Kepemimpinan tim: Peran yang memimpin dan mengembangkan orang", "Penjualan atau pengembangan bisnis: Sukses melalui hubungan", "Kewirausahaan dengan misi: Bisnis dengan tujuan sosial"]	["Check-in reguler: Tidak hanya status proyek tetapi bagaimana orang menangani", "Merayakan kesuksesan: Mengakui kontribusi individu dan tim", "Umpan balik yang peduli: Jujur dengan niat membantu berkembang"]	2025-12-23 06:15:22.310207+00	2025-12-23 06:15:22.310207+00
32	CA	Conventional Artistic (CA)	Conventional dan Artistic menggabungkan kecintaan pada sistem dengan kreativitas. Kamu adalah organisator yang juga kreatif. Pikirkan manajer produksi kreatif, editor dengan sistem yang ketat, atau administrator seni.	["Manajemen produksi kreatif: Mengorganisir proses kreatif yang kompleks", "Sistem untuk kreativitas: Membangun kerangka yang mendukung output kreatif konsisten", "Dokumentasi kreatif: Mencatat keputusan dan proses desain", "Anggaran kreatif: Mengelola sumber daya untuk proyek kreatif"]	["Ketegangan struktur versus spontanitas: Sistem bisa membatasi eksplorasi bebas", "Frustrasi dengan kekacauan kreatif: Proses orang lain yang tidak terstruktur mengganggu", "Perfeksionisme ganda: Ingin terorganisir sempurna DAN kreatif sempurna"]	["Jadwalkan waktu eksplorasi: Waktu tanpa aturan untuk eksplorasi bebas", "Sistem fleksibel: Kerangka yang memberikan struktur tetapi memungkinkan variasi", "Hargai proses berbeda: Orang lain mungkin kreatif dengan cara kurang terorganisir"]	["Administrasi seni: Mengelola organisasi atau program kreatif", "Produksi media: Mengkoordinasikan proses kreatif yang kompleks", "Penerbitan: Mengelola alur kerja editorial"]	["Komunikasi terstruktur tentang kreativitas: Menjelaskan keputusan dengan logika", "Dokumentasi visual: Mood board, panduan gaya yang terorganisir", "Deadline sebagai motivasi: Struktur membantu kreativitas"]	2025-12-23 06:15:22.313238+00	2025-12-23 06:15:22.313238+00
33	CE	Conventional Enterprising (CE)	Conventional dan Enterprising menggabungkan kecintaan pada sistem dengan ambisi. Kamu adalah pemimpin yang membangun melalui proses dan efisiensi. Pikirkan COO, manajer operasional, atau konsultan proses bisnis.	["Kepemimpinan operasional: Memimpin dengan fokus pada sistem dan efisiensi", "Pertumbuhan melalui proses: Mengembangkan organisasi dengan infrastruktur yang kuat", "Optimasi berkelanjutan: Selalu mencari cara untuk meningkatkan", "Akuntabilitas sistematis: Membangun budaya tanggung jawab yang jelas"]	["Terlalu fokus pada efisiensi: Bisa mengabaikan inovasi atau faktor manusia", "Resistensi terhadap perubahan besar: Investasi dalam sistem membuat sulit berubah", "Birokratisasi: Proses bisa menjadi tujuan daripada alat"]	["Alokasi untuk inovasi: Sisihkan sumber daya untuk eksperimen", "Dengarkan pengguna: Orang yang menggunakan sistem punya wawasan untuk perbaikan", "Tinjauan berkala: Evaluasi apakah sistem masih melayani tujuan"]	["Manajemen operasional: Peran yang mengawasi efisiensi organisasi", "Konsultasi proses: Membantu organisasi memperbaiki operasi", "Kepemimpinan eksekutif: Posisi C-level dengan fokus operasional"]	["Komunikasi berbasis proses: Diskusi tentang alur kerja dan efisiensi", "Rapat terstruktur: Agenda jelas dengan item tindakan", "Pelaporan reguler: Update terjadwal tentang metrik kunci"]	2025-12-23 06:15:22.315896+00	2025-12-23 06:15:22.315896+00
34	CI	Conventional Investigative (CI)	Conventional dan Investigative menggabungkan kecintaan pada sistem dengan analisis mendalam. Kamu adalah analis yang sangat terorganisir. Pikirkan auditor, analis keuangan, atau peneliti dengan metodologi ketat.	["Analisis sistematis: Mendekati riset dengan metodologi yang terstruktur", "Dokumentasi komprehensif: Setiap langkah analisis tercatat dengan baik", "Temuan yang dapat diverifikasi: Pekerjaanmu bisa diaudit dan direplikasi", "Manajemen data: Terampil mengorganisir dan memelihara dataset"]	["Fleksibilitas terbatas: Kadang terlalu terikat pada protokol yang ditetapkan", "Kesulitan dengan ambiguitas: Lebih nyaman dengan pertanyaan yang terdefinisi jelas", "Waktu untuk dokumentasi: Ketelitian memakan waktu signifikan"]	["Bangun fleksibilitas terstruktur: Titik evaluasi dalam protokol untuk penyesuaian", "Terima ketidakpastian: Beberapa ambiguitas adalah bagian normal riset", "Efisiensikan dokumentasi: Template untuk mempercepat pencatatan"]	["Audit atau kepatuhan: Peran yang menilai kepatuhan terhadap standar", "Analisis keuangan: Posisi yang memerlukan ketelitian dan organisasi", "Riset dengan standar tinggi: Institusi yang menghargai metodologi ketat"]	["Laporan terstruktur: Format pelaporan yang konsisten", "Diskusi berbasis bukti: Komunikasi yang didukung data", "Dokumentasi sebagai prioritas: Semua proses tercatat dengan jelas"]	2025-12-23 06:15:22.318556+00	2025-12-23 06:15:22.318556+00
35	CR	Conventional Realistic (CR)	Conventional dan Realistic menggabungkan kecintaan pada sistem dengan kemampuan praktis. Kamu adalah pelaksana teknis yang sangat terorganisir. Pikirkan teknisi dengan prosedur ketat, administrator sistem, atau spesialis QA.	["Eksekusi sistematis: Melakukan pekerjaan teknis dengan mengikuti prosedur yang jelas", "Dokumentasi teknis: Membuat dan memelihara prosedur operasi standar", "Konsistensi output: Hasil yang dapat diandalkan karena metodologi yang ketat", "Pemeliharaan sistem: Terampil dalam menjaga sistem teknis berjalan lancar"]	["Kekakuan: Preferensi untuk prosedur bisa menolak cara baru yang lebih baik", "Perfeksionisme teknis: Ingin sempurna bisa menunda penyelesaian", "Resistensi perubahan: Preferensi untuk stabilitas membuat adaptasi sulit"]	["Waktu untuk eksplorasi: Sisihkan waktu untuk menjelajahi metode baru", "Peningkatan bertahap: Perubahan sebagai evolusi, bukan revolusi", "Kolaborasi dengan inovator: Bermitra dengan orang yang mendorong batas"]	["Operasi teknis: Peran yang memerlukan keandalan dan konsistensi", "Jaminan kualitas: Posisi yang menguji dan memverifikasi", "Administrasi sistem: Memelihara infrastruktur teknis"]	["Komunikasi prosedural: Preferensi untuk instruksi yang jelas", "Dokumentasi sebagai standar: Harapan bahwa semua proses terdokumentasi", "Pertemuan terjadwal: Lebih suka rapat dengan agenda yang jelas"]	2025-12-23 06:15:22.322541+00	2025-12-23 06:15:22.322541+00
36	CS	Conventional Social (CS)	Conventional dan Social menggabungkan kecintaan pada sistem dengan kepedulian terhadap orang. Kamu adalah pembantu yang bekerja dalam kerangka terorganisir. Pikirkan pekerja sosial administratif, koordinator program, atau spesialis HR.	["Layanan sistematis: Membantu orang melalui proses yang terorganisir", "Koordinasi layanan: Mengelola program yang melayani banyak orang", "Dokumentasi untuk kontinuitas: Catatan yang memastikan layanan berkelanjutan", "Kepatuhan dengan kepedulian: Mengikuti regulasi sambil tetap peduli"]	["Frustrasi dengan birokrasi: Kadang aturan menghalangi bantuan", "Ketegangan empati versus protokol: Kadang hati dan aturan bertentangan", "Keterbatasan sistem: Frustrasi ketika tidak bisa membantu karena kebijakan"]	["Advokasi untuk perubahan: Bekerja untuk memperbaiki sistem dari dalam", "Solusi dalam aturan: Temukan cara kreatif dalam batasan yang ada", "Supervisi: Proses kasus menantang dengan mentor atau rekan"]	["Layanan sosial terstruktur: Program bantuan dengan prosedur jelas", "Administrasi kesehatan: Koordinasi perawatan, advokasi pasien", "Sumber daya manusia: Mendukung karyawan dalam kerangka kebijakan"]	["Empati profesional: Kehangatan dengan batasan yang sesuai", "Komunikasi prosedural yang jelas: Membantu orang memahami langkah-langkah", "Dokumentasi untuk keberlanjutan: Catatan yang membantu layanan berkelanjutan"]	2025-12-23 06:15:22.325379+00	2025-12-23 06:15:22.325379+00
37	RAC	Realistic Artistic Conventional (RAC)	Kombinasi langka yang menggabungkan kemampuan praktis, kreativitas, dan organisasi. Kamu bisa menciptakan karya yang indah dengan presisi teknis dan dokumentasi yang rapi. Ideal untuk desainer produk yang detail-oriented, arsitek dengan standar tinggi, atau pengrajin dengan sistem produksi yang terorganisir.	["Kreasi terstruktur: Menggabungkan visi artistik dengan eksekusi sistematis", "Dokumentasi desain: Mencatat proses kreatif dengan detail", "Produksi konsisten: Menghasilkan karya berkualitas secara teratur", "Standar estetika tinggi: Keindahan yang terukur dan dapat direplikasi"]	["Ketegangan spontanitas vs struktur: Kreativitas kadang memerlukan kebebasan dari sistem", "Perfeksionisme triple: Ingin sempurna secara teknis, estetis, DAN organisasional", "Waktu proses: Setiap langkah memerlukan perhatian"]	["Fase terpisah: Waktu eksplorasi bebas, lalu fase produksi terstruktur", "Template fleksibel: Sistem yang memberikan struktur tanpa membatasi kreativitas", "Prioritaskan: Tidak semua proyek perlu kesempurnaan di ketiga dimensi"]	["Studio desain terorganisir: Ruang kreatif dengan sistem yang jelas", "Produksi kerajinan: Workshop dengan standar kualitas", "Arsitektur atau desain interior: Estetika dengan spesifikasi teknis"]	["Presentasi visual terstruktur: Portofolio dengan dokumentasi proses", "Komunikasi detail: Menjelaskan keputusan desain dengan logika", "Brief yang jelas: Preferensi untuk spesifikasi yang terdefinisi"]	2025-12-23 06:15:22.328283+00	2025-12-23 06:15:22.328283+00
38	RAE	Realistic Artistic Enterprising (RAE)	Kombinasi dinamis dari kemampuan teknis, kreativitas, dan ambisi bisnis. Kamu adalah kreator yang juga entrepreneur. Ideal untuk pendiri startup kreatif, produser yang memimpin tim, atau desainer yang membangun bisnis.	["Kreasi dengan visi bisnis: Menciptakan produk yang indah dan marketable", "Kepemimpinan kreatif: Memimpin tim kreatif dengan kredibilitas teknis", "Inovasi yang menjual: Menggabungkan orisinalitas dengan viabilitas komersial", "Eksekusi ambisius: Mewujudkan visi besar dengan tangan sendiri"]	["Ketegangan seni vs komersial: Kadang apa yang indah tidak selalu laku", "Terlalu banyak peran: Kreator, pemimpin, dan pebisnis sekaligus", "Delegasi kreatif: Sulit mempercayakan visi kreatif pada orang lain"]	["Definisikan nilai unik: Apa yang membuat karyamu berbeda dan berharga", "Bangun tim: Rekrut orang yang melengkapi kemampuanmu", "Seimbangkan portofolio: Proyek komersial dan proyek passion"]	["Startup kreatif: Membangun bisnis berbasis kreativitas", "Studio independen: Kepemimpinan produksi kreatif", "Konsultasi desain: Bisnis yang menjual keahlian kreatif"]	["Pitch kreatif: Mempresentasikan visi dengan passion dan strategi", "Networking aktif: Membangun hubungan untuk peluang bisnis", "Demonstrasi kemampuan: Portofolio yang menunjukkan nilai"]	2025-12-23 06:15:22.330887+00	2025-12-23 06:15:22.330887+00
39	RAI	Realistic Artistic Investigative (RAI)	Kombinasi unik dari kemampuan praktis, kreativitas, dan pemikiran analitis. Kamu adalah creator-researcher yang menggabungkan eksperimen dengan eksekusi. Ideal untuk seniman yang berbasis riset, desainer dengan pendekatan ilmiah, atau inovator material.	["Eksperimen kreatif: Menguji ide dengan metodologi yang sistematis", "Inovasi berbasis riset: Kreativitas yang didukung pemahaman mendalam", "Prototipe analitis: Membangun dan menganalisis iterasi", "Dokumentasi eksperimen: Mencatat proses discovery dengan detail"]	["Terlalu banyak eksplorasi: Riset tanpa akhir sebelum membuat", "Ketegangan intuisi vs data: Kadang keputusan estetis sulit diukur", "Komunikasi kompleks: Menjelaskan proses yang multidimensional"]	["Batasi fase riset: Tenggat untuk beralih ke eksekusi", "Terima subjektivitas estetis: Tidak semua keputusan perlu dibuktikan", "Visualisasi proses: Gunakan diagram untuk menjelaskan metodologi"]	["Lab desain: R&D untuk produk kreatif", "Studio eksperimental: Ruang untuk eksplorasi material dan teknik", "Akademisi kreatif: Penelitian dalam bidang seni atau desain"]	["Presentasi proses: Menunjukkan perjalanan dari riset ke karya", "Diskusi teknis-kreatif: Dialog tentang material, teknik, dan konsep", "Dokumentasi visual: Catatan eksperimen yang estetis"]	2025-12-23 06:15:22.333704+00	2025-12-23 06:15:22.333704+00
40	RAS	Realistic Artistic Social (RAS)	Kombinasi yang menggabungkan kemampuan praktis, kreativitas, dan kepedulian sosial. Kamu adalah kreator yang bekerja untuk dan dengan orang lain. Ideal untuk terapis seni, pengajar kerajinan, atau desainer yang fokus pada komunitas.	["Kreasi kolaboratif: Membangun bersama orang lain", "Mengajar melalui praktek: Berbagi keterampilan dengan demonstrasi", "Desain untuk kebutuhan manusia: Kreativitas yang melayani orang", "Memfasilitasi ekspresi: Membantu orang lain mengekspresikan diri"]	["Keseimbangan waktu: Antara menciptakan sendiri dan membantu orang lain", "Standar vs inklusivitas: Standar tinggi bisa mengintimidasi pemula", "Kelelahan kreatif-emosional: Memberikan di dua dimensi sekaligus"]	["Jadwalkan waktu studio: Waktu khusus untuk praktik pribadi", "Diferensiasi: Standar berbeda untuk konteks berbeda", "Komunitas sesama: Dukungan dari kreator lain yang juga mengajar"]	["Pendidikan seni: Mengajar keterampilan kreatif", "Terapi seni: Menggunakan kreativitas untuk healing", "Desain komunitas: Proyek yang melibatkan dan melayani komunitas"]	["Workshop interaktif: Belajar sambil menciptakan bersama", "Umpan balik yang membangun: Kritik yang mendorong pertumbuhan", "Celebrasi proses: Menghargai perjalanan, bukan hanya hasil"]	2025-12-23 06:15:22.336845+00	2025-12-23 06:15:22.336845+00
41	RCA	Realistic Conventional Artistic (RCA)	Kombinasi yang menggabungkan kemampuan teknis, organisasi, dan sentuhan kreatif. Kamu adalah teknisi dengan mata untuk estetika dan sistem yang rapi. Ideal untuk drafter dengan sensibilitas desain, ilustrator teknis, atau spesialis CAD.	["Dokumentasi teknis yang estetis: Manual dan diagram yang jelas dan indah", "Presisi kreatif: Ketelitian teknis dengan sentuhan artistik", "Sistem visual: Mengorganisir informasi secara visual", "Standarisasi yang elegan: Prosedur yang efisien dan estetis"]	["Ketegangan efisiensi vs keindahan: Kadang yang indah tidak paling efisien", "Waktu finishing: Detail estetis memerlukan waktu ekstra", "Standar ganda: Teknis harus benar DAN terlihat bagus"]	["Prioritaskan konteks: Kapan estetika penting dan kapan tidak", "Template desain: Sistem yang sudah estetis secara default", "Komunikasikan nilai: Jelaskan mengapa estetika teknis penting"]	["Ilustrasi teknis: Visualisasi yang akurat dan menarik", "Desain CAD/CAM: Presisi dengan sensibilitas desain", "Dokumentasi produk: Manual yang informatif dan estetis"]	["Komunikasi visual: Preferensi diagram dan ilustrasi", "Standar presentasi: Dokumen yang rapi dan menarik", "Detail yang diperhatikan: Setiap elemen visual dipertimbangkan"]	2025-12-23 06:15:22.340483+00	2025-12-23 06:15:22.340483+00
43	RCI	Realistic Conventional Investigative (RCI)	Kombinasi yang menggabungkan kemampuan teknis, organisasi, dan analisis. Kamu adalah teknisi-analis yang bekerja dengan metodologi ketat. Ideal untuk teknisi laboratorium, spesialis QA, atau inspector teknis.	["Pengujian sistematis: Menguji dengan protokol yang ketat", "Dokumentasi temuan: Catatan analisis yang komprehensif", "Diagnosis terstruktur: Troubleshooting dengan metodologi jelas", "Standar berbasis bukti: Prosedur yang didukung data"]	["Kekakuan metodologis: Sulit beradaptasi ketika protokol tidak cocok", "Waktu dokumentasi: Ketelitian memakan waktu", "Analisis vs aksi: Kadang menganalisis terlalu lama"]	["Protokol adaptif: Panduan dengan ruang untuk judgment", "Efisiensikan pencatatan: Template untuk dokumentasi cepat", "Threshold keputusan: Kapan data cukup untuk bertindak"]	["Laboratorium teknis: Pengujian dan analisis", "Jaminan kualitas: Inspeksi dan verifikasi", "Forensik teknis: Investigasi sistematis"]	["Laporan terstruktur: Format yang konsisten", "Diskusi berbasis data: Komunikasi yang didukung bukti", "Dokumentasi lengkap: Setiap langkah tercatat"]	2025-12-23 06:15:22.345299+00	2025-12-23 06:15:22.345299+00
44	RCS	Realistic Conventional Social (RCS)	Kombinasi yang menggabungkan kemampuan teknis, organisasi, dan pelayanan. Kamu adalah teknisi yang bekerja dengan dan untuk orang dalam kerangka yang terstruktur. Ideal untuk teknisi medis, support teknis, atau administrator fasilitas.	["Layanan teknis terorganisir: Membantu dengan prosedur yang jelas", "Pelatihan terstruktur: Mengajar keterampilan teknis dengan kurikulum", "Support yang konsisten: Bantuan yang dapat diandalkan", "Dokumentasi untuk kontinuitas: Catatan yang membantu layanan berkelanjutan"]	["Ketegangan protokol vs kebutuhan: Kadang aturan tidak fit dengan situasi", "Beban administratif: Dokumentasi bisa mengambil waktu dari layanan", "Tekanan efisiensi vs kualitas layanan: Melayani lebih banyak vs lebih baik"]	["Advokasi dalam sistem: Bekerja untuk memperbaiki prosedur", "Prioritaskan dokumentasi kritis: Tidak semua perlu detail maksimal", "Self-care: Layanan berkelanjutan memerlukan energi yang dijaga"]	["Support teknis: Membantu pengguna dengan masalah teknis", "Administrasi kesehatan: Koordinasi perawatan terstruktur", "Fasilitas: Memelihara lingkungan untuk pengguna"]	["Komunikasi jelas: Instruksi yang mudah diikuti", "Empati profesional: Kehangatan dalam batasan yang sesuai", "Follow-up sistematis: Memastikan masalah terselesaikan"]	2025-12-23 06:15:22.347928+00	2025-12-23 06:15:22.347928+00
45	REA	Realistic Enterprising Artistic (REA)	Kombinasi dinamis dari kemampuan teknis, ambisi, dan kreativitas. Kamu adalah pemimpin yang membangun produk kreatif. Ideal untuk creative director dengan latar teknis, produser, atau founder studio kreatif.	["Produksi kreatif ambisius: Memimpin penciptaan karya besar", "Visi yang bisa dieksekusi: Mimpi besar dengan kemampuan mewujudkan", "Kepemimpinan kreatif teknis: Kredibel di kedua dunia", "Inovasi yang berdampak: Kreativitas dengan skala"]	["Terlalu banyak ambisi: Proyek besar dengan waktu/sumber daya terbatas", "Delegasi kreatif: Sulit mempercayakan visi pada orang lain", "Burnout triple: Tuntutan di tiga dimensi"]	["Prioritaskan proyek: Tidak semua ide perlu dikejar", "Bangun tim terpercaya: Orang yang share visi dan bisa eksekusi", "Jaga energi: Kreativitas butuh rest"]	["Studio kreatif: Memimpin tim produksi", "Startup produk: Membangun produk kreatif", "Agency: Bisnis layanan kreatif"]	["Pitch yang inspiratif: Visi yang memotivasi tim dan klien", "Demonstrasi kemampuan: Menunjukkan expertise langsung", "Networking strategis: Hubungan untuk peluang besar"]	2025-12-23 06:15:22.350381+00	2025-12-23 06:15:22.350381+00
46	REC	Realistic Enterprising Conventional (REC)	Kombinasi yang menggabungkan kemampuan teknis, ambisi, dan organisasi. Kamu adalah pemimpin operasional yang efisien. Ideal untuk plant manager, direktur operasi, atau pemilik bisnis manufaktur.	["Kepemimpinan operasional: Memimpin dengan fokus pada efisiensi", "Pertumbuhan terukur: Ekspansi melalui sistem yang scalable", "Optimasi berbasis data: Keputusan didukung metrik", "Akuntabilitas jelas: Struktur tanggung jawab yang terdefinisi"]	["Terlalu fokus pada efisiensi: Bisa mengabaikan inovasi atau moral tim", "Resistensi terhadap cara baru: Investasi dalam sistem membuat sulit berubah", "Tekanan produktivitas: Mendorong output bisa mengabaikan sustainability"]	["Alokasi untuk improvement: Waktu dan sumber daya untuk inovasi proses", "Dengarkan frontline: Operator punya insight berharga", "Balance: Efisiensi jangka pendek vs keberlanjutan jangka panjang"]	["Manufaktur: Manajemen produksi", "Logistik: Operasi distribusi", "Konstruksi: Manajemen proyek skala besar"]	["Komunikasi metrik: Bicara dalam angka dan KPI", "Rapat terstruktur: Agenda jelas dengan item tindakan", "Reporting reguler: Update terjadwal tentang kinerja"]	2025-12-23 06:15:22.353684+00	2025-12-23 06:15:22.353684+00
47	REI	Realistic Enterprising Investigative (REI)	Kombinasi yang menggabungkan kemampuan teknis, ambisi, dan analisis. Kamu adalah pemimpin teknis yang berbasis data. Ideal untuk CTO, VP Engineering, atau founder startup teknologi.	["Kepemimpinan teknis strategis: Arah teknologi berbasis analisis", "Inovasi yang terukur: Eksperimen dengan metrik keberhasilan", "Keputusan berbasis bukti: Data mendukung strategi", "Kredibilitas teknis: Memimpin dengan pemahaman mendalam"]	["Analysis paralysis strategis: Terlalu banyak riset sebelum memutuskan", "Ketidaksabaran dengan yang non-analitis: Frustrasi dengan keputusan intuitif", "Terlalu percaya data: Mengabaikan faktor kualitatif"]	["Threshold keputusan: Kapan data cukup untuk bergerak", "Integrasikan sinyal kualitatif: Feedback pelanggan, intuisi pasar", "Delegasikan analisis: Tidak semua riset perlu kamu lakukan"]	["Startup teknologi: Founder/co-founder teknis", "R&D leadership: Memimpin tim riset dan pengembangan", "Konsultasi teknologi: Strategi teknologi berbasis analisis"]	["Presentasi berbasis data: Rekomendasi dengan bukti", "Diskusi strategis teknis: Dialog tentang arah teknologi", "Dokumentasi keputusan: Alasan yang tercatat"]	2025-12-23 06:15:22.357171+00	2025-12-23 06:15:22.357171+00
48	RES	Realistic Enterprising Social (RES)	Kombinasi yang menggabungkan kemampuan teknis, ambisi, dan kepedulian sosial. Kamu adalah pemimpin yang membangun sambil mengembangkan orang. Ideal untuk training manager teknis, social entrepreneur, atau supervisor dengan fokus pengembangan tim.	["Kepemimpinan yang mengembangkan: Membangun kemampuan tim sambil mencapai hasil", "Pelatihan teknis: Mengajar keterampilan dengan efektif", "Motivasi tim: Mendorong performa melalui hubungan", "Sukses bersama: Pencapaian yang mengangkat semua orang"]	["Ketegangan hasil vs pengembangan: Tekanan untuk deliver bisa mengorbankan learning", "Beban kepemimpinan ganda: Tanggung jawab untuk hasil DAN kesejahteraan", "Favouritisme perceived: Perhatian yang tidak merata"]	["Integrasikan pembelajaran dalam pekerjaan: OJT yang terstruktur", "Transparansi: Komunikasikan alasan di balik keputusan", "Delegasi sebagai pengembangan: Tanggung jawab sebagai kesempatan tumbuh"]	["Training teknis: Mengembangkan workforce", "Social enterprise: Bisnis dengan misi sosial", "Supervisor: Memimpin tim dengan fokus pada orang"]	["Check-in reguler: Status proyek dan bagaimana orang", "Feedback yang membangun: Jujur dengan niat membantu", "Celebrasi tim: Mengakui kontribusi bersama"]	2025-12-23 06:15:22.359784+00	2025-12-23 06:15:22.359784+00
49	RIA	Realistic Investigative Artistic (RIA)	Kombinasi langka yang menggabungkan kemampuan praktis, analisis, dan kreativitas. Kamu adalah peneliti-kreator yang membangun berdasarkan pemahaman mendalam. Ideal untuk R&D desain, scientific illustrator, atau inovator produk berbasis riset.	["Inovasi berbasis riset: Kreativitas yang didukung pemahaman ilmiah", "Visualisasi data: Mengkomunikasikan kompleksitas secara estetis", "Eksperimen kreatif sistematis: Metodologi untuk eksplorasi", "Prototipe analitis: Membangun dan mengukur iterasi"]	["Terlalu banyak dimensi: Sulit fokus pada satu aspek", "Waktu proses: Riset, kreasi, dan eksekusi memakan waktu", "Komunikasi kompleks: Menjelaskan pekerjaan multidimensional"]	["Fase terpisah: Waktu untuk riset, kreasi, dan eksekusi", "Kolaborasi: Partner untuk aspek yang bukan kekuatan utama", "Prioritas proyek: Tidak semua perlu ketiga dimensi"]	["Lab desain: R&D produk kreatif", "Ilustrasi ilmiah: Visualisasi untuk sains", "Inovasi material: Eksperimen dengan medium baru"]	["Presentasi proses: Menunjukkan riset hingga kreasi", "Diskusi teknis-kreatif: Dialog tentang metodologi dan estetika", "Dokumentasi visual: Catatan yang informatif dan estetis"]	2025-12-23 06:15:22.362868+00	2025-12-23 06:15:22.362868+00
50	RIC	Realistic Investigative Conventional (RIC)	Kombinasi yang menggabungkan kemampuan teknis, analisis, dan organisasi. Kamu adalah peneliti teknis yang sangat sistematis. Ideal untuk engineer dengan metodologi ketat, analis teknis, atau spesialis quality assurance.	["Riset terstruktur: Investigasi dengan protokol yang jelas", "Dokumentasi komprehensif: Setiap langkah tercatat dengan detail", "Analisis yang dapat direplikasi: Metodologi yang konsisten", "Standar berbasis bukti: Prosedur yang didukung data"]	["Kekakuan metodologis: Sulit beradaptasi ketika protokol tidak fit", "Waktu dokumentasi: Ketelitian memakan waktu signifikan", "Analisis berlebihan: Terlalu banyak riset sebelum aksi"]	["Protokol adaptif: Panduan dengan ruang untuk judgment", "Template efisien: Sistem dokumentasi yang streamlined", "Threshold aksi: Kapan riset cukup untuk bergerak"]	["Laboratorium R&D: Riset dan pengembangan terstruktur", "Quality engineering: Standar dan pengujian", "Technical writing: Dokumentasi sistematis"]	["Laporan terstruktur: Format yang konsisten dan detail", "Diskusi berbasis bukti: Komunikasi dengan data", "Metodologi yang jelas: Proses yang dapat diaudit"]	2025-12-23 06:15:22.36529+00	2025-12-23 06:15:22.36529+00
51	RIE	Realistic Investigative Enterprising (RIE)	Kombinasi yang menggabungkan kemampuan teknis, analisis, dan ambisi. Kamu adalah innovator yang mengkomersialkan riset. Ideal untuk tech entrepreneur, R&D director, atau inventor dengan visi bisnis.	["Inovasi yang marketable: Riset yang mengarah pada produk viable", "Kepemimpinan teknis strategis: Arah berbasis pemahaman mendalam", "Komersialisasi riset: Menjembatani lab dan pasar", "Credibilitas teknis dan bisnis: Berbicara kedua bahasa"]	["Ketegangan riset vs bisnis: Pure science vs aplikasi komersial", "Impatience dengan riset panjang: Dorongan bisnis vs kebutuhan investigasi", "Komunikasi lintas audiens: Scientist dan investor berbeda"]	["Define milestones: Checkpoint untuk transisi riset ke bisnis", "Tim komplementer: Partner untuk sisi yang bukan kekuatan", "Dual narrative: Cerita berbeda untuk audiens berbeda"]	["Tech startup: Founder dengan latar teknis kuat", "Corporate R&D: Memimpin inovasi dengan orientasi bisnis", "Venture science: Investasi berbasis pemahaman teknis"]	["Pitch teknis: Menjual inovasi dengan kredibilitas", "Presentasi investor: Nilai bisnis dari riset", "Networking strategis: Hubungan untuk funding dan partnership"]	2025-12-23 06:15:22.367907+00	2025-12-23 06:15:22.367907+00
52	RIS	Realistic Investigative Social (RIS)	Kombinasi yang menggabungkan kemampuan teknis, analisis, dan kepedulian sosial. Kamu adalah researcher yang bekerja untuk kebaikan orang. Ideal untuk peneliti kesehatan, engineer untuk dampak sosial, atau educator teknis.	["Riset untuk dampak: Investigasi yang bertujuan membantu orang", "Transfer pengetahuan: Mengajar berdasarkan riset", "Solusi berbasis bukti: Membantu dengan pendekatan yang teruji", "Advokasi ilmiah: Menggunakan data untuk kebijakan yang membantu"]	["Ketegangan akademis vs praktis: Rigor vs relevansi langsung", "Waktu riset vs layanan: Investigasi memakan waktu dari membantu", "Frustrasi implementasi: Temuan tidak selalu diterapkan"]	["Research with purpose: Pertanyaan riset yang langsung relevan", "Kolaborasi komunitas: Melibatkan yang dilayani dalam riset", "Komunikasi hasil: Membuat temuan accessible"]	["Riset kesehatan: Investigasi untuk kesehatan masyarakat", "Engineering for good: Teknologi untuk dampak sosial", "Education research: Riset untuk perbaikan pendidikan"]	["Presentasi accessible: Menjelaskan riset untuk non-ahli", "Listening aktif: Memahami kebutuhan yang dilayani", "Kolaborasi: Bekerja dengan komunitas yang diteliti"]	2025-12-23 06:15:22.371325+00	2025-12-23 06:15:22.371325+00
53	RSA	Realistic Social Artistic (RSA)	Kombinasi yang menggabungkan kemampuan praktis, kepedulian sosial, dan kreativitas. Kamu adalah helper yang kreatif dan hands-on. Ideal untuk art therapist, occupational therapist, atau community artist.	["Terapi melalui kreasi: Membantu orang melalui proses kreatif", "Kreativitas yang accessible: Membuat seni inklusif", "Hands-on helping: Bantuan praktis dan ekspresif", "Komunitas kreatif: Membangun melalui seni bersama"]	["Balance fokus: Antara helper, kreator, dan praktisi", "Standar vs inklusivitas: Kualitas artistik vs partisipasi", "Energi ganda: Memberikan secara emosional dan kreatif"]	["Purpose clarity: Fokus utama adalah membantu, kreativitas adalah medium", "Different standards: Konteks berbeda, ekspektasi berbeda", "Self-care kreatif: Praktik pribadi untuk recharge"]	["Art therapy: Menggunakan seni untuk healing", "Community arts: Program seni untuk komunitas", "Occupational therapy: Rehabilitasi melalui aktivitas"]	["Fasilitasi hangat: Membimbing dengan empati", "Proses over produk: Fokus pada pengalaman, bukan hasil", "Celebrasi inklusif: Menghargai semua upaya"]	2025-12-23 06:15:22.374389+00	2025-12-23 06:15:22.374389+00
54	RSC	Realistic Social Conventional (RSC)	Kombinasi yang menggabungkan kemampuan praktis, kepedulian sosial, dan organisasi. Kamu adalah helper yang sangat terstruktur. Ideal untuk case manager, coordinator program, atau administrator pelayanan sosial.	["Layanan terorganisir: Membantu dengan sistem yang jelas", "Koordinasi care: Mengelola layanan untuk banyak orang", "Dokumentasi untuk kontinuitas: Catatan yang membantu layanan berlanjut", "Advokasi dalam sistem: Bekerja untuk yang dilayani dalam kerangka yang ada"]	["Ketegangan protokol vs kebutuhan: Aturan tidak selalu fit situasi", "Beban administratif: Paperwork mengambil waktu dari layanan", "Frustrasi birokrasi: Sistem tidak selalu mendukung helping"]	["Advokasi sistemis: Bekerja untuk memperbaiki prosedur", "Prioritaskan dokumentasi: Fokus pada yang benar-benar penting", "Support peer: Berbagi beban dengan rekan"]	["Case management: Koordinasi layanan untuk klien", "Program coordinator: Mengelola program bantuan", "Healthcare admin: Koordinasi perawatan pasien"]	["Komunikasi jelas: Instruksi yang mudah diikuti", "Empati profesional: Kehangatan dalam batasan", "Follow-up sistematis: Memastikan layanan tersampaikan"]	2025-12-23 06:15:22.377371+00	2025-12-23 06:15:22.377371+00
55	RSE	Realistic Social Enterprising (RSE)	Kombinasi yang menggabungkan kemampuan praktis, kepedulian sosial, dan ambisi. Kamu adalah pemimpin yang membangun untuk membantu orang. Ideal untuk social entrepreneur, nonprofit director, atau manajer program sosial.	["Dampak yang scalable: Membangun organisasi untuk membantu lebih banyak", "Kepemimpinan misi: Memimpin dengan tujuan sosial", "Resource mobilization: Mendapatkan dukungan untuk cause", "Praktis dan caring: Eksekusi yang efektif dengan hati"]	["Ketegangan misi vs sustainability: Dampak vs keberlanjutan organisasi", "Kepemimpinan emosional: Beban tanggung jawab untuk tim dan yang dilayani", "Burnout misi: Memberikan tanpa batas"]	["Sustainable impact: Organisasi yang sehat bisa membantu lebih lama", "Delegasi misi: Orang lain juga bisa membawa visi", "Self-care sebagai stewardship: Menjaga diri untuk menjaga misi"]	["Social enterprise: Bisnis dengan misi sosial", "Nonprofit leadership: Memimpin organisasi amal", "Program management: Mengelola inisiatif berdampak"]	["Storytelling misi: Mengkomunikasikan dampak", "Networking untuk cause: Membangun dukungan", "Team building caring: Tim yang peduli pada misi"]	2025-12-23 06:15:22.379597+00	2025-12-23 06:15:22.379597+00
56	RSI	Realistic Social Investigative (RSI)	Kombinasi yang menggabungkan kemampuan praktis, kepedulian sosial, dan analisis. Kamu adalah helper yang berbasis evidence. Ideal untuk health educator, researcher terapan, atau program evaluator.	["Helping berbasis bukti: Intervensi yang didukung riset", "Evaluasi program: Mengukur dampak layanan", "Transfer pengetahuan praktis: Mengajar berdasarkan temuan", "Advocacy berbasis data: Menggunakan bukti untuk perubahan"]	["Ketegangan akademis vs praktis: Rigor vs membantu langsung", "Waktu riset vs layanan: Evaluasi memakan waktu dari membantu", "Komunikasi temuan: Membuat riset accessible"]	["Practice-based research: Riset yang embedded dalam layanan", "Rapid evaluation: Metodologi cepat untuk feedback", "Plain language: Menjelaskan tanpa jargon"]	["Program evaluation: Menilai efektivitas intervensi", "Health education: Pendidikan kesehatan berbasis bukti", "Applied research: Riset untuk perbaikan praktik"]	["Presentasi accessible: Temuan untuk non-ahli", "Listening aktif: Memahami kebutuhan", "Collaborative inquiry: Riset dengan yang dilayani"]	2025-12-23 06:15:22.382407+00	2025-12-23 06:15:22.382407+00
57	IAC	Investigative Artistic Conventional (IAC)	Kombinasi yang menggabungkan analisis, kreativitas, dan organisasi. Kamu adalah peneliti kreatif yang terstruktur. Ideal untuk museum curator, archivist, atau research librarian.	["Riset kreatif terorganisir: Investigasi estetis dengan metodologi", "Curation sistematis: Mengorganisir koleksi dengan mata kuratorial", "Dokumentasi estetis: Catatan yang informatif dan menarik", "Knowledge management: Mengelola informasi secara kreatif"]	["Ketegangan tiga dimensi: Rigor, kreativitas, dan struktur bersaing", "Waktu untuk setiap aspek: Semuanya memerlukan perhatian", "Standar ganda atau triple: Sempurna di semua dimensi"]	["Prioritas kontekstual: Dimensi mana yang paling penting untuk tugas ini", "Sistem fleksibel: Struktur yang memberi ruang untuk discovery", "Kolaborasi: Partner untuk aspek yang bukan kekuatan utama"]	["Museum: Kurasi dan riset", "Archive: Mengelola koleksi historis", "Library: Research librarianship"]	["Presentasi kuratorial: Menjelaskan pilihan dengan rigor dan estetika", "Dokumentasi terstruktur: Catatan yang komprehensif", "Diskusi interdisipliner: Berbicara tentang riset dan kreativitas"]	2025-12-23 06:15:22.385114+00	2025-12-23 06:15:22.385114+00
58	IAE	Investigative Artistic Enterprising (IAE)	Kombinasi yang menggabungkan analisis, kreativitas, dan ambisi. Kamu adalah inovator kreatif yang ambisius. Ideal untuk creative agency founder, innovation consultant, atau entertainment executive.	["Inovasi kreatif strategis: Ide baru dengan visi bisnis", "Riset tren: Menganalisis pasar untuk peluang kreatif", "Kepemimpinan kreatif: Memimpin tim inovatif", "Pitch yang meyakinkan: Menjual ide dengan bukti dan estetika"]	["Terlalu banyak ide: Sulit fokus pada eksekusi", "Ketegangan art vs commerce: Kreativitas vs profitabilitas", "Analisis vs intuisi kreatif: Data tidak selalu menangkap magic"]	["Curate ideas: Pilih yang paling viable untuk dikejar", "Define success criteria: Apa yang membuat ide worth pursuing", "Trust creative intuition: Data sebagai input, bukan master"]	["Creative agency: Bisnis layanan kreatif", "Innovation consulting: Membantu organisasi berinovasi", "Entertainment: Produksi konten dengan visi bisnis"]	["Pitch kreatif: Presentasi yang inspiring dan strategis", "Networking industri: Hubungan untuk peluang", "Trend spotting: Diskusi tentang arah industri"]	2025-12-23 06:15:22.388056+00	2025-12-23 06:15:22.388056+00
59	IAR	Investigative Artistic Realistic (IAR)	Kombinasi yang menggabungkan analisis, kreativitas, dan kemampuan praktis. Kamu adalah peneliti-kreator yang bisa membangun. Ideal untuk R&D artist, experimental designer, atau scientific illustrator.	["Prototyping berbasis riset: Membangun berdasarkan investigasi", "Visualisasi kompleksitas: Membuat abstrak menjadi tangible", "Eksperimen hands-on: Testing ide secara praktis", "Kreasi analitis: Seni yang didukung pemahaman mendalam"]	["Terlalu banyak dimensi: Riset, kreasi, dan eksekusi semua penting", "Waktu proses: Setiap fase memerlukan perhatian", "Komunikasi kompleks: Menjelaskan pekerjaan multidimensional"]	["Fase project: Waktu terpisah untuk investigasi, ideasi, dan eksekusi", "Fokus per project: Mungkin tidak semua dimensi sama pentingnya", "Dokumentasi proses: Catatan untuk learning dan sharing"]	["Lab desain: R&D untuk produk kreatif", "Scientific visualization: Mengkomunikasikan sains secara visual", "Experimental art: Seni berbasis riset"]	["Presentasi proses: Menunjukkan perjalanan dari riset ke kreasi", "Demonstrasi: Menunjukkan prototipe dan eksperimen", "Diskusi interdisipliner: Sains dan seni bersama"]	2025-12-23 06:15:22.391257+00	2025-12-23 06:15:22.391257+00
60	IAS	Investigative Artistic Social (IAS)	Kombinasi yang menggabungkan analisis, kreativitas, dan kepedulian sosial. Kamu adalah peneliti kreatif untuk kebaikan manusia. Ideal untuk design researcher, art therapist researcher, atau social innovation designer.	["Riset untuk desain: Investigasi kebutuhan manusia untuk solusi kreatif", "Kreativitas empatis: Seni dan desain yang berakar pada pemahaman orang", "Knowledge sharing: Mengkomunikasikan temuan secara accessible", "Human-centered innovation: Inovasi berbasis riset tentang orang"]	["Ketegangan prioritas: Riset, kreativitas, atau membantu dulu", "Scope creep: Ingin memahami, menciptakan, DAN membantu semua", "Energi untuk tiga dimensi: Intellect, creativity, dan empathy semua dibutuhkan"]	["Define primary goal: Untuk siapa dan untuk apa", "Collaborative approach: Partner untuk dimensi yang bukan kekuatan", "Sustainable pace: Tidak harus semua sekaligus"]	["Design research: Memahami pengguna untuk desain", "Art therapy research: Riset efektivitas terapi seni", "Social innovation: Desain solusi untuk masalah sosial"]	["Presentasi empatis: Sharing temuan dengan sensitivitas", "Co-creation: Proses kreatif bersama yang diteliti", "Storytelling berbasis riset: Narasi yang didukung data"]	2025-12-23 06:15:22.393884+00	2025-12-23 06:15:22.393884+00
61	ICA	Investigative Conventional Artistic (ICA)	Kombinasi yang menggabungkan analisis, organisasi, dan kreativitas. Kamu adalah analis terstruktur dengan sensibilitas estetis. Ideal untuk information designer, technical illustrator, atau museum cataloguer.	["Visualisasi data: Mengkomunikasikan analisis secara estetis", "Sistem yang elegan: Organisasi yang fungsional dan indah", "Dokumentasi yang menarik: Laporan yang informatif dan engaging", "Knowledge architecture: Struktur informasi yang intuitif"]	["Ketegangan efisiensi vs estetika: Yang paling sistematis tidak selalu paling indah", "Waktu untuk polish: Detail visual memerlukan waktu ekstra", "Standar ganda: Akurat DAN menarik"]	["Design system: Template yang sudah estetis", "Prioritas konteks: Kapan estetika worth investment", "Collaboration: Partner untuk aspek yang bukan kekuatan"]	["Information design: Visualisasi data dan informasi", "Technical illustration: Diagram teknis yang jelas dan menarik", "Knowledge management: Organisasi informasi yang accessible"]	["Presentasi visual: Laporan dengan grafik dan layout yang baik", "Dokumentasi estetis: Catatan yang mudah dibaca dan menarik", "Diskusi sistematis: Menjelaskan dengan struktur yang jelas"]	2025-12-23 06:15:22.396553+00	2025-12-23 06:15:22.396553+00
62	ICE	Investigative Conventional Enterprising (ICE)	Kombinasi yang menggabungkan analisis, organisasi, dan ambisi. Kamu adalah analis strategis yang terstruktur. Ideal untuk management consultant, business analyst, atau strategy director.	["Analisis strategis: Investigasi untuk keputusan bisnis", "Framework metodologis: Pendekatan terstruktur untuk masalah kompleks", "Rekomendasi berbasis bukti: Saran yang didukung data", "Optimasi sistematis: Perbaikan berkelanjutan berbasis analisis"]	["Analysis paralysis: Terlalu banyak riset sebelum aksi", "Kekakuan metodologis: Terlalu terikat pada framework", "Overconfidence dari data: Data tidak menangkap semuanya"]	["Decision thresholds: Kapan data cukup untuk bergerak", "Adaptive frameworks: Metodologi yang bisa disesuaikan", "Integrate qualitative: Data kuantitatif bukan satu-satunya sumber"]	["Consulting: Strategi dan manajemen", "Business analysis: Mendukung keputusan dengan data", "Corporate strategy: Perencanaan jangka panjang"]	["Presentasi terstruktur: Rekomendasi dengan logika yang jelas", "Reporting reguler: Update berbasis data", "Diskusi strategis: Dialog tentang arah dan opsi"]	2025-12-23 06:15:22.399457+00	2025-12-23 06:15:22.399457+00
63	ICR	Investigative Conventional Realistic (ICR)	Kombinasi yang menggabungkan analisis, organisasi, dan kemampuan praktis. Kamu adalah researcher yang sangat sistematis dan hands-on. Ideal untuk lab manager, quality engineer, atau technical auditor.	["Riset praktis terstruktur: Investigasi dengan metodologi ketat dan eksekusi", "Quality management: Standar dan pengujian sistematis", "Troubleshooting metodis: Diagnosis berdasarkan protokol", "Dokumentasi teknis: Catatan komprehensif dari proses dan temuan"]	["Kekakuan metodologis: Protokol tidak selalu fit situasi baru", "Waktu dokumentasi: Ketelitian memakan waktu signifikan", "Resistensi adaptasi: Investasi dalam metode membuat sulit berubah"]	["Adaptive protocols: Panduan dengan ruang untuk judgment", "Efficient documentation: Template yang streamlined", "Continuous improvement: Metodologi juga perlu update"]	["Laboratory management: Mengawasi operasi lab", "Quality engineering: Standar dan pengujian", "Technical audit: Evaluasi sistematis"]	["Laporan terstruktur: Format yang konsisten dan detail", "Demonstrasi prosedur: Menunjukkan metodologi", "Diskusi teknis: Dialog tentang proses dan standar"]	2025-12-23 06:15:22.401873+00	2025-12-23 06:15:22.401873+00
64	ICS	Investigative Conventional Social (ICS)	Kombinasi yang menggabungkan analisis, organisasi, dan kepedulian sosial. Kamu adalah analis yang bekerja untuk membantu orang dalam kerangka terstruktur. Ideal untuk program evaluator, policy researcher, atau healthcare analyst.	["Evaluasi program: Mengukur dampak intervensi sosial", "Riset kebijakan: Investigasi untuk keputusan yang mempengaruhi orang", "Advocacy berbasis data: Menggunakan bukti untuk perubahan", "Layanan berbasis bukti: Memastikan intervensi efektif"]	["Ketegangan akademis vs praktis: Rigor vs relevansi langsung", "Frustrasi implementasi: Temuan tidak selalu diterapkan", "Komunikasi untuk non-ahli: Membuat riset accessible"]	["Actionable research: Investigasi dengan rekomendasi jelas", "Stakeholder engagement: Melibatkan yang terdampak dalam proses", "Plain language: Menjelaskan tanpa jargon"]	["Program evaluation: Menilai efektivitas layanan", "Policy research: Riset untuk keputusan kebijakan", "Healthcare analysis: Mengoptimalkan sistem kesehatan"]	["Presentasi accessible: Temuan untuk non-ahli", "Report yang actionable: Rekomendasi yang bisa diterapkan", "Kolaborasi: Bekerja dengan yang dilayani oleh kebijakan"]	2025-12-23 06:15:22.405449+00	2025-12-23 06:15:22.405449+00
65	IEA	Investigative Enterprising Artistic (IEA)	Kombinasi yang menggabungkan analisis, ambisi, dan kreativitas. Kamu adalah inovator strategis yang kreatif. Ideal untuk innovation director, venture creative, atau strategy consultant untuk industri kreatif.	["Strategi inovasi: Menganalisis peluang untuk kreativitas yang berdampak", "Trend analysis kreatif: Memahami arah industri untuk positioning", "Pitch yang meyakinkan: Menjual ide dengan riset dan vision", "Creative ventures: Investasi atau inkubasi ide kreatif"]	["Terlalu banyak ide: Analisis menunjukkan banyak peluang", "Ketegangan art vs commerce: Kreativitas murni vs viability", "Decision complexity: Tiga dimensi membuat keputusan kompleks"]	["Prioritization framework: Kriteria untuk memilih ide", "Quick validation: Test cepat sebelum investasi besar", "Balance passion dan profit: Tidak harus mutually exclusive"]	["Innovation consulting: Membantu organisasi berinovasi secara kreatif", "Creative ventures: Investasi di startup kreatif", "Strategy for creatives: Konsultasi untuk industri kreatif"]	["Pitch inspiratif: Visi dengan data pendukung", "Networking strategis: Hubungan untuk peluang", "Trend briefing: Sharing insight tentang arah industri"]	2025-12-23 06:15:22.408475+00	2025-12-23 06:15:22.408475+00
66	IEC	Investigative Enterprising Conventional (IEC)	Kombinasi yang menggabungkan analisis, ambisi, dan organisasi. Kamu adalah eksekutif yang berbasis riset. Ideal untuk VP Strategy, chief analyst, atau management consultant senior.	["Strategi berbasis bukti: Arah organisasi didukung analisis", "Governance data-driven: Pengambilan keputusan sistematis", "Optimasi skala: Perbaikan yang terukur dan scalable", "Leadership intellektual: Memimpin dengan insight dan rigor"]	["Analysis paralysis: Terlalu banyak riset sebelum bertindak", "Over-reliance on data: Tidak semua keputusan bisa dikuantifikasi", "Complexity in communication: Analisis yang terlalu teknis untuk audiens"]	["Decision protocols: Kapan data cukup untuk bergerak", "Simplify communication: Insight tanpa kompleksitas", "Trust intuition: Data sebagai input, bukan pengganti judgment"]	["Corporate strategy: Perencanaan strategis", "Management consulting: Advisory untuk eksekutif", "Business intelligence: Memimpin fungsi analitik"]	["Executive briefing: Insight yang ringkas dan actionable", "Board presentation: Strategi dengan data pendukung", "Strategic dialogue: Diskusi tentang arah dan opsi"]	2025-12-23 06:15:22.411526+00	2025-12-23 06:15:22.411526+00
67	IER	Investigative Enterprising Realistic (IER)	Kombinasi yang menggabungkan analisis, ambisi, dan kemampuan praktis. Kamu adalah teknolog-entrepreneur yang berbasis riset. Ideal untuk deep tech founder, R&D executive, atau technical investor.	["Tech commercialization: Membawa riset ke pasar", "Due diligence teknis: Evaluasi mendalam investasi teknologi", "Leadership R&D: Memimpin inovasi dengan orientasi bisnis", "Prototype to product: Mengeksekusi transisi dari lab ke produksi"]	["Tension research vs market: Pure science vs aplikasi komersial", "Impatience dengan riset panjang: Dorongan bisnis vs kebutuhan investigasi", "Technical optimism: Meremehkan tantangan komersialisasi"]	["Milestone clarity: Checkpoint untuk transisi lab ke market", "Market validation early: Test asumsi pasar sebelum investasi besar", "Diverse team: Partner untuk sisi yang bukan kekuatan"]	["Deep tech startup: Founder berbasis riset", "Corporate R&D leadership: Memimpin inovasi dengan orientasi bisnis", "Technical investing: VC atau angel untuk tech"]	["Pitch teknis: Kredibilitas teknologi dengan visi bisnis", "Investor presentation: Peluang pasar dengan defensibility teknis", "Technical networking: Hubungan di komunitas riset dan bisnis"]	2025-12-23 06:15:22.420388+00	2025-12-23 06:15:22.420388+00
68	IES	Investigative Enterprising Social (IES)	Kombinasi yang menggabungkan analisis, ambisi, dan kepedulian sosial. Kamu adalah pemimpin yang menggunakan riset untuk dampak sosial. Ideal untuk social enterprise leader, impact investor, atau policy entrepreneur.	["Impact measurement: Mengukur dan mengoptimalkan dampak sosial", "Evidence-based advocacy: Menggunakan riset untuk perubahan kebijakan", "Scaling solutions: Memperbesar solusi yang terbukti efektif", "Strategic philanthropy: Donasi dan investasi berbasis riset"]	["Tension scale vs depth: Menjangkau lebih banyak vs membantu lebih baik", "Data limitations: Tidak semua dampak mudah diukur", "Impatience dengan proses: Dorongan hasil vs kebutuhan riset"]	["Theory of change: Framework untuk dampak yang terukur", "Mixed methods: Kuantitatif dan kualitatif", "Long-term view: Dampak berkelanjutan vs quick wins"]	["Impact investing: Investasi untuk return dan dampak", "Social enterprise: Bisnis dengan misi sosial", "Policy entrepreneurship: Mendorong perubahan kebijakan"]	["Impact pitch: Menjual dampak dengan data", "Stakeholder engagement: Dialog dengan yang dilayani dan funder", "Advocacy presentation: Bukti untuk perubahan kebijakan"]	2025-12-23 06:15:22.426586+00	2025-12-23 06:15:22.426586+00
69	IRA	Investigative Realistic Artistic (IRA)	Kombinasi yang menggabungkan analisis, kemampuan praktis, dan kreativitas. Kamu adalah builder yang meneliti dan berkreasi. Ideal untuk experimental engineer, maker-researcher, atau product innovator.	["Build to learn: Membuat prototipe untuk memahami", "Creative engineering: Solusi teknis yang inovatif", "Research through making: Investigasi melalui kreasi", "Aesthetic functionality: Teknis yang juga indah"]	["Too many interests: Riset, building, dan kreativitas semua menarik", "Time allocation: Setiap dimensi memerlukan investasi", "Communication challenge: Menjelaskan pekerjaan multidimensional"]	["Project focus: Mana dimensi yang paling penting untuk ini", "Portfolio approach: Proyek berbeda, emphasis berbeda", "Documentation: Catatan untuk learning dan sharing"]	["Maker spaces: R&D yang hands-on dan kreatif", "Product innovation: Desain dan engineering produk baru", "Experimental engineering: Pushing boundaries teknis"]	["Show and tell: Demonstrasi prototipe dan proses", "Visual documentation: Catatan yang estetis", "Cross-disciplinary dialogue: Sains, craft, dan seni bersama"]	2025-12-23 06:15:22.429132+00	2025-12-23 06:15:22.429132+00
70	IRC	Investigative Realistic Conventional (IRC)	Kombinasi yang menggabungkan analisis, kemampuan praktis, dan organisasi. Kamu adalah researcher-technician yang sangat sistematis. Ideal untuk lab technician senior, quality analyst, atau technical standards specialist.	["Research execution: Menjalankan riset dengan presisi", "Method development: Membuat dan memperbaiki protokol", "Technical documentation: Catatan yang komprehensif dan replicable", "Quality assurance: Memastikan standar terpenuhi"]	["Rigid adherence: Terlalu terikat pada protokol yang ada", "Documentation overhead: Ketelitian memakan waktu", "Adaptation difficulty: Investasi dalam metode membuat perubahan sulit"]	["Protocol review: Evaluasi berkala untuk improvement", "Efficient templates: Dokumentasi yang streamlined", "Flexibility windows: Ruang untuk adaptasi dalam struktur"]	["Laboratory: Eksekusi riset terstruktur", "Quality control: Pengujian dan standar", "Technical standards: Pengembangan dan compliance"]	["Procedural communication: Instruksi yang jelas", "Technical reporting: Laporan yang detail dan terstruktur", "Method sharing: Dokumentasi untuk replikasi"]	2025-12-23 06:15:22.431803+00	2025-12-23 06:15:22.431803+00
71	IRE	Investigative Realistic Enterprising (IRE)	Kombinasi yang menggabungkan analisis, kemampuan praktis, dan ambisi. Kamu adalah teknolog-entrepreneur yang hands-on. Ideal untuk hardware startup founder, manufacturing innovator, atau technical product leader.	["Product development: Dari riset ke produk yang marketable", "Technical leadership: Memimpin dengan kredibilitas hands-on", "Prototyping untuk bisnis: Membangun untuk membuktikan viability", "Operational innovation: Memperbaiki proses produksi"]	["Doing vs leading: Preference untuk hands-on vs delegasi", "Technical perfectionism: Ingin sempurna sebelum launch", "Scale challenges: Prototipe berbeda dari produksi"]	["Build the team: Orang yang bisa eksekusi visimu", "MVP mindset: Good enough untuk validasi pasar", "Manufacturing partnership: Expertise untuk scale"]	["Hardware startup: Produk fisik dengan teknologi", "Manufacturing: Inovasi proses produksi", "Technical entrepreneurship: Bisnis berbasis keahlian teknis"]	["Demo culture: Showing working prototypes", "Technical pitch: Kredibilitas teknis dengan visi bisnis", "Operational metrics: Berbicara dalam efisiensi dan output"]	2025-12-23 06:15:22.434364+00	2025-12-23 06:15:22.434364+00
72	IRS	Investigative Realistic Social (IRS)	Kombinasi yang menggabungkan analisis, kemampuan praktis, dan kepedulian sosial. Kamu adalah researcher-practitioner yang membantu orang. Ideal untuk biomedical engineer, assistive technology developer, atau health researcher praktis.	["Solusi berbasis riset: Membangun untuk membantu berdasarkan bukti", "Human-centered engineering: Teknologi yang melayani kebutuhan manusia", "Practical intervention: Intervensi yang bisa diimplementasikan", "Applied research: Investigasi dengan tujuan langsung"]	["Tension academic vs applied: Rigor vs relevansi langsung", "User involvement: Melibatkan yang dilayani dalam proses", "Adoption challenges: Solusi bagus tidak selalu digunakan"]	["Co-design: Melibatkan pengguna dari awal", "Implementation science: Memahami adopsi, bukan hanya efficacy", "Communication for non-experts: Membuat riset accessible"]	["Biomedical: Teknologi untuk kesehatan", "Assistive technology: Alat untuk kebutuhan khusus", "Applied health research: Riset dengan aplikasi langsung"]	["User-centered presentation: Fokus pada manfaat untuk pengguna", "Demo dengan empati: Menunjukkan bagaimana solusi membantu", "Collaborative research: Bekerja dengan komunitas yang dilayani"]	2025-12-23 06:15:22.438708+00	2025-12-23 06:15:22.438708+00
73	ISA	Investigative Social Artistic (ISA)	Kombinasi yang menggabungkan analisis, kepedulian sosial, dan kreativitas. Kamu adalah researcher yang menggunakan kreativitas untuk memahami dan membantu orang. Ideal untuk ethnographer, qualitative researcher kreatif, atau arts-based researcher.	["Riset kreatif: Metodologi inovatif untuk memahami manusia", "Narrative research: Menggunakan cerita untuk insight", "Empathic inquiry: Investigasi yang sensitive dan mendalam", "Knowledge sharing kreatif: Menyampaikan temuan secara engaging"]	["Methodological tension: Rigor vs kreativitas vs sensitivitas", "Subjectivity management: Kedekatan emosional bisa bias", "Audience mismatch: Akademis vs populer vs yang diteliti"]	["Reflexivity: Kesadaran akan posisi dan bias", "Multiple outputs: Berbagai format untuk berbagai audiens", "Ethical creativity: Inovasi yang menghormati partisipan"]	["Qualitative research: Investigasi mendalam tentang manusia", "Arts-based research: Menggunakan seni sebagai metode", "Community research: Riset dengan dan untuk komunitas"]	["Storytelling research: Menyampaikan temuan melalui narasi", "Visual methods: Menggunakan gambar dan media dalam riset", "Participatory dialogue: Proses riset yang kolaboratif"]	2025-12-23 06:15:22.441989+00	2025-12-23 06:15:22.441989+00
74	ISC	Investigative Social Conventional (ISC)	Kombinasi yang menggabungkan analisis, kepedulian sosial, dan organisasi. Kamu adalah analis sistematis yang bekerja untuk orang. Ideal untuk social worker researcher, program analyst, atau institutional researcher.	["Systematic care: Layanan yang terorganisir dan berbasis bukti", "Program evaluation: Mengukur dan memperbaiki intervensi sosial", "Data for good: Menggunakan analisis untuk keputusan yang membantu", "Compliant advocacy: Bekerja dalam sistem untuk kebaikan"]	["Bureaucracy frustration: Sistem tidak selalu mendukung helping", "Data limitations: Tidak semua caring bisa diukur", "Role tension: Researcher vs helper vs administrator"]	["Purpose clarity: Analisis untuk membantu, bukan sebaliknya", "Mixed methods: Menangkap apa yang tidak bisa dikuantifikasi", "System navigation: Bekerja dalam batasan sambil advocating untuk perubahan"]	["Social research: Riset kebijakan dan program sosial", "Institutional research: Analisis untuk organisasi pendidikan atau kesehatan", "Program evaluation: Menilai efektivitas layanan"]	["Data-informed caring: Menjelaskan bagaimana data membantu keputusan", "Accessible reporting: Temuan untuk non-ahli", "Collaborative analysis: Melibatkan stakeholder dalam interpretasi"]	2025-12-23 06:15:22.444538+00	2025-12-23 06:15:22.444538+00
75	ISE	Investigative Social Enterprising (ISE)	Kombinasi yang menggabungkan analisis, kepedulian sosial, dan ambisi. Kamu adalah pemimpin yang menggunakan riset untuk dampak sosial skala besar. Ideal untuk social impact leader, policy entrepreneur, atau nonprofit executive berbasis riset.	["Evidence-based scaling: Memperbesar solusi yang terbukti", "Strategic philanthropy: Investasi sosial berbasis analisis", "Policy influence: Menggunakan riset untuk perubahan sistemik", "Impact leadership: Memimpin dengan insight dan ambisi"]	["Scale vs depth tension: Menjangkau banyak vs membantu mendalam", "Impatience with research: Dorongan hasil vs kebutuhan rigor", "Data-driven vs human-centered: Metrik vs cerita"]	["Theory of change: Framework untuk dampak terukur", "Balance metrics and stories: Data dan narasi bersama", "Long-term patience: Perubahan sistemik memerlukan waktu"]	["Impact sector leadership: Memimpin organisasi sosial", "Policy research: Riset untuk perubahan kebijakan", "Strategic philanthropy: Mengarahkan sumber daya untuk dampak maksimal"]	["Impact pitch: Data dan cerita untuk memotivasi aksi", "Stakeholder engagement: Dialog dengan funder, penerima manfaat, dan pembuat kebijakan", "Thought leadership: Sharing insight untuk menggerakkan sektor"]	2025-12-23 06:15:22.447509+00	2025-12-23 06:15:22.447509+00
76	ISR	Investigative Social Realistic (ISR)	Kombinasi yang menggabungkan analisis, kepedulian sosial, dan kemampuan praktis. Kamu adalah researcher-practitioner yang hands-on membantu orang. Ideal untuk occupational therapist researcher, public health practitioner, atau applied social researcher.	["Practice-based research: Riset yang embedded dalam layanan", "Practical interventions: Solusi yang bisa diimplementasikan", "Human-centered problem-solving: Memahami dan membantu secara konkret", "Knowledge translation: Membuat riset actionable"]	["Role tension: Researcher vs practitioner vs helper", "Time allocation: Riset, praktek, dan caring semua penting", "Adoption challenges: Temuan tidak selalu diterapkan"]	["Integrated practice: Riset sebagai bagian dari layanan", "Quick cycles: Test dan improve secara iterative", "Co-production: Melibatkan yang dilayani dalam proses"]	["Applied health research: Riset untuk praktik kesehatan", "Community-based research: Investigasi dengan komunitas", "Intervention development: Membuat dan menguji solusi praktis"]	["Accessible communication: Temuan untuk praktisi dan komunitas", "Demonstration: Menunjukkan intervensi yang bekerja", "Collaborative inquiry: Proses riset yang inklusif"]	2025-12-23 06:15:22.449756+00	2025-12-23 06:15:22.449756+00
77	ACE	Artistic Conventional Enterprising (ACE)	Kombinasi yang menggabungkan kreativitas, organisasi, dan ambisi. Kamu adalah kreator yang terorganisir dengan visi bisnis. Ideal untuk creative producer, brand manager, atau agency owner.	["Produksi kreatif terstruktur: Mengorganisir proses kreatif yang kompleks", "Brand building: Membangun identitas dengan kreativitas dan strategi", "Creative business: Mengembangkan bisnis berbasis kreativitas", "Project management kreatif: Mengelola proyek dengan timeline dan kualitas"]	["Tension kreativitas vs struktur: Sistem bisa membatasi eksplorasi", "Business vs art: Profitabilitas vs ekspresi murni", "Control vs freedom: Manajemen vs kreativitas"]	["Creative frameworks: Struktur yang memfasilitasi, bukan membatasi", "Portfolio balance: Proyek komersial dan passion", "Team building: Orang yang bisa handle berbagai aspek"]	["Creative agency: Bisnis layanan kreatif", "Brand management: Membangun dan mengelola brand", "Media production: Mengorganisir produksi konten"]	["Pitch terstruktur: Kreativitas dengan timeline dan budget", "Project updates: Laporan progress yang visual", "Client management: Menyeimbangkan visi dan kebutuhan klien"]	2025-12-23 06:15:22.452574+00	2025-12-23 06:15:22.452574+00
78	ACI	Artistic Conventional Investigative (ACI)	Kombinasi yang menggabungkan kreativitas, organisasi, dan analisis. Kamu adalah kreator yang sistematis dan berbasis riset. Ideal untuk UX researcher, information architect, atau design systems specialist.	["Research-based design: Kreativitas yang didukung investigasi", "Design systems: Membangun framework untuk konsistensi kreatif", "Information architecture: Mengorganisir kompleksitas secara intuitif", "Dokumentasi desain: Mencatat keputusan dan rationale"]	["Analysis vs intuition: Data tidak selalu menangkap magic", "System rigidity: Framework bisa membatasi eksplorasi", "Perfection paralysis: Ingin riset dan sistem sempurna"]	["Informed intuition: Riset sebagai input, bukan master", "Living systems: Framework yang evolve dengan pembelajaran", "Ship and iterate: Rilis dan perbaiki berdasarkan feedback"]	["UX research: Memahami pengguna untuk desain", "Design systems: Membangun dan memelihara konsistensi", "Information design: Mengorganisir dan memvisualisasi kompleksitas"]	["Research presentation: Insight untuk keputusan desain", "System documentation: Panduan yang jelas dan estetis", "Cross-functional dialogue: Berbicara dengan desainer dan developer"]	2025-12-23 06:15:22.456337+00	2025-12-23 06:15:22.456337+00
79	ACR	Artistic Conventional Realistic (ACR)	Kombinasi yang menggabungkan kreativitas, organisasi, dan kemampuan praktis. Kamu adalah kreator yang terorganisir dan hands-on. Ideal untuk production designer, prop master, atau exhibit designer.	["Production design: Menciptakan dunia fisik yang estetis", "Organized making: Proses kreatif yang terstruktur", "Material management: Mengorganisir sumber daya kreatif", "Technical creativity: Membangun dengan presisi dan keindahan"]	["Time pressure: Deadline produksi vs kesempurnaan kreatif", "Budget constraints: Visi vs realitas sumber daya", "Team coordination: Banyak orang dan proses untuk dikelola"]	["Contingency planning: Alternatif untuk setiap kemungkinan", "Resourcefulness: Kreativitas dalam batasan", "Clear delegation: Komunikasi yang tepat dengan tim"]	["Film/TV production: Desain set dan prop", "Event design: Menciptakan pengalaman fisik", "Exhibit design: Instalasi museum atau pameran"]	["Visual briefs: Komunikasi melalui sketsa dan referensi", "Production meetings: Koordinasi dengan berbagai departemen", "Hands-on demonstration: Menunjukkan apa yang dimaksud"]	2025-12-23 06:15:22.459002+00	2025-12-23 06:15:22.459002+00
80	ACS	Artistic Conventional Social (ACS)	Kombinasi yang menggabungkan kreativitas, organisasi, dan kepedulian sosial. Kamu adalah kreator yang membantu orang dalam kerangka terstruktur. Ideal untuk program coordinator seni, museum educator, atau arts administrator.	["Arts programming: Mengorganisir pengalaman kreatif untuk orang", "Community arts: Memfasilitasi kreativitas inklusif", "Arts education: Mengajar dengan kurikulum dan kreativitas", "Event coordination: Mengelola acara yang engaging dan terorganisir"]	["Bureaucracy vs creativity: Sistem administrasi bisa meredam semangat", "Inclusion vs excellence: Partisipasi luas vs standar tinggi", "Energy drain: Caring dan creating dan organizing semua melelahkan"]	["Purpose clarity: Organisasi melayani kreativitas dan komunitas", "Differentiated programming: Berbagai level untuk berbagai kebutuhan", "Self-care scheduling: Waktu untuk recharge"]	["Arts organization: Mengelola program seni", "Museum education: Mengembangkan dan deliver program", "Community center: Koordinasi program kreatif"]	["Warm professionalism: Caring dalam konteks formal", "Program promotion: Mengkomunikasikan peluang berpartisipasi", "Participant feedback: Mendengar dan merespons kebutuhan"]	2025-12-23 06:15:22.461799+00	2025-12-23 06:15:22.461799+00
81	AEC	Artistic Enterprising Conventional (AEC)	Kombinasi yang menggabungkan kreativitas, ambisi, dan organisasi. Kamu adalah entrepreneur kreatif yang terorganisir. Ideal untuk creative agency founder, entertainment producer, atau design firm leader.	["Creative business leadership: Memimpin organisasi kreatif", "Scalable creativity: Sistem untuk output kreatif konsisten", "Brand and business: Membangun reputasi dan revenue", "Client acquisition: Winning business dengan kreativitas"]	["Art vs commerce tension: Kreativitas murni vs profitabilitas", "Growth vs quality: Scale vs craft", "Leadership vs doing: Managing vs creating"]	["Clear positioning: Apa yang membuat berbeda dan valuable", "Quality controls: Sistem untuk mempertahankan standar", "Role clarity: Kapan lead, kapan create"]	["Creative agency: Bisnis layanan kreatif", "Entertainment company: Produksi konten dengan struktur bisnis", "Design studio: Praktek desain yang scalable"]	["New business pitch: Menjual kapabilitas kreatif", "Team leadership: Memotivasi kreator", "Client management: Menyeimbangkan ekspektasi dan delivery"]	2025-12-23 06:15:22.4641+00	2025-12-23 06:15:22.4641+00
82	AEI	Artistic Enterprising Investigative (AEI)	Kombinasi yang menggabungkan kreativitas, ambisi, dan analisis. Kamu adalah innovator kreatif yang strategis. Ideal untuk creative director strategis, innovation lead, atau trend forecaster.	["Strategic creativity: Kreativitas yang informed oleh riset dan tren", "Trend forecasting: Menganalisis dan memprediksi arah kreatif", "Innovation leadership: Memimpin pengembangan ide baru", "Creative intelligence: Insight untuk keputusan kreatif"]	["Analysis vs intuition: Data vs feeling kreatif", "Trend following vs setting: Mengikuti atau memimpin", "Complexity overload: Terlalu banyak variabel untuk dipertimbangkan"]	["Informed intuition: Riset sebagai input, bukan pengganti taste", "Point of view: Memiliki perspektif, bukan hanya mengikuti", "Simplify communication: Insight tanpa overwhelming complexity"]	["Trend agencies: Forecasting dan strategy", "Innovation teams: Pengembangan produk atau layanan baru", "Creative strategy: Consulting untuk brand dan kreativitas"]	["Trend briefing: Sharing insight tentang arah pasar", "Strategic creative presentation: Visi dengan rationale", "Client education: Membantu memahami landscape kreatif"]	2025-12-23 06:15:22.466619+00	2025-12-23 06:15:22.466619+00
83	AER	Artistic Enterprising Realistic (AER)	Kombinasi yang menggabungkan kreativitas, ambisi, dan kemampuan praktis. Kamu adalah kreator-entrepreneur yang hands-on. Ideal untuk maker-entrepreneur, creative producer, atau studio owner.	["Making and selling: Menciptakan dan mengkomersialkan", "Production leadership: Memimpin pembuatan karya", "Creative product development: Dari ide ke produk marketable", "Hands-on entrepreneurship: Founder yang bisa buat sendiri"]	["Doing vs scaling: Preference untuk hands-on vs growing business", "Quality vs quantity: Craft vs volume", "Time allocation: Create, lead, atau sell"]	["Leverage specialty: Fokus pada apa yang hanya kamu bisa", "Build team: Orang untuk aspek yang bukan kekuatan", "Product-service mix: Balance antara scalable dan bespoke"]	["Maker business: Studio atau workshop dengan produk", "Creative production: Memimpin pembuatan konten", "Product design: Menciptakan dan meluncurkan produk"]	["Show and sell: Demonstrasi kemampuan untuk menarik bisnis", "Maker story: Narasi proses untuk marketing", "Direct feedback: Belajar dari reaksi pelanggan"]	2025-12-23 06:15:22.469559+00	2025-12-23 06:15:22.469559+00
84	AES	Artistic Enterprising Social (AES)	Kombinasi yang menggabungkan kreativitas, ambisi, dan kepedulian sosial. Kamu adalah kreator yang ingin sukses sambil membuat perbedaan. Ideal untuk social enterprise kreatif, cause marketing, atau entertainment dengan misi.	["Purpose-driven creativity: Seni dan bisnis untuk kebaikan", "Cause engagement: Menggunakan platform untuk advocasi", "Community building: Membangun audiens yang peduli", "Impactful entertainment: Konten yang menghibur dan bermakna"]	["Authenticity concern: Apakah purpose genuine atau marketing", "Mission vs profit: Ketegangan antara dampak dan revenue", "Audience complexity: Melayani komunitas dan pelanggan"]	["Integrated purpose: Misi adalah bisnis, bukan add-on", "Transparent communication: Jujur tentang motivasi dan tradeoff", "Stakeholder alignment: Memastikan semua pihak share values"]	["Social enterprise kreatif: Bisnis seni dengan misi", "Cause marketing: Agency atau in-house untuk cause", "Impact entertainment: Produksi konten bermakna"]	["Story of purpose: Mengkomunikasikan why di balik apa", "Community dialogue: Listening dan responding ke audiens", "Partnership pitch: Menarik kolaborator yang share values"]	2025-12-23 06:15:22.472789+00	2025-12-23 06:15:22.472789+00
85	AIC	Artistic Investigative Conventional (AIC)	Kombinasi yang menggabungkan kreativitas, analisis, dan organisasi. Kamu adalah peneliti kreatif yang terstruktur. Ideal untuk design researcher, creative archivist, atau systematic curator.	["Structured creative research: Investigasi dengan metodologi untuk kreativitas", "Creative documentation: Catatan proses yang komprehensif dan estetis", "Knowledge curation: Mengorganisir informasi kreatif", "Systematic aesthetics: Desain yang didukung riset terstruktur"]	["Tension tiga dimensi: Rigor, kreativitas, dan struktur bersaing", "Perfection paralysis: Ingin sempurna di semua aspek", "Communication complexity: Berbicara ke audiens berbeda"]	["Project priorities: Dimensi mana paling penting untuk ini", "Good enough standards: Tidak semua perlu sempurna di setiap aspek", "Audience focus: Untuk siapa output ini"]	["Design research: Investigasi untuk keputusan desain", "Creative archive: Mengorganisir dan memelihara koleksi kreatif", "Knowledge management kreatif: Sistem untuk informasi desain"]	["Research presentation: Insight dalam format yang engaging", "Documentation sharing: Catatan yang bisa diakses dan dipahami", "Cross-functional communication: Berbicara dengan berbagai tim"]	2025-12-23 06:15:22.47609+00	2025-12-23 06:15:22.47609+00
86	AIE	Artistic Investigative Enterprising (AIE)	Kombinasi yang menggabungkan kreativitas, analisis, dan ambisi. Kamu adalah inovator kreatif yang ambisius dan berbasis riset. Ideal untuk creative strategist, innovation director, atau founder studio kreatif berbasis insight.	["Insight-driven creativity: Ide baru dari riset mendalam", "Strategic innovation: Kreativitas dengan visi bisnis", "Trend leadership: Menganalisis dan membentuk arah industri", "Creative ventures: Membangun bisnis berbasis inovasi kreatif"]	["Too many opportunities: Riset menunjukkan banyak kemungkinan", "Analysis vs action: Riset terus vs launch sekarang", "Art vs commerce: Kreativitas murni vs viability bisnis"]	["Validation gates: Checkpoint untuk go/no-go", "Informed bets: Riset cukup, lalu commit", "Portfolio approach: Beberapa proyek dengan risk profile berbeda"]	["Innovation lab: R&D kreatif dengan orientasi bisnis", "Creative venture: Startup berbasis kreativitas", "Strategic creative agency: Layanan berbasis insight"]	["Trend pitch: Insight tentang opportunity dengan visi kreatif", "Investor presentation: Peluang berbasis riset", "Thought leadership: Sharing perspektif untuk positioning"]	2025-12-23 06:15:22.478584+00	2025-12-23 06:15:22.478584+00
87	AIR	Artistic Investigative Realistic (AIR)	Kombinasi yang menggabungkan kreativitas, analisis, dan kemampuan praktis. Kamu adalah maker-researcher yang kreatif. Ideal untuk experimental artist, material researcher, atau creative technologist.	["Experimental making: Membangun untuk memahami dan menciptakan", "Material innovation: Meneliti dan menggunakan medium baru", "Research through creation: Investigasi melalui proses kreatif", "Technical artistry: Craft yang didukung pemahaman mendalam"]	["Scope creep: Terlalu banyak dimensi untuk dikejar", "Time allocation: Riset, buat, atau eksplorasi kreatif", "Communication challenge: Menjelaskan pekerjaan multidimensional"]	["Project definition: Fokus untuk setiap proyek", "Documentation practice: Catatan untuk learning dan sharing", "Collaboration: Partner untuk aspek yang bukan kekuatan"]	["Art-science lab: Eksplorasi di intersection", "Maker research: Investigasi melalui hands-on creation", "Material innovation: R&D untuk medium kreatif"]	["Process showcase: Menunjukkan perjalanan dari ide ke karya", "Technical-creative dialogue: Berbicara di dua dunia", "Exhibition as research: Karya sebagai temuan"]	2025-12-23 06:15:22.481249+00	2025-12-23 06:15:22.481249+00
88	AIS	Artistic Investigative Social (AIS)	Kombinasi yang menggabungkan kreativitas, analisis, dan kepedulian sosial. Kamu adalah peneliti kreatif untuk kebaikan manusia. Ideal untuk design anthropologist, participatory artist, atau community-based researcher kreatif.	["Empathic research: Memahami orang untuk kreativitas yang melayani", "Participatory creation: Seni bersama komunitas", "Knowledge sharing kreatif: Menyampaikan temuan secara engaging", "Human-centered innovation: Ide baru dari pemahaman mendalam tentang orang"]	["Role complexity: Researcher, kreator, dan helper", "Representation ethics: Bagaimana menampilkan orang yang diteliti", "Impact measurement: Apakah kreativitas benar-benar membantu"]	["Clear purpose: Untuk siapa dan untuk apa", "Ethical practice: Consent dan representation yang respectful", "Feedback loops: Mendengar dari yang dilayani"]	["Design research: Memahami pengguna melalui metode kreatif", "Community arts: Seni dengan dan untuk komunitas", "Social innovation: Solusi kreatif untuk masalah sosial"]	["Participatory process: Melibatkan orang dalam kreasi", "Story-based sharing: Temuan melalui narasi", "Community dialogue: Mendengar dan merespons"]	2025-12-23 06:15:22.485588+00	2025-12-23 06:15:22.485588+00
89	ARC	Artistic Realistic Conventional (ARC)	Kombinasi yang menggabungkan kreativitas, kemampuan praktis, dan organisasi. Kamu adalah maker yang terorganisir. Ideal untuk production manager kreatif, scenic fabricator, atau prop shop supervisor.	["Organized making: Proses produksi yang efisien dan berkualitas", "Technical creativity: Membangun dengan presisi dan keindahan", "Production systems: Workflow untuk output konsisten", "Quality craft: Standar tinggi dengan delivery yang reliable"]	["Creativity vs efficiency: Eksplorasi vs timeline", "Artistry vs production: Craft vs volume", "Control vs collaboration: Standar vs input tim"]	["Structured exploration: Waktu untuk experiment dalam jadwal", "Quality tiers: Standar berbeda untuk konteks berbeda", "Team standards: Komunikasi jelas tentang ekspektasi"]	["Production shop: Workshop dengan sistem produksi", "Scenic fabrication: Membangun untuk film, theater, event", "Manufacturing craft: Produksi skala dengan kualitas craft"]	["Production meetings: Koordinasi dengan berbagai pihak", "Technical specs: Dokumentasi yang jelas", "Quality feedback: Komunikasi konstruktif tentang standar"]	2025-12-23 06:15:22.489538+00	2025-12-23 06:15:22.489538+00
90	ARE	Artistic Realistic Enterprising (ARE)	Kombinasi yang menggabungkan kreativitas, kemampuan praktis, dan ambisi. Kamu adalah maker-entrepreneur. Ideal untuk studio owner, creative production company founder, atau design-build firm leader.	["Making and leading: Membangun dan mengelola bisnis", "Production entrepreneurship: Bisnis berbasis kemampuan buat", "Hands-on leadership: Memimpin dengan kredibilitas craft", "Scalable craft: Mengembangkan kemampuan produksi"]	["Doing vs growing: Hands-on vs building organization", "Quality vs scale: Craft vs volume", "Time allocation: Create, manage, atau develop business"]	["Core specialty: Fokus pada apa yang distinctive", "Team building: Orang yang bisa eksekusi standar kamu", "Business model clarity: Bagaimana menghasilkan sambil tetap true to craft"]	["Production studio: Workshop yang berkembang jadi bisnis", "Creative fabrication: Membangun untuk klien", "Design-build: Desain dan eksekusi bersama"]	["Capability showcase: Demonstrasi apa yang bisa dibuat", "Client development: Membangun hubungan untuk repeat business", "Team motivation: Memimpin craftspeople"]	2025-12-23 06:15:22.492851+00	2025-12-23 06:15:22.492851+00
91	ARI	Artistic Realistic Investigative (ARI)	Kombinasi yang menggabungkan kreativitas, kemampuan praktis, dan analisis. Kamu adalah maker yang meneliti. Ideal untuk material artist, experimental craftsperson, atau technical innovator kreatif.	["Research through making: Memahami melalui proses membangun", "Material experimentation: Menguji dan mengembangkan medium", "Technical-creative synthesis: Inovasi di intersection craft dan science", "Documented craft: Proses yang tercatat untuk learning"]	["Endless exploration: Selalu ada lebih untuk dipelajari dan dicoba", "Communication challenge: Menjelaskan pekerjaan multidimensional", "Commercial viability: Eksperimen vs apa yang bisa dijual"]	["Project constraints: Batasan yang productive", "Portfolio diversity: Proyek eksploratif dan komersial", "Documentation practice: Catatan untuk diri dan sharing"]	["Experimental studio: Ruang untuk eksplorasi material", "R&D craft: Pengembangan teknik dan material", "Technical arts: Seni yang memerlukan expertise teknis"]	["Process sharing: Menunjukkan eksperimen dan temuan", "Technical-creative dialogue: Berbicara di dua dunia", "Material stories: Narasi tentang medium"]	2025-12-23 06:15:22.496055+00	2025-12-23 06:15:22.496055+00
92	ARS	Artistic Realistic Social (ARS)	Kombinasi yang menggabungkan kreativitas, kemampuan praktis, dan kepedulian sosial. Kamu adalah maker yang membantu orang. Ideal untuk occupational therapist kreatif, community maker, atau adaptive technology designer.	["Making for people: Membangun untuk membantu", "Inclusive craft: Kreativitas yang accessible", "Therapeutic making: Proses kreatif sebagai healing", "Community building through craft: Membuat bersama"]	["Balance focus: Making, helping, atau creating", "Adaptation challenge: Menyesuaikan untuk berbagai kemampuan", "Resource constraints: Sering bekerja dengan keterbatasan"]	["Purpose clarity: Helping adalah tujuan, making adalah cara", "Adaptive mindset: Fleksibilitas untuk berbagai kebutuhan", "Community resources: Memanfaatkan apa yang ada"]	["Community workshop: Ruang untuk membuat bersama", "Adaptive technology: Menciptakan alat untuk kebutuhan khusus", "Art therapy practice: Menggunakan making untuk healing"]	["Warm instruction: Mengajar dengan sabar dan empati", "Celebratory feedback: Menghargai semua upaya", "Adaptive communication: Menyesuaikan untuk berbagai kemampuan"]	2025-12-23 06:15:22.5024+00	2025-12-23 06:15:22.5024+00
93	ASC	Artistic Social Conventional (ASC)	Kombinasi yang menggabungkan kreativitas, kepedulian sosial, dan organisasi. Kamu adalah kreator yang membantu dalam kerangka terstruktur. Ideal untuk art therapist dengan pendekatan sistematis, museum program manager, atau arts education administrator.	["Structured helping through arts: Program kreatif yang terorganisir", "Therapeutic creativity: Seni untuk kesehatan dalam protokol", "Arts program management: Mengelola inisiatif kreatif untuk komunitas", "Documented care: Catatan yang mendukung layanan berkelanjutan"]	["Bureaucracy vs spontaneity: Administrasi bisa meredam kreativitas", "Protocol vs personal: Struktur vs kebutuhan individual", "Paperwork burden: Dokumentasi mengambil waktu dari layanan"]	["Purposeful structure: Sistem melayani layanan, bukan sebaliknya", "Flexible protocols: Panduan dengan ruang untuk adaptasi", "Efficient documentation: Template yang streamlined"]	["Art therapy: Praktek dengan pendekatan terstruktur", "Arts education: Mengelola program pendidikan seni", "Museum programs: Mengkoordinasikan outreach dan edukasi"]	["Professional warmth: Caring dalam konteks formal", "Program communication: Mengkomunikasikan peluang partisipasi", "Progress documentation: Catatan yang mendukung kontinuitas"]	2025-12-23 06:15:22.508031+00	2025-12-23 06:15:22.508031+00
94	ASE	Artistic Social Enterprising (ASE)	Kombinasi yang menggabungkan kreativitas, kepedulian sosial, dan ambisi. Kamu adalah kreator yang membangun untuk dampak sosial. Ideal untuk social enterprise arts, community arts leader, atau cause-driven creative entrepreneur.	["Arts for impact: Menggunakan kreativitas untuk perubahan", "Community mobilization: Membangun gerakan melalui seni", "Sustainable arts: Membangun model bisnis untuk praktek sosial", "Platform building: Menciptakan ruang untuk suara lain"]	["Mission vs sustainability: Dampak vs keberlanjutan organisasi", "Representation: Siapa yang berbicara untuk siapa", "Scale vs depth: Menjangkau banyak vs dampak mendalam"]	["Sustainable mission: Organisasi sehat bisa serve lebih lama", "Amplification: Platform untuk suara komunitas, bukan substitusi", "Theory of change: Framework untuk dampak yang jelas"]	["Community arts organization: Memimpin praktek seni komunitas", "Social enterprise arts: Bisnis seni dengan misi", "Creative advocacy: Menggunakan platform untuk cause"]	["Story of change: Mengkomunikasikan dampak", "Community voice: Amplifying cerita dari komunitas", "Funder engagement: Menarik dukungan untuk misi"]	2025-12-23 06:15:22.512764+00	2025-12-23 06:15:22.512764+00
95	ASI	Artistic Social Investigative (ASI)	Kombinasi yang menggabungkan kreativitas, kepedulian sosial, dan analisis. Kamu adalah peneliti kreatif yang peduli pada orang. Ideal untuk design researcher empatis, arts-based researcher, atau social practice artist.	["Empathic inquiry: Riset yang sensitive dan kreatif", "Arts-based research: Menggunakan kreativitas sebagai metode", "Human-centered creativity: Seni yang berakar pada pemahaman orang", "Knowledge translation: Menyampaikan temuan secara engaging"]	["Method complexity: Rigor, kreativitas, dan sensitivitas bersama", "Representation ethics: Bagaimana menampilkan yang diteliti", "Impact ambiguity: Sulit mengukur dampak kerja kreatif-sosial"]	["Reflexive practice: Kesadaran akan posisi dan pengaruh", "Ethical creativity: Inovasi yang menghormati partisipan", "Multi-output: Berbagai format untuk berbagai audiens"]	["Design research: Memahami orang untuk kreativitas yang melayani", "Arts-based research: Seni sebagai metode riset", "Social practice art: Seni sebagai intervensi sosial"]	["Participatory process: Melibatkan orang dalam riset dan kreasi", "Visual storytelling: Menyampaikan temuan melalui seni", "Sensitive communication: Menghormati cerita orang"]	2025-12-23 06:15:22.518529+00	2025-12-23 06:15:22.518529+00
96	ASR	Artistic Social Realistic (ASR)	Kombinasi yang menggabungkan kreativitas, kepedulian sosial, dan kemampuan praktis. Kamu adalah maker yang membantu. Ideal untuk community builder, maker educator, atau hands-on arts facilitator.	["Making together: Memfasilitasi kreativitas komunitas", "Practical arts: Seni yang accessible dan hands-on", "Teaching through doing: Berbagi keterampilan secara langsung", "Resourceful creativity: Berkreasi dengan apa yang ada"]	["Balance attention: Making, teaching, atau facilitating", "Skill range: Melayani berbagai level kemampuan", "Resource constraints: Sering bekerja dengan keterbatasan"]	["Flexible facilitation: Adaptasi untuk berbagai kebutuhan", "Scaffolded learning: Struktur untuk berbagai level", "Community resources: Memanfaatkan kekuatan komunitas"]	["Maker space: Ruang untuk learning dan creating bersama", "Community workshop: Program hands-on untuk publik", "Arts education: Mengajar keterampilan kreatif"]	["Warm instruction: Mengajar dengan sabar", "Demo-based learning: Menunjukkan lalu memfasilitasi", "Celebratory feedback: Menghargai semua upaya"]	2025-12-23 06:15:22.524242+00	2025-12-23 06:15:22.524242+00
97	SAC	Social Artistic Conventional (SAC)	Kombinasi yang menggabungkan kepedulian sosial, kreativitas, dan organisasi. Kamu adalah helper kreatif yang terstruktur. Ideal untuk program coordinator seni komunitas, arts therapist administrator, atau event planner untuk nonprofit.	["Organized creative helping: Program kreatif yang well-managed", "Therapeutic arts administration: Mengelola layanan healing kreatif", "Community programming: Event dan program yang engaging dan terorganisir", "Documentation for continuity: Catatan yang membantu layanan berlanjut"]	["Bureaucracy vs spontaneity: Admin bisa meredam kreativitas dan caring", "Multiple hats: Helper, kreator, dan organizer", "Energy management: Tiga dimensi yang demanding"]	["Purpose first: Admin melayani helping dan kreativitas", "Sustainable pace: Tidak harus sempurna di semua dimensi", "Support systems: Orang atau tools yang membantu"]	["Arts nonprofit: Mengelola program kreatif untuk komunitas", "Community center: Koordinasi program engaging", "Healthcare arts: Administrasi program seni untuk kesehatan"]	["Warm professionalism: Caring dalam konteks terstruktur", "Program promotion: Mengkomunikasikan peluang", "Feedback integration: Mendengar dan merespons peserta"]	2025-12-23 06:15:22.527919+00	2025-12-23 06:15:22.527919+00
98	SAE	Social Artistic Enterprising (SAE)	Kombinasi yang menggabungkan kepedulian sosial, kreativitas, dan ambisi. Kamu adalah helper kreatif yang membangun. Ideal untuk social enterprise founder kreatif, community arts leader, atau entertainment dengan misi sosial.	["Creative social enterprise: Bisnis seni untuk kebaikan", "Platform building: Menciptakan ruang untuk suara komunitas", "Impactful entertainment: Konten yang menghibur dan bermakna", "Movement building: Menggerakkan orang melalui kreativitas"]	["Mission vs margin: Dampak vs keberlanjutan", "Authenticity concerns: Apakah genuinely helping atau exploiting", "Scale vs connection: Menjangkau banyak vs dampak personal"]	["Sustainable impact: Model bisnis yang support misi jangka panjang", "Transparent purpose: Jujur tentang motivasi dan tradeoff", "Community partnership: Bersama, bukan untuk"]	["Social arts venture: Bisnis kreatif dengan misi", "Community media: Platform untuk suara komunitas", "Cause entertainment: Produksi konten bermakna"]	["Story of impact: Mengkomunikasikan perubahan yang terjadi", "Community voice: Amplifying, bukan speaking for", "Partner engagement: Menarik kolaborator yang share values"]	2025-12-23 06:15:22.531831+00	2025-12-23 06:15:22.531831+00
99	SAI	Social Artistic Investigative (SAI)	Kombinasi yang menggabungkan kepedulian sosial, kreativitas, dan analisis. Kamu adalah helper kreatif yang berbasis riset. Ideal untuk design researcher empatis, arts therapy researcher, atau human-centered design lead.	["Empathic inquiry: Memahami orang melalui riset kreatif", "Evidence-based arts: Praktek kreatif yang didukung riset", "Knowledge translation: Menyampaikan temuan secara engaging", "Human insight: Memahami kebutuhan untuk solusi yang tepat"]	["Method tension: Rigor, kreativitas, dan sensitivity bersama", "Analysis vs action: Riset vs membantu langsung", "Communication complexity: Berbagai audiens, berbagai bahasa"]	["Purpose-driven research: Investigasi untuk membantu, bukan sebaliknya", "Rapid iteration: Test dan improve cepat", "Multiple outputs: Format berbeda untuk audiens berbeda"]	["Design research: Memahami pengguna dengan empati", "Arts therapy research: Riset efektivitas intervensi kreatif", "Social innovation: Solusi berbasis insight tentang orang"]	["Participatory research: Melibatkan orang dalam proses", "Visual communication: Menyampaikan dengan gambar dan cerita", "Empathic listening: Memahami sebelum berbicara"]	2025-12-23 06:15:22.537049+00	2025-12-23 06:15:22.537049+00
100	SAR	Social Artistic Realistic (SAR)	Kombinasi yang menggabungkan kepedulian sosial, kreativitas, dan kemampuan praktis. Kamu adalah helper kreatif yang hands-on. Ideal untuk art therapist, maker educator, atau community workshop facilitator.	["Therapeutic making: Menggunakan kreasi untuk healing", "Hands-on helping: Bantuan yang konkret dan kreatif", "Inclusive craft: Seni yang accessible untuk semua kemampuan", "Community making: Membangun bersama"]	["Balance attention: Helping, creating, atau making", "Adaptation: Menyesuaikan untuk berbagai kebutuhan dan kemampuan", "Energy management: Giving di multiple dimensions"]	["Purpose clarity: Helping adalah tujuan, making adalah cara", "Adaptive practice: Fleksibilitas untuk berbagai situasi", "Self-care: Mengisi ulang untuk terus memberi"]	["Art therapy: Menggunakan kreasi untuk kesembuhan", "Community workshop: Program making untuk publik", "Occupational therapy: Rehabilitasi melalui aktivitas"]	["Warm facilitation: Memandu dengan empati", "Process celebration: Menghargai perjalanan, bukan hanya hasil", "Adaptive instruction: Menyesuaikan untuk berbagai kemampuan"]	2025-12-23 06:15:22.54383+00	2025-12-23 06:15:22.54383+00
101	SCA	Social Conventional Artistic (SCA)	Kombinasi yang menggabungkan kepedulian sosial, organisasi, dan kreativitas. Kamu adalah helper terstruktur dengan sentuhan kreatif. Ideal untuk program manager nonprofit kreatif, event coordinator dengan flair, atau administrator pendidikan seni.	["Organized helping with creativity: Layanan terstruktur yang engaging", "Program design: Menciptakan pengalaman yang bermakna dan terkelola", "Administrative creativity: Membuat sistem yang user-friendly", "Community engagement: Outreach yang menarik dan organized"]	["Structure vs spontaneity: Sistem bisa membatasi kreativitas", "Paperwork vs people: Admin vs waktu dengan yang dilayani", "Multiple responsibilities: Organizing, helping, dan creating"]	["Creative systems: Struktur yang memfasilitasi, bukan membatasi", "Efficiency for connection: Admin yang streamlined untuk lebih banyak waktu helping", "Energy management: Tidak harus excel di semua setiap saat"]	["Nonprofit administration: Mengelola organisasi yang serving", "Community program: Koordinasi layanan dengan flair", "Arts education admin: Mengelola program pendidikan kreatif"]	["Organized warmth: Caring dalam konteks formal", "Creative communication: Materi yang menarik dan jelas", "Participant-centered systems: Proses yang mudah bagi yang dilayani"]	2025-12-23 06:15:22.548291+00	2025-12-23 06:15:22.548291+00
102	SCE	Social Conventional Enterprising (SCE)	Kombinasi yang menggabungkan kepedulian sosial, organisasi, dan ambisi. Kamu adalah helper terstruktur yang membangun. Ideal untuk nonprofit executive, healthcare administrator, atau social service director.	["Organizational helping: Memimpin organisasi yang melayani", "Scaled impact: Memperbesar jangkauan layanan", "Efficient caring: Sistem yang memaksimalkan dampak", "Sustainable service: Model yang berkelanjutan"]	["Mission vs margin: Dampak vs keberlanjutan finansial", "Bureaucracy growth: Organisasi besar bisa kehilangan soul", "Personal connection: Sulit maintain hubungan langsung saat scale"]	["Mission-driven efficiency: Sistem untuk dampak, bukan birokrasi", "Culture stewardship: Menjaga values saat organisasi tumbuh", "Delegation with purpose: Memberdayakan orang untuk serve"]	["Nonprofit leadership: Executive atau director", "Healthcare management: Memimpin sistem kesehatan", "Social service: Mengelola program layanan sosial"]	["Vision communication: Menginspirasi tentang dampak", "Board engagement: Bekerja dengan governance", "Staff development: Membangun tim yang caring dan capable"]	2025-12-23 06:15:22.551947+00	2025-12-23 06:15:22.551947+00
103	SCI	Social Conventional Investigative (SCI)	Kombinasi yang menggabungkan kepedulian sosial, organisasi, dan analisis. Kamu adalah helper terstruktur yang berbasis bukti. Ideal untuk program evaluator, social work researcher, atau healthcare quality analyst.	["Evidence-based service: Layanan yang didukung riset", "Program evaluation: Mengukur dan meningkatkan dampak", "Quality improvement: Analisis untuk layanan lebih baik", "Data-informed caring: Keputusan didukung bukti"]	["Data vs relationship: Metrik vs koneksi manusia", "Analysis vs action: Riset vs membantu langsung", "Bureaucracy of measurement: Tracking bisa menjadi beban"]	["Purpose-driven data: Mengukur apa yang matters", "Efficient tracking: System yang tidak membebani", "Balance: Data sebagai input, bukan master"]	["Program evaluation: Menilai efektivitas layanan", "Healthcare quality: Analisis untuk perbaikan sistem", "Social research: Riset untuk kebijakan dan praktek"]	["Accessible reporting: Temuan yang bisa diactionable", "Collaborative analysis: Melibatkan practitioners dalam interpretasi", "Improvement focus: Data untuk getting better, bukan judging"]	2025-12-23 06:15:22.556986+00	2025-12-23 06:15:22.556986+00
104	SCR	Social Conventional Realistic (SCR)	Kombinasi yang menggabungkan kepedulian sosial, organisasi, dan kemampuan praktis. Kamu adalah helper terstruktur yang hands-on. Ideal untuk case manager, healthcare coordinator, atau facility manager untuk human services.	["Organized practical help: Bantuan konkret yang terkoordinasi", "Service coordination: Mengelola layanan untuk banyak klien", "Facility management: Memelihara lingkungan untuk yang dilayani", "Reliable support: Bantuan yang konsisten dan terpercaya"]	["Protocol vs need: Aturan tidak selalu fit situasi", "Paperwork burden: Dokumentasi mengambil waktu dari helping", "Hands-on vs managing: Doing vs coordinating"]	["Efficient documentation: Fokus pada yang truly necessary", "Advocacy within system: Bekerja untuk memperbaiki aturan yang tidak serve", "Balance hands-on: Tetap connected meski managing"]	["Case management: Koordinasi layanan untuk klien", "Healthcare coordination: Mengatur perawatan pasien", "Human services facility: Memelihara dan mengelola tempat layanan"]	["Clear guidance: Instruksi yang mudah diikuti", "Reliable follow-up: Memastikan layanan tersampaikan", "Practical empathy: Caring yang konkret dan helpful"]	2025-12-23 06:15:22.560954+00	2025-12-23 06:15:22.560954+00
105	SEA	Social Enterprising Artistic (SEA)	Kombinasi yang menggabungkan kepedulian sosial, ambisi, dan kreativitas. Kamu adalah pemimpin yang menggunakan kreativitas untuk dampak. Ideal untuk cause marketing leader, social impact creative director, atau community organizer kreatif.	["Creative campaigning: Menggunakan seni untuk gerakan", "Movement aesthetics: Visual identity untuk cause", "Platform leadership: Membangun voice untuk komunitas", "Engaging advocacy: Advokasi yang menarik dan inspiring"]	["Authenticity concern: Marketing vs genuine caring", "Art vs message: Kreativitas murni vs komunikasi cause", "Representation: Siapa berbicara untuk siapa"]	["Transparent purpose: Jujur tentang motivasi", "Community partnership: Platform bersama, bukan untuk", "Art in service: Kreativitas sebagai alat, bukan tujuan"]	["Cause marketing: Komunikasi untuk impact", "Social campaign: Menggerakkan perubahan melalui kreativitas", "Community organizing: Membangun gerakan dengan flair"]	["Visual storytelling: Mengkomunikasikan dengan gambar dan narasi", "Movement building: Menginspirasi aksi", "Community voice: Amplifying, bukan replacing"]	2025-12-23 06:15:22.564219+00	2025-12-23 06:15:22.564219+00
106	SEC	Social Enterprising Conventional (SEC)	Kombinasi yang menggabungkan kepedulian sosial, ambisi, dan organisasi. Kamu adalah pemimpin yang membangun organisasi untuk kebaikan. Ideal untuk nonprofit CEO, social enterprise founder, atau healthcare system executive.	["Organizational impact: Memimpin untuk skala dan sustainability", "Efficient mission: Sistem yang memaksimalkan dampak per resource", "Governance: Membangun struktur yang accountable", "Sustainable growth: Ekspansi yang tidak mengorbankan mission"]	["Mission drift: Pertumbuhan bisa menggeser focus", "Bureaucratization: Organisasi besar bisa kehilangan soul", "Personal disconnection: Jauh dari yang dilayani saat scaling"]	["Mission metrics: Mengukur apa yang truly matters", "Culture intentionality: Menjaga values di setiap level", "Stay connected: Regular contact dengan frontline dan yang dilayani"]	["Nonprofit leadership: CEO atau executive director", "Social enterprise: Memimpin bisnis dengan misi", "Healthcare executive: Mengelola sistem untuk kesehatan"]	["Board communication: Bekerja dengan governance", "Staff inspiration: Memotivasi tentang mission", "Stakeholder management: Balancing berbagai kepentingan"]	2025-12-23 06:15:22.570031+00	2025-12-23 06:15:22.570031+00
107	SEI	Social Enterprising Investigative (SEI)	Kombinasi yang menggabungkan kepedulian sosial, ambisi, dan analisis. Kamu adalah pemimpin yang menggunakan riset untuk dampak. Ideal untuk policy entrepreneur, impact investor, atau evidence-based program director.	["Evidence-based scaling: Memperbesar apa yang terbukti bekerja", "Strategic philanthropy: Investasi sosial berbasis riset", "Policy influence: Menggunakan data untuk perubahan sistemik", "Impact measurement: Mengukur dan mengoptimalkan dampak"]	["Analysis vs action: Riset vs implementing sekarang", "Data limitations: Tidak semua dampak mudah diukur", "Scale vs adaptation: Fidelity vs local fit"]	["Good enough evidence: Kapan data cukup untuk bergerak", "Mixed methods: Capturing apa yang tidak dikuantifikasi", "Adaptive implementation: Flexibilitas dalam fidelity"]	["Impact investing: Investasi untuk return dan dampak", "Policy research: Riset untuk perubahan kebijakan", "Program leadership: Mengarahkan dengan evidence"]	["Impact pitch: Data dan cerita untuk memotivasi aksi", "Policy briefing: Bukti untuk pembuat keputusan", "Board reporting: Dampak dalam metrik dan narasi"]	2025-12-23 06:15:22.576216+00	2025-12-23 06:15:22.576216+00
108	SER	Social Enterprising Realistic (SER)	Kombinasi yang menggabungkan kepedulian sosial, ambisi, dan kemampuan praktis. Kamu adalah pemimpin yang membangun dan melayani. Ideal untuk social entrepreneur hands-on, community development leader, atau training business founder.	["Building for good: Konstruksi atau produksi untuk dampak sosial", "Skills training: Mengembangkan kemampuan yang marketable", "Community development: Membangun infrastruktur untuk komunitas", "Practical enterprise: Bisnis yang membantu secara konkret"]	["Doing vs leading: Preference hands-on vs managing growth", "Mission vs efficiency: Helping semua vs focusing for impact", "Scale challenges: Keeping quality saat growing"]	["Strategic hands-on: Kapan terlibat langsung vs delegate", "Focus for impact: Serving some well vs many poorly", "Quality systems: Standar yang mempertahankan values saat scale"]	["Social enterprise: Bisnis dengan misi yang hands-on", "Workforce development: Training dan employment", "Community development: Building capacity"]	["Lead by doing: Showing commitment melalui involvement", "Practical vision: Menjelaskan dampak yang konkret", "Team development: Building skills and motivation"]	2025-12-23 06:15:22.580973+00	2025-12-23 06:15:22.580973+00
109	SIA	Social Investigative Artistic (SIA)	Kombinasi yang menggabungkan kepedulian sosial, analisis, dan kreativitas. Kamu adalah peneliti kreatif yang peduli. Ideal untuk design anthropologist, participatory researcher, atau community-based creative researcher.	["Empathic research: Investigasi yang sensitive dan kreatif", "Participatory methods: Riset bersama komunitas", "Creative knowledge sharing: Menyampaikan temuan dengan engaging", "Human-centered insight: Memahami orang untuk solusi yang tepat"]	["Method complexity: Rigor, kreativitas, dan sensitivitas", "Representation ethics: Bagaimana menampilkan yang diteliti", "Academic vs accessible: Rigor vs readability"]	["Reflexivity: Kesadaran akan posisi dan pengaruh", "Multiple outputs: Format berbeda untuk audiens berbeda", "Community validation: Checking interpretation dengan yang diteliti"]	["Design research: Memahami orang untuk design", "Participatory research: Investigasi bersama komunitas", "Arts-based inquiry: Kreativitas sebagai metode riset"]	["Visual communication: Menyampaikan dengan gambar dan cerita", "Community dialogue: Listening dan sharing back", "Ethical storytelling: Menghormati cerita orang"]	2025-12-23 06:15:22.58716+00	2025-12-23 06:15:22.58716+00
110	SIC	Social Investigative Conventional (SIC)	Kombinasi yang menggabungkan kepedulian sosial, analisis, dan organisasi. Kamu adalah analis yang caring dan terstruktur. Ideal untuk program evaluator, policy analyst untuk social issues, atau institutional researcher.	["Systematic caring: Riset terstruktur untuk layanan lebih baik", "Program evaluation: Mengukur dan meningkatkan dampak", "Policy analysis: Investigasi untuk keputusan yang mempengaruhi orang", "Quality assurance: Memastikan standar layanan terpenuhi"]	["Data vs connection: Metrik vs relationship", "Bureaucracy of measurement: Tracking bisa membebani service", "Academic vs practical: Rigor vs actionability"]	["Purpose-driven metrics: Measuring what truly matters", "Efficient evaluation: System yang tidak membebani", "Actionable output: Temuan yang bisa diimplementasikan"]	["Program evaluation: Menilai efektivitas layanan", "Policy research: Analisis untuk keputusan kebijakan", "Quality improvement: Riset untuk perbaikan layanan"]	["Accessible reporting: Temuan untuk non-researchers", "Collaborative analysis: Melibatkan stakeholder dalam interpretasi", "Improvement focus: Data untuk getting better"]	2025-12-23 06:15:22.591021+00	2025-12-23 06:15:22.591021+00
111	SIE	Social Investigative Enterprising (SIE)	Kombinasi yang menggabungkan kepedulian sosial, analisis, dan ambisi. Kamu adalah pemimpin riset untuk dampak. Ideal untuk research institute director, policy entrepreneur, atau evidence-based nonprofit leader.	["Research for impact: Investigasi untuk perubahan besar", "Strategic evidence: Menggunakan data untuk keputusan strategis", "Scaled solutions: Memperbesar intervensi yang terbukti", "Thought leadership: Mempengaruhi sektor melalui insight"]	["Analysis vs action: Riset vs implementing sekarang", "Academic vs popular: Rigor vs influence", "Scale vs nuance: Generalisasi vs context-specific"]	["Good enough evidence: Kapan cukup untuk bergerak", "Multiple audiences: Akademis dan populer", "Adaptive scaling: Fidelity dengan local adaptation"]	["Research institute: Memimpin organisasi riset", "Policy advocacy: Menggunakan evidence untuk perubahan", "Evidence-based nonprofit: Mengarahkan dengan riset"]	["Thought leadership: Sharing insight untuk mempengaruhi", "Policy briefing: Evidence untuk pembuat keputusan", "Strategic communication: Riset untuk berbagai audiens"]	2025-12-23 06:15:22.594251+00	2025-12-23 06:15:22.594251+00
112	SIR	Social Investigative Realistic (SIR)	Kombinasi yang menggabungkan kepedulian sosial, analisis, dan kemampuan praktis. Kamu adalah researcher-practitioner yang hands-on. Ideal untuk applied health researcher, occupational therapy researcher, atau implementation scientist.	["Practice-embedded research: Riset dalam konteks layanan", "Practical evidence: Investigasi untuk solusi yang implementable", "Implementation science: Memahami adopsi dan adaptation", "Applied insight: Temuan yang langsung applicable"]	["Research vs practice: Rigor vs membantu sekarang", "Time allocation: Investigating vs doing", "Adoption challenges: Temuan tidak selalu diimplementasikan"]	["Integrated practice: Research sebagai bagian dari service", "Rapid iteration: Test dan improve cepat", "Implementation focus: Memikirkan adopsi dari awal"]	["Applied research: Investigasi untuk praktik", "Implementation science: Riset tentang bagaimana menerapkan", "Practice-based evidence: Generating knowledge dari service"]	["Practical communication: Temuan yang actionable", "Collaborative research: Bekerja dengan practitioners", "Demonstration: Showing how evidence applies"]	2025-12-23 06:15:22.597483+00	2025-12-23 06:15:22.597483+00
113	SRA	Social Realistic Artistic (SRA)	Kombinasi yang menggabungkan kepedulian sosial, kemampuan praktis, dan kreativitas. Kamu adalah helper hands-on yang kreatif. Ideal untuk occupational therapist, community maker, atau therapeutic recreation specialist.	["Creative practical helping: Bantuan konkret dan ekspresif", "Therapeutic activities: Menggunakan making untuk healing", "Accessible creativity: Seni untuk semua kemampuan", "Community making: Membangun bersama"]	["Balance focus: Helping, making, atau creating", "Adaptation challenges: Menyesuaikan untuk berbagai kebutuhan", "Resource constraints: Sering bekerja dengan keterbatasan"]	["Purpose clarity: Helping adalah tujuan", "Adaptive practice: Fleksibilitas untuk berbagai situasi", "Resourcefulness: Kreativitas dengan apa yang ada"]	["Occupational therapy: Rehabilitasi melalui aktivitas", "Therapeutic recreation: Healing melalui leisure", "Community workshop: Making bersama untuk wellbeing"]	["Warm facilitation: Memandu dengan empati", "Process focus: Perjalanan sama pentingnya dengan hasil", "Celebratory feedback: Menghargai semua upaya"]	2025-12-23 06:15:22.600681+00	2025-12-23 06:15:22.600681+00
114	SRC	Social Realistic Conventional (SRC)	Kombinasi yang menggabungkan kepedulian sosial, kemampuan praktis, dan organisasi. Kamu adalah helper hands-on yang terstruktur. Ideal untuk vocational counselor, rehabilitation specialist, atau assisted living coordinator.	["Structured practical helping: Bantuan konkret yang terorganisir", "Skills training: Mengajar kemampuan praktis dengan kurikulum", "Service coordination: Mengelola layanan hands-on", "Rehabilitation support: Membantu recovery secara sistematis"]	["Protocol vs individual need: Struktur tidak selalu fit", "Paperwork vs hands-on: Admin vs direct service", "Efficiency vs thoroughness: Serving many vs helping well"]	["Adaptive protocols: Struktur dengan ruang untuk individualisasi", "Efficient documentation: Fokus pada yang necessary", "Quality over quantity: Better to help fewer well"]	["Vocational rehabilitation: Membantu kembali bekerja", "Assisted living: Koordinasi perawatan praktis", "Skills training: Mengajar kemampuan untuk independence"]	["Clear instruction: Guidance yang mudah diikuti", "Patient teaching: Mengajar dengan empati", "Reliable follow-up: Memastikan progress berlanjut"]	2025-12-23 06:15:22.604218+00	2025-12-23 06:15:22.604218+00
115	SRE	Social Realistic Enterprising (SRE)	Kombinasi yang menggabungkan kepedulian sosial, kemampuan praktis, dan ambisi. Kamu adalah pemimpin yang membangun untuk membantu. Ideal untuk workforce development director, social contractor, atau training business leader.	["Building opportunity: Menciptakan pekerjaan dan skills", "Training enterprise: Bisnis yang mengembangkan orang", "Community development: Membangun infrastruktur untuk opportunity", "Scalable helping: Memperbesar dampak praktis"]	["Mission vs margin: Dampak vs keberlanjutan", "Quality vs quantity: Helping well vs reaching many", "Hands-on vs leading: Doing vs managing growth"]	["Sustainable mission: Model bisnis yang support dampak", "Quality standards: Tidak mengorbankan quality untuk scale", "Strategic involvement: Kapan hands-on vs delegate"]	["Workforce development: Training dan employment", "Social enterprise: Bisnis yang mempekerjakan atau melatih", "Community building: Infrastruktur untuk opportunity"]	["Practical vision: Dampak yang konkret dan tangible", "Team building: Developing skills dan motivation", "Partnership development: Building network untuk opportunity"]	2025-12-23 06:15:22.607765+00	2025-12-23 06:15:22.607765+00
116	SRI	Social Realistic Investigative (SRI)	Kombinasi yang menggabungkan kepedulian sosial, kemampuan praktis, dan analisis. Kamu adalah helper hands-on yang berbasis bukti. Ideal untuk physical therapist, ergonomist, atau applied health practitioner.	["Evidence-based practice: Intervensi yang didukung riset", "Practical assessment: Evaluasi untuk solusi konkret", "Applied research: Investigating untuk membantu lebih baik", "Measurable helping: Tracking progress secara objektif"]	["Research vs practice: Rigor vs membantu sekarang", "Measurement vs relationship: Data vs connection", "Protocol vs individual: Standard vs personalized care"]	["Integrated evidence: Research sebagai bagian dari practice", "Meaningful metrics: Mengukur apa yang matters untuk klien", "Adaptive protocols: Evidence-based dengan individualization"]	["Physical therapy: Rehabilitasi berbasis bukti", "Ergonomics: Analisis untuk workplace health", "Applied health: Praktik yang grounded dalam riset"]	["Clinical communication: Explaining dengan empati dan clarity", "Progress sharing: Showing improvement dengan data", "Collaborative goal-setting: Bersama menentukan target"]	2025-12-23 06:15:22.610826+00	2025-12-23 06:15:22.610826+00
117	EAC	Enterprising Artistic Conventional (EAC)	Kombinasi yang menggabungkan ambisi, kreativitas, dan organisasi. Kamu adalah pemimpin kreatif yang terstruktur. Ideal untuk creative agency CEO, entertainment producer, atau brand director.	["Creative business leadership: Memimpin organisasi kreatif dengan struktur", "Production management: Mengelola output kreatif yang konsisten", "Brand building: Membangun identitas dengan sistem", "Scalable creativity: Proses untuk kreativitas yang reproducible"]	["Art vs business: Kreativitas murni vs profitabilitas", "Control vs freedom: Struktur vs spontaneity", "Scale vs craft: Volume vs quality individual"]	["Creative frameworks: Sistem yang memfasilitasi, bukan membatasi", "Quality tiers: Different standards untuk different purposes", "Culture stewardship: Menjaga creative culture saat growing"]	["Creative agency: Memimpin bisnis kreatif", "Entertainment production: Managing content creation", "Brand management: Membangun dan memelihara brand"]	["Vision with structure: Inspiring dan organizing", "Client management: Balancing creative dan business needs", "Team leadership: Motivating creatives dalam struktur"]	2025-12-23 06:15:22.613453+00	2025-12-23 06:15:22.613453+00
118	EAI	Enterprising Artistic Investigative (EAI)	Kombinasi yang menggabungkan ambisi, kreativitas, dan analisis. Kamu adalah inovator strategis yang kreatif. Ideal untuk innovation director, venture creative, atau strategic creative director.	["Strategic innovation: Kreativitas dengan visi bisnis berbasis riset", "Trend leadership: Menganalisis dan membentuk arah industri", "Creative ventures: Investasi di ide kreatif viable", "Insight-driven creativity: Ide baru dari pemahaman pasar"]	["Analysis vs intuition: Data vs creative feeling", "Too many opportunities: Riset menunjukkan banyak kemungkinan", "Art vs commerce: Kreativitas murni vs viability"]	["Informed intuition: Riset sebagai input, bukan pengganti taste", "Focus discipline: Tidak semua peluang perlu dikejar", "Portfolio approach: Mix proyek dengan risk profile berbeda"]	["Innovation consulting: Helping organizations innovate creatively", "Creative ventures: Investing in creative startups", "Strategic creative: Agency atau in-house leadership"]	["Insight pitch: Opportunity berbasis riset dengan vision kreatif", "Trend briefing: Sharing perspective tentang arah industri", "Strategic dialogue: Diskusi tentang direction dan options"]	2025-12-23 06:15:22.616468+00	2025-12-23 06:15:22.616468+00
119	EAR	Enterprising Artistic Realistic (EAR)	Kombinasi yang menggabungkan ambisi, kreativitas, dan kemampuan praktis. Kamu adalah maker-entrepreneur. Ideal untuk product designer entrepreneur, creative studio founder, atau maker business owner.	["Making and building: Menciptakan dan mengelola bisnis", "Product vision: Dari ide ke produk marketable", "Hands-on leadership: Memimpin dengan kredibilitas craft", "Creative production: Building operation untuk output kreatif"]	["Doing vs growing: Hands-on vs building organization", "Quality vs scale: Craft vs volume", "Time allocation: Create, manage, atau develop business"]	["Leverage specialty: Fokus pada apa yang distinctive", "Build team: Hire untuk eksekusi dan operations", "Business model clarity: Bagaimana menghasilkan sambil true to craft"]	["Creative studio: Workshop yang berkembang jadi bisnis", "Product design: Creating dan launching products", "Maker business: Produksi dengan entrepreneurial drive"]	["Showcase capability: Demonstrating apa yang bisa dibuat", "Client development: Building relationships untuk business", "Team motivation: Leading craftspeople"]	2025-12-23 06:15:22.619457+00	2025-12-23 06:15:22.619457+00
120	EAS	Enterprising Artistic Social (EAS)	Kombinasi yang menggabungkan ambisi, kreativitas, dan kepedulian sosial. Kamu adalah pemimpin kreatif yang peduli. Ideal untuk social enterprise creative director, community arts leader, atau purpose-driven entertainment executive.	["Purpose-driven creativity: Seni dan bisnis untuk kebaikan", "Community engagement: Membangun audiens yang peduli", "Platform leadership: Menciptakan ruang untuk suara lain", "Impactful entertainment: Konten yang menghibur dan bermakna"]	["Authenticity concern: Marketing vs genuine caring", "Mission vs profit: Dampak vs revenue", "Representation: Siapa berbicara untuk siapa"]	["Integrated purpose: Misi adalah bisnis", "Transparent motivation: Jujur tentang why", "Community partnership: Bersama, bukan untuk"]	["Social creative enterprise: Bisnis seni dengan misi", "Community media: Platform untuk suara komunitas", "Purpose entertainment: Produksi konten bermakna"]	["Story of impact: Communicating change", "Community voice: Amplifying, bukan speaking for", "Partnership development: Building alliances dengan shared values"]	2025-12-23 06:15:22.623328+00	2025-12-23 06:15:22.623328+00
121	ECA	Enterprising Conventional Artistic (ECA)	Kombinasi yang menggabungkan ambisi, organisasi, dan kreativitas. Kamu adalah eksekutif dengan sentuhan kreatif. Ideal untuk brand CEO, marketing director, atau entertainment executive dengan operasional kuat.	["Creative operations: Mengelola bisnis kreatif dengan efisiensi", "Brand leadership: Membangun dan mempertahankan brand identity", "Systematic creativity: Proses untuk output kreatif konsisten", "Scalable aesthetic: Maintaining quality saat growing"]	["Efficiency vs artistry: Operations vs creative time", "Structure vs spontaneity: Process vs exploration", "Growth vs craft: Scale vs individual quality"]	["Creative operations: Sistem yang support creativity", "Quality standards: Metrics yang include aesthetics", "Culture preservation: Menjaga creative culture saat scaling"]	["Brand management: Memimpin brand organization", "Marketing leadership: Directing marketing dengan flair", "Creative operations: Managing creative production"]	["Operational creativity: Efficient dan menarik", "Brand communication: Consistent dan engaging", "Team direction: Balancing structure dan freedom"]	2025-12-23 06:15:22.626427+00	2025-12-23 06:15:22.626427+00
122	ECI	Enterprising Conventional Investigative (ECI)	Kombinasi yang menggabungkan ambisi, organisasi, dan analisis. Kamu adalah eksekutif yang sangat analitis. Ideal untuk management consulting partner, analytics executive, atau strategy director.	["Data-driven leadership: Keputusan berbasis evidence", "Operational strategy: Optimizing berdasarkan analysis", "Systematic growth: Expansion yang terukur", "Performance management: Metrik dan akuntabilitas yang jelas"]	["Analysis paralysis: Terlalu banyak riset sebelum action", "Over-systematization: Process bisa meredam agility", "Data tunnel vision: Mengabaikan yang tidak terukur"]	["Decision thresholds: Kapan data cukup", "Adaptive systems: Process yang bisa berubah", "Integrate qualitative: Kuantitatif bukan satu-satunya truth"]	["Management consulting: Strategy dan operations", "Corporate analytics: Memimpin fungsi data", "Strategy: Directing strategic planning"]	["Structured strategic dialogue: Discussions dengan framework", "Data-driven presentation: Recommendations dengan evidence", "Systematic communication: Regular reporting dengan metrics"]	2025-12-23 06:15:22.629488+00	2025-12-23 06:15:22.629488+00
123	ECR	Enterprising Conventional Realistic (ECR)	Kombinasi yang menggabungkan ambisi, organisasi, dan kemampuan praktis. Kamu adalah eksekutif operasional. Ideal untuk COO, plant director, atau operations executive.	["Operational excellence: Memimpin dengan fokus pada execution", "Scalable production: Memperbesar output dengan sistem", "Efficiency leadership: Optimizing resource utilization", "Reliable delivery: Consistent output yang bisa diandalkan"]	["Efficiency over innovation: Optimizing existing vs creating new", "Control focus: Detail management bisa mengorbankan big picture", "People vs process: System focus bisa mengabaikan human element"]	["Innovation allocation: Resources untuk improvement dan exploration", "Strategic perspective: Regular stepping back untuk big picture", "People investment: Developing team, bukan hanya managing process"]	["Manufacturing leadership: Directing production", "Operations executive: COO atau VP Operations", "Logistics: Managing supply chain"]	["Metrics communication: Talking in numbers dan targets", "Process updates: Regular reporting pada operational performance", "Direct leadership: Clear expectations dan accountability"]	2025-12-23 06:15:22.632439+00	2025-12-23 06:15:22.632439+00
124	ECS	Enterprising Conventional Social (ECS)	Kombinasi yang menggabungkan ambisi, organisasi, dan kepedulian sosial. Kamu adalah eksekutif yang caring. Ideal untuk HR executive, nonprofit COO, atau healthcare administrator.	["People-focused operations: Systems yang support human flourishing", "Organizational development: Building capable dan caring organizations", "Scalable care: Expanding reach sambil maintaining quality", "Efficient compassion: Maximizing impact per resource"]	["Efficiency vs individuality: Standard process vs personal needs", "Scale vs connection: Growing vs maintaining relationships", "Business vs mission: Sustainability vs unlimited giving"]	["Human-centered systems: Process yang designed around people", "Culture metrics: Measuring what matters untuk wellbeing", "Sustainable caring: Boundaries yang enable long-term service"]	["HR leadership: Chief People Officer atau HR Director", "Nonprofit operations: Managing social organization", "Healthcare administration: Leading health systems"]	["Caring leadership: Warmth dengan professionalism", "Organizational communication: Keeping everyone informed", "Performance conversations: Accountability dengan empathy"]	2025-12-23 06:15:22.636385+00	2025-12-23 06:15:22.636385+00
125	EIA	Enterprising Investigative Artistic (EIA)	Kombinasi yang menggabungkan ambisi, analisis, dan kreativitas. Kamu adalah strategist yang kreatif. Ideal untuk innovation executive, creative strategy director, atau venture builder.	["Strategic creativity: Innovation berbasis insight", "Trend intelligence: Understanding market untuk creative opportunity", "Venture building: Creating new businesses dari ideas", "Creative strategy: Direction yang both analytical dan imaginative"]	["Too many possibilities: Analysis dan creativity both generate options", "Rigor vs intuition: Data vs creative instinct", "Execution gap: Ideas abundant, implementation challenging"]	["Prioritization discipline: Not pursuing everything", "Informed intuition: Data sebagai input, bukan master", "Execution partnership: Team yang bisa implement"]	["Innovation leadership: Directing new ventures", "Creative strategy: Agency atau corporate", "Venture building: Creating new businesses"]	["Strategic creative pitch: Vision dengan evidence", "Trend communication: Sharing insight tentang opportunity", "Team inspiration: Motivating dengan ideas dan analysis"]	2025-12-23 06:15:22.641532+00	2025-12-23 06:15:22.641532+00
126	EIC	Enterprising Investigative Conventional (EIC)	Kombinasi yang menggabungkan ambisi, analisis, dan organisasi. Kamu adalah eksekutif yang sangat sistematis dan analitis. Ideal untuk strategy consulting partner, analytics firm leader, atau corporate strategy executive.	["Systematic strategy: Direction berbasis rigorous analysis", "Data governance: Building organizational data capability", "Analytical leadership: Leading dengan evidence dan structure", "Optimized operations: Continuous improvement berbasis data"]	["Over-analysis: Studying vs doing", "Rigid systematization: Process over agility", "Quantification bias: Valuing only what can be measured"]	["Decision protocols: Clear criteria for when to act", "Adaptive frameworks: Systems yang evolve", "Qualitative integration: Including what cannot be quantified"]	["Strategy consulting: Senior partner atau leadership", "Corporate strategy: Chief Strategy Officer", "Analytics leadership: Chief Data atau Analytics Officer"]	["Framework communication: Structured strategic dialogue", "Evidence-based recommendations: Data-supported direction", "Systematic reporting: Regular performance updates"]	2025-12-23 06:15:22.645935+00	2025-12-23 06:15:22.645935+00
127	EIR	Enterprising Investigative Realistic (EIR)	Kombinasi yang menggabungkan ambisi, analisis, dan kemampuan praktis. Kamu adalah teknolog-eksekutif. Ideal untuk CTO, technical founder, atau R&D director.	["Technical leadership: Directing dengan understanding mendalam", "Innovation commercialization: Bringing research ke market", "Applied R&D: Research dengan business orientation", "Technical strategy: Technology direction berbasis analysis"]	["Doing vs directing: Hands-on vs managing", "Research vs business: Pure investigation vs commercial application", "Technical optimism: Underestimating implementation challenges"]	["Strategic hands-on: Selective involvement in technical work", "Commercial milestones: Checkpoints untuk market relevance", "Team building: Hiring untuk execution capability"]	["Technical leadership: CTO atau VP Engineering", "R&D direction: Leading research dengan business focus", "Tech entrepreneurship: Technical founder"]	["Technical strategy communication: Vision dengan credibility", "Board technical updates: Explaining tech untuk non-technical", "Team technical leadership: Directing engineers"]	2025-12-23 06:15:22.649014+00	2025-12-23 06:15:22.649014+00
128	EIS	Enterprising Investigative Social (EIS)	Kombinasi yang menggabungkan ambisi, analisis, dan kepedulian sosial. Kamu adalah pemimpin yang menggunakan riset untuk dampak sosial. Ideal untuk impact investing director, policy entrepreneur, atau social research executive.	["Evidence-based impact: Scaling apa yang proven untuk work", "Strategic philanthropy: Investing sosial dengan rigor", "Policy influence: Using research untuk systemic change", "Impact leadership: Directing dengan insight dan ambition"]	["Analysis vs action: Research vs implementing now", "Scale vs depth: Reaching many vs helping deeply", "Data vs story: Metrics vs human narrative"]	["Good enough evidence: Knowing when to move", "Balanced communication: Data dan stories together", "Adaptive scaling: Fidelity dengan local customization"]	["Impact investing: Directing investments untuk return dan impact", "Policy leadership: Using evidence untuk systemic change", "Social research: Leading research untuk social benefit"]	["Impact pitch: Data dan narrative untuk inspiring action", "Policy briefing: Evidence untuk decision-makers", "Stakeholder communication: Speaking ke funders, beneficiaries, policymakers"]	2025-12-23 06:15:22.653102+00	2025-12-23 06:15:22.653102+00
129	ERA	Enterprising Realistic Artistic (ERA)	Kombinasi yang menggabungkan ambisi, kemampuan praktis, dan kreativitas. Kamu adalah builder-entrepreneur kreatif. Ideal untuk design-build firm owner, creative product founder, atau maker studio leader.	["Creative building: Making dan entrepreneurship together", "Product vision: From idea ke tangible product", "Hands-on leadership: Leading dengan craft credibility", "Making business: Business berbasis ability to create"]	["Doing vs growing: Hands-on preference vs scaling", "Artistry vs efficiency: Craft quality vs volume", "Role confusion: Creator, builder, atau business leader"]	["Core focus: What only you can do", "Team development: Hiring untuk complementary skills", "Business model: How to generate revenue staying true to making"]	["Design-build: Creating dan constructing", "Creative product: Making dan selling products", "Maker studio: Workshop dengan business orientation"]	["Demonstration: Showing capability", "Client development: Building relationships melalui quality", "Team leadership: Motivating makers dan builders"]	2025-12-23 06:15:22.656765+00	2025-12-23 06:15:22.656765+00
130	ERC	Enterprising Realistic Conventional (ERC)	Kombinasi yang menggabungkan ambisi, kemampuan praktis, dan organisasi. Kamu adalah eksekutif operasional yang hands-on. Ideal untuk manufacturing CEO, construction executive, atau logistics director.	["Operational leadership: Directing dengan understanding of work", "Efficient production: Optimizing output dengan systems", "Scalable operations: Growing dengan maintained quality", "Hands-on management: Credible leadership melalui knowledge"]	["Doing vs managing: Preference untuk involvement vs delegation", "Efficiency focus: Optimization bisa miss innovation", "Control orientation: Detail management vs empowerment"]	["Strategic involvement: Knowing when hands-on adds value", "Innovation allocation: Resources untuk improvement", "Team development: Building capability, bukan just managing"]	["Manufacturing executive: CEO atau COO of production", "Construction leadership: Executive in building industry", "Logistics direction: Managing distribution operations"]	["Operational metrics: Talking in efficiency dan output", "Direct communication: Clear expectations", "Floor presence: Visible dan involved leadership"]	2025-12-23 06:15:22.65965+00	2025-12-23 06:15:22.65965+00
131	ERI	Enterprising Realistic Investigative (ERI)	Kombinasi yang menggabungkan ambisi, kemampuan praktis, dan analisis. Kamu adalah teknolog-eksekutif yang hands-on. Ideal untuk technical startup CEO, engineering executive, atau applied research director.	["Technical commercialization: Bringing technical capability ke market", "Applied leadership: Directing with both analytical dan practical knowledge", "Innovation execution: From research ke product", "Credible technical direction: Leading dengan understanding"]	["Breadth challenge: Technical, analytical, dan business all demanding", "Delegation difficulty: Wanting involvement in everything", "Scale vs depth: Growing vs staying technically involved"]	["Focus discipline: Choosing where involvement adds most value", "Team building: Hiring untuk breadth of capability", "Role clarity: Knowing which hat wearing when"]	["Technical startup: CEO dengan technical background", "Engineering leadership: VP atau C-level in engineering", "Applied R&D: Directing research dengan commercial orientation"]	["Technical business communication: Speaking both languages", "Strategic technical updates: Direction dengan evidence", "Team technical leadership: Credible direction for engineers"]	2025-12-23 06:15:22.662396+00	2025-12-23 06:15:22.662396+00
132	ERS	Enterprising Realistic Social (ERS)	Kombinasi yang menggabungkan ambisi, kemampuan praktis, dan kepedulian sosial. Kamu adalah pemimpin yang membangun untuk orang. Ideal untuk social construction leader, workforce training executive, atau community development director.	["Building for community: Construction atau production untuk social benefit", "Skills development: Creating employment dan training opportunity", "Practical social enterprise: Business yang helps secara concrete", "Hands-on social leadership: Leading dengan doing"]	["Mission vs margin: Social impact vs business sustainability", "Hands-on vs scale: Involvement vs growing reach", "Quality vs quantity: Helping well vs helping many"]	["Sustainable model: Business yang supports continued impact", "Strategic involvement: Where hands-on most valuable", "Quality metrics: Standards untuk maintained impact"]	["Workforce development: Training dan employment organization", "Social construction: Building untuk community benefit", "Community development: Creating opportunity"]	["Practical vision: Concrete impact communication", "Team development: Building capability dan motivation", "Community partnership: Building with, tidak for"]	2025-12-23 06:15:22.66574+00	2025-12-23 06:15:22.66574+00
133	ESA	Enterprising Social Artistic (ESA)	Kombinasi yang menggabungkan ambisi, kepedulian sosial, dan kreativitas. Kamu adalah pemimpin yang menggunakan kreativitas untuk dampak. Ideal untuk creative social enterprise founder, cause marketing leader, atau community media executive.	["Creative social leadership: Using arts untuk social change", "Movement building: Inspiring action melalui creative expression", "Platform creation: Building voice untuk community", "Purpose-driven entertainment: Content yang entertains dan matters"]	["Authenticity concern: Marketing vs genuine caring", "Art vs message: Creative expression vs clear communication", "Scale vs connection: Reaching many vs deep engagement"]	["Transparent purpose: Being honest about motivations", "Community partnership: With, tidak for", "Integrated expression: Art serves purpose naturally"]	["Social creative enterprise: Business using arts untuk good", "Community media: Platform untuk community voice", "Cause creative: Using creativity untuk advocacy"]	["Story of impact: Communicating change through narrative", "Community amplification: Lifting community voices", "Partnership pitch: Building alliances dengan shared values"]	2025-12-23 06:15:22.668372+00	2025-12-23 06:15:22.668372+00
134	ESC	Enterprising Social Conventional (ESC)	Kombinasi yang menggabungkan ambisi, kepedulian sosial, dan organisasi. Kamu adalah eksekutif yang caring. Ideal untuk nonprofit CEO, social enterprise executive, atau human services director.	["Organizational social impact: Leading organization untuk good", "Efficient caring: Maximizing impact per resource", "Sustainable social enterprise: Business model yang supports mission", "Scalable service: Growing reach dengan maintained quality"]	["Mission drift: Growth bisa shift focus dari purpose", "Bureaucratization: Organization bisa lose soul saat growing", "Business vs mission: Sustainability vs unlimited giving"]	["Mission metrics: Measuring what truly matters", "Culture stewardship: Maintaining values at all levels", "Sustainable boundaries: Enabling long-term service"]	["Nonprofit leadership: CEO atau Executive Director", "Social enterprise: Leading purpose-driven business", "Human services: Directing social service organization"]	["Mission communication: Inspiring about purpose", "Stakeholder management: Balancing various interests", "Team motivation: Building caring dan capable team"]	2025-12-23 06:15:22.671679+00	2025-12-23 06:15:22.671679+00
135	ESI	Enterprising Social Investigative (ESI)	Kombinasi yang menggabungkan ambisi, kepedulian sosial, dan analisis. Kamu adalah pemimpin yang menggunakan riset untuk dampak. Ideal untuk evidence-based nonprofit director, impact measurement executive, atau policy organization leader.	["Evidence-based social leadership: Directing dengan research", "Impact optimization: Using data untuk maximize benefit", "Strategic advocacy: Using evidence untuk systemic change", "Scalable proven solutions: Growing apa yang works"]	["Analysis vs action: Research vs implementing now", "Metrics vs story: Data vs human narrative", "Scale vs adaptation: Fidelity vs local fit"]	["Good enough evidence: Knowing when to move", "Mixed methods: Quantitative dan qualitative", "Adaptive implementation: Evidence-based dengan flexibility"]	["Evidence-based nonprofit: Leading dengan research", "Impact measurement: Directing evaluation function", "Policy organization: Using evidence untuk advocacy"]	["Impact reporting: Data dan story together", "Evidence-based advocacy: Research untuk policy influence", "Stakeholder communication: Different messages untuk different audiences"]	2025-12-23 06:15:22.67468+00	2025-12-23 06:15:22.67468+00
136	ESR	Enterprising Social Realistic (ESR)	Kombinasi yang menggabungkan ambisi, kepedulian sosial, dan kemampuan praktis. Kamu adalah pemimpin yang membangun untuk membantu. Ideal untuk workforce development executive, social contractor, atau community building leader.	["Practical social enterprise: Building opportunity secara concrete", "Skills economy: Creating employment dan training", "Community development: Building infrastructure untuk opportunity", "Hands-on social leadership: Leading melalui doing"]	["Mission vs sustainability: Impact vs business viability", "Scale vs quality: Reaching many vs helping well", "Doing vs directing: Hands-on vs managing growth"]	["Sustainable model: Business yang supports impact long-term", "Quality standards: Not sacrificing quality untuk scale", "Strategic hands-on: Knowing when involvement adds value"]	["Workforce development: Employment dan training", "Social construction: Building untuk community", "Community development: Creating opportunity"]	["Practical vision: Tangible impact communication", "Partnership building: Creating network untuk opportunity", "Team development: Building skills dan motivation"]	2025-12-23 06:15:22.677326+00	2025-12-23 06:15:22.677326+00
137	CAE	Conventional Artistic Enterprising (CAE)	Kombinasi yang menggabungkan organisasi, kreativitas, dan ambisi. Kamu adalah manajer kreatif yang ambisius. Ideal untuk creative operations director, brand management executive, atau media production manager.	["Creative operations: Managing creative output dengan efficiency", "Brand stewardship: Maintaining identity dengan systems", "Production management: Delivering creative projects on time dan budget", "Scalable creativity: Building process untuk consistent output"]	["Structure vs spontaneity: Process bisa limit creative exploration", "Efficiency vs artistry: Speed vs quality", "Control vs freedom: Management vs creative autonomy"]	["Creative-friendly process: Systems that support rather than constrain", "Quality flexibility: Different standards untuk different purposes", "Team empowerment: Structure dengan autonomy"]	["Creative operations: Managing creative team dan output", "Brand management: Maintaining brand dengan process", "Media production: Delivering content projects"]	["Project communication: Status dengan creative sensitivity", "Team management: Balancing structure dan freedom", "Client liaison: Managing expectations dengan creative understanding"]	2025-12-23 06:15:22.680477+00	2025-12-23 06:15:22.680477+00
138	CAI	Conventional Artistic Investigative (CAI)	Kombinasi yang menggabungkan organisasi, kreativitas, dan analisis. Kamu adalah researcher-organizer kreatif. Ideal untuk design librarian, creative asset manager, atau UX research coordinator.	["Organized creative research: Systematic investigation dengan aesthetic sensitivity", "Asset management: Organizing creative resources", "Design documentation: Recording creative decisions systematically", "Research coordination: Managing investigative projects"]	["Tension tiga dimensi: Structure, creativity, dan rigor all demanding", "Perfection across all: Wanting excellent organization, aesthetics, AND analysis", "Role clarity: Researcher, organizer, atau creative"]	["Priority by project: Which dimension matters most here", "Good enough standards: Not everything needs perfection in all three", "Collaboration: Partnering untuk complementary strengths"]	["Design research coordination: Organizing UX research", "Creative asset management: Managing design libraries", "Knowledge management: Organizing creative information"]	["Structured creative communication: Organized dan engaging", "Research documentation: Findings dalam accessible format", "Cross-functional liaison: Speaking to different teams"]	2025-12-23 06:15:22.683314+00	2025-12-23 06:15:22.683314+00
139	CAR	Conventional Artistic Realistic (CAR)	Kombinasi yang menggabungkan organisasi, kreativitas, dan kemampuan praktis. Kamu adalah maker terorganisir. Ideal untuk production coordinator, prop house manager, atau exhibit fabrication supervisor.	["Organized making: Systematic creative production", "Production coordination: Managing fabrication projects", "Quality systems: Maintaining craft standards dengan process", "Resource management: Organizing materials dan tools"]	["Efficiency vs craft: Speed vs quality", "Structure vs creativity: Process vs exploration", "Managing vs making: Coordinating vs doing"]	["Protective structure: Process yang enables good making", "Quality metrics: Standards yang include craft", "Hands-on time: Maintaining connection to making"]	["Production coordination: Managing making projects", "Prop management: Organizing creative assets", "Fabrication supervision: Leading making team"]	["Production communication: Clear coordination", "Quality feedback: Constructive craft critique", "Team coordination: Organizing makers"]	2025-12-23 06:15:22.685755+00	2025-12-23 06:15:22.685755+00
140	CAS	Conventional Artistic Social (CAS)	Kombinasi yang menggabungkan organisasi, kreativitas, dan kepedulian sosial. Kamu adalah administrator kreatif yang caring. Ideal untuk arts program coordinator, museum education manager, atau community center arts director.	["Organized creative service: Managing creative programs untuk people", "Arts administration: Running arts organization dengan heart", "Program coordination: Delivering engaging experiences systematically", "Community arts management: Organizing creative opportunities untuk public"]	["Bureaucracy vs soul: Administration bisa dampen spirit", "Structure vs spontaneity: Process vs responsive caring", "Multiple demands: Organizing, creating, dan helping all needed"]	["Purpose-first admin: Systems serve mission", "Flexible protocols: Structure dengan responsiveness", "Self-care: Managing energy across demands"]	["Arts organization: Managing creative nonprofit", "Museum education: Coordinating public programs", "Community arts: Organizing creative community service"]	["Warm professionalism: Caring dalam organized context", "Program promotion: Communicating opportunities engagingly", "Participant focus: Systems yang serve people"]	2025-12-23 06:15:22.689302+00	2025-12-23 06:15:22.689302+00
141	CEA	Conventional Enterprising Artistic (CEA)	Kombinasi yang menggabungkan organisasi, ambisi, dan kreativitas. Kamu adalah eksekutif dengan sensibilitas kreatif. Ideal untuk brand operations director, marketing operations executive, atau creative business manager.	["Efficient creative business: Running creative organization dengan systems", "Brand operations: Maintaining identity dengan scale", "Creative business management: Financial dan operational rigor untuk creative org", "Systematic growth: Expanding dengan maintained quality"]	["Efficiency vs artistry: Operations vs creative time", "Scale vs craft: Growth vs individual quality", "Control vs freedom: Management vs creative autonomy"]	["Creative-supporting operations: Systems yang enable not constrain", "Quality metrics: Including aesthetic standards", "Culture preservation: Maintaining creative culture saat growing"]	["Brand operations: Managing brand dengan systems", "Marketing operations: Running marketing dengan efficiency", "Creative business: Managing creative company operations"]	["Operational dengan flair: Efficient dan engaging", "Brand communication: Consistent dan creative", "Team direction: Structure dengan freedom"]	2025-12-23 06:15:22.693041+00	2025-12-23 06:15:22.693041+00
142	CEI	Conventional Enterprising Investigative (CEI)	Kombinasi yang menggabungkan organisasi, ambisi, dan analisis. Kamu adalah eksekutif sangat analitis. Ideal untuk analytics director, strategy operations, atau business intelligence executive.	["Analytical operations: Running organization dengan data", "Strategic systems: Building processes berbasis evidence", "Optimized growth: Expansion berbasis analysis", "Performance infrastructure: Systems untuk measurement dan improvement"]	["Over-systematization: Too much process", "Analysis paralysis: Too much data sebelum decision", "Quantification bias: Ignoring yang tidak terukur"]	["Adaptive systems: Process yang can evolve", "Decision thresholds: Clear criteria untuk action", "Qualitative inclusion: Valuing yang tidak easily measured"]	["Analytics leadership: Directing data function", "Strategy operations: Managing strategic planning process", "Business intelligence: Leading BI organization"]	["Data-driven communication: Evidence-based recommendations", "Systematic reporting: Regular performance updates", "Framework dialogue: Structured strategic discussion"]	2025-12-23 06:15:22.696724+00	2025-12-23 06:15:22.696724+00
143	CER	Conventional Enterprising Realistic (CER)	Kombinasi yang menggabungkan organisasi, ambisi, dan kemampuan praktis. Kamu adalah eksekutif operasional yang hands-on. Ideal untuk operations director, plant manager, atau logistics executive.	["Operational leadership: Directing production dengan systems", "Efficient scale: Growing output dengan maintained efficiency", "Hands-on management: Credible operational leadership", "Process optimization: Continuous improvement berbasis data"]	["Efficiency focus: Optimization bisa miss innovation", "Control orientation: Managing bisa become micromanaging", "Scale vs quality: Volume vs individual attention"]	["Innovation allocation: Resources untuk improvement", "Empowerment: Developing team capability", "Quality standards: Not sacrificing untuk volume"]	["Operations management: Directing production", "Plant leadership: Managing manufacturing", "Logistics direction: Running distribution"]	["Metrics communication: Talking in numbers", "Direct leadership: Clear expectations", "Operational updates: Regular performance reporting"]	2025-12-23 06:15:22.699767+00	2025-12-23 06:15:22.699767+00
144	CES	Conventional Enterprising Social (CES)	Kombinasi yang menggabungkan organisasi, ambisi, dan kepedulian sosial. Kamu adalah eksekutif yang caring. Ideal untuk HR director, nonprofit operations, atau healthcare business manager.	["People-focused operations: Systems yang serve human needs", "Organizational caring: Building culture of wellbeing dengan efficiency", "Scalable service: Growing impact dengan maintained quality", "Efficient compassion: Maximizing benefit per resource"]	["Efficiency vs individuality: Standard process vs personal needs", "Scale vs connection: Growing vs maintaining relationships", "Business vs caring: Sustainability vs unlimited giving"]	["Human-centered systems: Process designed around people", "Culture metrics: Measuring wellbeing", "Sustainable caring: Boundaries untuk long-term service"]	["HR operations: Managing people function", "Nonprofit operations: Running social organization efficiently", "Healthcare business: Managing health service delivery"]	["Caring efficiency: Warmth dengan professionalism", "People communication: Keeping everyone informed", "Performance dengan heart: Accountability dengan empathy"]	2025-12-23 06:15:22.7035+00	2025-12-23 06:15:22.7035+00
145	CIA	Conventional Investigative Artistic (CIA)	Kombinasi yang menggabungkan organisasi, analisis, dan kreativitas. Kamu adalah peneliti terorganisir dengan sensibilitas estetis. Ideal untuk research librarian, information designer, atau museum cataloguer.	["Organized aesthetic research: Systematic investigation dengan creative sensitivity", "Information design: Making data beautiful dan accessible", "Knowledge curation: Organizing information engagingly", "Research documentation: Recording findings attractively"]	["Triple tension: Structure, rigor, dan creativity all demanding", "Perfection pressure: Excellence di semua dimensi", "Time allocation: Each dimension needs attention"]	["Project priorities: Which dimension matters most here", "Good enough: Not everything needs perfection everywhere", "Collaboration: Partnering untuk complementary skills"]	["Research librarianship: Organizing dan finding information", "Information design: Making data accessible dan beautiful", "Archive management: Curating collections"]	["Visual research communication: Findings yang engaging", "Organized creativity: Structure dengan aesthetic", "Documentation dengan flair: Records yang inviting"]	2025-12-23 06:15:22.706909+00	2025-12-23 06:15:22.706909+00
146	CIE	Conventional Investigative Enterprising (CIE)	Kombinasi yang menggabungkan organisasi, analisis, dan ambisi. Kamu adalah analis eksekutif. Ideal untuk analytics executive, research director, atau intelligence firm leader.	["Analytical leadership: Directing dengan evidence", "Strategic research: Investigation untuk business impact", "Organized analysis: Systematic approach to insight", "Intelligence operations: Running analytical function"]	["Analysis paralysis: Too much research sebelum action", "Over-systematization: Process bisa slow insight", "Quantification bias: Missing yang tidak easily measured"]	["Decision protocols: Clear criteria untuk action", "Adaptive methodology: Process yang evolves", "Qualitative integration: Including non-quantifiable insight"]	["Analytics leadership: Directing data organization", "Research management: Running research function", "Intelligence direction: Leading analytical capability"]	["Evidence-based recommendations: Data-supported direction", "Systematic strategic communication: Structured insight sharing", "Research leadership: Directing investigative team"]	2025-12-23 06:15:22.709941+00	2025-12-23 06:15:22.709941+00
147	CIR	Conventional Investigative Realistic (CIR)	Kombinasi yang menggabungkan organisasi, analisis, dan kemampuan praktis. Kamu adalah teknisi-analis sangat terstruktur. Ideal untuk laboratory manager, quality director, atau technical standards specialist.	["Systematic technical research: Investigation dengan precision", "Quality leadership: Directing testing dan standards", "Method management: Developing dan maintaining protocols", "Technical documentation: Recording procedures comprehensively"]	["Rigid methodology: Too attached to established process", "Documentation overhead: Recording everything takes time", "Adaptation difficulty: Changing proven methods is hard"]	["Protocol review: Regular evaluation untuk improvement", "Efficient documentation: Streamlined recording", "Flexibility windows: Room untuk adaptation dalam structure"]	["Laboratory management: Directing lab operations", "Quality direction: Leading QA function", "Standards: Developing dan maintaining technical standards"]	["Procedural communication: Clear methodological instruction", "Technical documentation: Comprehensive records", "Method sharing: Enabling replication"]	2025-12-23 06:15:22.71274+00	2025-12-23 06:15:22.71274+00
148	CIS	Conventional Investigative Social (CIS)	Kombinasi yang menggabungkan organisasi, analisis, dan kepedulian sosial. Kamu adalah analis yang caring. Ideal untuk program evaluation manager, social research coordinator, atau healthcare quality director.	["Systematic caring research: Investigation untuk service improvement", "Program quality: Ensuring services meet standards", "Evidence-based service: Using data untuk better helping", "Organized advocacy: Using evidence untuk systematic change"]	["Data vs relationship: Metrics bisa miss human connection", "Bureaucracy of measurement: Tracking bisa burden service", "Analysis vs action: Research bisa delay helping"]	["Purpose-driven data: Measuring apa yang truly matters", "Efficient evaluation: Tracking yang tidak burden", "Actionable output: Research yang leads ke improvement"]	["Program evaluation: Directing assessment function", "Healthcare quality: Leading quality improvement", "Social research: Managing research untuk social benefit"]	["Accessible evidence: Findings untuk non-researchers", "Improvement-focused communication: Data untuk getting better", "Collaborative analysis: Including stakeholders dalam interpretation"]	2025-12-23 06:15:22.715741+00	2025-12-23 06:15:22.715741+00
149	CRA	Conventional Realistic Artistic (CRA)	Kombinasi yang menggabungkan organisasi, kemampuan praktis, dan kreativitas. Kamu adalah teknisi terorganisir dengan sentuhan estetis. Ideal untuk technical illustrator, CAD specialist, atau precision craft documentation.	["Precise creative documentation: Technical records yang clear dan attractive", "Organized making: Systematic approach to craft", "Technical aesthetics: Function dengan form", "Standards dengan flair: Process yang efficient dan engaging"]	["Efficiency vs beauty: Speed vs aesthetic quality", "Precision vs creativity: Accuracy vs exploration", "Documentation vs making: Recording vs doing"]	["Context priorities: When aesthetics matter most", "Efficient beauty: Templates yang sudah attractive", "Balance time: Allocation across dimensions"]	["Technical illustration: Visual technical communication", "CAD/CAM: Precise design dengan aesthetic consideration", "Precision craft: Detailed making dengan documentation"]	["Visual technical communication: Diagrams yang clear dan attractive", "Organized creativity: Structured dengan aesthetic", "Documentation dengan care: Records yang inviting"]	2025-12-23 06:15:22.718797+00	2025-12-23 06:15:22.718797+00
150	CRE	Conventional Realistic Enterprising (CRE)	Kombinasi yang menggabungkan organisasi, kemampuan praktis, dan ambisi. Kamu adalah supervisor operasional. Ideal untuk production supervisor, operations coordinator, atau facility manager.	["Operational coordination: Running production dengan systems", "Efficient execution: Getting things done on time dan budget", "Process improvement: Continuous optimization", "Reliable delivery: Consistent output"]	["Efficiency tunnel vision: Optimization bisa miss bigger picture", "Control focus: Managing detail bisa become micromanaging", "Doing vs delegating: Preference untuk hands-on"]	["Strategic perspective: Regular stepping back", "Team development: Building capability", "Innovation time: Resources untuk improvement"]	["Production supervision: Managing making operations", "Operations coordination: Running daily operations", "Facility management: Maintaining operational space"]	["Metrics focus: Talking in efficiency dan output", "Clear direction: Straightforward expectations", "Regular updates: Consistent progress reporting"]	2025-12-23 06:15:22.723301+00	2025-12-23 06:15:22.723301+00
151	CRI	Conventional Realistic Investigative (CRI)	Kombinasi yang menggabungkan organisasi, kemampuan praktis, dan analisis. Kamu adalah teknisi-analis. Ideal untuk lab technician, quality analyst, atau technical inspector.	["Systematic technical work: Precise execution dengan analysis", "Quality analysis: Testing dan evaluation", "Method execution: Following protocols dengan precision", "Technical documentation: Recording procedures dan findings"]	["Rigid adherence: Too attached to protocol", "Documentation overhead: Recording takes time dari doing", "Adaptation difficulty: Hard to change established methods"]	["Protocol flexibility: Room untuk judgment dalam structure", "Efficient recording: Streamlined documentation", "Continuous improvement: Regular method review"]	["Laboratory: Technical testing dan analysis", "Quality control: Inspection dan evaluation", "Technical standards: Compliance dan verification"]	["Procedural communication: Clear methodological guidance", "Technical reporting: Detailed findings", "Systematic sharing: Consistent format"]	2025-12-23 06:15:22.727285+00	2025-12-23 06:15:22.727285+00
152	CRS	Conventional Realistic Social (CRS)	Kombinasi yang menggabungkan organisasi, kemampuan praktis, dan kepedulian sosial. Kamu adalah helper yang terstruktur dan hands-on. Ideal untuk vocational instructor, rehabilitation aide, atau assisted living coordinator.	["Organized practical helping: Systematic approach ke concrete assistance", "Skills instruction: Teaching practical abilities dengan curriculum", "Service coordination: Managing hands-on support", "Reliable care: Consistent, dependable assistance"]	["Protocol vs need: Structure tidak selalu fit individual", "Paperwork vs helping: Admin takes time dari direct service", "Efficiency vs thoroughness: Serving many vs helping well"]	["Adaptive protocols: Flexibility dalam structure", "Efficient documentation: Focus on truly necessary", "Quality priority: Better to help fewer well"]	["Vocational training: Teaching practical skills", "Rehabilitation: Hands-on recovery support", "Assisted living: Coordinating practical care"]	["Clear guidance: Instructions yang mudah follow", "Patient teaching: Empathetic skill transfer", "Reliable follow-up: Ensuring continued progress"]	2025-12-23 06:15:22.730224+00	2025-12-23 06:15:22.730224+00
153	CSA	Conventional Social Artistic (CSA)	Kombinasi yang menggabungkan organisasi, kepedulian sosial, dan kreativitas. Kamu adalah administrator yang caring dengan flair. Ideal untuk arts nonprofit coordinator, community program manager, atau event coordinator untuk social causes.	["Organized creative caring: Managing creative service dengan heart", "Program coordination: Running engaging helpful programs", "Event management: Creating meaningful experiences", "Community organizing: Building connection dengan structure"]	["Bureaucracy vs creativity: Admin bisa dampen creative spirit", "Structure vs spontaneity: Process vs responsive caring", "Multiple demands: Organizing, helping, dan creating all need attention"]	["Purpose-first admin: Systems serve mission dan creativity", "Flexible protocols: Structure dengan responsiveness", "Energy management: Sustainable across demands"]	["Arts nonprofit: Coordinating creative service", "Community program: Managing engaging outreach", "Event coordination: Creating meaningful gatherings"]	["Warm organized communication: Caring dengan professionalism", "Creative promotion: Engaging program communication", "Participant focus: Systems yang serve people"]	2025-12-23 06:15:22.732936+00	2025-12-23 06:15:22.732936+00
154	CSE	Conventional Social Enterprising (CSE)	Kombinasi yang menggabungkan organisasi, kepedulian sosial, dan ambisi. Kamu adalah manajer yang caring dan ambisius. Ideal untuk HR manager, nonprofit program director, atau healthcare coordinator.	["Efficient caring management: Leading service delivery dengan systems", "People operations: Managing human aspects dengan structure", "Scalable service: Growing impact dengan maintained quality", "Team development: Building caring dan capable team"]	["Efficiency vs individuality: Standards vs personal needs", "Growth vs connection: Scaling vs relationships", "Business vs mission: Sustainability vs unlimited service"]	["Human-centered process: Systems designed around people", "Caring metrics: Measuring wellbeing", "Sustainable boundaries: Enabling long-term service"]	["HR management: Running people function", "Nonprofit program: Directing service delivery", "Healthcare coordination: Managing care delivery"]	["Caring leadership: Warmth dengan professionalism", "Team communication: Keeping everyone informed dan motivated", "Performance dengan heart: Accountability dengan empathy"]	2025-12-23 06:15:22.736382+00	2025-12-23 06:15:22.736382+00
155	CSI	Conventional Social Investigative (CSI)	Kombinasi yang menggabungkan organisasi, kepedulian sosial, dan analisis. Kamu adalah administrator yang caring dan analitis. Ideal untuk program evaluator, social work supervisor, atau quality improvement coordinator.	["Systematic caring: Organized approach ke service improvement", "Evidence-based service: Using data untuk better helping", "Quality assurance: Ensuring standards dalam caring", "Program coordination: Managing research-informed service"]	["Data vs connection: Metrics bisa miss human element", "Analysis vs action: Research bisa delay helping", "Bureaucracy of care: Tracking bisa burden service"]	["Purpose-driven data: Measuring apa yang matters", "Efficient tracking: System yang tidak burden", "Actionable analysis: Research untuk improvement"]	["Program quality: Ensuring service standards", "Social work supervision: Managing casework dengan data", "Healthcare quality: Coordinating improvement efforts"]	["Improvement-focused communication: Data untuk getting better", "Collaborative analysis: Including team dalam interpretation", "Accessible reporting: Findings untuk non-researchers"]	2025-12-23 06:15:22.740166+00	2025-12-23 06:15:22.740166+00
156	CSR	Conventional Social Realistic (CSR)	Kombinasi yang menggabungkan organisasi, kepedulian sosial, dan kemampuan praktis. Kamu adalah helper yang terstruktur dan hands-on. Ideal untuk case manager, rehabilitation coordinator, atau community health worker.	["Organized practical caring: Systematic concrete assistance", "Service coordination: Managing hands-on support systematically", "Resource management: Connecting people dengan practical help", "Reliable support: Consistent, dependable assistance"]	["Protocol vs need: Structure tidak selalu fit situation", "Paperwork vs helping: Documentation takes time dari service", "Efficiency vs thoroughness: Many vs well"]	["Adaptive structure: Flexibility dalam process", "Efficient records: Focus on necessary documentation", "Quality focus: Helping fewer people better"]	["Case management: Coordinating services untuk clients", "Community health: Organized outreach dan support", "Rehabilitation: Structured recovery assistance"]	["Clear helpful guidance: Instructions yang easy to follow", "Reliable follow-through: Ensuring services delivered", "Practical empathy: Caring yang concrete dan helpful"]	2025-12-23 06:15:22.743521+00	2025-12-23 06:15:22.743521+00
\.


--
-- Data for Name: riasec_question_sets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.riasec_question_sets (id, test_session_id, question_ids, generated_at) FROM stdin;
\.


--
-- Data for Name: riasec_responses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.riasec_responses (id, test_session_id, responses_data, created_at) FROM stdin;
\.


--
-- Data for Name: riasec_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.riasec_results (id, test_session_id, score_r, score_i, score_a, score_s, score_e, score_c, riasec_code_id, riasec_code_type, is_inconsistent_profile, calculated_at) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, user_id, token, expires_at, is_active, auth_provider, device_info, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: user_ikigais; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_ikigais (id, user_id, profile, chart_data, hash, results, riasec_explanations, riasec_map_full, created_at) FROM stdin;
\.


--
-- Data for Name: user_riasecs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_riasecs (id, user_id, profile, normalized_scores, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, profile_image_url, fullname, email, password, is_verified, phone_number, role, created_at, updated_at, deleted_at) FROM stdin;
a1a2b473-f398-4489-b7ef-6984b60e4f10			admin@email.com	$2a$04$UW.zXoCijbmsa1L4Uqt/ceU80wRe9x6oagIUpqxPt9kXFvoegkftC	t	0811111111	ADMIN	2025-12-23 06:15:22.133307	2025-12-23 06:15:22.130035	\N
ef9cf8e8-46b1-4e91-89d0-40f6c824319e			user@email.com	$2a$04$EyPPk.W.8i86lSRAGrgKpeeNHTLER4GOjOZw.yJZOocKM4/x3PhWi	t	0888888888	USER	2025-12-23 06:15:22.140976	2025-12-23 06:15:22.138247	\N
\.


--
-- Name: career_recommendations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.career_recommendations_id_seq', 1, false);


--
-- Name: careerprofile_test_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.careerprofile_test_sessions_id_seq', 1, false);


--
-- Name: ikigai_candidate_professions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ikigai_candidate_professions_id_seq', 1, false);


--
-- Name: ikigai_dimension_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ikigai_dimension_scores_id_seq', 1, false);


--
-- Name: ikigai_responses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ikigai_responses_id_seq', 1, false);


--
-- Name: ikigai_total_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ikigai_total_scores_id_seq', 1, false);


--
-- Name: kenalidiri_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kenalidiri_categories_id_seq', 1, false);


--
-- Name: kenalidiri_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kenalidiri_history_id_seq', 1, false);


--
-- Name: riasec_codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.riasec_codes_id_seq', 1, false);


--
-- Name: riasec_question_sets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.riasec_question_sets_id_seq', 1, false);


--
-- Name: riasec_responses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.riasec_responses_id_seq', 1, false);


--
-- Name: riasec_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.riasec_results_id_seq', 1, false);


--
-- Name: career_recommendations career_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.career_recommendations
    ADD CONSTRAINT career_recommendations_pkey PRIMARY KEY (id);


--
-- Name: careerprofile_test_sessions careerprofile_test_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.careerprofile_test_sessions
    ADD CONSTRAINT careerprofile_test_sessions_pkey PRIMARY KEY (id);


--
-- Name: ikigai_candidate_professions ikigai_candidate_professions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_candidate_professions
    ADD CONSTRAINT ikigai_candidate_professions_pkey PRIMARY KEY (id);


--
-- Name: ikigai_dimension_scores ikigai_dimension_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_dimension_scores
    ADD CONSTRAINT ikigai_dimension_scores_pkey PRIMARY KEY (id);


--
-- Name: ikigai_responses ikigai_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_responses
    ADD CONSTRAINT ikigai_responses_pkey PRIMARY KEY (id);


--
-- Name: ikigai_total_scores ikigai_total_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_total_scores
    ADD CONSTRAINT ikigai_total_scores_pkey PRIMARY KEY (id);


--
-- Name: kenalidiri_categories kenalidiri_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kenalidiri_categories
    ADD CONSTRAINT kenalidiri_categories_pkey PRIMARY KEY (id);


--
-- Name: kenalidiri_history kenalidiri_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kenalidiri_history
    ADD CONSTRAINT kenalidiri_history_pkey PRIMARY KEY (id);


--
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id);


--
-- Name: riasec_codes riasec_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_codes
    ADD CONSTRAINT riasec_codes_pkey PRIMARY KEY (id);


--
-- Name: riasec riasec_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec
    ADD CONSTRAINT riasec_pkey PRIMARY KEY (id);


--
-- Name: riasec_question_sets riasec_question_sets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_question_sets
    ADD CONSTRAINT riasec_question_sets_pkey PRIMARY KEY (id);


--
-- Name: riasec_responses riasec_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_responses
    ADD CONSTRAINT riasec_responses_pkey PRIMARY KEY (id);


--
-- Name: riasec_results riasec_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_results
    ADD CONSTRAINT riasec_results_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: user_ikigais user_ikigais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_ikigais
    ADD CONSTRAINT user_ikigais_pkey PRIMARY KEY (id);


--
-- Name: user_riasecs user_riasecs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_riasecs
    ADD CONSTRAINT user_riasecs_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_career_recommendations_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_career_recommendations_test_session_id ON public.career_recommendations USING btree (test_session_id);


--
-- Name: idx_careerprofile_test_sessions_session_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_careerprofile_test_sessions_session_token ON public.careerprofile_test_sessions USING btree (session_token);


--
-- Name: idx_ikigai_candidate_professions_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_ikigai_candidate_professions_test_session_id ON public.ikigai_candidate_professions USING btree (test_session_id);


--
-- Name: idx_ikigai_dimension_scores_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_ikigai_dimension_scores_test_session_id ON public.ikigai_dimension_scores USING btree (test_session_id);


--
-- Name: idx_ikigai_responses_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_ikigai_responses_test_session_id ON public.ikigai_responses USING btree (test_session_id);


--
-- Name: idx_ikigai_total_scores_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_ikigai_total_scores_test_session_id ON public.ikigai_total_scores USING btree (test_session_id);


--
-- Name: idx_kenalidiri_categories_category_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_kenalidiri_categories_category_code ON public.kenalidiri_categories USING btree (category_code);


--
-- Name: idx_kenalidiri_history_test_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_kenalidiri_history_test_category_id ON public.kenalidiri_history USING btree (test_category_id);


--
-- Name: idx_riasec_codes_riasec_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_riasec_codes_riasec_code ON public.riasec_codes USING btree (riasec_code);


--
-- Name: idx_riasec_question_sets_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_riasec_question_sets_test_session_id ON public.riasec_question_sets USING btree (test_session_id);


--
-- Name: idx_riasec_responses_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_riasec_responses_test_session_id ON public.riasec_responses USING btree (test_session_id);


--
-- Name: idx_riasec_results_test_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_riasec_results_test_session_id ON public.riasec_results USING btree (test_session_id);


--
-- Name: idx_sessions_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_sessions_token ON public.sessions USING btree (token);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: career_recommendations fk_career_recommendations_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.career_recommendations
    ADD CONSTRAINT fk_career_recommendations_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: careerprofile_test_sessions fk_careerprofile_test_sessions_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.careerprofile_test_sessions
    ADD CONSTRAINT fk_careerprofile_test_sessions_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ikigai_candidate_professions fk_ikigai_candidate_professions_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_candidate_professions
    ADD CONSTRAINT fk_ikigai_candidate_professions_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ikigai_dimension_scores fk_ikigai_dimension_scores_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_dimension_scores
    ADD CONSTRAINT fk_ikigai_dimension_scores_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ikigai_responses fk_ikigai_responses_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_responses
    ADD CONSTRAINT fk_ikigai_responses_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ikigai_total_scores fk_ikigai_total_scores_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ikigai_total_scores
    ADD CONSTRAINT fk_ikigai_total_scores_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: kenalidiri_history fk_kenalidiri_history_test_category; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kenalidiri_history
    ADD CONSTRAINT fk_kenalidiri_history_test_category FOREIGN KEY (test_category_id) REFERENCES public.kenalidiri_categories(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: kenalidiri_history fk_kenalidiri_history_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kenalidiri_history
    ADD CONSTRAINT fk_kenalidiri_history_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: riasec_question_sets fk_riasec_question_sets_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_question_sets
    ADD CONSTRAINT fk_riasec_question_sets_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: riasec_responses fk_riasec_responses_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_responses
    ADD CONSTRAINT fk_riasec_responses_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: riasec_results fk_riasec_results_career_profile_test_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_results
    ADD CONSTRAINT fk_riasec_results_career_profile_test_session FOREIGN KEY (test_session_id) REFERENCES public.careerprofile_test_sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: riasec_results fk_riasec_results_riasec_code; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.riasec_results
    ADD CONSTRAINT fk_riasec_results_riasec_code FOREIGN KEY (riasec_code_id) REFERENCES public.riasec_codes(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict ZPmMUNU8yqbDLaTpjK8PsWL91ImdviZZZahgQh7ypTxxbLFJFBc1CmpIXFP7EM2


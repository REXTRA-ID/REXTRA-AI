# app/api/v1/categories/career_profile/prompts/ikigai_prompts.py
"""
Ikigai Prompts & Static Metadata

Berisi:
1. DIMENSION_METADATA — data statis 4 dimensi Ikigai untuk endpoint GET /dimensions (poin 4)
2. FALLBACK_CONTENT_TEMPLATE — teks fallback jika Gemini gagal generate konten

DIMENSION_METADATA digunakan oleh:
    routers/ikigai.py → GET /dimensions (poin 4)
    → Flutter merender label, pertanyaan, helper text, dan contoh placeholder

Setiap item DIMENSION_METADATA memiliki field:
    dimension_key          : key internal (sama dengan IKIGAI_DIMENSIONS)
    label                  : label pendek bahasa Inggris
    label_id               : label pendek bahasa Indonesia
    question_prompt        : pertanyaan utama yang ditampilkan Flutter sebagai judul soal
    description            : penjelasan tujuan dimensi (untuk tooltip/info card)
    helper_text_selected   : teks instruksi jika user MEMILIH opsi (poin 15)
    helper_text_not_selected: teks instruksi jika user TIDAK memilih opsi (poin 15)
    example_text_selected  : placeholder teks jika user memilih
    example_text_not_selected: placeholder teks jika user tidak memilih
    min_chars              : minimum karakter reasoning_text
    max_chars              : maksimum karakter reasoning_text
"""

# ---------------------------------------------------------------------------
# POIN 4 — Metadata statis 4 dimensi Ikigai
# Digunakan: GET /career-profile/ikigai/dimensions
# ---------------------------------------------------------------------------
DIMENSION_METADATA = [
    {
        "dimension_key":   "what_you_love",
        "label":           "What You Love",
        "label_id":        "Apa yang Kamu Cintai",
        "question_prompt": (
            "Dari beberapa aktivitas kerja berikut, manakah yang paling menarik "
            "dan paling ingin kamu lakukan secara berulang dalam kehidupan sehari-hari?"
        ),
        "description": (
            "Dimensi ini mengukur minat intrinsik dan potensi passion — "
            "ketertarikan yang kuat dan konsisten terhadap jenis aktivitas kerja tertentu, "
            "terlepas dari nama jabatan formalnya."
        ),
        # Poin 15 — helper text berbeda tergantung kondisi pemilihan
        "helper_text_selected": (
            "Bagian spesifik mana dari aktivitas yang kamu pilih yang paling kamu sukai? "
            "Jelaskan alasannya (Misal: karena Prosesnya / Interaksinya / Dampaknya)."
        ),
        "helper_text_not_selected": (
            "Tidak ada yang cocok? Ceritakan aktivitas kerja seperti apa yang "
            "sebenarnya paling membuatmu semangat dan lupa waktu saat melakukannya."
        ),
        "example_text_selected": (
            "Saya memilih ini karena saya paling suka prosesnya. "
            "Saya senang ketika harus berpikir keras memecahkan masalah rumit, "
            "meskipun tidak bertemu banyak orang."
        ),
        "example_text_not_selected": (
            "Sebenarnya saya lebih suka aktivitas yang banyak bergerak di luar ruangan "
            "dan bertemu orang baru setiap hari, daripada harus duduk menganalisis data."
        ),
        "min_chars": 20,
        "max_chars": 1000,
    },
    {
        "dimension_key":   "what_you_are_good_at",
        "label":           "What You Are Good At",
        "label_id":        "Apa yang Kamu Kuasai",
        "question_prompt": (
            "Jika kamu diminta untuk segera mengerjakan salah satu aktivitas berikut "
            "tanpa banyak persiapan, aktivitas mana yang paling kamu yakini dapat "
            "kamu kerjakan dengan baik?"
        ),
        "description": (
            "Dimensi ini mengukur persepsi kompetensi (self-efficacy) — "
            "keyakinan bahwa suatu tugas dapat dikerjakan dengan baik, "
            "karena sudah memiliki skill tersebut atau merasa mudah mempelajarinya."
        ),
        "helper_text_selected": (
            "Jelaskan secara spesifik, bagian mana dari aktivitas yang kamu pilih "
            "yang membuatmu merasa paling mampu mengerjakannya. Apakah karena sudah "
            "sering melakukannya, pernah belajar sebelumnya, atau merasa mudah mempelajarinya?"
        ),
        "helper_text_not_selected": (
            "Kamu tidak memilih opsi mana pun. Jelaskan aktivitas kerja seperti apa "
            "yang paling kamu kuasai atau paling mudah kamu pelajari. Fokuskan pada "
            "apa yang kamu lakukan, bukan nama jabatannya."
        ),
        "example_text_selected": (
            "Saya merasa mampu karena pernah mengerjakan tugas serupa di kuliah. "
            "Saya cepat memahami hal-hal yang berkaitan dengan analisis data dan "
            "sudah terbiasa dengan tools seperti Python dan SQL."
        ),
        "example_text_not_selected": (
            "Saya paling percaya diri ketika harus menjelaskan sesuatu kepada orang lain. "
            "Saya mudah menguasai tugas yang berkaitan dengan komunikasi dan presentasi."
        ),
        "min_chars": 20,
        "max_chars": 1000,
    },
    {
        "dimension_key":   "what_the_world_needs",
        "label":           "What The World Needs",
        "label_id":        "Apa yang Dunia Butuhkan",
        "question_prompt": (
            "Setiap pekerjaan memberikan dampak yang berbeda bagi orang lain. "
            "Dampak seperti apa yang menurutmu paling penting untuk dunia "
            "atau masyarakat saat ini?"
        ),
        "description": (
            "Dimensi ini mengidentifikasi nilai pribadi dan orientasi dampak sosial — "
            "berkaitan dengan potensi mission (rasa panggilan terhadap isu tertentu) "
            "dan vocation (peran sosial yang dirasa penting dan layak dijalani)."
        ),
        "helper_text_selected": (
            "Mengapa dampak ini begitu penting bagimu? Ceritakan apakah ada pengalaman "
            "pribadi yang memicu kepedulianmu terhadap isu ini, atau karena kamu merasa "
            "gelisah jika masalah ini tidak segera diselesaikan."
        ),
        "helper_text_not_selected": (
            "Kamu tidak memilih opsi mana pun. Jelaskan perubahan nyata apa yang ingin "
            "kamu lihat di dunia melalui pekerjaanmu. Fokuskan pada masalah apa yang "
            "ingin kamu atasi atau siapa yang paling ingin kamu bantu."
        ),
        "example_text_selected": (
            "Saya pernah melihat langsung bagaimana kurangnya akses pendidikan membuat "
            "banyak anak di daerah terpencil tertinggal. Saya merasa tidak tenang "
            "jika masalah ini dibiarkan begitu saja."
        ),
        "example_text_not_selected": (
            "Saya ingin mengurangi masalah kesehatan mental di kalangan anak muda. "
            "Saya ingin pekerjaan saya berkontribusi pada kelompok yang sering "
            "diabaikan oleh sistem yang ada."
        ),
        "min_chars": 20,
        "max_chars": 1000,
    },
    {
        "dimension_key":   "what_you_can_be_paid_for",
        "label":           "What You Can Be Paid For",
        "label_id":        "Apa yang Bisa Menghasilkan",
        "question_prompt": (
            "Setiap pekerjaan memiliki pola kerja dan imbalan yang berbeda. "
            "Pola seperti apa yang paling realistis dan nyaman untuk kehidupan "
            "yang kamu bayangkan dalam jangka panjang?"
        ),
        "description": (
            "Dimensi ini memetakan harapan finansial, preferensi pola kerja, dan "
            "toleransi risiko karier — berkaitan dengan profession dan vocation: "
            "pekerjaan yang tidak hanya dikuasai dan dibutuhkan, tetapi juga secara "
            "nyata bisa menjadi sumber penghidupan yang layak."
        ),
        "helper_text_selected": (
            "Mengapa pola kerja dan penghasilan seperti ini paling sesuai bagimu? "
            "Jelaskan apakah kamu lebih mengutamakan kestabilan, fleksibilitas waktu, "
            "peluang penghasilan tinggi, atau aspek lain yang penting untuk hidupmu ke depan."
        ),
        "helper_text_not_selected": (
            "Kamu tidak memilih opsi mana pun. Jelaskan pola kerja dan penghasilan "
            "seperti apa yang menurutmu paling ideal. Fokuskan pada bagaimana kamu "
            "ingin bekerja dan bagaimana penghasilan tersebut mendukung gaya hidupmu."
        ),
        "example_text_selected": (
            "Saya lebih nyaman dengan penghasilan tetap karena saya punya tanggungan "
            "keluarga. Saya butuh kepastian agar bisa merencanakan keuangan jangka panjang."
        ),
        "example_text_not_selected": (
            "Saya menginginkan penghasilan yang bisa naik seiring pengalaman, "
            "dengan jam kerja yang fleksibel. Saya bersedia menerima penghasilan "
            "awal yang lebih kecil asalkan ada jalur karier yang jelas."
        ),
        "min_chars": 20,
        "max_chars": 1000,
    },
]

# ---------------------------------------------------------------------------
# FALLBACK_CONTENT_TEMPLATE
# Digunakan oleh AIContentService jika Gemini gagal generate konten.
# ---------------------------------------------------------------------------
FALLBACK_CONTENT_TEMPLATE = {
    "what_you_love": (
        "Kamu akan mengerjakan aktivitas yang menantang dan memberikan kepuasan tersendiri. "
        "Pekerjaan ini cocok untuk kamu yang senang berpikir kritis dan menciptakan solusi baru."
    ),
    "what_you_are_good_at": (
        "Kamu memiliki kemampuan teknis yang kuat di bidang {skills}. "
        "Skill ini sangat relevan dan bisa langsung diterapkan dalam pekerjaan ini."
    ),
    "what_the_world_needs": (
        "Bidang ini memiliki dampak nyata terhadap kehidupan banyak orang. "
        "Kontribusimu di sini akan membantu menyelesaikan masalah yang dihadapi masyarakat luas."
    ),
    "what_you_can_be_paid_for": (
        "Profesi ini memiliki prospek karier yang baik dengan kompensasi yang kompetitif. "
        "Kamu bisa berkembang secara profesional seiring bertambahnya pengalaman dan keahlian."
    ),
    # Fallback opsi checkbox
    "what_you_love_option":            "Mengerjakan tugas inti profesi ini secara langsung setiap hari.",
    "what_you_are_good_at_option":     "Menyelesaikan tantangan teknis utama yang menjadi kompetensi khas profesi ini.",
    "what_the_world_needs_option":     "Berkontribusi pada kebutuhan nyata masyarakat melalui peran ini.",
    "what_you_can_be_paid_for_option": "Berkarir profesional dengan kompensasi pasar yang kompetitif.",
}

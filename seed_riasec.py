import json
import psycopg2

mockRiasecQuestions = [
  {'id': 'R1', 'pertanyaan': 'Saya senang merakit dan memperbaiki perangkat elektronik atau komponen teknologi'},
  {'id': 'R2', 'pertanyaan': 'Saya tertarik membangun dan mengatur infrastruktur jaringan komputer atau sistem penyimpanan data'},
  {'id': 'R3', 'pertanyaan': 'Saya suka memasang dan mengatur perangkat otomatis (sensor, IoT) untuk memantau kondisi sistem fisik atau lingkungan'},
  {'id': 'R4', 'pertanyaan': 'Saya merasa puas ketika berhasil menggunakan software teknis untuk desain atau simulasi sistem kompleks'},
  {'id': 'R5', 'pertanyaan': 'Saya senang mengatur dan menyiapkan peralatan recording, streaming, atau equipment untuk produksi konten digital'},
  {'id': 'R6', 'pertanyaan': 'Saya tertarik mengoptimalkan performa sistem digital, server, atau infrastruktur jaringan'},
  {'id': 'R7', 'pertanyaan': 'Saya yakin bisa mengoperasikan dan merawat perangkat elektronik presisi tinggi yang sensitif'},
  {'id': 'R8', 'pertanyaan': 'Saya yakin mampu mengatur sistem pelacakan dan monitoring untuk operasi logistik atau distribusi'},
  {'id': 'R9', 'pertanyaan': 'Saya percaya diri bisa mengatur infrastruktur teknologi atau sistem pembayaran digital'},
  {'id': 'R10', 'pertanyaan': 'Saya suka mengatur, merawat, dan memelihara server, sistem komputer, atau infrastruktur IT'},
  {'id': 'R11', 'pertanyaan': 'Saya tertarik mencoba dan mengeksplorasi teknologi otomasi seperti chatbot, AI assistant, atau sistem pintar'},
  {'id': 'R12', 'pertanyaan': 'Saya senang menggunakan sistem digital untuk mengelola dan mengorganisir berbagai keperluan'},
  {'id': 'I1', 'pertanyaan': 'Saya senang menganalisis data transaksi atau keuangan untuk menemukan pola, anomali, atau wawasan bisnis'},
  {'id': 'I2', 'pertanyaan': 'Saya tertarik meneliti dan menganalisis kumpulan data yang kompleks untuk menemukan pola atau insight penting'},
  {'id': 'I3', 'pertanyaan': 'Saya suka menggunakan analisis data untuk meningkatkan efisiensi dan produktivitas operasional suatu sistem'},
  {'id': 'I4', 'pertanyaan': 'Saya merasa tertantang untuk menganalisis kelemahan keamanan, celah sistem, atau ancaman digital'},
  {'id': 'I5', 'pertanyaan': 'Saya senang meneliti perilaku pengguna dan tren pasar untuk mendukung keputusan strategis'},
  {'id': 'I6', 'pertanyaan': 'Saya tertarik menganalisis data operasional untuk meningkatkan efisiensi proses dan pengambilan keputusan'},
  {'id': 'I7', 'pertanyaan': 'Saya yakin bisa menganalisis performa konten digital atau engagement untuk optimasi strategi'},
  {'id': 'I8', 'pertanyaan': 'Saya percaya diri dapat menganalisis data aset atau investasi untuk menghasilkan wawasan strategis'},
  {'id': 'I9', 'pertanyaan': 'Saya yakin mampu meneliti dan menganalisis data sumber daya untuk keberlanjutan dan efisiensi'},
  {'id': 'I10', 'pertanyaan': 'Saya suka menganalisis informasi secara mendalam untuk membuat kesimpulan atau keputusan yang tepat'},
  {'id': 'I11', 'pertanyaan': 'Saya tertarik melakukan riset mendalam tentang suatu topik atau masalah yang kompleks'},
  {'id': 'I12', 'pertanyaan': 'Saya senang menggunakan tools atau aplikasi untuk mengolah dan menganalisis data'},
  {'id': 'A1', 'pertanyaan': 'Saya senang mendesain tampilan antarmuka digital (UI/UX) yang menarik dan mudah digunakan'},
  {'id': 'A2', 'pertanyaan': 'Saya tertarik membuat konten kreatif visual untuk media sosial dan kampanye digital'},
  {'id': 'A3', 'pertanyaan': 'Saya suka mendesain identitas visual dan brand untuk perusahaan atau produk digital'},
  {'id': 'A4', 'pertanyaan': 'Saya merasa kreatif ketika membuat konten edukasi, infografis, atau materi visual pembelajaran'},
  {'id': 'A5', 'pertanyaan': 'Saya senang mendesain visualisasi data atau dashboard yang menarik dan mudah dipahami'},
  {'id': 'A6', 'pertanyaan': 'Saya tertarik mengeksplorasi gaya penulisan kreatif (copywriting) untuk kampanye atau promosi'},
  {'id': 'A7', 'pertanyaan': 'Saya yakin bisa mengedit dan merangkai video menjadi karya yang bercerita dan menggugah emosi'},
  {'id': 'A8', 'pertanyaan': 'Saya percaya diri dapat menciptakan karya ilustrasi, animasi, atau desain karakter digital'},
  {'id': 'A9', 'pertanyaan': 'Saya yakin mampu membuat konsep kreatif untuk desain produk atau kemasan digital'},
  {'id': 'A10', 'pertanyaan': 'Saya suka bereksperimen dengan warna, tata letak, dan tipografi untuk membuat desain yang estetis'},
  {'id': 'A11', 'pertanyaan': 'Saya tertarik membuat karya seni atau desain yang unik dan belum pernah dibuat sebelumnya'},
  {'id': 'A12', 'pertanyaan': 'Saya senang menuangkan ide dan imajinasi melalui tulisan atau desain visual'},
  {'id': 'S1', 'pertanyaan': 'Saya senang mengajar atau melatih orang lain menggunakan aplikasi atau teknologi baru'},
  {'id': 'S2', 'pertanyaan': 'Saya tertarik membantu pelanggan atau pengguna menyelesaikan masalah teknis mereka'},
  {'id': 'S3', 'pertanyaan': 'Saya suka mengelola komunitas online, memfasilitasi diskusi, dan menjaga interaksi positif'},
  {'id': 'S4', 'pertanyaan': 'Saya merasa puas ketika bisa mendengarkan masalah klien dan memberikan solusi digital yang tepat'},
  {'id': 'S5', 'pertanyaan': 'Saya senang bekerja dalam tim untuk mendukung dan memfasilitasi rekan kerja menyelesaikan proyek'},
  {'id': 'S6', 'pertanyaan': 'Saya tertarik membuat panduan atau tutorial yang memudahkan orang lain memahami sistem kompleks'},
  {'id': 'S7', 'pertanyaan': 'Saya yakin bisa memandu pengguna melewati proses onboarding layanan digital dengan ramah'},
  {'id': 'S8', 'pertanyaan': 'Saya yakin mampu mendengarkan keluhan dan memberikan empati pada pengguna yang mengalami kendala'},
  {'id': 'S9', 'pertanyaan': 'Saya percaya diri bisa menjadi penghubung antara kebutuhan bisnis dan solusi teknologi yang ramah pengguna'},
  {'id': 'S10', 'pertanyaan': 'Saya suka memotivasi dan mendorong anggota tim untuk berkolaborasi dan mencapai tujuan bersama'},
  {'id': 'S11', 'pertanyaan': 'Saya tertarik membantu orang lain mengembangkan potensi dan keterampilan mereka'},
  {'id': 'S12', 'pertanyaan': 'Saya senang berinteraksi dan membangun hubungan yang baik dengan berbagai macam orang'},
  {'id': 'E1', 'pertanyaan': 'Saya senang memimpin tim dan mengambil keputusan penting dalam proyek teknologi atau bisnis digital'},
  {'id': 'E2', 'pertanyaan': 'Saya tertarik merancang strategi pemasaran digital untuk meningkatkan penjualan dan pertumbuhan perusahaan'},
  {'id': 'E3', 'pertanyaan': 'Saya suka bernegosiasi dan meyakinkan klien atau partner untuk bekerja sama dalam proyek digital'},
  {'id': 'E4', 'pertanyaan': 'Saya merasa termotivasi untuk meluncurkan produk atau layanan digital baru ke pasar'},
  {'id': 'E5', 'pertanyaan': 'Saya senang mengelola kampanye iklan online dan mengoptimalkan anggaran untuk hasil maksimal'},
  {'id': 'E6', 'pertanyaan': 'Saya tertarik mempresentasikan ide bisnis atau solusi teknologi kepada calon investor atau klien'},
  {'id': 'E7', 'pertanyaan': 'Saya yakin bisa mengidentifikasi peluang pasar baru dan merancang strategi untuk merebutnya'},
  {'id': 'E8', 'pertanyaan': 'Saya yakin mampu mengarahkan jalannya rapat dan memastikan tujuan diskusi tercapai'},
  {'id': 'E9', 'pertanyaan': 'Saya percaya diri bisa mengelola proyek e-commerce atau platform penjualan online'},
  {'id': 'E10', 'pertanyaan': 'Saya suka mengambil inisiatif untuk memulai proyek atau program baru yang berdampak luas'},
  {'id': 'E11', 'pertanyaan': 'Saya tertarik membangun dan mengembangkan bisnis atau startup saya sendiri'},
  {'id': 'E12', 'pertanyaan': 'Saya senang menetapkan target yang ambisius dan memotivasi tim untuk mencapainya'},
  {'id': 'C1', 'pertanyaan': 'Saya senang mengatur dan memelihara database agar data tersusun rapi, akurat, dan mudah dicari'},
  {'id': 'C2', 'pertanyaan': 'Saya tertarik membuat dan mengikuti prosedur standar (SOP) untuk memastikan kualitas operasi digital'},
  {'id': 'C3', 'pertanyaan': 'Saya suka memeriksa ulang kode program, dokumen, atau data untuk memastikan tidak ada kesalahan'},
  {'id': 'C4', 'pertanyaan': 'Saya merasa tenang ketika bekerja dengan sistem pengarsipan digital atau manajemen dokumen yang terstruktur'},
  {'id': 'C5', 'pertanyaan': 'Saya senang melakukan audit atau pengecekan kepatuhan terhadap standar keamanan informasi'},
  {'id': 'C6', 'pertanyaan': 'Saya tertarik menyusun laporan keuangan, metrik, atau data operasional secara sistematis dan detail'},
  {'id': 'C7', 'pertanyaan': 'Saya yakin bisa mengelola inventaris, jadwal, atau sumber daya proyek digital menggunakan tools manajemen'},
  {'id': 'C8', 'pertanyaan': 'Saya percaya diri dapat memantau dan mencatat aktivitas log sistem untuk keperluan tracking dan keamanan'},
  {'id': 'C9', 'pertanyaan': 'Saya yakin mampu memastikan semua proses transaksi atau administrasi digital berjalan sesuai aturan'},
  {'id': 'C10', 'pertanyaan': 'Saya suka merapikan, mengkategorikan, dan mengatur informasi agar mudah diakses dan dipahami'},
  {'id': 'C11', 'pertanyaan': 'Saya tertarik membuat jadwal dan rencana kerja yang detail untuk memastikan semua tugas selesai tepat waktu'},
  {'id': 'C12', 'pertanyaan': 'Saya senang bekerja dengan angka dan data yang membutuhkan ketelitian dan akurasi tinggi'}
]

conn = psycopg2.connect("postgresql://user:password@db:5432/features")
cur = conn.cursor()

for q in mockRiasecQuestions:
    q_id = q['id']
    q_type = q_id[0]
    q_text = q['pertanyaan']
    cur.execute(
        "INSERT INTO riasec_questions (question_id, riasec_type, question_text) VALUES (%s, %s, %s) ON CONFLICT (question_id) DO UPDATE SET question_text = EXCLUDED.question_text",
        (q_id, q_type, q_text)
    )

conn.commit()
cur.close()
conn.close()
print("Success seeding 72 questions!")

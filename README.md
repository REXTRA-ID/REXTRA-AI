# REXTRA-AI: The Intelligence Layer

**REXTRA-AI** adalah *core engine* berbasis AI yang mengelola seluruh logika penalaran (*reasoning*) dan pemetaan karier digital dalam ekosistem REXTRA. Dibangun menggunakan **FastAPI**, *service* ini dirancang khusus untuk menangani komputasi berat, orkestrasi LLM (Large Language Models), dan algoritma kecocokan karier yang kompleks.

Service ini bekerja secara hibrida berdampingan dengan Core Backend (Golang) yang menangani manajemen user dan transaksi non-AI.

## 🏗 System Architecture & Directory Mapping

Struktur proyek ini mengacu pada pola *Domain-Driven Design* (DDD) yang dimodifikasi untuk skalabilitas fitur AI.

| Folder / File | Fungsi & Deskripsi |
| :--- | :--- |
| `app/api/v1/features/` | **Domain Hub.** Tempat seluruh sub-fitur AI (seperti Career Profile) berada. |
| `app/prompts/` | **Prompt Registry.** Manajemen instruksi LLM terpusat menggunakan YAML (terpisah dari kode). |
| `app/shared/ai/` | **AI Infrastructure.** Base class dan Prompt Manager untuk standarisasi pemanggilan LLM. |
| `app/shared/` | **Shared Modules.** Utilitas global seperti Caching (Redis), Database Client, dan Response Builder. |
| `app/core/` | **Global Config.** Pengaturan environment, logging, dan sistem keamanan (JWT/Otorisasi). |
| `app/models/` | **Relational Schemas.** Definisi tabel database PostgreSQL terkait metadata profesi. |
| `docker/` | **Containerization.** Konfigurasi environment-specific (Dev/Prod) Dockerfile. |
| `alembic/` | **Database Migrations.** Log perubahan skema database secara kronologis. |
| `Makefile` | **Command Orchestrator.** Shortcut standar untuk menjalankan, migrasi, dan testing proyek. |

## 🚀 AI Feature Roadmap & Progress

Status pengembangan fitur AI pada branch `feature/kenali-diri`:

| Fitur | Sub-Fitur | Status | Deskripsi Teknis |
| :--- | :--- | :--- | :--- |
| **Career Profile** | RIASEC Engine | ✅ Done | Kalkulasi 6 tipe kepribadian berbasis algoritma Holland. |
| | Career Expansion | ✅ Done | Ekspansi 5 profesi kandidat menggunakan 4-tier matching logic. |
| | Ikigai Scoring | ✅ Done | Parallel batch scoring menggunakan Gemini (semantic matching). |
| | Final Narrative | ✅ Done | Generasi narasi personalisasi hasil rekomendasi via AI. |
| **Interview Lab** | Mock Interview | ⏳ Backlog | Simulasi wawancara adaptif berdasarkan profil karier user. |
| **CV Analyzer** | Skill Gap Analysis | ⏳ Backlog | Analisis kecocokan CV dengan target profesi digital. |

## 🛠 Branching Strategy

Proyek ini mengikuti standar *Git Flow* untuk menjaga stabilitas produksi:

*   **`main`**: Branch produksi. Hanya berisi kode yang sudah *stable* dan siap di-deploy ke lingkungan *Live*.
*   **`dev`**: Branch integrasi. Tempat penggabungan fitur-fitur baru sebelum masuk ke tahap *Staging*.
*   **`feature/*`**: Branch granular untuk pengembangan fitur spesifik. Harus di-merge ke `dev` melalui *Pull Request*.

## 📝 Revision & Updates

| Tanggal | Versi | Perubahan Utama | Author |
| :--- | :--- | :--- | :--- |
| 15-03-2026 | v1.0.0 | Initial release: Refactoring Career Profile & Rebranding REXTRA-AI. | REXTRA-Team |
| 15-03-2026 | v1.1.0 | Implementasi Prompt Management (YAML) & Base AI Service. | REXTRA-Team |
| 15-03-2026 | v1.2.0 | Migrasi Docker structure (Dev/Prod) & Makefile integration. | REXTRA-Team |

## ⚙️ Quick Start

Gunakan `Makefile` untuk mempercepat setup lingkungan:

```bash
# Setup environment development (Docker)
make build-docker ENV=dev

# Jalankan migrasi database di dalam container
make docker-migrate ENV=dev

# Jalankan seeder data profesi & RIASEC
make docker-seeder ENV=dev
```

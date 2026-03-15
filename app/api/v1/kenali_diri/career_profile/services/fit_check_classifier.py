RIASEC_DISTANCE = {
    ("R","R"):0, ("R","I"):1, ("R","A"):2, ("R","S"):3, ("R","E"):2, ("R","C"):1,
    ("I","R"):1, ("I","I"):0, ("I","A"):1, ("I","S"):2, ("I","E"):3, ("I","C"):2,
    ("A","R"):2, ("A","I"):1, ("A","A"):0, ("A","S"):1, ("A","E"):2, ("A","C"):3,
    ("S","R"):3, ("S","I"):2, ("S","A"):1, ("S","S"):0, ("S","E"):1, ("S","C"):2,
    ("E","R"):2, ("E","I"):3, ("E","A"):2, ("E","S"):1, ("E","E"):0, ("E","C"):1,
    ("C","R"):1, ("C","I"):2, ("C","A"):3, ("C","S"):2, ("C","E"):1, ("C","C"):0,
}

def calculate_match_score(user_code: str, profession_code: str) -> float:
    """
    Skor 0.0-1.0 berdasarkan rata-rata kedekatan huruf.
    1.0 = identik, 0.0 = semua berlawanan.
    Hanya untuk transparansi - tidak digunakan untuk klasifikasi utama.
    """
    max_distance = 3  # jarak maksimum di heksagon
    total_distance = 0
    comparisons = 0

    # Pastikan membandingkan sampai panjang minimum dari kedua kode
    for i in range(min(len(user_code), len(profession_code))):
        dist = RIASEC_DISTANCE.get((user_code[i], profession_code[i]), max_distance)
        total_distance += dist
        comparisons += 1

    if comparisons == 0:
        return 0.5
    avg_distance = total_distance / comparisons
    return round(1.0 - (avg_distance / max_distance), 2)


def classify_fit_check(
    user_riasec_code: str,
    profession_riasec_code: str
) -> dict:
    """
    Rule-based classification untuk FIT_CHECK.
    Return dict yang siap di-INSERT ke fit_check_results.

    Hierarki klasifikasi:
    HIGH   = dominant_same AND composition_same (semua huruf sama, urutan boleh beda)
    MEDIUM = dominant_same tapi composition berbeda  (rule: dominant_same)
             ATAU dominant adjacent (jarak 1 di heksagon)    (rule: adjacent_dominant)
    LOW    = fallback - semua kondisi di atas tidak terpenuhi (rule: mismatch)
    """
    if not user_riasec_code or not profession_riasec_code:
        return {
            "match_category": "LOW",
            "rule_type": "mismatch",
            "dominant_letter_same": False,
            "is_adjacent_hexagon": False,
            "match_score": 0.0
        }

    user_dominant = user_riasec_code[0]
    prof_dominant = profession_riasec_code[0]

    dominant_same = (user_dominant == prof_dominant)
    composition_same = sorted(user_riasec_code) == sorted(profession_riasec_code)

    dominant_distance = RIASEC_DISTANCE.get((user_dominant, prof_dominant), 3)
    is_adjacent = dominant_distance <= 1

    match_score = calculate_match_score(user_riasec_code, profession_riasec_code)

    # === CEK HIGH: dominant_same AND composition_same ===
    if dominant_same and composition_same:
        rule_type = "exact_match" if user_riasec_code == profession_riasec_code else "permutation_match"
        return {
            "match_category": "HIGH",
            "rule_type": rule_type,
            "dominant_letter_same": True,
            "is_adjacent_hexagon": is_adjacent,
            "match_score": match_score
        }

    # === CEK MEDIUM: Kondisi A - dominant_same tapi composition berbeda ===
    if dominant_same:
        return {
            "match_category": "MEDIUM",
            "rule_type": "dominant_same",
            "dominant_letter_same": True,
            "is_adjacent_hexagon": is_adjacent,
            "match_score": match_score
        }

    # === CEK MEDIUM: Kondisi B - dominant adjacent (jarak 1 di heksagon) ===
    if dominant_distance == 1:
        return {
            "match_category": "MEDIUM",
            "rule_type": "adjacent_dominant",
            "dominant_letter_same": False,
            "is_adjacent_hexagon": True,
            "match_score": match_score
        }

    # === PERBAIKAN TEMUAN 1: CEK MEDIUM Kondisi C — tidak ada pasangan berlawanan ===
    has_opposite = any(
        RIASEC_DISTANCE.get((user_riasec_code[i], profession_riasec_code[i]), 0) >= 3
        for i in range(min(len(user_riasec_code), len(profession_riasec_code)))
    )
    if not has_opposite:
        return {
            "match_category": "MEDIUM",
            "rule_type": "close_profile",
            "dominant_letter_same": False,
            "is_adjacent_hexagon": is_adjacent,
            "match_score": match_score,
        }

    # === FALLBACK: LOW ===
    return {
        "match_category": "LOW",
        "rule_type": "mismatch",
        "dominant_letter_same": dominant_same,
        "is_adjacent_hexagon": is_adjacent,
        "match_score": match_score
    }


def build_fit_check_explanation(
    fit_result: dict,
    user_code: str,
    profession_code: str,
) -> dict:
    """
    Generate teks penjelasan dinamis dari data fit_check_results.
    Tidak menggunakan AI — semua berbasis rule.
    Copywriting mengikuti template spesifikasi UI per kondisi.
    """
    category  = fit_result["match_category"]
    rule_type = fit_result["rule_type"]

    user_dominant = user_code[0] if user_code else "?"
    prof_dominant = profession_code[0] if profession_code else "?"
    user_set_str  = ", ".join(sorted(user_code))  # misal "C, I, R"

    MATCH_LABELS = {
        "HIGH":   "Kecocokan Tinggi",
        "MEDIUM": "Kecocokan Sedang",
        "LOW":    "Kecocokan Rendah",
    }
    MATCH_STARS = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

    if category == "HIGH":
        if rule_type == "exact_match":
            reason_points = [
                f"Profil karier berkode {user_code} dan profesi ini juga berkode {profession_code}.",
                f"Kode identik menunjukkan keselarasan penuh — minat utama ({user_dominant}) "
                f"dan seluruh pola aktivitas kerja berada pada spektrum yang sama.",
            ]
        else:  # permutation_match
            reason_points = [
                f"Profil karier berkode {user_code} dan profesi ini berkode {profession_code}.",
                f"Huruf dominan sama ({user_dominant}) dan komposisi tiga huruf identik "
                f"({user_set_str}), sehingga menunjukkan keselarasan minat utama dan pendukung.",
            ]
        meaning = (
            "Kecocokan Tinggi menunjukkan bahwa minat dominan dan minat pendukung selaras "
            "dengan karakter utama profesi. Hal ini menandakan tingkat kesesuaian yang kuat "
            "antara profil karier dan aktivitas kerja yang dituntut profesi tersebut."
        )
        implication   = "Profesi ini layak diprioritaskan sebagai tujuan pengembangan."
        next_steps    = [
            "Perkuat kompetensi inti yang dibutuhkan profesi.",
            "Bangun pengalaman melalui proyek, magang, atau portofolio.",
            "Susun rencana pengembangan yang terarah.",
        ]
        cta_primary   = "Buat Rencana"
        cta_secondary = None

    elif category == "MEDIUM":
        if rule_type == "dominant_same":
            user_set  = set(user_code)
            prof_set  = set(profession_code)
            diff_user = user_set - prof_set
            diff_prof = prof_set - user_set
            diff_str  = ""
            if diff_user and diff_prof:
                diff_str = (
                    f" Huruf {', '.join(sorted(diff_user))} pada profil "
                    f"digantikan {', '.join(sorted(diff_prof))} pada profesi."
                )
            reason_points = [
                f"Profil berkode {user_code}, sedangkan profesi ini berkode {profession_code}.",
                (
                    f"Huruf dominan sama ({user_dominant}), namun salah satu komponen minat "
                    f"pendukung berbeda.{diff_str} Hal ini menunjukkan arah minat utama sejalan, "
                    f"tetapi beberapa karakter tugas mungkin memerlukan adaptasi."
                ),
            ]
        elif rule_type == "adjacent_dominant":
            reason_points = [
                f"Profil berkode {user_code}, sedangkan profesi ini berkode {profession_code}.",
                (
                    f"Huruf dominan berbeda ({user_dominant} pada profil, {prof_dominant} pada profesi) "
                    f"namun keduanya bertetangga dalam model RIASEC. "
                    f"Hal ini menunjukkan kedekatan minat meski orientasi aktivitas tidak sepenuhnya identik."
                ),
            ]
        else:  # close_profile
            reason_points = [
                f"Profil berkode {user_code}, sedangkan profesi ini berkode {profession_code}.",
                (
                    f"Meski huruf dominan berbeda ({user_dominant} vs {prof_dominant}), "
                    f"tidak ada pasangan minat yang berlawanan secara langsung dalam model RIASEC. "
                    f"Hal ini menunjukkan profil yang masih cukup berdekatan secara keseluruhan."
                ),
            ]
        meaning = (
            "Kecocokan Sedang menunjukkan adanya keselarasan pada sebagian komponen minat, "
            "namun terdapat perbedaan pada dominansi atau minat pendukung. "
            "Profesi masih relevan, tetapi memerlukan penyesuaian."
        )
        implication   = "Profesi ini tetap dapat dipertimbangkan dengan strategi penguatan yang tepat."
        next_steps    = [
            "Identifikasi komponen minat yang berbeda.",
            "Susun strategi adaptasi pada aspek tersebut.",
            "Bandingkan dengan profesi lain yang lebih selaras.",
        ]
        cta_primary   = "Lihat Rekomendasi"
        cta_secondary = "Strategi Adaptasi"

    else:  # LOW
        reason_points = [
            f"Profil berkode {user_code}, sedangkan profesi ini berkode {profession_code}.",
            (
                f"Huruf dominan berbeda ({user_dominant} pada profil, {prof_dominant} pada profesi) "
                f"dan tidak berada pada posisi bertetangga dalam model RIASEC, "
                f"sehingga arah minat utamanya tidak sejalan."
            ),
        ]
        meaning = (
            "Kecocokan Rendah menunjukkan bahwa minat dominan profil karier berbeda "
            "dan tidak berada pada spektrum yang berdekatan dengan karakter utama profesi. "
            "Tingkat keselarasan relatif rendah."
        )
        implication = (
            "Profesi ini tetap dapat dipilih, tetapi biasanya memerlukan adaptasi "
            "yang lebih besar dan pertimbangan yang lebih matang."
        )
        next_steps    = [
            "Tinjau kembali alasan memilih profesi ini.",
            "Eksplorasi profesi lain yang lebih selaras dengan profil karier.",
            "Jika tetap memilih profesi ini, siapkan strategi adaptasi yang lebih intens.",
        ]
        cta_primary   = "Cari Alternatif"
        cta_secondary = "Tetap Lanjut"

    return {
        "meaning":       meaning,
        "reason_points": reason_points,
        "implication":   implication,
        "next_steps":    next_steps,
        "cta_primary":   cta_primary,
        "cta_secondary": cta_secondary,
        "match_label":   MATCH_LABELS[category],
        "match_stars":   MATCH_STARS[category],
    }

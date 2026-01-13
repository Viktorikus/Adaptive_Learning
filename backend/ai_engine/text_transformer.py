from backend.utils.text_cleaner import clean_text
from backend.ai_engine.nlp.preprocessing import tokenize_text
from backend.services.analysis_service import (
    is_spltv_question,
    extract_spltv_coefficients
)
from backend.utils.json_helper import build_response
import re

def is_spltv_question(text: str) -> bool:
    """
    Validasi SPLTV yang benar secara matematis
    """

    equations = [eq.strip() for eq in text.split(",")]
    if len(equations) != 3:
        return False

    variables_found = set()

    for eq in equations:
        # pastikan ada '='
        if "=" not in eq:
            return False

        # cari variabel yang muncul
        vars_in_eq = re.findall(r"[xyz]", eq)
        variables_found.update(vars_in_eq)

    # SPLTV HARUS x, y, z (tidak harus di setiap persamaan)
    return variables_found == {"x", "y", "z"}

def transform_spltv_text(soal_text: str, konteks: str = "umum"):
    """
    Transformasi teks soal SPLTV ke konteks tertentu (teks saja)
    Fokus: menjaga struktur matematis SPLTV
    """

    # 1. Validasi input kosong
    if not soal_text or not soal_text.strip():
        return build_response(
            success=False,
            message="Teks soal kosong"
        )

    # 2. Cleaning teks dasar
    cleaned_text = clean_text(soal_text)

    # 3. Normalisasi SPLTV (PENTING: hapus 0x, 0y, 0z)
    equations = [eq.strip() for eq in cleaned_text.split(",")]
    equations = [normalize_equation(eq) for eq in equations]
    normalized_text = ", ".join(equations)

    # 4. Validasi SPLTV (SETELAH normalisasi)
    if not is_spltv_question(normalized_text):
        return build_response(
            success=False,
            message="Soal bukan termasuk SPLTV"
        )

    # 5. Tokenisasi (untuk AI adaptif / NLP)
    tokens = tokenize_text(normalized_text)

    # 6. Ekstraksi koefisien SPLTV
    coefficients = extract_spltv_coefficients(normalized_text)
    if not coefficients:
        return build_response(
            success=False,
            message="Gagal mengekstraksi koefisien SPLTV"
        )

    # 7. Transformasi konteks (narasi saja, tidak mengubah matematika)
    transformed_text = apply_context_transformation(normalized_text, konteks)

    return build_response(
        success=True,
        materi="SPLTV",
        konteks=konteks,
        original_soal=soal_text,
        cleaned_soal=normalized_text,
        transformed_soal=transformed_text,
        coefficients=coefficients
    )



def apply_context_transformation(text: str, konteks: str):
    """
    Aturan transformasi konteks teks SPLTV
    Hanya mengubah narasi, tidak menyentuh persamaan matematika
    """

    context_rules = {
        "game": {
            "pedagang": "pemain game",
            "harga": "poin",
            "uang": "poin",
            "membeli": "mengumpulkan",
            "barang": "item"
        },
        "olahraga": {
            "pedagang": "pelatih",
            "membeli": "mengatur",
            "barang": "latihan",
            "harga": "durasi",
            "uang": "waktu"
        }
    }

    rules = context_rules.get(konteks, {})

    for old_word, new_word in rules.items():
        text = text.replace(old_word, new_word)

    return text

def analyze_spltv_error(evaluation_detail):
    """
    Analisis kesalahan jawaban SPLTV siswa
    Berbasis rule sederhana (NLP simbolik)
    """

    incorrect = [d for d in evaluation_detail if not d["hasil"]]

    if not incorrect:
        return {
            "error_type": "none",
            "message": "Jawaban benar"
        }

    if len(incorrect) == len(evaluation_detail):
        return {
            "error_type": "conceptual",
            "message": "Kesalahan konsep SPLTV"
        }

    return {
        "error_type": "partial",
        "message": "Sebagian persamaan belum terpenuhi"
    }

def normalize_equation(eq: str):
    """
    Menghapus variabel dengan koefisien 0 agar parser SPLTV stabil
    """
    return (
        eq.replace("+ 0x", "")
          .replace("+ 0y", "")
          .replace("+ 0z", "")
          .replace("- 0x", "")
          .replace("- 0y", "")
          .replace("- 0z", "")
          .replace("  ", " ")
          .strip()
    )
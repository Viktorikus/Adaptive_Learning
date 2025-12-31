import nltk
from nltk.tokenize import word_tokenize

# Pastikan tokenizer tersedia
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


def classify_spltv_error(evaluation):
    """
    evaluation: dict hasil evaluasi SPLTV
    """

    if not evaluation or "detail" not in evaluation:
        return {
            "error_type": "unknown",
            "feedback": "Data evaluasi tidak valid"
        }

    details = evaluation["detail"]

    # -----------------------------
    # CASE 1: detail berbentuk dict
    # contoh:
    # {
    #   "x": "Benar",
    #   "y": "Salah ...",
    #   "z": "Salah ..."
    # }
    # -----------------------------
    if isinstance(details, dict):
        wrong_eq = sum(
            1 for v in details.values()
            if isinstance(v, str) and not v.lower().startswith("benar")
        )
        total = len(details)

    # -----------------------------
    # CASE 2: detail berbentuk list
    # contoh:
    # [
    #   {"hasil": True, ...},
    #   {"hasil": False, ...}
    # ]
    # -----------------------------
    elif isinstance(details, list):
        wrong_eq = sum(
            1 for d in details
            if isinstance(d, dict) and not d.get("hasil", False)
        )
        total = len(details)

    else:
        return {
            "error_type": "invalid_format",
            "feedback": "Format detail evaluasi tidak dikenali"
        }

    # -----------------------------
    # KLASIFIKASI ERROR
    # -----------------------------
    if wrong_eq == 0:
        return {
            "error_type": "no_error",
            "label": "mastery",
            "feedback": "Jawaban benar. Siswa menguasai SPLTV."
        }

    elif wrong_eq == total:
        return {
            "error_type": "conceptual_error",
            "label": "kesalahan_konsep",
            "feedback": "Semua persamaan salah. Perlu penguatan konsep SPLTV."
        }

    else:
        return {
            "error_type": "procedural_error",
            "label": "kesalahan_prosedural",
            "feedback": "Sebagian persamaan salah. Periksa langkah perhitungan."
        }

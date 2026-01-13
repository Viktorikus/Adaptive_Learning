import random

CONTEXT_TEMPLATES = {
    "game": {
        "variables": ["gold", "diamond", "energy"],
        "story": (
            "Seorang pemain game memiliki {v1}, {v2}, dan {v3}. "
            "Kombinasi item tersebut memenuhi persamaan berikut:"
        )
    },
    "olahraga": {
        "variables": ["lari", "push_up", "sit_up"],
        "story": (
            "Seorang atlet melakukan latihan {v1}, {v2}, dan {v3}. "
            "Jumlah latihan tersebut dinyatakan dalam sistem persamaan berikut:"
        )
    },
    "musik": {
        "variables": ["lagu_pop", "lagu_rock", "lagu_jazz"],
        "story": (
            "Seorang DJ memutar {v1}, {v2}, dan {v3}. "
            "Total durasi lagu memenuhi sistem persamaan berikut:"
        )
    },
    "umum": {
        "variables": ["x", "y", "z"],
        "story": "Diketahui sistem persamaan linear tiga variabel berikut:"
    }
}


def contextualize_spltv(soal_math: str, minat: str = "umum"):
    """
    Mengubah soal SPLTV matematis menjadi soal cerita sesuai minat siswa
    """

    context = CONTEXT_TEMPLATES.get(minat, CONTEXT_TEMPLATES["umum"])

    v1, v2, v3 = context["variables"]

    story = context["story"].format(v1=v1, v2=v2, v3=v3)

    soal_contextual = f"{story}\n{soal_math}"

    return {
        "minat": minat,
        "soal": soal_contextual,
        "variabel": [v1, v2, v3]
    }

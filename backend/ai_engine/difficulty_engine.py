def decide_difficulty(next_stage: str):
    """
    Menentukan tingkat kesulitan soal berdasarkan learning stage (hasil BFS)
    """

    if next_stage in ["review_konsep", "latihan_dasar"]:
        return {
            "difficulty": "easy",
            "reason": "Fokus penguatan konsep dasar"
        }

    if next_stage == "latihan_menengah":
        return {
            "difficulty": "medium",
            "reason": "Penguatan keterampilan prosedural"
        }

    if next_stage == "latihan_lanjutan":
        return {
            "difficulty": "hard",
            "reason": "Siswa siap tantangan lebih tinggi"
        }

    return {
        "difficulty": "medium",
        "reason": "Default difficulty"
    }

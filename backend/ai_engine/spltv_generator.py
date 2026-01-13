import random
import numpy as np

def generate_spltv_question(difficulty: str, stage: str):
    """
    Generate soal SPLTV berdasarkan difficulty dan stage
    """

    # Tentukan range koefisien berdasarkan stage
    if stage == "review_konsep":
        coef_range = (-3, 3)
        solution_range = (1, 5)

    elif stage == "latihan_dasar":
        coef_range = (-5, 5)
        solution_range = (1, 7)

    elif stage == "latihan_menengah":
        coef_range = (-7, 7)
        solution_range = (1, 10)

    elif stage == "latihan_lanjutan":
        coef_range = (-10, 10)
        solution_range = (2, 15)

    else:
        coef_range = (-5, 5)
        solution_range = (1, 7)

    # Tentukan solusi terlebih dahulu
    x = random.randint(*solution_range)
    y = random.randint(*solution_range)
    z = random.randint(*solution_range)

    solution = {"x": x, "y": y, "z": z}

    equations = []

    for _ in range(3):
        a = random.randint(*coef_range)
        b = random.randint(*coef_range)
        c = random.randint(*coef_range)

        const = a*x + b*y + c*z

        eq = f"{a}x + {b}y + {c}z = {const}"
        equations.append(eq)

    return {
        "stage": stage,
        "difficulty": difficulty,
        "soal": ", ".join(equations),
        "kunci_jawaban": solution
    }

import random

def generate_spltv_question(difficulty="medium"):
    """
    Generate soal SPLTV berdasarkan difficulty
    """

    if difficulty == "easy":
        coef_range = (1, 5)
        sol_range = (1, 5)

    elif difficulty == "hard":
        coef_range = (-10, 10)
        sol_range = (-5, 5)

    else:  # medium
        coef_range = (-7, 7)
        sol_range = (1, 7)

    # solusi sebenarnya
    x = random.randint(*sol_range)
    y = random.randint(*sol_range)
    z = random.randint(*sol_range)

    # koefisien
    def rand_coef():
        c = 0
        while c == 0:
            c = random.randint(*coef_range)
        return c

    a1, b1, c1 = rand_coef(), rand_coef(), rand_coef()
    a2, b2, c2 = rand_coef(), rand_coef(), rand_coef()
    a3, b3, c3 = rand_coef(), rand_coef(), rand_coef()

    d1 = a1*x + b1*y + c1*z
    d2 = a2*x + b2*y + c2*z
    d3 = a3*x + b3*y + c3*z

    soal = (
        f"{a1}x + {b1}y + {c1}z = {d1}, "
        f"{a2}x + {b2}y + {c2}z = {d2}, "
        f"{a3}x + {b3}y + {c3}z = {d3}"
    )

    return {
        "soal": soal,
        "difficulty": difficulty,
        "kunci_jawaban": {"x": x, "y": y, "z": z}
    }

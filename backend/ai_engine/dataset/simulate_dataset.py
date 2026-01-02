import random
import pandas as pd

ERROR_TYPES = [
    "no_error",
    "procedural_error",
    "conceptual_error"
]

ACTIONS = {
    "no_error": "naik_level",
    "procedural_error": "latihan_lagi",
    "conceptual_error": "remedial"
}

def simulate_student_case():
    """
    Simulasi 1 kondisi siswa
    """
    error_type = random.choice(ERROR_TYPES,
                               weights=[0.3, 0.4, 0.3],
                               k=1)[0]  # bobot distribusi

    if error_type == "no_error":
        wrong_count = random.choice([0,0,1])
        score = random.randint(80, 100)

    elif error_type == "procedural_error":
        wrong_count = random.choice([1, 2])
        score = random.randint(40, 79)

    else:  # conceptual_error
        wrong_count = random.choice([2,3])
        score = random.randint(0, 40)

    return {
        "score": score,
        "wrong_count": wrong_count,
        "error_type": error_type,
        "next_action": ACTIONS[error_type]
    }


def generate_dataset(n_samples=300):
    data = []
    per_class = n_samples // 3

    for error_type in ERROR_TYPES:
        for _ in range(per_class):
            if error_type == "no_error":
                wrong_count = 0
                score = random.randint(85, 100)

            elif error_type == "procedural_error":
                wrong_count = random.randint(1, 2)
                score = random.randint(40, 70)

            else:  # conceptual_error
                wrong_count = 3
                score = random.randint(0, 30)

            data.append({
                "score": score,
                "wrong_count": wrong_count,
                "error_type": error_type,
                "next_action": ACTIONS[error_type]
            })

    random.shuffle(data)
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_dataset(1000)   # perbanyak dataset
    df.to_csv("adaptive_dataset.csv", index=False)
    print("Dataset generated:", len(df))

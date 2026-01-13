from collections import defaultdict, deque

# In-memory student storage
_STUDENT_MEMORY = defaultdict(lambda: {
    "current_stage": "latihan_menengah",
    "history": deque(maxlen=10)  # simpan 10 interaksi terakhir
})


def get_student_profile(student_id: str):
    return _STUDENT_MEMORY[student_id]


def update_student_history(
    student_id: str,
    score: float,
    error_type: str,
    next_action: str,
    next_stage: str
):
    profile = _STUDENT_MEMORY[student_id]

    profile["history"].append({
        "score": score,
        "error_type": error_type,
        "next_action": next_action,
        "next_stage": next_stage
    })

    profile["current_stage"] = next_stage


def get_dominant_error(student_id: str):
    history = _STUDENT_MEMORY[student_id]["history"]

    if not history:
        return None

    counter = {}
    for h in history:
        et = h["error_type"]
        counter[et] = counter.get(et, 0) + 1

    return max(counter, key=counter.get)
def decide_difficulty(next_action, current_stage, dominant_error=None):
    """
    Menentukan difficulty berdasarkan aksi, stage, dan histori error
    """

    # Safety first
    if dominant_error == "conceptual_error":
        return {
            "difficulty": "easy",
            "reason": "Conceptual error detected"
        }

    if dominant_error == "procedural_error":
        return {
            "difficulty": "medium",
            "reason": "Procedural reinforcement"
        }

    # Mastery escalation
    if next_action == "naik_level":
        if current_stage == "latihan_lanjutan":
            return {
                "difficulty": "hard",
                "reason": "Mastery at advanced stage"
            }

        return {
            "difficulty": "medium",
            "reason": "Level up"
        }

    # Default fallback
    return {
        "difficulty": "medium",
        "reason": "Default difficulty"
    }

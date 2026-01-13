from collections import deque

LEARNING_GRAPH = {
    "review_konsep": ["latihan_dasar"],
    "latihan_dasar": ["latihan_menengah"],
    "latihan_menengah": ["latihan_lanjutan"],
    "latihan_lanjutan": []
}

def bfs_next_action(current_stage, target_stage, dominant_error=None):
    """
    BFS dengan pembatasan berdasarkan error dominan
    """

    # 🔒 Safety rule berbasis history
    if dominant_error == "conceptual_error":
        return "review_konsep"

    if dominant_error == "procedural_error" and current_stage == "latihan_menengah":
        return "latihan_menengah"

    # BFS normal (1-step)
    neighbors = LEARNING_GRAPH.get(current_stage, [])
    if target_stage in neighbors:
        return target_stage

    return current_stage
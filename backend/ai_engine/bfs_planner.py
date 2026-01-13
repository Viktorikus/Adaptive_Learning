from collections import deque

LEARNING_GRAPH = {
    "review_konsep": ["latihan_dasar"],
    "latihan_dasar": ["latihan_menengah"],
    "latihan_menengah": ["latihan_lanjutan"],
    "latihan_lanjutan": ["evaluasi"],
    "evaluasi": []
}

def bfs_next_action(start, target):
    """
    BFS untuk menentukan langkah belajar berikutnya
    """
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target:
            # Ambil langkah selanjutnya saja
            return path[1] if len(path) > 1 else node

        if node not in visited:
            visited.add(node)
            for neighbor in LEARNING_GRAPH.get(node, []):
                queue.append(path + [neighbor])

    return start

from backend.ai_engine.ml.model_loader import predict_next_action
from backend.ai_engine.text_transformer import transform_spltv_text
from backend.services.analysis_service import evaluate_spltv_answer
from backend.services.analysis_service import solve_spltv_numpy
from backend.ai_engine.nlp.literacy_classifier import classify_spltv_error
from backend.ai_engine.difficulty_engine import decide_difficulty
from backend.ai_engine.spltv_generator import generate_spltv_question
from backend.ai_engine.bfs_planner import bfs_next_action
from backend.ai_engine.spltv_contextualizer import contextualize_spltv
from backend.ai_engine.student_model.student_memory import (
    get_student_profile,
    update_student_history,
    get_dominant_error
)
# from backend.ai_engine.ml.random_forest import predict_learning_strategy

def solve_spltv_service(soal_text: str, konteks: str):
    """
    Service untuk menyelesaikan SPLTV
    """

    transform_result = transform_spltv_text(soal_text, konteks)

    if not transform_result.get("success"):
        return transform_result

    coefficients = transform_result.get("coefficients")

    solution = solve_spltv_numpy(coefficients)

    if not solution:
        return {
            "success": False,
            "message": "SPLTV tidak dapat diselesaikan"
        }

    return {
        "success": True,
        "materi": "SPLTV",
        "solution": solution
    }

def transform_soal_service(soal_text: str, konteks: str):
    """
    Service layer untuk transformasi soal SPLTV
    Menghubungkan route dengan AI engine
    """
    return transform_spltv_text(
        soal_text=soal_text,
        konteks=konteks
    )

def evaluate_soal_service(soal_text, konteks, student_answer):
    student_id = "student_001"  # sementara

    # === TRANSFORM SOAL ===
    transform_result = transform_spltv_text(soal_text, konteks)
    if not transform_result.get("success"):
        return transform_result

    coefficients = transform_result["coefficients"]

    # === EVALUASI ===
    evaluation = evaluate_spltv_answer(coefficients, student_answer)
    error_analysis = classify_spltv_error(evaluation)

    wrong_count = sum(
        1 for d in evaluation["detail"].values()
        if not d.lower().startswith("benar")
    )
    score = evaluation["score"]

    # === RANDOM FOREST ===
    adaptive_decision = predict_next_action(
        score=score,
        wrong_count=wrong_count,
        error_type=error_analysis["error_type"]
    )
    next_action = adaptive_decision["next_action"]

    # === STUDENT MEMORY ===
    profile = get_student_profile(student_id)
    current_stage = profile["current_stage"]
    dominant_error = get_dominant_error(student_id)

    # === ACTION → TARGET STAGE ===
    ACTION_TO_STAGE = {
        "naik_level": "latihan_lanjutan",
        "latihan_lagi": current_stage,
        "remedial": "review_konsep"
    }

    target_stage = ACTION_TO_STAGE.get(next_action, current_stage)

    # === BFS (LANGSUNG NEXT STAGE) ===
    next_stage = bfs_next_action(
        current_stage=current_stage,
        target_stage=target_stage,
        dominant_error=dominant_error
    )

    # === DIFFICULTY ===
    difficulty_decision = decide_difficulty(
        next_action=adaptive_decision["next_action"],
        current_stage=next_stage,
        dominant_error=dominant_error
    )

    # === GENERATE SOAL ===
    next_question = generate_spltv_question(
        stage=next_stage,
        difficulty=difficulty_decision["difficulty"]
    )

    # === UPDATE MEMORY ===
    update_student_history(
        student_id=student_id,
        score=score,
        error_type=error_analysis["error_type"],
        next_action=next_action,
        next_stage=next_stage
    )

    # === KONTEKSTUALISASI ===
    contextual_result = contextualize_spltv(
        soal_math=next_question["soal"],
        minat=konteks
    )

    return {
        "success": True,
        "materi": "SPLTV",

        "evaluation": evaluation,
        "error_analysis": error_analysis,

        "learning_strategy": {
            "rule_based": map_error_to_learning_strategy(error_analysis),
            "random_forest": adaptive_decision
        },

        "next_step": {
            "current_stage": current_stage,
            "target_stage": target_stage,
            "next_stage": next_stage,
            "difficulty_decision": difficulty_decision,

            "next_question": {
                "difficulty": difficulty_decision["difficulty"],
                "stage": next_stage,
                "soal_matematis": next_question["soal"],
                "soal_kontekstual": contextual_result["soal"],
                "kunci_jawaban": next_question["kunci_jawaban"],
                "minat": konteks,
                "variabel_konteks": contextual_result["variabel"]
            }
        }
    }

def map_error_to_learning_strategy(error_analysis: dict):
    """
    Mapping error_type ke strategi pembelajaran
    """

    error_type = error_analysis.get("error_type")

    if error_type == "no_error":
        return {
            "learning_strategy": "advanced_practice",
            "recommendation": "Berikan soal SPLTV dengan tingkat kesulitan lebih tinggi."
        }

    elif error_type == "procedural_error":
        return {
            "learning_strategy": "guided_practice",
            "recommendation": "Latihan SPLTV dengan panduan langkah-langkah penyelesaian."
        }

    elif error_type == "conceptual_error":
        return {
            "learning_strategy": "remedial_concept",
            "recommendation": "Penguatan konsep dasar SPLTV sebelum latihan lanjutan."
        }

    elif error_type == "invalid_format":
        return {
            "learning_strategy": "literacy_support",
            "recommendation": "Latihan memahami soal cerita dan pemodelan SPLTV."
        }

    return {
        "learning_strategy": "unknown",
        "recommendation": "Strategi pembelajaran belum tersedia."
    }


"""
Cognitive Score Calculator
Converts game performance metrics into clinical assessment scores
"""

def calculate_cognitive_scores(game_scores):
    """
    Convert game scores into clinical cognitive assessment features.
    
    Parameters:
    -----------
    game_scores : dict
        Dictionary with keys: "Memory", "Reaction", "TaskSwitch", "Pattern"
        Values are raw game scores (pairs matched, clicks, correct responses, rounds)
    
    Returns:
    --------
    dict : Cognitive assessment features matching model training data
    """
    
    cognitive_data = {}
    
    # Default values if games not played
    memory_score = game_scores.get("Memory", 0)  # 0-8 pairs
    reaction_score = game_scores.get("Reaction", 0)  # number of clicks
    task_switch_score = game_scores.get("TaskSwitch", 0)  # correct responses
    pattern_score = game_scores.get("Pattern", 0)  # rounds completed
    
    # Calculate MMSE (Mini-Mental State Examination): 0-30, higher is better
    # Based on combined performance across all games
    # Memory game: 0-10 points, Reaction: 0-7, Task switching: 0-8, Pattern: 0-5
    mmse_from_memory = min((memory_score / 8) * 10, 10)  # Max 10 points
    mmse_from_reaction = min((reaction_score / 50) * 7, 7)  # Max 7 points (50 clicks = excellent)
    mmse_from_task = min((task_switch_score / 40) * 8, 8)  # Max 8 points (40 correct = excellent)
    mmse_from_pattern = min(pattern_score, 5)  # Max 5 points (5 rounds = excellent)
    
    mmse_score = int(mmse_from_memory + mmse_from_reaction + mmse_from_task + mmse_from_pattern)
    cognitive_data["MMSE"] = max(0, min(30, mmse_score))  # Clamp to 0-30
    
    # Functional Assessment: 0-10, based on reaction time and task completion
    # Higher scores = better function
    functional_score = (
        min((reaction_score / 50) * 5, 5) +  # Reaction contributes 50%
        min((task_switch_score / 40) * 3, 3) +  # Task switching 30%
        min((pattern_score / 5) * 2, 2)  # Pattern recognition 20%
    )
    cognitive_data["FunctionalAssessment"] = int(max(0, min(10, functional_score)))
    
    # ADL (Activities of Daily Living): 0-10, based on task switching and overall performance
    # Higher scores = better ADL
    adl_score = (
        min((task_switch_score / 40) * 6, 6) +  # Task switching is key for ADL
        min((memory_score / 8) * 2, 2) +  # Memory helps
        min((pattern_score / 5) * 2, 2)  # Pattern recognition
    )
    cognitive_data["ADL"] = int(max(0, min(10, adl_score)))
    
    # Binary symptom flags (0 = No, 1 = Yes)
    # Thresholds indicate cognitive impairment if performance is below them
    
    # Memory Complaints & Forgetfulness: triggered if memory game score is low
    cognitive_data["MemoryComplaints"] = 1 if memory_score < 4 else 0  # <50% pairs matched
    cognitive_data["Forgetfulness"] = 1 if memory_score < 5 else 0  # <62.5% pairs matched
    
    # Confusion: triggered if task switching or reaction is poor
    confusion_indicator = (
        (task_switch_score < 20) or  # <50% correct on task switching
        (reaction_score < 25)  # <50 clicks in 30s (very slow)
    )
    cognitive_data["Confusion"] = 1 if confusion_indicator else 0
    
    # Disorientation: triggered if task switching is very poor (can't follow rules)
    cognitive_data["Disorientation"] = 1 if task_switch_score < 15 else 0  # <37.5% correct
    
    # Difficulty Completing Tasks: triggered if multiple games show poor performance
    poor_performance_count = sum([
        memory_score < 4,
        reaction_score < 30,
        task_switch_score < 20,
        pattern_score < 2
    ])
    cognitive_data["DifficultyCompletingTasks"] = 1 if poor_performance_count >= 2 else 0
    
    # Behavioral Problems: triggered if user didn't complete games (or scored 0)
    # This is a proxy - in real scenario you'd track game abandonment
    incomplete_games = sum([
        memory_score == 0,
        reaction_score == 0,
        task_switch_score == 0,
        pattern_score == 0
    ])
    cognitive_data["BehavioralProblems"] = 1 if incomplete_games >= 3 else 0
    
    # Personality Changes: Cannot infer from games alone
    # Default to 0, can be manually overridden if needed
    cognitive_data["PersonalityChanges"] = 0
    
    return cognitive_data


def get_cognitive_assessment_status(game_scores):
    """
    Check which cognitive assessments were inferred from games vs need manual input.
    
    Returns:
    --------
    dict : Status of each assessment source
    """
    games_played = sum([
        game_scores.get("Memory", 0) > 0,
        game_scores.get("Reaction", 0) > 0,
        game_scores.get("TaskSwitch", 0) > 0,
        game_scores.get("Pattern", 0) > 0
    ])
    
    return {
        "games_completed": games_played,
        "total_games": 4,
        "cognitive_scores_available": games_played > 0,
        "inferred_features": [
            "MMSE", "FunctionalAssessment", "ADL",
            "MemoryComplaints", "Forgetfulness", "Confusion",
            "Disorientation", "DifficultyCompletingTasks", "BehavioralProblems"
        ],
        "manual_features": ["PersonalityChanges"]  # Cannot infer from games
    }

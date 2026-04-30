from fastapi import HTTPException

# Define allowed transitions
VALID_TRANSITIONS = {
    "todo": ["in_progress"],
    "in_progress": ["review", "todo"],
    "review": ["done", "in_progress"],
    "done": []
}

def validate_transition(current_status: str, new_status: str):
    allowed = VALID_TRANSITIONS.get(current_status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition: '{current_status}' → '{new_status}'. "
                   f"Allowed: {allowed}"
        )
    return True
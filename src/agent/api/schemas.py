"""API schemas + tiny validation helpers."""


def validate_chat(payload: dict) -> tuple:
    message = (payload or {}).get("message")
    if not message or not isinstance(message, str):
        return None, "field 'message' (string) is required"
    return {"message": message}, None


def validate_run(payload: dict) -> tuple:
    goal = (payload or {}).get("goal")
    if not goal or not isinstance(goal, str):
        return None, "field 'goal' (string) is required"
    return {"goal": goal}, None

def decide_action(
    latest_message,
    requirements
):

    if requirements.get("off_topic"):
        return "REFUSE"
    
    if requirements.get("compare_request"):
        return "COMPARE"
    
    if not requirements.get("enough_information", False):
        return "CLARIFY"
    text = (latest_message or "").lower()

    if (
        "compare" in text
        or "difference" in text
        or "vs" in text
    ):
        return "COMPARE"

    if any(
        x in text
        for x in [
            "weather",
            "football",
            "cricket",
            "movie",
            "politics"
        ]
    ):
        return "REFUSE"

    return "RECOMMEND"
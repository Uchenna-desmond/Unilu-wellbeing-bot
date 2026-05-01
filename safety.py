
CRISIS_KEYWORDS = [
    "suicid", "kill myself", "end my life", "want to die", "better off dead",
    "hurt myself", "self-harm", "self harm", "no reason to live", "can't go on",
    "cannot go on", "nicht mehr leben", "umbringen", "sterben wollen"
]

CRISIS_MESSAGE = "IMMEDIATE SUPPORT: Die Dargebotene Hand 143"

def check_free_text(text: str) -> bool:
    lowered = text.lower()
    return any(kw in lowered for kw in CRISIS_KEYWORDS)

def check_phq9_q9(score: int) -> bool:
    return score >= 1

def escalate():
    print(CRISIS_MESSAGE)
    return True

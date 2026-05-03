
import json

OLBI_S_ITEMS = [
    {"text": "There are days when I feel tired before I arrive at school.", "reverse": False},
    {"text": "I can tolerate the pressure of my schoolwork very well.", "reverse": True},
    {"text": "After studying, I tend to need more time than in the past to relax and feel better.", "reverse": False},
    {"text": "I can endure the contents of my studies very well.", "reverse": True},
    {"text": "Lately, I tend to think less at school and do my work almost mechanically.", "reverse": False},
    {"text": "I find my studies to be a positive challenge.", "reverse": True},
    {"text": "During my studies, I often feel emotionally drained.", "reverse": False},
    {"text": "Over time, one can become detached from this type of study.", "reverse": False},
    {"text": "After studying I have enough energy for my leisure activities.", "reverse": True},
    {"text": "Sometimes I feel sickened by the subject matter of my studies.", "reverse": False},
    {"text": "When I study, I usually feel energised.", "reverse": True},
    {"text": "I have become less enthusiastic about my studies.", "reverse": False},
    {"text": "When working, I often feel worn out and weary.", "reverse": False},
    {"text": "I find the content of my studies stimulating.", "reverse": True},
    {"text": "In my studies, I have developed a cynical attitude.", "reverse": False},
    {"text": "I feel exhilarated when I accomplish something in my studies.", "reverse": True},
]

OLBI_ITEMS = [
    {"text": "There are days when I feel tired before I arrive at work.", "reverse": False},
    {"text": "I can tolerate the pressure of my work very well.", "reverse": True},
    {"text": "After work, I tend to need more time than in the past to relax and feel better.", "reverse": False},
    {"text": "I can endure the contents of my work very well.", "reverse": True},
    {"text": "Lately, I tend to think less at work and do my work almost mechanically.", "reverse": False},
    {"text": "I find my work to be a positive challenge.", "reverse": True},
    {"text": "During my work, I often feel emotionally drained.", "reverse": False},
    {"text": "Over time, one can become detached from this type of work.", "reverse": False},
    {"text": "After work I have enough energy for my leisure activities.", "reverse": True},
    {"text": "Sometimes I feel sickened by the subject matter of my work.", "reverse": False},
    {"text": "When I work, I usually feel energised.", "reverse": True},
    {"text": "I have become less enthusiastic about my work.", "reverse": False},
    {"text": "When working, I often feel worn out and weary.", "reverse": False},
    {"text": "I find the content of my work stimulating.", "reverse": True},
    {"text": "In my work, I have developed a cynical attitude.", "reverse": False},
    {"text": "I feel exhilarated when I accomplish something in my work.", "reverse": True},
]

PHQ9_ITEMS = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself - or that you are a failure",
    "Trouble concentrating on things",
    "Moving or speaking unusually slowly or being fidgety or restless",
    "Thoughts that you would be better off dead, or of hurting yourself",
]

GAD7_ITEMS = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid, as if something awful might happen",
]

def get_olbi_question(role, question_index, lang='en'):
    if lang == 'de':
        items = OLBI_S_ITEMS_DE if role == 'student' else OLBI_ITEMS_DE
    else:
        items = OLBI_S_ITEMS if role == 'student' else OLBI_ITEMS
    if question_index >= len(items):
        return {"error": "Index out of range"}
    return {
        "question_index": question_index,
        "total": len(items),
        "question": items[question_index]["text"],
        "scale": "1=Always  2=Often  3=Rarely  4=Never",
    }

def get_phq9_question(question_index, lang='en'):
    items = PHQ9_ITEMS_DE if lang == 'de' else PHQ9_ITEMS
    if question_index >= len(items):
        return {"error": "Index out of range"}
    return {
        "question_index": question_index,
        "total": len(PHQ9_ITEMS),
        "question": items[question_index],
        "scale": "0=Not at all  1=Several days  2=More than half the days  3=Nearly every day",
    }

def get_gad7_question(question_index, lang='en'):
    items = GAD7_ITEMS_DE if lang == 'de' else GAD7_ITEMS
    if question_index >= len(items):
        return {"error": "Index out of range"}
    return {
        "question_index": question_index,
        "total": len(GAD7_ITEMS),
        "question": items[question_index],
        "scale": "0=Not at all  1=Several days  2=More than half the days  3=Nearly every day",
    }

def score_burnout(role, answers):
    items = OLBI_S_ITEMS if role == "student" else OLBI_ITEMS
    exh_scores, dis_scores = [], []
    for i, item in enumerate(items):
        raw = answers[i]
        score = (5 - raw) if item["reverse"] else raw
        if i % 2 == 0:
            exh_scores.append(score)
        else:
            dis_scores.append(score)
    exhaustion = round(sum(exh_scores) / len(exh_scores), 2)
    disengagement = round(sum(dis_scores) / len(dis_scores), 2)
    exh_elevated = exhaustion >= 2.25
    dis_elevated = disengagement >= 2.10
    if exh_elevated and dis_elevated:
        level = "high"
    elif exh_elevated or dis_elevated:
        level = "moderate"
    else:
        level = "low"
    return {
        "exhaustion": exhaustion,
        "disengagement": disengagement,
        "exhaustion_elevated": exh_elevated,
        "disengagement_elevated": dis_elevated,
        "burnout_level": level,
    }

def score_phq9(answers):
    total = sum(answers)
    q9 = answers[8]
    if total <= 4: severity = "minimal"
    elif total <= 9: severity = "mild"
    elif total <= 14: severity = "moderate"
    elif total <= 19: severity = "moderately severe"
    else: severity = "severe"
    return {"total": total, "severity": severity, "crisis_flag": q9 >= 1, "q9_score": q9}

def score_gad7(answers):
    total = sum(answers)
    if total <= 4: severity = "minimal"
    elif total <= 9: severity = "mild"
    elif total <= 14: severity = "moderate"
    else: severity = "severe"
    return {"total": total, "severity": severity}

def dispatch(tool_name, tool_input, lang='en'):
    if tool_name == "get_olbi_question":
        result = get_olbi_question(tool_input["role"], tool_input["question_index"], lang)
    elif tool_name == "get_phq9_question":
        result = get_phq9_question(tool_input["question_index"], lang)
    elif tool_name == "get_gad7_question":
        result = get_gad7_question(tool_input["question_index"], lang)
    elif tool_name == "score_burnout":
        result = score_burnout(tool_input["role"], tool_input["answers"])
    elif tool_name == "score_phq9":
        result = score_phq9(tool_input["answers"])
    elif tool_name == "score_gad7":
        result = score_gad7(tool_input["answers"])
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result)

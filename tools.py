
import json

OLBI_S_ITEMS = [
    {"text": "There are days when I feel tired before I arrive at school.", "reverse": False},
    {"text": "I can tolerate the pressure of my schoolwork very well.", "reverse": True},
    {"text": "After studying, I tend to need more time than in the past to relax.", "reverse": False},
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
    {"text": "After work, I tend to need more time than in the past to relax.", "reverse": False},
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

OLBI_S_ITEMS_DE = [
    {"text": "Es gibt Tage, an denen ich mich muede fuehle, bevor ich in die Schule komme.", "reverse": False},
    {"text": "Ich kann den Druck meiner schulischen Arbeit sehr gut tolerieren.", "reverse": True},
    {"text": "Nach dem Lernen brauche ich mehr Zeit als frueher, um mich zu entspannen.", "reverse": False},
    {"text": "Ich kann die Inhalte meines Studiums sehr gut aushalten.", "reverse": True},
    {"text": "In letzter Zeit denke ich in der Schule weniger und erledige meine Arbeit fast mechanisch.", "reverse": False},
    {"text": "Ich empfinde mein Studium als positive Herausforderung.", "reverse": True},
    {"text": "Waehrend meines Studiums fuehle ich mich oft emotional erschoepft.", "reverse": False},
    {"text": "Im Laufe der Zeit kann man sich von diesem Studium distanzieren.", "reverse": False},
    {"text": "Nach dem Lernen habe ich genuegend Energie fuer meine Freizeitaktivitaeten.", "reverse": True},
    {"text": "Manchmal ekelt mich der Lernstoff meines Studiums an.", "reverse": False},
    {"text": "Wenn ich lerne, fuehle ich mich normalerweise energiegeladen.", "reverse": True},
    {"text": "Ich bin weniger begeistert von meinem Studium geworden.", "reverse": False},
    {"text": "Bei der Arbeit fuehle ich mich oft abgekaempft und muede.", "reverse": False},
    {"text": "Ich finde die Inhalte meines Studiums anregend.", "reverse": True},
    {"text": "In meinem Studium habe ich eine zynische Einstellung entwickelt.", "reverse": False},
    {"text": "Ich fuehle mich begeistert, wenn ich etwas in meinem Studium erreiche.", "reverse": True},
]

OLBI_ITEMS_DE = [
    {"text": "Es gibt Tage, an denen ich mich muede fuehle, bevor ich zur Arbeit komme.", "reverse": False},
    {"text": "Ich kann den Druck meiner Arbeit sehr gut tolerieren.", "reverse": True},
    {"text": "Nach der Arbeit brauche ich mehr Zeit als frueher, um mich zu entspannen.", "reverse": False},
    {"text": "Ich kann die Inhalte meiner Arbeit sehr gut aushalten.", "reverse": True},
    {"text": "In letzter Zeit denke ich bei der Arbeit weniger und erledige meine Aufgaben fast mechanisch.", "reverse": False},
    {"text": "Ich empfinde meine Arbeit als positive Herausforderung.", "reverse": True},
    {"text": "Waehrend meiner Arbeit fuehle ich mich oft emotional erschoepft.", "reverse": False},
    {"text": "Im Laufe der Zeit kann man sich von dieser Art von Arbeit distanzieren.", "reverse": False},
    {"text": "Nach der Arbeit habe ich genuegend Energie fuer meine Freizeitaktivitaeten.", "reverse": True},
    {"text": "Manchmal ekelt mich der Inhalt meiner Arbeit an.", "reverse": False},
    {"text": "Wenn ich arbeite, fuehle ich mich normalerweise energiegeladen.", "reverse": True},
    {"text": "Ich bin weniger begeistert von meiner Arbeit geworden.", "reverse": False},
    {"text": "Bei der Arbeit fuehle ich mich oft abgekaempft und muede.", "reverse": False},
    {"text": "Ich finde den Inhalt meiner Arbeit anregend.", "reverse": True},
    {"text": "In meiner Arbeit habe ich eine zynische Einstellung entwickelt.", "reverse": False},
    {"text": "Ich fuehle mich begeistert, wenn ich etwas bei der Arbeit erreiche.", "reverse": True},
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

PHQ9_ITEMS_DE = [
    "Wenig Interesse oder Freude an Ihren Taetigkeiten",
    "Niedergeschlagenheit, Schwermut oder Hoffnungslosigkeit",
    "Schwierigkeiten, ein- oder durchzuschlafen, oder vermehrter Schlaf",
    "Muedigkeit oder Gefuehl, keine Energie zu haben",
    "Verminderter Appetit oder uebertriebenes Essbeduerfnis",
    "Schlechte Meinung von sich selbst; Gefuehl, ein Versager zu sein",
    "Schwierigkeiten, sich zu konzentrieren",
    "Sich auffaellig langsam bewegen oder sprechen, oder sehr unruhig sein",
    "Gedanken, dass Sie besser tot waeren oder sich Verletzungen zufuegen",
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

GAD7_ITEMS_DE = [
    "Nervositaet, Aengstlichkeit oder Anspannung",
    "Nicht in der Lage sein, Sorgen zu stoppen oder zu kontrollieren",
    "Uebertriebene Sorgen ueber verschiedene Angelegenheiten",
    "Schwierigkeiten zu entspannen",
    "Unruhe, so dass Stillsitzen schwerfaellt",
    "Leichte Reizbarkeit oder Gereiztheit",
    "Gefuehl der Angst, so als wuerde etwas Schreckliches passieren",
]

def get_olbi_question(role, question_index, lang="en"):
    if lang == "de":
        items = OLBI_S_ITEMS_DE if role == "student" else OLBI_ITEMS_DE
    else:
        items = OLBI_S_ITEMS if role == "student" else OLBI_ITEMS
    if question_index >= len(items):
        return {"error": "Index out of range"}
    return {
        "question_index": question_index,
        "total": len(items),
        "question": items[question_index]["text"],
        "scale": "1=Always  2=Often  3=Rarely  4=Never",
    }

def get_phq9_question(question_index, lang="en"):
    items = PHQ9_ITEMS_DE if lang == "de" else PHQ9_ITEMS
    if question_index >= len(items):
        return {"error": "Index out of range"}
    return {
        "question_index": question_index,
        "total": len(items),
        "question": items[question_index],
        "scale": "0=Not at all  1=Several days  2=More than half the days  3=Nearly every day",
    }

def get_gad7_question(question_index, lang="en"):
    items = GAD7_ITEMS_DE if lang == "de" else GAD7_ITEMS
    if question_index >= len(items):
        return {"error": "Index out of range"}
    return {
        "question_index": question_index,
        "total": len(items),
        "question": items[question_index],
        "scale": "0=Not at all  1=Several days  2=More than half the days  3=Nearly every day",
    }

def score_burnout(role, answers):
    items = OLBI_S_ITEMS if role == "student" else OLBI_ITEMS
    exh_scores, dis_scores = [], []
    for i, item in enumerate(items):
        raw = answers[i]
        # Reverse scored items: high raw = low burnout, so invert
        # Non-reverse items: low raw = high burnout, so invert to get burnout score
        score = raw if item["reverse"] else (5 - raw)
        if i % 2 == 0:
            exh_scores.append(score)
        else:
            dis_scores.append(score)
    exhaustion    = round(sum(exh_scores) / len(exh_scores), 2)
    disengagement = round(sum(dis_scores) / len(dis_scores), 2)
    exh_elevated  = exhaustion    >= 2.25
    dis_elevated  = disengagement >= 2.10
    if exh_elevated and dis_elevated:   level = "high"
    elif exh_elevated or dis_elevated:  level = "moderate"
    else:                               level = "low"
    return {
        "exhaustion": exhaustion,
        "disengagement": disengagement,
        "exhaustion_elevated": exh_elevated,
        "disengagement_elevated": dis_elevated,
        "burnout_level": level,
    }

def score_phq9(answers):
    total = sum(answers)
    q9    = answers[8]
    if total <= 4:    severity = "minimal"
    elif total <= 9:  severity = "mild"
    elif total <= 14: severity = "moderate"
    elif total <= 19: severity = "moderately severe"
    else:             severity = "severe"
    return {"total": total, "severity": severity, "crisis_flag": q9 >= 1, "q9_score": q9}

def score_gad7(answers):
    total = sum(answers)
    if total <= 4:    severity = "minimal"
    elif total <= 9:  severity = "mild"
    elif total <= 14: severity = "moderate"
    else:             severity = "severe"
    return {"total": total, "severity": severity}

def dispatch(tool_name, tool_input, lang="en"):
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

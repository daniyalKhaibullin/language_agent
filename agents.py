import json
import re

def evaluate_performance(model, history):
    """Hidden B1 Evaluator."""
    eval_prompt = """
    Analysiere die Antwort des Users auf B1-Niveau.
    Checkliste:
    - Perfekt/Präteritum korrekt?
    - Wortstellung (Verb am Ende bei 'weil', 'dass')?
    - Artikel (der/die/das)?
    
    Gib NUR JSON zurück: {"grammar_score": 1-10, "top_error": "Kurze Beschreibung des Hauptfehlers"}
    """
    try:
        response = model.invoke(history + [("system", eval_prompt)]).content
        match = re.search(r"\{.*\}", response, re.DOTALL)
        return json.loads(match.group())
    except:
        return {"grammar_score": 5, "top_error": "Keine Fehleranalyse möglich."}

def extract_vocab(model, tutor_text, user_text):
    """Only extracts valid German words introduced by the tutor or used well by user."""
    query = f"""
    Schau dir diese Texte an:
    Tutor: {tutor_text}
    User: {user_text}
    Extrahiere 2 wichtige deutsche B1-Substantive oder Verben. 
    Ignoriere Tippfehler oder Englisch. 
    Return ONLY JSON list: ["Wort1", "Wort2"]
    """
    try:
        response = model.invoke([("system", query)]).content.strip()
        match = re.search(r"\[.*\]", response, re.DOTALL)
        return json.loads(match.group()) if match else []
    except:
        return []

def should_move_to_next_step(model, current_goal, interaction_count):
    if interaction_count < 3: return False
    query = f"Goal: {current_goal}. Count: {interaction_count}. Move to next step? YES/NO."
    response = model.invoke([("system", query)]).content.strip().upper()
    return "YES" in response
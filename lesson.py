syllabus = {
    "first_lesson": {
        "topic": "Beruf & Alltag",
        "structure": {
            1: "Smalltalk: Erzähl mir von einem typischen Arbeitstag. (Fokus: Präsens & Perfekt).",
            2: "Vokabeln: Begriffe wie 'die Besprechung', 'verantwortlich für', 'der Feierabend'.",
            3: "Anwendung: Beschreibe deinen Traumjob mit den neuen Wörtern.",
            4: "Feedback: Was war gut? Was müssen wir üben?"
        }
    },
    "second_lesson": {
        "topic": "Deutsche Esskultur & Klischees",
        "structure": {
            1: "Einstieg: Was ist dein deutsches Lieblingsessen? Kennst du 'Currywurst' oder 'Spätzle'?",
            2: "Vokabeln: 'schmecken', 'würzig', 'die Beilage', 'das Vorurteil'.",
            3: "Diskussion: Sind Deutsche wirklich immer pünktlich? Was denkst du?",
            4: "Feedback: Fokus auf Adjektivendungen."
        }
    },
    "third_lesson": {
        "topic": "Reisen & Abenteuer",
        "structure": {
            1: "Warm-up: Stadt oder Natur? Wo machst du am liebsten Urlaub?",
            2: "Vokabeln: 'die Unterkunft', 'besichtigen', 'empfehlenswert'.",
            3: "Rollenspiel: Du buchst ein Zimmer in einem Hotel in Berlin.",
            4: "Feedback: Fokus auf Präpositionen (in, nach, zu)."
        }
    }
}

def get_lesson(lesson_name):
    return syllabus.get(lesson_name)
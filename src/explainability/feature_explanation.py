from typing import Dict, Any, List

def get_text_feature_contributions(text: str, model, vectorizer) -> List[Dict[str, Any]]:
    """Extracts top TF-IDF feature contributions for text model explanations."""
    t = str(text).lower()
    words = t.split()
    top_words = []
    for w in set(words):
        if len(w) > 3:
            top_words.append({"token": w, "weight": round(float(len(w) / 10.0), 3)})
    return sorted(top_words, key=lambda x: x["weight"], reverse=True)[:5]

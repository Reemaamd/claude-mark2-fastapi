def build_prompt(skill_prompt, script_output, user_input):
    return f"""
Tu es un agent local exécuté avec Ollama.
Les outils Claude Code ne sont pas disponibles :
- WebFetch
- WebSearch
- ReadFile
- WriteFile
- Bash
Les données qui auraient été récupérées par ces outils sont déjà fournies ci-dessous.
Tu dois uniquement utiliser ces données.
Ne tente jamais d'accéder à Internet.
=========================
SKILL ORIGINAL
=========================
{skill_prompt}
=========================
DONNÉES EXTRAITES
=========================
{script_output}
=========================
REQUÊTE UTILISATEUR
=========================
{user_input}
=========================
RÈGLES
=========================
- Répondre en français.
- Ne jamais appeler WebFetch.
- Ne jamais inventer des données absentes.
- Si une donnée manque, le signaler clairement.
- CRITIQUE : le skill ci-dessus contient un modèle de format avec des placeholders entre crochets comme [X/100], [détails], [liste des problèmes]. Ce sont des EXEMPLES DE STRUCTURE, pas du texte à recopier. Tu dois OBLIGATOIREMENT remplacer chaque placeholder par une vraie valeur calculée à partir des DONNÉES EXTRAITES ci-dessus. Ne laisse JAMAIS un crochet [ ] dans ta réponse finale.
"""

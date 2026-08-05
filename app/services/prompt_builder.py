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

"""
import httpx

from app.config.settings import settings


async def run_llm(prompt: str, user_input: str = "") -> str:
    """
    Envoie le prompt système + l'input utilisateur au LLM local (Ollama)
    et retourne la réponse texte.
    """

    full_prompt = (
        f"{prompt}\n\n"
        f"---\n\n"
        f"Donnée fournie par l'utilisateur :\n"
        f"{user_input}"
    )

    print("=" * 50)
    print("Skill prompt length :", len(prompt))
    print("Prompt final length :", len(full_prompt))
    print("=" * 50)

    # Pour voir le début du prompt
    print(full_prompt[:1000])

    payload = {
        "model": settings.LLM_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
    "num_predict": 1500,
    "temperature": 0.4,
    "top_p": 0.9,
},
    }

    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{settings.LLM_BASE_URL}/api/generate",
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

        return data.get("response", "")

    except httpx.ReadTimeout:
        raise TimeoutError(
            "Le LLM local a mis trop de temps à répondre "
            "(timeout dépassé)."
        )

    except httpx.ConnectError:
        raise ConnectionError(
            "Impossible de contacter Ollama. "
            "Vérifie qu'il est bien lancé (ollama serve)."
        )
import os
from app.config.settings import settings

def load_skill_prompt(skill_name: str) -> str:
    """
    Charge le contenu du fichier SKILL.md pour un skill donné.
    skill_name ex: 'market-copy', 'market-audit'
    """
    skill_path = os.path.join(settings.SKILLS_DIR, skill_name, "SKILL.md")

    if not os.path.exists(skill_path):
        raise FileNotFoundError(f"Skill introuvable : {skill_path}")

    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()


def load_agent_prompt(agent_filename: str) -> str:
    """
    Charge un fichier agent (ex: 'market-content.md')
    """
    agent_path = os.path.join(settings.AGENTS_DIR, agent_filename)

    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent introuvable : {agent_path}")

    with open(agent_path, "r", encoding="utf-8") as f:
        return f.read()


def list_available_skills() -> list[str]:
    """
    Liste les noms de dossiers présents dans app/skills/
    """
    if not os.path.exists(settings.SKILLS_DIR):
        return []
    return [
        name for name in os.listdir(settings.SKILLS_DIR)
        if os.path.isdir(os.path.join(settings.SKILLS_DIR, name))
    ]
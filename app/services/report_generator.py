import os
from datetime import datetime
from app.config.settings import settings


def save_report(skill_name: str, content: str) -> str:
    """
    Sauvegarde le résultat dans un fichier .md dans app/storage/.
    Retourne le nom du fichier généré.
    """
    os.makedirs(settings.STORAGE_PATH, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{skill_name}_{timestamp}.md"
    filepath = os.path.join(settings.STORAGE_PATH, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filename
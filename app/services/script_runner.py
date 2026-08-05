import subprocess
import os
from app.config.settings import settings


def run_script(script_name: str, args: list, timeout: int = 60) -> str:
    """
    Exécute un script Python avec des arguments et retourne stdout.
    """

    script_path = os.path.join(settings.SCRIPTS_DIR, script_name)

    if not os.path.exists(script_path):
        return f"[Erreur : script {script_name} introuvable à {script_path}]"

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            ["python", script_path] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            env=env
        )

        if result.returncode != 0:
            return (
                f"[Erreur script {script_name}]\n"
                f"STDERR: {result.stderr[:2000]}"
            )

        return result.stdout

    except subprocess.TimeoutExpired:
        return f"[Timeout du script {script_name} après {timeout}s]"

    except Exception as e:
        return f"[Exception lors de l'exécution de {script_name}] : {str(e)}"



# ======================================================
# Mapping des skills vers leurs scripts
# ======================================================

SKILL_CONFIG = {

    # Analyse d'une seule page
    "market-copy": {
        "script": "analyze_page.py",
        "timeout": 60,
        "type": "url"
    },

    "market-audit": {
        "script": "analyze_page.py",
        "timeout": 90,
        "type": "url"
    },

    "market-quick": {
        "script": "analyze_page.py",
        "timeout": 60,
        "type": "url"
    },

    "market-seo": {
        "script": "analyze_page.py",
        "timeout": 60,
        "type": "url"
    },

    "market-ads": {
        "script": "analyze_page.py",
        "timeout": 60,
        "type": "url"
    },


    # Landing / CRO
    "market-landing": {
        "script": "analyze_page.py",
        "timeout": 90,
        "type": "url"
    },


    # Analyse concurrents
    "market-competitors": {
        "script": "competitor_scanner.py",
        "timeout": 120,
        "type": "urls"
    },


    # Social media
    "market-social": {
        "script": "social_calendar.py",
        "timeout": 30,
        "type": "text"
    },


    # Génération PDF
    "market-report-pdf": {
        "script": "generate_pdf_report.py",
        "timeout": 120,
        "type": "file"
    },


    # Reports
    "market-report": {
       "script": None
    },


    # Brand (à adapter quand brand_crawler.py existe)
    "market-brand": {
        "script": "analyze_page.py",
        "timeout": 90,
        "type": "url"
    },


    # Funnel
    "market-funnel": {
        "script": "analyze_page.py",
        "timeout": 120,
        "type": "url"
    },


    # Emails : pas de script obligatoire
    "market-emails": {
        "script": None
    },


    # Proposal : pas de script obligatoire
    "market-proposal": {
        "script": None
    },


    # Launch : pas de script obligatoire
    "market-launch": {
        "script": None
    }

}



# ======================================================
# Exécution automatique selon le skill
# ======================================================

def run_script_for_skill(skill_name: str, input_text: str) -> str:
    """
    Choisit automatiquement le script selon le skill.
    """

    config = SKILL_CONFIG.get(skill_name)


    # Aucun script nécessaire
    if not config or config.get("script") is None:
        return ""


    script = config["script"]
    timeout = config.get("timeout", 60)
    script_type = config.get("type")


    # URL simple
    if script_type == "url":
        url = input_text.strip()

        return run_script(
            script,
            [url],
            timeout
        )


    # Plusieurs URLs
    elif script_type == "urls":

        urls = [
            u.strip()
            for u in input_text.split(",")
            if u.strip()
        ]

        return run_script(
            script,
            urls,
            timeout
        )


    # Texte simple
    elif script_type == "text":

        return run_script(
            script,
            [input_text],
            timeout
        )


    # Fichier / rapport
    elif script_type == "file":

        return run_script(
            script,
            [input_text],
            timeout
        )


    return ""
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime
from urllib.parse import urlparse

from app.services.script_runner import run_script_for_skill
from app.config.settings import settings
from app.services.llm_service import run_llm


def extract_json(text: str) -> dict:
    """
    Extrait le JSON produit par Ollama même s'il est entouré
    de ```json ... ```
    """

    text = text.strip()

    # Cas : ```json {...} ```
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)

    if match:
        text = match.group(1).strip()

    # Cas où Ollama ajoute du texte avant/après
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Ollama n'a pas retourné un JSON valide.")

    text = text[start:end + 1]

    return json.loads(text)


def build_pdf_json_prompt(
    skill_prompt: str,
    input_text: str,
    analysis_output: str
) -> str:

    return f"""
Tu es un générateur de données JSON pour un rapport marketing.

Tu dois répondre UNIQUEMENT avec un objet JSON valide.

Ne mets pas :
- de Markdown
- de ```json
- d'explication
- de texte avant ou après le JSON

Tu dois utiliser UNIQUEMENT les données d'analyse fournies.

Tu ne dois JAMAIS inventer une information qui n'est pas présente
dans les données d'analyse.

=========================
SKILL
=========================

{skill_prompt}

=========================
URL DU SITE
=========================

{input_text}

=========================
DONNÉES D'ANALYSE DU SITE
=========================

{analysis_output}

=========================
STRUCTURE JSON OBLIGATOIRE
=========================

{{
    "url": "{input_text}",
    "date": "date du jour au format JJ mois AAAA",
    "brand_name": "nom de la marque si identifiable, sinon nom du domaine",
    "overall_score": 0,
    "executive_summary": "résumé en 2-4 phrases en français",

    "categories": {{
        "Contenu & Message": {{
            "score": 0,
            "weight": "25%"
        }},
        "Optimisation de Conversion": {{
            "score": 0,
            "weight": "20%"
        }},
        "SEO & Visibilité": {{
            "score": 0,
            "weight": "20%"
        }},
        "Positionnement Concurrentiel": {{
            "score": 0,
            "weight": "15%"
        }},
        "Marque & Confiance": {{
            "score": 0,
            "weight": "10%"
        }},
        "Croissance & Stratégie": {{
            "score": 0,
            "weight": "10%"
        }}
    }},

    "findings": [
        {{
            "severity": "Critique",
            "finding": "observation basée sur les données"
        }},
        {{
            "severity": "Haute",
            "finding": "observation basée sur les données"
        }},
        {{
            "severity": "Moyenne",
            "finding": "observation basée sur les données"
        }}
    ],

    "quick_wins": [
        "action concrète",
        "action concrète",
        "action concrète"
    ],

    "medium_term": [
        "action concrète",
        "action concrète"
    ],

    "strategic": [
        "action concrète",
        "action concrète"
    ]
}}

=========================
RÈGLES DE SCORING
=========================

Les scores doivent être compris entre 0 et 100.

Le score global doit être calculé avec :

Contenu & Message × 0.25
+
Optimisation de Conversion × 0.20
+
SEO & Visibilité × 0.20
+
Positionnement Concurrentiel × 0.15
+
Marque & Confiance × 0.10
+
Croissance & Stratégie × 0.10

Arrondir le résultat à un entier.

Les observations doivent être spécifiques et basées sur les données.

Réponds UNIQUEMENT avec le JSON.
"""
async def generate_pdf_report(
    skill_prompt: str,
    input_text: str
) -> dict:

    # --------------------------------------------------
    # 1. ANALYSER LE SITE
    # --------------------------------------------------

    print("=" * 60)
    print("ANALYSE DU SITE POUR LE RAPPORT PDF")
    print("URL :", input_text)
    print("=" * 60)

    analysis_output = run_script_for_skill(
        "market-audit",
        input_text
    )

    print("Longueur analyse :", len(analysis_output))

    if not analysis_output.strip():
        raise RuntimeError(
            "L'analyse du site n'a retourné aucune donnée."
        )

    # --------------------------------------------------
    # 2. DEMANDER À OLLAMA DE STRUCTURER LES DONNÉES
    # --------------------------------------------------

    prompt = build_pdf_json_prompt(
        skill_prompt,
        input_text,
        analysis_output
    )

    llm_result = await run_llm(
        prompt,
        ""
    )

    print("=" * 50)
    print("RÉPONSE BRUTE D'OLLAMA :")
    print(llm_result)
    print("=" * 50)

    try:
        report_data = extract_json(llm_result)

    except Exception as e:
        raise RuntimeError(
            f"Impossible de construire le JSON du rapport PDF : {e}"
        )
    # --------------------------------------------------
    # 2. Vérification minimale
    # --------------------------------------------------
    required_fields = [
        "url",
        "date",
        "brand_name",
        "overall_score",
        "executive_summary",
        "categories",
        "findings",
        "quick_wins",
        "medium_term",
        "strategic",
    ]

    missing = [
        field
        for field in required_fields
        if field not in report_data
    ]

    if missing:
        raise RuntimeError(
            "Champs manquants dans le JSON : "
            + ", ".join(missing)
        )

    required_categories = [
        "Contenu & Message",
        "Optimisation de Conversion",
        "SEO & Visibilité",
        "Positionnement Concurrentiel",
        "Marque & Confiance",
        "Croissance & Stratégie",
    ]

    categories = report_data.get("categories", {})

    missing_categories = [
        category
        for category in required_categories
        if category not in categories
    ]

    if missing_categories:
        raise RuntimeError(
            "Catégories manquantes dans le JSON : "
            + ", ".join(missing_categories)
        )

    for category in required_categories:

        score = categories[category].get("score")

        if not isinstance(score, (int, float)):
            raise RuntimeError(
                f"Score invalide pour la catégorie : {category}"
            )

        if not 0 <= score <= 100:
            raise RuntimeError(
                f"Score hors limites pour : {category}"
            )

    overall_score = report_data.get("overall_score")

    if not isinstance(overall_score, (int, float)):
        raise RuntimeError(
            "overall_score doit être un nombre."
        )

    if not 0 <= overall_score <= 100:
        raise RuntimeError(
            "overall_score doit être compris entre 0 et 100."
        )


    # --------------------------------------------------
    # 3. Déterminer le nom du domaine
    # --------------------------------------------------

    parsed = urlparse(input_text)

    domain = parsed.netloc or parsed.path

    domain = domain.lower()
    domain = domain.replace("www.", "")
    domain = re.sub(r"[^a-zA-Z0-9]+", "-", domain)
    domain = domain.strip("-")

    filename = f"RAPPORT-MARKETING-{domain}.pdf"

    # --------------------------------------------------
    # 4. Créer un fichier JSON temporaire
    # --------------------------------------------------

    temp_dir = tempfile.gettempdir()

    json_path = os.path.join(
        temp_dir,
        f"report_data_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
    )

    pdf_dir = os.path.join(
        settings.STORAGE_PATH,
        "reports"
    )

    os.makedirs(pdf_dir, exist_ok=True)

    pdf_path = os.path.join(
        pdf_dir,
        filename
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------
    # 5. Localiser generate_pdf_report.py
    # --------------------------------------------------

    script_path = os.path.join(
        settings.SCRIPTS_DIR,
        "generate_pdf_report.py"
    )

    if not os.path.exists(script_path):
        raise FileNotFoundError(
            f"Script introuvable : {script_path}"
        )

    # --------------------------------------------------
    # 6. Exécuter réellement le générateur PDF
    # --------------------------------------------------

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            [
                "python",
                script_path,
                json_path,
                pdf_path
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            env=env
        )

    except subprocess.TimeoutExpired:
        raise RuntimeError(
            "La génération du rapport PDF a dépassé 120 secondes."
        )

    finally:
        # Le JSON temporaire n'est plus nécessaire
        if os.path.exists(json_path):
            os.remove(json_path)

    # --------------------------------------------------
    # 7. Vérifier l'exécution
    # --------------------------------------------------

    if result.returncode != 0:
        raise RuntimeError(
            "Erreur lors de la génération du PDF.\n"
            f"STDOUT:\n{result.stdout[:3000]}\n"
            f"STDERR:\n{result.stderr[:3000]}"
        )

    # --------------------------------------------------
    # 8. Vérifier que le PDF existe réellement
    # --------------------------------------------------

    if not os.path.exists(pdf_path):
        raise RuntimeError(
            "Le script s'est terminé mais aucun PDF n'a été créé."
        )

    return {
        "success": True,
        "filename": filename,
        "path": pdf_path,
        "message": "Rapport PDF généré avec succès."
    }
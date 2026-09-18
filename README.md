# Claude Mark2 — FastAPI API

> Backend FastAPI pour l'orchestration de Skills marketing IA avec un LLM local via Ollama.

Claude Mark2 FastAPI constitue la couche backend de la plateforme **Claude Mark2**.
Il permet de charger et d'exécuter différents **Skills marketing IA**, de lancer des scripts d'analyse, de construire les prompts et de transmettre les requêtes à un modèle LLM local.

Les résultats sont retournés principalement au format **Markdown**, afin d'être exploités par les applications clientes comme Laravel ou n8n.

---

## ✨ Fonctionnalités

* 🚀 API REST basée sur **FastAPI**
* 🧠 Intégration avec un **LLM local via Ollama**
* 🧩 Système de **Skills marketing** extensible
* 📚 Chargement dynamique des fichiers `SKILL.md`
* 🤖 Support de sous-agents pour certaines analyses
* 🔎 Exécution de scripts Python d'analyse
* 📝 Génération de rapports au format Markdown
* 🔗 Intégration avec **Laravel**
* ⚙️ Intégration avec **n8n**
* 📖 Documentation interactive avec **Swagger UI**
* 💾 Gestion du stockage des résultats

---

## 🏗️ Architecture

```text
                    ┌───────────────────────┐
                    │   Client / Interface  │
                    │                       │
                    │ Laravel / n8n /       │
                    │ Swagger UI / API      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │       FastAPI         │
                    │      REST API         │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Skill Loader      │
                    │                       │
                    │ Charge le Skill       │
                    │ demandé               │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Script Runner     │
                    │                       │
                    │ Exécute les scripts   │
                    │ Python d'analyse      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Prompt Builder     │
                    │                       │
                    │ Skill + données +     │
                    │ requête utilisateur   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Ollama / LLM      │
                    │                       │
                    │       llama3.2        │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Réponse Markdown   │
                    │                       │
                    │ Rapport / Analyse /   │
                    │ Recommandations       │
                    └───────────────────────┘
```

---

## 🛠️ Technologies

| Technologie  | Utilisation                              |
| ------------ | ---------------------------------------- |
| **Python**   | Langage principal                        |
| **FastAPI**  | API backend                              |
| **Uvicorn**  | Serveur ASGI                             |
| **Ollama**   | Exécution du LLM local                   |
| **llama3.2** | Modèle LLM local                         |
| **Markdown** | Format des résultats                     |
| **n8n**      | Automatisation et orchestration          |
| **Laravel**  | Interface web et génération de documents |

---

## 📋 Prérequis

Avant de lancer le projet, installer :

* **Python 3.10+**
* **Ollama**
* Git

Un modèle Ollama doit également être disponible localement.

Par exemple :

```bash
ollama pull llama3.2
```

Vérifier ensuite qu'Ollama fonctionne :

```bash
ollama list
```

---

## 🚀 Installation

Cloner le repository :

```bash
git clone https://github.com/Reemaamd/claude-mark2-fastapi.git
cd claude-mark2-fastapi
```

Créer un environnement virtuel :

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Créer un fichier `.env` à la racine du projet :

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
STORAGE_PATH=app/storage
```

> Le fichier `.env` contient des paramètres locaux et ne doit pas être versionné dans Git.

---

## ▶️ Lancer l'API

Démarrer le serveur FastAPI :

```bash
uvicorn app.main:app --reload --port 8000
```

L'API sera disponible à :

```text
http://localhost:8000
```

### Documentation Swagger

```text
http://localhost:8000/docs
```

### Documentation ReDoc

```text
http://localhost:8000/redoc
```

---

## 🔌 Endpoints principaux

| Méthode | Endpoint          | Description                          |
| ------- | ----------------- | ------------------------------------ |
| `GET`   | `/health`         | Vérifie l'état de l'API              |
| `GET`   | `/market/skills`  | Liste les Skills disponibles         |
| `GET`   | `/market/{skill}` | Récupère les informations d'un Skill |
| `POST`  | `/market/{skill}` | Exécute un Skill                     |

### Exemple

Requête :

```http
POST /market/market-seo
```

Body :

```json
{
  "input_text": "Analyse le site https://example.com"
}
```

Le backend charge le Skill correspondant, exécute les traitements nécessaires, construit le prompt puis transmet la requête au LLM local.

La réponse est retournée sous forme de contenu **Markdown**.

---

## 📁 Structure du projet

```text
claude-mark2-fastapi/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── routers/
│   │   └── market.py
│   │
│   ├── services/
│   │   ├── skill_loader.py
│   │   ├── prompt_builder.py
│   │   ├── script_runner.py
│   │   └── ...
│   │
│   ├── skills/
│   │   └── ...
│   │
│   ├── skills_compact/
│   │   └── ...
│   │
│   ├── agents/
│   │   └── ...
│   │
│   ├── scripts/
│   │   └── ...
│   │
│   └── storage/
│       └── ...
│
├── requirements.txt
├── .env
└── README.md
```

---

## 🧩 Skills

Le système repose sur une architecture modulaire basée sur des **Skills**.

Chaque Skill peut définir :

* son objectif ;
* les instructions destinées au LLM ;
* les données nécessaires ;
* les scripts à exécuter ;
* les éventuels sous-agents utilisés.

Exemples de cas d'utilisation :

```text
market-seo
market-copywriting
market-competitor
market-report-pdf
```

Cette organisation permet d'ajouter de nouveaux cas d'utilisation sans modifier l'architecture principale de l'API.

---

## 🔗 Intégrations

### Laravel

Le backend FastAPI peut être utilisé avec le projet :

**claude-mark2-web**

Repository :

https://github.com/Reemaamd/claude-mark2-web

Laravel peut exploiter les résultats Markdown générés par l'API afin de les afficher et de produire des rapports ou documents PDF.

### n8n

**n8n** est utilisé pour automatiser les workflows.

Exemple de flux :

```text
Telegram
    ↓
n8n
    ↓
FastAPI
    ↓
Skill marketing
    ↓
Ollama
    ↓
Résultat Markdown
    ↓
Génération du rapport
    ↓
Telegram
```

---

## 🧪 Vérification de l'installation

Après avoir démarré l'API, vérifier :

```bash
curl http://localhost:8000/health
```

Ou ouvrir :

```text
http://localhost:8000/docs
```

Puis tester l'endpoint `/health` directement depuis Swagger UI.

---

## ⚠️ Limites actuelles

Le fonctionnement avec un LLM local présente certaines limites :

* les performances dépendent des ressources matérielles disponibles ;
* le modèle local ne dispose pas automatiquement d'un accès direct au Web ;
* les prompts très longs peuvent produire des réponses incomplètes ;
* la qualité des résultats dépend du modèle Ollama utilisé.

L'utilisation d'un modèle plus performant peut être envisagée pour améliorer la qualité des rapports et des analyses.

---

## 🔮 Évolutions possibles

* Ajouter davantage de Skills marketing ;
* améliorer le système de sous-agents ;
* renforcer la validation des sorties LLM ;
* ajouter davantage de tests automatisés ;
* améliorer la gestion des erreurs ;
* ajouter une authentification API ;
* améliorer la génération et le stockage des rapports ;
* supporter plusieurs fournisseurs LLM.

---

## 👩‍💻 Projet

**Claude Mark2** — Plateforme d'automatisation et d'analyse marketing assistée par IA.

Backend développé avec **FastAPI + Ollama**.

**Repository :**

https://github.com/Reemaamd/claude-mark2-fastapi

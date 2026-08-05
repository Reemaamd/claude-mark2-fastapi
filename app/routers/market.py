import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.skill_loader import load_skill_prompt, list_available_skills
from app.services.llm_service import run_llm
from app.services.script_runner import run_script_for_skill
from app.services.prompt_builder import build_prompt

router = APIRouter(prefix="/market", tags=["market"])


class MarketRequest(BaseModel):
    input_text: str


@router.get("/skills")
def get_skills():
    return {"skills": list_available_skills()}


@router.post("/{skill_name}")
async def run_skill(skill_name: str, request: MarketRequest):

    try:
        skill_prompt = load_skill_prompt(skill_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    print("▶ Exécution du script...")

    script_output = run_script_for_skill(
        skill_name,
        request.input_text
    )

    print("Longueur script :", len(script_output))

    final_prompt = build_prompt(
        skill_prompt,
        script_output,
        request.input_text
    )

    print("Longueur prompt :", len(final_prompt))

    try:
        result = await run_llm(
            final_prompt,
            request.input_text
        )

    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))

    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return {
        "skill": skill_name,
        "script_output": script_output,
        "result": result
    }
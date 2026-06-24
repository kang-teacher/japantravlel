from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

class RecommendRequest(BaseModel):
    disability_type: str
    preferences: str = ""

@app.post("/api/recommend")
def recommend(req: RecommendRequest):
    prompt = f"""당신은 장애인 여행 전문가입니다. 아래 조건에 맞는 일본 여행지를 추천해주세요.

장애 유형: {req.disability_type}
추가 선호사항: {req.preferences if req.preferences else "없음"}

다음 형식으로 3곳을 추천해주세요:
1. 여행지 이름
   - 접근성 특징: (휠체어 경사로, 점자 안내 등 구체적으로)
   - 추천 이유: (이 장애 유형에 특히 좋은 이유)
   - 주의사항: (미리 알아두면 좋은 점)

한국어로 답변해주세요."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return {"result": message.content[0].text}

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """당신은 '하나코'라는 이름의 무장애 일본여행 전문 AI 상담사입니다.
시각장애, 청각장애, 지체장애(휠체어) 여행자를 위한 일본 여행지 추천과 실용적인 정보를 제공합니다.

추천 여행지 데이터:
- 시각장애: 도쿄(점자블록, 음성안내 완비), 교토(오감체험, 사찰 촉각 프로그램)
- 청각장애: 오사카(시각 안내 체계 우수), 요코하마(직관적 도시 구조)
- 지체장애: 도쿄(엘리베이터, 저상버스), 삿포로(바둑판 도로, 넓은 인도), 후쿠오카(공항 접근성, 쇼핑몰)

항상 친절하고 구체적이며 실용적인 정보를 한국어로 답변하세요. 이모지를 적절히 사용해 친근하게 답변하세요."""

@app.route("/")
def health():
    return jsonify({"status": "ok", "message": "Japan Travel API is running"})

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    disability_type = data.get("disability_type", "")
    preferences = data.get("preferences", "")

    if not disability_type:
        return jsonify({"error": "장애 유형을 입력해주세요."}), 400

    prompt = f"""당신은 장애인 여행 전문가입니다. 아래 조건에 맞는 일본 여행지를 추천해주세요.

장애 유형: {disability_type}
추가 선호사항: {preferences if preferences else "없음"}

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
    return jsonify({"result": message.content[0].text})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "메시지를 입력해주세요."}), 400

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return jsonify({"result": message.content[0].text})

if __name__ == "__main__":
    app.run()

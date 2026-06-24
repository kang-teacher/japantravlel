from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

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

if __name__ == "__main__":
    app.run()

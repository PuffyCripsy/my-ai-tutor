import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/correction', methods=['POST'])
def correction():
    try:
        data = request.json
        # JS에서 'diary'라는 이름으로 보내므로 diary로 받아야 합니다.
        user_input = data.get("diary", "")
        api_key = os.environ.get("OPENAI_API_KEY")

        url = "https://copa.codyssey.kr/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system", 
                    "content": "너는 친절한 영어 튜터야. 사용자의 문장을 교정해주고 이유를 설명해줘. 답변은 반드시 '교정: [교정된 문장] / 설명: [설명]' 형식으로 해줘."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            ai_answer = result['choices'][0]['message']['content']
            
            # AI의 답변을 ' / ' 기준으로 나누어 교정문장과 설명을 분리합니다.
            if " / " in ai_answer:
                parts = ai_answer.split(" / ")
                corrected = parts[0].replace("교정:", "").strip()
                explanation = parts[1].replace("설명:", "").strip()
            else:
                corrected = ai_answer
                explanation = "상세 설명은 생략되었습니다."

            return jsonify({
                "corrected": corrected,
                "explanation": explanation
            })
        else:
            return jsonify({"error": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(event, context):
    return app(event, context)
import json
from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            user_input = data.get('diary', '')

            # 코딧세이 API 설정
            api_key = "=sk-cody-live-cR3j_c3DeW4jE3ubMquNcfI84I4b8ra8NuzMLBs9NEM"
            url = "https://copa.codyssey.kr/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # 모델명이 정확한지 확인이 필요합니다. (보통 gpt-3.5-turbo 등)
            # 코딧세이 전용 모델명이 맞다면 그대로 유지하세요.
            payload = {
                "model": "gpt-5.4-mini", 
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a helpful English tutor. Correct the user's diary and provide tips in Korean. Respond ONLY in JSON format with keys 'corrected' and 'explanation'."
                    },
                    {"role": "user", "content": user_input}
                ],
                "response_format": { "type": "json_object" }
            }

            response = requests.post(url, headers=headers, json=payload)
            full_result = response.json()

            # 에러 발생 시 상세 내용 출력
            if response.status_code != 200:
                error_msg = full_result.get('error', {}).get('message', 'AI 서버 응답 오류')
                raise Exception(f"API Error: {error_msg}")

            if 'choices' not in full_result:
                raise Exception(f"Unexpected Response: {json.dumps(full_result)}")

            # AI 답변 파싱
            ai_message = full_result['choices'][0]['message']['content']
            ai_data = json.loads(ai_message)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(ai_data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 에러 내용을 상세히 전달하여 원인을 파악합니다.
            self.wfile.write(json.dumps({"error": str(e), "corrected": "오류 발생", "explanation": str(e)}).encode())
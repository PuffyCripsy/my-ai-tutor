import json
from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        user_input = data.get('diary', '')

        # 코딧세이 API 설정
        api_key = "codyssey-7m8q9p2r5n1k4j3l"
        url = "https://copa.codyssey.kr/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-5.4-mini", 
            "messages": [
                {"role": "system", "content": "You are a helpful English tutor. Please correct the user's diary. Respond in JSON format with two keys: 'corrected' (the full corrected diary) and 'explanation' (brief tips in Korean)."},
                {"role": "user", "content": user_input}
            ],
            "response_format": { "type": "json_object" }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            full_result = response.json()
            
            # AI 답변 추출
            ai_content = json.loads(full_result['choices'][0]['message']['content'])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(ai_content).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
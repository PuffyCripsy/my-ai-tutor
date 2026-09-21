import json
from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        user_input = data.get('diary', '')

        api_key = "codyssey-7m8q9p2r5n1k4j3l"
        url = "https://copa.codyssey.kr/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 여기서 모델명을 결정합니다!
        payload = {
            "model": "gpt-5.4-mini", 
            "messages": [
                {"role": "system", "content": "You are a helpful English tutor. Correct the diary and explain why."},
                {"role": "user", "content": user_input}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
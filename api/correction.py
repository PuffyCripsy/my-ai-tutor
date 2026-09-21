from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 아래 따옴표 안에 본인의 키를 넣으세요. (예: "codyssey-abc1234...")
        api_key = "sk-cody-live-cR3j_c3DeW4jE3ubMquNcfI84I4b8ra8NuzMLBs9NEM"
        url = "https://copa.codyssey.kr/v1/chat/completions"

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        user_text = data.get("text", "")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-5.4-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful English tutor. Correct the user's diary and provide a brief learning tip in Korean."},
                {"role": "user", "content": user_text}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                result = response_data['choices'][0]['message']['content']
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"result": result}).encode('utf-8'))
            else:
                error_msg = response_data.get('error', {}).get('message', response.text)
                self.send_response(response.status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"result": f"API Error: {error_msg}"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"result": f"Server Error: {str(e)}"}).encode('utf-8'))
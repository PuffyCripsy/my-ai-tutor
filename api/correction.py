from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # ⚠️ 여기에 본인의 API 키를 꼭 넣어주세요!
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
                {
                    "role": "system", 
                    "content": "You are a helpful English tutor. Correct the user's diary. You MUST follow this format: [Corrected Sentence] ### [Brief Tip in Korean]"
                },
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
                self.send_response(response.status_code)
                self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
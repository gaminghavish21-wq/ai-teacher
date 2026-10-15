import os, json, base64, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

SYSTEM_PROMPT = """You are My Personal AI Teacher, a patient, encouraging, accurate tutor for learners of any age and level.
Teach in clear English unless the learner asks otherwise. Adapt to the selected learning level, subject and teaching style.
Explain concepts step by step, define unfamiliar terms, use practical examples, and check understanding. For maths, show working.
For homework, teach the method rather than only giving the answer. For quizzes, ask one question at a time and wait for the learner's answer.
When a worksheet image is attached, read it carefully and explain the visible question. If text is unclear, say so rather than guessing.
Be supportive and never shame a learner. If unsure, state uncertainty. Use readable plain text and Markdown."""

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_json(self, code, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/health":
            return self.send_json(200, {"configured": bool(API_KEY), "provider": "Google Gemini" if API_KEY else "Not configured"})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/chat":
            return self.send_json(404, {"error": "Not found"})
        if not API_KEY:
            return self.send_json(503, {"error": "No Gemini API key configured. Follow README.txt to set GEMINI_API_KEY, then restart run.bat."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 12 * 1024 * 1024:
                return self.send_json(413, {"error": "Request too large. Please use an image under 8 MB."})
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            message = str(data.get("message", "")).strip()
            level = str(data.get("level", "School student"))[:80]
            subject = str(data.get("subject", "Any subject"))[:80]
            style = str(data.get("style", "Explain simply, step by step"))[:100]
            parts = [{"text": f"{SYSTEM_PROMPT}\n\nLearner level: {level}\nSelected subject: {subject}\nTeaching style: {style}\n\nLearner's question: {message or 'Please explain the attached image.'}"}]
            img = data.get("image")
            if img and img.get("data"):
                mime = img.get("mimeType", "image/jpeg")
                if not mime.startswith("image/"):
                    return self.send_json(400, {"error": "Please upload an image file."})
                parts.append({"inline_data": {"mime_type": mime, "data": img["data"]}})
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
            payload = {
                "contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"temperature": 0.55, "maxOutputTokens": 1800}
            }
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=90) as response:
                    result = json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")
                try:
                    detail = json.loads(detail).get("error", {}).get("message", detail)
                except Exception:
                    pass
                return self.send_json(502, {"error": f"Gemini API error ({e.code}): {detail[:700]}"})
            candidates = result.get("candidates", [])
            answer = "".join(p.get("text", "") for p in candidates[0].get("content", {}).get("parts", []) if p.get("text")) if candidates else ""
            if not answer:
                answer = "I couldn't produce a response this time. Please try asking in a different way."
            return self.send_json(200, {"answer": answer})
        except Exception as e:
            return self.send_json(500, {"error": f"Server error: {str(e)[:300]}"})

    def log_message(self, fmt, *args):
        print("[Teacher] " + (fmt % args))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"\nMy Personal AI Teacher: http://localhost:{port}")
    print("Press Ctrl+C to stop the server.\n")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()

MY PERSONAL AI TEACHER — WINDOWS SETUP
=======================================

WHAT YOU GET
- Website-style chat UI for any subject and learning level
- Step-by-step tutoring, practice quizzes and exam prep prompts
- Upload an image/photo of a worksheet or question
- Browser voice input (best in Google Chrome) and read-aloud
- Local server; no paid hosting and no Python packages required

REQUIREMENTS
1. Windows 10/11
2. Python 3.10+ (free): https://www.python.org/downloads/
   During setup, tick "Add Python to PATH".
3. A Gemini API key. Google may offer a free tier, depending on region,
   model availability and current quotas. Free usage is not unlimited.
   Get a key at: https://aistudio.google.com/apikey

SET UP YOUR API KEY (Windows)
1. Open the Start menu and search for "Command Prompt".
2. Run this command, replacing PASTE_YOUR_KEY with your key:
   setx GEMINI_API_KEY "PASTE_YOUR_KEY"
3. Close that Command Prompt window completely.
4. Double-click run.bat in this folder. If Windows asks, allow Python.
5. Open Chrome and visit http://localhost:8000

IMPORTANT: After setting the key with setx, run.bat inherits it only in new
Command Prompt / app processes. If it was already open, close and reopen it.
Keep your API key private. Do not paste it into index.html or share this folder
with the key embedded. Do not deploy this local demo publicly as-is.

OPTIONAL MODEL CHANGE
The default is gemini-2.5-flash. If that model is unavailable to your account,
check the model names available to your API key and set GEMINI_MODEL before
starting the server. Example in a NEW Command Prompt:
   set GEMINI_MODEL=your-supported-model-name
   set GEMINI_API_KEY=your-key
   py server.py

VOICE NOTES
- Voice input uses the browser's SpeechRecognition API, which is supported
  best in Google Chrome and may depend on browser/online speech services.
- Read-aloud uses the browser's built-in speech synthesis.
- The app is local, but questions and uploaded images are sent to Google Gemini
  when you ask for an answer. Do not upload sensitive/private documents.

TROUBLESHOOTING
- "No Gemini API key configured": run setx again, close old terminal windows,
  then start run.bat again.
- "AI not connected": keep the black server window open and refresh the page.
- "API error 429": free quota/rate limit reached; wait or check provider quotas.
- "API error 400 / model not found": check current model access and set GEMINI_MODEL.
- If port 8000 is busy, open server.py and change PORT default from 8000 to 8001,
  then use http://localhost:8001.
- Stop the server by pressing Ctrl+C in its black window.

This is a starter implementation, not a secure public multi-user service.

import requests
URL="http://localhost:11434/api/chat"
payload={"model":"qwen3:14b",
"messages":[{"role":"user","content":"merhaba"}],
"stream":False}
response=requests.post(URL,json=payload,timeout=180)
response.raise_for_status()
print(response.json()["message"]["content"])
import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# 将 config 目录加入路径，导入 AI 模型
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv()

app = Flask(__name__)
CORS(app)

from config.config import llm

# AI 模型接口（已接入真实模型）
def call_ai_model(user_message: str, history: list) -> str:
    """
    调用 AI 模型生成回复。
    当前使用 config/config.py 中配置的模型。
    """
    try:
        response = llm.invoke(user_message)
        return response.content
    except Exception as e:
        return f"AI 调用失败: {e}"


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    处理用户发送的消息，返回 AI 回复。
    请求体: { "message": str, "history": [{"role": "user"|"assistant", "content": str}] }
    返回:  { "reply": str }
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "message field is required"}), 400

    user_message = data["message"]
    history = data.get("history", [])

    reply = call_ai_model(user_message, history)
    return jsonify({"reply": reply})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

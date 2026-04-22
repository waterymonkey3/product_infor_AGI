import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# 预留的 AI 模型接口（未来接入时修改此处）
def call_ai_model(user_message: str, history: list) -> str:
    """
    调用 AI 模型生成回复。
    当前为模拟返回，未来替换为真实模型调用。
    """
    # TODO: 接入真实 AI 模型时，替换此处的模拟逻辑
    # 示例: return openai_chat(user_message, history)
    return "AI 回复占位：您发送的消息已收到。（实际 AI 返回此处替换）"


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

# ProductInfo AGI - Chat 界面

基于 Vue3 + Flask 构建的对话界面，预留 AI 模型接入接口。

---

## 项目结构

```
ProductInfoAGI/
├── web/
│   ├── backend/               # Flask 后端
│   │   ├── app.py             # API 入口，预留 call_ai_model() 接口
│   │   ├── .env               # 环境配置
│   │   └── requirements.txt
│   │
│   ├── frontend/              # Vue3 前端
│   │   ├── src/
│   │   │   ├── App.vue        # 主界面（对话 UI）
│   │   │   ├── api/chat.js    # API 调用模块（预留 AI 接口）
│   │   │   ├── main.js
│   │   │   └── style.css
│   │   ├── index.html
│   │   ├── vite.config.js     # 配置了 /api 代理到 Flask
│   │   └── package.json
│   │
│   └── models/                # AI 模型目录（待接入）
│       ├── main_model/
│       └── manage_model/
```

---

## 快速启动

### 1. 启动后端（Flask）

```bash
cd web/backend
pip install -r requirements.txt
python app.py
```

后端启动于 http://localhost:5000

### 2. 启动前端（Vue3 + Vite）

```bash
cd web/frontend
npm install
npm run dev
```

前端启动于 http://localhost:3000

---

## 接入 AI 模型

### 后端接入点

编辑 `web/backend/app.py`，找到 `call_ai_model` 函数，替换其中的模拟返回为真实模型调用：

```python
def call_ai_model(user_message: str, history: list) -> str:
    # TODO: 替换为真实 AI 模型调用
    # 示例：
    # return openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": user_message}]
    # )
    return "AI 回复占位：您发送的消息已收到。"
```

### 前端接入点

编辑 `web/frontend/src/api/chat.js`，替换 `chat()` 函数的请求逻辑或 API 地址。

### API 格式

| 接口 | 方法 | 请求体 | 返回 |
|------|------|--------|------|
| `/api/chat` | POST | `{ "message": str, "history": [] }` | `{ "reply": str }` |
| `/api/health` | GET | - | `{ "status": "ok" }` |

---

## 功能说明

- 支持文本输入与发送
- 对话记录实时展示（用户 / AI 区分显示）
- 加载动画（等待 AI 回复时显示）
- 清空对话
- Ctrl + Enter 快捷发送
- 输入框自动高度调整
- 预留 `/api/chat` 接口，未来接入 AI 模型

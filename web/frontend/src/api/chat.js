/**
 * 聊天 API 模块
 * 预留 AI 模型接入接口，未来替换 chat() 中的实现即可。
 */

const API_BASE = "/api";

/**
 * 发送用户消息，获取 AI 回复
 * @param {string} message - 用户输入的消息
 * @param {Array}  history - 对话历史记录 [{role: "user"|"assistant", content: string}]
 * @returns {Promise<{reply: string}>}
 */
export async function chat(message, history = []) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

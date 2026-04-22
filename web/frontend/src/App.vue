<script setup>
import { ref, nextTick } from "vue";
import { chat } from "./api/chat.js";

const messages = ref([]);
const inputText = ref("");
const isLoading = ref(false);

// 预留：AI 角色配置，未来可扩展
const AI_ROLE = "assistant";

function buildHistory() {
  return messages.value.map((m) => ({
    role: m.role,
    content: m.content,
  }));
}

async function sendMessage() {
  const text = inputText.value.trim();
  if (!text || isLoading.value) return;

  // 添加用户消息
  messages.value.push({ role: "user", content: text });
  inputText.value = "";
  isLoading.value = true;

  await nextTick();
  scrollToBottom();

  try {
    const { reply } = await chat(text, buildHistory());
    messages.value.push({ role: AI_ROLE, content: reply });
  } catch (err) {
    messages.value.push({
      role: AI_ROLE,
      content: `请求失败: ${err.message}，请检查后端服务是否启动。`,
    });
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
}

function scrollToBottom() {
  const el = document.querySelector(".chat-messages");
  if (el) el.scrollTop = el.scrollHeight;
}

function clearChat() {
  messages.value = [];
}
</script>

<template>
  <div class="app-container">
    <!-- 顶部标题栏 -->
    <header class="app-header">
      <span class="app-title">ProductInfo AGI</span>
      <button class="btn-clear" @click="clearChat">清空对话</button>
    </header>

    <!-- 消息列表 -->
    <main class="chat-messages" role="log" aria-live="polite">
      <div v-if="messages.length === 0" class="empty-hint">
        <div class="empty-icon">💬</div>
        <p>发送一条消息开始对话</p>
      </div>

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        class="message-row"
        :class="msg.role"
      >
        <div class="avatar">{{ msg.role === "user" ? "U" : "AI" }}</div>
        <div class="bubble">{{ msg.content }}</div>
      </div>

      <div v-if="isLoading" class="message-row assistant">
        <div class="avatar">AI</div>
        <div class="bubble loading">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </main>

    <!-- 底部输入区 -->
    <footer class="chat-input-bar">
      <textarea
        v-model="inputText"
        class="chat-textarea"
        placeholder="输入消息，按 Ctrl+Enter 或点击发送..."
        rows="1"
        :disabled="isLoading"
        @keydown.enter.ctrl="sendMessage"
        @input="
          $event.target.style.height = 'auto';
          $event.target.style.height = $event.target.scrollHeight + 'px';
        "
      ></textarea>
      <button
        class="btn-send"
        :disabled="isLoading || !inputText.trim()"
        @click="sendMessage"
      >
        发送
      </button>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 800px;
  margin: 0 auto;
  background-color: #161b22;
  border-left: 1px solid #30363d;
  border-right: 1px solid #30363d;
}

/* ── Header ──────────────────────────────────────── */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid #30363d;
  background-color: #0d1117;
  flex-shrink: 0;
}

.app-title {
  font-size: 16px;
  font-weight: 600;
  color: #58a6ff;
  letter-spacing: 0.5px;
}

.btn-clear {
  background: transparent;
  border: 1px solid #30363d;
  color: #8b949e;
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
}

.btn-clear:hover {
  color: #e6edf3;
  border-color: #8b949e;
}

/* ── Messages ─────────────────────────────────────── */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
  color: #8b949e;
  user-select: none;
}

.empty-icon {
  font-size: 48px;
  line-height: 1;
}

.empty-hint p {
  font-size: 14px;
}

.message-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-row.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.message-row.user .avatar {
  background: #238636;
  color: #fff;
}

.message-row.assistant .avatar {
  background: #1f6feb;
  color: #fff;
}

.bubble {
  max-width: 72%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
}

.message-row.user .bubble {
  background: #238636;
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

.message-row.assistant .bubble {
  background: #21262d;
  color: #e6edf3;
  border: 1px solid #30363d;
  border-bottom-left-radius: 4px;
}

/* ── Loading dots ─────────────────────────────────── */
.bubble.loading {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 12px 18px;
}

.dot {
  width: 7px;
  height: 7px;
  background: #8b949e;
  border-radius: 50%;
  animation: blink 1.2s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%,
  80%,
  100% {
    opacity: 0.3;
  }
  40% {
    opacity: 1;
  }
}

/* ── Input bar ─────────────────────────────────────── */
.chat-input-bar {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  padding: 14px 16px;
  border-top: 1px solid #30363d;
  background-color: #0d1117;
  flex-shrink: 0;
}

.chat-textarea {
  flex: 1;
  resize: none;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 10px;
  color: #e6edf3;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  padding: 10px 14px;
  outline: none;
  max-height: 160px;
  overflow-y: auto;
  transition: border-color 0.2s;
}

.chat-textarea:focus {
  border-color: #58a6ff;
}

.chat-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-send {
  background: #238636;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 20px;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s, opacity 0.2s;
}

.btn-send:hover:not(:disabled) {
  background: #2ea043;
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

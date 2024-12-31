<template>
  <v-container :height="containerHeight" class="container">
    <div class="div_messages" ref="div_messages_ref">
      <div class="messages">
        <div
          v-for="(message, index) in chatHistory"
          :key="index"
          class="message"
          :class="message.role"
        >
          <div class="ma-2 pa-2" :class="message.role">
            <v-icon
              start
              icon="mdi-account"
              v-if="message.role === 'user'"
              color="blue"
            ></v-icon>
            <v-icon
              start
              icon="mdi-headset"
              v-if="message.role === 'agent'"
              color="green"
            ></v-icon>
            {{ message.text }}
            <span style="color: gray; margin-left: 5px">{{
              message.time
            }}</span>
          </div>
        </div>
      </div>
      <div v-if="isWaitingForReply" class="waiting">请稍候...</div>
    </div>

    <v-container class="div_input">
      <v-text-field
        v-model="newMessage"
        label="请输入您的问题"
        type="text"
        variant="outlined"
        clearable
        append-inner-icon="mdi-send"
        @click:append-inner="sendMessage"
        @keyup.enter="sendMessage"
        :disabled="isWaitingForReply"
      >
        <template v-slot:prepend>
          <v-tooltip location="bottom">
            <template v-slot:activator="{ props }">
              <v-icon v-bind="props" icon="mdi-help-circle-outline"></v-icon>
            </template>

            {{ tootTip }}
          </v-tooltip>
        </template>

        <template v-slot:append-inner>
          <v-fade-transition leave-absolute>
            <v-progress-circular
              v-if="isWaitingForReply"
              color="info"
              size="24"
              indeterminate
            ></v-progress-circular>
          </v-fade-transition>
        </template>

        <template v-slot:append>
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" class="mt-n2">
                <v-icon icon="mdi-menu"></v-icon>
              </v-btn>
            </template>

            <v-card>
              <v-card-text class="pa-6">
                <v-btn color="primary" variant="text" @click="clearChatHistory">
                  <v-icon icon="mdi-delete" start></v-icon>

                  清空聊天记录
                </v-btn>
              </v-card-text>
            </v-card>
          </v-menu>
        </template>
      </v-text-field>
    </v-container>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed, watch } from "vue";

const serviceInfo = {
  name: "consult",
  url: "http://127.0.0.1:8000/consulting/ask/v1",
};

const tootTip = ref("获取更多帮助，请联系Email:56008507@qq.com");
const isWaitingForReply = ref(false);
const newMessage = ref("");

// 处理聊天历史记录
const chatHistory = reactive([]);

const saveChatHistory = () => {
  localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
};

const clearChatHistory = () => {
  chatHistory.splice(0, chatHistory.length);
  saveChatHistory();
};

const loadChatHistory = () => {
  const savedHistory = localStorage.getItem("chatHistory");
  if (savedHistory) {
    for (let item of JSON.parse(savedHistory)) {
      item.time = getFriendlyTime(item.rawTime);
      chatHistory.push(item);
    }
  }
};

// 发送消息
import instance from "@/assets/js/axiosInstance";

const sendMessage = () => {
  newMessage.value = newMessage.value.trim();
  if (!newMessage.value.trim()) return;
  let rawTime = getCurrentTime();
  chatHistory.push({
    role: "user",
    text: newMessage.value.trim(),
    rawTime: rawTime,
    time: getFriendlyTime(rawTime),
  });
  let q = newMessage.value;
  newMessage.value = "";
  saveChatHistory();

  isWaitingForReply.value = true;

  instance
    .post(serviceInfo.url, {
      question: q,
    })
    .then(
      (response) => {
        let resTime = getCurrentTime();
        let answer = response.data.desc;
        chatHistory.push({
          role: "agent",
          text: answer,
          rawTime: resTime,
          time: getFriendlyTime(resTime),
        });
        isWaitingForReply.value = false;
        saveChatHistory();
      },
      (error) => {
        console.log(error);
        newMessage.value = error.message;
        isLoading.value = false;
        if (error.response && error.response.status === 401) {
          emits("navigate", "/" + serviceInfo.name);
        }
      }
    );
};

// 处理时间格式
const getCurrentTime = () => {
  const now = new Date();
  return formatTime(now);
};

// 把时间格式化为：xxxx年XX月XX日 XX:XX 格式。
const formatTime = (time) => {
  const year = time.getFullYear();
  const month = (time.getMonth() + 1).toString().padStart(2, "0"); // 月份是从0开始的
  const day = time.getDate().toString().padStart(2, "0");
  const hours = time.getHours().toString().padStart(2, "0");
  const minutes = time.getMinutes().toString().padStart(2, "0");

  const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}`;
  return formattedDate;
};

// 把消息时间转换成比较友好的显示形式
const getFriendlyTime = (dateStr) => {
  // 解析日期字符串
  const inputDate = new Date(dateStr);

  // 获取当前日期并重置时间为00:00:00
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  // 获取昨天的日期并重置时间为00:00:00
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  // 格式化小时和分钟
  const hours = inputDate.getHours().toString().padStart(2, "0");
  const minutes = inputDate.getMinutes().toString().padStart(2, "0");

  // 比较日期并返回格式化字符串
  if (inputDate >= today) {
    // 如果是今天
    return `${hours}:${minutes}`;
  } else if (inputDate >= yesterday) {
    // 如果是昨天
    return `昨天 ${hours}:${minutes}`;
  } else {
    // 如果是其它时间
    const year = inputDate.getFullYear();
    const month = (inputDate.getMonth() + 1).toString().padStart(2, "0");
    const day = inputDate.getDate().toString().padStart(2, "0");
    return `${year}年${month}月${day}日 ${hours}:${minutes}`;
  }
};

const div_messages_ref = ref(null);

// 监听内容变化
watch(chatHistory, async () => {
  // 等待 DOM 更新完成后滚动
  await nextTick();
  if (div_messages_ref.value) {
    //console.log("div_messages_ref:", div_messages_ref.value);
    div_messages_ref.value.scrollTop = div_messages_ref.value.scrollHeight;
  }
});

// 滚动到div的最下面
const scrollToBottom = () => {
  if (div_messages_ref.value) {
    //console.log(div_messages_ref.value);
    div_messages_ref.value.scrollTop = div_messages_ref.value.scrollHeight;
  }
};

onMounted(() => {
  loadChatHistory();
  scrollToBottom();
});

const containerHeight = computed(() => {
  return "calc(100vh - 64px)"; //toolbar默认高度是64px，这样刚好可以填满整个屏幕
});
</script>


<style>
.container {
  display: flex;
  flex-direction: column;
}
.div_messages {
  flex: 1; /* div_messages填充剩余空间 */
  overflow-y: auto; /* 超出高度时显示垂直滚动条 */
  padding-bottom: 16px;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.div_input {
  display: flex;
  align-items: stretch; /* 确保子元素（input）与div_input高度相同 */
  margin: 0; /* 移除默认边距 */
  padding: 0; /* 移除默认内边距 */
}

.message {
  display: flex;
  align-items: center;
  max-width: 80%;
  padding: 8px;
  border-radius: 8px;
}
.message.user {
  align-self: flex-end;
}
.message.agent {
  align-self: flex-start;
}

.waiting {
  text-align: center;
  margin-top: 10px;
  font-style: italic;
}
</style>
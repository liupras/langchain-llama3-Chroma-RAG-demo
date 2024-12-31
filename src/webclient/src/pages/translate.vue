<template>
  <v-container class="translation-page" fluid>
    <v-overlay :model-value="isLoading" class="justify-center align-center">
      <v-progress-circular indeterminate color="white"></v-progress-circular>
    </v-overlay>
    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-select
          v-model="targetLanguage"
          :items="languages"
          label="目标语言"
          outlined
        ></v-select>
      </v-col>
    </v-row>

    <v-form @submit.prevent>
      <v-row>
        <v-col cols="12">
          <v-textarea
            v-model="textToTranslate"
            label="输入待翻译的文字"
            outlined
            :rules="[rules.required, rules.max]"
            counter="1000"
          ></v-textarea>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-btn
            type="submit"
            @click="translateText"
            color="primary"
            class="mt-4"
            >翻译</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
    <v-row>
      <v-col cols="12">
        <v-card class="mt-4">
          <v-card-title>翻译结果</v-card-title>
          <v-card-text>
            {{ translatedText || "翻译后的文字将显示在此处" }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

const serviceInfo = {
  name: "translate",
  url: "http://127.0.0.1:8000/translation/trans/v1",
};


const languages = ref(["英语", "中文", "日语", "法语", "德语", "西班牙语"]);
const sourceLanguage = ref("中文");
const targetLanguage = ref("英语");
const textToTranslate = ref("");
const translatedText = ref("");

const isLoading = ref(false);

//校验规则
const rules = {
  required: (value) => !!value || "不能为空。",
  max: (value) => value.length <= 1000 || "最多1000个字符。",
};

const textLimitRule = (value) => {
  if (value && value.length > 1000) {
    return "文本长度不能超过1000个字符。";
  }
  return true;
};

import instance from "@/assets/js/axiosInstance";

const emits = defineEmits(["navagate"]);

const translateText = () => {
  let text = textToTranslate.value.trim();
  if (targetLanguage.value === "" || text === "") {
    return;
  }

  translatedText.value = "翻译正在进行中，请耐心等候...";
  isLoading.value = true;

  instance
    .post(serviceInfo.url, {
      lang: targetLanguage.value,
      text: text,
    })
    .then(
      (response) => {
        translatedText.value = response.data.desc;
        isLoading.value = false;
      },
      (error) => {
        console.log(error);        
        translatedText.value = error.message;
        isLoading.value = false;
        if (error.response && error.response.status === 401) {            
            emits("navigate","/"+serviceInfo.name);
        }
      }
    );
};
</script>

<style scoped>
.translation-page {
  max-width: 800px;
  margin: auto;
}
</style>
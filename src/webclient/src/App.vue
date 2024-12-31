<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
    >
      <v-list-item
        prepend-avatar="@/assets/image/liupras.jpg"
        title="大模型客户端"
        nav
      >
        <template v-slot:append>
          <v-btn
            icon="mdi-chevron-left"
            variant="text"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="(item, i) in menuItems"
          :key="i"
          :prepend-icon="item.icon"
          :title="item.title"
          :value="item.value"
          @click="navigate(item.route)"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar density="compact" style="padding-right: 1%">
      <v-container
        style="width: 200px; text-align: bottom; padding-bottom: 0px"
      >
        <v-app-bar-title>
          <v-btn icon="mdi-home-variant" to="/"></v-btn>
          <!--
          <v-select
            label="选择大模型"
            density="compact"
            single-line
            v-model="model_select"
            :items="model_list"
            item-title="name"
            item-value="value"
          ></v-select>-->
        </v-app-bar-title>
      </v-container>

     <v-spacer></v-spacer>
      <v-btn icon @click="changeTheme" style="margin-right: 4%">
        <v-icon
          :icon="myTheme ? 'mdi-weather-night' : 'mdi-weather-sunny'"
        ></v-icon>
      </v-btn>

      <v-btn class="primary" variant="outlined" to="/login" v-if="!isLoggedIn">
        登录
      </v-btn>
      <div v-else>
        <v-chip prepend-icon="mdi-account-outline">{{userName}}</v-chip>
        <v-btn icon="mdi-exit-to-app" @click="onLogout" ></v-btn>
      </div>      
    </v-app-bar>

    <v-main style="margin: 16px">
      <router-view  @login="onLogin" @navigate="navigate" v-slot="{ Component }">
        <v-slide-x-reverse-transition>
          <component :is="Component" />
        </v-slide-x-reverse-transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from "vue";

const drawer = ref(true);
const rail = ref(true);
const userName = ref("未登录");

// 处理登录登出状态
import { logout, checkLoggedIn,getUserId } from "@/assets/js/auth";
const isLoggedIn = ref(false);

let userId = getUserId();
if (userId) {
  userName.value = userId;
  isLoggedIn.value = true;
}

function onLogin(name) {
  //console.log("username is:", name);
  userName.value = name;
  isLoggedIn.value = true;
}

function onLogout() {
  logout();
  isLoggedIn.value = false;
}

// 处理切换主题
import { useTheme } from "vuetify";
const myTheme = ref(true);
const theme = useTheme();

function changeTheme() {
  myTheme.value = !myTheme.value;
  theme.global.name.value = myTheme.value ? "dark" : "light";
}

// 选择大模型
/*
const model_select = ref({ name: "llama", value: "llama3.1" });
const model_list = ref([{ name: "llama", value: "llama3.1" }]);
*/

// 菜单
const menuItems = ref([
  {
    icon: "mdi-comment-question-outline",
    title: "咨询",
    value: "consult",
    route: "/consult",
  },
  {
    icon: "mdi-translate",
    title: "翻译",
    value: "translate",
    route: "/translate",
  },
]);

// 获取路由实例
import { useRouter } from "vue-router";
const router = useRouter();

// 导航方法
const navigate = (route) => {
  //console.log("route is:",route);
  if (route == "/") {
    router.push(route);
  } else {
    if (checkLoggedIn()) {
      router.push(route);
    } else {
      router.push({ path: "/login", query: { redirect: route } });
    }
  }
};
</script>

<style>
</style>

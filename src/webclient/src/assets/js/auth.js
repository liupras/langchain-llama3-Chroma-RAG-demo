import { reactive } from 'vue';
import { jwtDecode } from "jwt-decode";

const state = reactive({
  token: null,
});

const token_name = 'token_liupras';

const setToken = (token) => { 
  state.token = token;
  localStorage.setItem(token_name, token);
};


const getToken = () => {
  if (!state.token) {
    state.token = localStorage.getItem(token_name);
  }
  return state.token;
};

const getUserId =() => {
  const token = getToken();
  if (token) {
    const decodedToken = jwtDecode(token);

    // 校验过期时间
    let exp_str = decodedToken['exp'];    
    let exp = parseInt(exp_str);   
    let now = parseInt(Date.now()/1000);    //转换为秒
    if (exp > now) {
      let diffDays = Math.floor((exp-now) / (60 * 60 * 24));
      console.log("token还有"+diffDays+"天过期。");
      return decodedToken.sub;
    }else{
      return null;
    }    
  }else{
    return null;
  }
};

const logout = () => {
  state.token = null;
  localStorage.removeItem(token_name);
};

const checkLoggedIn = () => {
  return !!getUserId();
};

export {setToken, getToken, logout, checkLoggedIn,getUserId};

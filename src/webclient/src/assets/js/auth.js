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
    return decodedToken.sub;
  }
  return null;
};

const logout = () => {
  state.token = null;
  localStorage.removeItem(token_name);
};

const checkLoggedIn = () => {
  return !!getToken();
};

export {setToken, getToken, logout, checkLoggedIn,getUserId};

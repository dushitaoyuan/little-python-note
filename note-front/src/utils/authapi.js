import axios from "../axios";
import webCache from 'web-storage-cache'
import $ from 'jquery'
import CryptoJS from 'crypto-js'
import ElementUI from 'element-ui';
import systemUtil from "./systemUtil";

var wsCache = new webCache();

var authApi = {
  /**
   *认证接口
   */
  auth(loginForm, noMsg) {
    if (!loginForm.loginType) {
      loginForm.loginType = 1;
    }
    var newLoginForm = JSON.parse(JSON.stringify(loginForm));
    if (loginForm.password) {
      newLoginForm.password = CryptoJS.SHA256(loginForm.password).toString(CryptoJS.enc.Hex)
    }
    $.ajax({
      type: "post",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(newLoginForm),
      async: false,
      url: axios.API_BASE_PATH + "login"
    }).done(
      function (result) {
        if (result.code == 1) {
          authApi.handleTokenData(result.data)
          if (!noMsg) {
            ElementUI.Message.success("登录成功")
          }
          systemUtil.vueApp.$router.push("/index")
          return;
        }
        if (result.msg) {
          ElementUI.Message.error(result.msg)
        }
      });
  },
  authRefresh() {
    var refreshToken = wsCache.get('refresh_token');
    if (!refreshToken) {
      $.ajax({
        type: "post",
        url: axios.API_BASE_PATH + "token/refresh",
        data: {refreshToken: refreshToken},
        async: false,
        dataType: "json",
      }).done(
        function (result) {
          if (result.code == 1) {
            authApi.handleTokenData(result.data)
          }
        });
    }
  },
  handleTokenData(tokenData) {
    var expire = tokenData.expire;
    var refreshExpire = parseInt(expire * 1.5, 10);
    wsCache.set('api_token', tokenData.api_token, {exp: expire});
    wsCache.set('refresh_token', tokenData.refresh_token, {exp: refreshExpire});
    wsCache.set('username', tokenData.username, {exp: refreshExpire});
    if (tokenData.remember_me_token) {
      wsCache.set('remember_me_token', tokenData.remember_me_token, {exp: tokenData.remember_me_expire - 30 * 60});
    }
  },
  getToken() {
    var apiToken = wsCache.get('api_token');
    if (apiToken) {
      return apiToken;
    }
    this.authRefresh();
    return wsCache.get('api_token');
  },
  isLogin() {
    if (webCache.get("api_token")) {
      return true;
    }
    return false;
  },
  isRemermber() {
    var remember_me_token = wsCache.get('remember_me_token');
    if (remember_me_token) {
      return true;
    }
    return false;
  },
  autoRemmeberLogin() {
    //没登录,免密登录
    if (authApi.isLogin()) {
      return;
    }
    if (isRemember()) {
      authApi.auth({remember_me_token: remember_me_token, loginType: 2}, true)
    }
  }
}
export default authApi;

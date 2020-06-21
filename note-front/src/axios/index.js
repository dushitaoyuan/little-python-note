/* eslint-disable */

import Vue from 'vue';
import axios from 'axios';
import qs from 'qs'
import systemUtil from "../utils/systemUtil";
import authApi from "../utils/authapi"
import ElementUI from 'element-ui';


//参数序列化(默认json)，全局处理等操作
var myAxios = axios.create({
  headers: {
    'Content-Type': 'application/json'
  },
  transformRequest: [function (data, headers) {
    let requestType = headers['Content-Type'];
    if (requestType) {
      requestType = requestType.toLowerCase();
      //json处理
      if (requestType.indexOf('json') > 0) {
        return JSON.stringify(data);
      }
      //form处理
      if (requestType.indexOf('x-www-form-urlencoded') > 0) {
        return qs.stringify(data, {arrayFormat: 'repeat'});
      }
    }
  }]
});
let publicUrl = ['/login', '/token/refresh', '/logout']

myAxios.API_BASE_PATH = 'http://localhost:8080/api/';
myAxios.VIRTUAL_BASE_PATH = "/note-api/";
myAxios.interceptors.request.use((config) => {
    /**
     * 基础路径替换
     */
    if (config.url.indexOf(myAxios.VIRTUAL_BASE_PATH) == 0) {
      config.url = myAxios.API_BASE_PATH + config.url.substr(myAxios.VIRTUAL_BASE_PATH.length);
    }
    /**
     * 添加header token
     */
    if (isPublic(config.url)) {
      config.headers.token = authApi.getToken();
      return config;
    }

    return config;
  },
  (error) => {
    isLoadingInstance()
    return Promise.reject(error);
  }
)
//axios 异常判断
myAxios.interceptors.response.use(
  response => {
    if (response.status != 200) {
      return Promise.reject(response);
    }
    if (response.status === 200 && !isSuccess(response.data)) {
      errorHandle(response.data)
      return Promise.reject(response);
    }
    return response
  },
  err => {
    return Promise.reject(err)
  }
)

function errorHandle(data) {
  console.error("error code" + data.code)
  ElementUI.Message.error(data.msg);
}

function isSuccess(data) {
  if (data.code == 1) {
    return true;
  }
  return false;
}


function isPublic(url) {
  for (var rule in publicUrl) {
    if (url.indexOf(rule) > -1) {
      return true;
    }
  }
  return false;
}


Vue.prototype.$axios = myAxios;

export default myAxios

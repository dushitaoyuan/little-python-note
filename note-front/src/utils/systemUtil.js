//系统工具
import webCache from 'web-storage-cache'

var wsCache = new webCache();
var systemUtil = {
  vueApp: {},
  getUsername() {
    return wsCache.get("username")
  }
}
export default systemUtil

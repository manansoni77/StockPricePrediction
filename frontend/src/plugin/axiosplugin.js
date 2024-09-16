import axios from "axios";

const axiosPlugin = {
  install(Vue) {
    Vue.prototype.$axios = axios;
    Vue.prototype.$setupAxios = function () {
      // this.$axios.defaults.baseURL = "http://localhost:5000/";
      this.$axios.defaults.headers["Content-Type"] = "application/json";
    };
  },
};

export default axiosPlugin;

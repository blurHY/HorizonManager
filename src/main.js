import Vue from "vue"
import App from "./App"
import router from "./router/index"
import PaperDashboard from "./plugins/paperDashboard"
import Notify from 'vue-notifyjs'
import 'font-awesome/css/font-awesome.css'
import "vue-notifyjs/themes/default.css"
import VueSocketIO from 'vue-socket.io'

Vue.use(new VueSocketIO({
  debug: true,
  connection: 'http://127.0.0.1:5000'
}))

Vue.use(PaperDashboard);
Vue.use(Notify)

/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App),
  data() {
    return {
      logs: []
    }
  }
}).$mount("#app");
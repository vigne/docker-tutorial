import Vue from 'vue'
import App from './App.vue'
import router from './router'

// import VueAxios from 'vue-axios'

import './../node_modules/bulma/css/bulma.css';

// import BSON from 'bson'

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})

// Vue.use(VueAxios, axios, BSON)

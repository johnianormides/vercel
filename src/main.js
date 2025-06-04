import { createPinia } from 'pinia'
import { createApp } from 'vue'

import '@fortawesome/fontawesome-free/css/all.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
// Disable devtools
app.config.devtools = false;
app.config.debug = false;
app.config.silent = true;
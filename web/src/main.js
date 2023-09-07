
import './assets/main.css';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import MarkdownIt from 'markdown-it'

const app = createApp(App)

app.use(router)
app.use(MarkdownIt)

app.mount('#app')

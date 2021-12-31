import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import router from './router/router'
import axios from 'axios'

const app = createApp(App)
app.use(router)
app.mount('#app')


axios.interceptors.request.use(
    config => {
        const auth = localStorage.getItem('Authorization')
        if (auth) {
            config.headers.Authorization = auth
        }
        return config
    },
    err => {
        router.push('/login')
        return Promise.reject(err)
    }
)

axios.interceptors.response.use(
    response => {
        return new Promise((resolve, reject) => {
           let data = response.data;
           if (response.status == 200) {
              return resolve(response);
           } else {
              return reject(response)
           }
        });
     },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    localStorage.removeItem('Authorization');
                    router.push('/login')
                    break;
                default:
                    return error.response
            }
        }
        return Promise.reject(error)
    }
)
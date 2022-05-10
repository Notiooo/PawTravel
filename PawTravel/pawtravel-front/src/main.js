import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons.js';

// loads the Icon plugin
UIkit.use(Icons);

// components can be called from the imported UIkit reference
// UIkit.notification('Hello world.');


createApp(App).use(router).mount('#app')
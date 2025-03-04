import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Import Vue Router
import "./assets/styles.css"; // Global CSS

const app = createApp(App);
app.use(router); // Use Router
app.mount("#app");

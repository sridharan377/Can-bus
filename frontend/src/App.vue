<template>
  <div class="container">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo-container">
        <img src="./assets/logo.png" alt="Logo" class="logo" />
        <h1>CAN Network Monitoring</h1>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link"> Home </router-link>
        <router-link to="/analysis" class="nav-link"> Analysis </router-link>
        <router-link to="/contact" class="nav-link"> Contact </router-link>
      </div>
    </nav>

    <!-- Router View -->
    <router-view />

    <!-- Main Content -->
    <div class="content">
      <!-- Left Panel: Real-Time Packet Table -->
      <div class="left-panel">
        <h2>Real-Time CAN Packets</h2>
        <CANMessage :messages="messages" @message-clicked="openDetail" />
      </div>

      <!-- Right Panel: Graph Visualization -->
      <div class="right-panel">
        <h2>Graph Visualization</h2>
        <GraphVisualization :messages="messages" />
      </div>
    </div>

    <!-- Message Detail Modal -->
    <MessageDetailModal
      v-if="showModal"
      :message="selectedMessage"
      @close="closeModal"
    />
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { io } from "socket.io-client";
import CANMessage from "./components/CANMessage.vue";
import GraphVisualization from "./components/GraphVisualization.vue";
import MessageDetailModal from "./components/MessageDetailModal.vue";

export default {
  components: { CANMessage, GraphVisualization, MessageDetailModal },
  setup() {
    const messages = ref([]);
    const showModal = ref(false);
    const selectedMessage = ref(null);
    const socket = io(import.meta.env.VITE_BACKEND_URL || "/");

    onMounted(async () => {
    
      try {
              
        // Fetch static API data from Firebase Hosting
        const response = await fetch("/api/hello.json");
        const data = await response.json();
        console.log("Fetched initial API data:", data);
        
        // Push initial API data into messages list
        messages.value.push({
          id: "API_Initial",
          message: data.message,
          timestamp: new Date().toLocaleTimeString(),
          type: "System",
        });
      } catch (error) {
        console.error("Error fetching API data:", error);
      }
      socket.on("new_message", (data) => {
        console.log("Received message from backend:", data);
        // Add a timestamp and assign a type based on message id
        data.timestamp = new Date().toLocaleTimeString();
        data.type = data.id === "0x666" ? "Malicious" : "Normal";
        
        console.log("Debug: Full Message received:", JSON.stringify(data,null,2));
        messages.value = [...messages.value, data];
        
        console.log("Updated messages array:", messages.value);
      });
    });

    const openDetail = (message) => {
      selectedMessage.value = message;
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
      selectedMessage.value = null;
    };

    return { messages, showModal, selectedMessage, openDetail, closeModal };
  },
};
</script>

<style scoped>
/* General Styles */
.container {
  font-family: Arial, sans-serif;
  background: #121212;
  color: #fff;
  padding: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #111;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0,255,128, 0.5);
  border-bottom: 2px solid #00ffcc;
  /*position: sticky;*/
  /*top: 0;*/
  /*z-index: 100;*/
  
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 50px;
  margin-right: 10px;
  width: 40px;
}

h1 {
  font-size: 1.5rem;
}

/* Navigation Links */
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-link {
  color: #00ffcc;
  margin: 0 15px;
  font-weight: bold;
  text-decoration: none;
  
  transition: color 0.3s;
}

.nav-link:hover {
  color: #ff00ff;
}

/* Content Section */
.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

/* Left Panel */
.left-panel, .right-panel {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
}

.left-panel {
  overflow-y: auto;
  max-height: 600px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .content {
    grid-template-columns: 1fr;
  }

  .navbar {
    flex-direction: column;
    text-align: center;
  }

  .nav-links {
    margin-top: 10px;
  }
}
</style>

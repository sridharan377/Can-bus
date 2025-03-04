<template>
  <div class="home">
  <div class= "cyber-circuit"></div>
    <div class="cyber-bg"></div>
    <div class="content">
      <h1>Welcome to CAN Bus Monitoring</h1>
      <p>This tool helps visualize real-time CAN messages.</p>
    </div>
  </div>
</template>

<style scoped>
.home {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* Cyber Grid Background */
.cyber-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(0, 255, 128, 0.3) 0%, rgba(0, 0, 0, 0.9) 80%);
  animation: flicker 3s infinite alternate;
}

@keyframes flicker {
  0% { opacity: 0.8; }
  100% { opacity: 1; }
}

.content {
  padding: 20px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 10px;
  text-align: center;
  color: white;
  z-index: 1;
}
</style>

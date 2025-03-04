<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <button class="close-btn" @click="close">X</button>
      <h2>Message Details</h2>
      <p><strong>ID:</strong> {{ message.id }}</p>
      <p><strong>Data:</strong> {{ message.data }}</p>
      <p><strong>Timestamp:</strong> {{ message.timestamp }}</p>
      <p><strong>Type:</strong> {{ message.type }}</p>
      <p><strong>CRC:</strong> {{ message.crc }}</p>
      <p><strong>ACK:</strong> {{ message.ack }}</p>
      <p><strong>RTR:</strong> {{ message.rtr }}</p>
      <p><strong>Bus Load:</strong> {{ message.busLoad }}%</p>
      <p><strong>Frequency:</strong> {{ message.frequency }} Hz</p>
      <p><strong>Analysis:</strong> Detailed analysis goes here. You can add logs, historical data, or any other insights you'd like to display.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ["message"],
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 8px;
  position: relative;
  width: 80%;
  max-width: 500px;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #ff4d4d;
  border: none;
  color: white;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
}
</style>

<template>
  <div class="analysis">
    <h1>CAN Bus Data Analysis</h1>
    
        <CanMessage :messages="messages" />
        <GraphVisalization :messages="messages" />

  </div>
  
</template>

<script>
import { ref } from "vue";
import CanMessage from '@/components/CANMessage.vue';
import GraphVisualization from '@/components/GraphVisualization.vue';

export default {
  components: {
    CanMessage,
    GraphVisualization,
  },
  setup() {
     const messages = ref([]);
     return { messages };
  },
};
</script>

<style scoped>
.analysis {
  text-align: center;
  padding: 50px;
  color: #00ffcc;
  text-shadow: 0 0 10px #00ffcc;
  font-family: "Orbitron", sans-serif;
}



</style>

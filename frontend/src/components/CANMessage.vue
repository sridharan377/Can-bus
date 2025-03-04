<template>
  <div class="table-container">
    <table class="styled-table">
      <thead>
        <tr>
          <th>Message ID</th>
          <th>Data</th>
          <th>Timestamp</th>
          <th>Type</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(msg, index) in messages"
          :key="index"
          @click="$emit('message-clicked', msg)"
          :class="{'malicious': msg.type === 'Malicious', 'normal': msg.type === 'Normal'}"
        >
          <td>{{ msg.id }}</td>
          <td>{{ msg.data }}</td>
          <td>{{ msg.timestamp }}</td>
          <td>
             <span v-if="msg.type === 'Malicious'" class = "warning"> {{ msg.type }} /span>
             span v-else>{{msg.type}}</span>
          </td>
          
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ["messages"],
};
</script>

<style scoped>
.table-container {
  max-height: 600px; /* Fixed height for scrolling */
  overflow-y: auto;
  border: 1px solid #444;
  border-radius: 4px;
}
.styled-table {
  width: 100%;
  border-collapse: collapse;
}
.styled-table th,
.styled-table td {
  padding: 8px;
  border: 1px solid #444;
  text-align: left;
}
.styled-table tr:hover {
  background: #333;
  cursor: pointer;
}
.styled-table tr.malicious {
  background-color: #4d0000;
}
.styled-table tr.normal:hover {
  background-color: #2e2e2e;
}
.warning {
  color: red;
  font-weight: bold;
}
</style>

<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import Chart from "chart.js/auto";

export default {
  props: ["messages"],
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null;

    onMounted(() => {
      if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext("2d");
        // Create a vertical gradient for the line
        let gradient = ctx.createLinearGradient(0, 0, 0, 500);
        gradient.addColorStop(0, 'rgba(58,123,213,1)');
        gradient.addColorStop(1, 'rgba(0,210,255,0.3)');

        chartInstance = new Chart(ctx, {
          type: "line",
          data: {
            labels: [],
            datasets: [
              {
                label: "Message Count",
                data: [],
                borderColor: gradient,
                backgroundColor: 'rgba(0,210,255,0.3)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgba(58,123,213,1)',
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                labels: {
                  color: "#fff",
                  font: { size: 14 }
                }
              }
            },
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: "Time",
                  color: "#fff",
                  font: { size: 14 },
                },
                ticks: { color: "#fff" },
                grid: { color: "rgba(255,255,255,0.1)" }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: "Message Count",
                  color: "#fff",
                  font: { size: 14 },
                },
                ticks: { color: "#fff" },
                grid: { color: "rgba(255,255,255,0.1)" },
                beginAtZero: true,
              },
            },
          },
        });
      }
    });

    // Watch for changes in messages count and update the chart accordingly
    watch(
      () => props.messages.length,
      (newLength) => {
        if (chartInstance) {
          const now = new Date().toLocaleTimeString();
          chartInstance.data.labels.push(now);
          chartInstance.data.datasets[0].data.push(newLength);

          // Keep only the latest 20 data points
          if (chartInstance.data.labels.length > 20) {
            chartInstance.data.labels.shift();
            chartInstance.data.datasets[0].data.shift();
          }
          chartInstance.update();
        }
      }
    );

    return { chartCanvas };
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 500px; /* fixed width */
  height: 500px;      /* fixed height to keep it square */
  margin: 0 auto;
  background: #1e1e1e;
  border: 2px solid #333;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>

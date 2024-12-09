<template>
    <div class="bar-chart">
      <canvas ref="chart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  
  export default {
    props: {
      data: {
        type: Array,
        default: () => [],
      },
    },
    mounted() {
      this.renderChart();
    },
    watch: {
      data: 'renderChart',
    },
    methods: {
      renderChart() {
        if (this.chart) {
          this.chart.destroy();
        }
        const ctx = this.$refs.chart.getContext('2d');
        this.chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: this.data.map((item) => item.label),
            datasets: [
              {
                data: this.data.map((item) => item.value),
                backgroundColor: '#6a5acd',
              },
            ],
          },
          options: {
            plugins: {
              legend: {
                display: false, // Отключение легенды
              },
            },
          },
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .bar-chart {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }
  </style>  
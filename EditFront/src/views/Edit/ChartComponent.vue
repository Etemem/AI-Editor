<template>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  const props = defineProps({
    chartData: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      default: () => ({})
    }
  })
  
  const chartCanvas = ref(null)
  let chart = null
  
  onMounted(() => {
    createChart()
  })
  
  watch(() => props.chartData, (newVal) => {
    if (chart) {
      chart.data = newVal
      chart.update()
    }
  }, { deep: true })
  
  const createChart = () => {
    const ctx = chartCanvas.value.getContext('2d')
    chart = new Chart(ctx, {
      type: 'bar',
      data: props.chartData,
      options: props.options
    })
  }
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    height: 300px;
    width: 100%;
  }
  </style>
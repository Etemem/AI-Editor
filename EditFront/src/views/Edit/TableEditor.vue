<template>
    <div class="table-editor">
      <el-table :data="tableData" style="width: 100%" height="100%" @cell-click="onCellClick">
        <el-table-column v-for="(col, index) in columns" :key="index" :prop="col" :label="col">
          <template #default="scope">
            <el-input v-model="scope.row[col]" @change="onDataChange" />
          </template>
        </el-table-column>
      </el-table>
      <el-button @click="addRow">Add Row</el-button>
      <el-button @click="addColumn">Add Column</el-button>
      <chart-component :chart-data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import ChartComponent from './ChartComponent.vue'
  
  const props = defineProps({
    initialData: {
      type: Array,
      default: () => [{ A: '', B: '' }],
    },
  })
  
  const emit = defineEmits(['update:data'])
  
  const tableData = ref(props.initialData)
  const columns = computed(() => Object.keys(tableData.value[0] || {}))
  
  const addRow = () => {
    const newRow = {}
    columns.value.forEach(col => newRow[col] = '')
    tableData.value.push(newRow)
    emit('update:data', tableData.value)
  }
  
  const addColumn = () => {
    const newColName = String.fromCharCode(65 + columns.value.length) // A, B, C, ...
    tableData.value.forEach(row => row[newColName] = '')
    emit('update:data', tableData.value)
  }
  
  const onDataChange = () => {
    emit('update:data', tableData.value)
  }
  
  const onCellClick = (row, column) => {
    // Handle cell click event if needed
  }
  
  // Chart data and options (simplified example)
  const chartData = computed(() => ({
    labels: columns.value,
    datasets: [{
      label: 'Data',
      data: tableData.value.map(row => Object.values(row).map(Number)),
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  }))
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
  }
  </script>
  
  <style scoped>
  .table-editor {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  </style>
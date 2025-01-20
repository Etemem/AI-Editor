<template>
  <div class="toolbar-container">
    <div class="toolbar-header">
      <el-icon class="toolbar-icon" :size="24">
        <Tools />
      </el-icon>
      <span class="toolbar-title">工具栏</span>
    </div>
    <div class="left-toolbar">
      <el-card v-for="tool in tools" :key="tool.name" class="tool-card" @click="activateTool(tool)">
        <el-icon>
          <component :is="tool.icon" />
        </el-icon>
        <span>{{ tool.name }}</span>
      </el-card>
      <el-dialog v-model="dialogVisible" :title="activeToolName">
        <p>{{ processingResult }}</p>
        <el-image v-if="processedImage" :src="processedImage" fit="contain" />
      </el-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElCard, ElIcon, ElDialog, ElImage } from 'element-plus'
import { Document, Microphone, Tools, Grid } from '@element-plus/icons-vue'
import axios from 'axios'

const tools = [
  { name: 'OCR识别', icon: Document, type: 'ocr', accept: 'image/*' },
  { name: '语音识别', icon: Microphone, type: 'speech', accept: 'audio/*' },
  { name: '表格识别', icon: Grid, type: 'table', accept: 'image/*' },
]

const dialogVisible = ref(false)
const activeToolName = ref('')
const processingResult = ref('')
const processedImage = ref('')

const activateTool = async (tool) => {
  activeToolName.value = tool.name

  const input = document.createElement('input')
  input.type = 'file'
  input.accept = tool.accept
  input.onchange = (event) => uploadFile(event, tool.type)
  input.click()
}

const uploadFile = async (event, type) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await axios.post(`https://k8geo688qf2e8ei3.aistudio-hub.baidu.com/api/${type}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    processingResult.value = JSON.stringify(response.data.result, null, 2)
    processedImage.value = response.data.processedImage ? `data:image/jpeg;base64,${response.data.processedImage}` : ''
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('处理失败，请重试')
    console.error(error)
  }
}
</script>

<style scoped>
.toolbar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.toolbar-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.toolbar-icon {
  margin-right: 10px;
}

.toolbar-title {
  font-size: 18px;
  font-weight: bold;
}

.left-toolbar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.tool-card {
  cursor: pointer;
  text-align: center;
}

.tool-card:hover {
  background-color: #f0f0f0;
}
</style>

<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isLogin ? '登录' : '注册' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group" v-if="!isLogin">
          <input type="text" v-model="name" required placeholder="姓名">
        </div>
        <div class="form-group">
          <input type="text" v-model="username" required placeholder="用户名">
        </div>
        <div class="form-group">
          <input type="password" v-model="password" required placeholder="密码">
        </div>
        <button type="submit" class="submit-btn">{{ isLogin ? '登录' : '注册' }}</button>
      </form>
      <p class="switch-mode" @click="toggleMode">
        {{ isLogin ? '没有账号？点击注册' : '已有账号？点击登录' }}
      </p>
      <p v-if="message" :class="['message', { 'error': isError }]">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLogin: true,
      name: '',
      username: '',
      password: '',
      message: '',
      isError: false
    }
  },
  methods: {
    async handleSubmit() {
      try {
        const url = this.isLogin ? '/api/login' : '/api/register';
        const data = this.isLogin ? 
          { username: this.username, password: this.password } :
          { name: this.name, username: this.username, password: this.password };
        
        const response = await axios.post(url, data);
        
        if (response.data.success) {
          this.message = response.data.message;
          this.isError = false;
          // 登录或注册成功,跳转到仪表板页面
          setTimeout(() => this.$router.push('/dashboard'), 1500);
        } else {
          this.message = response.data.message;
          this.isError = true;
        }
      } catch (error) {
        this.message = '发生错误,请稍后再试';
        this.isError = true;
        console.error('Error:', error);
      }
    },
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.message = '';
      this.name = '';
      this.username = '';
      this.password = '';
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
.auth-box {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 300px;
}
h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}
.submit-btn {
  width: 100%;
  padding: 0.5rem;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}
.submit-btn:hover {
  background-color: #40a9ff;
}
.switch-mode {
  text-align: center;
  margin-top: 1rem;
  color: #1890ff;
  cursor: pointer;
}
.message {
  text-align: center;
  margin-top: 1rem;
}
.error {
  color: #ff4d4f;
}
</style>
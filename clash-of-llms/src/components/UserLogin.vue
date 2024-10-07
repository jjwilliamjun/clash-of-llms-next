<template>
  <div class="login-form">
    <h2>Log In</h2>
    <form @submit.prevent="login">
      <div>
        <input type="text" v-model="username" placeholder="Enter Username" required />
      </div>
      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Enter Password" required />
        <span class="password-toggle" @click="togglePasswordVisibility">
          <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
        </span>
      </div>
      <button type="submit">Log In</button>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      showPassword: false,
    };
  },
  methods: {
    login() {
      const validUsername = 'user';
      const validPassword = 'password';

      if (this.username === validUsername && this.password === validPassword) {
        this.error = '';
        this.$emit('login-success');
      } else {
        this.error = 'Invalid username or password';
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
  },
};
</script>

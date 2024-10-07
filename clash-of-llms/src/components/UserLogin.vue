<template>
  <div class="login-form">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
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
      error: ''
    };
  },
  methods: {
    login() {
      // Replace with your predetermined username and password
      const validUsername = 'user'; // Replace with your valid username
      const validPassword = 'password'; // Replace with your valid password

      if (this.username === validUsername && this.password === validPassword) {
        this.error = '';
        this.$emit('login-success'); // Emit event on successful login
      } else {
        this.error = 'Invalid username or password'; // Show error message
      }
    }
  }
};
</script>

  
  <style scoped>
  .login {
    margin: 20px;
  }
  .error {
    color: red;
  }
  </style>
  
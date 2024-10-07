<template>
  <div class="login-form">
    <h2>Log In</h2>
    <form @submit.prevent="login">
      <div class="input-container">
        <input type="text" v-model="username" class="login-input" placeholder="Enter Username" required />
      </div>
      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" class="login-input" placeholder="Enter Password" required />
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

<style scoped>
/* Login Page Styles */
.login-form {
  max-width: 400px;
  margin: 60px auto;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.login-form h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #333;
  font-weight: bold;
}

.login-form form {
  display: flex;
  flex-direction: column;
  gap: 25px;
  align-items: center; /* Center form elements */
  width: 100%;
}

.input-container, .password-container {
  width: 100%;
}

.login-input {
  padding: 16px 18px;
  font-size: 1rem;
  border-radius: 30px; /* Rounded corners */
  border: 1px solid #ddd;
  background-color: #f0f0f0; /* Light grey background */
  box-shadow: inset 1px 1px 3px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s ease;
  width: 100%;
  max-width: 360px; /* Consistent maximum width for both inputs */
  box-sizing: border-box; /* Include padding and border in element width */
}

.login-input:focus {
  outline: none;
  border-color: #007bff;
}

.password-toggle {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #666;
}

.password-toggle:hover {
  color: #333;
}

.login-form button {
  padding: 15px;
  background-color: #ff7f50; /* Coral color for button */
  color: white;
  border: none;
  border-radius: 30px; /* Rounded corners */
  font-weight: bold;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  width: 100%;
  max-width: 360px; /* Match max-width for consistency */
}

.login-form button:hover {
  background-color: #e56739; /* Darker coral color for hover */
  transform: translateY(-2px);
}

.login-form .error-message {
  color: #d9534f;
  font-size: 1rem;
  text-align: center;
  margin-top: 10px;
}

</style>

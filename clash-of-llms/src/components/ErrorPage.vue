<template>
  <div id="app">
    <div>
      <p class="error-container">{{ errorMessage }}</p>
      <p>Please try again. If issue persists, see "Help Section" on the About Page.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    errorMessage: {
      type: String,
      default:  "An unexpected error occurred. Please try again later."
    }
  }
};
</script>
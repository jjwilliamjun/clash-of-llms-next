<template>
  <div id="app">
    <div>
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      errorMessage: this.$route.query.errorMessage || "An unexpected error occurred. Please try again later.",
    };
  },
};
</script>

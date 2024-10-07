<template>
  <div id="app">
    <nav id="app-nav">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
      <router-link to="/network">Network Graph</router-link>
      <router-link to="/preview">Preview</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}

#app-nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background-color: #a2a2a2;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

#app-nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  padding: 8px 16px;
  transition: color 0.3s, background-color 0.3s, transform 0.2s;
}

#app-nav a:hover {
  color: #0056b3;
  background-color: #c0c0c0;
  border-radius: 6px;
  transform: translateY(-2px);
}

#app-nav a.router-link-exact-active {
  color: #42b983;
  border-bottom: 3px solid #42b983;
  padding-bottom: 5px;
}
</style>

<template>
  <div id="app">
    <h1 id="title">Stock Price Predictor</h1>
    <router-view />
  </div>
</template>

<style>
#title {
  font-style: italic;
  font-weight: bolder;
  padding: 25px;
  background-color: #2f2fa2;
  color: white;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>

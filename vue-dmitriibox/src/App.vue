<template>
  <Nav />
  <nav>
    <router-link to="/">Home</router-link> | <!-- это ссылка местного фремворка межлу странцами -->
    <router-link to="/about">About</router-link> |
    <!--    https://v3.router.vuejs.org/ru/guide/essentials/named-routes.html-->
    <router-link :to="{ name: 'MainRoom'}">MainRoom</router-link> |
    <router-link :to="{ name: 'GameRoom'}">GameRooms</router-link> |
    <router-link :to="{ name: 'Login'}">Login</router-link> |
  </nav>
  <router-view/>
</template>

<style>
@import "assets/css/base.css";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
<script>
import Nav from "@/components/Nav";
export default {
  components: {Nav}
}
</script>
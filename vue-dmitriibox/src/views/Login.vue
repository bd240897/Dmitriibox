<template>
  <h1>Login</h1>

  <div>
    <p>auth_token = {{auth_token}}</p>
    <p>username = {{username}}</p>
    <p>auth = {{ auth }}</p>
    <p>temp = {{ temp }}</p>
  </div>

  <div>
    <input v-model="login" type="text" placeholder="Логин"/>
    <input v-model="password" type="password" placeholder="Пароль"/>
    <button v-if="!auth" @click="setLogin">Войти</button>
    <button v-if="auth" @click="logout">Выйти</button>
  </div>

  <div>
    <button v-on:click="getUsername">GetUsername</button>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      login: 'amid',
      password: '1',
      auth_token: '',
      username: '',
    }
  },
  // TODO разница между mounted and crated???
  created() {

  },
  watch:{
    auth: function() {
      // https://v3.ru.vuejs.org/ru/api/options-lifecycle-hooks.html#mounted
      // TODO delete
      console.log('changed');
    }
  },

  computed:{
    auth() {
      // https://ru.vuejs.org/v2/cookbook/client-side-storage.html
      if (this.auth_token==='') {
        console.log("auth empty")
        return false
      }
      else {
        console.log("auth full")
        return !!sessionStorage.getItem('auth_token')
      }
    },
  },
  methods: {
    setAjaxSetup(){
      $.ajaxSetup({
        headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
      });
    },
    removeAjaxSetup(){
      $.ajaxSetup({});
    },
    setLogin() {
      $.ajax({
        url: "http://127.0.0.1:8000/auth/token/login/",
        type: "POST",
        data: {
          username: this.login,
          password: this.password
        },
        success: (response) => {
          console.log(response)
          alert("Спасибо что Вы с нами")
          sessionStorage.setItem("auth_token", response.auth_token)
          this.auth_token = response.auth_token
          this.setAjaxSetup()
          this.getUsername()
          console.log("(setLogin) Новый auth_token записан в sessionStorage")
          // this.$router.push({name: "home"})
        },
        error: (response) => {
          if (response.status === 400) {
            alert("(setLogin) Логин или пароль не верен")
          }
        }
      })
    },
    logout(){
      $.ajax({
        url: "http://127.0.0.1:8000/api/v1/auth/users/me/",
        type: "GET",
        // headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
        success: (response) => {
          sessionStorage.removeItem("auth_token")
          this.auth_token = ''
          this.username = ''
          this.removeAjaxSetup()
          console.log("(logout) Текущий auth_token удален из sessionStorage")
        },
        error: (response) => {
          alert("(logout) Ошибка выхода", response)
        }
      })
    },
    getUsername(){
      console.log("(getUsername) получили auth_token из localStorage", sessionStorage.getItem('auth_token'))
      $.ajax({
        url: "http://127.0.0.1:8000/api/v1/auth/users/me/",
        type: "GET",
        headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
        success: (response) => {
          console.log(response)
          this.username = response.username
          console.log("(getUsername) Имя " + response.username + " записано в перменную username")
        },
        error: (response) => {
          alert("(getUsername) Ошибка получения username", response)
        }
      })
    },
  }
}


</script>

<style scoped>

</style>
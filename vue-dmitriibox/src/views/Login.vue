<template>
<!--  <h1>Login</h1>-->

<!--  <div>-->
<!--    <p>auth_token = {{auth_token}}</p>-->
<!--    <p>username = {{username}}</p>-->
<!--    <p>auth = {{ auth }}</p>-->
<!--  </div>-->

<!--  <div>-->
<!--    <input v-model="login" type="text" placeholder="Логин"/>-->
<!--    <input v-model="password" type="password" placeholder="Пароль"/>-->
<!--    <button v-if="!auth" @click="setLogin">Войти</button>-->
<!--    <button v-if="auth" @click="logout">Выйти</button>-->
<!--  </div>-->

<!--  <div>-->
<!--    <button v-on:click="getUsername">GetUsername</button>-->
<!--  </div>-->

  <section class="login-page vh-100">
    <div class="header container h-100">

      <!--ЗАГОЛОВОК-->
      <div class="header">
        <h1 class="header__text p-2 d-flex justify-content-center text-white rounded-pill">Страница входа</h1>
      </div>

      <!--ВХОД-->
      <div class="entry row d-flex justify-content-center align-items-center h-100">
        <div class="col-sm-10 col-lg-6">

          <div v-if="auth" class="entry__form">
            <form method="post">

              <div class="entry__form__input form-group mb-3">
                <input v-model="username" type="text" class="form-control" id="1" placeholder="Password">
              </div>
              <div class="entry__form__input form-group mb-3">
                <input v-model="password" type="password" class="form-control" id="2" placeholder="Password">
              </div>
              <button v-on:click.prevent="login" class="entry__form__btn w-100 btn btn-primary" type="submit">Войти</button>
            </form>

            <div class="entry__register text-center">
              <a href="#" class="" role="button">Зарегистрироваться</a>
            </div>
          </div>

          <div v-else class="entry__exit">
            <button v-on:click.prevent="logout" type="submit" class="entry__form__btn w-100 btn btn-primary">Выйти</button>
          </div>

        </div>
      </div>
    </div>
  </section>

</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: 'amid',
      password: '1',
      auth_token: '',
    }
  },
  created() {
    //pass
  },
  watch:{
    //pass
  },
  computed:{
    auth() {
      return !this.auth_token
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
    login() {
      $.ajax({
        url: this.$store.state.host + "/auth/token/login/",
        type: "POST",
        data: {
          username: this.username,
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
          this.$router.push({ name: 'MainRoom'})
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
        url: this.$store.state.host + "/api/v1/auth/users/me/",
        type: "GET",
        // headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
        success: (response) => {
          sessionStorage.removeItem("auth_token")
          this.auth_token = ''
          this.username = ''
          this.$store.state.username = ''

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
        url: this.$store.state.host + "/api/v1/auth/users/me/",
        type: "GET",
        headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
        success: (response) => {
          console.log(response)
          this.$store.state.username = response.username
          this.username = response.username
          console.log("(getUsername) Имя " + this.$store.username + " записано в store")
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
/* ЗАГОЛОВОК  */
.header__text{
  font-weight: bold;
  font-size: 26px;
  background-color: orange;
}
/* ВХОД */
/* pass */
</style>
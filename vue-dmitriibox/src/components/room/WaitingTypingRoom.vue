<template>
  <h1>WaitingTypingRoom</h1>

    <div>
    <p>username = {{username}}</p>
  </div>
</template>

<script>
export default {
  name: "WaitingTypingRoom",
  data() {
    return {
      username: '',
    }
  },
  created() {
    this.getUsername()
  },
  methods: {
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
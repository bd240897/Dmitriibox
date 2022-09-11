<template>
  <h1>WaitingRoom</h1>
</template>

<script>
// import store from '@/store/index.js';

export default {
  name: "WaitingRoom",
  data(){
    return {
      list_players: '',
      data: this.$store.state.name
    }
  },
  created(){
    // выводим имя при создании компонента
    console.log(this.$options.name)


    this.loadPlayers()
    setInterval(() => {
      this.loadPlayers()
    }, 5000)
  },
  methods:{
    loadPlayers() {
      $.ajax({
        url: this.$store.state.waitingRoomPlayersUrlAPI, //"http://127.0.0.1:8000/api/v1/room/waiting/SQPQ/gatusers/",
        type: "GET",
        success: (response) => {
          console.log(response)
          this.list_players = response.users
        }
      })
    },
  }

}


</script>

<style scoped>

</style>
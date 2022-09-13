<template>
  <h1>WaitingRoom</h1>


  <div>
    List of player
    <button>Refresh</button>
  </div>

  <div>
    massage: {{massage}}
  </div>
  <div>
    <button v-on:click="joinToGame">Join to game</button>
    <button>Exit to game</button>
    <button>Delete room</button>
  </div>
</template>

<script>
// import store from '@/store/index.js';

export default {
  name: "WaitingRoom",
  data(){
    return {
      list_players: '',
      data: this.$store.state.name,
      roomCode: 'SQPQ',
      massage: '',
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
    joinToGame(){
            $.ajax({
        url: 'http://127.0.0.1:8000/game/join/',
        data: {room_code: this.roomCode,},
        type: "GET",
        success: (response) => {
          this.massage = response.massage
        }
      })
    },
    exitToGame(){

    },

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
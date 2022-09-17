<template>
  <div>
    <h1>Navigation</h1>

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

    <div>
      <div>Store nameCurrentRoom: {{this.$store.state.nameCurrentRoom}}</div>
      <button v-on:click="toPreviousRoom">Previous room</button>
      <button v-on:click="toNextRoom">Next room</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Navigation",
  data(){
    return {
      massage: '',
    }
  },
  created(){
    //pass
  },
  computed:{
    roomCode(){
      return this.$store.state.roomCode
    },
    username() {
      return this.$store.state.username
    },
  },
  methods:{
    // ПЕРЕКЛЮЧЕНИЕ КОМНАТ
    toPreviousRoom() {
      console.log('1')
      this.$store.state.toPreviousRoom()
    },
    toNextRoom() {
      console.log('2')
      this.$store.state.toNextRoom()
    },
    getGameStatus(){
      // ***Получает текущий статус игры***
    },
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
      //pass
    },
  }

}
</script>

<style scoped>

</style>
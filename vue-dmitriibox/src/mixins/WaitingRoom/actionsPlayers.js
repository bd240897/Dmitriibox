////// ДЕЙСТВИЯ В КОМНАТЕ WaitingRoom //////

export default {
  methods:{
    joinToGame(){
      // присоединиться к игре
      $.ajax({
        url: this.$store.state.host + '/vue/game/join/',
        data: {room_code: this.roomCode,},
        type: "GET",
        success: (response) => {
          console.log(response)
          this.success = response.success
          this.error = response.error
        },
        error: (response) => {
          console.log(response)
          alert("(joinToGame)")
        }
      })
    },
    exitToGame(){
      // выйти из игры
      $.ajax({
        url: this.$store.state.host + '/vue/game/exit/',
        data: {room_code: this.roomCode,},
        type: "GET",
        success: (response) => {
          console.log(response)
          this.success = response.success
          this.error = response.error
        },
        error: (response) => {
          console.log(response)
          alert("(exitToGame)")
        }
      })
    },
    deleteRoom(){
      // удалить комнату
      $.ajax({
        url: this.$store.state.host + '/vue/game/delete/',
        data: {room_code: this.roomCode,},
        type: "GET",
        success: (response) => {
          console.log(response)
          this.success = response.success
          this.error = response.error
          this.$router.push({ name: 'MainRoom'})
        },
        error: (response) => {
          console.log(response)
          alert("(deleteRoom)")
        }
      })
    },
    startGame(){
      // начинает игру
      // this.$store.state.nameCurrentRoom = 'typing_room';
      this.$store.state.toNextRoom();
    },
  }
}
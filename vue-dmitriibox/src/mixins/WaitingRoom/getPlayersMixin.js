////// отвечает за получение списка игроков //////

export default {
  data(){
    return {
      players: '',
    }
  },
  created() {
    // получить список игроков при входе
    this.getPlayers()
    // получить список игроков каждые 5 секунд
    // setInterval(() => {
    //   this.getPlayers()
    // }, 5000)
  },
  methods:{
    getPlayers() {
      // получить список игроков в комнате ожидания
      $.ajax({
        url: this.$store.state.host + "/vue/game/players/",
        data: {room_code: this.roomCode,},
        type: 'get',
        dataType: 'json',
        success: (response) => {
          console.log(response)
          this.players = response.players;
        },
      })
    },
  }
}

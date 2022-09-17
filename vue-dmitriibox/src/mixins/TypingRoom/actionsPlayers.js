////// ДЕЙСТВИЯ В КОМНАТЕ TypingRoom //////

export default {
  data() {
    return {
      questionObj: {
        question: '',
        right_answer: '',
        img: '',
      }
    }
  },
  methods: {
    getQuestion() {
      // получить вопрос для текущего раунда
      $.ajax({
        url: this.$store.state.host + '/vue/game/question/',
        data: {room_code: this.roomCode,},
        type: "GET",
        success: (response) => {
          console.log(response)
          this.success = response.success
          this.error = response.error
          this.questionObj.question = response.massage.question
          this.questionObj.right_answer = response.massage.right_answer
          this.questionObj.img = this.$store.state.host + response.massage.img
        },
        error: (response) => {
          console.log(response)
          alert("(getQuestion)")
        }
      })
    },
    sendAnswer() {
      // отправить вопрос на текущий раунд
      $.ajax({
        url: this.$store.state.host + "/vue/game/send/",
        type: "POST",
        dataType: 'json',
        data: {
          room_code: this.roomCode,
          answer: this.form.textarea,
        },
        success: (response) => {
          console.log(response)
        },
        error: (response) => {
          console.log(response)
          alert("(sendAnswer)")
        }
      })
    }
  }
}
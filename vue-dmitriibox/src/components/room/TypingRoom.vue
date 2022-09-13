<template>
  <h1>TypingRoom</h1>

  <div>{{this.$store.state.name}}</div>


  <div>
    <p>{{ form.textarea }}</p>
    <textarea v-model="form.textarea"
              :rows="4"
              placeholder="Введите текст сообщения"></textarea>
    <div><button class="btn-send" @click="sendAnswer">Отправить</button></div>
  </div>
</template>

<script>
export default {
  name: "TypingRoom",
  data() {
    return {
      form: {
        textarea: '',
      },
      username: '',
      roomCode: 'SQPQ',
      previous_room: 'waiting_room',
      current_room: 'typing_room',
      next_room: 'waiting_typing_room'
    }
  },
  created() {

  },
  methods: {
    sendAnswer(){
      $.ajax({
        url:  "http://127.0.0.1:8000/game/room/typing/",
        type: "POST",
        dataType: 'json',
        data: {
          room_code: this.roomCode,
          answer: this.form.textarea,
          username: this.username},
        success: (response) => {
          console.log(response)
        }
      })
    },
  },
}



</script>

<style scoped>

</style>
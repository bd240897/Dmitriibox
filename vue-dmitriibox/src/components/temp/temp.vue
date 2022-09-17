<template>

</template>

<script>
export default {
  name: "temp",
  data() {
    return {
      api_msg: '',
    }
  },
  created() {

  },
  watch: {
    // следить за измнениями стора
    '$store.state.username': function() {
      console.log(this.$store.state.username)
    },

    // как работает вотчер
    auth: function() {
      // https://v3.ru.vuejs.org/ru/api/options-lifecycle-hooks.html#mounted
      // TODO delete
      console.log('changed');
    },
  },

  methods: {

    // отправить POST запрос на API
    // https://learn.javascript.ru/fetch
    async loadMovie() {
      this.api_msg = await fetch(`http://127.0.0.1:8000/api/v1/room/waiting/SQPQ/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({"action": "START_GAME"})
      }).then(response => response.json());
    }
  }
}
</script>

<style scoped>

</style>



<!--  <div>-->
<!--    <button v-on:click="toPreviousRoom">Previous room</button>-->
<!--    <button v-on:click="toNextRoom">Next room</button>-->
<!--  </div>-->
<!--      toPreviousRoom() {-->
<!--      this.$store.state.nameCurrentRoom = this.previous_room-->
<!--    },-->
<!--    toNextRoom() {-->
<!--      this.$store.state.nameCurrentRoom = this.next_room-->
<!--    }-->



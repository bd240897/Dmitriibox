<template>
  <h1>TypingRoom</h1>
  {{ api_msg.massage }}
</template>

<script>
export default {
  name: "TypingRoom",
  data() {
    return {
      api_msg: '',
    }
  },
  created() {
    this.loadMovie()
  },
  methods: {

    // отправить POST запрос на API
    // https://learn.javascript.ru/fetch
    async loadMovie() {
      this.api_msg  = await fetch(`http://127.0.0.1:8000/api/v1/room/waiting/SQPQ/`, {
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
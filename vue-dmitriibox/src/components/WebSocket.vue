<template>

</template>

<script>
export default {
  name: "WebSocket",
    created() {
    this.createWebSocket()
  },
  methods: {
    createWebSocket(){
      // ***Создает Веб Сокет***

      var localContext = this;

      console.log("WebSocke created")

      // имя комнаты
      const roomName = "SQPQ";
      const hostDjango = "127.0.0.1:8000"; // window.location.host
      // веб сокет
      var connectionString = 'ws://' + hostDjango + '/ws/game/' + roomName + '/';
      const chatSocket = new WebSocket(connectionString);

      // получить сообщение
      chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("Cообщение получено", data)
        localContext.gameStatus = data.message;
      };

      // закрытие соекта
      chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        localContext.gameStatus = "deleted"
      };
    }
  }
}
</script>

<style scoped>

</style>
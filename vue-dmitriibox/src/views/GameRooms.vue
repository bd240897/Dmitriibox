<template>
  GameRooms
  {{ $route.params.roomCode }}
  <h6>WebSocket gameStatus = {{ gameStatus }}</h6>

  <!--Тут рендерятся комнаты-->
  <div class="rooms-block">
    <WaitingRoom v-if="gameStatus === 'waiting_room'"/>  <!-- -->
    <TypingRoom v-if="gameStatus === 'typing_room'"/>
    <WaitingTypingRoom v-if="true"/> <!-- gameStatus === 'waiting_typing_room' -->
    <ResultRoom v-if="gameStatus === 'result_room'"/>
    <ResultListRoom v-if="gameStatus === 'result_list_room'"/>
    <GameOverRoom v-if="gameStatus === 'gameover_room'"/>
  </div>

</template>

<script>
import WaitingRoom from "@/components/room/WaitingRoom";
import TypingRoom from "@/components/room/TypingRoom";
import ResultRoom from "@/components/room/ResultRoom";
import $ from 'jquery'
import appInstance from '../main'
import WaitingTypingRoom from "@/components/room/WaitingTypingRoom";
import ResultListRoom from "@/components/room/ResultListRoom";
import GameOverRoom from "@/components/room/GameOverRoom";

export default {
  name: "GameRooms",
  components: {GameOverRoom, ResultListRoom, WaitingTypingRoom, WaitingRoom, TypingRoom, ResultRoom},
  data(){
    return {
      roomCode: '',
      gameStatus: 'init'
    }
  },
  created() {
    this.getGameStatus()
    this.createWebSocket()
  },
  methods:{
    getGameStatus(){
      // ***Получает текущий статус игры***
    },
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

  },
}

$(document).ready(function(){})

</script>

<style scoped>

</style>
<template>
  GameRooms
  {{ $route.params.roomCode }}
  <h6>WebSocket gameStatus = {{ gameStatus }}</h6>

  <!--Тут рендерятся комнаты-->
  <div class="rooms-block">
    <WaitingRoom v-if="gameStatus === 'waiting_room'"/>  <!-- gameStatus === 'waiting_room' -->
    <TypingRoom v-if="gameStatus === 'typing_room'"/> <!-- gameStatus === 'typing_room' -->
    <WaitingTypingRoom v-if="gameStatus === 'waiting_typing_room'"/> <!-- gameStatus === 'waiting_typing_room' -->
    <ResultRoom v-if="gameStatus === 'result_room'"/> <!-- gameStatus === 'result_room' -->
    <ResultListRoom v-if="gameStatus === 'result_list_room'"/> <!-- gameStatus === 'result_list_room' -->
    <GameOverRoom v-if="gameStatus === 'gameover_room'"/> <!-- gameStatus === 'gameover_room' -->
  </div>

  <div>
    <div>{{this.$store.state.nameCurrentRoom}}</div>
    <button v-on:click="toPreviousRoom">Previous room</button>
    <button v-on:click="toNextRoom">Next room</button>
  </div>

  <!-- Тут подключается ws -->
<!--  <WebSocket v-if="false"/>-->
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
import WebSocket from "@/components/WebSocket";

export default {
  name: "GameRooms",
  components: {WebSocket, GameOverRoom, ResultListRoom, WaitingTypingRoom, WaitingRoom, TypingRoom, ResultRoom},
  data(){
    return {
      roomCode: '',
    }
  },
  computed: {
    gameStatus() {
      return this.$store.state.nameCurrentRoom
    },
  },
  created() {

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

  },

}


</script>

<style scoped>

</style>
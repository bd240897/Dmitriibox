<template>
  GameRooms
  <Navigation/>


  <!--Тут рендерятся комнаты-->
  <div class="rooms-block">
    <WaitingRoom v-if="gameStatus === 'waiting_room'"/>  <!-- gameStatus === 'waiting_room' -->
    <TypingRoom v-if="gameStatus === 'typing_room'"/> <!-- gameStatus === 'typing_room' -->
    <WaitingTypingRoom v-if="gameStatus === 'waiting_typing_room'"/> <!-- gameStatus === 'waiting_typing_room' -->
    <ResultRoom v-if="gameStatus === 'result_room'"/> <!-- gameStatus === 'result_room' -->
    <ResultListRoom v-if="gameStatus === 'result_list_room'"/> <!-- gameStatus === 'result_list_room' -->
    <GameOverRoom v-if="gameStatus === 'gameover_room'"/> <!-- gameStatus === 'gameover_room' -->
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
import Navigation from "@/components/Navigation";

export default {
  name: "GameRooms",
  components: {
    Navigation,
    WebSocket, GameOverRoom, ResultListRoom, WaitingTypingRoom, WaitingRoom, TypingRoom, ResultRoom},
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


  },

}


</script>

<style scoped>

</style>
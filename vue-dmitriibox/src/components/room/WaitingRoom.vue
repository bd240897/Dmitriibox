<template>
  <div>

    <section class="waiting-room "> vh-100
      <div class="container pt-1 pb-1 h-100">
        <div class="d-flex flex-column justify-content-center align-items-between h-100">

          <!-- КОД КОМНАТЫ -->
          <div class="room-code">
            <!-- TODO delete id -->
            <h1 id="pop-room-code" class="room-code__text pop-instruction--user pop-instruction--admin
                                          p-2 d-flex justify-content-center bg-success
                                          text-white rounded-pill">Комната {{roomCode}} </h1>
          </div>

          <!-- ВЫ ВОШЛИ КАК -->
          <div class="user p-2 bg-primary text-white rounded-pill text-center">
            <h1 class="user__username"> Вы вошли как {{username}} . </h1>
            <h1 class="user__text"> Ждем остальных игроков. </h1>
          </div>

          <!-- ОПОВЕЩЕНИЯ ДЖАНГИ -->
          <Massages v-bind:error="error" v-bind:success="success"/>

          <!-- СПИСОК ИГРОКОВ -->
          <div class="plyers-list border border-primary pt-3 pb-3 mb-3 bt-3 p-3">
            <h2 class="plyers-list__header text-center">Список игроков в лобби</h2>
            <div class="plyers-list__container pt-3 pb-3">
              <!-- условие тут
              <div class="plyers-list__container__empty">
                  Пока тут никого нет
              </div> -->

              <!-- условие тут -->
              <div id="waitingPlayersThere" class="plyers-list__container__full d-flex align-items-center justify-content-center">
                <div v-for="player in players" class="plyers-list__player d-inline p-2 mx-1 bg-success text-white"> {{ player.username }} </div>
              </div>
              <!-- TODO delete id ненужная кнопка-->
              <button id="pop-list-players" v-on:click="getPlayers" class="plyers-list__container__btn pop-instruction--user pop-instruction--admin btn"> Обновить список </button>
            </div>
          </div>

          <!-- КНОПКИ УПРАВЛЕНИЯ -->
          <div class="player-actions d-flex flex-column text-center border border-primary pt-1 pb-1">
            <h2 class="player-actions__header">Управление:</h2>
            <!-- TODO delete id ненужная кнопка-->
            <a href="#" class="player-actions_btn disabled btn btn-primary m-2" >Добавить бота</a>

            <!-- ВХОД ВЫХОД API -->
            <a id="waiting_room_API_join" v-on:click="joinToGame" class="player-actions_btn pop-instruction--user btn btn-primary m-2">Присоединиться к игре API</a>
            <a id="waiting_room_API_exit" v-on:click="exitToGame" class="player-actions_btn btn btn-primary m-2">Выйти из игры API</a>

            <!-- ДОП ФУНКЦИИ -->

            <a href="#" class="player-actions_btn btn btn-primary m-2">Удалить всех пользователей</a>
            <a v-on:click="deleteRoom" class="player-actions_btn btn btn-primary m-2">Удалить комнату</a>
            <!-- TODO delete id-->
            <a v-on:click="startGame" id="pop-start-game" href="#" class="player-actions_btn pop-instruction--admin btn btn-success m-2 " >Начать игру</a>

            <div class="waiting-owner">
              <div class="waiting-owner__header d-flex flex-column pt-2 pb-2">
                Ждем пока создатель комнаты owner начнет игру.
              </div>
              <!-- TODO delete id-->
              <div id="pop-wait-owner-start" class="waiting-owner__body pop-instruction--user d-flex flex-column pt-2 pb-2 fw-bold fs-5 text-white justify-content-center align-items-center">
                <p class="waiting-owner__body__text d-inline">Ждем пока создатель комнаты</p>
                <p class="waiting-owner__body__owner d-inline"> owner </p>
                <p class="waiting-owner__body__text d-inline"> начнет игру. </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>

import getPlayersMixin from "@/mixins/WaitingRoom/getPlayersMixin";
import actionsPlayers from "@/mixins/WaitingRoom/actionsPlayers";
import Massages from "@/components/blocks/Massages";

export default {
  name: "WaitingRoom",
  components: {Massages},
  mixins: [getPlayersMixin, actionsPlayers],
  data(){
    return {
      success: '',
      error: '',
      roomCode: 'SQPQ',
    }
  },
  created(){
    // pass
  },
  destroyed() {
    console.log('destroyed');
  },
  computed:{
    username() {
      return this.$store.state.username
    },
  },
  methods:{
    //pass
  }
}


</script>

<style scoped>

</style>
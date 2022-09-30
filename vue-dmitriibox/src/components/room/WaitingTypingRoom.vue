<template>
  <section class="waiting-typing vh-100">
    <div class="container pt-1 pb-1 h-100">
      <div class="d-flex flex-column justify-content-center align-items-between h-100">

        <!-- ЗАГОЛВОК -->

        <div class="header">
          <h1 class="header__text p-2 mx-2 d-flex justify-content-center bg-primary text-center text-white rounded-pill">Ждем игроков раунда №{{ round }} из {{ max_rounds }}</h1>
        </div>

        <!-- ОПОВЕЩЕНИЯ ДЖАНГИ -->

        <Massages v-bind:error="error" v-bind:success="success"/>

        <!-- УЖЕ ОТВЕТИВШИЕ ИГРОКИ -->

        <div class="players text-center">
          <h2 class="players__text">Игроки которые уже ответили</h2>

          <div class="players__container" id="waitingPlayersThere">
            <div class="row">
              <div v-for="player in players"  class="col-3 p-auto pb-2">
                <div class="bg-success text-center text-white fw-bold">
                  <div class="players__username pt-2">{{player.player}}</div>
                  <div class="players__text pb-2 pt-2">done</div>
                </div>
              </div>
            </div>
          </div>

          <button v-on="getPlayers" class="players__btn btn"> Обновить </button>
        </div>

        <!-- КНОПКИ УПРАВЛЕНИЯ -->

        <div class="player-actions">
          <h2 class="player-actions__header">Управление:</h2>

          <div class="player-actions_btn d-flex flex-column pt-2 pb-2">
            <a v-on:click="toShowAnswers" href="#" class="answer_link btn btn-primary alredy_done__link">Показать ответы</a>
          </div>

          <div class="waiting-owner">
            <!-- TODO delete id-->
            <div id="pop-wait-owner-start" class="waiting-owner__body pop-instruction--user d-flex flex-column pt-2 pb-2 fw-bold fs-5 text-white justify-content-center align-items-center">
              <p class="waiting-owner__body__text d-inline">Ждем пока создатель комнаты</p>
              <p class="waiting-owner__body__owner d-inline"> owner </p>
              <p class="waiting-owner__body__text d-inline"> продолжит игру. </p>
            </div>
          </div>

        </div>

      </div>
    </div>
  </section>

</template>

<script>
import Massages from "@/components/blocks/Massages";
import getPlayers from "@/mixins/WaitingTypingRoom/getPlayers";
export default {
  name: "WaitingTypingRoom",
  components: {Massages},
  mixins: [getPlayers],
  data() {
    return {
      success: '',
      error: '',
      roomCode: 'SQPQ',
    }
  },
  created() {
    //pass
  },
  methods: {
    toShowAnswers(){
      // TODO to know
      this.$store.state.toNextRoom();
    },
  },
}
</script>

<style scoped>
/* ЗАГОЛВОК */
.header__text{
  font-weight: bold;
  font-size: 26px;
}

/* ОПОВЕЩЕНИЯ ДЖАНГИ */
/* pass1 */

/* УЖЕ ОТВЕТИВШИЕ ИГРОКИ */
/* pass */

/* КНОПКИ УПРАВЛЕНИЯ */
.waiting-owner__body__owner{
  color: red;
}
.waiting-owner__body{
  background-color: orange;
}
</style>
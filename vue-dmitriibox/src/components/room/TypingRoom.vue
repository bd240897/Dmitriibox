<template>
  <!--  <h1>TypingRoom</h1>-->

  <!--  <div>{{this.$store.state.name}}</div>-->


  <!--  <div>-->
  <!--    <p>{{ form.textarea }}</p>-->
  <!--    <textarea v-model="form.textarea"-->
  <!--              :rows="4"-->
  <!--              placeholder="Введите текст сообщения"></textarea>-->
  <!--    <div><button class="btn-send" @click="sendAnswer">Отправить</button></div>-->
  <!--  </div>-->
  <section class="typing-room">
    <div class="container pt-1 pb-1 border border-success animation-container">

      <!-- ЗАГОЛОВОК -->

      <div class="header">
        <h1 class="header__text p-2 d-flex justify-content-center bg-primary text-white rounded-pill">Пишем ответы раунда № round из max_rounds</h1>
      </div>

      <!-- ОПОВЕЩЕНИЯ ДЖАНГИ -->
      <Massages v-bind:error="error" v-bind:success="success"/>

      <!-- ВОПРОС -->

      <div class="question pt-2 pb-2">
        <h2 class="question__text text-center">Вопрос:</h2>
        <h2 class="question_text text-center"> {{questionObj.question}} </h2>
        <div class="question__img d-flex flex-column justify-content-center align-items-center py-2" >
          <img :src="questionObj.img" class="img-fluid" alt="...">
        </div>
      </div>

      <!-- ФОРМА ОТВЕТА -->

      <form class="send-form" method="post">
        <div class="send-form__answer mb-3">
          <textarea v-model="answer" class="form-control" type="text" placeholder="Напишите Ваше сообщение" style="height: 200px"></textarea>
        </div>
        <div class="send-form__btn d-grid gap-2">
          <button v-on:click.prevent="sendAnswer" type="submit" class="btn btn-primary btn-lg" value="Submit">Отправить</button>
        </div>
      </form>

    </div>
  </section>
</template>

<script>
import Massages from "@/components/blocks/Massages";
import actionsPlayers from "@/mixins/TypingRoom/actionsPlayers";
export default {
  name: "TypingRoom",
  components: {Massages},
  mixins: [actionsPlayers],
  data() {
    return {
      success: '',
      error: '',
      username: '',
      roomCode: 'SQPQ',
    }
  },
  created() {
    this.getQuestion()
  },
  methods: {
    //pass
  },
}



</script>

<style scoped>
/* АНИМАЦИЯ */

.animation-container {
  opacity: 0;
  animation: ani 2.5s forwards;
}

@keyframes ani {
  0% {opacity: 0;}
  100% {opacity: 1;}
}

/* ЗАГОЛОВОК  */
.header__text{
  font-weight: bold;
  font-size: 26px;
}

/* ОПОВЕЩЕНИЯ ДЖАНГИ */
/* pass1 */

/* ВОПРОС  */
.question{
  background-color: #f5d060;
  border-radius: 20px;
}
/* TODO check */
.question__img img{
  width: 100%;
  height: auto;
  max-width: 600px;
}
/* ВОЙТИ В КОМНАТУ */
/* pass1 */
</style>
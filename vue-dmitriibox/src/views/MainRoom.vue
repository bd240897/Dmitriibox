<template>
  <div>
    <h1>main_room</h1>
    <section class="main-room vh-100">
      <div class="container pt-1 pb-1 h-100">
        2222
        <div class="d-flex flex-column justify-content-center align-items-between h-100">

          <!--          {# ЗАГОЛОВОК СТРАНИЦЫ #}-->

          <div class="main-room-header py-1">
            <h1 class="p-2 d-flex justify-content-center bg-primary text-white rounded-pill" style="font-weight: bold; font-size: 26px">Игра #1</h1>
          </div>


          <!--          {# ВЫ ВОШЛИ КАК #}-->

          <div class="main-room-user py-1">
            <h2 class="p-2 d-flex justify-content-center align-items-center" style="background-color: cornsilk; font-weight:bold; font-size: 20px; color: black; border-radius: 50px;">
              <!--            {% if user.is_authenticated %}-->
              <div>Вы вошли как:&nbsp;</div>
              <!--              <div style="color: red"> {{ user.username }}</div>-->
              <!--            {% else %}-->
              <div>Вы не вошли в систему&nbsp;</div>
              <!--            {% endif %}-->
            </h2>
          </div>

          <!--          {# ЛПИСАНИЕ ИГРЫ #}-->

          <div class="main-room-description py-1">
            <h1 class="p-2 d-flex justify-content-center align-items-center" style="background-color: cornsilk; font-weight:bold; font-size: 20px; color: black; height: 200px; border-radius: 50px;">Краткое поисание тут.Краткое поисание тут.Краткое поисание тут</h1>
          </div>

          <!--          {# ПРАВИЛА ИГРЫ #}-->

          <div class="main-room-rules py-1">
            <div class="d-grid gap-2">
              <button class="btn btn-primary h-100" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
                Правила игры
              </button>
            </div>

            <!--          <div class="collapse " id="collapseExample">-->
            <!--            {% include '../blocks/game_rules.html' %}-->
            <!--          </div>-->
          </div>

          <!--          {# ВОЙТИ В КОМНАТУ #}-->

          <div class="d-flex flex-column justify-content-center align-items-center py-2">
            <form class="row g-3" method="post">
              <div class="col-auto">
                <!--              {{ form.room_code }}-->
                <input type="text"
                       v-model="inputRoomCode"
                       class="form-control text-center"
                       placeholder="Номер комнаты"
                       id="room_code"
                       >
              </div>
              <div class="col-auto">
                <button id="btn-enter-game" type="submit" class="btn btn-primary mb-3">Войти в комнату</button>
              </div>
              <!--            {% csrf_token %}-->
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
  <button @click.stop.prevent="submit()"> 1111 </button>
</template>

<script>
export default {
  name: "MainRoom",
  data(){
    return {
      inputRoomCode : 'SQPQ'
    }
  },
  methods: {
    submit(){
      // console.log(this.inputRoomCode)
      this.$router.push({ name: 'TypingRoom', params: {room_code: this.inputRoomCode }})
    }
  }
}



</script>

<style scoped>

</style>
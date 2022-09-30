<template>
  <section class="main-room vh-100">
    <div class="container pt-1 pb-1 h-100">
      <div class="d-flex flex-column justify-content-center align-items-between h-100">

        <!-- ЗАГОЛОВОК СТРАНИЦЫ -->

        <div class="header py-1">
          <h1 class="header__text p-2 d-flex justify-content-center bg-primary text-white rounded-pill">Игра #1</h1>
        </div>

        <!-- ОПОВЕЩЕНИЯ ДЖАНГИ -->

        <div class="messages">
          <div class="massage__success alert alert-success" role="alert" v-if="success">
            {{success}}
          </div>
          <div class="massage__danger waiting-massage alert alert-danger" role="alert" v-if="error">
            {{error}}
          </div>
        </div>

        <!-- ВЫ ВОШЛИ КАК -->

        <div class="user py-1">
          <div class="use__container p-2 d-flex justify-content-center align-items-center">
            <!-- TODO if -->
            <div class="user__joined" v-if="username">
              <span class="user__joined__text">Вы вошли как:&nbsp;</span>
              <span class="user__joined__username"> {{username}} </span>
            </div>
            <div class="user__nojoined" v-else>
                <span class="user__nojoined__text">Вы не вошли в систему&nbsp;</span>
            </div>
          </div>
        </div>

        <!-- ОПИСАНИЕ ИГРЫ -->

        <div class="description py-1">
          <h1 class="description__text p-2 d-flex justify-content-center align-items-center">Краткое поисание тут.Краткое поисание тут.Краткое поисание тут</h1>
        </div>

        <!-- ПРАВИЛА ИГРЫ -->

        <div class="rules py-1">
          <div class="d-grid gap-2">
            <button id="btn-rules" class="btn btn-primary h-100" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
              Правила игры
            </button>
          </div>

          <div class="collapse " id="collapseExample">
            <div class="accordion accordion-flush" id="accordion-parent">
              <div class="accordion-item">
                <h2 class="accordion-header" id="flush-heading-1">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse-1" aria-expanded="false" aria-controls="flush-collapse-1">
                    rule.header
                  </button>
                </h2>
                <div id="flush-collapse-1" class="accordion-collapse collapse" aria-labelledby="flush-heading-1" data-bs-parent="#accordion-parent">
                  <div class="rules card mx-2 py-1">
                    <div class="d-flex justify-content-center">
                      <img src="#" class="card-img-top" alt="..." style="width: 100%; height: auto; max-width: 800px;">
                    </div>
                    <div class="rules-body card-body">
                      <h5 class="rules-title card-title">rule.description</h5>
                      <p class="rules-text card-text">rule.description</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ВОЙТИ В КОМНАТУ -->

        <div class="enter-game d-flex flex-column justify-content-center align-items-center py-2">
          <form class="enter-game__form row g-3" method="post">
            <div class="enter-game__input col-auto">
              <input type="text" class="form-control text-center" placeholder="Номер комнаты" v-model="roomCode">
            </div>
            <div class="enter-game__btn col-auto">
              <button id="btn-enter-game" class="btn btn-primary mb-3" v-on:click.prevent="goToGameRooms">Войти в комнату</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "MainRoom",
  data(){
    return {
      roomCode : 'SQPQ',
      success: '',
      error: '',
    }
  },
  computed:{
    username() {
      console.log('computed', this.$store.state.username)
      return this.$store.state.username
    },
  },
  methods: {
    goToGameRooms(){
      // console.log(this.inputRoomCode)
      this.clearMassages()
      this.createRoom()
      //
    },
    createRoom(){
      $.ajax({
        url:  this.$store.state.host + "/vue/game/create/",
        type: "POST",
        dataType: 'json',
        data: {
          room_code: this.roomCode},
        success: (response) => {
          console.log(response)
          this.success = response.success;
          this.error = response.error;

          // TODO to know
          // если комната уже существует то перейдем в игру
          if (response.next_room){
            this.$store.state.roomCode = this.roomCode;
            this.$router.push({ name: 'GameRoom'})
          }

          // если пришел успех переходим в комнату ожидания
          if (response.success){
            this.$store.state.roomCode = this.roomCode;
            this.$router.push({ name: 'GameRoom'})
          }
        }
      })
    },
    clearMassages(){
      this.success = '';
      this.error = '';
    },
  }
}



</script>

<style scoped>
/* ЗАГОЛОВОК СТРАНИЦЫ */
.header__text{
  font-weight: bold;
  font-size: 26px;
}

/* ОПОВЕЩЕНИЯ ДЖАНГИ */
/* pass */

/* ВЫ ВОШЛИ КАК */
.user__container{
  background-color: cornsilk;
  font-weight:bold;
  font-size: 20px;
  color: black;
  border-radius: 50px;
}
.user__joined__username{
  color: red;
}

/* ОПИСАНИЕ ИГРЫ */
.description__text{
  background-color: cornsilk;
  font-weight:bold;
  font-size: 20px;
  color: black;
  height: 200px;
  border-radius: 50px;
}

/* ПРАВИЛА ИГРЫ  */
/* pass */

/* ВОЙТИ В КОМНАТУ */
/* pass1 */
</style>
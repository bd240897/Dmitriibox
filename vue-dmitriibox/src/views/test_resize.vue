<template>
<!--  https://ru.stackoverflow.com/questions/991163/Отображение-блока-по-условию-v-if-и-v-else-в-зависимости-от-размеров-окна-vue-j-->
<!--  https://translated.turbopages.org/proxy_u/en-ru.ru.ee3608e8-63248c70-b1316c3e-74722d776562/https/stackoverflow.com/questions/63239954/vue-js-change-switch-class-depending-on-viewport-size-->
<!--  https://www.youtube.com/watch?v=ybwsXGDcGcI  -->

  <div id="test_resize">
    <div v-if="small">
      <h3>Small div</h3>
    </div>
    <div v-else>
      <h2>Large div</h2>
    </div>
    <!-- Монтировать комоненты можно так :is=перменная или is=имя-->
     <component :is="name"></component>
  </div>

</template>

<script>


import WaitingRoom from "@/components/room/WaitingRoom";
export default {
  name: "test_resize",
  components: {WaitingRoom},
  data: () => ({
    small: false,
    name: "WaitingRoom",
  }),
  created() {
    console.log('created');
    window.addEventListener('resize', this.onResize);
    this.onResize();
  },
  destroyed() {
    console.log('destroyed');
    window.removeEventListener('resize', this.onResize)
  },
  methods: {
    onResize() {
      this.small = window.innerWidth <= 600;
    }
  }

}

</script>

<style scoped>

</style>
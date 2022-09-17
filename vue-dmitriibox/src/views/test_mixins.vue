<template>
  11111
<!--Learn Vue.js (RU) - Mixins-->
<!--  https://www.youtube.com/watch?v=xzq0gyUuimY&list=PLu_62Q68DvTrWAR_3-iOfIdbqKU912i3z&index=14-->
<!--https://stackoverflow.com/questions/54506161/vue-js-how-to-separate-methods-data-computed-etc-in-separate-js-files-->
<!--  Learn Vue.js (RU) - Компоненты #4 - Слоты -->
<!--https://www.youtube.com/watch?v=rve1Tbq-BxE&list=PLu_62Q68DvTrWAR_3-iOfIdbqKU912i3z&index=9-->
<!--Learn Vue.js (RU) - Компоненты #5 - Динамические компоненты-->
<!--  https://www.youtube.com/watch?v=UZabVD3AJnk&list=PLu_62Q68DvTrWAR_3-iOfIdbqKU912i3z&index=10-->
<Profile/>
</template>


<script>
import {defineComponent,createApp} from 'vue'

const Profile = defineComponent({
  name: "Profile",
  template: '<p>{{ firstName }} {{ lastName }} — {{ alias }}</p>',
  data() {
    return {
      firstName: 'Walter',
      lastName: 'White',
      alias: 'Heisenberg'
    }
  }
})

export default {
  name: "test_mixins",
  components: {Profile}
}

// import Nav from "@/components/Nav";
// import app from '../main.js'
// app.component('max', Nav)



</script>

<style scoped>

</style>
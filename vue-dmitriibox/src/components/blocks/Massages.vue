<template>
  <div class="messages">
    <div class="massage__success alert alert-success" role="alert" v-if="success">
      {{success}}
    </div>
    <div class="massage__danger waiting-massage alert alert-danger" role="alert" v-if="error">
      {{error}}
    </div>
  </div>
</template>

<script>
export default {
  name: "Massages",
  props: {
    success: {
      default: () => '',
    },
    error: {
      default: () => '',
    },
  }
}
</script>

<style scoped>

</style>
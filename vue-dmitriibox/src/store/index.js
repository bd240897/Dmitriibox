import { createStore } from "vuex"

// https://stackoverflow.com/questions/67056563/vuex-cannot-read-property-state-of-undefined
const store = createStore({
   state:{
      name: "Vue",
      waitingRoomPlayersUrlAPI: "http://127.0.0.1:8000/api/v1/room/waiting/SQPQ/gatusers/",
      roomStartURL: '/vue/room',
   }
})

export default store
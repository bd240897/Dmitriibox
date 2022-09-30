import { createStore } from "vuex"

// https://stackoverflow.com/questions/67056563/vuex-cannot-read-property-state-of-undefined
const store = createStore({
    state:{
        name: "Vue",
        username: '',
        roomCode: '',
        host: 'http://127.0.0.1:8000', //'http://45.67.58.152:8000',//

        numberCurrentRoom: 1,
        listRooms: ['waiting_room', 'typing_room', 'waiting_typing_room', 'result_room', 'result_list_room', 'gameover_room'],
        nameCurrentRoom: 'waiting_room',
        toNextRoom(){
            if (this.numberCurrentRoom < this.listRooms.length){
                this.numberCurrentRoom += 1;
                this.nameCurrentRoom = this.listRooms[this.numberCurrentRoom-1];
            }
            else {
                console.log('Rooms end')
            }
        },
        toPreviousRoom(){
            if (this.numberCurrentRoom > 1){
                this.numberCurrentRoom -= 1;
                this.nameCurrentRoom = this.listRooms[this.numberCurrentRoom-1];
            }
            else {
                console.log('It is first room')
            }
        }

    },
    actions:{


    }
})

export default store
//////////////////////////////////////////////
var listRooms = ['waiting_room', 'typing_room', 'waiting_typing_room', 'result_room', 'result_list_room'];
var numberCurrentRoom = 1;
var nameCurrentRoom = listRooms[numberCurrentRoom-1];

function toNextRoom(){
    if (numberCurrentRoom < listRooms.length){
        numberCurrentRoom += 1;
        nameCurrentRoom = listRooms[numberCurrentRoom-1];
    }
    else {
        console.log('Rooms end')
    }
}

function toPreviousRoom(){
    if (numberCurrentRoom > 1){
        numberCurrentRoom -= 1;
        nameCurrentRoom = listRooms[numberCurrentRoom-1];
    }
    else {
        console.log('It is first room')
    }
}

        // waitingRoomPlayersUrlAPI: "http://127.0.0.1:8000/api/v1/room/waiting/SQPQ/gatusers/",
        // roomStartURL: '/vue/room',
//////////////////////////////////////////////
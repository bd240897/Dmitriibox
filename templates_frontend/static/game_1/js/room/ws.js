
$(function(){

    // имя комнаты
    const roomName = "SQPQ";
    // веб сокет
    var connectionString = 'ws://' + window.location.host + '/ws/game/' + roomName + '/';
    const chatSocket = new WebSocket(connectionString);

    // получить сообщение
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data)
        relocation(data.message)
    };

    // закрытие соекта
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    // отравить сообщение при клике
    $("#test").click(()=>{
        // message = "ПРИВЕТ Я ДИМА"
        let message = {
            "action": "MOVE",
            "message": "ПРИВЕТ Я ДИМА"
        }
        chatSocket.send(JSON.stringify({
            'message': message
        }));
    })
})
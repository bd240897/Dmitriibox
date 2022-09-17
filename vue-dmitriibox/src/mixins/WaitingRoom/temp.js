//Request with GET/HEAD method cannot have body.
fetch('http://127.0.0.1:8000/vue/game/players/', {
    method: 'GET', // Здесь так же могут быть GET, PUT, DELETE
    body: JSON.stringify({room_code: this.roomCode,}), // Тело запроса в JSON-формате
    headers: {'Content-type': 'application/json; charset=UTF-8'},
}).then((response) => response.json())
    .then((data) => {console.log(data)})
////////////// ВСПЫЛВАЮЩИЕ ПОДСКАЗКИ В КОМНАТЕ ОЖИДАНИЯ //////////////

jQuery(document).ready(function($) {

    // включить подсказки - сохраняем в сессию
    var insructuon_1 = true;
    if (sessionStorage.getItem('insructuon_1')) {
        // если есть в хранилище
        insructuon_1 = sessionStorage.getItem('insructuon_1');
        insructuon_1 = $.parseJSON(insructuon_1.toLowerCase());
    }

    // вывод в консоль
    // sessionStorage.setItem('insructuon_1', true)
    // https://learn.javascript.ru/localstorage
    if (insructuon_1){
        console.log("Подсказки будут показаны, insructuon_1 = ", insructuon_1)
    }
    else{
        console.log("Подсказки НЕ показаны, insructuon_1 = ", insructuon_1)
    }

    // конструктор подсказок
    function createPopover(popSelector='.example', side='bottom', number='1', text='1'){
        var title = '<div class="text-center">' + "Подсказка " + number  + '</div>'
        var content = '<div class="text-center fs-4">' + `${text}` + '</div>'
        $(popSelector).popover({
            placement: 'bottom',
            trigger: 'manual',
            html: true,
            title: `${title}`,
            content: `${content}`
        });
    }

    // создаем отдельные подсказки
    createPopover('#pop-room-code', 'bottom', '1', "Поделитесь кодом комнаты с друзьями.")
    // $('#room-code').popover('show');

    createPopover('#pop-list-players', 'bottom', '2', "Дождитесь когда всё игроки присоединятся к ваше комнате.")
    // $('#btn-list-players').popover('show');

    createPopover('#pop-start-game', 'bottom', '3', "Когда все будут готовы начните игру.")
    // $('#btn-start-game').popover('show');

    // перебираем все подсказки включая-выключая их (общий класс подсказок pop_instr_1)
    var listExample = $('.pop_instr_1')
    var time = 500;
    var TIMESTAMP = 2500

    console.log(insructuon_1)
    if (insructuon_1){
        console.log(insructuon_1)
        listExample.each(function (index, num){
            var oneExamle = $(this);
            setTimeout( function(){ oneExamle.popover('show')}, time)
            time += TIMESTAMP;
            setTimeout( function(){ oneExamle.popover('hide')}, time)
            // time += TIMESTAMP;
        })
        sessionStorage.setItem('insructuon_1', false)
    }

})

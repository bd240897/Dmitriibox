////////////// ВСПЫЛВАЮЩИЕ ПОДСКАЗКИ В КОМНАТЕ ОЖИДАНИЯ //////////////

jQuery(document).ready(function($) {

    // включить подсказки - сохраняем в сессию
    var insructuon_2 = true;
    if (sessionStorage.getItem('insructuon_2')) {
        // если есть в хранилище
        insructuon_2 = sessionStorage.getItem('insructuon_2');
        insructuon_2 = $.parseJSON(insructuon_2.toLowerCase());
    }

    // вывод в консоль
    //sessionStorage.setItem('insructuon_2', true)
    if (insructuon_2){
        console.log("Подсказки будут показаны, insructuon_1 = ", insructuon_2)
    }
    else{
        console.log("Подсказки НЕ показаны, insructuon_1 = ", insructuon_2)
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
    createPopover('#pop-room-code', 'bottom', '1', "Вы вошли в комнату с кодом")
    // $('#room-code').popover('show');

    createPopover('#pop-join', 'top', '2', "Нажмите чтобы присоединиться к игре.")
    // $('#btn-join').popover('show');

    createPopover('#pop-list-players', 'bottom', '3', "Посмотрите кто еще играет с вами..")
    // $('#btn-list-players').popover('show');

    createPopover('#pop-wait-owner-start', 'bottom', '4', "Дождитесь когда владелец комнаты начнет игру.")
    // $('#wait-owner-start').popover('show');

    // перебираем все подсказки включая-выключая их (общий класс подсказок pop_instr_1)
    var listExample = $('.pop_instr_2')
    var time = 500;
    var TIMESTAMP = 2500

    if (insructuon_2){
        listExample.each(function (index, num){
            var oneExamle = $(this);
            setTimeout( function(){ oneExamle.popover('show')}, time)
            time += TIMESTAMP;
            setTimeout( function(){ oneExamle.popover('hide')}, time)
            // time += TIMESTAMP;
        })
        sessionStorage.setItem('insructuon_2', false)
    }
})

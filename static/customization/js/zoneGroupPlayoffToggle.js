$(document).ready(function() {

// Первоначальное отключение полей для выбора группы/зоны в окне создания

       $('.modify-form .chooseZone').prop('disabled', true);
      $('.modify-form .chooseGroup').prop('disabled', true);
    $('.modify-form .choosePlayoff').prop('disabled', true);
    $('.selectpicker').selectpicker('refresh');

// Динамическое включение/выключение полей для выбора группы/зоны/плэй-офф при выборе отфильтовывающих их радиокнопок

    $('.zoneGroupPlayoffToggle > label').click(function() {

        var activeLabel      = $(this).hasClass('active');
        var activeLabelIndex = $(this).index(activeLabel) - 1;
            console.log("это кнопка номер " + activeLabelIndex);

        if(activeLabelIndex == 1) {
                console.log("условие номер 1");
               $('.chooseZone').prop('disabled', false);
                console.log("Z vis");
              $('.chooseGroup').prop('disabled', true);
                console.log("G dis");
            $('.choosePlayoff').prop('disabled', true);
                console.log("P dis");
        }
        if(activeLabelIndex == 2) {
            console.log("условие номер 2");
               $('.chooseZone').prop('disabled', true);
                console.log("Z dis");
              $('.chooseGroup').prop('disabled', false);
                console.log("G vis");
            $('.choosePlayoff').prop('disabled', true);
                console.log("P dis");
        }
        if(activeLabelIndex == 4) {
            console.log("условие номер 3");
               $('.chooseZone').prop('disabled', true);
                console.log("Z dis");
              $('.chooseGroup').prop('disabled', true);
                console.log("G dis");
            $('.choosePlayoff').prop('disabled', false);
                console.log("P vis");
        };

        $('.selectpicker').selectpicker('refresh');

    });

});
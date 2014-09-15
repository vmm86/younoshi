$(document).ready(function() {

//  Отображение данных

/// Фильтр списка команд в игровой стадии по сезону

    $('#filterSeasonforSAST').change(function() {
        var seasonid = $(this).val();
        var ageid    = 0;
        var sasid    = 0;
        console.log('season ', seasonid, 'age', $('#filterAgeforSAST').val(), 'sas', sasid);
        path         = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/team';
        window.location.href = path;
    });

/// Фильтр списка команд в игровой стадии по возрасту

    $('input[name="filterAgeforSAST"]').change(function() {
        var seasonid = $('#filterSeasonforSAST').val();
        var ageid    = $(this).val();
        var sasid    = 0;
        console.log('age ', ageid, 'season ', seasonid, 'sas', sasid);
        path         = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/team';
        window.location.href = path;
    });

/// Фильтр списка команд в игровой стадии по самой игровой стадии

    // $('#zoneGroupPlayoffToggle label').click(function() {

    //     var activeLabel      = $(this).hasClass('active');
    //     var activeLabelIndex = $(this).index(activeLabel) - 1;
    //     console.log("это кнопка номер " + activeLabelIndex);

    //     if(activeLabelIndex == 1) {
    //         console.log("условие номер 1");
    //            $('#chooseZone').prop('disabled', false);
    //           $('#chooseGroup').prop('disabled', true);
    //         $('#choosePlayoff').prop('disabled', true);
    //     }
    //     if(activeLabelIndex == 2) {
    //         console.log("условие номер 2");
    //            $('#chooseZone').prop('disabled', true);
    //           $('#chooseGroup').prop('disabled', false);
    //         $('#choosePlayoff').prop('disabled', true);
    //     }
    //     if(activeLabelIndex == 4) {
    //         console.log("условие номер 3");
    //            $('#chooseZone').prop('disabled', true);
    //           $('#chooseGroup').prop('disabled', true);
    //         $('#choosePlayoff').prop('disabled', false);
    //     };

    //     $('.selectpicker').selectpicker('refresh');

    // });

    $('#chooseZone, #chooseGroup, #zoneGroupPlayoffToggle_P').change(function() {
        var seasonid = $('#filterSeasonforSAST').val();
        var ageid    = $('input[name="filterAgeforSAST"]').val();
        var sasid    = $(this).val();
        console.log('season ', seasonid, 'age', ageid, 'sas', sasid);
        path         = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/team';
        window.location.href = path;
    });

//  Добаление/изменение данных

/// Фильтр школ (для команд) по городам

    $('#filterCity').change(function() {
        var cityid         = $(this).val();
        var school_of_city = '#filterSchool option[data-city-id="' + cityid + '"]';
        $('#filterSchool option:not(:first-child)').removeAttr('selected').hide();
            console.log('s-hide');
        $(school_of_city).show();
            console.log('s-show');
        $('.selectpicker').selectpicker('refresh');
            console.log('s-refresh');
        // $('ul.dropdown-menu').removeAttr('min-height');
        //     console.log('s-remove');
    });

/// Фильтр команд по школам

    $('#filterSchool').change(function() {
        var schoolid       = $(this).val();
        var team_of_school = '#filterTeam option[data-school-id="' + schoolid + '"]';
        $('#filterTeam option:not(:first-child)').removeAttr('selected').hide();
            console.log('t-hide');
        $(team_of_school).show();
            console.log('t-show');
        $('.selectpicker').selectpicker('refresh');
            console.log('t-refresh');
        // $('ul.dropdown-menu').removeAttr('min-height');
        //     console.log('t-remove');
    });

    $('#filterTeam').change(function() {
        teamid = $(this).val();
        console.log('team ID is ', teamid);
    });

});
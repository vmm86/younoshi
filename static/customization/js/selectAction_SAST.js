$(document).ready(function() {

//  Отображение данных

    function routeSAST(seasonid, ageid, sasid) {
        console.log('season ', seasonid, 'age', ageid, 'sas', sasid);
        path = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/team';
        window.location.href = path;
    }

/// Фильтр списка команд в игровой стадии по сезону

    $('#filterSeasonforSAST').change(function() {
        var seasonid = $(this).val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = 0;

        var sasid = 0;

        routeSAST(seasonid, ageid, sasid);
    });

/// Фильтр списка команд в игровой стадии по возрасту

    $('input[name="filterAgeforSAST"]').change(function() {
        var seasonid = $('#filterSeasonforSAST').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $(this).val();
        if (typeof ageid === "undefined")
            ageid = 0;

        var sasid = 0;

        routeSAST(seasonid, ageid, sasid);
    });

/// Фильтр списка команд в игровой стадии по самой игровой стадии

    $('#chooseZone, #chooseGroup, #zoneGroupPlayoffToggle_P').change(function() {
        var seasonid = $('#filterSeasonforSAST').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $('input[name="filterAgeforSAST"]').val();
        if (typeof ageid === "undefined")
            ageid = 0;

        var sasid = $(this).val();
        if (typeof sasid === "undefined")
            sasid = 0;

        routeSAST(seasonid, ageid, sasid);
    });

//  Добавление/изменение данных

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
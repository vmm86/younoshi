$(document).ready(function() {

//  Отображение данных

    function routeSAST(seasonid, ageid, sasid) {
        console.log('season ', seasonid, 'age', ageid, 'sas', sasid);
        path = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/team';
        return window.location.href = path;
    }

/// Фильтр списка команд в игровой стадии по сезону

    $('[name="filterSeason"]').change(function() {
        var seasonid = $(this).val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = 0;

        var sasid = 0;

        routeSAST(seasonid, ageid, sasid);
    });

/// Фильтр списка команд в игровой стадии по возрасту

    $('[name="filterAge"]').change(function() {
        var seasonid = $('[name="filterSeason"]').val();
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
        var seasonid = $('[name="filterSeason"]').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $('[name="filterAge"]').val();
        if (typeof ageid === "undefined")
            ageid = 0;

        var sasid = $(this).val();
        if (typeof sasid === "undefined")
            sasid = 0;

        routeSAST(seasonid, ageid, sasid);
    });

//  Добавление/изменение данных

/// Фильтр школ (для команд) по городам

    $('[name="filterCity"]').change(function() {
        var cityid         = $(this).val();
        var school_of_city = '[name="filterSchool"] option[data-city-id="' + cityid + '"]';
        $('[name="filterSchool"] option:not(:first-child)').removeAttr('selected').hide();
            console.log('s-hide');
        $(school_of_city).show();
            console.log('s-show');
        $('.selectpicker').selectpicker('refresh');
            console.log('s-refresh');
        // $('ul.dropdown-menu').removeAttr('min-height');
        //     console.log('s-remove');
    });

/// Фильтр команд по школам

    $('[name="filterSchool"]').change(function() {
        var schoolid       = $(this).val();
        var team_of_school = '[name="filterTeam"] option[data-school-id="' + schoolid + '"]';
        $('[name="filterTeam"] option:not(:first-child)').removeAttr('selected').hide();
            console.log('t-hide');
        $(team_of_school).show();
            console.log('t-show');
        $('.selectpicker').selectpicker('refresh');
            console.log('t-refresh');
        // $('ul.dropdown-menu').removeAttr('min-height');
        //     console.log('t-remove');
    });

    $('[name="filterTeam"]').change(function() {
        teamid = $(this).val();
        console.log('team ID is ', teamid);
    });

});
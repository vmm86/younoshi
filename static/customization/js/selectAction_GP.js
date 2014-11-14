$(document).ready(function() {

//  Отображение данных

    function routeGP(seasonid, ageid, sasid) {
        console.log('season ', seasonid, 'age', ageid, 'sas', sasid);
        path = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/gp';
        return window.location.href = path;
    }

///  Фильтр списка команд в игровой стадии по сезону

    $('[name="filterSeason"]').change(function() {
        var seasonid = $(this).val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = 0;

        var sasid = 0;

        routeGP(seasonid, ageid, sasid);
    });

///  Фильтр списка команд в игровой стадии по возрасту

    $('[name="filterAge"]').change(function() {
        var seasonid = $('[name="filterSeason"]').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $(this).val();
        if (typeof ageid === "undefined")
            ageid = 0;

        var sasid = 0;

        routeGP(seasonid, ageid, sasid);
    });

///  Фильтр списка команд в игровой стадии по самой игровой стадии

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

        routeGP(seasonid, ageid, sasid);
    });

});
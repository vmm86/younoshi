$(document).ready(function() {

    function routeGP(seasonid, ageid, sasid) {
        console.log('season ', seasonid, 'age', ageid, 'sas', sasid);
        path = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/gp';
        return window.location.href = path;
    }

//  Фильтр списка команд в игровой стадии по сезону

    $('#filterSeasonforGP').change(function() {
        var seasonid = $(this).val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = 0;

        var sasid = 0;

        routeGP(seasonid, ageid, sasid);
    });

//  Фильтр списка команд в игровой стадии по возрасту

    $('input[name="filterAgeforGP"]').change(function() {
        var seasonid = $('#filterSeasonforGP').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $(this).val();
        if (typeof ageid === "undefined")
            ageid = 0;

        var sasid = 0;

        routeGP(seasonid, ageid, sasid);
    });

//  Фильтр списка команд в игровой стадии по самой игровой стадии

    $('#chooseZone, #chooseGroup, #zoneGroupPlayoffToggle_P').change(function() {
        var seasonid = $('#filterSeasonforGP').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $('input[name="filterAgeforGP"]').val();
        if (typeof ageid === "undefined")
            ageid = 0;

        var sasid = $(this).val();
        if (typeof sasid === "undefined")
            sasid = 0;

        routeGP(seasonid, ageid, sasid);
    });

});
$(document).ready(function() {

//  Отображение данных

    function routeSAS(seasonid, ageid) {
        console.log('season ', seasonid, 'age', ageid);
        path = '/season/' + seasonid + '/age/' + ageid + '/stage';
        return window.location.href = path;
    }

///  Фильтр игровых стадий по сезону

    $('[name="filterSeason"]').change(function() {
        var seasonid = $(this).val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = 0;

        routeSAS(seasonid, ageid);
    });

///  Фильтр игровых стадий по возрасту

    $('[name="filterAge"]').change(function() {
        var seasonid = $('[name="filterSeason"]').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $(this).val();
        if (typeof ageid === "undefined")
            ageid = 0;

        routeSAS(seasonid, ageid);
    });

});
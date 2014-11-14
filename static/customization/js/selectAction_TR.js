$(document).ready(function() {

//  Отображение данных

    function routeTR(seasonid_from, seasonid_to, ageid) {
        console.log('season_from', seasonid_from, 'season_to', seasonid_to, 'age', ageid);
        path = '/teamrating/season/' + seasonid_from + '-' + seasonid_to + '/age/' + ageid;
        return window.location.href = path;
    }

///  Фильтр рейтинга команд по начальному сезону

    $('[name="filterSeason_from"]').change(function() {
        var seasonid_from = $(this).val();
        if (typeof seasonid_from === "undefined")
            seasonid_from = 0;

        var seasonid_to = $('[name="filterSeason_to"]').val();
        if (typeof seasonid_to === "undefined")
            seasonid_to = 0;

        var ageid = 0;

        routeTR(seasonid_from, seasonid_to, ageid)
    });

///  Фильтр рейтинга команд по конечному сезону

    $('[name="filterSeason_to"]').change(function() {
        var seasonid_from = $('[name="filterSeason_from"]').val();
        if (typeof seasonid_from === "undefined")
            seasonid_from = 0;

        var seasonid_to = $(this).val();
        if (typeof seasonid_to === "undefined")
            seasonid_to = 0;

        var ageid = 0;

        routeTR(seasonid_from, seasonid_to, ageid)
    });

///  Фильтр рейтинга команд по возрасту

    $('[name="filterAge"]').change(function() {
        var seasonid_from = $('[name="filterSeason_from"]').val();
        if (typeof seasonid_from === "undefined")
            seasonid_from = 0;

        var seasonid_to = $('[name="filterSeason_to"]').val();
        if (typeof seasonid_to === "undefined")
            seasonid_to = 0;

        var ageid = $(this).val();
        if (typeof ageid === "undefined")
            ageid = 0;

        routeTR(seasonid_from, seasonid_to, ageid)
    });

});
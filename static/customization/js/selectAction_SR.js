$(document).ready(function() {

    function routeSR(seasonid_from, seasonid_to) {
        console.log('season_from', seasonid_from, 'season_to', seasonid_to);
        path = '/schoolrating/season/' + seasonid_from + '-' + seasonid_to;
        return window.location.href = path;
    }

//  Фильтр рейтинга команд по начальному сезону

    $('#filterSeasonforSR_from').change(function() {
        var seasonid_from = $(this).val();
        if (typeof seasonid_from === "undefined")
            seasonid_from = 0;

        var seasonid_to = 0;

        routeSR(seasonid_from, seasonid_to);
    });

//  Фильтр рейтинга команд по конечному сезону

    $('#filterSeasonforSR_to').change(function() {
        var seasonid_from = $('#filterSeasonforSR_from').val();
        if (typeof seasonid_from === "undefined")
            seasonid_from = 0;

        var seasonid_to = $(this).val();
        if (typeof seasonid_to === "undefined")
            seasonid_to = 0;

        routeSR(seasonid_from, seasonid_to);
    });

});
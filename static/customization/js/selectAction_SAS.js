$( document ).ready(function() {

    function routeSAS(seasonid, ageid) {
        console.log('season ', seasonid, 'age', $('#filterAgeforSAS').val());
        path = '/season/' + seasonid + '/age/' + ageid + '/stage';
        return window.location.href = path;
    }

//  Фильтр игровых стадий по сезону

    $('#filterSeasonforSAS').change(function() {
        var seasonid = $(this).val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = 0;

        routeSAS(seasonid, ageid);
    });

//  Фильтр игровых стадий по возрасту

    $('input[name="filterAgeforSAS"]').change(function() {
        var seasonid = $('#filterSeasonforSAS').val();
        if (typeof seasonid === "undefined")
            seasonid = 0;

        var ageid = $(this).val();
        if (typeof ageid === "undefined")
            ageid = 0;

        routeSAS(seasonid, ageid);
    });

});
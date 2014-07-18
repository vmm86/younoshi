$( document ).ready(function() {

//  Фильтр игровых стадий по сезону

    $('#filterSeasonforSAS').change(function() {
        var seasonid = $(this).val();
        var ageid = 0;
        console.log('season ', seasonid, 'age', $('#filterAgeforSAS').val());
        path = '/season/' + seasonid + '/age/' + ageid + '/stage';
        window.location.href = path;
    });

//  Фильтр игровых стадий по возрасту

    $('input[name="filterAgeforSAS"]').change(function() {
        var seasonid   = $('#filterSeasonforSAS').val();
        var ageid = $(this).val();
        console.log('age ', ageid, 'season ', seasonid);
        path = '/season/' + seasonid + '/age/' + ageid + '/stage';
        window.location.href = path;
    });

});
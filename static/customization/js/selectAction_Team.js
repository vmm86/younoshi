$( document ).ready(function() {

//  Фильтр школ по городам

    $('#filterCityforTeam').change(function() {
        var cityid   = $(this).val();
        var schoolid = 0;
        console.log('city ', cityid, 'school', $('#filterSchoolforTeam').val());
        path = '/city/' + cityid + '/school/' + schoolid + '/team';
        window.location.href = path;
    });

//  Фильтр команд по школам

    $('#filterSchoolforTeam').change(function() {
        var cityid   = $('#filterCityforTeam').val();
        var schoolid = $(this).val();
        console.log('school ', schoolid);
        path = '/city/' + cityid + '/school/' + schoolid + '/team';
        window.location.href = path;
    });

});
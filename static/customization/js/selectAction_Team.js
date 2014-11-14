$(document).ready(function() {

//  Отображение данных

    function routeTeam(cityid, schoolid) {
        console.log('city ', cityid, 'school', schoolid);
        path = '/city/' + cityid + '/school/' + schoolid + '/team';
        return window.location.href = path;
    }

///  Фильтр школ по городам

    $('[name="filterCity"]').change(function() {
        var cityid = $(this).val();
        if (typeof cityid === "undefined")
            cityid = 0;

        var schoolid = 0;

        routeTeam(cityid, schoolid);
    });

///  Фильтр команд по школам

    $('[name="filterSchool"]').change(function() {
        var cityid = $('[name="filterCity"]').val();
        if (typeof cityid === "undefined")
            cityid = 0;

        var schoolid = $(this).val();
        if (typeof schoolid === "undefined")
            schoolid = 0;

        routeTeam(cityid, schoolid);
    });

});
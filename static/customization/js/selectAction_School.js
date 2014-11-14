$(document).ready(function() {

//  Отображение данных

    function routeSchool(cityid) {
        console.log('city ', cityid);
        path = '/city/' + cityid + '/school';
        return window.location.href = path;
    }

///  Фильтр школ по городам

    $('[name="filterCity"]').change(function() {
        var cityid = $(this).val();
        if (typeof cityid === "undefined")
            cityid = 0;

        routeSchool(cityid);
    });

});
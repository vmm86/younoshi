$( document ).ready(function() {

//  Фильтр школ по городам

    $('#filterCityforSchool').change(function() {
        var cityid = $(this).val();
        console.log('city ', cityid);
        path = '/city/' + cityid + '/school';
        window.location.href = path;
    });

});
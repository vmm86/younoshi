$(document).ready(function() {

//  Отображение данных

/// Фильтр списка команд в игровой стадии по сезону

    $('#filterSeasonforGP').change(function() {
        var seasonid = $(this).val();
        var ageid    = 0;
        var sasid    = 0;
        console.log('season ', seasonid, 'age', $('#filterAgeforGP').val(), 'sas', sasid);
        path         = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/gp';
        window.location.href = path;
    });

/// Фильтр списка команд в игровой стадии по возрасту

    $('input[name="filterAgeforGP"]').change(function() {
        var seasonid = $('#filterSeasonforGP').val();
        var ageid    = $(this).val();
        var sasid    = 0;
        console.log('age ', ageid, 'season ', seasonid, 'sas', sasid);
        path         = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/gp';
        window.location.href = path;
    });

/// Фильтр списка команд в игровой стадии по самой игровой стадии

    $('#chooseZone, #chooseGroup, #zoneGroupPlayoffToggle_P').change(function() {
        var seasonid = $('#filterSeasonforGP').val();
        var ageid    = $('input[name="filterAgeforGP"]').val();
        var sasid    = $(this).val();
        console.log('season ', seasonid, 'age', ageid, 'sas', sasid);
        path         = '/season/' + seasonid + '/age/' + ageid + '/stage/' + sasid + '/gp';
        window.location.href = path;
    });

// //  Добавление/изменение данных

// /// Фильтр школ (для команд) по городам

//     $('#filterCity').change(function() {
//         var cityid         = $(this).val();
//         var school_of_city = '#filterSchool option[data-city-id="' + cityid + '"]';
//         $('#filterSchool option:not(:first-child)').removeAttr('selected').hide();
//             console.log('s-hide');
//         $(school_of_city).show();
//             console.log('s-show');
//         $('.selectpicker').selectpicker('refresh');
//             console.log('s-refresh');
//         // $('ul.dropdown-menu').removeAttr('min-height');
//         //     console.log('s-remove');
//     });

// /// Фильтр команд по школам

//     $('#filterSchool').change(function() {
//         var schoolid       = $(this).val();
//         var team_of_school = '#filterTeam option[data-school-id="' + schoolid + '"]';
//         $('#filterTeam option:not(:first-child)').removeAttr('selected').hide();
//             console.log('t-hide');
//         $(team_of_school).show();
//             console.log('t-show');
//         $('.selectpicker').selectpicker('refresh');
//             console.log('t-refresh');
//         // $('ul.dropdown-menu').removeAttr('min-height');
//         //     console.log('t-remove');
//     });

//     $('#filterTeam').change(function() {
//         teamid = $(this).val();
//         console.log('team ID is ', teamid);
//     });

});
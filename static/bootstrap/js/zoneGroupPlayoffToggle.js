$('#zoneGroupPlayoffToggle > label').click(function() {

    var activeLabel = $(this).hasClass('active');
    var activeLabelIndex = $(this).index(activeLabel) - 1;
    console.log("это кнопка номер " + activeLabelIndex);

    if (activeLabelIndex == 1) {
        console.log("условие номер 1");
        $('#chooseZone').prop('disabled', false);
        $('#chooseGroup').prop('disabled', true);
    }
    if(activeLabelIndex == 2) {
        console.log("условие номер 2");
        $('#chooseZone').prop('disabled', true);
        $('#chooseGroup').prop('disabled', false);
    }
    if(activeLabelIndex == 4) {
        console.log("условие номер 3");
        $('#chooseZone').prop('disabled', true);
        $('#chooseGroup').prop('disabled', true);
    };

    $('.selectpicker').selectpicker('refresh');

});
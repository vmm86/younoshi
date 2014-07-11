$(document).ready(function() {
    $('#create').bootstrapValidator(
        {
            message: 'This value is not valid',
        fields: {
            teamName: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {message: 'Не забудьте указать название команды'}
                }
            },
            ageid: {
                validators: {
                    notEmpty: {message: 'Не забудьте указать возраст игроков команды'}
                }
            }
        }
    });
});
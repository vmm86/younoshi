$(document).ready(function() {
    $('.create-form, .update-form').bootstrapValidator(
        {
            message: 'This value is not valid',
        fields: {
            cityName: {
                message: 'cityName is not valid',
                validators: {
                    notEmpty: {message: 'Не забудьте указать город'}
                }
            },
            schoolName: {
                message: 'schoolName is not valid',
                validators: {
                    notEmpty: {message: 'Не забудьте указать название спортивной школы'}
                }
            },
            teamName: {
                message: 'teamName is not valid',
                validators: {
                    notEmpty: {message: 'Не забудьте указать название команды'}
                }
            },
            ageid: {
                validators: {
                    notEmpty: {message: 'Не забудьте указать возраст игроков команды'}
                }
            },
            seasonName: {
                validators: {
                    notEmpty: {message: 'Не забудьте указать сезон'}
                }
            },
            stagetype: {
                validators: {
                    notEmpty: {message: 'Не забудьте указать тип игровой стадии'}
                }
            },
            stageName: {
                validators: {
                    notEmpty: {message: 'Не забудьте указать название игровой стадии'}
                }
            }
        }
    });
});
$(document).ready(function() {
    $('.create-form, .update-form').bootstrapValidator({
        excluded: [':disabled'],
        message: 'This value is not valid',
        fields: {
            'cityName': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать город'
                    }
                }
            },
            'schoolName': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать название спортивной школы'
                    }
                }
            },
            'teamName': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать название команды'
                    }
                }
            },
            'age_ID': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать возраст игроков команды'
                    }
                }
            },
            'seasonName': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать сезон'
                    }
                }
            },
            'stageType': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать тип игровой стадии'
                    }
                }
            },
            'stageName': {
                validators: {
                    notEmpty: {
                        message: 'Не забудьте указать название игровой стадии'
                    }
                }
            },
            'zoneGroupPlayoffToggle': {
                validators: {
                    choice: {
                        min: 1, 
                        max: 1, 
                        message: 'Не забудьте выбрать тип игровой стадии'
                    }
                }
            },
            'gameType': {
                validators: {
                    choice: {
                        min: 1, 
                        max: 1, 
                        message: 'Не забудьте выбрать тип соревнований'
                    }
                }
            }
        }
    });
});
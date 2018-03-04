$(document).ready(function() {
    // Generate a simple captcha
    function randomNumber(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };
    $('#captchaOperation').html([randomNumber(1, 20), '+', randomNumber(1, 30), '='].join(' '));
	
	
	//EXAMPLE REGISTER FORM
    $('#registerForm').bootstrapValidator({
        message: 'این مقدار نامعتبر است',
        fields: {
            username: {
                message: 'نام کاربری نا معتبر است',
                validators: {
                    notEmpty: {
                        message: 'نام کاربری ضروری است  ، نمیتوانید خالی بگذارید'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'نام کاربری باید بیشتر از 6 کاراکتر و کمتر از 30 کاراکتر باشد'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: 'نام کاربری باید شامل حروف ، عدد ، نقطه و خط باشد'
                    },
                    different: {
                        field: 'password',
                        message: 'نام کاربری و پسورد نباید شبیه هم باشد'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'آدرس ایمیل ضروری است لطفا تکمیل نمایید'
                    },
                    emailAddress: {
                        message: 'آدرس ایمیل معتبر نمی باشد'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: 'کلمه عبور ضروری است لطفا تکمیل نمایید'
                    },
                    identical: {
                        field: 'confirmPassword',
                        message: 'رمز عبور و تأیید آن مشابه نیست'
                    },
                    different: {
                        field: 'username',
                        message: 'رمز عبور نمی تواند همان نام کاربری باشد'
                    }
                }
            },
            confirmPassword: {
                validators: {
                    notEmpty: {
                        message: 'رمز عبور تأیید لازم است و نمی تواند خالی باشد'
                    },
                    identical: {
                        field: 'password',
                        message: 'رمز عبور و تایید آن یکسان نیست'
                    },
                    different: {
                        field: 'username',
                        message: 'رمز عبور نمی تواند همان نام کاربری باشد'
                    }
                }
            },
            phoneNumber: {
                validators: {
                    digits: {
                        message: 'ارزش تنها می تواند شامل رقم باشد'
                    }
                }
            },
            acceptTerms: {
                validators: {
                    notEmpty: {
                        message: 'شما باید شرایط و ضوابط را قبول کنید'
                    }
                }
            },
            captcha: {
                validators: {
                    callback: {
                        message: 'Wrong answer',
                        callback: function(value, validator) {
                            var items = $('#captchaOperation').html().split(' '), sum = parseInt(items[0]) + parseInt(items[2]);
                            return value == sum;
                        }
                    }
                }
            }
        }
    });
	
	
	//EXAMPLE CONTACT FORM
    $('#contactForm').bootstrapValidator({
        message: 'مقدار وارد شده نامعتبر است',
        fields: {
            name: {
                message: 'نام معتبر نیست',
                validators: {
                    notEmpty: {
                        message: 'نام مورد نیاز است و نمی تواند خالی باشد'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: 'نام تنها میتواند از حروف الفبا، شماره، نقطه و زیرخط باشد'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'آدرس ایمیل مورد نیاز است و نمی تواند خالی باشد'
                    },
                    emailAddress: {
                        message: 'ورودی یک آدرس ایمیل معتبر نیست'
                    }
                }
            },
            website: {
                validators: {
                    uri: {
                        message: 'ورودی نشانی اینترنتی معتبر نیست'
                    }
                }
            },
            Contactmessage: {
                validators: {
                    notEmpty: {
                        message: 'پیام مورد نیاز است و نمی تواند خالی باشد'
                    },
                    stringLength: {
                        min: 6,
                        message: 'پیام باید بیش از 6 کاراکتر داشته باشد'
                    }
                }
            },
            captcha: {
                validators: {
                    callback: {
                        message: 'پاسخ اشتباه',
                        callback: function(value, validator) {
                            var items = $('#captchaOperation').html().split(' '), sum = parseInt(items[0]) + parseInt(items[2]);
                            return value == sum;
                        }
                    }
                }
            }
        }
    });
	
	
	//Regular expression based validators
    $('#ExpressionValidator').bootstrapValidator({
        message: 'این مقدار معتبر نیست',
        fields: {
             email: {
                validators: {
                    notEmpty: {
                        message: 'آدرس ایمیل مورد نیاز است و نمی تواند خالی باشد'
                    },
                    emailAddress: {
                        message: 'ورودی یک آدرس ایمیل معتبر نیست'
                    }
                }
            },
            website: {
                validators: {
                    uri: {
                        message: 'ورودی نشانی اینترنتی معتبر نیست'
                    }
                }
            },
            phoneNumber: {
                validators: {
                    digits: {
                        message: 'ارزش تنها می تواند شامل رقم باشد'
                    }
                }
            },
            color: {
                validators: {
                    hexColor: {
                        message: 'ورودی یک رنگ شصت معتبر نیست'
                    }
                }
            },
            zipCode: {
                validators: {
                    usZipCode: {
                        message: 'کدپستی معتبر نمی باشد'
                    }
                }
            }
        }
    });
	
	
	//Regular expression based validators
    $('#NotEmptyValidator').bootstrapValidator({
        message: 'این مقدار معتبر نیست',
        fields: {
            username: {
                message: 'نام کاربری معتبر نیست',
                validators: {
                    notEmpty: {
                        message: 'نام کاربری مورد نیاز است و نمی تواند خالی باشد'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'نام کاربری باید بیش از 6 و کمتر از 30 کاراکتر دارد'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: 'نام کاربری تنها می تواند شامل حروف الفبا، شماره، نقطه و زیر خط کش باشد'
                    }
                }
            },
            country: {
                validators: {
                    notEmpty: {
                        message: 'کشور مورد نیاز است و نمی تواند خالی باشد'
                    }
                }
            }
        }
    });
	
	
	//Regular expression based validators
    $('#IdenticalValidator').bootstrapValidator({
        message: 'این مقدار معتبر نیست',
        fields: {
            password: {
                validators: {
                    notEmpty: {
                        message: 'رمز عبور مورد نیاز است و نمی تواند خالی باشد'
                    },
                    identical: {
                        field: 'confirmPassword',
                        message: 'رمز عبور و تایید آن یکسان نیست'
                    }
                }
            },
            confirmPassword: {
                validators: {
                    notEmpty: {
                        message: 'رمز عبور تأیید لازم است و نمی تواند خالی باشد'
                    },
                    identical: {
                        field: 'password',
                        message: 'رمز عبور و تایید آن یکسان نیست'
                    }
                }
            }
        }
    });
	
	//Regular expression based validators
    $('#OtherValidator').bootstrapValidator({
        message: 'این مقدار معتبر نیست',
        fields: {
            ages: {
                validators: {
                    lessThan: {
                        value: 100,
                        inclusive: true,
                        message: 'سن باید کمتر از 100 باشد'
                    },
                    greaterThan: {
                        value: 10,
                        inclusive: false,
                        message: 'سن باید بیشتر یا برابر با 10 باشد'
                    }
                }
            }
        }
    });
	
});
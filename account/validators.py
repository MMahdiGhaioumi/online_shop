from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

password_validators = [
    MinLengthValidator(
        8,
        message='رمز باید حداقل ۸ کاراکتر داشته باشد!!',
    ),

    MaxLengthValidator(
        255,
        message='رمز باید حداکثر ۲۵۵ کاراکتر باشد!!',
    ),

    RegexValidator(
        r'^\S+$',
        'نباید فضای خالی در رمز وجود داشته باشد!!',
        'no_whitespace',
    ),

    RegexValidator(
        r'^[\x21-\x7E]+$',
        'رمز باید فقط شامل کاراکترهای ASCII باشد!!',
        'ascii_only',
    ),

    RegexValidator(
        r'[A-Z]',
        'باید حداقل یک حرف بزرگ داشته باشد!!',
        'exists_capital_character',
    ),

    RegexValidator(
        r'[a-z]',
        'باید حداقل یک حرف کوچک داشته باشد!!',
        'exists_small_character',
    ),

    RegexValidator(
        r'\d',
        'باید حداقل یک عدد داشته باشد!!',
        'exists_digit',
    ),
]

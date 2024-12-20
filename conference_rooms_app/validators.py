from django.core.exceptions import ValidationError


def validate_phone(phone_number):

    if len(phone_number) != 9:

        raise ValidationError('Numer telefonu musi zawierać 9 cyfr')
    
    for number in phone_number:

        if not number.isdigit():

            raise ValidationError('Numer telefonu musi zawierać tylko cyfry')
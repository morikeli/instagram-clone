from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator
from phonenumber_field.phonenumber import PhoneNumber
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.http import HttpResponse


def check_username_exists(request):
    """ This function validates if the typed username exists. """

    _username = request.POST.get('username')
    username_exists = get_user_model().objects.filter(username=_username).exists()

    if _username != '' and username_exists:
        return HttpResponse('<div class="error">This username exists!</div>')
    elif _username == '' or str(_username).isspace():
        return HttpResponse('<div class="error">Invalid username!</div>')
    else:
        return HttpResponse(f'<div class="success">"{_username}" is available.</div>')


def email_address_validation(request):
    """ This function validates if the typed email address exists or is valid. """

    _email = request.POST.get('email')

    email_exists = get_user_model().objects.filter(email=_email).exists()
    
    if email_exists:
        return HttpResponse('<div class="error">Email address provided exists!</div>')
    
    try:
        validate_email(_email)      # validate email address
    
    except ValidationError as error:
        return HttpResponse('<div class="error">Invalid email address!</div>')

    return HttpResponse('')


def validate_phone_number(phone_number):
    """ This is a function used to parse a mobile number and check if it is a valid. """
    try:
        # parse the number
        parsed_number = PhoneNumber.from_string(phone_number)
        
        # Check if the phone number is valid
        if not parsed_number.is_valid():
            raise ValidationError('Invalid phone number!')
    
    except Exception as e:
        # If parsing fails, raise a validation error
        raise ValidationError("Invalid mobile number!")

    return None     # if validation is successful, return None


def mobile_number_validation(request):
    """ Validate the mobile number provided by the user. """
    _mobile_no = request.POST.get('phone_no', '')

    try:
        validate_phone_number(_mobile_no)   # validate the mobile number
    
    except ValidationError as error:
        return HttpResponse(f'<div class="error">{"".join(error)}</div>')

    return HttpResponse('<div class="success">Phone number is valid.</div>')


def validate_password_with_django_validators(password):
    """ This function validates passwords using in-built django password validators. """
    
    validators = [
        MinimumLengthValidator(),
        CommonPasswordValidator(),
        NumericPasswordValidator(),
        UserAttributeSimilarityValidator(),
    ]

    errors = []
    for validator in validators:
        try:
            # Validate the password using each validator
            validator.validate(password)
        except ValidationError as e:
            # If validation fails, collect the error message
            errors.extend(e.messages)

    return errors


def password_match_and_length_validation(request):
    """ This function checks performs password validation on the passwords input by the user. """

    _password1 = request.POST.get('password1', None)
    _password2 = request.POST.get('password2', None)

    
    errors = validate_password_with_django_validators(_password1)
    if errors:
        # Construct error message HTML
        error_message = "<br>".join(errors)
        return HttpResponse(f'<div class="error">{error_message}</div>')
    
    if _password1 and _password2:
        if _password1 != _password2:
            return HttpResponse('<div class="error">Passwords didn\'t match</div>')

    return HttpResponse('<div class="success">You\'re good to go!</div>')

from django.core.exceptions import ValidationError
import magic


def is_image_file(file):
    """ 
        This function is used to validate if the uploaded profile picture file is an image file.
        Accepted image file extensions/type are: .jpg, .jpeg & .png
    """
    accept = ['image/jpg', 'image/jpeg', 'image/png']
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)

    if file_mime_type not in accept:
        raise ValidationError('Unsupported file type for profile picture!')

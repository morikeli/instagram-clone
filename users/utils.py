from django.core.exceptions import ValidationError
import magic


def is_valid_media_file(file):
    """ 
        This function is used to validate if the uploaded file is a valid media file.
        Accepted file type are:
        - Audio: .mpeg, .ogg, .opus & .wav
        - Images: .jpg, .jpeg & .png
        - Video: .3gpp, .mp4, .mpeg &.ogg
    """
    accept = [
        'audio/mpeg',
        'audio/ogg',
        'audio/opus',
        'audio/wav',
        'image/jpg',
        'image/jpeg',
        'image/png',
        'video/mp4',
        'video/mpeg',
        'video/ogg',
        'video/3gpp; audio/3gpp',   # if it doesn't contain video.
    ]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)

    if file_mime_type not in accept:
        raise ValidationError('Unsupported file format!')

from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    extention = os.path.splitext(value.name)[1]
    print(extention)
    valid_extentions = ['.png', '.jpg', '.jpeg']
    if not extention.lower() in valid_extentions:
        raise ValidationError('Unsupported file extenstion. Allowed file type: '+ str(valid_extentions))
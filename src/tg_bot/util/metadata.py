import piexif

def get_original_image_path(image):
    return __get_value_from_metadata(image, "0th", piexif.ImageIFD.ImageDescription)

def set_original_image_path(image, path):
    return __set_value_to_metadata(image, "0th", piexif.ImageIFD.ImageDescription, path)

def get_photo_uid(image):
    return __get_value_from_metadata(image, "0th", piexif.ImageIFD.DocumentName)

def set_photo_uid(image, uid):
    return __set_value_to_metadata(image, "0th", piexif.ImageIFD.DocumentName, uid)

def get_person_name(image):
    return __get_value_from_metadata(image, "Exif", piexif.ExifIFD.UserComment)

def set_person_name(image, name):
    return __set_value_to_metadata(image, "Exif", piexif.ExifIFD.UserComment, name)


def __get_value_from_metadata(image, ifd, key):
    exif = image.info.get("exif")

    if not exif:
        return None
    
    exif = piexif.load(exif)
    value = exif[ifd].get(key)

    if not value:
        return None

    return value.decode("utf-8")

def __set_value_to_metadata(image, ifd, key, value):
    exif = image.info.get("exif")

    if not exif:
        exif = piexif.dump(())
    
    exif = piexif.load(exif)
    exif[ifd][key] = value.encode("utf-8")

    return exif

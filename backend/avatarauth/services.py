import qrcode

from . import models


def create_avatar():
    u = models.User()
    u.is_active = False
    u.save()
    return u


def generate_qr_code(user: models.User):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=2
    )

    qr.add_data(user.uuid)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    return img

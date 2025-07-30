import os
import qrcode
import asyncio

custom_dir = "/tmp/qrcodes"
os.makedirs(custom_dir, exist_ok=True)

async def get_qr(target_string: str) -> str:
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(target_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    safe_name = "".join(c for c in target_string if c.isalnum() or c in ('-', '_'))
    image_name = f"{safe_name}.png"

    path_name = os.path.join(custom_dir, image_name)
    img.save(path_name)

    return path_name

    print("QR code saved as qrcode.png")

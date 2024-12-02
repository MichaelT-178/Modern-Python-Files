import qrcode
from termcolor import colored as c
import os

# The folder the output image will be downloaded to
output_path = f"../qr_codes"

def generate_qr_code(link, output_image_name):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(link)
        qr.make(fit=True)

        # You can change the colors if you want 
        img = qr.make_image(fill="black", back_color="white")

        img.save(f"{output_path}/{output_image_name}")

        print(c(f"\nQR Code generated and saved as \"{output_image_name}!\"", 'green'))

    except Exception as e:
        print(c(f"Error generating QR Code: {e}", 'red'))


website_link = input(c("Paste the link you want to generate a QR code for : ", 'cyan'))
output_image_name = input(c("What do you want to name the output image? (no ext.) : ", 'cyan'))
output_image_name = f'{output_image_name}.jpg'

confirmation = input(c(f"\nCreate QR Code for \"{website_link}\" and save in the \"{output_path}/\" folder as \"{output_image_name}\"? (y/n): ", 'yellow'))


if confirmation.upper().strip() in ['YES', 'Y']:
    generate_qr_code(website_link, output_image_name)
    os.system(f"open -a Finder {output_path}")
else:
    print(c("Process cancelled", 'red'))

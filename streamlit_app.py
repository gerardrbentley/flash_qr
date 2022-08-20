import io
import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer
from PIL import Image

st.header("Flash QR")
st.write("Generate Unique QR Codes from Flash Drawings")

website_url = st.text_input("QR Code Destination URL", "https://gerardbentley.com")
dot_mapping = {
    'square': SquareModuleDrawer,
    'round': RoundedModuleDrawer
}
dot_style = st.radio('QR Dot Style', dot_mapping)

# Decide how the User will provide an image
use_upload = "Upload an Image"
use_camera = "Use Camera to take a Photo"
no_image = "No Image"
image_method = st.radio("Embeded QR Image", [no_image, use_upload, use_camera])

if image_method == use_upload:
    image_file = st.file_uploader(
        "Upload Image File for center of QR 🌄", ["png", "jpg", "jpeg"], accept_multiple_files=False
    )
elif image_method == use_camera:
    image_file = st.camera_input("Take a Photo for center of QR 📸")
elif image_method == no_image:
    image_file = None

embeded_image = None
if image_method in (use_camera, use_upload):
    # uploaded_img = st.file_uploader('Upload Flash for Center of QR', ['jpg', 'jpeg', 'png'])
    if image_file is not None:
        try:
            with st.expander('Show uploaded image'):
                st.image(image_file)
            st.success('Will use this image for center of the QR')
            embeded_image = Image.open(image_file)
        except Exception as e:
            print(e)
            st.error('Could not use uploaded image for center of QR 😢\nTry another image or no image.')
            st.stop()
    else:
        st.warning("Choose / take a photo to continue")
        st.stop()

qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(website_url)
qr.make(fit=True)

img = qr.make_image(
    fill_color="black",
    back_color="white",
    image_factory=StyledPilImage,
    module_drawer=dot_mapping[dot_style](),
    embeded_image=embeded_image
)

with io.BytesIO() as output:
    img.save(output, format="png")
    contents = output.getvalue()
    btn = st.download_button(
        label="Download QR Code Image",
        data=output,
        file_name="qr.png",
        mime="image/png",
    )

st.image(contents)

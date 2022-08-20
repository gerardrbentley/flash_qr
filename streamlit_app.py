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

emb = None
uploaded_img = st.file_uploader('Upload Flash for Center of QR', ['jpg', 'jpeg', 'png'])
if uploaded_img is not None:
    try:
        with st.expander('Show uploaded image'):
            st.image(uploaded_img)
        st.success('Will use this image for center of the QR')
        emb = Image.open(uploaded_img)
    except Exception as e:
        print(e)
        st.error('Could not use uploaded image for center of QR 😢')

qr = qrcode.QRCode(
    version=10,
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
    embeded_image=emb
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

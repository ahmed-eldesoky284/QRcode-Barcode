import streamlit as st
import qrcode
from PIL import Image as PILImage
import io

# دالة لتوليد QR Code مع تخصيص اللون والخلفية وإضافة صورة داخل QR Code
def generate_qr_code(link, color="black", background="white", logo_path=None, logo_size=0.2):
    # توليد QR Code باستخدام مكتبة qrcode
    qr_code = qrcode.QRCode(
        version=1,  # حجم QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_code.add_data(link)
    qr_code.make(fit=True)

    # تخصيص الألوان
    qr_code_image = qr_code.make_image(fill=color, back_color=background)

    # إضافة صورة الشعار داخل QR Code
    if logo_path:
        logo = PILImage.open(logo_path)
        
        # تغيير حجم الشعار بما يتناسب مع حجم QR Code
        logo_size = int(qr_code_image.width * logo_size)
        logo = logo.resize((logo_size, logo_size), PILImage.ANTIALIAS)
        
        # تحديد موضع الصورة داخل الـ QR Code
        logo_position = ((qr_code_image.width - logo.width) // 2, (qr_code_image.height - logo.height) // 2)
        qr_code_image.paste(logo, logo_position, logo.convert("RGBA"))

    return qr_code_image

# واجهة المستخدم
st.title("توليد QR Code أو Barcode")

# اختيار نوع الكود
code_type = st.selectbox("اختر نوع الكود:", ["QR Code", "Barcode"])

if code_type == "QR Code":
    # إدخال الرابط أو النص لتوليد QR Code
    link = st.text_input("أدخل الرابط أو النص لتوليد QR Code:", "")
    
    # تخصيص اللون
    color = st.color_picker("اختر اللون:", "#000000")
    background = st.color_picker("اختر اللون الخلفي:", "#ffffff")

    # رفع الشعار (اختياري)
    logo = st.file_uploader("رفع الشعار لتضمينه داخل QR Code (اختياري)", type=["png", "jpg", "jpeg"])

    # حجم الشعار
    logo_size = st.slider("حجم الشعار داخل QR Code (0 إلى 1)", 0.05, 0.3, 0.2)

    if link:
        # توليد QR Code
        qr_code_image = generate_qr_code(link, color, background, logo_path=logo, logo_size=logo_size)
        st.image(qr_code_image)
    else:
        st.error("يرجى إدخال رابط أو نص لتوليد QR Code.")

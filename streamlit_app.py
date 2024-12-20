import streamlit as st
import pyqrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image as PILImage

# دالة لتوليد QR Code مع تخصيص اللون والخلفية وإضافة صورة داخل QR Code
def generate_qr_code(link, color="black", background="white", logo_path=None, logo_size=0.2):
    # توليد QR Code
    qr_code = pyqrcode.create(link)
    
    # تحويل QR Code إلى صورة PIL
    qr_code_pil = PILImage.open(qr_code.png_as_base64_str(scale=10))
    
    # تخصيص الألوان
    qr_code_pil = qr_code_pil.convert("RGB")
    pixels = qr_code_pil.load()
    
    for i in range(qr_code_pil.width):
        for j in range(qr_code_pil.height):
            if pixels[i, j] == (0, 0, 0):  # إذا كانت الخلية سوداء
                pixels[i, j] = color
            elif pixels[i, j] == (255, 255, 255):  # إذا كانت الخلية بيضاء
                pixels[i, j] = background

    # إضافة صورة شعار داخل QR Code
    if logo_path:
        logo = PILImage.open(logo_path)
        
        # تغيير حجم الشعار بما يتناسب مع حجم QR Code
        logo_size = int(qr_code_pil.width * logo_size)
        logo = logo.resize((logo_size, logo_size), PILImage.ANTIALIAS)
        
        # تحديد موضع الصورة داخل الـ QR Code
        logo_position = ((qr_code_pil.width - logo.width) // 2, (qr_code_pil.height - logo.height) // 2)
        qr_code_pil.paste(logo, logo_position, logo.convert("RGBA"))

    return qr_code_pil

# دالة لتوليد Barcode
def generate_barcode(barcode_number):
    barcode_format = barcode.get_barcode_class('ean13')
    barcode_image = barcode_format(barcode_number, writer=ImageWriter())
    barcode_filename = 'barcode_image'
    barcode_image.save(barcode_filename)
    return f"{barcode_filename}.png"

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

elif code_type == "Barcode":
    # إدخال رقم الباركود لتوليد Barcode
    barcode_number = st.text_input("أدخل رقم الباركود (12 رقمًا):", "123456789012")
    
    if len(barcode_number) == 12:
        barcode_file = generate_barcode(barcode_number)
        st.image(barcode_file)
    else:
        st.error("رقم الباركود يجب أن يحتوي على 12 رقمًا.")

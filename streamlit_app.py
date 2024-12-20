import streamlit as st
import qrcode
import io
from PIL import Image as PILImage
import barcode
from barcode.writer import ImageWriter
import random

# دالة لتوليد QR Code مع تخصيص اللون والخلفية وإضافة صورة داخل QR Code
def generate_qr_code(link, color="black", background="white", logo_path=None, logo_size=0.2):
    # توليد QR Code
    qr_code = qrcode.make(link)
    
    # حفظ الـ QR Code كـ PNG في ذاكرة مؤقتة باستخدام BytesIO
    qr_code_io = io.BytesIO()
    qr_code.save(qr_code_io, format="PNG")
    qr_code_io.seek(0)  # إعادة مؤشر الملف إلى البداية
    
    # تحويل الصورة إلى PIL
    qr_code_pil = PILImage.open(qr_code_io)
    
    # إضافة صورة الشعار داخل الـ QR Code
    if logo_path:
        logo = PILImage.open(logo_path)
        
        # تغيير حجم الشعار بما يتناسب مع حجم QR Code
        logo_size = int(qr_code_pil.width * logo_size)
        logo = logo.resize((logo_size, logo_size), PILImage.ANTIALIAS)

        # تحديد موضع الصورة داخل الـ QR Code
        logo_position = ((qr_code_pil.width - logo.width) // 2, (qr_code_pil.height - logo.height) // 2)
        qr_code_pil.paste(logo, logo_position, logo.convert("RGBA"))

    return qr_code_pil

# دالة لتوليد Barcode مع توليد رقم عشوائي إذا لم يتم إدخاله
def generate_barcode(barcode_number=None):
    if not barcode_number:
        # توليد رقم عشوائي للباركود (12 رقمًا)
        barcode_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    
    barcode_format = barcode.get_barcode_class('ean13')
    barcode_image = barcode_format(barcode_number, writer=ImageWriter())
    barcode_filename = 'barcode_image'
    barcode_image.save(barcode_filename)
    return f"{barcode_filename}.png", barcode_number

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
        if logo:
            qr_code_image = generate_qr_code(link, color, background, logo_path=logo, logo_size=logo_size)
        else:
            qr_code_image = generate_qr_code(link, color, background)
        
        st.image(qr_code_image)

        # تحميل الصورة الناتجة
        qr_code_image_path = io.BytesIO()
        qr_code_image.save(qr_code_image_path, format="PNG")
        qr_code_image_path.seek(0)
        
        st.download_button(
            label="تحميل QR Code",
            data=qr_code_image_path,
            file_name="qrcode.png",
            mime="image/png"
        )
    else:
        st.error("يرجى إدخال رابط أو نص لتوليد QR Code.")

elif code_type == "Barcode":
    # إدخال رقم الباركود أو توليد رقم عشوائي
    barcode_number = st.text_input("أدخل رقم الباركود (12 رقمًا) أو اتركه لتوليد رقم عشوائي:", "")
    
    # توليد Barcode
    barcode_file, barcode_number_generated = generate_barcode(barcode_number if barcode_number else None)
    
    # عرض Barcode
    st.image(barcode_file)
    
    # عرض الرقم الذي تم توليده
    st.write(f"رقم الباركود الذي تم توليده: {barcode_number_generated}")

    # تحميل الصورة الناتجة
    with open(barcode_file, "rb") as barcode_image:
        barcode_image_bytes = barcode_image.read()

    st.download_button(
        label="تحميل Barcode",
        data=barcode_image_bytes,
        file_name="barcode.png",
        mime="image/png"
    )

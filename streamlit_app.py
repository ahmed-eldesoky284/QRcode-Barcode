import streamlit as st
import barcode
from barcode.writer import ImageWriter
from IPython.display import Image as IPImage
import random
import io

# دالة لتوليد رقم عشوائي مكون من 12 رقمًا
def generate_barcode_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

# دالة لتوليد Barcode
def generate_barcode(barcode_number=None):
    if not barcode_number:
        # توليد رقم عشوائي للباركود (12 رقمًا)
        barcode_number = generate_barcode_number()
    
    # تحديد نوع الباركود (مثال: 'ean13')
    barcode_format = barcode.get_barcode_class('ean13')
    
    # توليد الباركود باستخدام ImageWriter لكتابة الصورة
    barcode_image = barcode_format(barcode_number, writer=ImageWriter())
    
    # حفظ الصورة الناتجة
    barcode_filename = 'barcode_image'
    barcode_image.save(barcode_filename)

    return barcode_filename, barcode_number

# واجهة المستخدم
st.title("توليد QR Code أو Barcode")

# اختيار نوع الكود
code_type = st.selectbox("اختر نوع الكود:", ["QR Code", "Barcode"])

if code_type == "QR Code":
    # إدخال الرابط أو النص لتوليد QR Code
    link = st.text_input("أدخل الرابط أو النص لتوليد QR Code:", "")
    
    # تخصيص اللون
    color = st.color_picker("اختر لون الخطوط لـ QR Code:", "#000000")  # اللون الأساسي لـ QR Code
    background = st.color_picker("اختر اللون الخلفي لـ QR Code:", "#ffffff")  # اللون الخلفي

    # رفع الشعار (اختياري)
    logo = st.file_uploader("رفع الشعار لتضمينه داخل QR Code (اختياري)", type=["png", "jpg", "jpeg"])

    # رفع صورة الخلفية (اختياري)
    background_image = st.file_uploader("رفع صورة الخلفية لـ QR Code (اختياري)", type=["png", "jpg", "jpeg"])

    # حجم الشعار
    logo_size = st.slider("حجم الشعار داخل QR Code (0 إلى 1)", 0.05, 0.3, 0.2)

    # التحكم في حجم QR Code باستخدام شريط تمرير
    box_size = st.slider("حجم QR Code (box size)", 5, 20, 10)

    if link:
        # توليد QR Code مع الخلفية والشعار
        if background_image:
            qr_code_image = generate_qr_code(link, color, background, logo_path=logo, logo_size=logo_size, background_image_path=background_image, box_size=box_size)
        else:
            qr_code_image = generate_qr_code(link, color, background, logo_path=logo, logo_size=logo_size, box_size=box_size)
        
        # تحويل الصورة إلى تنسيق يمكن لـ Streamlit التعامل معه
        qr_code_image_path = io.BytesIO()
        qr_code_image.save(qr_code_image_path, format="PNG")
        qr_code_image_path.seek(0)

        st.image(qr_code_image_path)

        # تحميل الصورة الناتجة
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
    st.image(f'{barcode_file}.png')  # عرض الصورة مباشرة
    
    # عرض الرقم الذي تم توليده
    st.write(f"الرقم الذي تم توليده للباركود هو: {barcode_number_generated}")

    # تحميل الصورة الناتجة
    with open(f'{barcode_file}.png', "rb") as barcode_image:
        barcode_image_bytes = barcode_image.read()

    st.download_button(
        label="تحميل Barcode",
        data=barcode_image_bytes,
        file_name="barcode.png",
        mime="image/png"
    )

import streamlit as st
import pandas as pd

# إعداد الصفحة مع العنوان والأيقونة
st.set_page_config(
    page_title="منظومة تسجيل المقررات الدراسية",
    page_icon="🎓",
    layout="centered"
)

# تخصيص التصميم ودعم الهواتف الذكية واللغة العربية (اتزان اليمين لليسار)
st.markdown("""
    <style>
    body, html, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    .university-header {
        font-size: 26px;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .department-header {
        font-size: 22px;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .main-header {
        font-size: 20px;
        color: #475569;
        text-align: center;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 14px;
        color: #64748B;
        text-align: center;
        margin-bottom: 20px;
    }
    .student-card {
        background-color: #F8FAFC;
        border-right: 5px solid #2563EB;
        border-left: none;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: right;
    }
    /* تصميم متجاوب لترتيب معلومات الطالب عمودياً على شاشات الجوال */
    .info-grid {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        direction: rtl;
        gap: 10px;
    }
    .info-item {
        flex: 1 1 45%;
        min-width: 140px;
    }
    @media (max-width: 640px) {
        .info-item {
            flex: 1 1 100%;
        }
        .university-header { font-size: 22px; }
        .department-header { font-size: 19px; }
        .main-header { font-size: 17px; }
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 40px;
    }
    .stTextInput label {
        direction: rtl;
    }
    /* تكبير خط نص الزر وجعله بارزاً */
    .stButton button p {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    .stButton button {
        direction: rtl;
        height: 48px;
    }
    /* توسيط نصوص جميع خلايا وعناوين جداول البيانات بدقة وتوفير التمرير الأفقي للجوال */
    [data-testid="stDataFrame"] {
        overflow-x: auto;
    }
    [data-testid="stDataFrame"] table, 
    [data-testid="stDataFrame"] th, 
    [data-testid="stDataFrame"] td {
        text-align: center !important;
        justify-content: center !important;
    }
    /* محاذاة عنوان البحث إلى اليمين */
    .search-title {
        text-align: right;
        font-weight: bold;
        font-size: 18px;
        color: #1E3A8A;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    /* محاذاة عناوين الأقسام إلى اليمين */
    .section-title {
        text-align: right;
        font-weight: bold;
        font-size: 18px;
        color: #1E3A8A;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# رأس الصفحة بخطوط متجاوبة
st.markdown('<div class="university-header">جامعة بنغازي — كلية الآداب والعلوم سلوق</div>', unsafe_allow_html=True)
st.markdown('<div class="department-header">قسم اللغة الإنجليزية</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header">🎓 منظومة تنزيل المواد الدراسية للطلبة</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">بوابة الاستعلام عن الجداول الدراسية والبيانات الأكاديمية</div>', unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 0px; margin-bottom: 20px;'>", unsafe_allow_html=True)

excel_file = "student_portal_database.xlsx"

@st.cache_data
def load_data(file):
    df_courses = pd.read_excel(file, sheet_name="المواد المسجلة")
    df_students = pd.read_excel(file, sheet_name="بيانات الطلبة")
    return df_courses, df_students

try:
    df_courses, df_students = load_data(excel_file)
except Exception as e:
    st.error(f"خطأ في تحميل ملف قاعدة البيانات: {e}")
    st.stop()

# حقل البحث مع محاذاة العنوان إلى اليمين
st.markdown('<div class="search-title">🔍 أدخل الرقم الدراسي</div>', unsafe_allow_html=True)
student_id_input = st.text_input("أدخل الرقم الجامعي للطالب:", placeholder="مثال: 4808", label_visibility="collapsed")

search_clicked = st.button("عرض الجدول الدراسي", type="primary", use_container_width=True)

if search_clicked:
    if student_id_input:
        try:
            search_id = float(student_id_input)
        except ValueError:
            search_id = student_id_input

        # تصفية البيانات حسب الرقم الجامعي
        student_info = df_students[df_students['الرقم الجامعي'].astype(str).str.contains(str(student_id_input))]
        student_records = df_courses[df_courses['الرقم الجامعي'].astype(str).str.contains(str(student_id_input))]

        if not student_records.empty:
            st.success("تم العثور على بيانات الطالب بنجاح!")
            
            # ترتيب الأعمدة من اليمين لليسار في العرض
            display_columns = ['موعد المحاضرة', 'المحاضر', 'الوحدات', 'اسم المادة', 'رمز المادة']
            existing_columns = [col for col in display_columns if col in student_records.columns]
            
            # تجهيز الجدول وإسقاط الفهرس التسلسلي
            student_records_display = student_records[existing_columns].reset_index(drop=True)

            # استخراج معلومات الطالب
            if not student_info.empty:
                s_name = student_info['اسم الطالب'].values[0]
                s_program = student_info['البرنامج'].values[0]
                s_status = student_info['الحالة'].values[0]
            else:
                s_name = "غير متوفر"
                s_program = "اللغة الانجليزية"
                s_status = "منتظم"

            # بطاقة معلومات الطالب بتصميم متجاوب مع الهواتف الذكية
            st.markdown(f"""
                <div class="student-card">
                    <h4 style="margin-top: 0px; color: #1E3A8A; text-align: right; font-size: 17px;">👤 معلومات الطالب</h4>
                    <hr style="margin: 5px 0 12px 0;">
                    <div class="info-grid">
                        <div class="info-item"><b>الاسم:</b> {s_name}</div>
                        <div class="info-item"><b>الرقم الجامعي:</b> {student_id_input}</div>
                        <div class="info-item"><b>القسم:</b> {s_program}</div>
                        <div class="info-item"><b>الوضع الدراسي:</b> {s_status}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # عنوان جدول المقررات محاذى إلى اليمين
            st.markdown('<div class="section-title">📅 جدول المقررات الدراسية:</div>', unsafe_allow_html=True)
            
            # عرض الجدول مع التوسيط لجميع الخلايا ودعم التمرير
            st.dataframe(student_records_display, use_container_width=True, hide_index=True)
            
        else:
            st.warning(f"عذراً، لم يتم العثور على أي مقررات مسجلة للرقم الجامعي: {student_id_input}")
    else:
        st.error("الرجاء إدخال الرقم الجامعي للطالب أولاً.")

# تذييل الصفحة
st.markdown('<div class="footer">كلية الآداب والعلوم سلوق — بوابة الإدارة الأكاديمية © 2026</div>', unsafe_allow_html=True)
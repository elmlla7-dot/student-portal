import streamlit as st
import pandas as pd

# إعداد الصفحة مع العنوان والأيقونة
st.set_page_config(
    page_title="منظومة تسجيل المقررات الدراسية",
    page_icon="🎓",
    layout="centered"
)

# تخصيص التصميم ليتناسب بسلاسة فائقة مع متصفحات الهواتف المحمولة وتوجيه الواجهة (RTL)
st.markdown("""
    <style>
    body, html, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    
    /* تحسين الهوامش العامة لتناسب الشاشات الصغيرة */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }

    .university-header {
        font-size: 20px;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .department-header {
        font-size: 17px;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 6px;
    }
    .main-header {
        font-size: 16px;
        color: #475569;
        text-align: center;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .sub-header {
        font-size: 13px;
        color: #64748B;
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* بطاقة الطالب المتجاوبة مع الهواتف */
    .student-card {
        background-color: #F8FAFC;
        border-right: 4px solid #2563EB;
        border-left: none;
        padding: 12px;
        border-radius: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        text-align: right;
    }
    .info-grid {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        direction: rtl;
        gap: 8px;
    }
    .info-item {
        flex: 1 1 100%;
        min-width: 100%;
        font-size: 14px;
    }
    
    @media (min-width: 640px) {
        .info-item {
            flex: 1 1 45%;
            min-width: 140px;
        }
        .university-header { font-size: 24px; }
        .department-header { font-size: 20px; }
        .main-header { font-size: 18px; }
    }

    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        margin-top: 30px;
    }
    
    .stTextInput label {
        direction: rtl;
        font-size: 14px;
    }
    
    .stButton button p {
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    .stButton button {
        direction: rtl;
        height: 45px;
        width: 100%;
    }
    
    /* ضمان التمرير السليم للجداول على الهواتف */
    [data-testid="stDataFrame"] {
        direction: rtl !important;
        overflow-x: auto;
        max-width: 100%;
    }
    
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] td,
    [data-testid="stDataFrame"] div,
    [data-testid="stDataFrame"] span {
        text-align: center !important;
        text-align-last: center !important;
        font-size: 13px !important;
    }
    
    [data-testid="stDataFrame"] td div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
    }

    .search-title, .section-title {
        text-align: right;
        font-weight: bold;
        font-size: 16px;
        color: #1E3A8A;
        margin-top: 10px;
        margin-bottom: 6px;
    }
    
    /* تحسين مظهر التبويبات على الموبايل */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 13px !important;
        padding: 8px 12px;
    }
    </style>
""", unsafe_allow_html=True)

# رأس الصفحة
st.markdown('<div class="university-header">جامعة بنغازي — كلية الآداب والعلوم سلوق</div>', unsafe_allow_html=True)
st.markdown('<div class="department-header">قسم اللغة الإنجليزية</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header">🎓 منظومة تنزيل المواد الدراسية والنتائج</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">بوابة الاستعلام عن الجداول الدراسية والسجل الأكاديمي</div>', unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 0px; margin-bottom: 15px;'>", unsafe_allow_html=True)

excel_file = "student_portal_database.xlsx"

@st.cache_data
def load_data(file):
    df_courses = pd.read_excel(file, sheet_name="المواد المسجلة")
    df_students = pd.read_excel(file, sheet_name="بيانات الطلبة")
    df_transcript = pd.read_excel(file, sheet_name="السجل الدراسي والنتائج")
    return df_courses, df_students, df_transcript

try:
    df_courses, df_students, df_transcript = load_data(excel_file)
except Exception as e:
    st.error(f"خطأ في تحميل ملف قاعدة البيانات: {e}")
    st.stop()

# حقل البحث
st.markdown('<div class="search-title">🔍 أدخل الرقم الدراسي</div>', unsafe_allow_html=True)
student_id_input = st.text_input("أدخل الرقم الجامعي للطالب:", placeholder="مثال: 4808 أو 7000", label_visibility="collapsed")

search_clicked = st.button("عرض البيانات الأكاديمية", type="primary", use_container_width=True)

if search_clicked:
    if student_id_input:
        try:
            search_id_clean = int(float(student_id_input))
        except:
            search_id_clean = student_id_input

        # إنشاء التبويبات
        tab1, tab2 = st.tabs(["📅 الجدول الحالي", "📊 السجل والنتائج"])
        
        # استخراج معلومات الطالب العامة
        student_info = df_students[df_students['الرقم الجامعي'].astype(str).str.contains(str(search_id_clean))]
        if not student_info.empty:
            s_name = student_info['اسم الطالب'].values[0]
            s_program = student_info[' البرنامح '].values[0] if ' البرنامح ' in student_info.columns else student_info['البرنامج'].values[0] if 'البرنامج' in student_info.columns else "اللغة الانجليزية"
            s_status = student_info['الحالة'].values[0]
        else:
            s_name = "غير متوفر"
            s_program = "اللغة الانجليزية"
            s_status = "منتظم"

        # بطاقة معلومات الطالب المشتركة
        student_card_html = f"""
            <div class="student-card">
                <h4 style="margin-top: 0px; color: #1E3A8A; text-align: right; font-size: 15px;">👤 معلومات الطالب</h4>
                <hr style="margin: 4px 0 8px 0;">
                <div class="info-grid">
                    <div class="info-item"><b>الاسم:</b> {s_name}</div>
                    <div class="info-item"><b>الرقم الجامعي:</b> {student_id_input}</div>
                    <div class="info-item"><b>القسم:</b> {s_program}</div>
                    <div class="info-item"><b>الوضع:</b> {s_status}</div>
                </div>
            </div>
        """

        # استخراج مقررات الجدول الحالي لهذا الطالب لتحديد المواد قيد الإنجاز
        current_student_courses = df_courses[df_courses['الرقم الجامعي'].astype(str).str.contains(str(search_id_clean))]
        current_enrolled_codes = set()
        for _, c_row in current_student_courses.iterrows():
            if 'رمز المادة' in c_row and pd.notna(c_row['رمز المادة']):
                try:
                    current_enrolled_codes.add(str(int(float(c_row['رمز المادة']))).strip())
                except:
                    current_enrolled_codes.add(str(c_row['رمز المادة']).strip())

        # --- التبويب الأول: الجدول الدراسي الحالي ---
        with tab1:
            st.markdown(student_card_html, unsafe_allow_html=True)
            
            if not current_student_courses.empty:
                st.success("تم العثور على جدول المواد المسجلة بنجاح!")
                display_columns = ['موعد المحاضرة', 'المحاضر', 'الوحدات', 'اسم المادة', 'رمز المادة']
                existing_columns = [col for col in display_columns if col in current_student_courses.columns]
                student_records_display = current_student_courses[existing_columns].reset_index(drop=True)
                st.dataframe(student_records_display, use_container_width=True, hide_index=True)
            else:
                st.warning(f"عذراً، لم يتم العثور على أي مقررات مسجلة لهذا الرقم في الجدول الحالي.")

        # --- التبويب الثاني: السجل الدراسي والنتائج ---
        with tab2:
            st.markdown(student_card_html, unsafe_allow_html=True)
            
            target_col_idx = None
            row0 = df_transcript.iloc[0]
            for idx in range(6, len(df_transcript.columns)):
                val = row0.iloc[idx]
                if pd.notna(val):
                    try:
                        if int(float(val)) == int(float(search_id_clean)):
                            target_col_idx = idx
                            break
                    except:
                        if str(search_id_clean) in str(val):
                            target_col_idx = idx
                            break
            
            if target_col_idx is not None:
                target_col = df_transcript.columns[target_col_idx]
                
                col_code = df_transcript.columns[0]
                col_name = df_transcript.columns[1]
                col_prereq = df_transcript.columns[2]
                col_schedule = df_transcript.columns[3]
                col_prof = df_transcript.columns[4]
                
                passed_courses = {}
                for idx, row in df_transcript.iterrows():
                    c_code = row.get(col_code, "")
                    if pd.isna(c_code) or str(c_code).strip() == "" or str(c_code).lower() == "nan": continue
                    try:
                        c_code_clean = str(int(float(c_code))).strip()
                    except:
                        c_code_clean = str(c_code).strip()
                        
                    c_status_val = row.get(target_col, 0)
                    try:
                        passed_courses[c_code_clean] = int(float(c_status_val)) == 1
                    except:
                        passed_courses[c_code_clean] = False

                transcript_data = []
                for idx, row in df_transcript.iterrows():
                    c_name = row.get(col_name, "")
                    
                    # التحقق إذا كان الصف يمثل فاصل للفصل الدراسي
                    if pd.notna(c_name) and ("الفصل" in str(c_name) or "Semester" in str(c_name)):
                        transcript_data.append({
                            'الاستاذ': '',
                            'الجدول': '',
                            'حالة المقرر': '',
                            'الأسبقية': '',
                            'اسم المادة / الفصل': f"─── {c_name} ───",
                            'رقم المقرر': ''
                        })
                        continue
                        
                    c_code = row.get(col_code, "")
                    if pd.isna(c_code) or str(c_code).strip() == "" or str(c_code).lower() == "nan":
                        continue
                    
                    try:
                        c_code_clean = str(int(float(c_code))).strip()
                    except:
                        c_code_clean = str(c_code).strip()
                        
                    c_prereq = row.get(col_prereq, "")
                    c_schedule = row.get(col_schedule, "")
                    c_prof = row.get(col_prof, "")
                    
                    try:
                        student_mark = int(float(row.get(target_col, 0)))
                    except:
                        student_mark = 0
                    
                    # تحديد حالة المقرر
                    if student_mark == 1:
                        status_str = "ناجح"
                    elif c_code_clean in current_enrolled_codes:
                        status_str = "قيد الإنجاز"
                    else:
                        if pd.isna(c_prereq) or str(c_prereq).strip() == "" or str(c_prereq).lower() == "nan" or str(c_prereq).strip() == "0" or str(c_prereq).strip() == "لا يوجد":
                            status_str = "متاح"
                        else:
                            try:
                                prereq_clean = str(int(float(c_prereq))).strip()
                            except:
                                prereq_clean = str(c_prereq).strip()
                                
                            if prereq_clean in passed_courses and passed_courses[prereq_clean]:
                                status_str = "متاح"
                            else:
                                status_str = "أسبقية"
                    
                    display_prereq = str(c_prereq).strip()
                    if pd.isna(c_prereq) or display_prereq == "" or display_prereq.lower() == "nan" or display_prereq == "0":
                        display_prereq = "لا يوجد"
                    else:
                        try:
                            display_prereq = str(int(float(c_prereq)))
                        except:
                            pass

                    transcript_data.append({
                        'الاستاذ': c_prof if pd.notna(c_prof) else "-",
                        'الجدول': c_schedule if pd.notna(c_schedule) else "-",
                        'حالة المقرر': status_str,
                        'الأسبقية': display_prereq,
                        'اسم المادة / الفصل': c_name,
                        'رقم المقرر': c_code_clean
                    })
                
                df_result_transcript = pd.DataFrame(transcript_data)
                
                # ترتيب الأعمدة مع وضع "حالة المقرر" بين "الأسبقية" و "الجدول"
                df_result_transcript = df_result_transcript[['الاستاذ', 'الجدول', 'حالة المقرر', 'الأسبقية', 'اسم المادة / الفصل', 'رقم المقرر']]

                # دالة تلوين خلايا عمود "حالة المقرر"
                def highlight_status(val):
                    if val == "ناجح":
                        return 'background-color: #FEF3C7; color: #92400E; font-weight: bold; text-align: center;'
                    elif val == "متاح":
                        return 'background-color: #D1E7DD; color: #0F5132; font-weight: bold; text-align: center;'
                    elif val == "قيد الإنجاز":
                        return 'background-color: #DBEAFE; color: #1E40AF; font-weight: bold; text-align: center;'
                    elif val == "أسبقية":
                        return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold; text-align: center;'
                    return 'text-align: center;'

                styled_df = df_result_transcript.style.map(highlight_status, subset=['حالة المقرر'])

                st.success("تم تحديث السجل الدراسي بنجاح!")
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                st.warning(f"عذراً، لم يتم العثور على أعمدة نتائج مخصصة للرقم الجامعي: {student_id_input} في شيت السجل الدراسي.")
    else:
        st.error("الرجاء إدخال الرقم الجامعي للطالب أولاً.")

# تذييل الصفحة
st.markdown('<div class="footer">كلية الآداب والعلوم سلوق — بوابة الإدارة الأكاديمية © 2026</div>', unsafe_allow_html=True)
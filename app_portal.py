import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# إعداد الصفحة مع العنوان والأيقونة
st.set_page_config(
    page_title="منظومة تسجيل المقررات الدراسية",
    page_icon="🎓",
    layout="centered"
)

# تخصيص التصميم وتوجيه الواجهة (RTL) وتنسيق الطباعة A4 Portrait
st.markdown("""
    <style>
    body, html, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    
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
    
    .student-card {
        background-color: #F8FAFC;
        border-right: 4px solid #2563EB;
        border-left: none;
        padding: 12px;
        border-radius: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        text-align: right;
        direction: rtl;
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
        text-align: right;
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

    .search-title, .section-title {
        text-align: right;
        font-weight: bold;
        font-size: 16px;
        color: #1E3A8A;
        margin-top: 10px;
        margin-bottom: 6px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 13px !important;
        padding: 8px 12px;
    }

    /* تنسيق الجداول لضمان اتجاه اليمين لليسار بدقة وثبات */
    table.custom-rtl-table {
        width: 100% !important;
        border-collapse: collapse !important;
        direction: rtl !important;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    table.custom-rtl-table th, table.custom-rtl-table td {
        padding: 9px !important;
        text-align: right !important;
        direction: rtl !important;
        border: 1px solid #cbd5e1 !important;
        font-size: 12px !important;
    }
    table.custom-rtl-table th {
        background-color: #f1f5f9 !important;
        color: #1e3a8a !important;
        text-align: right !important;
    }

    /* إعدادات الطباعة المباشرة على مقاس A4 Portrait وبدون عناصر تحكم */
    @media print {
        @page {
            size: A4 portrait;
            margin: 10mm;
        }
        .stButton, .stTextInput, header, footer, [data-testid="stSidebar"], [data-testid="stDecoration"], iframe {
            display: none !important;
        }
        body, html, [class*="css"] {
            direction: rtl;
            text-align: right;
            background-color: white !important;
            font-size: 11px !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        tr {
            page-break-inside: avoid !important;
        }
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

        tab1, tab2 = st.tabs(["📅 الجدول الحالي", "📊 السجل والنتائج"])
        
        student_info = df_students[df_students['الرقم الجامعي'].astype(str).str.contains(str(search_id_clean))]
        if not student_info.empty:
            s_name = student_info['اسم الطالب'].values[0]
            s_program = student_info[' البرنامح '].values[0] if ' البرنامح ' in student_info.columns else student_info['البرنامج'].values[0] if 'البرنامج' in student_info.columns else "اللغة الانجليزية"
            s_status = student_info['الحالة'].values[0]
        else:
            s_name = "غير متوفر"
            s_program = "اللغة الانجليزية"
            s_status = "منتظم"

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
                display_columns = ['رمز المادة', 'اسم المادة', 'الوحدات', 'المحاضر', 'موعد المحاضرة']
                existing_columns = [col for col in display_columns if col in current_student_courses.columns]
                student_records_display = current_student_courses[existing_columns].copy().reset_index(drop=True)
                
                # تحويل عمود الوحدات إلى رقم صحيح بدون علامة عشرية إن وجد
                if 'الوحدات' in student_records_display.columns:
                    def clean_units(val):
                        try:
                            return str(int(float(val)))
                        except:
                            return val if pd.notna(val) else "-"
                    student_records_display['الوحدات'] = student_records_display['الوحدات'].apply(clean_units)

                def render_rtl_table(df):
                    cols = list(df.columns)
                    html = "<div style='overflow-x:auto;'><table class='custom-rtl-table'><thead><tr>"
                    for col in cols:
                        html += f"<th>{col}</th>"
                    html += "</tr></thead><tbody>"
                    for _, row in df.iterrows():
                        html += "<tr>"
                        for col in cols:
                            val = row[col] if pd.notna(row[col]) else "-"
                            html += f"<td>{val}</td>"
                        html += "</tr>"
                    html += "</tbody></table></div>"
                    return html

                st.markdown(render_rtl_table(student_records_display), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                print_html_schedule = """
                <div style="text-align: center; direction: rtl;">
                    <button onclick="parent.window.print();" style="
                        background-color: #2563EB;
                        color: white;
                        border: none;
                        padding: 12px 20px;
                        font-size: 16px;
                        font-family: inherit;
                        font-weight: bold;
                        border-radius: 6px;
                        cursor: pointer;
                        width: 100%;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    ">🖨️ طباعة أو حفظ الجدول (PDF)</button>
                </div>
                """
                components.html(print_html_schedule, height=55)
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
                    
                    if pd.notna(c_name) and ("الفصل" in str(c_name) or "Semester" in str(c_name)):
                        transcript_data.append({
                            'رقم المقرر': '',
                            'اسم المادة / الفصل': f"─── {c_name} ───",
                            'الأسبقية': '',
                            'حالة المقرر': '',
                            'الجدول': '',
                            'الاستاذ': ''
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
                    
                    prof_str = str(c_prof).strip() if pd.notna(c_prof) else "-"
                    if prof_str == "" or prof_str == "0" or prof_str.lower() == "nan":
                        prof_str = "-"

                    try:
                        student_mark = int(float(row.get(target_col, 0)))
                    except:
                        student_mark = 0
                    
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
                        'رقم المقرر': c_code_clean,
                        'اسم المادة / الفصل': c_name,
                        'الأسبقية': display_prereq,
                        'حالة المقرر': status_str,
                        'الجدول': c_schedule if pd.notna(c_schedule) else "-",
                        'الاستاذ': prof_str
                    })
                
                df_result_transcript = pd.DataFrame(transcript_data)
                
                def render_transcript_table(df):
                    cols = ['رقم المقرر', 'اسم المادة / الفصل', 'الأسبقية', 'حالة المقرر', 'الجدول', 'الاستاذ']
                    html = "<div style='overflow-x:auto;'><table class='custom-rtl-table'><thead><tr>"
                    for col in cols:
                        html += f"<th>{col}</th>"
                    html += "</tr></thead><tbody>"
                    
                    for _, row in df.iterrows():
                        html += "<tr>"
                        is_header_row = "───" in str(row['اسم المادة / الفصل'])
                        
                        if is_header_row:
                            val = row['اسم المادة / الفصل']
                            html += f"<td colspan='6' style='background-color: #e2e8f0; font-weight: bold; text-align: center; color: #1e3a8a;'>{val}</td>"
                        else:
                            for col in cols:
                                val = row[col]
                                bg_style = ""
                                if col == 'حالة المقرر':
                                    if val == "ناجح":
                                        bg_style = "background-color: #FEF3C7; color: #92400E; font-weight: bold;"
                                    elif val == "متاح":
                                        bg_style = "background-color: #D1E7DD; color: #0F5132; font-weight: bold;"
                                    elif val == "قيد الإنجاز":
                                        bg_style = "background-color: #DBEAFE; color: #1E40AF; font-weight: bold;"
                                    elif val == "أسبقية":
                                        bg_style = "background-color: #FEE2E2; color: #991B1B; font-weight: bold;"
                                html += f"<td style='{bg_style}'>{val}</td>"
                        html += "</tr>"
                    html += "</tbody></table></div>"
                    return html

                st.success("تم تحديث السجل الدراسي بنجاح!")
                
                st.markdown(render_transcript_table(df_result_transcript), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                print_html_transcript = """
                <div style="text-align: center; direction: rtl;">
                    <button onclick="parent.window.print();" style="
                        background-color: #2563EB;
                        color: white;
                        border: none;
                        padding: 12px 20px;
                        font-size: 16px;
                        font-family: inherit;
                        font-weight: bold;
                        border-radius: 6px;
                        cursor: pointer;
                        width: 100%;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    ">🖨️ طباعة أو حفظ السجل كامل (PDF)</button>
                </div>
                """
                components.html(print_html_transcript, height=55)
            else:
                st.warning(f"عذراً، لم يتم العثور على أعمدة نتائج مخصصة للرقم الجامعي: {student_id_input} في شيت السجل الدراسي.")
    else:
        st.error("الرجاء إدخال الرقم الجامعي للطالب أولاً.")

st.markdown('<div class="footer">كلية الآداب والعلوم سلوق — بوابة الإدارة الأكاديمية © 2026</div>', unsafe_allow_html=True)
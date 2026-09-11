import streamlit as st

def apply_custom_theme():
    st.markdown("""
    <style>
        /* 1. خلفية التطبيق الرئيسية ولون النصوص */
        .stApp {
            background-color: #0d1b2a;
            color: #ffffdd;
        }
        
        /* 2. العناوين والنصوص الرئيسية */
        h1, h2, h3, h4, h5, h6, .stMarkdown p {
            color: #ffffdd !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* 3. إصلاح وتنسيق الشريط الجانبي (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #1b263b !important;
            border-left: 1px solid #415a77;
        }
        
        /* إجبار جميع النصوص والعناوين داخل الشريط الجانبي على الظهور باللون الأبيض */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* تنسيق تسميات المدخلات (Labels) داخل الشريط الجانبي */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stWidgetLabel p {
            color: #f8fafc !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* 4. تنسيق حقول الإدخال والـ Selectbox داخل الشريط الجانبي */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] input {
            background-color: #0d1b2a !important;
            color: #ffffff !important;
            border: 1px solid #415a77 !important;
            border-radius: 6px !important;
        }

        /* 5. الأزرار العامة */
        .stButton>button {
            background-color: #1b263b;
            color: #ffffdd;
            border: 1px solid #e0e1dd;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #415a77;
            border-color: #ffffdd;
            color: #ffffff;
        }
        
        /* 6. كتل الأكواد البرمجية */
        .stCodeBlock {
            border: 1px solid #415a77;
            border-radius: 6px;
        }
    </style>
    """, unsafe_allow_html=True)
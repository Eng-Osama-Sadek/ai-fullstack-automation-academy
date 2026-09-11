import sys
from pathlib import Path
import os
import requests
import asyncio
import streamlit as st

# إضافة المجلد الرئيسي للمشروع إلى مسارات بايثون
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent))

from utils.styles import apply_custom_theme
from utils.curriculum import COURSES_DATA
from services.ai_engine import AITutorEngine
from services.exporter import export_to_docx, export_to_pdf
from services.ticket_processor import run_ticket_pipeline, RawTicket

# ==========================================
# 1. إعداد واجهة Streamlit
# ==========================================
st.set_page_config(
    page_title="AI Full-Stack & Automation Academy",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التنسيق الخاص الأساسي
apply_custom_theme()

# ==========================================
# تحسين شامل ومتقدم للتنسيق البصري (CSS UI/UX Polish)
# ==========================================
st.markdown(
    """
    <style>
    /* 1. استيراد خط Cairo الأنيق */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', -apple-system, BlinkMacSystemFont, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }

    /* 2. تحسين العناوين والنصوص */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
        color: #38BDF8 !important;
        letter-spacing: -0.02em !important;
    }
    
    p, li, label, div {
        color: #E2E8F0 !important;
        line-height: 1.8 !important;
        font-size: 15px !important;
    }

    /* 3. تصميم البطاقات والحاويات المجمعة (Modern Dashboard Cards) */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] {
        border-radius: 12px !important;
    }

    /* 4. إجبار وتنسيق اتجاه النصوص داخل مربع الإدخال */
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"] input,
    textarea, input {
        direction: rtl !important;
        text-align: right !important;
        color: #0F172A !important;             
        background-color: #FFFFFF !important;    
        font-weight: 600 !important;             
        font-size: 15px !important;
        font-family: 'Cairo', sans-serif !important;
        border-radius: 8px !important;
        -webkit-text-fill-color: #0F172A !important;
    }

    div[data-baseweb="textarea"] textarea::placeholder,
    div[data-baseweb="input"] input::placeholder {
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
    }

    /* 5. الشريط الجانبي Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-left: 1px solid #334155 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* 6. ضبط كتلة الكود البرمجي بالكامل (LTR Isolation) */
    div[data-testid="stCodeBlock"], pre, code {
        direction: ltr !important;
        text-align: left !important;
        font-family: 'Fira Code', 'Consolas', monospace !important;
    }
    
    div[data-testid="stCodeBlock"] {
        background-color: #020617 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }

    pre code, .stCodeBlock code {
        color: #38BDF8 !important;
        background-color: transparent !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    code:not(pre code) {
        color: #38BDF8 !important;
        background-color: #1E293B !important;
        padding: 2px 8px !important;
        border-radius: 4px !important;
        direction: ltr !important;
        display: inline-block !important;
    }

    /* 7. تحسين مخرجات الـ JSON ومؤشرات الأرقام */
    div[data-testid="stJson"] {
        background-color: #020617 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        direction: ltr !important;
        text-align: left !important;
    }
    div[data-testid="stJson"] * {
        color: #38BDF8 !important;
        -webkit-text-fill-color: #38BDF8 !important;
        font-family: 'Fira Code', 'Consolas', monospace !important;
    }

    div[data-testid="stMetricValue"] * {
        color: #38BDF8 !important;
        -webkit-text-fill-color: #38BDF8 !important;
    }
    div[data-testid="stMetricLabel"] * {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
    }

    /* 8. تحسين تصميم الأزرار */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Cairo', sans-serif !important;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border: 1px solid #38BDF8 !important;
        color: #38BDF8 !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        background: #38BDF8 !important;
        color: #0F172A !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⚡ منصة الاحتراف: Senior Full-Stack & AI Automation Engineer")
st.caption("من الصفر إلى أعلى مستويات الخبرة البرمجية مع المساعد الذكي التفاعلي")

# ------------------------------------------
# الشريط الجانبي (Sidebar)
# ------------------------------------------
st.sidebar.title("📌 المسارات والضبط")
track = st.sidebar.selectbox("اختر المسار البرمجي للتدريب:", list(COURSES_DATA.keys()))

api_key = st.sidebar.text_input(
    "مفتاح Gemini API Key (لتفعيل المساعد الذكي):",
    type="password",
    help="أدخل مفتاح API الخاص بك لتشغيل المساعد الذكي وتحليل التمارين."
)

st.sidebar.divider()
st.sidebar.markdown("### 🌐 حالة الخادم (Backend)")
st.sidebar.info("FastAPI Server: Running independently")
st.sidebar.code("POST http://127.0.0.1:8000/api/v1/ask-tutor", language="bash")

# ------------------------------------------
# الشاشة الرئيسية (Main Layout)
# ------------------------------------------
ai_tutor = AITutorEngine(api_key=api_key)

col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"📘 مسار: {track}")
    course_info = COURSES_DATA[track]
    
    st.markdown("### 🎯 الموضوعات والتقنيات الرئيسية:")
    for topic in course_info["topics"]:
        st.markdown(f"- **{topic}**")
        
    st.markdown(f"**عدد التمارين والمشاريع المتاحة:** `{course_info['exercises_count']}+ تمرين ومفهوم متقدم`")
    st.markdown(f"**المشروع النهائي (Capstone Project):** {course_info['capstone_project']}")

    st.divider()
    
    st.header("💻 المساعد الذكي ومحلل الأكواد والتمارين")
    st.write("اطرح أي سؤال، اطلب تمرينًا جديداً، أو ضع كودك هنا للمراجع وتصحيح الأخطاء وفق أعلى معايير الـ Clean Code:")

    user_query = st.text_area(
        "أدخل سؤالك أو الكود البرمجي هنا:",
        placeholder="مثال: اعطني تمرينًا متقدمًا في هذا المسار مع كود الحل والشرح التفصيلي...",
        height=180
    )
    
    btn_col1, btn_col2 = st.columns([1, 1])
    
    with btn_col1:
        if st.button("🚀 استشارة المساعد الذكي"):
            if user_query.strip():
                with st.spinner("جاري التحليل وتوليد الحل البرمجي بواسطة الذكاء الاصطناعي..."):
                    response = ai_tutor.ask_tutor(user_query, context=track)
                    st.session_state["last_response"] = response
            else:
                st.warning("يرجى كتابة سؤال أو كود أولاً.")

    with btn_col2:
        if st.button("🧩 توليد تمرين ذكي متقدم"):
            with st.spinner("جاري إنشاء تمرين برمجي جديد مخصص لمستواك..."):
                gen_prompt = "اعطني تمرينًا برمجياً متقدمًا مع سيناريو واقعي، واطلب مني حله، ثم زودني بالحل النموذجي والشرح."
                response = ai_tutor.ask_tutor(gen_prompt, context=track)
                st.session_state["last_response"] = response

    # عرض النتيجة إن وجدت
    if "last_response" in st.session_state:
        st.markdown("### 💡 مخرجات المساعد الذكي:")
        st.markdown(st.session_state["last_response"])

    # ==========================================
    # وحدة أتمتة وتصنيف التذاكر
    # ==========================================
    st.divider()
    st.header("⚙️ نظام أتمتة وتصنيف التذاكر (Async Pipeline & Retries)")
    st.write("اختبار أتمتة معالجة التذاكر بالتوازي مع التحكم بالتزامن (Semaphore) وإعادة المحاولة (Tenacity Retry):")
    
    if st.button("⚙️ تشغيل أتمتة معالجة التذاكر (Test Pipeline)"):
        sample_tickets = [
            RawTicket(ticket_id=f"TICK-{i}", customer_id=f"CUST-{i}", issue_description="مشكلة في الاستجابة بطيئة للخدمة")
            for i in range(1, 8)
        ]
        with st.spinner("جاري معالجة 7 تذاكر بالتوازي وتطبيق Retry عند الأعطال..."):
            processed_tickets = asyncio.run(run_ticket_pipeline(sample_tickets))
            
            st.success(f"تمت معالجة {len(processed_tickets)} تذكرة بنجاح!")
            
            escalated = [t for t in processed_tickets if t.needs_escalation]
            m1, m2, m3 = st.columns(3)
            m1.metric("إجمالي التذاكر", len(processed_tickets))
            m2.metric("تذاكر مصعدة", len(escalated))
            m3.metric("تذاكر عادية", len(processed_tickets) - len(escalated))
            
            st.json([t.model_dump() for t in processed_tickets])

with col2:
    st.header("📄 حفظ وتصدير الشاشة")
    st.write("حفظ وتصدير الإجابة الحالية أو الدرس إلى ملفات وورد أو PDF:")
    
    content_to_export = st.session_state.get(
        "last_response",
        f"محتوى المسار التعليمي الحالي: {track}\nالموضوعات:\n" + "\n".join([f"- {t}" for t in COURSES_DATA[track]["topics"]])
    )
    
    # تصدير Word
    docx_file = export_to_docx(f"درس وحل - {track}", content_to_export)
    st.download_button(
        label="📥 تصدير كـ Word (.docx)",
        data=docx_file,
        file_name=f"{track}_lesson.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
    
    # تصدير PDF
    pdf_file = export_to_pdf(f"درس وحل - {track}", content_to_export)
    st.download_button(
        label="📥 تصدير كـ PDF (.pdf)",
        data=pdf_file,
        file_name=f"{track}_lesson.pdf",
        mime="application/pdf",
        use_container_width=True
    )
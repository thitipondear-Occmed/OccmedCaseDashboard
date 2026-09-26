import streamlit as st
import datetime

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Interesting Case Dashboard", page_icon="🩺", layout="wide")

# แทรกโค้ด CSS เพื่อปรับแต่ง UI ให้สวยงามเหมือน React (Tailwind)
st.markdown("""
<style>
    /* 1. เปลี่ยนสีพื้นหลังแอปให้เป็นสีเทาอ่อน (slate-50) */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* 2. ซ่อนเมนูขวาบนและ Footer ของ Streamlit ออก ให้ดูเป็น Web App มืออาชีพ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    /* 3. ปรับแต่งกล่อง Container (การ์ด) ให้มีขอบมน เงาสวยงาม และพื้นหลังสีขาว */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 1rem !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        padding: 0.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* 4. เพิ่มลูกเล่น (Hover) ตอนเอาเมาส์ชี้ที่การ์ด ให้การ์ดลอยขึ้นเล็กน้อย */
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04) !important;
        border-color: #cbd5e1 !important;
    }

    /* 5. ปรับแต่งปุ่มกดให้ดูนุ่มนวลขึ้น */
    div.stButton > button:first-child {
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    /* 6. ปรับแต่งข้อความแจ้งเตือน (Alerts/Info) ให้ขอบมน */
    [data-testid="stAlert"] {
        border-radius: 0.75rem !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# อัปเดตนิยาม EPA
EPA_DICTIONARY = {
    "EPA1": {"name": "EPA 1: ประเมินความพร้อมในการเข้าทำงาน หรือกลับเข้าทำงาน (Fit for work/Return to work)", "color": "#1e3a8a", "bg": "#dbeafe"},
    "EPA2": {"name": "EPA 2: การส่งเสริมสุขภาพพนักงาน", "color": "#065f46", "bg": "#d1fae5"},
    "EPA3": {"name": "EPA 3: การเฝ้าระวังทางการแพทย์", "color": "#5b21b6", "bg": "#ede9fe"},
    "EPA4": {"name": "EPA 4: การวินิจฉัยเนื่องจากการทำงาน", "color": "#92400e", "bg": "#fef3c7"},
    "EPA5": {"name": "EPA 5: การสอบสวนโรคจากการทำงาน", "color": "#9f1239", "bg": "#ffe4e6"}
}

# ข้อมูลจำลอง (ถ้าต่อจริงจะดึงจาก Google Sheets)
INITIAL_CASES = [
    {
        "id": "case-001", "timestamp": "9/21/2026, 11:23:10 AM", "submitter": "R2 พลวัต",
        "epas": ["EPA1"], "topic": "Fit for work in colour vision deficiency",
        "summary": "พนักงานมีภาวะตาบอดสี ตรวจพบจากการตรวจสุขภาพประจำปี จำเป็นต้องประเมินความพร้อมในการทำงาน...",
        "note": "", "link": "https://docs.google.com/presentation/d/1JtK...",
        "presentationPoints": "", "staffFeedback": "", "isNominated": False, "isApproved": False, "isPresented": False
    },
    {
        "id": "case-002", "timestamp": "9/18/2026, 11:10:45 PM", "submitter": "R1 เจตะพงศ์",
        "epas": ["EPA4", "EPA5"], "topic": "ผลการตรวจสาร trans, trans-Muconic acid ในปัสสาวะผิดปกติเป็นเนื่องจากการทำงานหรือไม่",
        "summary": "ผลตรวจติดตาม Biomarker พบค่า t,t-Muconic acid ในปัสสาวะสูงกว่าเกณฑ์...",
        "note": "ตอนที่ไปสอบสวน ดูน่าจะไม่ใช่จากงานคับ", "link": "https://drive.google.com/open?id=1z6iBl...",
        "presentationPoints": "ต้องการปรึกษาแนวทางการให้คำแนะนำพนักงานเบื้องต้นก่อนผลตรวจซ้ำจะออก", 
        "staffFeedback": "", "isNominated": True, "isApproved": False, "isPresented": False
    },
    {
        "id": "case-003", "timestamp": "8/27/2026, 11:21:22 PM", "submitter": "R3 ธิติพล",
        "epas": ["EPA4"], "topic": "Was this contact dermatitis patient WR or not?",
        "summary": "ผู้ป่วยมาด้วยอาการผื่นแดง คัน และลอกบริเวณมือทั้งสองข้าง ประวัติการทำงานมีการสัมผัสสารเคมี...",
        "note": "", "link": "https://docs.google.com/presentation/d/1yym...",
        "presentationPoints": "วิธีการ Approach เคสผิวหนังอักเสบในโรงงาน", 
        "staffFeedback": "", "isNominated": False, "isApproved": False, "isPresented": True
    },
    {
        "id": "case-004", "timestamp": "8/24/2026, 1:04:12 PM", "submitter": "R2 พลวัต",
        "epas": ["EPA1"], "topic": "Fit to drive after stroke private driver",
        "summary": "พนักงานขับรถส่วนบุคคลมีประวัติเจ็บป่วยด้วย Stroke ต้องการกลับมาทำงานเดิม...",
        "note": "", "link": "https://docs.google.com/presentation/d/1DqG...",
        "presentationPoints": "", 
        "staffFeedback": "", "isNominated": False, "isApproved": False, "isPresented": False
    }
]

# เริ่มต้น State ของระบบ (เก็บค่าต่างๆ ไว้ไม่ให้หายตอนหน้ารีเฟรช)
if "cases" not in st.session_state:
    st.session_state.cases = INITIAL_CASES
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "success_screen" not in st.session_state:
    st.session_state.success_screen = False

# ฟังก์ชันอัปเดตสถานะเคส
def update_case(case_id, key, value):
    for case in st.session_state.cases:
        if case["id"] == case_id:
            case[key] = value
            break

# หน้าต่าง Popup รายละเอียด (ใช้ฟีเจอร์ Dialog ของ Streamlit)
@st.dialog("รายละเอียด Case", width="large")
def case_detail_dialog(case):
    st.write(f"**Topic:** {case['topic']}")
    
    # แสดง Badge หมวดหมู่
    badges = " ".join([f"<span style='background-color:{EPA_DICTIONARY[e]['bg']}; color:{EPA_DICTIONARY[e]['color']}; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px; font-weight: bold;'>{e}</span>" for e in case['epas']])
    st.markdown(f"**หมวดหมู่:** {badges} &nbsp;&nbsp; | &nbsp;&nbsp; 👤 **ผู้ส่ง:** {case['submitter']} &nbsp;&nbsp; | &nbsp;&nbsp; 🕒 **เวลา:** {case['timestamp']}", unsafe_allow_html=True)
    
    st.divider()

    # แสดง Status
    if case["isPresented"]:
        st.info("🎤 เคสนี้ถูกนำไปใช้พรีเซนต์ใน Conference แล้ว")
    elif case["isApproved"]:
        st.success("✅ อาจารย์ (Staff) ได้อนุมัติเลือกเคสนี้สำหรับทำ Conference แล้ว")
    
    st.markdown(f"**✨ AI Summary (สรุปเนื้อหา):**\n> {case['summary']}")
    
    if case['note']:
        st.warning(f"**📝 หมายเหตุจากผู้ส่ง:** {case['note']}")

    # ส่วนของประเด็นนำเสนอ
    st.subheader("📌 ประเด็นสำคัญที่จะนำเสนอ")
    if st.session_state.user_role == "CHIEF" and not case["isPresented"] and not case["isApproved"]:
        new_points = st.text_area("ประเด็นการนำเสนอ (จำเป็นต้องกรอกก่อนเสนอเคส):", value=case.get('presentationPoints', ''))
        if new_points != case.get('presentationPoints', ''):
            update_case(case['id'], 'presentationPoints', new_points)
    else:
        st.write(case.get('presentationPoints', 'ยังไม่ได้ระบุประเด็น'))

    # ส่วนของข้อเสนอแนะจากอาจารย์
    if case["isApproved"] or case.get("staffFeedback"):
        st.subheader("💡 ข้อเสนอแนะ / ประเด็นเพิ่มเติมจากอาจารย์")
        if st.session_state.user_role == "STAFF" and not case["isPresented"]:
            new_feedback = st.text_area("พิมพ์ข้อเสนอแนะที่นี่...", value=case.get('staffFeedback', ''))
            if new_feedback != case.get('staffFeedback', ''):
                update_case(case['id'], 'staffFeedback', new_feedback)
        else:
            st.info(case.get('staffFeedback', 'ไม่มีข้อเสนอแนะเพิ่มเติม'))

    st.markdown(f"[🔗 คลิกลิงก์เปิดไฟล์แนบ ({case['link']})]({case['link']})")

    st.divider()

    # ปุ่ม Action ต่างๆ
    col1, col2 = st.columns([1, 1])
    
    with col2:
        if st.session_state.user_role == "CHIEF" and not case["isPresented"]:
            if case["isApproved"]:
                st.button("✅ อาจารย์อนุมัติเคสนี้แล้ว", disabled=True, use_container_width=True)
            else:
                is_disabled = not case["isNominated"] and not case.get("presentationPoints", "").strip()
                btn_text = "ยกเลิกการเสนอ" if case["isNominated"] else "👑 Chief: เสนอเคสนี้"
                if st.button(btn_text, disabled=is_disabled, use_container_width=True):
                    update_case(case['id'], 'isNominated', not case['isNominated'])
                    st.rerun()
                    
        elif st.session_state.user_role == "STAFF" and not case["isPresented"]:
            btn_text = "ยกเลิกการเลือก" if case["isApproved"] else "✅ Staff: อนุมัติเคสนี้"
            if st.button(btn_text, type="primary" if not case["isApproved"] else "secondary", use_container_width=True):
                update_case(case['id'], 'isApproved', not case['isApproved'])
                st.rerun()
                
    if st.session_state.user_role == "CHIEF":
        btn_presented_text = "ยกเลิก (พรีเซนต์แล้ว)" if case["isPresented"] else "🎤 ทำเครื่องหมายว่า พรีเซนต์ไปแล้ว"
        if st.button(btn_presented_text, use_container_width=True):
            update_case(case['id'], 'isPresented', not case['isPresented'])
            st.rerun()


# --- หน้าจอเข้าสู่ระบบ (เลือก Role) ---
if st.session_state.user_role is None:
    st.markdown("<h1 style='text-align: center; color: #1e293b;'>🩺 Interesting Case Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>กรุณาเลือกบทบาทในการเข้าใช้งานระบบ</p>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        st.info("### 👑 Chief Resident\nจัดการข้อมูลเคสทั้งหมด และพิจารณาเสนอเคสให้อาจารย์")
        if st.button("เข้าสู่ระบบในฐานะ Chief", use_container_width=True):
            st.session_state.user_role = "CHIEF"
            st.session_state.status_filter = "ACTIVE"
            st.rerun()
            
    with col3:
        st.success("### ✅ Staff (อาจารย์)\nดูเคสที่ถูกจัดเตรียมมา และอนุมัติใช้งานใน Conference")
        if st.button("เข้าสู่ระบบในฐานะ Staff", use_container_width=True):
            st.session_state.user_role = "STAFF"
            st.session_state.status_filter = "NOMINATED"
            st.rerun()

# --- หน้าจอทำรายการสำเร็จ ---
elif st.session_state.success_screen:
    approved_count = len([c for c in st.session_state.cases if c["isApproved"] and not c["isPresented"]])
    
    st.markdown("<h1 style='text-align: center; color: #059669; font-size: 3rem;'>✅ ดำเนินการเสร็จสิ้น!</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'>ระบบได้รับทราบการยืนยันการเลือกเคสจำนวน <b>{approved_count}</b> เคส สำหรับ Conference เรียบร้อยแล้ว</p>", unsafe_allow_html=True)
    
    st.info("💡 **ขั้นตอนต่อไป:** คุณสามารถปิดหน้านี้ และแจ้งให้ Chief Resident ทราบเพื่อดำเนินการมอบหมายผู้พรีเซนต์ได้เลยครับ")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ย้อนกลับไปแก้ไขการเลือกเคส", use_container_width=True):
            st.session_state.success_screen = False
            st.rerun()

# --- หน้าจอ Dashboard หลัก ---
else:
    # Header
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("🩺 Interesting Case Dashboard")
        st.caption(f"กำลังใช้งานในโหมด: **{st.session_state.user_role}**")
    with col_logout:
        if st.button("🚪 เปลี่ยนบทบาท"):
            st.session_state.user_role = None
            st.rerun()

    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("🔍 ตัวกรองข้อมูล")
        search_query = st.text_input("ค้นหา Topic, ชื่อผู้ส่ง...")
        
        st.subheader("สถานะ Workflow")
        
        # ตั้งค่า Filter ตาม Role
        if "status_filter" not in st.session_state:
            st.session_state.status_filter = "ACTIVE" if st.session_state.user_role == "CHIEF" else "NOMINATED"
            
        status_options = {
            "ALL_STATUS": "🗂️ รายการเคสทั้งหมด",
            "ACTIVE": "📥 รอพิจารณา (ซ่อนที่ทำแล้ว)",
            "NOMINATED": "👑 เสนอโดย Chief (รออาจารย์เลือก)",
            "APPROVED": "✅ อาจารย์อนุมัติแล้ว",
            "PRESENTED": "🎤 พรีเซนต์ไปแล้ว"
        }
        
        # สร้าง Radio button สำหรับเลือกสถานะ
        selected_status_name = st.radio("เลือกดูสถานะ:", list(status_options.values()), 
                                        index=list(status_options.keys()).index(st.session_state.status_filter))
        # อัปเดตกลับไปเป็น Key
        for k, v in status_options.items():
            if v == selected_status_name:
                st.session_state.status_filter = k
                break

        st.subheader("หมวดหมู่ EPA")
        epa_options = ["ดูทั้งหมด"] + list(EPA_DICTIONARY.keys())
        selected_epa = st.selectbox("เลือก EPA:", epa_options)
        
        st.info("💡 กดปุ่มที่การ์ดเพื่อดูรายละเอียดเพิ่มเติมและดำเนินการ (เสนอ/อนุมัติ/พรีเซนต์)")

    # การกรองและเรียงลำดับข้อมูล
    filtered_cases = []
    for c in st.session_state.cases:
        # 1. กรองสถานะ
        match_status = True
        status_f = st.session_state.status_filter
        if status_f == "NOMINATED": match_status = c["isNominated"] and not c["isPresented"]
        if status_f == "APPROVED": match_status = c["isApproved"] and not c["isPresented"]
        if status_f == "PRESENTED": match_status = c["isPresented"]
        if status_f == "ACTIVE": match_status = not c["isPresented"]
        
        # 2. กรอง EPA
        match_epa = (selected_epa == "ดูทั้งหมด") or (selected_epa in c["epas"])
        
        # 3. ค้นหา
        match_search = search_query.lower() in c["topic"].lower() or search_query.lower() in c["submitter"].lower()
        
        if match_status and match_epa and match_search:
            filtered_cases.append(c)

    # เรียงลำดับ (Sort)
    def get_sort_key(case):
        # แปลงเวลาเป็น Date (ใช้วิธีลัดสำหรับ Mockup data)
        try:
            date_val = datetime.datetime.strptime(case["timestamp"].split(',')[0], "%m/%d/%Y").timestamp()
        except:
            date_val = 0
            
        priority = 0
        if st.session_state.user_role == "STAFF":
            # ให้เคสที่ Chief เสนอขึ้นบนสุด
            priority = 1 if (case["isNominated"] and not case["isPresented"]) else 0
            
        return (priority, date_val)
        
    filtered_cases.sort(key=get_sort_key, reverse=True)

    # แสดงผลจำนวนเคส
    st.write(f"พบข้อมูลทั้งหมด **{len(filtered_cases)}** รายการ")

    # แสดง Cards (ใช้ Columns)
    if len(filtered_cases) == 0:
        st.warning("ไม่พบเคสที่ตรงกับเงื่อนไขการค้นหา")
    else:
        # แบ่งแสดงเป็นแถวละ 2 กล่อง
        for i in range(0, len(filtered_cases), 2):
            cols = st.columns(2)
            
            # กล่องที่ 1
            case1 = filtered_cases[i]
            with cols[0]:
                with st.container(border=True):
                    # Status Badge
                    if case1["isPresented"]: st.caption("🎤 พรีเซนต์แล้ว")
                    elif case1["isApproved"]: st.caption("✅ อาจารย์เลือกแล้ว")
                    elif case1["isNominated"]: st.caption("👑 Chief เสนอเคสนี้")
                    
                    st.markdown(f"#### {case1['topic']}")
                    st.write(f"**โดย:** {case1['submitter']} | 🕒 {case1['timestamp'].split(',')[0]}")
                    
                    if st.button("ดูรายละเอียด & จัดการ", key=f"btn_{case1['id']}", use_container_width=True):
                        case_detail_dialog(case1)

            # กล่องที่ 2 (ถ้ามี)
            if i + 1 < len(filtered_cases):
                case2 = filtered_cases[i+1]
                with cols[1]:
                    with st.container(border=True):
                        if case2["isPresented"]: st.caption("🎤 พรีเซนต์แล้ว")
                        elif case2["isApproved"]: st.caption("✅ อาจารย์เลือกแล้ว")
                        elif case2["isNominated"]: st.caption("👑 Chief เสนอเคสนี้")
                        
                        st.markdown(f"#### {case2['topic']}")
                        st.write(f"**โดย:** {case2['submitter']} | 🕒 {case2['timestamp'].split(',')[0]}")
                        
                        if st.button("ดูรายละเอียด & จัดการ", key=f"btn_{case2['id']}", use_container_width=True):
                            case_detail_dialog(case2)
    
    # แถบด้านล่างสำหรับ Staff (กดยืนยัน)
    st.write("")
    st.write("")
    st.write("")
    if st.session_state.user_role == "STAFF":
        approved_count = len([c for c in st.session_state.cases if c["isApproved"] and not c["isPresented"]])
        
        st.markdown("""<hr style="height:2px;border:none;color:#10b981;background-color:#10b981;" />""", unsafe_allow_html=True)
        col_text, col_btn = st.columns([3, 1])
        with col_text:
            st.markdown(f"### ✅ สรุปการเลือกเคส: คุณเลือกเคสรอทำ Conference จำนวน **{approved_count}** เคส")
        with col_btn:
            if st.button("กดยืนยัน และแจ้ง Chief", type="primary", disabled=(approved_count==0), use_container_width=True):
                st.session_state.success_screen = True
                st.rerun()

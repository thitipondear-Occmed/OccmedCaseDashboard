import streamlit as st
import pandas as pd

# ==========================================
# 1. การตั้งค่าหน้าเว็บ (Page Config & CSS)
# ==========================================
st.set_page_config(page_title="Interesting Case Dashboard", page_icon="🩺", layout="wide")

# ซ่อนเมนู Streamlit และเพิ่ม CSS ให้พื้นหลังดูเป็นแอปพลิเคชัน
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* เปลี่ยนสีพื้นหลังของแอปให้เป็นสีเทาอ่อนแบบ Tailwind (bg-slate-50) */
    .stApp {
        background-color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. จำลองฐานข้อมูล (Session State Database)
# ==========================================
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.role = 'chief' # เริ่มต้นที่ Chief
    st.session_state.selected_case = None
    st.session_state.show_success_screen = False
    
    # ข้อมูลจำลอง 4 เคส
    initial_cases = [
        {
            "Case ID": "C1",
            "Date": "9/21/2026",
            "Author": "R2 พลวัต",
            "Topic": "Fit for work in colour vision deficiency",
            "EPAs": ["EPA 1"],
            "EPA_Detail": "ประเมินความพร้อมในการเข้าทำงาน หรือกลับเข้าทำงาน (Fit for work or Return to work)",
            "Link": "https://docs.google.com/presentation/d/1JtKRCcPHNOwsdhk-hsyG1fwr5FFhW-teFCqx-zAZ_VM/edit?usp=sharing",
            "Note": "-",
            "Status": "New",
            "KeyPoints": "",
            "StaffFeedback": ""
        },
        {
            "Case ID": "C2",
            "Date": "9/18/2026",
            "Author": "R1 เจตะพงศ์",
            "Topic": "ผลการตรวจสาร trans, trans-Muconic acid ในปัสสาวะผิดปกติเป็นเนื่องจากการทำงานหรือไม่",
            "EPAs": ["EPA 4", "EPA 5"],
            "EPA_Detail": "การวินิจฉัยเนื่องจากการทำงาน และ การสอบสวนโรคจากการทำงานในสถานประกอบกิจการ",
            "Link": "https://drive.google.com/open?id=1z6iBlU0zbNahp2Jtcq8FokGvi18ju60A",
            "Note": "ตอนที่ไปสอบสวน ดูน่าจะไม่ใช่จากงานคับ มีนัดตรวจซ้ำไว้ แต่ไม่แน่ใจว่าผลเป็นไงบ้างคับ",
            "Status": "Nominated", # จำลองว่า Chief เลือกไว้แล้ว 1 เคส
            "KeyPoints": "สงสัยเรื่องผล Lab ว่าสัมพันธ์กับการสัมผัสในที่ทำงานจริงหรือไม่",
            "StaffFeedback": ""
        },
        {
            "Case ID": "C3",
            "Date": "8/27/2026",
            "Author": "R3 ธิติพล",
            "Topic": "Was this contact dermatitis patient WR or not?",
            "EPAs": ["EPA 4"],
            "EPA_Detail": "การวินิจฉัยเนื่องจากการทำงาน (โดยที่ไม่ได้ลงพื้นที่สอบสวน)",
            "Link": "https://docs.google.com/presentation/d/1yymZmB360ijT9awvnVy_yimrolH461kgZJNGyA_mpVo/edit?usp=sharing",
            "Note": "-",
            "Status": "Presented", # จำลองว่าพรีเซนต์ไปแล้ว
            "KeyPoints": "การวินิจฉัยแยกโรค",
            "StaffFeedback": ""
        },
        {
            "Case ID": "C4",
            "Date": "8/24/2026",
            "Author": "R2 พลวัต",
            "Topic": "Fit to drive after stroke private driver",
            "EPAs": ["EPA 1"],
            "EPA_Detail": "ประเมินความพร้อมในการเข้าทำงาน หรือกลับเข้าทำงาน (Fit for work or Return to work)",
            "Link": "https://docs.google.com/presentation/d/1DqGkVO-4muxD8zT0RFowPLRQ9ZKQeGAnL5lpr6q9x04/edit?usp=drivesdk",
            "Note": "-",
            "Status": "New",
            "KeyPoints": "",
            "StaffFeedback": ""
        }
    ]
    st.session_state.cases_db = initial_cases

# ==========================================
# 3. โครงสร้างส่วนหัว (Header & Role Toggle)
# ==========================================
col_title, col_role = st.columns([3, 1])
with col_title:
    st.title("🩺 Interesting Case Dashboard")
    if st.session_state.role == 'chief':
        st.caption("กำลังใช้งานในโหมด: **CHIEF RESIDENT**")
    else:
        st.caption("กำลังใช้งานในโหมด: **STAFF (อาจารย์)**")
        
with col_role:
    st.write("") # spacer
    if st.button("🔄 เปลี่ยนบทบาท", use_container_width=True):
        st.session_state.role = 'staff' if st.session_state.role == 'chief' else 'chief'
        st.session_state.selected_case = None # Reset view
        st.rerun()

st.divider()

# ==========================================
# 4. หน้าจอเสร็จสิ้น (Success Screen)
# ==========================================
if st.session_state.show_success_screen:
    st.success("🎉 ดำเนินการเสร็จสิ้น! บันทึกและแจ้งเตือน Chief เรียบร้อยแล้ว")
    st.markdown("### อาจารย์ได้ทำการเลือกเคสสำหรับ Conference เรียบร้อยแล้ว")
    st.write("ระบบได้ทำการอัปเดตสถานะและเปิดช่องให้ Chief มองเห็นข้อเสนอแนะของอาจารย์แล้วครับ")
    st.write("")
    if st.button("⬅️ กลับไปหน้า Dashboard"):
        st.session_state.show_success_screen = False
        st.rerun()
        
# ==========================================
# 5. หน้าต่างรายละเอียดเคส (Detail View)
# ==========================================
elif st.session_state.selected_case is not None:
    if st.button("⬅️ ย้อนกลับไปหน้ารายการเคส"):
        st.session_state.selected_case = None
        st.rerun()
        
    case_id = st.session_state.selected_case
    # ดึงข้อมูลเคสปัจจุบันมาแสดง
    case = next(item for item in st.session_state.cases_db if item["Case ID"] == case_id)
    
    st.subheader(case["Topic"])
    st.markdown(f"**ผู้นำเสนอ:** {case['Author']} | **วันที่ส่ง:** {case['Date']}")
    st.markdown(f"**หมวดหมู่ EPA:** {', '.join(case['EPAs'])}")
    st.info(f"**🎯 Learning Objective:** {case['EPA_Detail']}")
    if case["Note"] != "-":
        st.warning(f"**📝 หมายเหตุจากผู้ส่ง:** {case['Note']}")
    st.markdown(f"**🔗 เอกสารแนบ:** [คลิกเปิดลิงก์สไลด์/ข้อมูล]({case['Link']})")
    
    st.divider()
    
    # ------------------------------------
    # มุมมองและเครื่องมือสำหรับ Chief Resident
    # ------------------------------------
    if st.session_state.role == 'chief':
        if case['Status'] == 'New':
            st.markdown("### 👑 เครื่องมือสำหรับ Chief")
            key_pts = st.text_area("ประเด็นสำคัญที่จะนำเสนอ (กรอกเพื่อเสนอเคส)", value=case['KeyPoints'])
            if st.button("👑 เสนอเคสนี้ให้อาจารย์ (Nominate)", type="primary", disabled=(len(key_pts) == 0)):
                case['Status'] = 'Nominated'
                case['KeyPoints'] = key_pts
                st.session_state.selected_case = None
                st.rerun()
                
        elif case['Status'] == 'Nominated':
            st.info("⏳ เสนอเคสนี้ไปแล้ว รออาจารย์พิจารณา...")
            st.text_area("ประเด็นสำคัญที่จะนำเสนอ", value=case['KeyPoints'], disabled=True)
            
        elif case['Status'] == 'Approved':
            st.success("✅ อาจารย์ (Staff) ได้อนุมัติเลือกเคสนี้สำหรับทำ Conference แล้ว!")
            if case['StaffFeedback']:
                st.markdown(f"**💬 ข้อเสนอแนะจากอาจารย์:**\n\n> {case['StaffFeedback']}")
            
            st.markdown("---")
            if st.button("🎤 ทำเครื่องหมายว่า พรีเซนต์ไปแล้ว", type="primary"):
                case['Status'] = 'Presented'
                st.session_state.selected_case = None
                st.rerun()
                
        elif case['Status'] == 'Presented':
            st.markdown("🎤 **เคสนี้ถูกพรีเซนต์เรียบร้อยแล้ว**")
            
    # ------------------------------------
    # มุมมองและเครื่องมือสำหรับ Staff (อาจารย์)
    # ------------------------------------
    else:
        st.markdown("### 📋 ข้อมูลประกอบการพิจารณา")
        st.text_area("ประเด็นสำคัญที่ Chief เสนอ:", value=case['KeyPoints'], disabled=True)
        
        if case['Status'] == 'Nominated':
            if st.button("✅ อนุมัติเคสนี้สำหรับ Conference", type="primary"):
                case['Status'] = 'Approved'
                st.rerun()
                
        elif case['Status'] == 'Approved':
            st.success("✅ คุณเลือกเคสนี้แล้ว (รอให้ Chief นำไปพรีเซนต์)")
            feedback = st.text_area("💬 เพิ่มข้อเสนอแนะให้ Chief (บันทึกอัตโนมัติ):", value=case['StaffFeedback'])
            # บันทึกข้อเสนอแนะเมื่อมีการพิมพ์
            if feedback != case['StaffFeedback']:
                case['StaffFeedback'] = feedback

# ==========================================
# 6. หน้าจอหลัก (Dashboard List View)
# ==========================================
else:
    col_sidebar, col_main = st.columns([1, 3])
    
    # ------------------------------------
    # เมนูตัวกรองด้านซ้าย (Sidebar)
    # ------------------------------------
    with col_sidebar:
        st.markdown("**สถานะ Workflow**")
        
        # ตั้งค่า Filter พื้นฐานตามบทบาท
        default_status = 'All'
        if st.session_state.role == 'staff':
            # โหมด Staff ให้ตั้งค่าเริ่มต้นเป็น Nominated
            st.info("💡 แสดงเฉพาะ 'เคสที่ Chief เสนอมา' หากต้องการดูเคสทั้งหมดให้เลือกเมนูด้านล่าง")
            default_status = 'Nominated'
            
        status_filter = st.radio(
            "เลือกดูสถานะ:",
            ['All', 'New', 'Nominated', 'Approved', 'Presented'],
            format_func=lambda x: {
                'All': '🗂️ รายการเคสทั้งหมด',
                'New': '🆕 รอพิจารณา',
                'Nominated': '👑 เสนอโดย Chief',
                'Approved': '✅ อาจารย์อนุมัติแล้ว',
                'Presented': '🎤 พรีเซนต์ไปแล้ว'
            }[x],
            index=['All', 'New', 'Nominated', 'Approved', 'Presented'].index(default_status)
        )
        
        st.markdown("**หมวดหมู่ EPA**")
        epa_filter = st.selectbox("เลือก EPA:", ["ทั้งหมด", "EPA 1", "EPA 2", "EPA 3", "EPA 4", "EPA 5"])

    # ------------------------------------
    # พื้นที่แสดงการ์ดเคส (Main View)
    # ------------------------------------
    with col_main:
        # 1. กรองข้อมูลตามที่เลือก
        filtered_cases = [c for c in st.session_state.cases_db]
        
        if status_filter != 'All':
            filtered_cases = [c for c in filtered_cases if c['Status'] == status_filter]
            
        if epa_filter != "ทั้งหมด":
            filtered_cases = [c for c in filtered_cases if epa_filter in c['EPAs']]
            
        # 2. เรียงลำดับข้อมูล
        if st.session_state.role == 'staff':
            # ของอาจารย์ เอาที่อนุมัติแล้วหรือเพิ่งเสนอขึ้นบน
            filtered_cases.sort(key=lambda x: 0 if x['Status'] in ['Nominated', 'Approved'] else 1)
        else:
            # ของ Chief เอาใหม่ล่าสุดขึ้นบน (จำลองจากรหัส C4, C3, C2...)
            filtered_cases.reverse()
            
        st.markdown(f"**พบข้อมูลทั้งหมด {len(filtered_cases)} รายการ**")
        
        # 3. วาดการ์ด HTML ทับลงไป
        for case in filtered_cases:
            # กำหนดสีขอบซ้าย (Border Left) ตามสถานะ
            border_color = "#3b82f6" # สีฟ้า (Default)
            badge_html = ""
            
            if case['Status'] == 'Nominated':
                border_color = "#eab308" # สีเหลือง
                badge_html = '<span style="background:#fef08a; color:#854d0e; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">👑 Chief เสนอ</span>'
            elif case['Status'] == 'Approved':
                border_color = "#22c55e" # สีเขียว
                badge_html = '<span style="background:#bbf7d0; color:#166534; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">✅ อาจารย์เลือกแล้ว</span>'
            elif case['Status'] == 'Presented':
                border_color = "#9ca3af" # สีเทา
                badge_html = '<span style="background:#e5e7eb; color:#374151; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">🎤 พรีเซนต์ไปแล้ว</span>'
            else:
                badge_html = '<span style="background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">🆕 เคสใหม่</span>'

            # HTML & CSS สำหรับการ์ด
            html_card = f"""
            <div style="
                background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); 
                border-left: 6px solid {border_color};
                margin-bottom: 10px;
                border: 1px solid #f3f4f6;
            ">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    {badge_html}
                </div>
                <h3 style="margin: 0 0 10px 0; color: #1f2937; font-size: 18px; font-weight: 600; line-height: 1.4;">
                    {case['Topic']}
                </h3>
                <p style="margin: 0; color: #6b7280; font-size: 14px;">
                    <strong>โดย:</strong> {case['Author']} | 🕒 {case['Date']}
                </p>
            </div>
            """
            # สั่งให้ Streamlit เรนเดอร์ HTML แบบเต็มความกว้าง
            st.markdown(html_card, unsafe_allow_html=True)
            
            # วางปุ่มกดของ Streamlit ไว้ใต้การ์ด
            if st.button(f"🔍 ดูรายละเอียด & จัดการ ({case['Case ID']})", key=f"btn_{case['Case ID']}", use_container_width=True):
                st.session_state.selected_case = case['Case ID']
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True) # เว้นระยะห่างให้สวยงาม

    # ------------------------------------
    # แถบยืนยันด้านล่างสุด (เฉพาะ Staff)
    # ------------------------------------
    if st.session_state.role == 'staff':
        approved_count = len([c for c in st.session_state.cases_db if c['Status'] == 'Approved'])
        st.divider()
        st.markdown(f"### 📊 สรุปการเลือกเคสสำหรับ Conference: เลือกไปแล้ว **{approved_count}** เคส")
        if approved_count > 0:
            if st.button("✅ ยืนยันการเลือกเคส และแจ้งเตือน Chief", type="primary", use_container_width=True):
                st.session_state.show_success_screen = True
                st.rerun()

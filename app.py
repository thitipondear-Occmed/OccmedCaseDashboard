import streamlit as st
import pandas as pd

# ----------------------------------------
# 1. ตั้งค่าหน้าเพจและ CSS (UI ให้ออกมาสวยงาม)
# ----------------------------------------
st.set_page_config(page_title="Interesting Case Dashboard", page_icon="🩺", layout="wide")

st.markdown("""
    <style>
    /* ซ่อนเมนูหลักของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ปรับปุ่มให้ดูสวยและขอบมนขึ้น */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------------------
# 2. ข้อมูลจำลองและคำจำกัดความ (Mock Data)
# ----------------------------------------
epa_dict = {
    "EPA1": {"name": "EPA 1: ประเมินความพร้อมในการเข้าทำงาน หรือกลับเข้าทำงาน (Fit for work/Return to work)", "obj": "เพื่อให้สามารถประเมินและตัดสินใจเรื่องความพร้อมในการเข้า/กลับเข้าทำงานได้อย่างถูกต้องและปลอดภัย"},
    "EPA2": {"name": "EPA 2: การส่งเสริมสุขภาพพนักงาน", "obj": "เพื่อให้สามารถวางแผนและดำเนินการส่งเสริมสุขภาพพนักงานในสถานประกอบการได้อย่างเหมาะสม"},
    "EPA3": {"name": "EPA 3: การเฝ้าระวังทางการแพทย์", "obj": "เพื่อให้สามารถออกแบบและดำเนินการเฝ้าระวังทางสุขภาพให้กับกลุ่มเสี่ยงได้อย่างถูกต้อง"},
    "EPA4": {"name": "EPA 4: การวินิจฉัยเนื่องจากการทำงาน (ไม่ได้ลงพื้นที่)", "obj": "เพื่อให้สามารถประเมินและวินิจฉัยโรคว่าเกี่ยวเนื่องจากการทำงานหรือไม่"},
    "EPA5": {"name": "EPA 5: การสอบสวนโรคจากการทำงานในสถานประกอบกิจการ", "obj": "เพื่อให้สามารถวางแผนและลงพื้นที่สอบสวนโรคในสถานประกอบกิจการได้"}
}

if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame([
        {"Case ID": "C1", "Date": "9/21/2026", "Author": "R2 พลวัต", "EPA": "EPA1", "Topic": "Fit for work in colour vision deficiency", "Note": "", "Link": "https://docs.google.com/presentation/...", "Status": "New", "Key_Points": "", "Staff_Feedback": ""},
        {"Case ID": "C2", "Date": "9/18/2026", "Author": "R1 เจตะพงศ์", "EPA": "EPA4, EPA5", "Topic": "ผลการตรวจสาร trans, trans-Muconic acid ในปัสสาวะผิดปกติเป็นเนื่องจากการทำงานหรือไม่", "Note": "ตอนที่ไปสอบสวน ดูน่าจะไม่ใช่จากงานคับ...", "Link": "https://drive.google.com/open?id=...", "Status": "Nominated", "Key_Points": "ปรึกษาเรื่องการแปลผล biological monitoring", "Staff_Feedback": ""},
        {"Case ID": "C3", "Date": "8/27/2026", "Author": "R3 ธิติพล", "EPA": "EPA4", "Topic": "Was this contact dermatitis patient WR or not?", "Note": "", "Link": "https://docs.google.com/presentation/...", "Status": "Presented", "Key_Points": "เกณฑ์การวินิจฉัย Occupational Contact Dermatitis", "Staff_Feedback": "เตรียมรูปผื่นและ patch test มาให้ชัดเจน"},
        {"Case ID": "C4", "Date": "8/24/2026", "Author": "R2 พลวัต", "EPA": "EPA1", "Topic": "Fit to drive after stroke private driver", "Note": "", "Link": "https://docs.google.com/presentation/...", "Status": "New", "Key_Points": "", "Staff_Feedback": ""}
    ])

# ----------------------------------------
# 3. สถานะหน้าจอ (Session State)
# ----------------------------------------
if 'role' not in st.session_state:
    st.session_state.role = 'Chief Resident'
if 'selected_case' not in st.session_state:
    st.session_state.selected_case = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'list' 

# ----------------------------------------
# 4. เมนูด้านข้าง (Sidebar - เฉพาะตัวกรอง)
# ----------------------------------------
with st.sidebar:
    st.title("🩺 ตัวกรองข้อมูล")
    
    st.subheader("สถานะ Workflow")
    if st.session_state.role == 'Staff (อาจารย์)':
        status_filter = st.radio("เลือกดูรายการ:", ["👑 เสนอโดย Chief (รอพิจารณา)", "🗂️ รายการเคสทั้งหมด", "✅ อาจารย์อนุมัติแล้ว", "🎤 พรีเซนต์ไปแล้ว"], index=0)
        st.info("💡 โหมดอาจารย์: แสดงเฉพาะเคสที่ Chief เสนอมาเป็นค่าเริ่มต้น")
    else:
        status_filter = st.radio("เลือกดูรายการ:", ["🗂️ รายการเคสทั้งหมด", "👑 เสนอโดย Chief", "✅ อาจารย์อนุมัติแล้ว", "🎤 พรีเซนต์ไปแล้ว"], index=0)
        
    st.markdown("---")
    epa_filter = st.selectbox("กรองตามหมวดหมู่ EPA:", ["ดูทั้งหมด", "EPA1", "EPA2", "EPA3", "EPA4", "EPA5"])

# ----------------------------------------
# ส่วนหัวของแอป (Header & Role Selector) - อยู่ด้านบนเสมอ
# ----------------------------------------
col_header, col_role = st.columns([3, 1])
with col_header:
    if st.session_state.view_mode == 'list':
        st.header("🗂️ Interesting Case Dashboard")
        st.caption(f"กำลังใช้งานในโหมด: **{st.session_state.role}**")
with col_role:
    new_role = st.selectbox("👤 เข้าใช้งานในฐานะ:", ["Chief Resident", "Staff (อาจารย์)"], index=0 if st.session_state.role == 'Chief Resident' else 1)
    if new_role != st.session_state.role:
        st.session_state.role = new_role
        st.session_state.selected_case = None
        st.session_state.view_mode = 'list'
        st.rerun()

st.markdown("---")

# ----------------------------------------
# 5. ฟังก์ชันแสดงรายการเคส (List View - แบบ 2 คอลัมน์)
# ----------------------------------------
def show_list_view():
    df = st.session_state.cases
    
    # การกรองข้อมูล
    if status_filter == "👑 เสนอโดย Chief" or status_filter == "👑 เสนอโดย Chief (รอพิจารณา)":
        df = df[df['Status'] == 'Nominated']
    elif status_filter == "✅ อาจารย์อนุมัติแล้ว":
        df = df[df['Status'] == 'Approved']
    elif status_filter == "🎤 พรีเซนต์ไปแล้ว":
        df = df[df['Status'] == 'Presented']
        
    if epa_filter != "ดูทั้งหมด":
        df = df[df['EPA'].str.contains(epa_filter)]
        
    if st.session_state.role == 'Chief Resident':
        df = df.sort_values(by="Date", ascending=False)
        
    st.write(f"พบข้อมูลทั้งหมด **{len(df)}** รายการ")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # แบ่งเลย์เอาต์เป็น 2 คอลัมน์
    cols = st.columns(2)
    
    # วนลูปสร้างการ์ด HTML ลงในแต่ละคอลัมน์
    for index, (df_idx, row) in enumerate(df.iterrows()):
        case_id = row['Case ID']
        border_color = "#3b82f6" 
        badge_html = ""
        
        if row['Status'] == 'Nominated':
            border_color = "#eab308" 
            badge_html = '<span style="background:#fef08a; color:#854d0e; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:bold;">👑 Chief เสนอเคสนี้</span>'
        elif row['Status'] == 'Approved':
            border_color = "#22c55e" 
            badge_html = '<span style="background:#bbf7d0; color:#166534; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:bold;">✅ อาจารย์เลือกแล้ว</span>'
        elif row['Status'] == 'Presented':
            border_color = "#9ca3af" 
            badge_html = '<span style="background:#e5e7eb; color:#374151; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:bold;">🎤 พรีเซนต์ไปแล้ว</span>'

        html_card = f"""
        <div style="
            background-color: white; 
            padding: 20px; 
            border-radius: 12px; 
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); 
            border-left: 6px solid {border_color};
            margin-bottom: 15px;
            border: 1px solid #f3f4f6;
            min-height: 140px;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                {badge_html}
            </div>
            <h3 style="margin: 0 0 10px 0; color: #1f2937; font-size: 16px; font-weight: 600; line-height: 1.4;">
                {row['Topic']}
            </h3>
            <p style="margin: 0; color: #6b7280; font-size: 13px;">
                <strong>โดย:</strong> {row['Author']} | 🕒 {row['Date']}
            </p>
        </div>
        """
        
        # ใส่การ์ดลงในคอลัมน์ซ้ายหรือขวา (สลับกันไป)
        with cols[index % 2]:
            st.markdown(html_card, unsafe_allow_html=True)
            if st.button("🔍 ดูรายละเอียด & จัดการ", key=f"btn_{case_id}", use_container_width=True):
                st.session_state.selected_case = case_id
                st.session_state.view_mode = 'detail'
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------
# 6. ฟังก์ชันแสดงรายละเอียดเคส (Detail View)
# ----------------------------------------
def show_detail_view():
    if st.button("← ย้อนกลับไปหน้ารวม", type="secondary"):
        st.session_state.view_mode = 'list'
        st.session_state.selected_case = None
        st.rerun()
        
    df = st.session_state.cases
    case_idx = df.index[df['Case ID'] == st.session_state.selected_case].tolist()[0]
    case = df.iloc[case_idx]
    
    st.markdown("---")
    
    if case['Status'] == 'Nominated':
        st.warning("👑 **สถานะ:** เคสนี้ถูกเสนอโดย Chief Resident (รออาจารย์พิจารณา)")
    elif case['Status'] == 'Approved':
        st.success("✅ **สถานะ:** อาจารย์ (Staff) อนุมัติเลือกเคสนี้สำหรับ Conference แล้ว")
    elif case['Status'] == 'Presented':
        st.info("🎤 **สถานะ:** เคสนี้ถูกนำไปพรีเซนต์เรียบร้อยแล้ว")
        
    st.title(case['Topic'])
    st.write(f"**ผู้นำเสนอ:** {case['Author']} | **วันที่ส่ง:** {case['Date']}")
    
    if case['Note']:
        st.info(f"**📝 หมายเหตุจากผู้ส่ง:** {case['Note']}")
        
    st.markdown(f"**🔗 [คลิกที่นี่เพื่อเปิดดูเอกสารแนบ (สไลด์/ข้อมูล)]({case['Link']})**")
    
    st.markdown("### 🎯 วัตถุประสงค์การเรียนรู้ (Learning Objective)")
    epa_list = [e.strip() for e in case['EPA'].split(',')]
    for epa in epa_list:
        if epa in epa_dict:
            st.markdown(f"- **{epa_dict[epa]['name']}**: {epa_dict[epa]['obj']}")

    st.markdown("---")
    
    if st.session_state.role == 'Chief Resident':
        st.subheader("🛠️ การจัดการ (สำหรับ Chief)")
        
        if case['Status'] == 'New':
            input_keypoints = st.text_area("ประเด็นสำคัญที่จะนำเสนอ (บังคับกรอกก่อนเสนอเคส):", value=case['Key_Points'])
            if st.button("👑 เสนอเคสนี้ให้อาจารย์", type="primary", disabled=not input_keypoints.strip()):
                st.session_state.cases.at[case_idx, 'Status'] = 'Nominated'
                st.session_state.cases.at[case_idx, 'Key_Points'] = input_keypoints
                st.session_state.view_mode = 'list'
                st.rerun()
        elif case['Status'] == 'Approved':
            st.write(f"**ประเด็นที่เสนอไว้:** {case['Key_Points']}")
            if case['Staff_Feedback']:
                st.success(f"**💬 ข้อเสนอแนะจากอาจารย์:** {case['Staff_Feedback']}")
            if st.button("🎤 ทำเครื่องหมายว่า พรีเซนต์ไปแล้ว"):
                st.session_state.cases.at[case_idx, 'Status'] = 'Presented'
                st.session_state.view_mode = 'list'
                st.rerun()
        else:
            st.write(f"**ประเด็นที่เสนอไว้:** {case['Key_Points']}")
            st.info("เคสนี้ทำรายการไปแล้ว หรือรออาจารย์อนุมัติ")

    elif st.session_state.role == 'Staff (อาจารย์)':
        st.subheader("🛠️ การพิจารณา (สำหรับอาจารย์)")
        
        if case['Key_Points']:
            st.warning(f"**📌 ประเด็นสำคัญจาก Chief:** {case['Key_Points']}")
            
        if case['Status'] == 'Nominated':
            feedback = st.text_area("ข้อเสนอแนะเพิ่มเติม (ถ้ามี):")
            if st.button("✅ อนุมัติเคสนี้", type="primary"):
                st.session_state.cases.at[case_idx, 'Status'] = 'Approved'
                st.session_state.cases.at[case_idx, 'Staff_Feedback'] = feedback
                st.session_state.view_mode = 'success'
                st.rerun()
        elif case['Status'] == 'Approved':
            st.success(f"**💬 ข้อเสนอแนะที่คุณพิมพ์ไว้:** {case['Staff_Feedback']}")
            st.info("คุณอนุมัติเคสนี้ไปแล้ว")
        else:
            st.info("เคสนี้ยังไม่ถูกเสนอ หรือพรีเซนต์ไปแล้ว")

# ----------------------------------------
# 7. หน้าจอเสร็จสิ้น (Success Screen)
# ----------------------------------------
def show_success_view():
    st.balloons()
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.success("🎉 **ดำเนินการเสร็จสิ้น!**")
        st.write("ระบบได้บันทึกการอนุมัติเคส และข้อเสนอแนะของคุณเรียบร้อยแล้ว")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← กลับไปหน้ารายการเคส", use_container_width=True):
            st.session_state.view_mode = 'list'
            st.session_state.selected_case = None
            st.rerun()

# ----------------------------------------
# ควบคุมการแสดงผล (Main Routing)
# ----------------------------------------
if st.session_state.view_mode == 'list':
    show_list_view()
elif st.session_state.view_mode == 'detail':
    show_detail_view()
elif st.session_state.view_mode == 'success':
    show_success_view()

import streamlit as st
import pyautogui
from sql_execute import farm_tb_insert
st.set_page_config(
    page_title="ทะเบียนที่อยู่แปลง",
    page_icon="⛺",
)

def main():
    st.title("ทะเบียนที่อยู่แปลง⛺")
    with st.sidebar:
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page();
    with create_page_tab:
        create_page();
    with update_page_tab:
        update_page();

def create_page():
    with st.form("farm_form",clear_on_submit=True):
        st.subheader("ข้อมูลที่อยู่")
        col_left, col_right = st.columns([1,1])
        with col_left:
            vil_name = st.text_input(label="ชื่อหมู่บ้าน")
            subdistrict_name = st.text_input(label="ชื่อตำบล")
            province_name = st.text_input(label="ชื่อจังหวัด")
        with col_right:
            vil_no = st.text_input(label="เลขที่หมู่", max_chars=2)
            district_name = st.text_input(label="ชื่ออำเภอ")
        st.subheader("ข้อมูลคุณสมบัติ")
        land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน")
        soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", value=False)
        water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", value=False)
        gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", value=False)
        st.markdown("""---""")
        col1, col_center, col3 = st.columns([2,1,2])
        with col_center:
            submit_button_clicked = st.form_submit_button(label="เพิ่มข้อมูล")
        if submit_button_clicked:
            farm_tb_insert(vil_name, district_name, vil_no, subdistrict_name, province_name,
                            land_privileges, soil_analysis, water_analysis, gap_analysis)
            st.success("เพิ่มข้อมูลสำเร็จ!")

def update_page():
    a = [1, "12", "ทดสอบชื่อหมู่บ้าน", "ทดสอบชื่อตำบล", "ทดสอบชื่ออำเภอ", "ทดสอบชื่อจังหวัด", "50300", 20,
         2,"ทดสอบสิทธิประโยชน์ที่ดิน", True, True, False]
    b = [2, "14", "ทดสอบชื่อหมู่บ้าน2", "ทดสอบชื่อตำบล2", "ทดสอบชื่ออำเภอ2", "ทดสอบชื่อจังหวัด2", "50400", 19,
         3,"ทดสอบสิทธิประโยชน์ที่ดิน2", False, True, False]
    # st.write(a,b)
    update_page_options = (a, b)
    st.subheader("รายชื่อที่อยู่แปลง")
    farm_selected = st.selectbox(label="กรุณาเลือกที่อยู่แปลง", options=update_page_options)
    if farm_selected:
        st.subheader("ข้อมูลที่อยู่")
        col_left, col_right = st.columns([1,1])
        with col_left:
            vil_name = st.text_input(label="ชื่อหมู่บ้าน", value=farm_selected[2])
            district_name = st.text_input(label="ชื่ออำเภอ", value=farm_selected[4])
            postcode = st.text_input(label="รหัสไปรษณีย์", value=farm_selected[6], max_chars=5)
        with col_right:
            vil_no = st.text_input(label="เลขที่หมู่", value=farm_selected[1], max_chars=2)
            subdistrict_name = st.text_input(label="ชื่อตำบล", value=farm_selected[3])
            province_name = st.text_input(label="ชื่อจังหวัด", value=farm_selected[5])
        st.subheader("ข้อมูลคุณสมบัติ")
        col_left, col_right = st.columns([2,2])
        with col_left:
            farm_quantity = st.number_input(label="จำนวนพื้นที่(ไร่)", value=farm_selected[7], min_value=0, step=1)
        with col_right:
            building_quantity = st.number_input(label="จำนวนพื้นที่(โรงเรือน)", value=farm_selected[8], min_value=0, step=1)
        land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน", value=farm_selected[9])
        soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", value=farm_selected[10])
        water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", value=farm_selected[11])
        gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", value=farm_selected[12])
        st.markdown("""---""")
        col_left, col2, col3, col_right, col5 = st.columns([1, 1, 1, 1, 1])
        with col_right:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col_right:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked:
            st.success("แก้ไขข้อมูลสำเร็จ!")
        if delete_button_clicked:
            st.error("ลบข้อมูลสำเร็จ!")
            pyautogui.hotkey("ctrl", "F5")

def select_page():
    a = [1, "6", "ทดสอบชื่อหมู่บ้าน1", "ทดสอบชื่อตำบล1", "ทดสอบชื่ออำเภอ1", "ทดสอบชื่อจังหวัด1", "ทดสอบสิทธิประโยชน์ที่ดิน1", True, True, False]
    b = [2, "2", "ทดสอบชื่อหมู่บ้าน2", "ทดสอบชื่อตำบล2", "ทดสอบชื่ออำเภอ2", "ทดสอบชื่อจังหวัด2", "ทดสอบสิทธิประโยชน์ที่ดิน2", True, True, False]
    data = (a, b)
    #st.write(a)
    n = 1
    for i in data:
        col_left, col_right, col3 = st.columns([1, 2, 2])
        with col_left:
            st.title("{}. {:03d}".format(n, i[0]))
        with col_right:
            st.caption("ข้อมูลที่อยู่แปลง")
            st.text("ที่อยู่:หมู่ที่ {}".format(i[1]))
            st.text("ตำบล: {}".format(i[3]))
            st.text("จังหวัด: {}".format(i[5]))
            st.caption("คุณสมบัติ")
            st.text("สิทธิประโยชน์ที่ดิน: ")
            st.text("ได้รับการตรวจวิเคราะห์ดินแล้ว: ")
            st.text("ได้รับการตรวจวิเคราะห์น้ำแล้ว: ")
            st.text("ได้รับการรับรองระบบ GAP แล้ว: ")
        with col3:
            st.caption(".")
            st.text("หมู่บ้าน: {}".format(i[2]))
            st.text("อำเภอ: {}".format(i[4]))
            st.caption(".")
            st.caption(".")
            st.text(i[6])
            if i[7] == True:
                st.text("ตรวจแล้ว")
            else: st.text("ยังไม่ได้ตรวจ")
            if i[8] == True:
                st.text("ตรวจแล้ว")
            else: st.text("ยังไม่ได้ตรวจ")
            if i[9] == True:
                st.text("ตรวจแล้ว")
            else: st.text("ยังไม่ได้ตรวจ")
        st.markdown("""---""")
        n += 1

main()
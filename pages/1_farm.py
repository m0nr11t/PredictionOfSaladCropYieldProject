import streamlit as st
import pyautogui
from sql_execute import farm_tb_insert,farm_tb_select
from calculate import timestamp
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
        created_at = timestamp()
        updated_at = created_at
        col_left, col_right = st.columns([1,1])
        with col_left:
            vil_no = st.text_input(label="เลขที่หมู่", max_chars=2)
            subdistrict_name = st.text_input(label="ชื่อตำบล")
            province_name = st.text_input(label="ชื่อจังหวัด")
        with col_right:
            vil_name = st.text_input(label="ชื่อหมู่บ้าน")
            district_name = st.text_input(label="ชื่ออำเภอ")
        st.subheader("ข้อมูลคุณสมบัติ")
        col_left,col_center,col_right = st.columns([1,1,1])
        with col_left:
            geo_x = st.text_input(label="พิกัดแกน X")
        with col_center:
            geo_y = st.text_input(label="พิกัดแกน Y")
        with col_right:
            geo_z = st.text_input(label="พิกัดแกน Z")
        land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน")
        soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", value=False)
        water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", value=False)
        gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", value=False)
        st.markdown("""---""")
        col1, col_center, col3 = st.columns([2,1,2])
        with col_center:
            submit_button_clicked = st.form_submit_button(label="เพิ่มข้อมูล")
        if submit_button_clicked:
            farm_tb_insert(vil_name, district_name, vil_no, subdistrict_name, province_name, geo_x, geo_y, geo_z,
                            land_privileges, soil_analysis, water_analysis, gap_analysis,created_at,updated_at)
            st.success("เพิ่มข้อมูลสำเร็จ!")

def update_page():
        st.subheader("ข้อมูลที่อยู่")
        updated_at = timestamp()
        update_page_options = farm_tb_select()
        farm_selected = st.selectbox("วันที่แก้ไข", options=update_page_options,
                                     format_func=lambda update_page_options: "หมู่ที่ {} ตำบล{} อำเภอ{} จังหวัด{}".format(update_page_options[0],update_page_options[1],update_page_options[2],update_page_options[3]))
        st.write(farm_selected)
        col_left, col_right = st.columns([1,1])
        with col_left:
            vil_no = st.text_input(label="เลขที่หมู่", max_chars=2)
            subdistrict_name = st.text_input(label="ชื่อตำบล")
            province_name = st.text_input(label="ชื่อจังหวัด")
        with col_right:
            vil_name = st.text_input(label="ชื่อหมู่บ้าน")
            district_name = st.text_input(label="ชื่ออำเภอ")
        st.subheader("ข้อมูลคุณสมบัติ")
        col_left,col_center,col_right = st.columns([1,1,1])
        with col_left:
            geo_x = st.text_input(label="พิกัดแกน X")
        with col_center:
            geo_y = st.text_input(label="พิกัดแกน Y")
        with col_right:
            geo_z = st.text_input(label="พิกัดแกน Z")
        land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน")
        soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", value=False)
        water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", value=False)
        gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", value=False)
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
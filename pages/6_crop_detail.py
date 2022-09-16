import streamlit as st
import pyautogui

def main():
    st.title("รายละเอียดแผนการเก็บเกี่ยว🔪")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page()
    with create_page_tab:
        create_page()
    with update_page_tab:
        update_page()

def create_page():
    with st.form("crop_detail",clear_on_submit=True):
        crop_id = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย",options=("รอดึงข้อมูล","รอดึงข้อมูล"))
        farmer_id = st.selectbox(label="รหัสเกษตรกร",options=("รอดึงข้อมูล","รอดึงข้อมูล"))
        plant_weight_before_trim = st.number_input(label="น้ำหนักผลผลิตก่อนตัดแต่ง",min_value=0.00)
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง",min_value=0.00)
        plant_quantity = st.number_input(label="จำนวนกล้า",min_value=0,step=1)
        col1, col2 = st.columns([2, 2])
        with col1:
            farm_rai = st.number_input(label="จำนวนพื้นที่(ไร่)", min_value=0, step=1)
            farm_ngan = st.number_input(label="จำนวนพื้นที่(งาน)", min_value=0, step=1)
        with col2:
            farm_building = st.number_input(label="จำนวนพื้นที่(โรงเรือน)", min_value=0, step=1)
            farm_plang = st.number_input(label="จำนวนพื้นที่(แปลง)", min_value=0, step=1)
        plant_number = st.number_input(label="จำนวนต้น",min_value=0,step=1)
        col1, col2 = st.columns([2, 2])
        with col1:
            animal_place = st.number_input(label="จำนวนแห่ง", min_value=0, step=1)
        with col2:
            animal_pond = st.number_input(label="จำนวนบ่อ", min_value=0, step=1)
        animal_number = st.number_input(label="จำนวนตัว", min_value=0, step=1)
        if st.form_submit_button(label="เพิ่มข้อมูล"):
            st.success("เพิ่มข้อมูลสำเร็จ!")

def update_page():
    a = [1, 1, 20, 20, 10, 15]
    b = [1, 1, 20, 20, 10, 15]
    update_options = (a, b)
    crop_id = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย", options=(update_options))
    farmer_id = st.selectbox(label="รหัสเกษตรกร", options=(update_options))
    if farmer_id:
        plant_weight_before_trim = st.number_input(label="น้ำหนักผลผลิตก่อนตัดแต่ง",min_value=0.00)
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง",min_value=0.00)
        plant_quantity = st.number_input(label="จำนวนกล้า", min_value=0, step=1)
        plant_area = st.number_input(label="พื้นที่เพาะปลูก", min_value=0, step=1)
        st.markdown("""---""")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked:
            st.success("แก้ไขข้อมูลสำเร็จ!")
        elif delete_button_clicked:
            st.error("ลบข้อมูลสำเร็จ!")
            pyautogui.hotkey("ctrl", "F5")

def select_page():
    a = [1, 1, 20, 20, 10, 15]
    b = [1, 1, 20, 20, 10, 15]
    data = (a, b)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.title("{}. {:03d}".format(n, i[0]))
        with col2:
            st.text("รหัสแผนการเพาะปลูกโดยย่อย: ".format(i[1]))
            st.text("ชื่อ: {}".format(i[1]))
            st.text("น้ำหนักผลผลิตก่อนตัดแต่ง: ".format(i[1]))
            st.text("จำนวนกล้า: ".format(i[1]))
        with col3:
            st.text(".")
            st.text("นามสกุล: {}".format(i[1]))
            st.text("น้ำหนักผลผลิตหลังตัดแต่ง: ".format(i[1]))
            st.text("พื้นที่เพาะปลูก: ".format(i[1]))
        st.markdown("""---""")
        n += 1

main()
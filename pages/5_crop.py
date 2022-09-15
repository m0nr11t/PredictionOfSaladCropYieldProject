import streamlit as st
import pyautogui
from datetime import datetime

def main():
    st.title("แผนการเพาะปลูกโดยย่อย🔪")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page()
    with create_page_tab:
        create_page()
    with update_page_tab:
        update_page()

def create_page():
    with st.form("crop_form",clear_on_submit=True):
        crop_id = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย",options=("รอดึงข้อมูล","รอดึงข้อมูล"))
        plan_id = st.selectbox(label="รหัสแผนการเพาะปลูก",options=("รอดึงข้อมูล","รอดึงข้อมูล"))
        cropstart_date = st.date_input(label="วันที่เริ่มต้นแผนการปลูก")
        cropfinish_date = st.date_input(label="วันที่สิ้นสุดแผนการปลูก")
        cropmove_date = st.date_input(label="วันที่ย้ายแผนการปลูก")
        number_farmers = st.number_input(label="จำนวนเกษตรกร",min_value=0,step=1)
        if st.form_submit_button(label="เพิ่มข้อมูล"):
            st.success("เพิ่มข้อมูลสำเร็จ!")
def update_page():
    a = [1, 1, '2022-08-23', '2022-08-23', '2022-08-23', 5]
    b = [2, 1, '2022-08-30', '2022-08-30', '2022-08-30', 5]
    update_page_options = (a, b)
    st.subheader("รหัสแผนการเพาะปลูกโดยย่อย")
    crop_selected = st.selectbox(label="กรุณาเลือกรหัสแผนการเพาะปลูกโดยย่อย", options=update_page_options)
    if crop_selected:
        if crop_selected[2]:
            cropstart_date = datetime.strptime(crop_selected[2],'%Y-%m-%d')
        cropstart_date = st.date_input(label="วันที่เริ่มต้นแผนการปลูก", value=cropstart_date)
        if crop_selected[3]:
            cropfinish_date = datetime.strptime(crop_selected[2],'%Y-%m-%d')
        cropfinish_date = st.date_input(label="วันที่สิ้นสุดแผนการปลูก", value=cropfinish_date)
        if crop_selected[4]:
            cropmove_date = datetime.strptime(crop_selected[2],'%Y-%m-%d')
        cropmove_date = st.date_input(label="วันที่ย้ายแผนการปลูก", value=cropmove_date)
        number_farmers = st.number_input(label="จำนวนเกษตรกร",min_value=0,step=1, value=crop_selected[5])
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
    a = [1, 1, '2022-08-23', '2022-08-23', '2022-08-23', 5]
    b = [2, 1, '2022-08-30', '2022-08-30', '2022-08-30', 5]
    data = (a, b)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.title("{}. {:03d}".format(n, i[0]))
        with col2:
            st.text("แผนการปลูก: ")
            st.text("วันที่เริ่มต้นแผนการปลูก: ")
            st.text("วันที่สิ้นสุดแผนการปลูก: ")
            st.text("วันที่ย้ายแผนการปลูก: ")
            st.text("จำนวนเกษตรกร: ")
        with col3:
            st.text(i[1])
            st.text(i[2])
            st.text(i[3])
            st.text(i[4])
            st.text(i[5])
        st.markdown("""---""")
        n += 1

main()
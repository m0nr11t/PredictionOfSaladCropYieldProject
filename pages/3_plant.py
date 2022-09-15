import streamlit as st
import pyautogui
from calculate import timestamp
from sql_execute import plant_tb_insert
st.set_page_config(
    page_title="พืช",
    page_icon="🌱",
)

def main():
    st.title("พืช🌱")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page()
    with create_page_tab:
        create_page()
    with update_page_tab:
        update_page()

def create_page():
    with st.form("plant_form",clear_on_submit=True):
        plant_name = st.text_input(label="ชื่อพืช")
        uploaded_file = st.file_uploader(label="แนบภาพไฟล์รูป",type=["jpg","png","jpeg"], accept_multiple_files=False)
        if uploaded_file is not None:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)
            st.write(bytes_data)
        col1, col2, col3 = st.columns([2,1,2])
        with col2:
            submit_button_clicked = st.form_submit_button(label="เพิ่มข้อมูล")
        if submit_button_clicked:
            created_at = timestamp()
            updated_at = created_at
            plant_tb_insert(plant_name, bytes_data, created_at, updated_at)
            st.success("เพิ่มข้อมูลสำเร็จ!")


def update_page():
    a = [1,"ประเภทที่ 1","ผักคะน้าฮ่องกง"]
    b = [2,"ประเภทที่ 2","ผักบุ้ง"]
    update_page_options = (a, b)
    st.subheader("รายชื่อพืช")
    plant_selected = st.selectbox(label="กรุณาเลือกพืช", options=update_page_options)
    st.subheader("ข้อมูลพืช")
    if plant_selected:
        plant_name = st.text_input(label="ชื่อพืช",value=plant_selected[2])
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
    a = [1, "ประเภทที่ 1", "ผักคะน้าฮ่องกง"]
    b = [2, "ประเภทที่ 2", "ผักบุ้ง"]
    data = (a, b)
    # st.write(data)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.title("{}. {:03d}".format(n, i[0]))
        with col2:
            st.text("ประเภทพืช: ")
            st.text("พืช: ")
        with col3:
            st.text(i[1])
            st.text(i[2])
        st.markdown("""---""")
        n += 1

main()
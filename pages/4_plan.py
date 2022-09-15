import streamlit as st
import pyautogui

def main():
    st.title("แผนการเพาะปลูก📃")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page()
    with create_page_tab:
        create_page()
    with update_page_tab:
        update_page()

def create_page():
    with st.form("plan_form",clear_on_submit=True):
        plant_name = st.selectbox(label="ชื่อพืช",options=("รอดึงข้อมูล","รอดึงข้อมูล"))
        category_options = category_tb_select()
        category_selected = st.selectbox(label="ประเภทพืช",options=(category_options), format_func=lambda category_options: "{:03d}: {}".format(category_options[0],category_options[1]))
        if category_selected:
            category_id = category_selected[0]
        plan_year = st.number_input(label="แผนปีที่",min_value=1900,max_value=9999,step=1,format="%d")
        if st.form_submit_button(label="เพิ่มข้อมูล"):
            st.success("เพิ่มข้อมูลสำเร็จ! {}".format(plant_name))

def update_page():
    a = [1, "ผักคะน้าฮ่องกง",2022]
    b = [2, "ผักบุ้ง",2023]
    update_page_options = (a, b)
    st.subheader("รายชื่อพืช")
    plan_selected = st.selectbox(label="กรุณาเลือกพืช", options=update_page_options)
    st.subheader("ข้อมูลพืช")
    if plan_selected:
        plan_year = st.number_input(label="แผนปีที่",min_value=1900,max_value=9999,step=1,format="%d",value=plan_selected[2])
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
    a = [1, "ผักคะน้าฮ่องกง", 2022]
    b = [2, "ผักบุ้ง", 2023]
    data = (a, b)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.title("{}. {:03d}".format(n, i[0]))
        with col2:
            st.text("พืช: ")
            st.text("ปีที่วางแผน: ")
        with col3:
            st.text(i[1])
            st.text(i[2])
        st.markdown("""---""")
        n += 1

main()
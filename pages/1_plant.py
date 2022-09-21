import streamlit as st
import pyautogui
import time
from calculate import timestamp, load_image
from sql_execute import plants_tb_insert, plants_tb_select, tb_select_pil, plants_tb_update, plants_tb_delete
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
    with st.form("plants_form",clear_on_submit=True):
        plant_name = st.text_input(label="ชื่อพืช:")
        image_file = st.file_uploader(label="แนบไฟล์รูป:",type=["jpg","png","jpeg"], accept_multiple_files=False)
        if image_file is not None:
            image_file = load_image(image_file)
        else:
            image_file = load_image('none.png')
        col1, col2, col3 = st.columns([2,1,2])
        with col2:
            submit_button_clicked = st.form_submit_button(label="เพิ่มข้อมูล")
        if submit_button_clicked:
            created_at = timestamp()
            updated_at = created_at
            plants_tb_insert(plant_name, image_file, created_at, updated_at)
            st.success("เพิ่มข้อมูล พืช{} สำเร็จ!".format(plant_name))
            time.sleep(1.5)
            st.experimental_rerun()


def update_page():
    update_page_options = plants_tb_select()
    st.subheader("รายชื่อพืช:")
    plant_selected = st.selectbox(label="กรุณาเลือกพืช:", options=update_page_options,format_func=lambda update_page_options: "{:03d}: {}".format(update_page_options[0],update_page_options[1]))
    plant_id = plant_selected[0]
    plant_name = plant_selected[1]
    table_name = ("plants")
    pk = ("plant_id")
    img,row = tb_select_pil(table_name, pk,plant_selected[0], outfile=None)
    image_before = row
    col_left,col_right = st.columns([1, 1])
    with col_left:
        st.subheader("รูปภาพ")
        st.image(img,width=300)

    with col_right:
        st.subheader("ข้อมูลพืช")
        if plant_selected:
            plant_name = st.text_input(label="แก้ไขชื่อพืช",value=plant_selected[1])
            image_file_after = st.file_uploader(label="แก้ไขรูป", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
            if image_file_after is not None:
                image_file = load_image(image_file_after)
            else:
                image_file = image_before
    st.markdown("""---""")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        edit_button_clicked = st.button(label="แก้ไขข้อมูล")
    with col4:
        delete_button_clicked = st.button(label="ลบข้อมูล")
    if edit_button_clicked:
        updated_at = timestamp()
        plants_tb_update(plant_id,plant_name,image_file,updated_at)
        st.success("แก้ไขข้อมูลสำเร็จ!")
        time.sleep(1.5)
        st.experimental_rerun()
    elif delete_button_clicked:
        plants_tb_delete(plant_id)
        st.error("ลบข้อมูลสำเร็จ!")
        time.sleep(1.5)
        pyautogui.hotkey("ctrl", "F5")
        st.experimental_rerun()


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
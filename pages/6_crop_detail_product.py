import streamlit as st
import pyautogui
import time
from calculate import timestamp,load_image
from sql_execute import crops_options_select,crop_details_tb_select,crop_detail_products_tb_insert,crop_detail_products_duplicate,crop_detail_products_tb_select,tb_select_pil,crop_detail_products_tb_update,crop_detail_products_tb_delete

def main():
    st.title("ผลผลิตการเก็บเกี่ยว🔪")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page()
    with create_page_tab:
        create_page()
    with update_page_tab:
        update_page()

def create_page():
    crop_options = crops_options_select()
    crop_selected = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย", options=crop_options, format_func=lambda crop_options: "แผน{} ({}) ครอปที่ {}".format(crop_options[1],crop_options[2],crop_options[3]))
    crop_details_options = crop_details_tb_select(crop_selected[0])
    crop_details_selected = st.selectbox(label="รหัสเกษตรกร", options=crop_details_options, format_func=lambda crop_details_options: "{}: {} {} ({})".format(crop_details_options[1],crop_details_options[2],crop_details_options[3],crop_details_options[4]))
    if crop_details_selected is None:
        plant_weight_before_trim = st.number_input(label="น้ำหนักผลผลิตก่อนตัดแต่ง", min_value=float(0), format=("%f"), disabled=True)
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง", min_value=float(0), format=("%f"), disabled=True)
    else:
        plant_weight_before_trim = st.number_input(label="น้ำหนักผลผลิตก่อนตัดแต่ง",min_value=float(0), format=("%f"))
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง",min_value=float(0), format=("%f"))
        image_file = st.file_uploader(label="แนบไฟล์รูป:", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
        if image_file is not None:
            image_file = load_image(image_file)
        else:
            image_file = load_image('none.png')
        crop_detail_products_check = crop_detail_products_duplicate()
        duplicate_crop_detail_products_check = True
        for rows in crop_detail_products_check:
            condition_duplicate = (str(rows[0]) + str(rows[1]) == str(crop_details_selected[0]) + str(crop_details_selected[1]))
            if condition_duplicate == True:
                duplicate_crop_detail_products_check = False
        if st.button(label="เพิ่มข้อมูล"):
            if duplicate_crop_detail_products_check == True:
                created_at = timestamp()
                updated_at = created_at
                crop_detail_products_tb_insert(plant_weight_before_trim, plant_weight_after_trim, image_file, created_at, updated_at, crop_details_selected[0], crop_details_selected[1])
                st.success("เพิ่มข้อมูลสำเร็จ!")
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.error("ข้อมูลผลการเก็บเกี่ยวรายนี้ถูกเพิ่มไว้แล้ว ไปที่เมนูแก้ไข")

def update_page():
    crop_options = crops_options_select()
    crop_selected = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย", options=crop_options,
                                 format_func=lambda crop_options: "แผน{} ({}) ครอปที่ {}".format(crop_options[1],
                                                                                                 crop_options[2],
                                                                                                 crop_options[3]), key=("update_crop_selected"))
    crop_detail_products_options = crop_detail_products_tb_select(crop_selected[0])
    crop_detail_product_tb_selected = st.selectbox(label="รหัสเกษตรกร", options=crop_detail_products_options,
                                         format_func=lambda crop_detail_products_options: "{}: {} {} ({})".format(
                                             crop_detail_products_options[2], crop_detail_products_options[3], crop_detail_products_options[4],
                                             crop_detail_products_options[5]), key=("update_crop_details_selected"))
    if crop_detail_product_tb_selected is None:
        plant_weight_before_trim = st.number_input(label="น้ำหนักผลผลิตก่อนตัดแต่ง", min_value=float(0), format=("%f"),
                                                   disabled=True, key=("update_plant_weight_before_trim"))
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง", min_value=float(0), format=("%f"),
                                                  disabled=True, key=("update_plant_weight_after_trim"))
    else:
        table_name = ("crop_detail_products")
        pk = ("crop_detail_product_id")
        img, row = tb_select_pil(table_name, pk, crop_detail_product_tb_selected[0], outfile=None)
        image_before = row
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.image(img, width=250)
        with col_right:
            plant_weight_before_trim = st.number_input(label="น้ำหนักผลผลิตก่อนตัดแต่ง", min_value=float(0), format=("%f"), key=("update_plant_weight_before_trim"))
            plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง", min_value=float(0), format=("%f"), key=("update_plant_weight_after_trim"))
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
            crop_detail_products_tb_update(crop_detail_product_tb_selected[0], plant_weight_before_trim,
                                           plant_weight_after_trim, image_file, updated_at)
            st.success("แก้ไขข้อมูลสำเร็จ!")
            time.sleep(1.5)
            st.experimental_rerun()
        elif delete_button_clicked:
            crop_detail_products_tb_delete(crop_detail_product_tb_selected[0])
            st.error("ลบข้อมูลสำเร็จ!")
            time.sleep(1.5)
            pyautogui.hotkey("ctrl", "F5")
            st.experimental_rerun()


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
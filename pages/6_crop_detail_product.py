import streamlit as st
import pyautogui
import time
from calculate import timestamp,load_image
from sql_execute import crops_options_select,crop_details_tb_select,\
    crop_detail_products_duplicate,tb_select_pil,\
    table_details_select,variables_query,db_connection,variable_update,variable_delete,variable_img_update

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
    table_name = ("crop_detail_products")
    crop_options = crops_options_select()
    crop_selected = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย", options=crop_options, format_func=lambda crop_options: "แผน{} ({}) ครอปที่ {}".format(crop_options[1],crop_options[2],crop_options[3]))
    crop_details_options = crop_details_tb_select(crop_selected[0])
    crop_details_selected = st.selectbox(label="รหัสเกษตรกร", options=crop_details_options, format_func=lambda crop_details_options: "{}: {} {} ({})".format(crop_details_options[1],crop_details_options[2],crop_details_options[3],crop_details_options[4]))
    columns = table_details_select(table_name)
    if crop_details_selected is None:
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง", value=float(0), min_value=float(0), format=("%f"), disabled=True)
        for rows in columns:
            if rows[2] == "double precision":
                column_name = rows[0]
                globals()[column_name] = st.number_input(label=rows[1], value=float(0) ,min_value=float(0), key=rows[0], format=("%f"), disabled=True)
            elif rows[2] == "integer":
                column_name = rows[0]
                globals()[column_name] = int(st.number_input(label=rows[1], value=0, min_value=0, step=1, key=rows[0], format=("%d")))
    else:
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง",min_value=float(0), format=("%f"))
        sql_columns_name = ("")
        updated_at = timestamp()
        n = 0
        for rows in columns:
            if rows[2] == "double precision":
                column_name = rows[0]
                globals()[column_name] = float(st.number_input(label=rows[1],min_value=float(0), key=rows[0], format=("%f")))
            elif rows[2] == "integer":
                column_name = rows[0]
                globals()[column_name] = int(st.number_input(label=rows[1], min_value=0, step=1, key=rows[0], format=("%d")))
            if n == 0:
                sql_columns_name = sql_columns_name + rows[0]
            else:
                sql_columns_name = sql_columns_name + str(",") + rows[0]
            n+=1
        sql_columns_name = sql_columns_name + str(",created_at,updated_at")
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
                created_at = str(timestamp())
                updated_at = created_at
                db_connect, c = db_connection()
                sql_statement = """INSERT INTO crop_detail_products(plant_weight_after_trim, img, crop_id, farmer_id, {})
                                     VALUES (%s, %s, %s, %s, {});""".format(sql_columns_name,
                                                                                              str(eval(sql_columns_name)).replace("(","").replace(")",""))
                values = (plant_weight_after_trim, image_file, crop_details_selected[0], crop_details_selected[1])
                st.write(sql_statement)
                c.execute(sql_statement,values)
                db_connect.commit()
                db_connect.close()
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

    table_name = "crop_detail_products"
    columns_query = (
        "crop_detail_product_id, crop_id, crop_detail_products.farmer_id, firstname, lastname, farmer_gov_id, plant_weight_after_trim,")
    from_con = "FROM crop_detail_products"
    join_con = ("INNER JOIN farmers")
    on_con = ("ON crop_detail_products.farmer_id = farmers.farmer_id")
    where_con = ("WHERE crop_id = {}".format(crop_selected[0]))
    order_by_con = ("")
    columns = table_details_select(table_name)
    n = 0
    for columns_name in columns:
        if n == 0:
            columns_query = columns_query + columns_name[0]
        else:
            columns_query = columns_query + str(",") + columns_name[0]
    update_page_options = variables_query(columns_query,from_con, join_con, on_con, where_con,order_by_con)
    update_page_options_selected = st.selectbox(label="รหัสเกษตรกร", options=update_page_options,
                                         format_func=lambda update_page_options: "{}: {} {} ({})".format(
                                             update_page_options[2], update_page_options[3], update_page_options[4],
                                             update_page_options[5]), key=("update_crop_details_selected"))
    if update_page_options_selected is None:
        plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง", value=0.00, min_value=float(0), format=("%f"),
                                                   disabled=True, key=("update_plant_weight_after_trim"))
        for rows in columns:
            if rows[2] == "double precision":
                column_name = rows[0]
                globals()[column_name] = float(st.number_input(label=(rows[1]), min_value=float(0), format=("%f"),
                                                               key=(str("edit_") + rows[0]),
                                                               value=0.00, disabled=True))
            elif rows[2] == "integer":
                column_name = rows[0]
                globals()[column_name] = int(st.number_input(label=rows[1], min_value=int(0), format=("%d"), step=1,
                                                             key=(str("edit_") + rows[0]),
                                                             value=0, disabled=True))
    else:
        table_name = ("crop_detail_products")
        pk = ("crop_detail_product_id")
        img, row = tb_select_pil(table_name, pk, update_page_options_selected[0], outfile=None)
        image_before = row
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.image(img, width=250)
        with col_right:
            plant_weight_after_trim = st.number_input(label="น้ำหนักผลผลิตหลังตัดแต่ง", min_value=float(0), format=("%f"), key=("update_plant_weight_after_trim"),value=update_page_options_selected[6])
            updated_at = str(timestamp())
            sql_update = ("plant_weight_after_trim = '") + str(plant_weight_after_trim) + str("', ")
            n = 7
            for rows in columns:
                if rows[2] == "double precision":
                    column_name = rows[0]
                    globals()[column_name] = float(st.number_input(label=(rows[1]), min_value=float(0), format=("%f"),
                                                                   key=(str("edit_") + rows[0]),
                                                                   value=update_page_options_selected[n]))
                elif rows[2] == "integer":
                    column_name = rows[0]
                    globals()[column_name] = int(st.number_input(label=rows[1], min_value=int(0), format=("%d"), step=1,
                                                                 key=(str("edit_") + rows[0]),
                                                                 value=update_page_options_selected[n]))
                n += 1
                sql_update = sql_update + rows[0] + str(" = '") + str(eval(rows[0])) + str("', ")
            where_update = ("WHERE crop_detail_product_id = {}".format(update_page_options_selected[0]))
            image_file_after = st.file_uploader(label="แก้ไขรูป", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
            if image_file_after is not None:
                image_file = load_image(image_file_after)
            else:
                image_file = image_before
            sql_update = sql_update + str("updated_at = '") + str(updated_at) + str("'")
        st.markdown("""---""")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked:
            variable_update(table_name, sql_update, where_update)
            variable_img_update(image_file, update_page_options_selected[0])
            st.success("แก้ไขข้อมูลสำเร็จ!")
            time.sleep(1.5)
            st.experimental_rerun()
        elif delete_button_clicked:
            where_delete = ("WHERE crop_detail_product_id = {}".format(update_page_options_selected[0]))
            variable_delete(table_name, where_delete)
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
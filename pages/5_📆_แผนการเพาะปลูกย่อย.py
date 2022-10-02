import streamlit as st
# import pyautogui
import time
from datetime import date,datetime,timedelta
from sql_execute import plans_tb_select,crops_tb_insert,crop_number,crops_tb_select,crops_tb_update,crops_tb_delete,crops_tb_plans_select
from calculate import timestamp

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
    plan_options = plans_tb_select()
    plan_selected = st.selectbox(label="กรุณาเลือกแผน", options=plan_options, format_func=lambda plan_options: "แผน{} ({})".format(plan_options[5],plan_options[0]))
    crop_no = crop_number(plan_selected[3])
    crop_no = crop_no[0] + 1
    st.markdown("##### ครอปที่ {}:".format(crop_no))
    cropstart_date = st.date_input(label="วันที่เริ่มต้นแผนการปลูก",min_value=date(1900,1,1))
    cropmove_date = st.date_input(label="วันที่ย้ายแผนการปลูก", value=(cropstart_date+timedelta(days=1)), min_value=(cropstart_date+timedelta(days=1)))
    cropfinish_date = st.date_input(label="วันที่สิ้นสุดแผนการปลูก", value=(cropmove_date+timedelta(days=1)), min_value=(cropmove_date+timedelta(days=1)))
    if st.button(label="เพิ่มข้อมูล"):
        created_at = timestamp()
        updated_at = created_at
        crops_tb_insert(cropstart_date, cropmove_date, cropfinish_date, created_at, updated_at, plan_selected[3])
        st.success("เพิ่มข้อมูลสำเร็จ!")
        time.sleep(1.5)
        st.experimental_rerun()

def update_page():
    plans_options = crops_tb_plans_select()
    plan_selected = st.selectbox(label="กรุณาเลือกแผน", options=plans_options, format_func=lambda plans_options: "แผน{} ({})".format(plans_options[1],plans_options[0]), key=("updated_plan_id"))
    update_page_options = crops_tb_select(plan_selected[2])
    crop_selected = st.selectbox(label="กรุณาเลือกครอป", options=update_page_options, format_func=lambda update_page_options: "ครอปที่ {}".format(update_page_options[7]), key=("updated_crop_id"))
    cropstart_date = st.date_input(label="วันที่เริ่มต้นแผนการปลูก",min_value=date(1900,1,1), value=crop_selected[0], key=("update_cropstart_date"))
    if cropstart_date == crop_selected[0]:
        cropmove_date = st.date_input(label="วันที่ย้ายแผนการปลูก", min_value=(cropstart_date+timedelta(days=1)), value=crop_selected[1], key=("update_cropmove_date"))
    else:
        cropmove_date = st.date_input(label="วันที่ย้ายแผนการปลูก", min_value=(cropstart_date + timedelta(days=1)),
                                      value=(cropstart_date + timedelta(days=1)), key=("update_cropmove_date"))
    if cropmove_date == crop_selected[1]:
        cropfinish_date = st.date_input(label="วันที่สิ้นสุดแผนการปลูก",
                                        min_value=(cropmove_date + timedelta(days=1)), value=crop_selected[2],
                                        key=("update_cropfinish_date"))
    else:
        cropfinish_date = st.date_input(label="วันที่สิ้นสุดแผนการปลูก",
                                        min_value=(cropmove_date + timedelta(days=1)), value=(cropmove_date + timedelta(days=1)),
                                        key=("update_cropfinish_date"))
    st.markdown("""---""")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        edit_button_clicked = st.button(label="แก้ไขข้อมูล")
    with col4:
        delete_button_clicked = st.button(label="ลบข้อมูล")
    if edit_button_clicked:
        updated_at = timestamp()
        crops_tb_update(crop_selected[5], cropstart_date, cropmove_date ,cropfinish_date, updated_at)
        st.success("แก้ไขข้อมูลสำเร็จ!")
        time.sleep(1.5)
        st.experimental_rerun()
    elif delete_button_clicked:
        crops_tb_delete(crop_selected[5])
        st.error("ลบข้อมูลสำเร็จ!")
        time.sleep(1.5)
        # pyautogui.hotkey("ctrl", "F5")
        st.experimental_rerun()


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
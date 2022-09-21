import streamlit as st
import time
import pyautogui
from calculate import timestamp
from sql_execute import plants_tb_select,plans_tb_insert,plan_duplicate,plans_tb_select,plans_tb_update,plans_tb_delete

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
    with st.form("plans_form",clear_on_submit=True):
         plants_options = plants_tb_select()
         st.subheader("แผนของพืช")
         plant_selected = st.selectbox(label="รายชื่อพืช",options=(plants_options), format_func=lambda plants_options: "{:03d}: {}".format(plants_options[0],plants_options[1]))
         st.subheader("ข้อมูลแผน")
         plan_year = int(st.number_input(label="ปีที่วางแผน",min_value=1900,max_value=9999,step=1,format="%d"))
         plan_check = plan_duplicate()
         duplicate_plan_check = True
         for rows in plan_check:
             condition_duplicate = (str(plant_selected[0])+str(plan_year) == str(rows[1])+str(rows[0]))
             if condition_duplicate == True:
                 duplicate_plan_check = False
         if st.form_submit_button(label="เพิ่มข้อมูล"):
             if duplicate_plan_check == True:
                 created_at = timestamp()
                 updated_at = created_at
                 plans_tb_insert(plan_year, created_at, updated_at, plant_selected[0])
                 st.success("เพิ่มข้อมูลสำเร็จ! แผนพืช{} ปี {}".format(plant_selected[1],plan_year))
                 time.sleep(1.5)
                 st.experimental_rerun()
             else:
                st.error("แผนพืช{} ปี {} ถูกเพิ่มไว้แล้ว กรุณาสร้างแผนอื่น".format(plant_selected[1],plan_year))

def update_page():
    update_page_options = plans_tb_select()
    st.subheader("เลือกข้อมูลแผน")
    plan_selected = st.selectbox(label="กรุณาเลือกแผน", options=update_page_options, format_func=lambda update_page_options: "แผน{} ({})".format(update_page_options[5],update_page_options[0]))
    st.subheader("ข้อมูลพืช")
    if plan_selected:
        plan_year = st.number_input(label="แผนปีที่",min_value=1900,max_value=9999,step=1,format="%d",value=plan_selected[0])
        st.markdown("""---""")
        plan_check = plan_duplicate()
        duplicate_plan_check = True
        for rows in plan_check:
            condition_duplicate = (str(plan_year) == str(rows[0]))
            if condition_duplicate == True:
                duplicate_plan_check = False
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked:
            if duplicate_plan_check == True:
                updated_at = timestamp()
                plans_tb_update(plan_year, updated_at, plan_selected[3])
                st.success("แก้ไขข้อมูลสำเร็จ!")
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.error("แผนพืช{} ปี {} ถูกเพิ่มไว้แล้ว กรุณาแก้ไขเป็นปีอื่น".format(plan_selected[5],plan_year))
        elif delete_button_clicked:
            plans_tb_delete(plan_selected[3])
            st.error("ลบข้อมูลสำเร็จ!")
            time.sleep(1.5)
            pyautogui.hotkey("ctrl", "F5")
            st.experimental_rerun()

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
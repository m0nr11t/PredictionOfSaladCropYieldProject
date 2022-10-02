import pandas as pd
import streamlit as st
# import pyautogui
import time
from calculate import timestamp, load_image
from sql_execute import plants_tb_insert, plants_tb_select, tb_select_pil, plants_tb_update, plants_tb_delete,\
                        plants_tb_select,plans_tb_insert,plan_duplicate,plans_tb_select,plans_tb_update,plans_tb_delete,\
                        plans_tb_select_all
st.set_page_config(
    page_title="พืชและแผน",
    page_icon="🌱",
    layout="wide"
)

def main():
    st.subheader("พืช🌱")
    with st.expander("จัดการข้อมูลพืช..."):
        select_plants_page_tab, create_plants_page_tab, update_plants_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
        with select_plants_page_tab:
            select_plants_page()
        with create_plants_page_tab:
            create_plants_page()
        with update_plants_page_tab:
            update_plants_page()
    st.subheader("แผนการเพาะปลูก📃")
    with st.expander("จัดการข้อมูลแผน..."):
        select_plans_page_tab, create_plans_page_tab, update_plans_page_tab = st.tabs(
            ["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
        with select_plans_page_tab:
            select_plans_page()
        with create_plans_page_tab:
            create_plans_page()
        with update_plans_page_tab:
            update_plans_page()

def create_plants_page():
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


def update_plants_page():
    update_plants_page_options = plants_tb_select()
    plant_selected = st.selectbox(label="กรุณาเลือกพืช:", options=update_plants_page_options,format_func=lambda update_plants_page_options: "{:03d}: {}".format(update_plants_page_options[0],update_plants_page_options[1]))
    plant_id = plant_selected[0]
    plant_name = plant_selected[1]
    table_name = ("plants")
    pk = ("plant_id")
    img,row = tb_select_pil(table_name, pk,plant_selected[0], outfile=None)
    image_before = row
    col_left,col_right = st.columns([1, 1])
    with col_left:
        st.image(img,width=300)

    with col_right:
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
        # pyautogui.hotkey("ctrl", "F5")
        st.experimental_rerun()


def select_plants_page():
    table_name = ("plants")
    pk = ("plant_id")
    col = ['รหัสพืช','พืช']
    df = pd.DataFrame(plants_tb_select(),columns=col)
    st.table(df['พืช'])

def create_plans_page():
    with st.form("plans_form", clear_on_submit=True):
        plants_options = plants_tb_select()
        plant_selected = st.selectbox(label="รายชื่อพืช", options=(plants_options),
                                      format_func=lambda plants_options: "{:03d}: {}".format(plants_options[0],
                                                                                             plants_options[1]))
        plan_year = int(st.number_input(label="ปีที่วางแผน", min_value=1900, max_value=9999, step=1, format="%d"))
        plan_check = plan_duplicate()
        duplicate_plan_check = True
        for rows in plan_check:
            condition_duplicate = (str(plant_selected[0]) + str(plan_year) == str(rows[1]) + str(rows[0]))
            if condition_duplicate == True:
                duplicate_plan_check = False
        if st.form_submit_button(label="เพิ่มข้อมูล"):
            if duplicate_plan_check == True:
                created_at = timestamp()
                updated_at = created_at
                plans_tb_insert(plan_year, created_at, updated_at, plant_selected[0])
                st.success("เพิ่มข้อมูลสำเร็จ! แผนพืช{} ปี {}".format(plant_selected[1], plan_year))
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.error("แผนพืช{} ปี {} ถูกเพิ่มไว้แล้ว กรุณาสร้างแผนอื่น".format(plant_selected[1], plan_year))

def update_plans_page():
    update_plans_page_options = plans_tb_select()
    plan_selected = st.selectbox(label="กรุณาเลือกแผนที่ต้องการแก้ไข:", options=update_plans_page_options,
                                 format_func=lambda update_plans_page_options: "แผน{} ({})".format(
                                     update_plans_page_options[5], update_plans_page_options[0]))
    if plan_selected:
        plan_year = st.number_input(label="แผนปีที่ต้องการแก้ไข:", min_value=1900, max_value=9999, step=1, format="%d",
                                    value=plan_selected[0])
        st.markdown("""---""")
        plan_check = plan_duplicate()
        duplicate_plan_check = True
        for rows in plan_check:
            condition_duplicate = (str(plan_year) == str(rows[0]))
            if condition_duplicate == True:
                duplicate_plan_check = False
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล",key=("plan_update"))
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล",key=("plan_delete"))
        if edit_button_clicked:
            if duplicate_plan_check == True:
                updated_at = timestamp()
                plans_tb_update(plan_year, updated_at, plan_selected[3])
                st.success("แก้ไขข้อมูลสำเร็จ!")
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.error("แผนพืช{} ปี {} ถูกเพิ่มไว้แล้ว กรุณาแก้ไขเป็นปีอื่น".format(plan_selected[5], plan_year))
        elif delete_button_clicked:
            plans_tb_delete(plan_selected[3])
            st.error("ลบข้อมูลสำเร็จ!")
            time.sleep(1.5)
            # pyautogui.hotkey("ctrl", "F5")
            st.experimental_rerun()

def select_plans_page():
    plant_options = plants_tb_select()
    plant_options.append([0,'ทั้งหมด'])
    # st.write(plant_options)
    plant_selected = st.selectbox("เลือกพืช",options=plant_options,format_func=lambda plant_options:"{}".format(plant_options[1]))
    # st.write(plant_selected)
    data = plans_tb_select_all(plant_selected[0])
    col = ['ชื่อพืช','แผนปีที่']
    df = pd.DataFrame(data,columns=col)
    st.table(df)
    # st.dataframe(df['รหัสพืช','รหัสแผน','ปีที่วางแผน','วันทีสร้าง','วันที่แก้ไข'])

main()
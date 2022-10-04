import streamlit as st
# import pyautogui
import time
from calculate import timestamp
from sql_execute import crops_options_select,farmers_tb_select,crop_details_tb_insert,crop_details_tb_select,\
    crop_details_tb_update,crop_details_tb_delete,crop_details_duplicate
st.set_page_config(
    page_title="รายละเอียดการเพาะปลูก",
    page_icon="🥦"
)
def main():
    st.subheader("รายละเอียดการเพาะปลูก🥦")
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
    farmer_options = farmers_tb_select()
    farmer_selected = st.selectbox(label="รหัสเกษตรกร", options=farmer_options, format_func=lambda farmer_options: "{}: {} {} ({})".format(farmer_options[0],farmer_options[2],farmer_options[3],farmer_options[4]))
    col1, col2 = st.columns([2, 2])
    with col1:
        farm_rai = st.number_input(label="จำนวนพื้นที่(ไร่)", min_value=float(0), format=("%f"))
        farm_building = st.number_input(label="จำนวนพื้นที่(โรงเรือน)", min_value=int(0), step=1, format=("%d"))
    with col2:
        farm_ngan = st.number_input(label="จำนวนพื้นที่(งาน)", min_value=float(0), format=("%f"))
        farm_plang = st.number_input(label="จำนวนพื้นที่(แปลง)", min_value=float(0), format=("%f"))
    seedling_quantity = st.number_input(label="จำนวนต้นกล้า", min_value=int(0), format=("%d"))
    crop_details_check = crop_details_duplicate()
    duplicate_crop_details_check = True
    for rows in crop_details_check:
        condition_duplicate = (str(rows[0]) +  str(rows[1]) == str(crop_selected[0]) + str(farmer_selected[0]))
        if condition_duplicate == True:
            duplicate_crop_details_check = False
    if st.button(label="เพิ่มข้อมูล"):
        if duplicate_crop_details_check == True:
            created_at = timestamp()
            updated_at = created_at
            crop_details_tb_insert(crop_selected[0], farmer_selected[0], farm_rai, farm_building, farm_ngan, farm_plang, seedling_quantity, created_at, updated_at)
            st.success("เพิ่มข้อมูลสำเร็จ!")
            time.sleep(1.5)
            st.experimental_rerun()
        else:
            st.error("ข้อมูลคุณ {} {} ({}) ในแผน{} ({}) ครอปที่ {} ถูกเพิ่มไว้แล้ว ไปที่เมนูแก้ไข".format(farmer_selected[2],farmer_selected[3],farmer_selected[4],crop_selected[1],crop_selected[2],crop_selected[3]))

def update_page():
    crop_options = crops_options_select()
    crop_selected = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย", options=crop_options, format_func=lambda crop_options: "แผน{} ({}) ครอปที่ {}".format(crop_options[1],crop_options[2],crop_options[3]), key=("edit_plan_optins"))
    update_options = crop_details_tb_select(crop_selected[0])
    farmer_selected = st.selectbox(label="รหัสเกษตรกร", options=update_options, format_func=lambda update_options: "{}: {} {} ({})".format(update_options[1],update_options[2],update_options[3],update_options[4]), key=("edit_farmer_options"))
    col1, col2 = st.columns([2, 2])
    if farmer_selected is None:
        with col1:
            farm_rai = st.number_input(label="จำนวนพื้นที่(ไร่)", min_value=float(0), key=("update_farm_rai"), disabled=True)
            farm_building = st.number_input(label="จำนวนพื้นที่(โรงเรือน)", min_value=int(0), step=1,
                                            key=("update_farm_building"), disabled=True)
        with col2:
            farm_ngan = st.number_input(label="จำนวนพื้นที่(งาน)", min_value=float(0), key=("update_farm_ngan"), disabled=True)
            farm_plang = st.number_input(label="จำนวนพื้นที่(แปลง)", min_value=float(0), key=("update_farm_plang"), disabled=True)
        seedling_quantity = st.number_input(label="จำนวนต้นกล้า", min_value=int(0), key=("update_seedling_quantity"), format=("%d"), disabled=True)
    else:
        with col1:
            farm_rai = st.number_input(label="จำนวนพื้นที่(ไร่)", min_value=float(0), format=("%f"), key=("update_farm_rai"), value=float(farmer_selected[5]))
            farm_building = st.number_input(label="จำนวนพื้นที่(โรงเรือน)", min_value=int(0), step=1, format=("%d"),
                                            key=("update_farm_building"), value=int(farmer_selected[7]))
        with col2:
            farm_ngan = st.number_input(label="จำนวนพื้นที่(งาน)", min_value=float(0), format=("%f"), key=("update_farm_ngan"), value=float(farmer_selected[6]))
            farm_plang = st.number_input(label="จำนวนพื้นที่(แปลง)", min_value=float(0), format=("%f"), key=("update_farm_plang"), value=float(farmer_selected[8]))
        seedling_quantity = st.number_input(label="จำนวนต้นกล้า", min_value=int(0), format=("%d"), key=("update_seedling_quantity"), value=int(farmer_selected[9]))
        st.markdown("""---""")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked:
            updated_at = timestamp()
            st.success("แก้ไขข้อมูลสำเร็จ!")
            crop_details_tb_update(farmer_selected[0], farmer_selected[1], farm_rai, farm_building, farm_ngan, farm_plang, seedling_quantity,
                                   updated_at)
            time.sleep(1.5)
            st.experimental_rerun()
        elif delete_button_clicked:
            crop_details_tb_delete(farmer_selected[0], farmer_selected[1])
            st.error("ลบข้อมูลสำเร็จ!")
            time.sleep(1.5)
            # pyautogui.hotkey("ctrl", "F5")
            st.experimental_rerun()
def select_page():
    crop_options = crops_options_select()
    crop_selected = st.selectbox(label="รหัสแผนการเพาะปลูกโดยย่อย", options=crop_options,
                                 format_func=lambda crop_options: "แผน{} ({}) ครอปที่ {}".format(crop_options[1],
                                                                                                 crop_options[2],
                                                                                                 crop_options[3]),
                                 key=("plan_options"))
    data = crop_details_tb_select(crop_selected[0])
    # st.write(data)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.title("{}.".format(n))
        with col2:
            st.text("รหัสเกษตรกร: {}".format(i[4]))
            st.text("ชื่อ: {}".format(i[2]))
            st.text("พื้นที่: {} งาน".format(i[6]))
            st.text("พื้นที่: {} แปลง".format(i[8]))
            st.text("จำนวนต้นกล้า: {:,} ต้น".format(i[9]))
        with col3:
            st.markdown("# ")
            st.text("นามสกุล: {}".format(i[3]))
            st.text("พื้นที่: {} ไร่".format(i[5]))
            st.text("พื้นที่: {} โรงเรือน".format(i[7]))
        st.markdown("""---""")
        n += 1

main()
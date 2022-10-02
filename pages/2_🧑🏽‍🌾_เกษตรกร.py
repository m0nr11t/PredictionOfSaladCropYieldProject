import streamlit as st
# import pyautogui
import time
from calculate import prename_transform,timestamp,load_image
from sql_execute import farmers_tb_insert,farmers_tb_select,tb_select_pil,farmers_tb_update, farmers_tb_delete

st.set_page_config(
    page_title="ป่าแป๋-ทะเบียนเกษตรกร",
    page_icon="🕴"
)

def main():
    st.subheader("ทะเบียนเกษตรกร🧑‍🌾")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page();
    with create_page_tab:
        create_page();
    with update_page_tab:
        update_page();

def create_page():
    with st.form("farmers_form",clear_on_submit=True):
        st.markdown("##### ข้อมูลส่วนตัว")
        prename = st.radio(label="คำนำหน้า",options=("นาย","นาง","นางสาว"),horizontal=True, key="prename")
        col1, col2 = st.columns([2,2])
        with col1:
            firstname = st.text_input(label="ชื่อ",key="name")
            farmer_gov_id = st.text_input(label="รหัสเกษตรกร", max_chars=8, key="farmer_gov_id")
            tel = st.text_input(label="เบอร์โทรศัพท์", max_chars=10, key="tel")
        with col2:
            lastname = st.text_input(label="นามสกุล", key="lastname")
            gov_id = st.text_input(label="รหัสประชาชน",max_chars=13, key="gov_id")
        st.markdown("##### ข้อมูลที่อยู่")
        col1, col2 = st.columns([2, 2])
        with col1:
            house_no = st.text_input(label="เลขที่บ้าน", max_chars=6, key="house_no")
            vil_name = st.text_input(label="ชื่อหมู่บ้าน", key="vil_name")
            district_name = st.text_input(label="ชื่ออำเภอ", key="district_name")
            postcode = st.text_input(label="รหัสไปรษณีย์", max_chars=5, key="postcode")
        with col2:
            vil_no = st.text_input(label="เลขที่หมู่", max_chars=2, key="vil_no")
            subdistrict_name = st.text_input(label="ชื่อตำบล", key="subdistrict_name")
            province_name = st.text_input(label="ชื่อจังหวัด", key="province")
        st.markdown("##### ข้อมูลที่อยู่แปลง")
        col_left, col_right = st.columns([1, 1])
        with col_left:
            farm_vil_no = st.text_input(label="เลขที่หมู่", max_chars=2, key="farm_vil_no")
            farm_subdistrict_name = st.text_input(label="ชื่อตำบล", key="farm_subdistrict_name")
            farm_province_name = st.text_input(label="ชื่อจังหวัด", key="farm_province_name")
        with col_right:
            farm_vil_name = st.text_input(label="ชื่อหมู่บ้าน", key="farm_vil_name")
            farm_district_name = st.text_input(label="ชื่ออำเภอ", key="farm_district_name")
        st.markdown("##### ข้อมูลคุณสมบัติแปลง")
        col_left, col_center, col_right = st.columns([1, 1, 1])
        with col_left:
            farm_geo_x = st.text_input(label="พิกัดแกน X", key="farm_geo_x")
        with col_center:
            farm_geo_y = st.text_input(label="พิกัดแกน Y", key="farm_geo_y")
        with col_right:
            farm_geo_z = st.text_input(label="พิกัดแกน Z", key="farm_geo_z")
        farm_land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน", key="farm_land_privileges")
        farm_soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", value=False, key="farm_soil_analysis")
        farm_water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", value=False, key="farm_water_analysis")
        farm_gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", value=False, key="farm_gap_analysis")
        image_file = st.file_uploader(label="แนบไฟล์รูป:", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
        if image_file is not None:
            image_file = load_image(image_file)
        else:
            image_file = load_image('none.png')
        st.markdown("""---""")
        col1, col_center, col3 = st.columns([2, 1, 2])
        with col_center:
            submit_button_clicked = st.form_submit_button(label="เพิ่มข้อมูล")
        if submit_button_clicked:
            created_at = timestamp()
            updated_at = created_at
            farmers_tb_insert(prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                             image_file , farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, created_at, updated_at)
            st.success("เพิ่มข้อมูลสำเร็จ!")
            time.sleep(1.5)
            st.experimental_rerun()

def update_page():
    update_page_options = farmers_tb_select()
    farmer_selected = st.selectbox("กรุณาเลือกเกษตรกร", options=update_page_options, format_func=lambda update_page_options: "{:03d}: {} {} ({})".format(update_page_options[0],update_page_options[2],update_page_options[3],update_page_options[4]))
    table_name = ("farmers")
    pk = ("farmer_id")
    img,row = tb_select_pil(table_name, pk, farmer_selected[0], outfile=None)
    image_before = row
    col_left, col_center, col_right = st.columns([1,1,1])
    with col_center:
        st.image(img, width=250)
    prename_index = prename_transform(farmer_selected[1])
    if farmer_selected:
        st.markdown("##### ข้อมูลส่วนตัว")
        prename = st.radio(label="คำนำหน้า",index=prename_index, options=("นาย", "นาง", "นางสาว"), horizontal=True, key="edit_prename")
        col1, col2 = st.columns([2, 2])
        with col1:
            firstname = st.text_input(label="ชื่อ", key="edit_name",value=farmer_selected[2])
            farmer_gov_id = st.text_input(label="รหัสเกษตรกร", max_chars=8, key="edit_farmer_gov_id",value=farmer_selected[4])
            tel = st.text_input(label="เบอร์โทรศัพท์", max_chars=10, key="edit_tel",value=farmer_selected[6])
        with col2:
            lastname = st.text_input(label="นามสกุล", key="edit_lastname",value=farmer_selected[3])
            gov_id = st.text_input(label="รหัสประชาชน", max_chars=13, key="edit_gov_id",value=farmer_selected[5])
        st.markdown("##### ข้อมูลที่อยู่")
        col1, col2 = st.columns([2, 2])
        with col1:
            house_no = st.text_input(label="เลขที่บ้าน", max_chars=6, key="edit_house_no",value=farmer_selected[7])
            vil_name = st.text_input(label="ชื่อหมู่บ้าน", key="edit_vil_name",value=farmer_selected[9])
            district_name = st.text_input(label="ชื่ออำเภอ", key="edit_district_name",value=farmer_selected[11])
            postcode = st.text_input(label="รหัสไปรษณีย์", max_chars=5, key="edit_postcode",value=farmer_selected[13])
        with col2:
            vil_no = st.text_input(label="เลขที่หมู่", max_chars=2, key="edit_vil_no",value=farmer_selected[8])
            subdistrict_name = st.text_input(label="ชื่อตำบล", key="edit_subdistrict_name",value=farmer_selected[10])
            province_name = st.text_input(label="ชื่อจังหวัด", key="edit_province",value=farmer_selected[12])
        st.markdown("##### ข้อมูลที่อยู่แปลง")
        col_left, col_right = st.columns([1, 1])
        with col_left:
            farm_vil_no = st.text_input(label="เลขที่หมู่", max_chars=2, key="edit_farm_vil_no",value=farmer_selected[14])
            farm_subdistrict_name = st.text_input(label="ชื่อตำบล", key="edit_farm_subdistrict_name",value=farmer_selected[16])
            farm_province_name = st.text_input(label="ชื่อจังหวัด", key="edit_farm_province_name",value=farmer_selected[18])
        with col_right:
            farm_vil_name = st.text_input(label="ชื่อหมู่บ้าน", key="edit_farm_vil_name",value=farmer_selected[15])
            farm_district_name = st.text_input(label="ชื่ออำเภอ", key="edit_farm_district_name",value=farmer_selected[17])
        st.markdown("##### ข้อมูลคุณสมบัติแปลง")
        col_left, col_center, col_right = st.columns([1, 1, 1])
        with col_left:
            farm_geo_x = st.text_input(label="พิกัดแกน X", key="edit_farm_geo_x",value=farmer_selected[19])
        with col_center:
            farm_geo_y = st.text_input(label="พิกัดแกน Y", key="edit_farm_geo_y",value=farmer_selected[20])
        with col_right:
            farm_geo_z = st.text_input(label="พิกัดแกน Z", key="edit_farm_geo_z",value=farmer_selected[21])
        farm_land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน", key="edit_farm_land_privileges",value=farmer_selected[22])
        farm_soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", key="edit_farm_soil_analysis",value=farmer_selected[23])
        farm_water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", key="edit_farm_water_analysis",value=farmer_selected[24])
        farm_gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", key="edit_farm_gap_analysis",value=farmer_selected[25])
        image_file_after = st.file_uploader(label="แก้ไขรูป", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
        if image_file_after is not None:
            image_file = load_image(image_file_after)
        else:
            image_file = image_before
        st.markdown("""---""")
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked==True:
            updated_at = timestamp()
            farmers_tb_update(prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name,
                                  subdistrict_name, district_name, province_name, postcode,
                                  image_file, farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name,
                                  farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                                  farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis,
                                  updated_at, farmer_selected[0])
            st.success("แก้ไขข้อมูลสำเร็จ! {} {} {}".format(prename, firstname, lastname))
            time.sleep(1.5)
            st.experimental_rerun()
        elif delete_button_clicked==True:
            farmers_tb_delete(farmer_selected[0])
            st.error("ลบข้อมูลสำเร็จ!")
            time.sleep(1.5)
            # pyautogui.hotkey("ctrl", "F5")
            st.experimental_rerun()

def select_page():
    a = [1,"นาย","ทดสอบชื่อ","ทดสอบนามสกุล","12345678","1234567890123","0881234567","798/12","12","ทดสอบชื่อหมู่บ้าน",
         "ทดสอบชื่อตำบล","ทดสอบชื่ออำเภอ","ทดสอบชื่อจังหวัด","50300"]
    b = [2,"นาง","ทดสอบชื่อ","ทดสอบนามสกุล","12345678","1234567890123","0881234567","798/12","12","ทดสอบชื่อหมู่บ้าน",
         "ทดสอบชื่อตำบล","ทดสอบชื่ออำเภอ","ทดสอบชื่อจังหวัด","50300"]
    data = (a, b)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1,2,2])
        with col1:
            st.title("{}. {:03d}".format(n,i[0]))
        with col2:
            st.caption("ข้อมูลส่วนตัว")
            st.text("รหัสเกษตรกร: {}".format(i[4]))
            st.text("ชื่อ: {}".format(i[2]))
            st.text("เบอร์โทรศัพท์: {}".format(i[6]))
            st.caption("ข้อมูลที่อยู่")
            st.text("ที่อยู่: {} หมู่ที่ {}".format(i[7],i[8]))
            st.text("ตำบล: {}".format(i[10]))
            st.text("จังหวัด: {}".format(i[12]))
        with col3:
            st.caption(".")
            st.text("คำนำหน้า: {}".format(i[1]))
            st.text("นามสกุล: {}".format(i[3]))
            st.text("รหัสประชาชน: {}".format(i[5]))
            st.caption(".")
            st.text("หมู่บ้าน: {}".format(i[9]))
            st.text("อำเภอ: {}".format(i[11]))
        st.markdown("""---""")
        n+=1

main();
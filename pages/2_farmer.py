import streamlit as st
import pyautogui
from calculate import prename_transform,timestamp
from sql_execute import farmer_tb_insert,farm_tb_select

st.set_page_config(
    page_title="ป่าแป๋-ทะเบียนเกษตรกร",
    page_icon="🕴"
)

def main():
    st.title("ทะเบียนเกษตรกร🧑‍🌾")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page();
    with create_page_tab:
        create_page();
    with update_page_tab:
        update_page();

def create_page():
    with st.form("farmer_form",clear_on_submit=True):
        st.subheader("ข้อมูลส่วนตัว")
        prename = st.radio(label="คำนำหน้า",options=("นาย","นาง","นางสาว"),horizontal=True, key="prename")
        col1, col2 = st.columns([2,2])
        with col1:
            firstname = st.text_input(label="ชื่อ",key="name")
            farmer_gov_id = st.text_input(label="รหัสเกษตรกร", max_chars=8, key="farmer_gov_id")
            tel = st.text_input(label="เบอร์โทรศัพท์", max_chars=10, key="tel")
        with col2:
            lastname = st.text_input(label="นามสกุล", key="lastname")
            gov_id = st.text_input(label="รหัสประชาชน",max_chars=13, key="gov_id")
        st.subheader("ข้อมูลที่อยู่")
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
        st.subheader("ข้อมูลที่อยู่แปลง")
        col_left, col_right = st.columns([1, 1])
        with col_left:
            vil_no = st.text_input(label="เลขที่หมู่", max_chars=2, key="farm_vil_no")
            subdistrict_name = st.text_input(label="ชื่อตำบล", key="farm_subdistrict_name")
            province_name = st.text_input(label="ชื่อจังหวัด", key="farm_province_name")
        with col_right:
            vil_name = st.text_input(label="ชื่อหมู่บ้าน", key="farm_vil_name")
            district_name = st.text_input(label="ชื่ออำเภอ", key="farm_district_name")
        st.subheader("ข้อมูลคุณสมบัติแปลง")
        col_left, col_center, col_right = st.columns([1, 1, 1])
        with col_left:
            geo_x = st.text_input(label="พิกัดแกน X", key="farm_geo_x")
        with col_center:
            geo_y = st.text_input(label="พิกัดแกน Y", key="farm_geo_y")
        with col_right:
            geo_z = st.text_input(label="พิกัดแกน Z", key="farm_geo_z")
        land_privileges = st.text_input(label="สิทธิประโยชน์การใช้ที่ดิน", key="farm_land_privileges")
        soil_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์ดินแล้ว", value=False, key="farm_soil_analysis")
        water_analysis = st.checkbox("ได้รับการตรวจวิเคราะห์น้ำแล้ว", value=False, key="farm_water_analysis")
        gap_analysis = st.checkbox("ได้ผ่านการรับรองระบบ GAP แล้ว", value=False, key="farm_gap_analysis")
        st.markdown("""---""")
        created_at = timestamp()
        updated_at = created_at
        col1, col_center, col3 = st.columns([2, 1, 2])
        with col_center:
            submit_button_clicked = st.form_submit_button(label="เพิ่มข้อมูล")
        if submit_button_clicked:
            farmer_tb_insert(vil_name, district_name, vil_no, subdistrict_name, province_name, geo_x, geo_y, geo_z,
                           land_privileges, soil_analysis, water_analysis, gap_analysis, created_at, updated_at)
            st.success("เพิ่มข้อมูลสำเร็จ!")

def update_page():
    a = [1,"นาย","ทดสอบชื่อ","ทดสอบนามสกุล","12345678","1234567890123","0881234567","798/12","12","ทดสอบชื่อหมู่บ้าน",
         "ทดสอบชื่อตำบล","ทดสอบชื่ออำเภอ","ทดสอบชื่อจังหวัด","50300"]
    b = [1,"นาง","ทดสอบชื่อ","ทดสอบนามสกุล","12345678","1234567890123","0881234567","798/12","12","ทดสอบชื่อหมู่บ้าน",
         "ทดสอบชื่อตำบล","ทดสอบชื่ออำเภอ","ทดสอบชื่อจังหวัด","50300"]
    # st.write(a,b)
    update_page_options = (a,b)
    farmer_selected = st.selectbox("กรุณาเลือกเกษตรกร", options=update_page_options)
    farmer_selected = prename_transform(farmer_selected)
    if farmer_selected:
        st.subheader("ข้อมูลส่วนตัว")
        prename = st.radio(label="คำนำหน้า", index=farmer_selected[1], options=("นาย", "นาง", "นางสาว"), horizontal=True)
        col1, col2 = st.columns([2,2])
        with col1:
            firstname = st.text_input(label="ชื่อ", value=farmer_selected[2])
            farmer_gov_id = st.text_input(label="รหัสเกษตรกร", value=farmer_selected[4], max_chars=8)
            tel = st.text_input(label="เบอร์โทรศัพท์", value=farmer_selected[6], max_chars=10)
        with col2:
            lastname = st.text_input(label="นามสกุล", value=farmer_selected[3])
            gov_id = st.text_input(label="รหัสประชาชน", value=farmer_selected[5], max_chars=13)
        st.subheader("ข้อมูลที่อยู่")
        col1, col2 = st.columns([2, 2])
        with col1:
            house_no = st.text_input(label="เลขที่บ้าน", value=farmer_selected[7], max_chars=6)
            vil_name = st.text_input(label="ชื่อหมู่บ้าน", value=farmer_selected[9])
            district_name = st.text_input(label="ชื่ออำเภอ", value=farmer_selected[11])
            postcode = st.text_input(label="รหัสไปรษณีย์", value=farmer_selected[13], max_chars=5)
        with col2:
            vil_no = st.text_input(label="เลขที่หมู่", value=farmer_selected[8], max_chars=2)
            subdistrict_name = st.text_input(label="ชื่อตำบล", value=farmer_selected[10])
            province_name = st.text_input(label="ชื่อจังหวัด", value=farmer_selected[12])
        st.markdown("""---""")
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        with col2:
            edit_button_clicked = st.button(label="แก้ไขข้อมูล")
        with col4:
            delete_button_clicked = st.button(label="ลบข้อมูล")
        if edit_button_clicked==True:
            st.success("แก้ไขข้อมูลสำเร็จ! {} {} {}".format(prename, firstname, lastname))
        elif delete_button_clicked==True:
            st.error("ลบข้อมูลสำเร็จ!")
            pyautogui.hotkey("ctrl", "F5")

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
import streamlit as st
from calculate import timestamp
from sql_execute import variable_tb_insert, variable_create_columns

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.title("Configuration Page")
def main():
    with st.expander(label="สร้างฟิลด์ตัวแปรในตารางตัวแปรอิสระเพิ่มเติม"):
        with st.form(key="indepentdent_add"):
            columns_table_name = ('independent_variables')
            columns_name = st.text_input(label="ชื่อตัวฟิลด์ภาษาอังกฤษ",help="1.ต้องเป็นตัวอักษรภาษาอังกฤษเท่านั้น \n 2.ห้ามมีอักขระพิเศษอื่นใด \n 3.ห้ามเป็นคำต้องห้าม SQL")
            columns_alias = st.text_input(label="ชื่อตัวฟิลด์ภาษาไทย")
            columns_datatype = st.selectbox(label="ชนิดข้อมูล", options=("double precision","smallint"),index=1)
            columns_cal = st.selectbox(label="การคำนวณข้อมูลภายในฟิลด์", options=("SUM", "MAX", "MIN", "AVG", "COUNT"), index=1)
            created_at = timestamp()
            col_left,col_center,col_right = st.columns([2,1,2])
            with col_center:
                submit_clicked = st.form_submit_button("ยืนยัน")
            if submit_clicked:
                variable_tb_insert(columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name)
                variable_create_columns(columns_table_name, columns_name, columns_datatype)
                st.success("เพิ่มข้อมูล ฟิลด์{} สำเร็จ!".format(columns_alias))

    with st.expander(label="สร้างฟิลด์ตัวแปรในตารางรายละเอียดการเพาะปลูกเพิ่มเติม"):
        with st.form(key="crop_details_add"):
            columns_table_name = ("crop_details")
            columns_name = st.text_input(label="ชื่อตัวฟิลด์ภาษาอังกฤษ",help="1.ต้องเป็นตัวอักษรภาษาอังกฤษเท่านั้น \n 2.ห้ามมีอักขระพิเศษอื่นใด \n 3.ห้ามเป็นคำต้องห้าม SQL")
            columns_alias = st.text_input(label="ชื่อตัวฟิลด์ภาษาไทย")
            columns_datatype = st.selectbox(label="ชนิดข้อมูล", options=("double precision","smallint"),index=1)
            columns_cal = st.selectbox(label="การคำนวณข้อมูลภายในฟิลด์", options=("SUM", "MAX", "MIN", "AVG", "COUNT"), index=1)
            created_at = timestamp()
            col_left,col_center,col_right = st.columns([2,1,2])
            with col_center:
                submit_clicked = st.form_submit_button("ยืนยัน")
            if submit_clicked:
                variable_tb_insert(columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name)
                variable_create_columns(columns_table_name, columns_name, columns_datatype)
                st.success("เพิ่มข้อมูล ฟิลด์{} สำเร็จ!".format(columns_alias))


main()
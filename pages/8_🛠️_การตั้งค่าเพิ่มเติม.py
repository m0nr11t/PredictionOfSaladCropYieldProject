import pandas as pd
import streamlit as st
from calculate import timestamp
from sql_execute import variable_tb_insert, variable_create_columns,download,download_columns
import datetime
st.set_page_config(
    page_title="การตั้งค่าเพิ่มเติม",
    page_icon="🛠️",
)

st.subheader("การตั้งค่าเพิ่มเติม 🛠️")
def main():
    expander_independent_variables_field_add()
    expander_crop_details_field_add()
    # expander_crop_detail_products_field_add()
    download_data()



def expander_independent_variables_field_add():
    with st.expander(label="สร้างฟิลด์ตัวแปรในตารางตัวแปรอิสระเพิ่มเติม"):
        with st.form(key="indepentdent_add"):
            col1,col2 = st.columns([1,1])
            columns_table_name = ('independent_variables')
            with col1:
                columns_name = st.text_input(label="ชื่อตัวฟิลด์ภาษาอังกฤษ",help="1.ต้องเป็นตัวอักษรภาษาอังกฤษเท่านั้น \n 2.ห้ามมีอักขระพิเศษอื่นใด \n 3.ห้ามเป็นคำต้องห้าม SQL")
            with col2:
                columns_alias = st.text_input(label="ชื่อตัวฟิลด์ภาษาไทย")
            with col1:
                columns_datatype = st.selectbox(label="ชนิดข้อมูล", options=("double precision","integer"),index=1)
            with col2:
                columns_cal = st.selectbox(label="การคำนวณข้อมูลภายในฟิลด์", options=("SUM", "MAX", "MIN", "AVG", "COUNT"), index=1)
            created_at = timestamp()
            col_left,col_center,col_right = st.columns([5,1,5])
            with col_center:
                submit_clicked = st.form_submit_button("ยืนยัน")
            if submit_clicked:
                variable_tb_insert(columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name)
                variable_create_columns(columns_table_name, columns_name, columns_datatype)
                st.success("เพิ่มข้อมูล ฟิลด์{} สำเร็จ!".format(columns_alias))

def expander_crop_details_field_add():
    with st.expander(label="สร้างฟิลด์ตัวแปรในตารางรายละเอียดการเพาะปลูกเพิ่มเติม"):
        with st.form(key="crop_details_add"):
            columns_table_name = ("crop_details")
            col1, col2 = st.columns([1, 1])
            with col1:
                columns_name = st.text_input(label="ชื่อตัวฟิลด์ภาษาอังกฤษ",
                                             help="1.ต้องเป็นตัวอักษรภาษาอังกฤษเท่านั้น \n 2.ห้ามมีอักขระพิเศษอื่นใด \n 3.ห้ามเป็นคำต้องห้าม SQL")
            with col2:
                columns_alias = st.text_input(label="ชื่อตัวฟิลด์ภาษาไทย")
            with col1:
                columns_datatype = st.selectbox(label="ชนิดข้อมูล", options=("double precision", "integer"), index=1)
            with col2:
                columns_cal = st.selectbox(label="การคำนวณข้อมูลภายในฟิลด์",
                                           options=("SUM", "MAX", "MIN", "AVG", "COUNT"), index=1)
            created_at = timestamp()
            col_left,col_center,col_right = st.columns([2,1,2])
            with col_center:
                submit_clicked = st.form_submit_button("ยืนยัน")
            if submit_clicked:
                variable_tb_insert(columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name)
                variable_create_columns(columns_table_name, columns_name, columns_datatype)
                st.success("เพิ่มข้อมูล ฟิลด์{} สำเร็จ!".format(columns_alias))

def download_data():
    with st.expander("ดาวน์โหลดข้อมูล"):
        download_options = [['พืช','plants'],['แผน','plans'],['ปัจจัยอิสระรายวัน','independent_variables'],['เกษตรกร','farmers'],['แผนการเพาะปลูกย่อย','crops'],['รายละเอียดการเพาะปลูก','crop_details'],['ผลผลิตการเก็บเกี่ยว','crop_detail_products']]
        download_selected = st.selectbox("ตารางที่ต้องการดาวน์โหลดข้อมูล",options=download_options,format_func=lambda download_options:"{}".format(download_options[0]))
        dt = download(download_selected[1])
        col = download_columns(download_selected[1])
        df = pd.DataFrame(dt,columns=col)
        csv = df.to_csv().encode('utf-8')
        timenow = datetime.datetime.now()
        Date = timenow.strftime('%Y-%m-%d')
        st.download_button(
            label="ดาวน์โหลด",
            data=csv,
            file_name='{}_{}.csv'.format(download_selected[1],Date),
            mime='text/csv',
        )
main()
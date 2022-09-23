import streamlit as st
import time
import pyautogui
from calculate import timestamp
from sql_execute import table_details_select,independent_variable_details_by_crop_select,sql_crop_details_by_crop_argument


def main():

    data = independent_variable_details_by_crop_select()
    st.table(data)
    st.subheader("ข้อมูลสรุปตัวแปรอิสระ (รายครอป)🌦️")
    select_page(data)

def select_page(data):
    data
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.title("{}. {:03d}".format(n, i[0]))
            pass
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

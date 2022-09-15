import streamlit as st
st.title("ข้อมูลการพยากรณ์🌦️")
with st.form("forecast_form",clear_on_submit=True):
    # temp_avg = st.number_input(label="อุณหภูมิเฉลี่ย")
    temp_max = st.number_input(label="อุณหภูมิสูงสุด")
    temp_min = st.number_input(label="อุณหภูมิต่ำสุด")
    farmer_number = st.number_input(label="จำนวนเกษตรกร",min_value=0,step=1)
    # humin_avg = st.number_input(label="ความชื้นเฉลี่ย")
    # humin_max = st.number_input(label="ความชื้นสูงสุด")
    # humin_min = st.number_input(label="ความชื้นต่ำสุด")
    # rain = st.number_input(label="ปริมาณน้ำฝน")
    # win_avg = st.number_input(label="ความเร็วลมเฉลี่ย")
    # win_max = st.number_input(label="ความเร็วลมสูงสุด")
    # win_min = st.number_input(label="ความเร็วลมต่ำสุด")
    weight = st.number_input(label="น้ำหนักหลังตัดแต่ง")
    if st.form_submit_button(label="เพิ่มข้อมูล"):
        st.success("เพิ่มข้อมูลสำเร็จ!")
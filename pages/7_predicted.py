import streamlit as st
st.title("ข้อมูลการพยากรณ์🌦️")
with st.form("forecast_form",clear_on_submit=True):
    # temp_avg = st.number_input(label="อุณหภูมิเฉลี่ย",min_value=0.00)
    temp_max = st.number_input(label="อุณหภูมิสูงสุด",min_value=0.00)
    temp_min = st.number_input(label="อุณหภูมิต่ำสุด",min_value=0.00)
    farmer_number = st.number_input(label="จำนวนเกษตรกร",min_value=0,step=1)
    # humin_avg = st.number_input(label="ความชื้นเฉลี่ย",min_value=0.00)
    # humin_max = st.number_input(label="ความชื้นสูงสุด",min_value=0.00)
    # humin_min = st.number_input(label="ความชื้นต่ำสุด",min_value=0.00)
    # rain = st.number_input(label="ปริมาณน้ำฝน",min_value=0.00)
    # win_avg = st.number_input(label="ความเร็วลมเฉลี่ย",min_value=0.00)
    # win_max = st.number_input(label="ความเร็วลมสูงสุด",min_value=0.00)
    # win_min = st.number_input(label="ความเร็วลมต่ำสุด",min_value=0.00)
    weight = st.number_input(label="น้ำหนักหลังตัดแต่ง",min_value=0.00)
    if st.form_submit_button(label="เพิ่มข้อมูล"):
        st.success("เพิ่มข้อมูลสำเร็จ!")
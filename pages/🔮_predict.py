import pandas as pd
import streamlit as st
import pickle
from sql_execute import models_tb_options,models_tb_select
st.set_page_config(
    page_title="การพยากรณ์",
    page_icon="🔮",
    layout="wide"
)
def main():
    st.subheader("การพยากรณ์ (Prediction)🔮")
    model_options = models_tb_options()
    model_selected = st.selectbox("โปรดเลือกแบบจำลอง:",options=model_options,format_func=lambda model_options:"{}".format(model_options[2]))
    model_dt = models_tb_select(model_selected[0])
    model = pickle.loads(model_dt[2])
    predicted = model.predict([[2]])
    st.write(predicted[0])
    st.write("ปริมา {}".format(model_selected[2]))

main()

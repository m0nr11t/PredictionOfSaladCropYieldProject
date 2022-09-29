import pandas as pd
import streamlit as st
import pickle
from sql_execute import models_tb_options,models_tb_select,crop_can_predict_options,predict_arguments,\
columns_name_independent_weather,columns_name_independent_crop
from calculate import transform_colname_th_en,columns_name_for_predicted
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
    model_id = model_dt[0]
    plant_id = model_dt[1]
    model = pickle.loads(model_dt[2])
    model_var = model_dt[3]
    model_coef = model_dt[4]
    model_intercept = model_dt[5]
    model_name = model_dt[6]
    crop_predict_options = crop_can_predict_options(model_selected[1])
    crop_predict_selected = st.selectbox("โปรดเลือกครอปที่ต้องการพยากรณ์",options=crop_predict_options,format_func=lambda crop_predict_options:"ปี {} ครอปที่ {}".format(crop_predict_options[2],crop_predict_options[4]))
    model_var_en = transform_colname_th_en(model_dt[3]).values.tolist()
    model_argument_values = predict_arguments(crop_predict_selected[3],model_var_en)
    columns_independent_weather = columns_name_independent_weather()
    columns_independent_crop = columns_name_independent_crop()
    columns_name = columns_name_for_predicted(columns_independent_weather, columns_independent_crop)
    dt_all = pd.DataFrame(model_argument_values,columns=columns_name)
    st.write(dt_all[model_var])
    st.write(model_var)
    predicted = model.predict([[2]])
    # st.write(pd.DataFrame(model_dt[3]))
    st.write("ปริมาณ {}".format(model_selected[2]))

main()

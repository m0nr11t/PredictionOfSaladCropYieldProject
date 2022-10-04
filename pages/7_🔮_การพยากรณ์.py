import pandas as pd
import streamlit as st
import pickle
from sql_execute import models_tb_options,models_tb_select,crop_can_predict_options,predict_arguments,\
columns_name_independent_weather,columns_name_independent_crop
from calculate import transform_colname_th_en,columns_name_for_predicted,solve
st.set_page_config(
    page_title="การพยากรณ์",
    page_icon="🔮",
)
def main():
    st.subheader("การพยากรณ์ (Prediction)🔮")
    col1, col2 = st.columns([1, 1])
    with col1:
        model_options = models_tb_options()
        model_selected = st.selectbox("1️⃣เลือกแบบจำลอง:",options=model_options,format_func=lambda model_options:"{}".format(model_options[2]))
        model_dt = models_tb_select(model_selected[0])
        model_id = model_dt[0]
        plant_id = model_dt[1]
        model = pickle.loads(model_dt[2])
        model_var = model_dt[3]
        model_coef = model_dt[4]
        model_intercept = model_dt[5]
        model_name = model_dt[6]
        model_rmse = model_dt[7]
        model_r2 = model_dt[8]
    with col2:
        crop_predict_options = crop_can_predict_options(model_selected[1])
        crop_predict_selected = st.selectbox("2️⃣เลือกครอปที่ต้องการพยากรณ์:",options=crop_predict_options,format_func=lambda crop_predict_options:"ปี {} ครอปที่ {}".format(crop_predict_options[2],crop_predict_options[4]))
    model_var_en = transform_colname_th_en(model_dt[3]).values.tolist()
    model_argument_values = predict_arguments(crop_predict_selected[3],model_var_en)
    columns_independent_weather = columns_name_independent_weather()
    columns_independent_crop = columns_name_independent_crop()
    columns_name = columns_name_for_predicted(columns_independent_weather, columns_independent_crop)
    all_arguments = pd.DataFrame(model_argument_values,columns=columns_name,dtype=('float64'))
    model_arguments = all_arguments[model_var]
    if model_arguments.empty is True:
        st.error("ระบบไม่สามารถทำการพยากรณ์ได้ เนื่องจากข้อมูลตัวแปรอิสระน้อยจนเกินไป 😿")
    else:
        with st.expander("ความหมายแบบจำลอง"):
            predicted = model.predict(model_arguments)
        col1,col2 = st.columns([1,1])
        with col1:
            st.markdown("🧙🏽‍♂️**คาดว่าจะได้รับปริมาณผลผลิต** {:.02f} กก.".format(predicted[0]))
            st.caption("**โมเดลนี้มีความคลาดเคลื่อน {:.02f} กิโลกรัม".format(model_rmse))
        with col2:
            st.markdown("**ข้อมูลแผนการเก็บเกี่ยว**🥦")
            st.text("🌱 พืช: {}".format(crop_predict_selected[1]))
            st.text("🌰 แผนปีที่: {}".format(crop_predict_selected[2]))
            st.text("👩🏽‍🌾 ครอปที่: {}".format(crop_predict_selected[4]))
            st.text("📆 วันที่เริ่มต้น: {}".format(crop_predict_selected[6].strftime("%d %B %Y")))
            st.text("📆 วันที่ย้ายการปลูก: {}".format(crop_predict_selected[7].strftime("%d %B %Y")))
            st.text("📆 วันที่สิ้นสุดการปลูก: {}".format(crop_predict_selected[8].strftime("%d %B %Y")))
        with st.expander("ดูข้อมูลเพิ่มเติม..."):
            coefficent_x_var = ("")
            n=0
            for coef_var in (model_coef):
                # st.write(coef_var[0],model_var[n])
                co = coef_var[0]
                if coef_var[0] >= 0:
                    co = str("+") + str(round(coef_var[0], 3))
                else:
                    co = round(co, 3)
                coefficent_x_var = str(co) + str("(") + str(model_var[n]) + str(")") + str(coefficent_x_var)
                n += 1
            st.markdown("**รูปสมการ:**")
            st.text("""ปริมาณผลผลิต = {:.3f} {}""".format(model_intercept, coefficent_x_var))
            if st.checkbox("👈🏽ดูข้อมูล",value=False):
                st.write(model_arguments)
            st.markdown("**อธิบายได้ว่า**")
            n=0
            for coef_var in model_coef:
                if coef_var[0] >= 0:
                    st.text("{}. เมื่อ{}เพิ่มขึ้น 1 หน่วย ส่งผลให้ปริมาณผลผลิตเพิ่มขึ้น {} กิโลกรัม".format(n+1,model_var[n],str(round(coef_var[0],2)).replace("+","")))
                else:
                    st.text("{}. เมื่อ{}ลดลง 1 หน่วย ส่งผลให้ปริมาณผลผลิตเพิ่มขึ้น {} กิโลกรัม".format(n+1,model_var[n],str(round(coef_var[0],2)).replace("-","")))
                n += 1
            col1,col2 = st.columns([1,1])
            with col1:
                weight = st.number_input("ปริมาณผลผลิตที่ต้องการ:",min_value=0.00,format=("%f"))
            with col2:
                control = st.selectbox("ปัจจัยอิสระที่ควบคุมได้:",options=(model_var),format_func=lambda model_var:"{}".format(model_var))
            st.markdown("**ระดับควรที่ควบคุม**")
            col = []
            for i in model_var:
                col.append(i)
            model_arguments.columns=col
            equation = ("")
            n =0
            for col_name in (model_arguments):
                value = model_arguments[col_name].tolist()
                if col_name == control:
                    value = str("x")
                else:
                    value = value[0]
                coef = abs(model_coef[n][0])
                if model_coef[n][0] >=0:
                    equation = ("+ ({} * {})".format(coef,value)) + equation
                else:
                    equation = ("- ({} * {})".format(coef,value)) + equation
                n += 1
            equation = str(weight) + str(" = ") + str(model_intercept) + equation
            # st.write(equation)
            answer = solve(equation)
            if answer == "No solution":
                st.error("ขออภัยปัจจัยควบคุมได้ที่คุณเลือก ไม่ได้มีความสัมพันธ์ต่อโมเดลนี้ โปรดสร้างโมเดลใหม่อีกครั้ง หรือเลือกปัจจัยอื่น")
            else:
                st.markdown("คุณควรควบคุม{}ในระดับ {} หน่วย".format(control,round(float(answer),2)))
            st.caption("*โมเดลที่คุณเลือกมีค่าความเชื่อมั่นที่ตัวแปรอิสระสามารถอธิบายตัวแปรตามได้ {}% ".format(round(model_r2,2)*100))
            st.caption("**โปรดมั่นใจว่าตัวแปรอิสระตัวอื่นต้องอยู่ในระดับคงที่")
main()

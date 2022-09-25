import streamlit as st
import pandas as pd
import plotly.express as px
from sql_execute import plants_tb_select,table_details_select,independent_variable_details_by_crop_select,columns_name_independent_weather,columns_name_independent_crop
from calculate import columns_name_for_dataframe
st.set_page_config(
    page_title="Modeling",
    page_icon="👋",
    layout="wide"
)

st.subheader("สร้างแบบจำลองพหุคูณ")
def main():
    with st.expander("การคัดเลือกตัวแปรต้นและตัวแปรอิสระ"):
        plant_options = plants_tb_select()
        plant_selected = st.selectbox("กรุณาเลือกพืช",plant_options,format_func= lambda plant_options: "{}".format(plant_options[1]))
        columns_independent_weather = columns_name_independent_weather()
        columns_independent_crop = columns_name_independent_crop()
        columns_name = columns_name_for_dataframe(columns_independent_weather, columns_independent_crop)
        dt = independent_variable_details_by_crop_select(plant_selected[0])
        df = pd.DataFrame(dt, columns=columns_name)
        col_left, col_right = st.columns([1, 3])
        with col_left:
            dependent_options = table_details_select("only_dependent")
            dependent_selected = st.selectbox(label="ตัวแปรตาม:", options=dependent_options, format_func=lambda dependent_options: "{}".format(dependent_options[1]), disabled=True)

        with col_right:
            independent_options = table_details_select("only_independent")
            independent_selected = st.multiselect(label="ตัวแปรอิสระ:", options=independent_options, format_func=lambda independent_options: "{}".format(independent_options[1]),default=independent_options)
            columns_selected = []
            for rows in independent_selected:
                columns_selected.append(rows[1])
        #df.loc[:, columns_selected]
        df = df[columns_selected]
        describe_status = st.checkbox("แสดงตารางอธิบายข้อมูล (Data Describe):", value=False)
        if describe_status is True:
            st.text("ตารางอธิบายข้อมูล")
            st.table(df.describe(percentiles=None))
        else:
            pass
        outlier_status = st.checkbox("แสดงการวิเคราะห์ค่านอกขอบเขต (Outliers):",value=False)
        if outlier_status is True:
            outlier_independent_selected = st.selectbox(label="ค่านอกขอบเขตตัวแปรอิสระ:", options=independent_options,
                                              format_func=lambda independent_options: "{}".format(
                                                  independent_options[1]))
            outlier_df = df[outlier_independent_selected[1]]
            box_df = px.data.tips()
            fig = px.box(box_df, y=outlier_df,width=500)
            st.plotly_chart(fig)
        else:
            pass
main()


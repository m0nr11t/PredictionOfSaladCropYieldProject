import streamlit as st
from sql_execute import independent_variable_details_by_crop_select,plants_tb_select,columns_name_independent_weather,\
columns_name_independent_crop,table_details_select
from calculate import columns_name_for_dataframe
import pandas as pd
import plotly.express as px
import seaborn as sb
st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.title("หน้าแรก")
# from streamlit_option_menu import option_menu
# # horizontal Menu
# selected = option_menu(None, ["เรียกดูข้อมูล", "เพิ่มข้อมูล", "แก้ไขข้อมูล"],
# icons=["book-fill", "file-earmark-plus-fill", "pencil-fill"],
# # menu_icon="cast", default_index=0, orientation="horizontal")
# with st.expander("Select Independent and Dependent Variables Process"):
#     col_left, col_right = st.columns([1,2])
#     with col_left:
#         dependent_options = ['a','b','c']
#         dependent_selected = st.selectbox(label="Dependent",options=dependent_options)
#         sql_dependent = dependent_selected + str(", ")
#     st.write(sql_dependent)  ### For Test ###
#     with col_right:
#         opt = test_select_independent_options()
#         n = 0
#         independent_options = []
#         for values in opt:
#             c = opt[n][0]
#             independent_options.append(c)
#             n+=1
#         independent_selected = st.multiselect(label="Independent",options=independent_options)
#         for values in independent_options:
#             sql_independent = ", ".join(independent_selected)
#
#     st.write(sql_independent) ### For Test ###
#
# def columns_name_split(sql_independent):
#     var = sql_independent.split(', ')
#     return var
# columns_name = columns_name_split(sql_independent)
#
# with st.expander("Model Assumptions Process"):
#     if sql_independent == "":
#         st.error("กรุณาเลือกตัวแปรอิสระอย่างน้อย 1 ตัว")
#     else:
#         st.write("1. สรุปข้อมูลเบื้องต้น")
#         variable_raw_data = test_select_variable(sql_dependent,sql_independent)
#         variable_data = pd.DataFrame(variable_raw_data,columns=columns_name)
#         #Plot Describe Table#
#         variable_data_describe = variable_data.describe()
#         st.table(variable_data_describe)
#
#         st.write("2. กราฟ Boxplot")
#         #Plot boxplot#
#         boxplot_fig = px.box(variable_data, y=columns_name)
#         st.plotly_chart(boxplot_fig, use_container_width=True)
#
#         st.write("3. กราฟ Pairplot")
#         pairplot_fig = sb.pairplot(variable_data,kind='reg',
#                      plot_kws={'scatter_kws': {'alpha': 0.4},
#                                'line_kws': {'color': 'red'}},
#                      diag_kws={'color': 'blue', 'alpha': 0.2});
#         st.pyplot(pairplot_fig)

with st.expander("Select Independent and Dependent Variables Process"):
    plant_options = plants_tb_select()
    # st.write(plant_options)
    plant_selected = st.selectbox(label="plants",options=plant_options)
    # st.write(plant_selected)
    columns_name_independent_weather = columns_name_independent_weather()
    columns_name_independent_crop = columns_name_independent_crop()
    columns_name = columns_name_for_dataframe(columns_name_independent_weather, columns_name_independent_crop)
    dt = independent_variable_details_by_crop_select(plant_selected[0])
    df = pd.DataFrame(dt,columns=columns_name)
    st.write(df)
    independent_options = table_details_select("only_independent")
    independent_selected = st.multiselect(label="ตัวแปรอิสระ:", options=independent_options,
                                          format_func=lambda independent_options: "{}".format(independent_options[1]),
                                          default=independent_options)
    columns_selected = []
    for rows in independent_selected:
        columns_selected.append(rows[1])
    df.loc[:, columns_selected]



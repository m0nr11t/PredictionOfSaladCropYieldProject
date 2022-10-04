import streamlit as st
from pyecharts.faker import Faker

from sql_execute import plants_tb_select,farmers_tb_select,dashboard_select,plan_year_options_select,\
sql_independent_variable_details_by_crop_argument,columns_name_independent_weather,weight_year_by_vil,\
columns_name_independent_crop,farm_analysis_select
from calculate import *
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Line
from streamlit_echarts import st_pyecharts, st_echarts

st.set_page_config(
    page_title="หน้าแรก",
    page_icon="🏠",
    layout="wide"
)

def main():
    st.subheader("หน้าแรก")
    with st.container():
        col1,col2,col3,col4 = st.columns([2,1,1,1])
        with col4:
            plant_options = plants_tb_select()
            plant_options.insert(0,[0,'ทั้งหมด'])
            plant_selected = st.selectbox("พืช",options=plant_options,format_func=lambda plant_options:"{}".format(plant_options[1]))
        # st.write(plant_selected[0])
        dt = dashboard_select(plant_selected[0],'ทั้งหมด')
        columns_independent_weather = columns_name_independent_weather()
        columns_independent_crop = columns_name_independent_crop()
        columns_name = columns_name_for_dataframe(columns_independent_weather, columns_independent_crop)
        df = pd.DataFrame(dt,columns=columns_name)
        # st.write(df)
        dt_group_plant = dashboard_select(plant_selected[0],str('ทั้งหมด'))
        df_group_plant = pd.DataFrame(dt_group_plant,columns=columns_name)
        weight_year_df = df_group_plant[['ปริมาณผลผลิตก่อนตัดแต่ง','plan_year']]
        weight_year_df = weight_year_df.groupby(['plan_year']).sum()
        weight_year_df.reset_index(inplace=True)
        weight_year_df.plan_year = weight_year_df.plan_year.astype(str)
        year_list = weight_year_df['plan_year'].values.tolist()
        weight_list = weight_year_df['ปริมาณผลผลิตก่อนตัดแต่ง'].values.tolist()

    with st.container():
        st.markdown("#### แนวโน้มปริมาณผลผลิตของพืชแต่ละชนิด (กิโลกรัม)")
        weight_trend_plant = (
            Line()
                .add_xaxis(year_list)
                .add_yaxis("ปริมาณผลผลิต", weight_list)
            # .set_global_opts(title_opts=opts.TitleOpts(title="แนวโน้มปริมาณผลผลิต (กิโลกรัม)",title_textstyle_opts=opts.TextStyleOpts(color="#6e7079",font_size=20)))
        )
        st_pyecharts(weight_trend_plant, height="500px",key="weight_trend_plant")
    with st.container():
        col1,col2,col3,col4 = st.columns([2,1,1,1])
        with col4:
            farm_vil_name_options = farm_analysis_select(0)
            farm_vil_selected = st.selectbox("เลือกหมู่บ้าน", options=farm_vil_name_options,
                                             format_func=lambda farm_vil_name_options: "{}".format(
                                                 farm_vil_name_options[0]))
    with st.container():
        col1,col2 = st.columns([1.5,1])
        with col2:
            weight_year_by_vil_dt = weight_year_by_vil(farm_vil_selected[0], plant_selected[0])
            weight_year_by_vil_df = pd.DataFrame(weight_year_by_vil_dt,
                                                 columns=['plan_year', 'plant_weight_before_trim'])
            # weight_group_by_vil_year = weight_year_by_vil_df.groupby(['plan_year']).sum()
            plan_year_df = weight_year_by_vil_df.plan_year.astype(str)
            plan_year_list = plan_year_df.unique().tolist()
            weight_vil_list = weight_year_by_vil_df['plant_weight_before_trim'].values.tolist()
            st.markdown("##### แนวโน้มปริมาณผลผลิต (กิโลกรัม)")
            weight_trend_vil = (
                Line()
                    .add_xaxis(plan_year_list)
                    .add_yaxis("ปริมาณผลผลิต", weight_vil_list)
                    # .set_global_opts(title_opts=opts.TitleOpts(title="แนวโน้มปริมาณผลผลิต (กิโลกรัม)",title_textstyle_opts=opts.TextStyleOpts(color="#6e7079",font_size=20)))
            )
            st_pyecharts(weight_trend_vil,height="500px",key="weight_trend_vil")
        with col1:
            st.markdown("##### สัดส่วนการตรวจคุณภาพแปลงแต่ละหมู่บ้าน (แห่ง)")
            farm_analysis_dt = farm_analysis_select(farm_vil_selected[0])
            farm_analysis_df = pd.DataFrame(farm_analysis_dt,columns=['farm_vil_name','soil_analysis','water_analysis','gap_analysis'])
            farm_analysis_df = farm_analysis_df.rename(columns={'farm_vil_name':'vilname','soil_analysis':'Soil Analysis','water_analysis':'Water Analysis','gap_analysis':'GAP Analysis'})
            farm_analysis_df = farm_analysis_df.transpose()
            farm_analysis_df = farm_analysis_df.drop(farm_analysis_df.index[:1])
            farm_analysis_df = farm_analysis_df.reset_index()
            farm_analysis_df = farm_analysis_df.rename(columns={"index": "name", 0:"value"})
            ls = farm_analysis_df.values.tolist()
            farm_test_vil = (
                Pie()
                    .add("", ls)
                    # .set_global_opts(title_opts=opts.TitleOpts(title="สัดส่วนที่อยู่แปลง",title_textstyle_opts=opts.TextStyleOpts(color="#6e7079",font_size=20)))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
            st_pyecharts(farm_test_vil,height="500px",key="farm_test_vil")
    with st.container():
        pass
main()
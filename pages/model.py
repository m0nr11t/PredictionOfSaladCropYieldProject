import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from matplotlib import font_manager
location = ['C:/Users/monmo/Downloads/Kanit']
font_files = font_manager.findSystemFonts(fontpaths = ['C:/Users/monmo/Downloads/Kanit'])
for file in font_files:
    font_manager.fontManager.addfont(file)
sns.set_theme(font="Kanit")
import sklearn as sk
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import statsmodels.api as sm
import math
from sql_execute import plants_tb_select,table_details_select,data_query_for_modeling,columns_name_independent_weather,columns_name_independent_crop
from calculate import columns_name_for_dataframe
st.set_page_config(
    page_title="Modeling",
    page_icon="👋",
    layout="wide"
)

st.subheader("สร้างแบบจำลองพหุคูณ")
def main():
    plant_options = plants_tb_select()
    plant_selected = st.selectbox("กรุณาเลือกพืช", plant_options,
                                  format_func=lambda plant_options: "{}".format(plant_options[1]))
    columns_independent_weather = columns_name_independent_weather()
    columns_independent_crop = columns_name_independent_crop()
    columns_name = columns_name_for_dataframe(columns_independent_weather, columns_independent_crop)
    dt = data_query_for_modeling(plant_selected[0])
    df_raw = pd.DataFrame(dt, columns=columns_name)
    # df_raw = df_raw.fillna(0)
    col_left, col_right = st.columns([1, 3])
    with col_left:
        dependent_options = table_details_select("only_dependent")
        dependent_selected = st.selectbox(label="ตัวแปรตาม:", options=dependent_options,
                                          format_func=lambda dependent_options: "{}".format(dependent_options[1]),
                                          disabled=True)
        de_column_selected = dependent_selected[1]
    with col_right:
        independent_options = table_details_select("only_independent")
        independent_selected = st.multiselect(label="ตัวแปรอิสระ:", options=independent_options,
                                              format_func=lambda independent_options: "{}".format(
                                                  independent_options[1]), default=independent_options)
        inde_columns_selected = []
        for rows in independent_selected:
            inde_columns_selected.append(rows[1])
    # df.loc[:, columns_selected]
    df = df_raw[inde_columns_selected]
    if df.empty:
        st.error("ไม่สามารถสร้างแบบจำลองได้ เนื่องจากไม่พบข้อมูล กรุณาเพิ่มข้อมูลก่อนดำเนินการ")
    else:
        X = df_raw[inde_columns_selected]
        Y = df_raw[de_column_selected]
        X_train, X_test = train_test_split(X, test_size=0.3, random_state=1)
        Y_train, Y_test = train_test_split(Y, test_size=0.3, random_state=1)
        regression_predict_model = LinearRegression()
        regression_predict_model.fit(X_train, Y_train)
        intercept = regression_predict_model.intercept_
        col_name_list = list(X.columns)
        coefficients = pd.DataFrame(regression_predict_model.coef_, X.columns)
        coefficent_x_var = ("")
        n = 0
        for rows in col_name_list:
            co = coefficients.loc[col_name_list[n]][0]
            if coefficients.loc[col_name_list[n]][0] >= 0:
                co = str("+") + str(round(coefficients.loc[col_name_list[n]][0],3))
            coefficent_x_var = str(co) + str("(") + str(col_name_list[n]) + str(")")  + str(coefficent_x_var)
            n+=1
        st.text("รูปสมการ:")
        st.text("""Y = {:.3f} {}""".format(intercept,coefficent_x_var))

        with st.expander("การวิเคราะห์ข้อมูลตัวแปรเบื้องต้น"):
            st.write("ข้อมูล (Data):")
            st.dataframe(df, width=2500)
            # fill_na = st.checkbox("เติมข้อมูลที่ว่างด้วยค่าศุนย์",value=False)
            # if fill_na is True:
            #     df = df.fillna(0)
            #     df_raw[de_column_selected].fillna(0)
            # else:
            #     df = df_raw[inde_columns_selected]
            # st.dataframe(df)
            st.markdown("---")
            describe_status = st.checkbox("1. ตารางอธิบายข้อมูล (Data Describe):", value=False)
            if describe_status is True:
                st.table(df.describe().applymap('{:,.2f}'.format))
                st.markdown("---")
            else:
                pass
            outlier_status = st.checkbox("2. การวิเคราะห์ค่านอกขอบเขต (Outliers):",value=False)
            if outlier_status is True:
                outlier_independent_selected = st.selectbox(label="ค่านอกขอบเขตตัวแปรอิสระ:", options=independent_selected,
                                                  format_func=lambda independent_selected: "{}".format(
                                                      independent_selected[1]))
                outlier_df = df[outlier_independent_selected[1]]
                col1,col2,col3 = st.columns([1,2,1])
                with col2:
                    box_df = px.data.tips()
                    fig = px.box(box_df, y=outlier_df,width=500)
                    st.plotly_chart(fig)
                st.markdown("---")
            else:
                pass
            pairplot_status = st.checkbox("3. การวิเคราะห์ความสัมพันธ์เชิงเส้นจากแผนภาพ (Pairplot):",value=False,key="pairplot")
            if pairplot_status is True:
                with st.spinner('ระบบกำลังวิเคราะห์ข้อมูล กรุณารอซักครู่😫'):
                    pairplot_fig = sns.pairplot(df,
                                     kind='reg',
                                     plot_kws={'scatter_kws': {'alpha': 0.4},
                                               'line_kws': {'color': '#F652A0'}},
                                     diag_kws={'color': 'green', 'alpha': 0.2});
                    st.pyplot(pairplot_fig)
                    st.markdown('---')
            else:
                pass
            corr_status = st.checkbox("4. การวิเคราะห์ค่าสหสัมพันธ์โดยวิธีการของ (Pearson correlation):",value=False)
            if corr_status is True:
                df_corr = df.corr(method='pearson')
                st.table(df_corr)
                st.markdown('---')
            else:
                pass
            corr_heatmap_status = st.checkbox("5. การวิเคราะห์ความเป็นอิสระต่อกันของตัวแปร (Multicollinearity):",value=False)
            if corr_heatmap_status is True:
                df_corr_abs = df.corr(method='pearson').abs()
                col1,col2,col3=st.columns([1,2,1])
                with col2:
                    fig, ax = plt.subplots(figsize=(10, 10))
                    colormap = sns.light_palette("Green",n_colors=10)
                    sns.heatmap(df_corr_abs, annot=True, linewidths=1,cmap=colormap)
                    st.pyplot(fig)
                st.markdown('---')
            else:
                pass

            dist_status = st.checkbox("6. การวิเคราะห์การกระจายตัวของข้อมูล (Data Distribution):",value=False)
            if dist_status is True:
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    std = np.std(df_raw[de_column_selected], ddof=1)
                    mean = np.mean(df_raw[de_column_selected])
                    domain = np.linspace(np.min(df_raw[de_column_selected]), np.max(df_raw[de_column_selected]))
                    fig,ax = plt.subplots()
                    plt.plot(domain, norm.pdf(domain, mean, std),
                             label=f'Mean: {round(mean)} Standard: {round(std)}',color="#F652A0")
                    plt.hist(df_raw[de_column_selected],color="green", edgecolor="green", alpha=0.5, density=True)
                    plt.title("Normal Fit")
                    plt.xlabel("Value")
                    plt.ylabel("Density")
                    st.pyplot(fig)
                st.markdown('---')
            else:
                pass
        with st.expander("ประเมินแบบจำลอง (Model Evaluation)"):
            Y_predicted = regression_predict_model.predict(X_test)

            st.write("การประเมินค่าความคลาดเคลื่อนเฉลี่ย (The Standard Error of The Regression):")
            MAE = sk.metrics.mean_absolute_error(Y_test, Y_predicted)
            MSE = sk.metrics.mean_squared_error(Y_test, Y_predicted)
            RMSE = np.sqrt(MSE)
            R2 = sk.metrics.r2_score(Y_test, Y_predicted)
            outlier_check = st.checkbox("ข้อมูลมีค่านอกขอบเขต (Outlier)",value=False)
            if outlier_check is True:
                st.write("ค่าความคลาดเคลื่อนสัมบูรณ์เฉลี่ย (Mean Absolute Error or MAE): ",round(MAE,3))
                st.write("หมายความว่า ปริมาณผลผลิตพยากรณ์จำนวนใด ๆ กิโลกรัม จะมีความคลาดเคลื่อนอยู่ที่ {:.2f} กิโลกรัม".format(MAE))
            else:
                st.write("ค่ารากที่สองของค่าเฉลี่ยความคลาดเคลื่อนยกกำลังสอง (Root Mean Square Error or RMSE): ",round(RMSE,3))
                st.write("หมายความว่า ปริมาณผลผลิตพยากรณ์จำนวนใด ๆ กิโลกรัม จะมีความคลาดเคลื่อนอยู่ที่ {:.2f} กิโลกรัม".format(RMSE))
            st.write("การประเมินความเชื่อมั่นของแบบจำลอง :")
            st.write(R2)
            X_test = sm.add_constant(X)
            model = sm.OLS(Y, X_test)
            linear_multi_Reg = model.fit()
            st.write(linear_multi_Reg.conf_int())
main()


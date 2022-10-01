import datetime
from io import BytesIO
from PIL import Image
import pandas as pd
import streamlit as st
from sql_execute import table_details_select

def prename_transform(farmer_selected):
    ### Transform Str to Int for Radiobutton Index ###
    if farmer_selected == "นาย":
        prename_index = 0
    elif farmer_selected == "นาง":
        prename_index = 1
    elif farmer_selected == "นางสาว":
        prename_index = 2
    return prename_index

def timestamp():
    timenow = datetime.datetime.now()
    return timenow

def load_image(image_file):
    img = Image.open(image_file)
    fp = BytesIO()
    img.save(fp, "PNG")
    bytes_data = fp.getvalue()
    return bytes_data

def columns_name_for_dataframe(columns_name_independent_weather,columns_name_independent_crop):
    columns_name = ['plants_plant_id', 'plant_name', 'plans_plant_id', 'plan_year', 'crops_plan_id', 'crops_crop_id',
                    'cropstart_date', 'cropfinish_date', 'crops_crop_id_daily']
    # columns_name_2
    columns_name_independent_weather = columns_name_independent_weather
    for rows in columns_name_independent_weather:
        columns_name.append(rows)
    columns_name.append('crops_crop_id_crop')
    columns_name_independent_crop = columns_name_independent_crop
    for rows in columns_name_independent_crop:
        columns_name.append(rows)
    columns_name.append('crop_details_crop_id')
    columns_name.append('ปริมาณผลผลิตก่อนตัดแต่ง')
    return columns_name

def transform_colname_th_en(model_var):
    df_model_var = pd.DataFrame(model_var)
    tb_details = table_details_select("only_independent")
    df_tb_name = pd.DataFrame(tb_details)
    # st.write(df_tb_name)
    # st.write(df_model_var)
    col_name_en = pd.merge(left=df_tb_name,right=df_model_var,left_on=[1],right_on=[0],how="inner")
    # st.write(col_name_en)
    col_name_en = col_name_en[['0_x',1,2,3,4]]
    return col_name_en

def columns_name_for_predicted(columns_name_independent_weather,columns_name_independent_crop):
    columns_name = ['crops_plan_id', 'crops_crop_id','crop_id']
    columns_name_independent_weather = columns_name_independent_weather
    for rows in columns_name_independent_weather:
        columns_name.append(rows)
    columns_name.append('crops_crop_id_crop')
    columns_name_independent_crop = columns_name_independent_crop
    for rows in columns_name_independent_crop:
        columns_name.append(rows)
    columns_name.append('crop_details_crop_id')
    columns_name.append('ปริมาณผลผลิตก่อนตัดแต่ง')
    return columns_name


def solve(equation):
    """Solve Linear Equations using eval() function in Python
    Special Thanks to Greeksforgreeks
    Cr. https://www.geeksforgeeks.org/solve-linear-equations-using-eval-in-python/
    """
    # replacing all the x terms with j
    # the imaginary part
    s1 = equation.replace('x', 'j')

    # shifting the equal sign to start
    # an opening bracket
    s2 = s1.replace('=', '-(')

    # adding the closing bracket to form
    # a complete expression
    s = s2 + ')'

    # mapping the literal j to the complex j
    z = eval(s, {'j': 1j})
    real, imag = z.real, -z.imag

    # if the imaginary part is true return the
    # answer
    if imag:
        return "%f" % (real / imag)
    else:
        if real:
            return "No solution"
        else:
            return "Infinite solutions"

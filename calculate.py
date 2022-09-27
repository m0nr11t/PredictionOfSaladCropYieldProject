import datetime
from io import BytesIO
from PIL import Image
import pandas as pd
import statsmodels.api as sm
import streamlit as st
from statsmodels.stats.outliers_influence import variance_inflation_factor

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

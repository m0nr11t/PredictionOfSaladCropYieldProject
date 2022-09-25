import pandas as pd
from postgres_con import db_local_connect
from io import BytesIO
from PIL import Image
import streamlit as st

def db_connection():
    "This function connected postgresql database and create cursor for SQL statements support"
    db_connected = db_local_connect()
    c = db_connected.cursor()
    return db_connected,c

def tb_select_pil(table_name, pk, pk_value, outfile=None):
    db_connect, c = db_connection()
    c.execute("""SELECT img FROM {}
                        WHERE {} = {};""".format(table_name,pk,pk_value))
    row = c.fetchone()
    if row:
        bytes_stream = BytesIO(row[0])
        img = Image.open(bytes_stream)
        return img, row
    return None

def test_select_independent_options():
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    c.execute("""SELECT column_name FROM information_schema.columns
                WHERE table_name = 'plants'
                AND column_name IN
                    (SELECT column_name FROM information_schema.columns
                    WHERE column_name NOT LIKE 'plant_id'
                    AND column_name NOT LIKE 'img'
                    AND column_name NOT LIKE 'created_at'
                    AND column_name NOT LIKE 'updated_at'
                    AND column_name NOT LIKE 'plant_name');""")
    data = c.fetchall()
    db_connect.close()
    return data

def test_select_variable(sql_dependent,sql_independent):
    "This function for select data where dependent selected's columns from dependent table"
    db_connect, c = db_connection()
    c.execute("""SELECT {} FROM plants;""".format(sql_dependent,sql_independent))
    data = c.fetchall()
    db_connect.close()
    return data

def farmers_tb_select():
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    sql_statement = """SELECT farmer_id, prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                              farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, updated_at FROM farmers ORDER BY farmer_id;"""
    c.execute(sql_statement)
    data = c.fetchall()
    db_connect.close()
    return data

def farmers_tb_insert(prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                             image_file , farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, created_at, updated_at):
    "This function for insert data to farmer's table from farmer's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO farmers(prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                             img , farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, created_at, updated_at)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    values = (prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                             image_file , farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, created_at, updated_at)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def farmers_tb_update(prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                             image_file , farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, updated_at, pk_value):
    db_connect, c = db_connection()
    sql_statement = """UPDATE farmers
                         SET prename = %s, firstname = %s, lastname = %s, farmer_gov_id = %s, gov_id = %s, tel = %s,
                            house_no = %s, vil_no = %s, vil_name = %s, subdistrict_name = %s, district_name = %s,
                            province_name = %s, postcode = %s, img = %s, farm_vil_no = %s, farm_vil_name = %s,
                            farm_subdistrict_name = %s, farm_district_name = %s, farm_province_name = %s, farm_geo_x = %s,
                            farm_geo_y = %s, farm_geo_z = %s, farm_land_privileges = %s, farm_soil_analysis = %s,
                            farm_water_analysis = %s, farm_gap_analysis = %s, updated_at = %s
                         WHERE farmer_id = '%s';"""
    values = (prename, firstname, lastname, farmer_gov_id, gov_id, tel, house_no, vil_no, vil_name, subdistrict_name, district_name, province_name, postcode,
                             image_file , farm_vil_no, farm_vil_name, farm_subdistrict_name, farm_district_name, farm_province_name, farm_geo_x, farm_geo_y, farm_geo_z,
                           farm_land_privileges, farm_soil_analysis, farm_water_analysis, farm_gap_analysis, updated_at, pk_value)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def farmers_tb_delete(farmer_id):
    "This function fot delete data to farmers's table from user selected"
    db_connect, c = db_connection()
    c.execute("DELETE FROM farmers WHERE farmer_id = %s;", [farmer_id])
    db_connect.commit()
    db_connect.close()

def plants_tb_select():
    db_connect, c = db_connection()
    sql_statement = """SELECT plant_id, plant_name FROM plants ORDER BY plant_id;"""
    c.execute(sql_statement)
    data = c.fetchall()
    db_connect.close()
    return data

def plants_tb_insert(plant_name, img, created_at, updated_at):
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO plants(plant_name, img, created_at, updated_at)
                     VALUES (%s, %s, %s, %s);"""
    values = (plant_name, img, created_at, updated_at)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plants_tb_update(plant_id,plant_name,plant_img,updated_at):
    "This function fot update data to plant's table from user selected"
    db_connect, c = db_connection()
    sql_statement = """UPDATE plants
                         SET plant_name = %s, img = %s, updated_at = %s
                         WHERE plant_id = %s;"""
    values = (plant_name,plant_img,updated_at,plant_id)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plants_tb_delete(plant_id):
    "This function fot delete data to plant's table from user selected"
    db_connect, c = db_connection()
    c.execute("DELETE FROM plants WHERE plant_id = %s;", [plant_id])
    db_connect.commit()
    db_connect.close()

def plans_tb_insert(plan_year, created_at, updated_at, fk_value):
    "This function for insert data to plans's table from plan's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO plans(plan_year, created_at, updated_at, plant_id)
                             VALUES (%s, %s, %s, %s);"""
    values = (plan_year, created_at, updated_at, fk_value)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plans_tb_select():
    db_connect, c = db_connection()
    sql_statement = """SELECT p.*, pt.plant_name FROM plans AS p INNER JOIN plants AS pt ON p.plant_id = pt.plant_id ORDER BY plan_id;"""
    c.execute(sql_statement)
    data = c.fetchall()
    db_connect.close()
    return data

def plans_tb_update(plan_year, updated_at, plan_id):
    db_connect, c = db_connection()
    sql_statement = """UPDATE plans
                         SET plan_year = %s, updated_at = %s
                         WHERE plan_id = %s;"""
    values = (plan_year, updated_at, plan_id)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plan_duplicate():
    db_connect, c = db_connection()
    c.execute("""SELECT plan_year, plant_id FROM plans;""")
    data = c.fetchall()
    db_connect.close()
    return data

def plans_tb_delete(plan_id):
    "This function fot delete data to plans's table from user selected"
    db_connect, c = db_connection()
    c.execute("DELETE FROM plans WHERE plan_id = %s;", [plan_id])
    db_connect.commit()
    db_connect.close()

def crop_number(plan_id):
    db_connect, c = db_connection()
    c.execute("""SELECT COUNT(crop_id) FROM crops INNER JOIN plans ON crops.plan_id = plans.plan_id
                    WHERE crops.plan_id = {};""".format(plan_id))
    data = c.fetchone()
    db_connect.close()
    return data

def crops_tb_insert(cropstart_date, cropmove_date, cropfinish_date, created_at, updated_at, fk_value):
    "This function for insert data to crops's table from crop's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO crops(cropstart_date, cropmove_date, cropfinish_date, created_at, updated_at, plan_id)
                                 VALUES (%s, %s, %s, %s, %s, %s);"""
    values = (cropstart_date, cropmove_date, cropfinish_date, created_at, updated_at, fk_value)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def crops_tb_plans_select():
    db_connect, c = db_connection()
    c.execute("""SELECT plans.plan_year,plants.plant_name,plans.plan_id FROM crops INNER JOIN plans ON crops.plan_id = plans.plan_id
    	                INNER JOIN plants ON plans.plant_id = plants.plant_id
    	                GROUP BY plans.plan_id, plants.plant_id;""")
    data = c.fetchall()
    db_connect.close()
    return data

def crops_tb_select(plan_id):
    db_connect, c = db_connection()
    c.execute("""SELECT crops.*,ROW_NUMBER() OVER(ORDER BY crops.crop_id) AS row_no FROM crops INNER JOIN plans ON crops.plan_id = plans.plan_id
	                INNER JOIN plants ON plans.plant_id = plants.plant_id 
	                WHERE crops.plan_id = %s;""",([plan_id]))
    data = c.fetchall()
    db_connect.close()
    return data

def crops_tb_update(crop_id, cropstart_date, cropmove_date ,cropfinish_date, updated_at):
    db_connect, c = db_connection()
    sql_statement = """UPDATE crops
                             SET cropstart_date = %s, cropmove_date = %s, cropfinish_date = %s, updated_at = %s
                             WHERE crop_id = %s;"""
    values = (cropstart_date, cropmove_date ,cropfinish_date, updated_at, crop_id)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def crops_tb_delete(crop_id):
    "This function fot delete data to crops's table from user selected"
    db_connect, c = db_connection()
    c.execute("DELETE FROM crops WHERE crop_id = %s;", [crop_id])
    db_connect.commit()
    db_connect.close()

def crops_options_select():
    db_connect, c = db_connection()
    c.execute("""SELECT crops.crop_id, plant_name, plan_year, ROW_NUMBER() OVER (PARTITION BY plant_name, plan_year ORDER By plant_name, plan_year) AS num_row 
	                FROM crops INNER JOIN plans ON crops.plan_id = plans.plan_id
		                INNER JOIN plants ON plans.plant_id = plants.plant_id ;""")
    data = c.fetchall()
    db_connect.close()
    return data

def crop_details_tb_select(crop_id):
    db_connect, c = db_connection()
    c.execute("""SELECT crop_details.crop_id, crop_details.farmer_id, firstname, lastname, farmer_gov_id, rai_area, ngan_area, building_area, plang_area, seedling_quantity FROM crop_details INNER JOIN farmers ON crop_details.farmer_id = farmers.farmer_id
		INNER JOIN crops ON crop_details.crop_id = crops.crop_id
		WHERE crop_details.crop_id = {};""".format(crop_id))
    data = c.fetchall()
    db_connect.close()
    return data

def crop_details_duplicate():
    db_connect, c = db_connection()
    c.execute("""SELECT crop_id, farmer_id  FROM crop_details""")
    data = c.fetchall()
    db_connect.close()
    return data

def crop_details_tb_insert(crop_id, farmer_id, farm_rai, farm_building, farm_ngan, farm_plang, seedling_quantity, created_at, updated_at):
    "This function for insert data to crop_details's table from crop details's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO crop_details(crop_id, farmer_id, rai_area, building_area, ngan_area, plang_area, seedling_quantity, created_at, updated_at)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    values = (crop_id, farmer_id, farm_rai, farm_building, farm_ngan, farm_plang, seedling_quantity, created_at, updated_at)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def crop_details_tb_update(crop_id, farmer_id, farm_rai, farm_building, farm_ngan, farm_plang, seedling_quantity, updated_at):
    db_connect, c = db_connection()
    sql_statement = """UPDATE crop_details
                             SET rai_area = %s, building_area = %s, ngan_area = %s, plang_area = %s, seedling_quantity = %s, updated_at = %s
                             WHERE crop_id = %s AND farmer_id = %s;"""
    values = (farm_rai, farm_building, farm_ngan, farm_plang, seedling_quantity, updated_at, crop_id, farmer_id)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def crop_details_tb_delete(crop_id, farmer_id):
    db_connect, c = db_connection()
    c.execute("DELETE FROM crop_details WHERE crop_id = %s AND farmer_id = %s;", (crop_id,farmer_id))
    db_connect.commit()
    db_connect.close()

def crop_detail_products_duplicate():
    db_connect, c = db_connection()
    c.execute("""SELECT crop_id, farmer_id FROM crop_detail_products""")
    data = c.fetchall()
    db_connect.close()
    return data

def variable_tb_insert(columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name):
    "This function for insert data to variables's table from config's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO variables(columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name)
                         VALUES (%s, %s, %s, %s, %s, %s);"""
    values = (columns_name, columns_alias, columns_datatype, created_at, columns_cal, columns_table_name)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def variable_create_columns(column_table_name, column_name, column_datatype):
    db_connect, c = db_connection()
    c.execute("ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} {};".format(column_table_name, column_name, column_datatype))
    db_connect.commit()
    db_connect.close()

def table_details_select(table_name):
    db_connect, c = db_connection()
    if (table_name == "only_dependent"):
        c.execute("""SELECT columns_name, columns_alias, columns_datatype, columns_table_name, columns_lasted_order, columns_cal FROM variables
        WHERE columns_name LIKE 'plant_weight_before_trim';""")
    elif (table_name == "only_independent"):
        c.execute("""SELECT columns_name, columns_alias, columns_datatype, columns_table_name, columns_lasted_order, columns_cal FROM variables
                        WHERE columns_name NOT LIKE 'plant_weight_before_trim';""".format(table_name))
    else:
        c.execute("""SELECT columns_name, columns_alias, columns_datatype, columns_table_name, columns_lasted_order, columns_cal FROM variables
                WHERE columns_table_name = '{}';""".format(table_name))
    data = c.fetchall()
    db_connect.close()
    return data

def independent_var_duplicate_date_input():
    db_connect, c = db_connection()
    c.execute("""SELECT date_input FROM independent_variables;""")
    data = c.fetchall()
    db_connect.close()
    return data

def variables_query(columns_query,from_con, join_con, on_con, where_con,order_by_con):
    db_connect, c = db_connection()
    c.execute("""SELECT {} {} {} {} {} {};""".format(columns_query,from_con, join_con, on_con, where_con,order_by_con))
    data = c.fetchall()
    db_connect.close()
    return data

def variable_update(table_name, set_update, where_update):
    "This function fot update data to independent variables's table from user selected"
    db_connect, c = db_connection()
    sql_statement = ("""UPDATE {} SET {} {};""".format(table_name, set_update, where_update))
    c.execute(sql_statement)
    db_connect.commit()
    db_connect.close()

def variable_img_update(image_file, pk_value):
    db_connect, c = db_connection()
    sql_statement = ("""UPDATE crop_detail_products SET img = %s WHERE crop_detail_product_id = %s;""")
    values = (image_file, pk_value)
    # st.write(sql_statement,values)
    c.execute(sql_statement,values)
    db_connect.commit()
    db_connect.close()

def variable_delete(table_name, where_delete):
    db_connect, c = db_connection()
    c.execute("DELETE FROM {} {};".format(table_name,where_delete))
    db_connect.commit()
    db_connect.close()

def sql_independent_variable_details_by_crop_argument():
    table_name = ("independent_variables")
    col_in_independent_variables = table_details_select(table_name)
    sql_col_independent_variables_query = ("")
    for rows in col_in_independent_variables:
        sql_col_independent_variables_query = sql_col_independent_variables_query + str(rows[5]) + str("(") + str(rows[0]) + str("),")
    sql_col_independent_variables_query = ''.join(sql_col_independent_variables_query.rsplit(',', 1))
    return sql_col_independent_variables_query

def columns_name_independent_weather():
    table_name = ("independent_variables")
    col_in_independent_variables = table_details_select(table_name)
    columns_name = []
    for rows in col_in_independent_variables:
        columns_name.append(rows[1])
    return columns_name

def sql_crop_details_by_crop_argument():
    table_name = ("crop_details")
    col_in_crop_details_variables = table_details_select(table_name)
    sql_col_crop_details_variables_query = ("COUNT(cd.farmer_id),")
    for rows in col_in_crop_details_variables:
        sql_col_crop_details_variables_query = sql_col_crop_details_variables_query + str(rows[5]) + str("(") + str(rows[0]) + str("),")
    sql_col_crop_details_variables_query = ''.join(sql_col_crop_details_variables_query.rsplit(',', 1))
    return sql_col_crop_details_variables_query

def columns_name_independent_crop():
    table_name = ("crop_details")
    col_in_crop_details_variables = table_details_select(table_name)
    columns_name = ['จำนวนเกษตรกร']
    for rows in col_in_crop_details_variables:
        columns_name.append(rows[1])
    return columns_name

def independent_variable_details_by_crop_select(plant):
    sql_col_independent_variables_query = sql_independent_variable_details_by_crop_argument()
    sql_col_crop_details_variables_query = sql_crop_details_by_crop_argument()
    db_connect, c = db_connection()
    c.execute("""SELECT plants.plant_id,plants.plant_name,summary_data_by_plan.* FROM
                    (SELECT PLANS.plant_id,PLANS.plan_year,summary_data_by_crop.* FROM
                        (SELECT crops.plan_id,crops.crop_id,cropstart_date,cropfinish_date,independent_weather.*, independent_crop.*, dependent_crop.* FROM
                            (SELECT  c.crop_id,{} FROM independent_variables 
                                                    RIGHT JOIN crops c 
                                                        ON date_input BETWEEN cropstart_date AND cropfinish_date
                                                    GROUP BY c.crop_id
                                                    ORDER BY c.crop_id) AS independent_weather
                        INNER JOIN
                            (SELECT c.crop_id,{} FROM farmers f
                                            INNER JOIN 
                                                crop_details cd 
                                            ON cd.farmer_id = f.farmer_id
                                            RIGHT JOIN 
                                                crops c
                                            ON cd.crop_id = c.crop_id
                                            GROUP BY c.crop_id
                                            ORDER BY c.crop_id) AS independent_crop
                        ON independent_weather.crop_id = independent_crop.crop_id
                        INNER JOIN		
                            (SELECT c.crop_id,SUM(plant_weight_before_trim) FROM crop_details cd 
                                            FULL OUTER JOIN 
                                                crop_detail_products cdp 
                                            ON cd.farmer_id = cdp.farmer_id AND cd.crop_id = cdp.crop_id
                                            RIGHT JOIN 
                                                crops c
                                            ON cd.crop_id = c.crop_id
                                            GROUP BY c.crop_id
                                            ORDER BY c.crop_id) AS dependent_crop
                        ON independent_crop.crop_id = dependent_crop.crop_id
                        RIGHT JOIN crops 
                        ON crops.crop_id = independent_weather.crop_id 
                        AND crops.crop_id = independent_crop.crop_id 
                        AND crops.crop_id = dependent_crop.crop_id 
                        ) AS summary_data_by_crop
                    RIGHT JOIN 
                    PLANS
                    ON PLANS.plan_id = summary_data_by_crop.plan_id) AS summary_data_by_plan
                RIGHT JOIN 
                plants 
                ON summary_data_by_plan.plant_id = plants.plant_id
                WHERE plants.plant_id = '{}';""".format(sql_col_independent_variables_query,sql_col_crop_details_variables_query,plant))
    data = c.fetchall()
    db_connect.close()
    return data


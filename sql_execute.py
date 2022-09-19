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
    c.execute("""SELECT columns_name, columns_alias, columns_datatype, columns_table_name FROM variables
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

def independent_var_tb_select(columns_query):
    db_connect, c = db_connection()
    c.execute("""SELECT {} FROM independent_variables ORDER BY date_input;""".format(columns_query))
    data = c.fetchall()
    db_connect.close()
    return data

def independent_var_update(sql_update,date_selected):
    "This function fot update data to independent variables's table from user selected"
    db_connect, c = db_connection()
    c.execute("""UPDATE independent_variables
                         SET {}
                         WHERE date_input = '{}';""".format(sql_update,date_selected))
    db_connect.commit()
    db_connect.close()

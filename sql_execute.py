from postgres_con import db_local_connect
from io import BytesIO
from PIL import Image
import streamlit as st

def db_connection():
    "This function connected postgresql database and create cursor for SQL statements support"
    db_connected = db_local_connect()
    c = db_connected.cursor()
    return db_connected,c

def test_select_independent_options():
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    c.execute("""SELECT column_name FROM information_schema.columns
                WHERE table_name = 'plant'
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
    c.execute("""SELECT {} FROM plant;""".format(sql_dependent,sql_independent))
    data = c.fetchall()
    db_connect.close()
    return data

def farm_tb_insert(vil_name, district_name, vil_no, subdistrict_name, province_name, geo_x, geo_y, geo_z,
                            land_privileges, soil_analysis, water_analysis, gap_analysis,created_at,updated_at):
    "This function for insert data to farm's table from farm's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO farm(vil_name, district_name, vil_no, subdistrict_name, province_name, geo_x, geo_y, geo_z,
                            land_privileges, soil_analysis, water_analysis, gap_analysis,created_at,updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    values = (vil_name, district_name, vil_no, subdistrict_name, province_name, geo_x, geo_y, geo_z,
                            land_privileges, soil_analysis, water_analysis, gap_analysis,created_at,updated_at)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def farm_tb_select():
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    sql_statement = """SELECT * FROM farm;"""
    c.execute(sql_statement)
    data = c.fetchall()
    db_connect.close()
    return data

def farmer_tb_insert(prename, firstname, farmer_gov_id, tel, lastname, gov_id, house_no, vil_name, district_name,
                     postcode, vil_no, subdistrict_name, province_name, farm_id):
    "This function for insert data to farmer's table from farmer's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO farmer(prename, firstname, farmer_gov_id, tel, lastname, gov_id, house_no, vil_name,
                     district_name, postcode, vil_no, subdistrict_name, province_name, farm_id)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    values = (prename, firstname, farmer_gov_id, tel, lastname, gov_id, house_no, vil_name, district_name, postcode,
              vil_no, subdistrict_name, province_name, farm_id)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plant_tb_select():
    "This function for select datas from farm's table to farmer's page"
    db_connect, c = db_connection()
    sql_statement = """SELECT plant_id, plant_name FROM plant ORDER BY plant_name;"""
    c.execute(sql_statement)
    data = c.fetchall()
    db_connect.close()
    return data

def plant_tb_select_pil(params, outfile=None):
    sql_statement = """SELECT img FROM plant
                        WHERE plant_id = %s;"""
    db_connect, c = db_connection()
    c.execute(sql_statement, params)
    row = c.fetchone()
    if row:
        bytes_stream = BytesIO(row[0])
        img = Image.open(bytes_stream)
        return img, row
    return None

def plant_tb_insert(plant_name, img, created_at, updated_at):
    "This function for insert data to farmer's table from farmer's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO plant(plant_name, img, created_at, updated_at)
                     VALUES (%s, %s, %s, %s);"""
    values = (plant_name, img, created_at, updated_at)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plant_tb_update(plant_id,plant_name,plant_img,updated_at):
    "This function fot update data to plant's table from user selected"
    db_connect, c = db_connection()
    sql_statement = """UPDATE plant
                         SET plant_name = %s, img = %s, updated_at = %s
                         WHERE plant_id = %s;"""
    values = (plant_name,plant_img,updated_at,plant_id)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def plant_tb_delete(plant_id):
    "This function fot delete data to plant's table from user selected"
    db_connect, c = db_connection()
    c.execute("DELETE FROM plant WHERE plant_id = %s;", [plant_id])
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
    "This function for select datas from farm's table to farmer's page"
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

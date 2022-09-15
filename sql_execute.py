from postgres_con import db_local_connect

def db_connection():
    "This function connected postgresql database and create cursor for SQL statements support"
    db_connected = db_local_connect()
    c = db_connected.cursor()
    return db_connected,c

def test_select_independent_options():
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    c.execute("""SELECT column_name, column_comment FROM information_schema.columns
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

def farm_tb_insert(vil_name, district_name, postcode, vil_no, subdistrict_name, province_name, farm_quantity,
                   building_quantity, land_privileges, soil_analysis, water_analysis, gap_analysis):
    "This function for insert data to farm's table from farm's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO farm(vil_name, district_name, postcode, vil_no, subdistrict_name, province_name, 
                    farm_quantity, building_quantity, land_privileges, soil_analysis, water_analysis, gap_analysis)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    values = (vil_name, district_name, postcode, vil_no, subdistrict_name, province_name, farm_quantity,
              building_quantity, land_privileges, soil_analysis, water_analysis, gap_analysis)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()

def farm_tb_select():
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    sql_statement = """SELECT farm_id, vil_no, vil_name, subdistrict_name, district_name FROM farm;"""
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
    "This function for select data from farm's table to farmer's page"
    db_connect, c = db_connection()
    sql_statement = """SELECT plant_id, plant_name FROM plant;"""
    c.execute(sql_statement)
    data = c.fetchall()
    db_connect.close()
    return data

def plant_tb_insert(plant_name, img, created_at, updated_at):
    "This function for insert data to farmer's table from farmer's page"
    db_connect, c = db_connection()
    sql_statement = """INSERT INTO plant(plant_name, img, created_at, updated_at)
                     VALUES (%s, %s, %s);"""
    values = (plant_name, img, created_at, updated_at)
    c.execute(sql_statement, values)
    db_connect.commit()
    db_connect.close()



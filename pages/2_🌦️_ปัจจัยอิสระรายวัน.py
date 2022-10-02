import streamlit as st
import time
import pyautogui
from calculate import timestamp
from sql_execute import table_details_select,db_connection,independent_var_duplicate_date_input,variables_query,variable_update,variable_delete
def main():
    st.subheader("ข้อมูลตัวแปรอิสระ (รายวัน)🌦️")
    select_page_tab, create_page_tab, update_page_tab = st.tabs(
        ["📖 เรียกดูข้อมูล", "➕ เพิ่มข้อมูล", "📝 แก้ไขข้อมูล"])
    with select_page_tab:
        select_page()
    with create_page_tab:
        create_page()
    with update_page_tab:
        update_page()

def create_page():
    with st.form("independent_form", clear_on_submit=True):
        table_name = "independent_variables"
        columns = table_details_select(table_name)
        sql_columns_name = ("date_input,")
        n = 0
        for rows in columns:
            if n == 0:
                column_name = ("date_input")
                globals()[column_name] = st.date_input("วันที่").strftime('%Y-%m-%d')
            if rows[2] == "double precision":
                column_name = rows[0]
                globals()[column_name] = float(st.number_input(label=rows[1],min_value=float(0.000), key=rows[0], format=("%f")))
            elif rows[2] == "integer":
                column_name = rows[0]
                globals()[column_name] = int(st.number_input(label=rows[1], min_value=0, step=1, key=rows[0], format=("%d")))
            if n == 0:
                sql_columns_name = sql_columns_name + rows[0]
            else:
                sql_columns_name = sql_columns_name + str(",") + rows[0]
            n+=1
        sql_columns_name = sql_columns_name + str(",created_at,updated_at")
        date_check = independent_var_duplicate_date_input()
        duplicate_date_check = True
        for rows in date_check:
            if date_input == str(rows[0]):
                duplicate_date_check = False
        if st.form_submit_button(label="เพิ่มข้อมูล"):
            if duplicate_date_check == True:
                created_at = str(timestamp())
                updated_at = created_at
                db_connect, c = db_connection()
                sql_statement = """INSERT INTO independent_variables({}) VALUES {};""".format(sql_columns_name,eval(sql_columns_name))
                c.execute(sql_statement)
                db_connect.commit()
                db_connect.close()
                st.success("เพิ่มข้อมูลสำเร็จ!")
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.error("วันที่ซ้ำ! กรุณาเลือกวันที่ใหม่ หรือไปที่เมนูแก้ไข")

def update_page():
    table_name = "independent_variables"
    from_con = "FROM independent_variables"
    join_con = ("")
    on_con = ("")
    where_con = ("")
    order_by_con = "ORDER BY date_input"
    columns = table_details_select(table_name)
    columns_query = ("independent_id,date_input")
    for columns_name in columns:
        columns_query = columns_query + str(",") + columns_name[0]
    update_page_options = variables_query(columns_query,from_con, join_con, on_con, where_con,order_by_con)
    sql_update = ("")
    updated_at = str(timestamp())
    n = 2
    for rows in columns:
        if n == 2:
            date_selected = st.selectbox("วันที่แก้ไข",options=update_page_options,format_func=lambda update_page_options: "{}".format(update_page_options[1]))
        if rows[2] == "double precision":
            column_name = rows[0]
            globals()[column_name] = float(st.number_input(label=(rows[1]), min_value=float(0), format=("%f"), key=(str("edit_")+rows[0]),value=date_selected[n]))
        elif rows[2] == "integer":
            column_name = rows[0]
            globals()[column_name] = int(st.number_input(label=rows[1], min_value=int(0), format=("%d"), step=1, key=(str("edit_")+rows[0]),value=date_selected[n]))
        n += 1
        sql_update = sql_update + rows[0] + str(" = '") + str(eval(rows[0])) + str("', ")
    sql_update = sql_update + str("updated_at = '") + str(updated_at) + str("'")
    where_update = ("WHERE date_input = '{}'".format(date_selected[1]))
    st.markdown("""---""")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        edit_button_clicked = st.button(label="แก้ไขข้อมูล")
    with col4:
        delete_button_clicked = st.button(label="ลบข้อมูล")
    if edit_button_clicked:
        variable_update(table_name,sql_update,where_update)
        st.success("แก้ไขข้อมูลสำเร็จ!")
        time.sleep(1.5)
        st.experimental_rerun()
    elif delete_button_clicked:
        where_delete = ("WHERE independent_id = {}".format(date_selected[0]))
        variable_delete(table_name, where_delete)
        st.error("ลบข้อมูลสำเร็จ!")
        time.sleep(1.5)
        pyautogui.hotkey("ctrl", "F5")
        st.experimental_rerun()

def select_page():
    a = [1, 1, '2022-08-23', '2022-08-23', '2022-08-23', 5]
    b = [2, 1, '2022-08-30', '2022-08-30', '2022-08-30', 5]
    data = (a, b)
    n = 1
    for i in data:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            # st.title("{}. {:03d}".format(n, i[0]))
            pass
        with col2:
            st.text("แผนการปลูก: ")
            st.text("วันที่เริ่มต้นแผนการปลูก: ")
            st.text("วันที่สิ้นสุดแผนการปลูก: ")
            st.text("วันที่ย้ายแผนการปลูก: ")
            st.text("จำนวนเกษตรกร: ")
        with col3:
            st.text(i[1])
            st.text(i[2])
            st.text(i[3])
            st.text(i[4])
            st.text(i[5])
        st.markdown("""---""")
        n += 1

main()

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode
import mysql.connector as mydb

# コネクションの作成
conn = mydb.connect(
    host='www.ryhintl.com',
    port='36000',
    user='smairuser',
    password='smairuser',
    database='smair'
)

cur = conn.cursor(dictionary=True)

st.title("ドキュメントフィードバック")
#docid= st.text_input("DOCID", "13")

#if st.button("取得"):
cur.execute("SELECT * FROM eprag_workflow where active = '1'")

# 全てのデータを取得
rows = cur.fetchall()

#st.write(rows)

# サンプルデータの作成
data = rows
df = pd.DataFrame(data)

# GridOptionsの設定
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=True)  # ページネーションの設定
gb.configure_default_column(editable=True)  # 全ての列を編集可能に設定
grid_options = gb.build()

# AgGridの表示
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=True,
    height=350,
    reload_data=True
)

# 編集後のデータを取得
updated_df = grid_response['data']

# 編集後のデータを表示
st.write("Updated DataFrame:")
st.dataframe(updated_df)

if st.button("更新"):
    try:
        # データフレームの各行をループして更新
        for index, row in updated_df.iterrows():
            sql = "UPDATE eprag_workflow SET feedback = '"+row['feedback']+"', approvedby = '"+row['approvedby'] +"' WHERE id = "+str(row['id'])
            cur.execute(sql)
        conn.commit()
        st.write("データが更新されました。")
    finally:
        cur.close()

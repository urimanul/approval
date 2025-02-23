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

# DOCIDの入力
docid = st.text_input("DOCID", "13")
print(docid)

if st.button("取得"):
    # SQLクエリを実行してデータを取得
    cur.execute("SELECT * FROM eprag_workflow id = "+str(docid))
    rows = cur.fetchall()

    # データフレームに変換
    df = pd.DataFrame(rows)

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
                sql = "UPDATE eprag_workflow SET feedback = '"+row['feedback']+"' WHERE id = 13"
                cur.execute(sql)
            conn.commit()
            st.success("Database updated successfully!")
        except Exception as e:
            st.error(f"Failed to update database: {e}")
        finally:
            conn.close()

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# サンプルデータの作成
data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda'],
    'Age': [28, 24, 35, 32],
    'City': ['New York', 'Paris', 'Berlin', 'London']
}
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

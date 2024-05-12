import streamlit as st
import pandas as pd
import base64
from datetime import datetime

# データフレームを初期化
def init_df():
    data = {'食品名': [], 'エネルギー': [], 'たんぱく質': [], '脂質': [], '炭水化物': [], '食塩': [], '単価': []}
    return pd.DataFrame(data)

# Streamlitアプリを設定
st.title('食品データベース')

# 食品成分の登録フォーム
st.subheader('食品成分の登録')
food_name = st.text_input('食品名')
energy = st.number_input('エネルギー', min_value=0.0, step=0.1, format="%.1f")
protein = st.number_input('たんぱく質', min_value=0.0, step=0.1, format="%.1f")
fat = st.number_input('脂質', min_value=0.0, step=0.1, format="%.1f")
carbs = st.number_input('炭水化物', min_value=0.0, step=0.1, format="%.1f")
salt = st.number_input('食塩', min_value=0.0, step=0.1, format="%.1f")
price = st.number_input('単価', min_value=0.0, step=0.01, format="%.1f")
register_button = st.button('食品成分を登録')

# 登録された食品成分を表示するためのデータフレーム
df = st.session_state.get('food_df', None)

# データフレームがない場合は初期化
if df is None:
    df = init_df()
    st.session_state['food_df'] = df

# 食品成分を登録する関数
def register_food(food_name, energy, protein, fat, carbs, salt, price):
    df.loc[len(df)] = [food_name, energy, protein, fat, carbs, salt, price]
    st.session_state['food_df'] = df

# 登録ボタンがクリックされたら食品成分を登録
if register_button:
    if food_name != '':
        register_food(food_name, energy, protein, fat, carbs, salt, price)

# 登録された食品成分を表示する
st.subheader('登録された食品成分:')
st.write(df)

# 新しい食品成分一覧表を保存する
current_time = datetime.now().strftime('%Y%m%d%H%M%S')
combined_filename = f'combined_food_list_{current_time}.csv'
combined_csv = df.round(1).to_csv(index=False, encoding='shift_jis')  # Shift-JISでエンコード
b64_combined = base64.b64encode(combined_csv.encode('shift_jis')).decode()
href_combined = f'<a href="data:file/csv;base64,{b64_combined}" download="{combined_filename}">登録データと合計のCSVファイルをダウンロード</a>'
st.markdown(href_combined, unsafe_allow_html=True)


# アップロードされたファイルがあれば読み込み、結合して表示
uploaded_file = st.file_uploader('食品成分の一覧表をアップロードする', type=['csv'])
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    combined_df = pd.concat([df, uploaded_df], ignore_index=True)
    st.subheader('新しい食品成分一覧:')
    st.write(combined_df)

    # 結合した食品成分一覧表を保存する
   
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    combined_filename = f'combined_food_list_{current_time}.csv'
    combined_csv = combined_df.round(1).to_csv(index=False, encoding='shift_jis')  # Shift-JISでエンコード
    b64_combined = base64.b64encode(combined_csv.encode('shift_jis')).decode()
    href_combined = f'<a href="data:file/csv;base64,{b64_combined}" download="{combined_filename}">登録データと合計のCSVファイルをダウンロード</a>'
    st.markdown(href_combined, unsafe_allow_html=True)
   
import streamlit as st
import folium
from streamlit_folium import st_folium
from supabase import create_client # 記得加上這行 import

st.set_page_config(layout="wide")
st.title("Dongju Map")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 從雲端讀取 ---
def load_notes():
    response = supabase.table("notes").select("*").execute()
    return response.data

# --- 存入雲端 ---
def save_note(lat, lng, title, note):
    supabase.table("notes").insert({"lat": lat, "lng": lng, "title": title, "note": note}).execute()

# --- 新增這行以獲取資料 ---
all_notes = load_notes()

m = folium.Map(location=[25.9625, 119.9705], zoom_start=16,
               tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
               attr="Esri Satellite")

for n in all_notes:
    folium.Marker([n["lat"], n["lng"]], 
                  popup=f"<b>{n['title']}</b><br>{n['note']}").add_to(m)

output = st_folium(m, width=1200, height=500)

if output["last_clicked"]:
    lat = output["last_clicked"]["lat"]
    lng = output["last_clicked"]["lng"]
    with st.sidebar:
        title = st.text_input("Name")
        note = st.text_area("Note")
        if st.button("Save"):
            # 修改為正確的呼叫方式
            save_note(lat, lng, title, note)
            st.success("Saved!")
            st.rerun() # 加上這行可以讓地圖存檔後馬上顯示新標記
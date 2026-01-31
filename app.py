import streamlit as st
import json
import os
from rapidfuzz import process, fuzz

# --- 页面配置 ---
st.set_page_config(page_title="品牌名转换器", page_icon="👜")

class BrandSystem:
    def __init__(self, json_path):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(base_path, json_path)
        self.brands = self.load_data()

    def load_data(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def translate(self, text):
        if not self.brands or not text:
            return None, 0
        if text in self.brands:
            return self.brands[text], 100
        choices = list(self.brands.keys())
        result = process.extractOne(text, choices, scorer=fuzz.WRatio)
        if result:
            match_name, score, _ = result
            if score > 60:
                return self.brands[match_name], score
        return None, 0

# --- 网页界面展示 ---
st.title("✨ 日语品牌翻译系统")
st.markdown("输入日语品牌名，自动匹配对应的英语官方名称。")

# 加载系统
sys = BrandSystem('brands.json')

# 输入框
user_input = st.text_input("请输入日语品牌名 (例如: シャネル 或 ぶぁれんしあが):", "")

if user_input:
    english_name, confidence = sys.translate(user_input)
    
    if confidence == 100:
        st.success(f"**准确结果：** {english_name}")
        st.balloons() # 成功时撒花庆祝
    elif confidence > 60:
        st.warning(f"🤔 你是不是在找：**{english_name}**?")
        st.caption(f"匹配相似度：{confidence:.0f}%")
    else:
        st.error("❌ 词库中暂无记录，请尝试其他拼写。")

# 侧边栏说明
with st.sidebar:
    st.header("关于词库")
    st.write(f"当前词库共收录品牌：**{len(sys.brands)}** 个")
    if st.checkbox("查看完整品牌清单"):
        st.write(sys.brands)
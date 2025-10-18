# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # 引入 go 模块来做更精细的图表控制

# --- 页面配置 (最好放在最前面) ---
st.set_page_config(
    page_title="书店市场情报看板",
    page_icon="📚",
    layout="wide"  # "centered" 或 "wide"
)

# --- 数据加载 ---
# 使用 @st.cache_data 装饰器来缓存数据，避免每次交互都重新加载，提升性能
@st.cache_data
def load_data():
    df = pd.read_csv('books_data.csv')
    return df

df = load_data()

# --- 页面标题 ---
st.title("📚 Books-to-Scrape 市场情报看板")
st.write("这是一个交互式看板，用于分析 `books.toscrape.com` 网站上的书籍数据。")

# --- 侧边栏过滤器 (Sidebar) ---
st.sidebar.header("筛选器")

# 价格区间滑块
min_price = float(df['价格(£)'].min())
max_price = float(df['价格(£)'].max())
price_range = st.sidebar.slider(
    "选择价格区间 (£)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price) # 默认选择整个区间
)

# 星级多选框
# 确保星级排序正确，从低到高
all_ratings = sorted(df['星级'].unique()) 
selected_ratings = st.sidebar.multiselect(
    "选择星级",
    options=all_ratings,
    default=all_ratings # 默认全选
)

# --- 根据筛选器过滤数据 ---
df_filtered = df[
    (df['价格(£)'] >= price_range[0]) &
    (df['价格(£)'] <= price_range[1]) &
    (df['星级'].isin(selected_ratings))
]

# --- 主页面内容 ---

# 1. 关键指标 (KPIs)
st.header("关键指标概览")
col1, col2, col3 = st.columns(3)
col1.metric("筛选后书籍总数", f"{len(df_filtered)}")
col2.metric("平均价格", f"£{df_filtered['价格(£)'].mean():.2f}")
col3.metric("平均星级", f"{df_filtered['星级'].mean():.2f} ⭐")


# 2. 图表可视化
st.header("数据可视化分析")

# 价格分布直方图
fig_price = px.histogram(
    df_filtered,
    x='价格(£)',
    nbins=30, # 保持箱数不变
    title='书籍价格分布',
    color_discrete_sequence=px.colors.qualitative.Plotly # 使用Plotly默认的颜色序列
)
# 核心改动：为直方图的每个条形添加白色边框
fig_price.update_traces(marker_line_width=1, marker_line_color='white') 
st.plotly_chart(fig_price, use_container_width=True)


# 星级分布条形图
# 确保星级在图表中按数值顺序显示
rating_counts = df_filtered['星级'].value_counts().sort_index().reset_index()
rating_counts.columns = ['星级', '书籍数量'] # 重命名列以便Plotly使用

fig_rating = px.bar(
    rating_counts,
    x='星级',
    y='书籍数量',
    title='书籍星级分布',
    labels={'星级': '星级 (⭐)', '书籍数量': '书籍数量'},
    color='星级', # 根据星级着色
    color_continuous_scale=px.colors.sequential.Viridis # 使用连续颜色渐变
)
# 核心改动：为条形图的每个条形添加白色边框
fig_rating.update_traces(marker_line_width=1, marker_line_color='white')
# 进一步美化：确保X轴是分类的，并增加条形间距
fig_rating.update_xaxes(type='category') 
fig_rating.update_layout(bargap=0.1) # 增加条形之间的间距

st.plotly_chart(fig_rating, use_container_width=True)


# 3. 原始数据表格
st.header("原始数据浏览")
st.dataframe(df_filtered)
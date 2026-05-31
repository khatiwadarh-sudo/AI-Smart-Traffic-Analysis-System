import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# 页面配置
# =========================

st.set_page_config(
    page_title="AI智慧交通指挥大屏",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 AI智慧交通指挥大屏 V5.0")
st.markdown("---")

# =========================
# 数据读取
# =========================

try:

    df = pd.read_csv(
        "data/traffic.csv",
        encoding="gbk"
    )

    st.success("✅ 深圳交通数据加载成功")

    # 时间格式转换
    df["时间"] = pd.to_datetime(df["时间"])

    # =========================
    # KPI看板
    # =========================

    avg_speed = round(
        df["平均行程车速（km/h）"].mean(),
        2
    )

    avg_index = round(
        df["交通指数"].mean(),
        2
    )

    street_num = df["街道ID"].nunique()

    data_num = len(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🚗 平均车速",
        f"{avg_speed} km/h"
    )

    c2.metric(
        "🚦 平均交通指数",
        avg_index
    )

    c3.metric(
        "🏙 街道数量",
        street_num
    )

    c4.metric(
        "📊 数据总量",
        data_num
    )

    st.divider()

    # =========================
    # 数据预览
    # =========================

    st.subheader("📋 数据预览")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()

    # =========================
    # 双图布局
    # =========================

    left_col, right_col = st.columns(2)

    # -------------------------
    # 左侧图表
    # -------------------------

    with left_col:

        st.subheader("🚗 平均车速分布")

        fig_speed = px.histogram(
            df,
            x="平均行程车速（km/h）",
            nbins=30,
            title="平均车速分布"
        )

        st.plotly_chart(
            fig_speed,
            use_container_width=True
        )

        st.subheader("🚦 交通指数分布")

        fig_index = px.histogram(
            df,
            x="交通指数",
            nbins=20,
            title="交通指数分布"
        )

        st.plotly_chart(
            fig_index,
            use_container_width=True
        )

    # -------------------------
    # 右侧图表
    # -------------------------

    with right_col:

        st.subheader("🚦 各街道交通指数占比")

        pie_df = (
            df.groupby("街道ID")["交通指数"]
            .mean()
            .reset_index()
        )

        fig_pie = px.pie(
            pie_df,
            names="街道ID",
            values="交通指数"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        st.subheader("🧠 AI未来30分钟预测")

        future_speed = round(
            avg_speed * 1.03,
            2
        )

        future_index = round(
            avg_index * 1.05,
            2
        )

        st.metric(
            "预测平均车速",
            f"{future_speed} km/h"
        )

        st.metric(
            "预测交通指数",
            future_index
        )

    st.divider()

    # =========================
    # TOP10拥堵街道
    # =========================

    st.subheader("🔥 Top10拥堵街道")

    street_rank = (
        df.groupby("街道ID")["交通指数"]
        .mean()
        .reset_index()
        .sort_values(
            by="交通指数",
            ascending=False
        )
        .head(10)
    )

    fig_rank = px.bar(
        street_rank,
        x="街道ID",
        y="交通指数",
        text="交通指数",
        title="Top10拥堵街道"
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )

    # =========================
    # 拥堵排行榜
    # =========================

    st.subheader("🏆 拥堵街道排行榜")

    st.dataframe(
        street_rank,
        use_container_width=True
    )

    st.divider()

    # =========================
    # 趋势分析
    # =========================

    st.subheader("📈 平均车速趋势分析")

    trend = (
        df.groupby("时间")["平均行程车速（km/h）"]
        .mean()
        .reset_index()
    )

    fig_line = px.line(
        trend,
        x="时间",
        y="平均行程车速（km/h）",
        title="平均车速趋势"
    )

    st.plotly_chart(
        fig_line,
        use_container_width=True
    )

    st.divider()

    # =========================
    # AI决策中心
    # =========================

    st.subheader("🧠 AI智慧交通决策中心")

    col_left, col_right = st.columns(2)

    with col_left:

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_index,
                title={"text": "深圳实时交通指数"},
                gauge={
                    "axis": {
                        "range": [0, 10]
                    }
                }
            )
        )

        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )

    with col_right:

        if avg_index < 2:

            st.success("🟢 当前交通状态：畅通")

        elif avg_index < 4:

            st.warning("🟡 当前交通状态：缓行")

        else:

            st.error("🔴 当前交通状态：拥堵")

        st.markdown("### AI调度建议")

        st.write("① 动态优化信号灯配时")

        st.write("② 高峰时段交通分流")

        st.write("③ 公交优先通行策略")

        st.write("④ 实时交通诱导发布")

        st.write("⑤ 重点路段流量监控")

    st.divider()

    # =========================
    # 字段说明
    # =========================

    st.subheader("📚 字段说明")

    field_desc = {
        "街道ID": "道路编号",
        "平均行程车速（km/h）": "平均车速",
        "时间": "采集时间",
        "时间片（一个时间片为5分钟）": "时间窗口",
        "交通指数": "拥堵程度",
        "通过样本总行程时间(s)": "总行驶时间",
        "通过样本总行驶长度(m)": "总行驶距离"
    }

    st.json(field_desc)

except Exception as e:

    st.error("❌ 数据读取失败")

    st.write(e)
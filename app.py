import streamlit as st
import pandas as pd
from datetime import date, datetime
from textwrap import dedent

#初始化页面
st.set_page_config(
    page_title="我的健康管家",
    page_icon="🌿",
    layout="wide"
)
st.title("🌿我的健康管家")
st.divider()

if "weight_history" not in st.session_state:
    st.session_state.weight_history = []

if "health_score" not in st.session_state:
    st.session_state.health_score = None

if "daily_advice" not in st.session_state:
    st.session_state.daily_advice = []

#侧边栏导航
st.sidebar.title("健康管理中心")

page = st.sidebar.radio(
    "页面导航",
    [
        "👤 个人信息",
        "⚖️ BMI分析"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()
# 如果用户已经填写过信息，就显示摘要
if "user_info" in st.session_state:

    user = st.session_state.user_info

    st.sidebar.subheader("👤 我的档案")

    if user["name"]:
        st.sidebar.write(f"昵称：{user['name']}")

    st.sidebar.write(f"年龄：{user['age']} 岁")
    st.sidebar.write(f"性别：{user['gender']}")
    st.sidebar.write(f"身高：{user['height']} cm")
    st.sidebar.write(f"体重：{user['weight']} kg")

else:
    st.sidebar.info("请先填写个人信息")


if page == "👤 个人信息":
    st.header("👤 创建我的健康档案")
    st.write(
        "请填写或选择你的个人信息"
    )

    # 用户填写过程中不会不断触发整个页面重新运行
    with st.form("user_information_form"):

        st.subheader("个人基本信息")
        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input(
                "昵称",
                placeholder="请输入你的昵称"
            )

        with col2:
            gender = st.selectbox(
                "性别",
                [
                    "男",
                    "女",
                    "你认为你是…"
                ],
                index=None,
                placeholder="请选择"
            )

        with col3:
            age = st.selectbox(
                "年龄",
                list(range(3, 120)),
                index=None,
                placeholder="请选择"
            )

        st.subheader("身体信息")

        col1, col2 = st.columns(2)

        with col1:
            height = st.selectbox(
                "身高（cm）",
                list(range(60, 250)),
                index=None,
                placeholder="请选择"
            )

        with col2:
            weight = st.number_input(
                "体重（kg）",
                min_value=0.0,
                max_value=250.0,
                value=None,
                step=0.5,
                placeholder="请输入你的体重"
            )

        st.subheader("日常生活习惯")

        exercise_level = st.radio(
            "平时运动频率",
            [
                "几乎不运动",
                "每周 1～2 次",
                "每周 3～4 次",
                "每周 5 次以上"
            ],
            index=None,
            horizontal=True
        )

        exercise = st.selectbox(
            "今天运动了多长时间？",
            [
                "今天只是休息啦…",
                "15 分钟",
                "30 分钟",
                "45 分钟",
                "1 小时",
                "1.5 小时",
                "2 小时",
                "我还不累，2小时以上~"
            ],
            index=None,
            placeholder="请选择"
        )

        sleep = st.selectbox(
            "昨晚大约睡了多久？",
            [
                "困鼠了，少于 5 小时",
                "5～6 小时",
                "6～7 小时",
                "7～8 小时",
                "8～9 小时",
                "睡美了，9 小时以上"
            ],
            index=None,
            placeholder="请选择"
        )

        water = st.selectbox(
            "今天大约喝了多少水呀？",
            [
                "嗓子冒烟啦，少于 500 mL",
                "500～1000 mL",
                "1000～1500 mL",
                "1500～2000 mL",
                "2000～2500 mL",
                "水牛来了（？）2500 mL 以上"
            ],
            index=None,
            placeholder="请选择"
        )

        submitted = st.form_submit_button(
            "保存健康档案",
            type="primary",
            use_container_width=True
        )

    # 用户点击保存后
    if submitted:
        if (
            name.strip() == ""
            or gender is None
            or age is None
            or height is None
            or weight is None
            or exercise_level is None
            or exercise is None
            or sleep is None
            or water is None
        ):
            st.error("请填写完整个人信息后再保存")

        else:
            exercise_map = {
                "今天只是休息啦…": 0,
                "15 分钟": 15,
                "30 分钟": 30,
                "45 分钟": 45,
                "1 小时": 60,
                "1.5 小时": 90,
                "2 小时": 120,
                "我还不累，2小时以上~": 120
            }

            sleep_map = {
                "困鼠了，少于 5 小时": 4.5,
                "5～6 小时": 5.5,
                "6～7 小时": 6.5,
                "7～8 小时": 7.5,
                "8～9 小时": 8.5,
                "睡美了，9 小时以上": 9.5
            }

            water_map = {
                "嗓子冒烟啦，少于 500 mL": 400,
                "500～1000 mL": 750,
                "1000～1500 mL": 1250,
                "1500～2000 mL": 1750,
                "2000～2500 mL": 2250,
                "水牛来了（？）2500 mL 以上": 2750
            }

            st.session_state.user_info = {
                "name": name,
                "gender": gender,
                "age": int(age),
                "height": float(height),
                "weight": float(weight),

                "exercise_level": exercise_level,
                "exercise": exercise_map[exercise],

                "sleep": sleep_map[sleep],
                "water": water_map[water]
            }

            st.success("个人健康档案保存成功")

    # 显示已经保存的健康档案
    if "user_info" in st.session_state:
        st.divider()
        st.subheader("健康档案")

        user = st.session_state.user_info

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "年龄",
            f"{user['age']} 岁"
        )

        col2.metric(
            "身高",
            f"{user['height']:.0f} cm"
        )

        col3.metric(
            "体重",
            f"{user['weight']:.1f} kg"
        )

        col4.metric(
            "今日运动",
            f"{user['exercise']} 分钟"
        )


elif page == "⚖️ BMI分析":

    st.header("⚖️ BMI 健康分析")

    # 判断是否已经填写个人信息

    if "user_info" not in st.session_state:

        st.warning(
            "⚠️ 请先前往“个人信息”页面完成健康档案"
        )

        st.info(
            "填写身高和体重后，系统才能计算并分析你的 BMI。"
        )

    else:

        # 获取用户数据
        user = st.session_state.user_info

        height = user["height"]
        weight = user["weight"]

        # 身高 cm 转换为 m
        height_m = height / 100

        #计算 BMI
        bmi = weight / (height_m ** 2)

        st.session_state.bmi = bmi


        # 判断 BMI 状态
        if bmi < 18.5:

            bmi_status = "偏瘦"
            status_icon = "🔵"

        elif bmi < 24:

            bmi_status = "正常"
            status_icon = "🟢"

        elif bmi < 28:

            bmi_status = "超重"
            status_icon = "🟡"

        else:

            bmi_status = "肥胖"
            status_icon = "🔴"

        #身体数据
        st.subheader("📊 我的身体数据")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "身高",
                f"{height:.0f} cm"
            )

        with col2:

            st.metric(
                "体重",
                f"{weight:.1f} kg"
            )

        with col3:

            st.metric(
                "BMI",
                f"{bmi:.2f}"
            )

        # BMI 滑动条
        st.divider()

        st.subheader("📏 BMI 位置")

        # 防止极端 BMI 超出 slider 范围
        display_bmi = max(
            10.0,
            min(float(bmi), 35.0)
        )

        # 显示当前 BMI 状态
        col1, col2 = st.columns([1, 3])

        with col1:

            st.metric(
                "当前 BMI",
                f"{bmi:.1f}"
            )

        with col2:

            if bmi < 18.5:

                st.info(
                    "🔵 当前状态：偏瘦"
                )

            elif bmi < 24:

                st.success(
                    "🟢 当前状态：正常"
                )

            elif bmi < 28:

                st.warning(
                    "🟡 当前状态：超重"
                )

            else:

                st.error(
                    "🔴 当前状态：肥胖"
                )


        # BMI 滑动条组件
        st.slider(
            "BMI 位置",
            min_value=10.0,
            max_value=35.0,
            value=float(round(display_bmi, 1)),
            step=0.1,
            disabled=True,
            key="bmi_position_slider"
        )


        # BMI 区间
        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown("#### 🔵 偏瘦")

            st.caption(
                "BMI < 18.5"
            )

        with col2:

            st.markdown("#### 🟢 正常")

            st.caption(
                "18.5 ～ 23.9"
            )

        with col3:

            st.markdown("#### 🟡 超重")

            st.caption(
                "24.0 ～ 27.9"
            )

        with col4:

            st.markdown("#### 🔴 肥胖")

            st.caption(
                "BMI ≥ 28.0"
            )


        # 参考体重范围
        st.divider()

        st.subheader("🎯 参考体重范围")

        # 正常 BMI 范围：18.5 ~ 23.9
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 23.9 * (height_m ** 2)

        st.write(
            f"按照你的身高 **{height:.0f} cm**，"
            f"正常 BMI 参考范围对应的体重大约为："
        )

        st.markdown(
            f"### {min_weight:.1f} kg ～ {max_weight:.1f} kg"
        )

        st.write(
            f"你当前的体重为 **{weight:.1f} kg**。"
        )


        # 当前体重与参考范围比较
        if weight < min_weight:

            difference = min_weight - weight

            st.info(
                f"当前体重比参考范围下限低约 "
                f"**{difference:.1f} kg**。"
            )

        elif weight > max_weight:

            difference = weight - max_weight

            st.warning(
                f"当前体重比参考范围上限高约 "
                f"**{difference:.1f} kg**。"
            )

        else:

            st.success(
                "✅ 当前体重位于参考体重范围内。"
            )


        # BMI 健康提示
        st.divider()

        st.subheader("💡 BMI 健康提示")

        if bmi < 18.5:

            st.write(
                "🍚 可以关注每天的饮食是否规律，"
                "适当增加优质蛋白质、主食和其他营养食物的摄入。"
            )

            st.write(
                "🏋️ 如果有运动习惯，可以适当加入力量训练，"
                "帮助维持较好的身体状态。"
            )

        elif bmi < 24:

            st.write(
                "✅ 当前 BMI 状态较理想，可以继续保持规律饮食、"
                "适量运动和稳定作息。"
            )

            st.write(
                "🚶 日常保持一定活动量，比短时间进行高强度运动"
                "更有利于形成稳定的健康习惯。"
            )

        elif bmi < 28:

            st.write(
                "🚶 可以尝试增加每天的步行时间，"
                "或进行慢跑、骑行等适合自己的运动。"
            )

            st.write(
                "🥗 饮食方面可以适当减少高糖、高油食品的摄入频率，"
                "保持规律饮食。"
            )

        else:

            st.write(
                "🏃 可以从增加轻度运动开始，例如散步、快走，"
                "再逐渐提高运动时间和频率。"
            )

            st.write(
                "🥗 体重管理更适合长期进行，"
                "不建议通过极端节食等方式追求短期变化。"
            )

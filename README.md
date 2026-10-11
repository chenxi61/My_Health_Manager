# 🌿 我的健康管家

基于 Streamlit 的个性化 BMI 健康管理系统。

## 项目简介

本项目实现了一个简单的个人健康管理 App，用户可以填写个人信息，
系统根据身高、体重等数据完成 BMI 分析，并提供健康状态展示。

## 当前功能

- 👤 个人健康档案填写
  - 昵称
  - 性别
  - 年龄
  - 身高
  - 体重
  - 运动频率
  - 睡眠情况
  - 饮水情况

- ⚖️ BMI 健康分析
  - BMI 自动计算
  - BMI 状态判断
  - BMI 位置滑动展示
  - 正常体重范围计算
  - 个性化健康提示

## 环境要求

Python 3.9+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
streamlit run app.py
```

## 项目结构

```
My_Health_Manager/
│
├── app.py              # 主程序
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
```


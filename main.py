import streamlit as st
import torch
import cv2
import numpy as np
from PIL import Image
import os
import time

@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
    return model

model = load_model()



st.set_page_config(page_title="电动车头盔佩戴检测", layout="wide")

# 侧边栏
st.sidebar.title("选择检测")
detection_type = st.sidebar.selectbox("检测类型", ["图片检测", "视频检测", "摄像头检测"])

# 主区域
st.title("演示时间2023年5月")
st.markdown("---")

if detection_type == "图片检测":
    st.sidebar.subheader("上传图片")
    uploaded_file = st.sidebar.file_uploader("选择图片", type=["png", "jpeg", "jpg"], accept_multiple_files=False)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的图片", use_container_width=True)

        if st.sidebar.button("开始检测"):
            # 将PIL图片转换为numpy数组
            img = np.array(image)
            # 执行检测
            results = model(img)
            # 渲染结果
            results.render()
            # 显示检测结果
            st.image(results.ims[0], caption="检测结果", use_container_width=True)

elif detection_type == "视频检测":
    st.sidebar.subheader("上传视频")
    uploaded_file = st.sidebar.file_uploader("选择视频", type=["mp4", "avi"], accept_multiple_files=False)

    if uploaded_file is not None:
        # 临时保存上传的视频
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.read())

        if st.sidebar.button("开始检测"):
            # 打开视频
            cap = cv2.VideoCapture("temp_video.mp4")
            stframe = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                # 执行检测
                results = model(frame)
                # 渲染结果
                results.render()
                # 显示帧
                stframe.image(results.ims[0], channels="BGR", use_container_width=True)
                time.sleep(0.03)  # 调整帧率

            cap.release()
            os.remove("temp_video.mp4")

elif detection_type == "摄像头检测":
    st.sidebar.subheader("摄像头检测")
    if st.sidebar.button("开始检测"):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # 执行检测
            results = model(frame)
            # 渲染结果
            results.render()
            # 显示帧
            stframe.image(results.ims[0], channels="BGR", use_container_width=True)
            time.sleep(0.03)  # 调整帧率

        cap.release()

st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #e6f7ff;
    }
    .stButton>button {
        background-color: #ff9900;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
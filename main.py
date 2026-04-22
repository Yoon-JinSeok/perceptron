# app.py
import numpy as np
import streamlit as st
import pandas as pd

# ------------------------------
# 활성화 함수 정의하기
# ------------------------------
def activation(y):
    if y > 0:
        return 1
    else:
        return 0

# ------------------------------
# 퍼셉트론 정의하기
# ------------------------------
def perceptron(x, w, b):
    return activation(sum(x * w) + b)

# ------------------------------
# 진리표 입력 데이터
# ------------------------------
xArray = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# ------------------------------
# Streamlit UI 시작
# ------------------------------
st.set_page_config(page_title="퍼셉트론 논리 게이트", page_icon="🧠", layout="wide")
st.title("🧠 퍼셉트론 기반 논리 게이트 시뮬레이터")
st.caption("AND / OR / NAND 게이트의 가중치(w1, w2)와 편향(b)을 직접 설정하고, XOR 게이트의 내부 구성도 드롭박스로 선택해 보세요.")

# ------------------------------
# 사이드바: 각 게이트의 w1, w2, b 입력
# ------------------------------
st.sidebar.header("⚙️ 게이트 파라미터 설정")

st.sidebar.subheader("AND 게이트")
and_w1 = st.sidebar.number_input("AND w1", value=1.0, step=1.0, key="and_w1")
and_w2 = st.sidebar.number_input("AND w2", value=1.0, step=1.0, key="and_w2")
and_b  = st.sidebar.number_input("AND b",  value=-1.0, step=1.0, key="and_b")

st.sidebar.subheader("OR 게이트")
or_w1 = st.sidebar.number_input("OR w1", value=2.0, step=1.0, key="or_w1")
or_w2 = st.sidebar.number_input("OR w2", value=3.0, step=1.0, key="or_w2")
or_b  = st.sidebar.number_input("OR b",  value=-1.0, step=1.0, key="or_b")

st.sidebar.subheader("NAND 게이트")
nand_w1 = st.sidebar.number_input("NAND w1", value=-1.0, step=1.0, key="nand_w1")
nand_w2 = st.sidebar.number_input("NAND w2", value=-1.0, step=1.0, key="nand_w2")
nand_b  = st.sidebar.number_input("NAND b",  value=2.0,  step=1.0, key="nand_b")

# ------------------------------
# 게이트 함수 정의 (사용자 입력 적용)
# ------------------------------
def AndGate(x):
    w = np.array([and_w1, and_w2])
    b = and_b
    return perceptron(x, w, b)

def OrGate(x):
    w = np.array([or_w1, or_w2])
    b = or_b
    return perceptron(x, w, b)

def NandGate(x):
    w = np.array([nand_w1, nand_w2])
    b = nand_b
    return perceptron(x, w, b)

# ------------------------------
# XOR 게이트: 드롭박스 선택
# ------------------------------
st.sidebar.subheader("XOR 게이트 구성")
gate_options = {
    "AndGate": AndGate,
    "OrGate": OrGate,
    "NandGate": NandGate,
}

y1_choice     = st.sidebar.selectbox("y1 =", list(gate_options.keys()), index=2)  # 기본 NandGate
y2_choice     = st.sidebar.selectbox("y2 =", list(gate_options.keys()), index=1)  # 기본 OrGate
return_choice = st.sidebar.selectbox("return =", list(gate_options.keys()), index=0)  # 기본 AndGate

def XorGate(x):
    y1 = gate_options[y1_choice](x)
    y2 = gate_options[y2_choice](x)
    y = np.array([y1, y2])
    return gate_options[return_choice](y)

# ------------------------------
# 결과 표 생성
# ------------------------------
rows = []
for x in xArray:
    rows.append({
        "x1": int(x[0]),
        "x2": int(x[1]),
        "AND":  AndGate(x),
        "OR":   OrGate(x),
        "NAND": NandGate(x),
        "XOR":  XorGate(x),
    })
df = pd.DataFrame(rows)

st.subheader("📊 진리표 결과")
st.dataframe(df, use_container_width=True)

# ------------------------------
# 현재 설정 요약
# ------------------------------
with st.expander("🔎 현재 설정 값 보기"):
    st.markdown(f"""
    - **AND**: w = [{and_w1}, {and_w2}], b = {and_b}
    - **OR**: w = [{or_w1}, {or_w2}], b = {or_b}
    - **NAND**: w = [{nand_w1}, {nand_w2}], b = {nand_b}
    - **XOR**:
        - y1 = `{y1_choice}(x)`
        - y2 = `{y2_choice}(x)`
        - return = `{return_choice}([y1, y2])`
    """)

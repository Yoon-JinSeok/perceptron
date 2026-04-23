# app.py
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="퍼셉트론 논리 게이트 단계별 학습", page_icon="🧠", layout="wide")
st.title("🧠 퍼셉트론 기반 논리 게이트 — 단계별 실행")

# ======================================================
# 공통 함수 (1단계에서 소개)
# ======================================================
def activation(y):
    if y > 0:
        return 1
    else:
        return 0

def perceptron(x, w, b):
    return activation(sum(x * w) + b)

xArray = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# 진리표 출력용 헬퍼
def show_truth_table(gate_func, gate_name):
    rows = []
    for x in xArray:
        rows.append({"x1": int(x[0]), "x2": int(x[1]), gate_name: gate_func(x)})
    st.dataframe(pd.DataFrame(rows), use_container_width=False)

# ======================================================
# 탭 구성
# ======================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ 기본 코드",
    "2️⃣ AND 게이트",
    "3️⃣ OR 게이트",
    "4️⃣ NAND 게이트",
    "5️⃣ XOR 게이트",
])

# ------------------------------------------------------
# 1단계: 활성화 함수 / 퍼셉트론 / 진리표 코드 확인
# ------------------------------------------------------
with tab1:
    st.header("1단계. 활성화 함수, 퍼셉트론, 진리표")
    st.code('''
import numpy as np

# 활성화 함수 정의
def activation(y):
    if y > 0:
        return 1
    else:
        return 0

# 퍼셉트론 정의
def perceptron(x, w, b):
    return activation(sum(x*w) + b)

# 진리표 입력 데이터
xArray = np.array([[0,0], [0,1], [1,0], [1,1]])
''', language="python")

    st.subheader("📋 진리표 입력 데이터")
    st.dataframe(pd.DataFrame(xArray, columns=["x1", "x2"]), use_container_width=False)
    st.info("다음 단계(2단계)로 이동하여 AND 게이트를 설정해 보세요.")

# ------------------------------------------------------
# 2단계: AND 게이트
# ------------------------------------------------------
with tab2:
    st.header("2단계. AND 게이트")
    st.code('''
def AndGate(x):
    w = np.array([w1, w2])
    b = b
    return perceptron(x, w, b)
''', language="python")

    st.subheader("🔧 w1, w2, b 입력")
    c1, c2, c3 = st.columns(3)
    with c1:
        and_w1 = st.number_input("w1", value=0.0, step=1.0, key="and_w1")
    with c2:
        and_w2 = st.number_input("w2", value=0.0, step=1.0, key="and_w2")
    with c3:
        and_b  = st.number_input("b",  value=0.0, step=1.0, key="and_b")

    def AndGate(x):
        w = np.array([and_w1, and_w2])
        b = and_b
        return perceptron(x, w, b)

    st.session_state["AndGate"] = AndGate

    st.subheader("✅ AND 게이트 출력값")
    show_truth_table(AndGate, "AND")

# ------------------------------------------------------
# 3단계: OR 게이트
# ------------------------------------------------------
with tab3:
    st.header("3단계. OR 게이트")
    st.code('''
def OrGate(x):
    w = np.array([w1, w2])
    b = b
    return perceptron(x, w, b)
''', language="python")

    st.subheader("🔧 w1, w2, b 입력")
    c1, c2, c3 = st.columns(3)
    with c1:
        or_w1 = st.number_input("w1", value=0.0, step=1.0, key="or_w1")
    with c2:
        or_w2 = st.number_input("w2", value=0.0, step=1.0, key="or_w2")
    with c3:
        or_b  = st.number_input("b",  value=0.0, step=1.0, key="or_b")

    def OrGate(x):
        w = np.array([or_w1, or_w2])
        b = or_b
        return perceptron(x, w, b)

    st.session_state["OrGate"] = OrGate

    st.subheader("✅ OR 게이트 출력값")
    show_truth_table(OrGate, "OR")

# ------------------------------------------------------
# 4단계: NAND 게이트
# ------------------------------------------------------
with tab4:
    st.header("4단계. NAND 게이트")
    st.code('''
def NandGate(x):
    w = np.array([w1, w2])
    b = b
    return perceptron(x, w, b)
''', language="python")

    st.subheader("🔧 w1, w2, b 입력")
    c1, c2, c3 = st.columns(3)
    with c1:
        nand_w1 = st.number_input("w1", value=0.0, step=1.0, key="nand_w1")
    with c2:
        nand_w2 = st.number_input("w2", value=0.0, step=1.0, key="nand_w2")
    with c3:
        nand_b  = st.number_input("b",  value=0.0, step=1.0, key="nand_b")

    def NandGate(x):
        w = np.array([nand_w1, nand_w2])
        b = nand_b
        return perceptron(x, w, b)

    st.session_state["NandGate"] = NandGate

    st.subheader("✅ NAND 게이트 출력값")
    show_truth_table(NandGate, "NAND")

# ------------------------------------------------------
# 5단계: XOR 게이트
# ------------------------------------------------------
with tab5:
    st.header("5단계. XOR 게이트")
    st.code('''
def XorGate(x):
    y1 = NandGate(x)   # ← 드롭다운으로 선택
    y2 = OrGate(x)     # ← 드롭다운으로 선택
    y  = np.array([y1, y2])
    return AndGate(y)  # ← 드롭다운으로 선택
''', language="python")

    # 앞 단계에서 설정이 안 되었을 경우 경고
    required = ["AndGate", "OrGate", "NandGate"]
    missing = [g for g in required if g not in st.session_state]
    if missing:
        st.warning(f"⚠️ 먼저 다음 단계를 실행해 주세요: {', '.join(missing)}")
    else:
        st.subheader("🔽 y1, y2, return 드롭다운 선택")
        gate_options = {
            "AndGate":  st.session_state["AndGate"],
            "OrGate":   st.session_state["OrGate"],
            "NandGate": st.session_state["NandGate"],
        }

        c1, c2, c3 = st.columns(3)
        with c1:
            y1_choice = st.selectbox("y1 =", list(gate_options.keys()), index=0, key="xor_y1")
        with c2:
            y2_choice = st.selectbox("y2 =", list(gate_options.keys()), index=0, key="xor_y2")
        with c3:
            ret_choice = st.selectbox("return =", list(gate_options.keys()), index=0, key="xor_ret")

        def XorGate(x):
            y1 = gate_options[y1_choice](x)
            y2 = gate_options[y2_choice](x)
            y  = np.array([y1, y2])
            return gate_options[ret_choice](y)

        st.markdown(f"""
        **현재 구성**
        - y1 = `{y1_choice}(x)`
        - y2 = `{y2_choice}(x)`
        - return = `{ret_choice}([y1, y2])`
        """)

        st.subheader("✅ XOR 게이트 출력값")
        show_truth_table(XorGate, "XOR")

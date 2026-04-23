# app.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import streamlit as st


st.set_page_config(page_title="퍼셉트론 논리 게이트 단계별 학습", page_icon="🧠", layout="wide")
st.title("🧠 퍼셉트론 기반 논리 게이트 — 단계별 실행")

# ======================================================
# 공통 함수
# ======================================================
def activation(y):
    if y > 0:
        return 1
    else:
        return 0

def perceptron(x, w, b):
    return activation(sum(x * w) + b)

xArray = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# ------------------------------------------------------
# 진리표 출력 헬퍼
# ------------------------------------------------------
def show_truth_table(gate_func, gate_name):
    rows = []
    for x in xArray:
        rows.append({"x1": int(x[0]), "x2": int(x[1]), gate_name: gate_func(x)})
    st.dataframe(pd.DataFrame(rows), use_container_width=False)

# ------------------------------------------------------
# 좌표평면 시각화 헬퍼
#   - 점: 출력 0 → 파란색, 출력 1 → 빨간색
#   - 직선: x1*w1 + x2*w2 + b = 0
# ------------------------------------------------------
def plot_gate_plane(gate_func, title, w1=None, w2=None, b=None, draw_line=True):
    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    # 점 그리기
    for x in xArray:
        out = gate_func(x)
        color = "red" if out == 1 else "blue"
        ax.scatter(x[0], x[1], color=color, s=250, zorder=3,
                   edgecolor="black", linewidth=1.2)
        ax.annotate(f"({x[0]},{x[1]}) → {out}", (x[0], x[1]),
                    textcoords="offset points", xytext=(10, 10), fontsize=10)

    # 결정 경계 직선 그리기
    if draw_line and (w1 is not None) and (w2 is not None) and (b is not None):
        xs = np.linspace(-0.5, 1.5, 200)
        if w2 != 0:
            ys = -(w1 * xs + b) / w2
            ax.plot(xs, ys, "g-", linewidth=2,
                    label=f"{w1}·x1 + {w2}·x2 + {b} = 0")
        elif w1 != 0:
            xv = -b / w1
            ax.axvline(xv, color="green", linewidth=2,
                       label=f"x1 = {xv}")
        else:
            # w1 = w2 = 0: 직선 없음
            ax.text(0.5, -0.35, "※ w1=w2=0 → 직선 없음",
                    ha="center", color="green", fontsize=10)

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title(title)
    if draw_line:
        ax.legend(loc="upper right", fontsize=9)
    st.pyplot(fig)
    plt.close(fig)

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
# 1단계
# ------------------------------------------------------
with tab1:
    st.header("1단계. 활성화 함수, 퍼셉트론, 진리표")
    st.code('''
import numpy as np

def activation(y):
    if y > 0:
        return 1
    else:
        return 0

def perceptron(x, w, b):
    return activation(sum(x*w) + b)

xArray = np.array([[0,0], [0,1], [1,0], [1,1]])
''', language="python")

    st.subheader("📋 진리표 입력 데이터")
    st.dataframe(pd.DataFrame(xArray, columns=["x1", "x2"]), use_container_width=False)
    st.info("다음 단계(2단계)로 이동하여 AND 게이트를 설정해 보세요.")

# ------------------------------------------------------
# 2단계: AND
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
    col_t, col_p = st.columns([1, 1])
    with col_t:
        show_truth_table(AndGate, "AND")
    with col_p:
        plot_gate_plane(AndGate, "AND", and_w1, and_w2, and_b)

# ------------------------------------------------------
# 3단계: OR
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
    col_t, col_p = st.columns([1, 1])
    with col_t:
        show_truth_table(OrGate, "OR")
    with col_p:
        plot_gate_plane(OrGate, "OR", or_w1, or_w2, or_b)

# ------------------------------------------------------
# 4단계: NAND
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
    col_t, col_p = st.columns([1, 1])
    with col_t:
        show_truth_table(NandGate, "NAND")
    with col_p:
        plot_gate_plane(NandGate, "NAND", nand_w1, nand_w2, nand_b)

# ------------------------------------------------------
# 5단계: XOR
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
        col_t, col_p = st.columns([1, 1])
        with col_t:
            show_truth_table(XorGate, "XOR")
        with col_p:
            # XOR은 단일 선형 분리가 불가능하므로 점만 표시
            plot_gate_plane(XorGate, "XOR (선형 분리 불가)", draw_line=False)
            st.caption("※ XOR은 하나의 직선으로 분리할 수 없으므로 결정 경계선을 그리지 않습니다.")

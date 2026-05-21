import streamlit as st
import base64

st.set_page_config(page_title="Aero Chat", layout="wide")


# ================= BACKGROUND + THEME =================
def set_bg_from_local(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>

        /* ===== BACKGROUND ===== */
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* ===== GLASS PANELS (LEFT + RIGHT) ===== */
        div[data-testid="column"] {{
            background: rgba(10, 10, 30, 0.22);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-radius: 16px;
            padding: 18px;
            margin: 10px;
            border: 1px solid rgba(168, 85, 247, 0.2);
        }}

        /* LEFT PANEL BLUE BORDER */
        div[data-testid="column"]:nth-child(1) {{
            border-right: 2px solid rgba(59, 130, 246, 0.4);
        }}

        /* RIGHT PANEL VIOLET BORDER */
        div[data-testid="column"]:nth-child(2) {{
            border-left: 2px solid rgba(168, 85, 247, 0.4);
        }}

        /* ===== HEADINGS (GALAXY GRADIENT) ===== */
        h1, h2, h3 {{
            background: linear-gradient(90deg, #3b82f6, #a855f7, #0b0f2a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }}

        /* ===== TEXT GLOW ===== */
        p, div, span, label {{
            color: #d6dcff !important;
            text-shadow:
                0 0 6px rgba(59, 130, 246, 0.25),
                0 0 10px rgba(168, 85, 247, 0.15),
                1px 1px 2px rgba(0, 0, 0, 0.8);
        }}

        /* ===== SELECTBOX ===== */
        div[data-baseweb="select"] > div {{
            background: rgba(10, 10, 30, 0.4) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            color: #e6eaff !important;
        }}

        /* ===== BUTTONS ===== */
        button {{
            background: linear-gradient(90deg, #3b82f6, #a855f7);
            color: white !important;
            border-radius: 10px;
            border: none;
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.3);
            transition: 0.3s;
        }}

        button:hover {{
            transform: scale(1.03);
            box-shadow: 0 0 18px rgba(59, 130, 246, 0.5);
        }}

        /* ===== CHAT TEXT ===== */
        .stMarkdown {{
            color: #cfd6ff !important;
        }}

        /* ===== 🌌 TRANSPARENT CHAT INPUT (FIXED + GLASS) ===== */
        div[data-testid="stTextInput"] input {{
            background: rgba(10, 10, 30, 0.35) !important;
            border: 1px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 10px;
            color: #e6eaff !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}

        div[data-testid="stTextInput"] input::placeholder {{
            color: rgba(214, 220, 255, 0.6) !important;
        }}

        div[data-testid="stTextInput"] input:focus {{
            border: 1px solid rgba(59, 130, 246, 0.7) !important;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
            outline: none;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ================= APPLY BACKGROUND =================
set_bg_from_local(r"aeroenv\4686241.jpg")


# ================= LAYOUT =================
left, right = st.columns([1, 2])


# ================= LEFT PANEL =================
with left:
    st.markdown("## ⚙️ Settings")

    theme = st.selectbox("Theme", ["Galaxy", "Dark", "Light"])
    model = st.selectbox("Model", ["Gemini", "GPT-style mock", "Custom LLM"])

    st.checkbox("Enable memory")
    st.checkbox("Show typing animation")

    st.markdown("---")
    st.markdown("## 📜 Chat History")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages:
        for i, (role, msg) in enumerate(st.session_state.messages):
            st.markdown(f"{i+1}. **{role}:** {msg}")
    else:
        st.info("No history yet.")


# ================= RIGHT PANEL =================
with right:
    st.markdown("## 💬 Chat Window")

    user_input = st.text_input("Type your message")

    if st.button("Send"):
        if user_input:
            st.session_state.messages.append(("You", user_input))
            st.session_state.messages.append(("AI", "This is a demo reply 🤖"))

    for role, msg in st.session_state.messages:
        if role == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 AI:** {msg}")
import streamlit as st
import requests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
matplotlib.use("Agg")

st.set_page_config(
    page_title="TalentIQ · AI Recruitment",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
#  DEEP OCEAN THEME  — Rich Indigo + Violet + Cyan
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* ─── Core palette ─── */
:root {
    --bg0:    #0a0b14;
    --bg1:    #0d0f1c;
    --bg2:    #111428;
    --card:   #151829;
    --card2:  #1a1d32;
    --border: #252840;
    --hi:     #7c6af7;        /* primary violet */
    --hi2:    #00d4ff;        /* cyan accent */
    --hi3:    #f857a6;        /* pink accent */
    --hi4:    #43e97b;        /* green accent */
    --text:   #e8e9f8;
    --muted:  #6b6f8e;
    --r:      14px;
}

/* ─── Base ─── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.2rem 3rem 5rem !important;
    max-width: 1400px !important;
    transition: all .3s ease !important;
}

/* ─── RICH BACKGROUND  ─── */
.stApp {
    background:
        radial-gradient(ellipse 90% 60% at -5% -5%,   #2d1b69 0%, transparent 50%),
        radial-gradient(ellipse 70% 55% at 105% 105%,  #0d3360 0%, transparent 50%),
        radial-gradient(ellipse 50% 40% at 50%  50%,   #1a0a3d 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80%  10%,   #1d0042 0%, transparent 45%),
        linear-gradient(160deg, #0a0b14 0%, #0d0f1e 50%, #080d1a 100%) !important;
}

/* animated shimmer lines */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        linear-gradient(105deg, transparent 40%, rgba(124,106,247,.04) 50%, transparent 60%),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 79px,
            rgba(124,106,247,.03) 80px
        ),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 79px,
            rgba(0,212,255,.025) 80px
        );
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg,
            rgba(45,27,105,.6) 0%,
            rgba(13,19,40,.95) 40%,
            rgba(10,11,20,.98) 100%) !important;
    border-right: 1px solid rgba(124,106,247,.2) !important;
    backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }

/* nav items */
[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center !important;
    padding: 0.6rem 1rem !important; border-radius: 10px !important;
    color: var(--muted) !important; font-weight: 500 !important;
    font-size: 0.88rem !important; letter-spacing: .01em !important;
    transition: all .2s !important; cursor: pointer !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(124,106,247,.15) !important;
    color: var(--text) !important;
    border-color: rgba(124,106,247,.25) !important;
}
[data-testid="stSidebar"] .stRadio { gap: 3px !important; }

/* ─── Keep sidebar always visible ─── */
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"][aria-expanded="false"] {
    transform: none !important;
    min-width: 240px !important;
    width: 240px !important;
}

/* ─── Main content always fills remaining space ─── */
.main .block-container {
    padding: 2.2rem 3rem 5rem !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* ─── When sidebar is collapsed, expand content to full width ─── */
[data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container,
[data-testid="stSidebar"][aria-expanded="false"] ~ section .block-container {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ─── Sidebar toggle button — make it glow ─── */
button[data-testid="collapsedControl"] {
    background: rgba(124,106,247,.2) !important;
    border: 1px solid rgba(124,106,247,.4) !important;
    border-radius: 50% !important;
    color: #a78bfa !important;
}

/* ─── Smooth transition on content area ─── */
.main { transition: all .3s ease !important; }

/* ─── Responsive: narrow / mobile screens ─── */
@media (max-width: 900px) {
    .block-container { padding: 1rem 1rem 3rem !important; }
    [data-testid="stSidebar"] { min-width: 200px !important; width: 200px !important; }
}
@media (max-width: 640px) {
    [data-testid="stSidebar"] { min-width: 160px !important; width: 160px !important; }
    .block-container { padding: .8rem .8rem 2rem !important; }
}

/* ─── ALL INPUTS ─── */
input, textarea,
.stTextInput input, .stTextArea textarea {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}
input:focus, textarea:focus,
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--hi) !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,.22) !important;
    outline: none !important;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, #7c6af7 0%, #a78bfa 50%, #c084fc 100%) !important;
    border: none !important; border-radius: 10px !important;
    color: #fff !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; font-size: .88rem !important;
    letter-spacing: .03em !important; padding: .55rem 1.4rem !important;
    box-shadow: 0 4px 24px rgba(124,106,247,.45) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 32px rgba(124,106,247,.65) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: none !important; }

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card) !important;
    border-radius: 12px !important; padding: 4px !important;
    gap: 4px !important; border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important; color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important; padding: .5rem 1.4rem !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
    color: #fff !important; font-weight: 700 !important;
    box-shadow: 0 2px 12px rgba(124,106,247,.4) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--card) !important;
    border-radius: 0 12px 12px 12px !important;
    padding: 1.6rem !important;
    border: 1px solid var(--border) !important; border-top: none !important;
}

/* ─── METRICS ─── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--card) 0%, var(--card2) 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important; padding: 1.3rem 1.6rem !important;
    position: relative; overflow: hidden;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stMetric"]::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #7c6af7, #00d4ff, #f857a6);
}
[data-testid="stMetric"]:hover {
    border-color: rgba(124,106,247,.5) !important;
    box-shadow: 0 8px 32px rgba(124,106,247,.2) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important; font-size: .72rem !important;
    text-transform: uppercase !important; letter-spacing: .09em !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important; font-weight: 800 !important;
    font-size: 2rem !important; letter-spacing: -.02em !important;
}

/* ─── DATAFRAME ─── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important; overflow: hidden !important;
}
.dvn-scroller { background: var(--card) !important; }

/* ─── ALERTS ─── */
div[data-testid="stAlert"] {
    border-radius: 11px !important; font-size: .87rem !important;
}
.stSuccess {
    background: rgba(67,233,123,.08) !important;
    border-left: 4px solid #43e97b !important;
    border-radius: 11px !important;
}
.stInfo {
    background: rgba(124,106,247,.09) !important;
    border-left: 4px solid var(--hi) !important;
    border-radius: 11px !important;
}
.stWarning {
    background: rgba(251,191,36,.08) !important;
    border-left: 4px solid #fbbf24 !important;
    border-radius: 11px !important;
}
.stError {
    background: rgba(248,87,166,.09) !important;
    border-left: 4px solid var(--hi3) !important;
    border-radius: 11px !important;
}

/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] > div {
    background: var(--card2) !important;
    border: 2px dashed rgba(124,106,247,.35) !important;
    border-radius: var(--r) !important; transition: all .2s !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--hi) !important;
    background: rgba(124,106,247,.07) !important;
}

/* ─── SELECT ─── */
.stSelectbox div[data-baseweb="select"] > div {
    background: var(--card2) !important; border-color: var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
}

/* ─── SLIDER ─── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--hi) !important;
    box-shadow: 0 0 0 4px rgba(124,106,247,.25) !important;
}

/* ─── DATE / TIME ─── */
.stDateInput input, .stTimeInput input {
    background: var(--card2) !important; border-color: var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
}

/* ─── CHECKBOX ─── */
.stCheckbox label { color: var(--muted) !important; font-size: .88rem !important; }

/* ─── SPINNER ─── */
.stSpinner > div { border-top-color: var(--hi) !important; }

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg0); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--hi); }
hr { border-color: var(--border) !important; opacity: 1 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  REUSABLE COMPONENTS
# ─────────────────────────────────────────
def page_header(icon, title, subtitle=""):
    sub_html = (
        f"<p style='margin:2px 0 0;color:#6b6f8e;font-size:.83rem;letter-spacing:.01em;'>{subtitle}</p>"
        if subtitle else ""
    )
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:1.1rem;
        padding:1.6rem 0 1.2rem;
        border-bottom:1px solid rgba(124,106,247,.2);
        margin-bottom:2rem;
    ">
        <div style="
            width:50px; height:50px; border-radius:15px; flex-shrink:0;
            background:linear-gradient(135deg,rgba(124,106,247,.4) 0%,rgba(0,212,255,.15) 100%);
            border:1px solid rgba(124,106,247,.45);
            display:flex; align-items:center; justify-content:center;
            font-size:1.4rem;
            box-shadow:0 4px 20px rgba(124,106,247,.3);
        ">{icon}</div>
        <div>
            <h1 style="
                margin:0; font-family:'Outfit',sans-serif;
                font-size:1.7rem; font-weight:900; letter-spacing:-.03em;
                background:linear-gradient(120deg,#e8e9f8 20%,#a78bfa 60%,#00d4ff 100%);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            ">{title}</h1>
            {sub_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(icon, label, value, color="#7c6af7", sublabel=""):
    sub_html   = f"<div style='font-size:.75rem;color:#6b6f8e;margin-top:.3rem;'>{sublabel}</div>" if sublabel else ""
    bar_color  = color                          # top accent bar
    icon_bg    = f"rgba(124,106,247,.12)"       # default subtle bg
    icon_bdr   = f"rgba(124,106,247,.25)"       # default border
    # map per color so no hex-concat happens
    rgba_map = {
        "#7c6af7": ("rgba(124,106,247,.12)", "rgba(124,106,247,.28)"),
        "#00d4ff": ("rgba(0,212,255,.12)",   "rgba(0,212,255,.28)"),
        "#a78bfa": ("rgba(167,139,250,.12)", "rgba(167,139,250,.28)"),
        "#43e97b": ("rgba(67,233,123,.12)",  "rgba(67,233,123,.28)"),
        "#f857a6": ("rgba(248,87,166,.12)",  "rgba(248,87,166,.28)"),
        "#fbbf24": ("rgba(251,191,36,.12)",  "rgba(251,191,36,.28)"),
    }
    icon_bg, icon_bdr = rgba_map.get(color, ("rgba(124,106,247,.12)", "rgba(124,106,247,.28)"))
    html = (
        '<div style="background:linear-gradient(135deg,#151829 0%,#1a1d32 100%);'
        'border:1px solid #252840;border-radius:13px;padding:.9rem 1rem;'
        'position:relative;overflow:hidden;">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:3px;'
        f'background:linear-gradient(90deg,{bar_color},transparent);"></div>'
        '<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px;">'
        '<div style="min-width:0;flex:1;">'
        f'<div style="font-size:.62rem;color:#6b6f8e;text-transform:uppercase;'
        f'letter-spacing:.07em;font-weight:600;margin-bottom:.3rem;'
        f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{label}</div>'
        f'<div style="font-size:1.7rem;font-weight:900;color:#e8e9f8;'
        f'letter-spacing:-.03em;line-height:1.1;">{value}</div>'
        f'{sub_html}'
        '</div>'
        f'<div style="width:36px;height:36px;border-radius:10px;flex-shrink:0;'
        f'background:{icon_bg};border:1px solid {icon_bdr};'
        f'display:flex;align-items:center;justify-content:center;font-size:1rem;">'
        f'{icon}</div>'
        '</div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section_title(text):
    st.markdown(
        f'<p style="font-family:\'Outfit\',sans-serif;font-weight:700;font-size:.95rem;'
        f'color:#e8e9f8;margin:.9rem 0 .5rem;display:flex;align-items:center;gap:.5rem;">'
        f'{text}</p>',
        unsafe_allow_html=True
    )


def render_results_table(results):
    medal = ["🥇","🥈","🥉"]
    rows  = ""
    for i, r in enumerate(results):
        score     = r["Score"]
        pct       = int(score * 100)
        bar_color = "#43e97b" if score >= .6 else ("#a78bfa" if score >= .35 else "#f857a6")
        rank_html = f'<span style="font-size:1.3rem;">{medal[i]}</span>' if i < 3 \
                    else f'<span style="color:#6b6f8e;font-weight:700;font-size:.85rem;">#{i+1}</span>'
        name      = r["Candidate"].replace(".pdf","").replace("_"," ")

        def pills(text, bg, fg, bdr):
            pts = [s.strip() for s in text.split(",") if s.strip()]
            if not pts:
                return "<span style='color:#6b6f8e;font-size:.76rem;'>—</span>"
            return "".join(
                f'<span style="display:inline-block;margin:2px 3px 2px 0;padding:2px 9px;'
                f'border-radius:999px;background:{bg};color:{fg};'
                f'border:1px solid {bdr};font-size:.72rem;font-weight:600;">{p}</span>'
                for p in pts
            )

        rows += (
            '<div style="display:grid;grid-template-columns:46px 1.2fr 110px 1fr 1fr;'
            'gap:10px;align-items:center;padding:12px 16px;margin-bottom:7px;'
            'background:linear-gradient(135deg,#151829,#1a1d32);'
            'border:1px solid #252840;border-radius:12px;">'
            f'<div style="text-align:center;">{rank_html}</div>'
            f'<div style="font-weight:700;font-size:.92rem;color:#e8e9f8;">{name}</div>'
            '<div>'
            f'<div style="font-weight:800;font-size:1.05rem;color:{bar_color};'
            f'margin-bottom:5px;letter-spacing:-.01em;">{score:.3f}</div>'
            '<div style="height:5px;background:#252840;border-radius:999px;overflow:hidden;">'
            f'<div style="width:{pct}%;height:100%;border-radius:999px;background:{bar_color};"></div>'
            '</div></div>'
            f'<div style="line-height:1.9;">{pills(r["Matched Skills"],"rgba(67,233,123,.12)","#43e97b","rgba(67,233,123,.3)")}</div>'
            f'<div style="line-height:1.9;">{pills(r["Missing Skills"],"rgba(248,87,166,.12)","#f857a6","rgba(248,87,166,.3)")}</div>'
            '</div>'
        )

    header = """
    <div style="
        display:grid; grid-template-columns:46px 1.2fr 110px 1fr 1fr;
        gap:10px; padding:6px 16px 9px;
        font-size:.69rem; color:#6b6f8e;
        text-transform:uppercase; letter-spacing:.09em; font-weight:700;
        border-bottom:1px solid #252840; margin-bottom:8px;
    ">
        <span>#</span><span>Candidate</span><span>Score</span>
        <span>Matched Skills</span><span>Missing Skills</span>
    </div>"""

    st.markdown(f"""
    <div style="
        background:#111428; border:1px solid #252840;
        border-radius:14px; padding:12px;
    ">{header}{rows}</div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
for k, v in [
    ("login",False),("role",None),
    ("username",None),("token",None),
    ("match_results",[]),("reset_counter",0),
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────
#  API
# ─────────────────────────────────────────
def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def safe_get(url):
    try:
        r = requests.get(url, headers=get_headers())
        return r.json() if r.status_code == 200 else None
    except Exception:
        st.error("⚠️ Backend unreachable")

def safe_post(url, data=None, files=None):
    try:
        r = requests.post(url, data=data, files=files, headers=get_headers())
        if r.status_code == 200: return r.json()
        st.error(r.text); return None
    except Exception as e:
        st.error(str(e))


# ─────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────
if not st.session_state.login:

    st.markdown("""
    <div style="text-align:center;padding:4rem 0 2.5rem;">
        <div style="
            display:inline-flex;align-items:center;justify-content:center;
            width:76px;height:76px;border-radius:24px;
            background:linear-gradient(135deg,#7c6af7 0%,#a78bfa 60%,#00d4ff 100%);
            font-size:2.2rem;margin-bottom:1.2rem;
            box-shadow:0 12px 50px rgba(124,106,247,.55);
        ">🧠</div>
        <h1 style="
            font-family:'Outfit',sans-serif;font-size:3.2rem;font-weight:900;margin:0;
            background:linear-gradient(120deg,#e8e9f8 20%,#a78bfa 60%,#00d4ff 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:-.04em;
        ">TalentIQ</h1>
        <p style="color:#6b6f8e;font-size:1rem;margin-top:.5rem;letter-spacing:.02em;">
            AI-powered candidate screening &amp; recruitment intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1,1.4,1])
    with mid:
        t1,t2,t3 = st.tabs(["  Sign In  ","  Sign Up  ","  Reset  "])
        with t1:
            u = st.text_input("Username", placeholder="your_username", key="lu")
            p = st.text_input("Password", type="password", placeholder="••••••••", key="lp")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", width='stretch'):
                res  = requests.post("http://127.0.0.1:8000/login", data={"username":u,"password":p})
                data = res.json()
                if "access_token" in data:
                    st.session_state.update({"login":True,"role":data["role"],"username":u,"token":data["access_token"]})
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        with t2:
            nu = st.text_input("Username",  placeholder="choose_username",        key="su_user")
            ne = st.text_input("Email",     placeholder="you@company.com",        key="su_email")
            np = st.text_input("Password",  type="password", placeholder="••••••••", key="su_pass")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", width='stretch'):
                res = requests.post("http://127.0.0.1:8000/signup", data={"username":nu,"email":ne,"password":np})
                st.success("Account created!") if res.status_code == 200 else st.error(res.text)
        with t3:
            em  = st.text_input("Email",        placeholder="you@company.com",    key="fp_email")
            if st.button("Send OTP", width='stretch'):
                res = requests.post("http://127.0.0.1:8000/forgot_password", data={"email":em})
                if res.status_code == 200: st.success("OTP sent.")
            ot  = st.text_input("OTP",          placeholder="6-digit code",       key="fp_otp")
            np2 = st.text_input("New Password", type="password", placeholder="••••••••", key="fp_pass")
            if st.button("Reset Password →", width='stretch'):
                v = requests.post("http://127.0.0.1:8000/verify_otp", data={"email":em,"otp":ot})
                if v.status_code == 200:
                    r = requests.post("http://127.0.0.1:8000/reset_password", data={"email":em,"new_password":np2})
                    st.success("Password reset!") if r.status_code == 200 else st.error("Failed.")
                else:
                    st.error("Invalid OTP.")
    st.stop()


# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    # Logo strip
    st.markdown("""
    <div style="
        display:flex;align-items:center;gap:.8rem;
        padding:.3rem 0 1.8rem;
    ">
        <div style="
            width:42px;height:42px;border-radius:13px;
            background:linear-gradient(135deg,#7c6af7,#00d4ff);
            display:flex;align-items:center;justify-content:center;
            font-size:1.2rem;box-shadow:0 4px 20px rgba(124,106,247,.5);
            flex-shrink:0;
        ">🧠</div>
        <div>
            <div style="font-family:'Outfit',sans-serif;font-weight:900;
                font-size:1.1rem;letter-spacing:-.02em;
                background:linear-gradient(90deg,#e8e9f8,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                TalentIQ</div>
            <div style="font-size:.63rem;color:#6b6f8e;
                letter-spacing:.09em;text-transform:uppercase;">Recruitment AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "nav", [
            "🏠 Dashboard","📄 Resume Matching","👩‍💼 Candidates",
            "⭐ Recommendations","🔍 Search","📊 Analytics",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1px;background:rgba(124,106,247,.15);margin:1rem 0'></div>",
                unsafe_allow_html=True)

    rc      = {"admin":"#a78bfa","recruiter":"#00d4ff"}.get(st.session_state.role or "","#6b6f8e")
    rc_bg   = {"admin":"rgba(167,139,250,.13)","recruiter":"rgba(0,212,255,.13)"}.get(st.session_state.role or "","rgba(107,111,142,.13)")
    rc_bdr  = {"admin":"rgba(167,139,250,.35)","recruiter":"rgba(0,212,255,.35)"}.get(st.session_state.role or "","rgba(107,111,142,.35)")
    st.markdown(
        '<div style="background:rgba(124,106,247,.08);border:1px solid rgba(124,106,247,.18);'
        'border-radius:12px;padding:.9rem 1rem;margin-bottom:.6rem;">'
        '<div style="display:flex;align-items:center;gap:.6rem;">'
        f'<div style="width:34px;height:34px;border-radius:50%;background:{rc_bg};'
        f'border:1.5px solid {rc_bdr};display:flex;align-items:center;justify-content:center;'
        'font-size:.9rem;">👤</div>'
        '<div>'
        f'<div style="font-weight:700;font-size:.88rem;color:#e8e9f8;">{st.session_state.username}</div>'
        f'<div style="font-size:.68rem;color:{rc};text-transform:uppercase;letter-spacing:.06em;">{st.session_state.role}</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    if st.button("Sign Out", width='stretch'):
        st.session_state.clear(); st.rerun()


# ─────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────
if menu == "🏠 Dashboard":
    page_header("🏠","Dashboard","Real-time overview of your recruitment pipeline")

    data       = safe_get("http://127.0.0.1:8000/analytics")
    candidates = safe_get("http://127.0.0.1:8000/ranked_candidates") or []

    approved = sum(1 for c in candidates if c.get("status") == "Approved")
    denied   = sum(1 for c in candidates if c.get("status") == "Denied")
    pending  = sum(1 for c in candidates if c.get("status","AI Recommended") == "AI Recommended")

    if data:
        skills = data.get("skill_distribution", {})
        top    = max(skills, key=skills.get) if skills else "N/A"
        scores = data.get("scores", [])
        avg    = round(sum(scores)/len(scores), 2) if scores else 0
        total  = data.get("total_candidates", 0)
    else:
        skills, top, avg, total, scores = {}, "N/A", 0, len(candidates), []

    # ── Row 1: 4 Stat Cards ──
    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("👥", "Total Candidates",  total,        "#7c6af7")
    with c2: stat_card("⚡", "Top Skill",          top,          "#00d4ff")
    with c3: stat_card("📊", "Avg Match Score",    avg,          "#a78bfa")
    with c4: stat_card("🏆", "Candidates Scored",  len(scores),  "#43e97b")

    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    # ── Row 2: Left (Pipeline + Interviews) | Right (Skills + Candidates) ──
    left_col, right_col = st.columns([1, 1.4])

    with left_col:
        section_title("🔄 Pipeline Overview")
        # 3 pipeline cards stacked vertically
        for label, count, color, bg, bdr, emoji in [
            ("AI Recommended", pending,  "#a78bfa",
             "rgba(124,106,247,.15)", "rgba(124,106,247,.28)", "🤖"),
            ("Approved",       approved, "#43e97b",
             "rgba(67,233,123,.13)",  "rgba(67,233,123,.28)",  "✅"),
            ("Denied",         denied,   "#f857a6",
             "rgba(248,87,166,.13)", "rgba(248,87,166,.28)",  "❌"),
        ]:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{bg},{bg.replace(".13",".04").replace(".15",".04")});'
                f'border:1px solid {bdr};border-radius:12px;padding:.75rem 1rem;margin-bottom:7px;'
                'display:flex;align-items:center;justify-content:space-between;">'
                '<div>'
                f'<div style="font-size:.65rem;color:#6b6f8e;text-transform:uppercase;'
                f'letter-spacing:.07em;font-weight:600;margin-bottom:.15rem;">{label}</div>'
                f'<div style="font-size:1.7rem;font-weight:900;color:{color};letter-spacing:-.03em;line-height:1.1;">{count}</div>'
                '</div>'
                f'<div style="font-size:1.5rem;opacity:.85;">{emoji}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # Upcoming Interviews — robust display
        section_title("📅 Upcoming Interviews")
        upcoming = safe_get("http://127.0.0.1:8000/upcoming_interviews")

        # Normalise: could be a list, a dict with a key, or None
        if isinstance(upcoming, dict):
            upcoming = upcoming.get("interviews") or upcoming.get("data") or []
        if not upcoming:
            upcoming = []

        # Fallback: pull scheduled interviews from candidates directly
        if not upcoming:
            all_cands = safe_get("http://127.0.0.1:8000/ranked_candidates") or []
            for cand in all_cands:
                iv = safe_get(f"http://127.0.0.1:8000/interview/{cand['_id']}")
                if iv and iv.get("date"):
                    upcoming.append({
                        "Name":  cand.get("name","—"),
                        "Email": cand.get("email",""),
                        "Date":  iv.get("date",""),
                        "Time":  iv.get("time",""),
                    })

        if upcoming:
            # render as styled cards instead of dataframe
            for iv in upcoming:
                name  = iv.get("Name") or iv.get("name","—")
                email = iv.get("Email") or iv.get("email","")
                date  = iv.get("Date") or iv.get("date","")
                time  = iv.get("Time") or iv.get("time","")
                st.markdown(
                    '<div style="background:linear-gradient(135deg,#151829,#1a1d32);'
                    'border:1px solid rgba(124,106,247,.25);border-left:3px solid #7c6af7;'
                    'border-radius:11px;padding:.8rem 1rem;margin-bottom:6px;'
                    'display:flex;align-items:center;justify-content:space-between;">'
                    '<div>'
                    f'<div style="font-weight:700;font-size:.88rem;color:#e8e9f8;">{name}</div>'
                    f'<div style="font-size:.72rem;color:#6b6f8e;">{email}</div>'
                    '</div>'
                    '<div style="text-align:right;">'
                    f'<div style="font-size:.82rem;font-weight:700;color:#a78bfa;">{date}</div>'
                    f'<div style="font-size:.75rem;color:#6b6f8e;">{time}</div>'
                    '</div></div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#151829,#1a1d32);'
                'border:1px dashed rgba(124,106,247,.2);border-radius:12px;'
                'padding:1.2rem;text-align:center;">'
                '<div style="font-size:1.3rem;margin-bottom:.3rem;">📭</div>'
                '<div style="color:#6b6f8e;font-size:.82rem;">No upcoming interviews.</div>'
                '</div>',
                unsafe_allow_html=True
            )

    with right_col:
        # Top Skills Breakdown
        section_title("🎯 Top Skills Breakdown")
        if skills:
            sorted_skills = sorted(skills.items(), key=lambda x: -x[1])[:8]
            max_count = max(v for _, v in sorted_skills) if sorted_skills else 1
            palette   = ["#7c6af7","#00d4ff","#f857a6","#43e97b","#a78bfa","#fbbf24","#fb7185","#34d399"]
            all_rows  = ""
            for idx, (skill, count) in enumerate(sorted_skills):
                pct       = int((count / max_count) * 100)
                bar_color = palette[idx % len(palette)]
                bar_style = (
                    f"width:{pct}%;height:100%;border-radius:6px;"
                    f"background:{bar_color};"
                    "display:flex;align-items:center;padding-left:8px;"
                    "box-sizing:border-box;min-width:24px;"
                )
                all_rows += (
                    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">'
                    f'<div style="width:95px;font-size:.8rem;color:#e8e9f8;font-weight:600;'
                    f'text-align:right;flex-shrink:0;">{skill}</div>'
                    '<div style="flex:1;height:22px;background:#1a1d32;border-radius:6px;'
                    'overflow:hidden;border:1px solid #252840;">'
                    f'<div style="{bar_style}">'
                    f'<span style="font-size:.7rem;font-weight:700;color:#fff;">{count}</span>'
                    '</div></div></div>'
                )
            st.markdown(
                '<div style="background:linear-gradient(135deg,#151829,#1a1d32);'
                'border:1px solid #252840;border-radius:14px;padding:1.2rem 1.4rem;">'
                + all_rows + '</div>',
                unsafe_allow_html=True
            )
        else:
            st.info("No skill data available.")

        # Recent Candidates compact
        section_title("👥 Recent Candidates")
        if candidates:
            recent   = candidates[:4]
            sc_rgba  = {
                "Approved": ("#43e97b", "rgba(67,233,123,.15)",  "rgba(67,233,123,.35)"),
                "Denied":   ("#f857a6", "rgba(248,87,166,.15)",  "rgba(248,87,166,.35)"),
            }
            default_rgba = ("#a78bfa", "rgba(167,139,250,.15)", "rgba(167,139,250,.35)")
            rc_cols = st.columns(len(recent))
            for col, c in zip(rc_cols, recent):
                status         = c.get("status", "AI Recommended")
                color, bg, bdr = sc_rgba.get(status, default_rgba)
                score          = round(c.get("score", 0), 3)
                pct            = int(score * 100)
                name           = c.get("name", "—")
                skill_txt      = ", ".join(c.get("skills", [])[:2])
                with col:
                    st.markdown(
                        '<div style="background:linear-gradient(135deg,#151829,#1a1d32);'
                        f'border:1px solid #252840;border-top:2px solid {color};'
                        'border-radius:12px;padding:.85rem .9rem;text-align:center;">'
                        f'<div style="width:36px;height:36px;border-radius:50%;margin:0 auto .5rem;'
                        f'background:{bg};border:1.5px solid {bdr};'
                        'display:flex;align-items:center;justify-content:center;font-size:1rem;">👤</div>'
                        f'<div style="font-weight:700;font-size:.8rem;color:#e8e9f8;margin-bottom:.15rem;'
                        'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
                        f'{name}</div>'
                        f'<div style="font-size:.67rem;color:#6b6f8e;margin-bottom:.4rem;">{skill_txt}</div>'
                        '<div style="height:3px;background:#252840;border-radius:999px;overflow:hidden;margin-bottom:.35rem;">'
                        f'<div style="width:{pct}%;height:100%;background:{color};border-radius:999px;"></div>'
                        '</div>'
                        f'<span style="font-size:.7rem;font-weight:700;color:{color};">{score}</span>'
                        '</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.info("No candidates yet.")


# ─────────────────────────────────────────
#  RESUME MATCHING
# ─────────────────────────────────────────
elif menu == "📄 Resume Matching":
    page_header("📄","Resume Matching","Upload resumes and match against a job description")

    col_l, col_r = st.columns([1.1,1])
    with col_l:
        st.markdown("""<p style="color:#6b6f8e;font-size:.72rem;text-transform:uppercase;
            letter-spacing:.09em;font-weight:700;margin-bottom:.4rem;">
            Upload Resumes (PDF)</p>""", unsafe_allow_html=True)
        files = st.file_uploader("Resumes", type=["pdf"], accept_multiple_files=True,
            key=f"rf_{st.session_state.reset_counter}", label_visibility="collapsed")
    with col_r:
        st.markdown("""<p style="color:#6b6f8e;font-size:.72rem;text-transform:uppercase;
            letter-spacing:.09em;font-weight:700;margin-bottom:.4rem;">
            Job Description</p>""", unsafe_allow_html=True)
        job = st.text_area("JD", height=155, placeholder="Paste the full job description here...",
            key=f"jd_{st.session_state.reset_counter}", label_visibility="collapsed")

    st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
    ca,cb,_ = st.columns([1,1,3])
    with ca: match_clicked = st.button("⚡ Match Candidates", width='stretch')
    with cb:
        if st.session_state.get("match_results"):
            if st.button("🗑 Clear", width='stretch'):
                st.session_state.match_results = []
                st.session_state.reset_counter += 1
                st.rerun()

    if match_clicked:
        if files and job:
            res = []
            with st.spinner("Running AI engine..."):
                for f in files:
                    d = safe_post("http://127.0.0.1:8000/match",
                                  data={"job_description":job}, files={"file":f})
                    if d:
                        ex = d.get("explanation",{})
                        res.append({
                            "Candidate":      f.name,
                            "Score":          round(d.get("score",0),3),
                            "Matched Skills": ", ".join(ex.get("matched_skills",[])),
                            "Missing Skills": ", ".join(ex.get("missing_skills",[])),
                        })
            st.session_state.match_results = res
        else:
            st.warning("Upload at least one resume and enter a job description.")

    if st.session_state.get("match_results"):
        ranked = sorted(st.session_state.match_results, key=lambda x: x["Score"], reverse=True)
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        st.success(f"✅ Matched {len(ranked)} candidate(s) — ranked by AI score")
        render_results_table(ranked)


# ─────────────────────────────────────────
#  CANDIDATES
# ─────────────────────────────────────────
elif menu == "👩‍💼 Candidates":
    page_header("👩‍💼","Candidates","Browse, manage, and schedule all candidates")

    candidates = safe_get("http://127.0.0.1:8000/ranked_candidates")
    if not candidates:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#151829,#1a1d32);
            border:1px dashed rgba(124,106,247,.25);border-radius:14px;
            padding:3rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:.5rem;">🫥</div>
            <div style="color:#6b6f8e;">No candidates found.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for c in candidates:
            status = c.get("status","AI Recommended")
            sc     = {"Approved":"#43e97b","Denied":"#f857a6"}.get(status,"#a78bfa")
            sc_rgba_map = {
                "#43e97b": ("rgba(67,233,123,.12)",  "rgba(67,233,123,.35)",  "rgba(67,233,123,.12)",  "rgba(67,233,123,.3)"),
                "#f857a6": ("rgba(248,87,166,.12)",  "rgba(248,87,166,.35)",  "rgba(248,87,166,.12)",  "rgba(248,87,166,.3)"),
                "#a78bfa": ("rgba(167,139,250,.12)", "rgba(167,139,250,.35)", "rgba(167,139,250,.12)", "rgba(167,139,250,.3)"),
            }
            avatar_bg, avatar_bdr, badge_bg, badge_bdr = sc_rgba_map.get(sc, sc_rgba_map["#a78bfa"])
            name   = c.get('name','—')
            email  = c.get('email','')
            skills_str = ', '.join(c.get('skills',[]))
            score_val  = round(c.get('score',0),3)

            with st.container():
                st.markdown(
                    '<div style="background:linear-gradient(135deg,#151829 0%,#1a1d32 100%);'
                    f'border:1px solid #252840;border-left:3px solid {sc};'
                    'border-radius:14px;padding:1.1rem 1.4rem .6rem;margin-bottom:.7rem;">'
                    '<div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.4rem;">'
                    f'<div style="width:40px;height:40px;border-radius:50%;flex-shrink:0;'
                    f'background:{avatar_bg};border:1.5px solid {avatar_bdr};'
                    'display:flex;align-items:center;justify-content:center;font-size:1.1rem;">👤</div>'
                    '<div>'
                    f'<div style="font-weight:700;font-size:.97rem;color:#e8e9f8;">{name}</div>'
                    f'<div style="font-size:.76rem;color:#6b6f8e;">{email}</div>'
                    '</div>'
                    '<div style="margin-left:auto;display:flex;gap:.45rem;flex-wrap:wrap;">'
                    f'<span style="padding:3px 11px;border-radius:999px;'
                    f'background:{badge_bg};color:{sc};border:1px solid {badge_bdr};'
                    f'font-size:.72rem;font-weight:700;">{status}</span>'
                    '<span style="padding:3px 11px;border-radius:999px;'
                    'background:rgba(124,106,247,.15);color:#a78bfa;'
                    'border:1px solid rgba(124,106,247,.3);'
                    f'font-size:.72rem;font-weight:700;">Score: {score_val}</span>'
                    '</div></div>'
                    f'<div style="font-size:.78rem;color:#6b6f8e;margin-bottom:.5rem;">'
                    f'Skills: {skills_str}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                iv = safe_get(f"http://127.0.0.1:8000/interview/{c['_id']}")
                if iv:
                    st.markdown(f"""<div style="margin:-.3rem 0 .4rem 1rem;
                        font-size:.78rem;color:#43e97b;">
                        📅 Interview: {iv.get('date')} at {iv.get('time')}</div>""",
                        unsafe_allow_html=True)

                if st.session_state.role in ["admin","recruiter"]:
                    s_col, i_col, d_col = st.columns([1.2,2,.6])
                    with s_col:
                        opts = ["AI Recommended","Approved","Denied"]
                        sel  = st.selectbox("Status", opts,
                                            index=opts.index(c.get("status","AI Recommended")),
                                            key=f"st_{c['_id']}", label_visibility="collapsed")
                        if st.button("Update", key=f"up_{c['_id']}"):
                            safe_post(f"http://127.0.0.1:8000/update_status/{c['_id']}",
                                      data={"status":sel})
                            st.success("Updated."); st.rerun()
                    with i_col:
                        dc, tc = st.columns(2)
                        with dc: dt = st.date_input("Date", key=f"d_{c['_id']}",
                                                     label_visibility="collapsed")
                        with tc: tm = st.time_input("Time", key=f"t_{c['_id']}",
                                                     label_visibility="collapsed")
                        if st.button("📅 Schedule", key=f"sc_{c['_id']}"):
                            safe_post(f"http://127.0.0.1:8000/schedule_interview/{c['_id']}",
                                      data={"date":str(dt),"time":str(tm)})
                            st.success("Scheduled."); st.rerun()
                    with d_col:
                        if st.session_state.role == "admin":
                            if st.button("🗑", key=f"dl_{c['_id']}"):
                                requests.delete(
                                    f"http://127.0.0.1:8000/delete_candidate/{c['_id']}",
                                    headers=get_headers())
                                st.success("Deleted."); st.rerun()

    if st.session_state.role == "admin":
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(248,87,166,.06);border:1px solid rgba(248,87,166,.2);
            border-radius:14px;padding:1.1rem 1.4rem;">
            <div style="font-weight:700;color:#f857a6;margin-bottom:.5rem;font-size:.93rem;">
                ⚠️ Danger Zone</div>""", unsafe_allow_html=True)
        confirm = st.checkbox("I understand this will permanently delete ALL candidates")
        if st.button("🗑 Delete All Candidates"):
            if confirm:
                rr = requests.delete("http://127.0.0.1:8000/clear_all", headers=get_headers())
                st.success("All deleted.") if rr.status_code == 200 else st.error("Failed.")
                st.rerun()
            else:
                st.warning("Check the confirmation box first.")
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  RECOMMENDATIONS
# ─────────────────────────────────────────
elif menu == "⭐ Recommendations":
    page_header("⭐","Top Recommendations","AI-ranked shortlist of your best candidates")

    limit = st.slider("Show top N candidates", 1, 10, 5)
    rec   = safe_get(f"http://127.0.0.1:8000/recommend_candidates?limit={limit}")

    if rec:
        medal = ["🥇","🥈","🥉"]
        for i, r in enumerate(rec):
            score      = round(r.get("score",0),3)
            pct        = int(score*100)
            icon       = medal[i] if i < 3 else f"#{i+1}"
            bc         = "#43e97b" if score>=.6 else ("#a78bfa" if score>=.35 else "#f857a6")
            name_r     = r.get('name','—')
            skills_r   = ', '.join(r.get('skills',[]))
            st.markdown(
                '<div style="background:linear-gradient(135deg,#151829,#1a1d32);'
                'border:1px solid #252840;border-radius:14px;'
                'padding:1.1rem 1.4rem;margin-bottom:.7rem;'
                'display:flex;align-items:center;gap:1rem;">'
                f'<div style="font-size:1.8rem;min-width:40px;text-align:center;">{icon}</div>'
                '<div style="flex:1;">'
                f'<div style="font-weight:700;font-size:.97rem;color:#e8e9f8;margin-bottom:.2rem;">{name_r}</div>'
                f'<div style="font-size:.76rem;color:#6b6f8e;margin-bottom:.45rem;">{skills_r}</div>'
                '<div style="height:5px;background:#252840;border-radius:999px;overflow:hidden;">'
                f'<div style="width:{pct}%;height:100%;background:{bc};border-radius:999px;"></div>'
                '</div></div>'
                f'<div style="font-weight:900;font-size:1.35rem;color:{bc};'
                f'min-width:58px;text-align:right;letter-spacing:-.02em;">{score}</div>'
                '</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("No recommendations available.")


# ─────────────────────────────────────────
#  SEARCH
# ─────────────────────────────────────────
elif menu == "🔍 Search":
    page_header("🔍","Candidate Search","Find candidates by skill")

    ci, cb = st.columns([3,1])
    with ci:
        skill = st.text_input("Skill", placeholder="e.g. Python, React, SQL...",
                               label_visibility="collapsed")
    with cb:
        go = st.button("Search →", width='stretch')

    if go and skill:
        res = safe_get(f"http://127.0.0.1:8000/search_candidates?skill={skill}")
        if res:
            st.markdown(f"""<p style="color:#6b6f8e;font-size:.84rem;margin-bottom:.8rem;">
                Found <strong style="color:#a78bfa;">{len(res)}</strong>
                result(s) for "<em>{skill}</em>"</p>""", unsafe_allow_html=True)
            for r in res:
                pills = "".join([
                    f'<span style="display:inline-block;margin:2px 3px;padding:2px 9px;'
                    f'border-radius:999px;background:rgba(124,106,247,.12);color:#a78bfa;'
                    f'border:1px solid rgba(124,106,247,.25);font-size:.72rem;">{s}</span>'
                    for s in r.get("skills",[])
                ])
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#151829,#1a1d32);
                    border:1px solid #252840;border-radius:12px;
                    padding:.95rem 1.2rem;margin-bottom:.55rem;">
                    <div style="font-weight:700;color:#e8e9f8;margin-bottom:.4rem;">
                        {r.get('name','—')}</div>
                    <div>{pills}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info(f"No candidates found with skill: **{skill}**")


# ─────────────────────────────────────────
#  ANALYTICS
# ─────────────────────────────────────────
elif menu == "📊 Analytics":
    page_header("📊","Analytics","Skill distribution & score analysis")

    data = safe_get("http://127.0.0.1:8000/analytics")

    if data:
        skills = data.get("skill_distribution", {})
        scores = data.get("scores", [])

        col1, col2 = st.columns(2)

        # ── Skill Distribution — pure HTML bars ──
        with col1:
            section_title("📊 Skill Distribution")
            if skills:
                sorted_skills = sorted(skills.items(), key=lambda x: -x[1])
                max_count     = max(v for _, v in sorted_skills) if sorted_skills else 1
                palette       = ["#7c6af7","#00d4ff","#f857a6","#43e97b",
                                  "#a78bfa","#fbbf24","#fb7185","#34d399",
                                  "#60a5fa","#e879f9"]
                rows = ""
                for idx, (skill, count) in enumerate(sorted_skills):
                    pct   = int((count / max_count) * 100)
                    color = palette[idx % len(palette)]
                    rows += (
                        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:9px;">'
                        f'<div style="width:130px;font-size:.8rem;color:#e8e9f8;font-weight:600;'
                        f'text-align:right;flex-shrink:0;">{skill}</div>'
                        '<div style="flex:1;height:24px;background:#1a1d32;border-radius:6px;'
                        'overflow:hidden;border:1px solid #252840;">'
                        f'<div style="width:{pct}%;height:100%;background:{color};'
                        'border-radius:6px;display:flex;align-items:center;'
                        'padding-left:8px;box-sizing:border-box;min-width:26px;">'
                        f'<span style="font-size:.72rem;font-weight:700;color:#fff;">{count}</span>'
                        '</div></div></div>'
                    )
                st.markdown(
                    '<div style="background:linear-gradient(135deg,#151829,#1a1d32);'
                    'border:1px solid #252840;border-radius:14px;padding:1.2rem 1.4rem;">'
                    + rows + '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.info("No skill data yet.")

        # ── Score Distribution — matplotlib via BytesIO ──
        with col2:
            section_title("📈 Score Distribution")
            if scores:
                import io

                fig2, ax2 = plt.subplots(figsize=(5, 3.5))
                fig2.patch.set_facecolor("#111428")
                ax2.set_facecolor("#111428")

                n, bins, patches = ax2.hist(
                    scores, bins=min(10, len(scores)),
                    edgecolor="#252840", linewidth=.5, zorder=3
                )
                for patch, le in zip(patches, bins[:-1]):
                    patch.set_facecolor(
                        "#43e97b" if le >= .6 else ("#a78bfa" if le >= .3 else "#f857a6")
                    )

                ax2.tick_params(axis="x", colors="#6b6f8e", labelsize=8)
                ax2.tick_params(axis="y", colors="#6b6f8e", labelsize=8)
                for spine in ax2.spines.values():
                    spine.set_edgecolor("#252840")
                ax2.set_axisbelow(True)
                ax2.yaxis.grid(color="#252840", linewidth=.6)
                ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                fig2.tight_layout(pad=.4)

                buf = io.BytesIO()
                fig2.savefig(buf, format="png", dpi=130,
                             facecolor="#111428", bbox_inches="tight")
                buf.seek(0)
                st.image(buf, width='stretch')
                plt.close(fig2)

                s1, s2, s3 = st.columns(3)
                with s1: st.metric("Min Score", round(min(scores), 3))
                with s2: st.metric("Avg Score", round(sum(scores)/len(scores), 3))
                with s3: st.metric("Max Score", round(max(scores), 3))

                st.markdown(
                    '<div style="display:flex;gap:1.2rem;margin-top:.5rem;flex-wrap:wrap;">'
                    '<span style="font-size:.76rem;color:#43e97b;font-weight:600;">● ≥ 0.6 — Strong</span>'
                    '<span style="font-size:.76rem;color:#a78bfa;font-weight:600;">● 0.3–0.6 — Moderate</span>'
                    '<span style="font-size:.76rem;color:#f857a6;font-weight:600;">● &lt; 0.3 — Weak</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.info("No score data yet.")
    else:
        st.info("No analytics data available.")
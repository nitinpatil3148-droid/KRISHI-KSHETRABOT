import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Agricultural Rover Control System", page_icon="🌱", layout="wide")

if "functions" not in st.session_state:
    st.session_state.functions = {"Cutter": False, "Pump": False, "Seed": False, "Plough": False}
if "activity" not in st.session_state:
    st.session_state.activity = ["Dashboard loaded — ESP32 not connected"]
if "rover_status" not in st.session_state:
    st.session_state.rover_status = "Ready"

def log(message):
    st.session_state.activity.insert(0, f"{datetime.now():%H:%M:%S}  {message}")
    st.session_state.activity = st.session_state.activity[:10]

def toggle(name):
    st.session_state.functions[name] = not st.session_state.functions[name]
    log(f"{name} {'ON' if st.session_state.functions[name] else 'OFF'}")

def emergency():
    for name in st.session_state.functions:
        st.session_state.functions[name] = False
    st.session_state.rover_status = "Stopped"
    log("EMERGENCY STOP requested")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html,body,[data-testid="stAppViewContainer"]{font-family:Inter,sans-serif;background:linear-gradient(180deg,#e9f8e9,#fbfff9 55%,#e9f8e9);}
[data-testid="stHeader"],[data-testid="stToolbar"],#MainMenu,footer{visibility:hidden;height:0;}
.block-container{max-width:100%;padding:.5rem clamp(.4rem,1.3vw,1.3rem) 1rem;}
.hero{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;background:linear-gradient(105deg,#003b15,#08732c 55%,#164b22);color:white;border-radius:17px;padding:clamp(12px,1.5vw,22px) clamp(14px,2vw,28px);margin-bottom:12px;box-shadow:0 4px 12px #003c1b38;}
.brand{font-size:clamp(22px,2.8vw,40px);font-weight:900;line-height:1.05;}
.sub{font-size:clamp(14px,1.7vw,23px);font-weight:750;color:#c9f4c8;margin-top:4px;}
.connection{background:#fff;color:#14271a;border:2px solid #18bd31;border-radius:50px;padding:10px 18px;font-weight:800;font-size:clamp(12px,1.25vw,17px);}
[data-testid="stHorizontalBlock"]{gap:clamp(8px,1.2vw,18px)!important;align-items:stretch;}
[data-testid="column"]{min-width:0!important;}
[data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(145deg,#fff,#eff9ed);border:1.5px solid #83b98a;border-radius:18px;box-shadow:0 3px 9px #164b2020;padding:.6rem!important;}
.panel-title{background:linear-gradient(90deg,#00551c,#003e16);color:white;border-radius:12px;padding:12px 8px;text-align:center;font-weight:850;font-size:clamp(16px,1.5vw,23px);margin-bottom:10px;}
div.st-key-move_f button,div.st-key-move_l button,div.st-key-move_s button,div.st-key-move_r button,div.st-key-move_b button{min-height:clamp(58px,8vh,88px);font-size:clamp(14px,1.2vw,19px);font-weight:850;border-radius:16px;background:linear-gradient(145deg,#087d24,#004817);color:white;border:2px solid #159b2b;box-shadow:0 3px 7px #003e1d35;}
div.st-key-move_s button{background:linear-gradient(145deg,#ff4035,#c90000);border-color:#ff9a8f;}
.rover-stage{height:clamp(260px,42vh,440px);border:2px solid #6da879;border-radius:15px;background:radial-gradient(ellipse at 50% 78%,#a4c982 0%,#477d3a 42%,#b9d8b5 75%,#dcefe0 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;}
.rover-stage:before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(165deg,transparent 0 38px,#ffffff18 39px 42px);}
.rover-icon{font-size:clamp(75px,8vw,135px);z-index:1;filter:drop-shadow(0 9px 7px #163b1c66);}
.rover-status{position:absolute;bottom:9px;left:9px;right:9px;background:#f7fff2ed;color:#102b16;border-radius:11px;padding:10px;text-align:center;font-weight:800;font-size:clamp(12px,1vw,15px);}
.pill{display:inline-block;background:#07821f;color:white;border-radius:30px;padding:5px 14px;}
div.st-key-func_cutter button,div.st-key-func_pump button,div.st-key-func_seed button,div.st-key-func_plough button{min-height:clamp(82px,12vh,125px);font-size:clamp(14px,1.2vw,19px);font-weight:850;border:2px solid #1a9c34;background:linear-gradient(145deg,#087d24,#003f16);color:white;white-space:pre-wrap;}
div.st-key-func_cutter button[kind="primary"],div.st-key-func_pump button[kind="primary"],div.st-key-func_seed button[kind="primary"],div.st-key-func_plough button[kind="primary"]{background:linear-gradient(145deg,#22ed42,#078b1e)!important;border:3px solid #b8ffad!important;box-shadow:0 0 10px #14d735,0 0 23px #16d735aa!important;color:white!important;}
div.st-key-emergency button{min-height:55px;background:linear-gradient(180deg,#ff4035,#c90000);color:white;border:3px solid #ff9a8f;font-weight:900;font-size:clamp(15px,1.4vw,20px);box-shadow:0 0 12px #ef1d1d77;}
.note{text-align:center;color:#55705a;font-size:11px;margin-top:6px;}
.bottom{background:#f2fff0;border:2px solid #08722a;border-radius:16px;padding:8px 12px;margin-top:10px;}
@media(max-width:760px){.hero{justify-content:center;text-align:center;}.block-container{padding:.35rem .45rem .8rem;}.rover-stage{height:270px;}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div><div class="brand">🌿 Agricultural Rover</div><div class="sub">━━ Control System ━━</div></div>
  <div class="connection">🔵 &nbsp; 🟢 Wi-Fi: <span style="color:#a66b00">Not connected</span></div>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 1.12, 1], gap="small")

with left:
    with st.container(border=True):
        st.markdown('<div class="panel-title">🎮 Rover Movement</div>', unsafe_allow_html=True)
        _, up, _ = st.columns(3)
        with up:
            if st.button("⬆️\nForward", key="move_f", use_container_width=True):
                st.session_state.rover_status = "Moving Forward"; log("Forward command selected")
        a,b,c = st.columns(3, gap="small")
        with a:
            if st.button("⬅️\nLeft", key="move_l", use_container_width=True):
                st.session_state.rover_status = "Turning Left"; log("Left command selected")
        with b:
            if st.button("■\nSTOP", key="move_s", use_container_width=True):
                st.session_state.rover_status = "Ready"; log("Rover stop selected")
        with c:
            if st.button("➡️\nRight", key="move_r", use_container_width=True):
                st.session_state.rover_status = "Turning Right"; log("Right command selected")
        _, down, _ = st.columns(3)
        with down:
            if st.button("⬇️\nBackward", key="move_b", use_container_width=True):
                st.session_state.rover_status = "Moving Backward"; log("Backward command selected")
        st.markdown('<div class="note">Movement controls</div>', unsafe_allow_html=True)

with center:
    with st.container(border=True):
        st.markdown('<div class="panel-title">🚜 Rover View</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rover-stage"><div class="rover-icon">🚜</div>
        <div class="rover-status">🚜 &nbsp; Rover Status: <span class="pill">{st.session_state.rover_status}</span></div></div>
        <div class="note">3D rover model and free camera view will be integrated next.</div>
        """, unsafe_allow_html=True)

with right:
    with st.container(border=True):
        st.markdown('<div class="panel-title">🌱 Agricultural Functions</div>', unsafe_allow_html=True)
        # Independent function toggles: primary button style indicates active/glowing state.
        for row_names in (("Cutter","Pump"),("Seed","Plough")):
            c1,c2 = st.columns(2, gap="small")
            for col,name in zip((c1,c2),row_names):
                with col:
                    active = st.session_state.functions[name]
                    icon = {"Cutter":"⚙️","Pump":"💧","Seed":"🌾","Plough":"⚒️"}[name]
                    key = "func_" + name.lower()
                    if st.button(f"{icon}\n{name}\n{'ON' if active else 'OFF'}", key=key,
                                 type="primary" if active else "secondary", use_container_width=True):
                        toggle(name); st.rerun()
        st.markdown('<div class="note">Tap once to activate · tap again to deactivate</div>', unsafe_allow_html=True)

st.markdown('<div class="bottom">', unsafe_allow_html=True)
s1,s2,s3 = st.columns([1.1,1.2,1], vertical_alignment="center")
with s1:
    st.markdown("**📋 System Status:** <span style='color:#a66b00;font-weight:800'>Not connected</span>", unsafe_allow_html=True)
with s2:
    if st.button("⚠️  EMERGENCY STOP", key="emergency", use_container_width=True):
        emergency(); st.rerun()
with s3:
    with st.expander("📄 Activity Log"):
        for entry in st.session_state.activity:
            st.write("• " + entry)
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Dashboard preview only — controls are not yet connected to the ESP32. Use a physical power cutoff for hardware emergencies.")

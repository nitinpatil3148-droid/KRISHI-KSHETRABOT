import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Agricultural Rover Control System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- SESSION STATE --------------------
if "functions" not in st.session_state:
    st.session_state.functions = {
        "Cutter": False, "Pump": False, "Seed": False, "Plough": False
    }
if "activity" not in st.session_state:
    st.session_state.activity = ["Dashboard initialized — waiting for ESP32 connection."]
if "rover_status" not in st.session_state:
    st.session_state.rover_status = "Ready"

def log(message):
    st.session_state.activity.insert(
        0, f"{datetime.now().strftime('%H:%M:%S')}  {message}"
    )
    st.session_state.activity = st.session_state.activity[:10]

def toggle_function(name):
    st.session_state.functions[name] = not st.session_state.functions[name]
    log(f"{name} {'activated' if st.session_state.functions[name] else 'deactivated'}")

def emergency_stop():
    for name in st.session_state.functions:
        st.session_state.functions[name] = False
    st.session_state.rover_status = "Stopped"
    log("EMERGENCY STOP requested — all functions commanded OFF")

# -------------------- STYLING --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
:root { --green:#00651f; --dark:#003f16; --bright:#19e33a; }
html, body, [data-testid="stAppViewContainer"] {
    font-family:Inter,sans-serif;
    background:linear-gradient(180deg,#e8f7e8,#fbfffa 52%,#e8f7e8);
}
[data-testid="stHeader"],[data-testid="stToolbar"],#MainMenu,footer {visibility:hidden;}
.block-container {max-width:1800px;padding:0.6rem 1rem 1.2rem;}
.hero {
    min-height:112px;border-radius:17px;padding:16px 26px;margin-bottom:16px;
    color:white;display:flex;align-items:center;justify-content:space-between;gap:16px;
    background:linear-gradient(105deg,#003d16 0%,#08702c 54%,#174b22 100%);
    box-shadow:0 5px 15px #003c1b38;
}
.brand {font-size:clamp(25px,3vw,42px);font-weight:900;line-height:1.05;}
.brand-sub {font-size:clamp(16px,1.8vw,25px);font-weight:750;color:#c9f4c8;margin-top:5px;}
.connection {
    border:3px solid #17bd31;background:#fff;color:#13251a;border-radius:60px;
    padding:12px 22px;font-size:clamp(13px,1.4vw,19px);font-weight:800;
    box-shadow:0 4px 13px #001b0c44;white-space:nowrap;
}
.panel {
    background:linear-gradient(145deg,#fff,#eff9ed);border:1.5px solid #83b98a;
    border-radius:22px;overflow:hidden;box-shadow:0 4px 10px #164b2020;
    padding-bottom:14px;min-height:510px;
}
.panel-head {
    background:linear-gradient(90deg,#00551c,#003e16);color:#fff;text-align:center;
    padding:15px 10px;font-size:clamp(17px,1.55vw,25px);font-weight:850;
}
.panel-inner {padding:16px 14px;}
.rover-stage {
    min-height:390px;border:2px solid #6da879;border-radius:17px;
    background:radial-gradient(ellipse at 50% 78%,#a4c982 0%,#477d3a 42%,#b9d8b5 75%,#dcefe0 100%);
    display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;
}
.rover-stage:before {
    content:"";position:absolute;inset:0;
    background:repeating-linear-gradient(165deg,transparent 0 38px,#ffffff18 39px 42px);
}
.rover-emoji {font-size:clamp(85px,9vw,145px);z-index:1;filter:drop-shadow(0 10px 7px #163b1c66);}
.rover-status {
    position:absolute;bottom:10px;left:10px;right:10px;background:#f7fff2ed;
    color:#102b16;border-radius:12px;padding:12px;text-align:center;font-weight:800;
}
.status-pill {display:inline-block;background:#07821f;color:#fff;border-radius:30px;padding:6px 18px;}
.small-note {font-size:11px;color:#526c55;text-align:center;margin-top:8px;}
div.stButton > button {
    border-radius:15px;border:2px solid #159b2b;
    background:linear-gradient(145deg,#087d24,#004817);color:white;
    font-weight:800;min-height:66px;white-space:pre-wrap;
    box-shadow:0 4px 8px #003e1d35;transition:all .15s ease;
}
div.stButton > button:hover {border-color:#70ff72;color:white;box-shadow:0 0 13px #18d83b;}
div.st-key-func_cutter button,div.st-key-func_pump button,
div.st-key-func_seed button,div.st-key-func_plough button {min-height:104px;font-size:17px;}
div.st-key-func_cutter.active button,div.st-key-func_pump.active button,
div.st-key-func_seed.active button,div.st-key-func_plough.active button {
    background:linear-gradient(145deg,#20e83d,#078b1e)!important;
    border:3px solid #b8ffad!important;color:#fff!important;
    box-shadow:0 0 10px #14d735,0 0 25px #16d735aa!important;
}
div.st-key-move_stop button {
    background:linear-gradient(145deg,#ff3d32,#c90000)!important;
    border:2px solid #ff9a8f!important;
}
div.st-key-emergency button {
    background:linear-gradient(180deg,#ff3d32,#c90000)!important;
    border:3px solid #ff9a8f!important;min-height:58px;font-size:18px;
    box-shadow:0 0 13px #ef1d1d88!important;
}
.bottom-strip {
    border:2px solid #08722a;border-radius:18px;padding:12px 14px;
    background:#f2fff0;box-shadow:0 3px 8px #174b2020;margin-top:14px;
}
@media(max-width:850px) {
    .hero {flex-direction:column;text-align:center;}
    .connection {white-space:normal;}
    .panel {min-height:unset;}
    .rover-stage {min-height:280px;}
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="hero">
  <div>
    <div class="brand">🌿 Agricultural Rover</div>
    <div class="brand-sub">━━ Control System ━━</div>
  </div>
  <div class="connection">🔵 &nbsp; 🟢 Wi-Fi: <span style="color:#b06b00">Not connected</span></div>
</div>
""", unsafe_allow_html=True)

# -------------------- THREE-PANEL DASHBOARD --------------------
left, center, right = st.columns([1.02, 1.12, 1.02], gap="medium")

with left:
    st.markdown('<div class="panel"><div class="panel-head">🎮 &nbsp; Rover Movement</div><div class="panel-inner">', unsafe_allow_html=True)
    _, up, _ = st.columns(3)
    with up:
        if st.button("⬆️\nForward", key="move_forward", use_container_width=True):
            st.session_state.rover_status = "Moving Forward"
            log("Forward command selected")
    l, stop, r = st.columns(3)
    with l:
        if st.button("⬅️\nLeft", key="move_left", use_container_width=True):
            st.session_state.rover_status = "Turning Left"
            log("Left command selected")
    with stop:
        if st.button("■\nStop", key="move_stop", use_container_width=True):
            st.session_state.rover_status = "Ready"
            log("Rover stop selected")
    with r:
        if st.button("➡️\nRight", key="move_right", use_container_width=True):
            st.session_state.rover_status = "Turning Right"
            log("Right command selected")
    _, down, _ = st.columns(3)
    with down:
        if st.button("⬇️\nBackward", key="move_backward", use_container_width=True):
            st.session_state.rover_status = "Moving Backward"
            log("Backward command selected")
    st.markdown('<div class="small-note">Hold-to-move behaviour and ESP32 commands will be connected in the integration stage.</div></div></div>', unsafe_allow_html=True)

with center:
    st.markdown('<div class="panel"><div class="panel-head">🚜 &nbsp; Rover View</div><div class="panel-inner">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rover-stage">
      <div class="rover-emoji">🚜</div>
      <div class="rover-status">🚜 &nbsp; Rover Status: <span class="status-pill">{st.session_state.rover_status}</span></div>
    </div>
    <div class="small-note">3D rover model and interactive camera view will be added in the next stage.</div>
    </div></div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-head">🌱 &nbsp; Agricultural Functions</div><div class="panel-inner">', unsafe_allow_html=True)
    function_info = [
        ("Cutter", "⚙️", "func_cutter"),
        ("Pump", "💧", "func_pump"),
        ("Seed", "🌾", "func_seed"),
        ("Plough", "⚒️", "func_plough"),
    ]
    row1a, row1b = st.columns(2, gap="small")
    row2a, row2b = st.columns(2, gap="small")
    for col, (name, icon, key) in zip(
        (row1a, row1b, row2a, row2b), function_info
    ):
        with col:
            active = st.session_state.functions[name]
            if active:
                st.markdown(f'<div class="st-key-{key} active">', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="st-key-{key}">', unsafe_allow_html=True)
            if st.button(
                f"{icon}\n{name}\n{'ON' if active else 'OFF'}",
                key=key, use_container_width=True
            ):
                toggle_function(name)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="small-note">Tap once to activate · tap again to deactivate</div></div></div>', unsafe_allow_html=True)

# -------------------- BOTTOM STATUS BAR --------------------
st.markdown('<div class="bottom-strip">', unsafe_allow_html=True)
status_col, stop_col, log_col = st.columns([1.2, 1.15, 1.0], vertical_alignment="center")
with status_col:
    st.markdown("**📋 System Status:** <span style='color:#a46a00;font-weight:800'>Not connected</span>", unsafe_allow_html=True)
with stop_col:
    if st.button("⚠️  EMERGENCY STOP", key="emergency", use_container_width=True):
        emergency_stop()
        st.rerun()
with log_col:
    with st.expander("📄 Activity Log"):
        for item in st.session_state.activity:
            st.write("• " + item)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("UI prototype only: controls currently update the dashboard locally and do not yet send commands to the ESP32. Keep the rover safely raised during hardware testing; retain a physical power cutoff.")


import os
import requests
import streamlit as st
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Agricultural Rover Control System",
    page_icon="🌱",
    layout="wide"
)

BACKEND_URL = os.getenv("BACKEND_URL", "").rstrip("/")
DASHBOARD_API_KEY = os.getenv("DASHBOARD_API_KEY", "")

HEADERS = {"X-Dashboard-Key": DASHBOARD_API_KEY}

# =====================================================
# SESSION STATE
# =====================================================

if "functions" not in st.session_state:
    st.session_state.functions = {
        "Cutter": False,
        "Pump": False,
        "Seed": False,
        "Plough": False
    }

if "activity" not in st.session_state:
    st.session_state.activity = ["Dashboard started"]

if "rover_status" not in st.session_state:
    st.session_state.rover_status = "Ready"

# =====================================================
# BACKEND COMMUNICATION
# =====================================================

def log(message):
    st.session_state.activity.insert(
        0, f"{datetime.now():%H:%M:%S} - {message}"
    )
    st.session_state.activity = st.session_state.activity[:10]


def send_command(command, description):
    if not BACKEND_URL or not DASHBOARD_API_KEY:
        st.error("Backend configuration is missing.")
        return False

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/command",
            json={"command": command},
            headers=HEADERS,
            timeout=8
        )
        response.raise_for_status()
        log(f"{description} sent")
        return True

    except requests.RequestException as error:
        st.error(f"Unable to send {description}. Check backend connection.")
        return False


def get_device_status():
    if not BACKEND_URL or not DASHBOARD_API_KEY:
        return False

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/status",
            headers=HEADERS,
            timeout=5
        )
        response.raise_for_status()
        return response.json().get("device_connected", False)

    except requests.RequestException:
        return False


# =====================================================
# CONTROL FUNCTIONS
# =====================================================

def movement(command, status, description):
    if send_command(command, description):
        st.session_state.rover_status = status


def toggle_function(name):
    current = st.session_state.functions[name]

    commands = {
        "Cutter": ("C", "c"),
        "Pump": ("W", "w"),
        "Seed": ("G", "g"),
        "Plough": ("D", "U")
    }

    command = commands[name][0] if not current else commands[name][1]
    action = "ON" if not current else "OFF"

    if send_command(command, f"{name} {action}"):
        st.session_state.functions[name] = not current


def emergency_stop():
    if send_command("X", "Emergency Stop"):
        for name in st.session_state.functions:
            st.session_state.functions[name] = False

        st.session_state.rover_status = "Emergency Stopped"


# =====================================================
# DEVICE STATUS
# =====================================================

device_connected = get_device_status()

if device_connected:
    connection_text = "🟢 ESP32 Connected"
    connection_color = "#07821f"
else:
    connection_text = "🔴 ESP32 Not Connected"
    connection_color = "#c90000"


# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: Inter, sans-serif;
    background: linear-gradient(180deg,#e9f8e9,#fbfff9,#e9f8e9);
}

[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 100%;
    padding: 1rem;
}

.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
    background: linear-gradient(105deg,#003b15,#08732c,#164b22);
    color: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 14px;
}

.brand {
    font-size: 32px;
    font-weight: 900;
}

.sub {
    color: #c9f4c8;
    font-size: 18px;
    font-weight: 700;
}

.connection {
    background: white;
    border-radius: 30px;
    padding: 10px 18px;
    font-weight: 800;
}

.panel-title {
    background: linear-gradient(90deg,#00551c,#003e16);
    color: white;
    border-radius: 11px;
    padding: 13px 8px;
    text-align: center;
    font-weight: 850;
    font-size: 19px;
    margin-bottom: 12px;
}

.rover-stage {
    width: 100%;
    height: 350px;
    box-sizing: border-box;
    border: 2px solid #6da879;
    border-radius: 15px;
    background: radial-gradient(ellipse at 50% 78%,#a4c982,#477d3a 45%,#dcefe0);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.rover-stage:before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(165deg,transparent 0 38px,#ffffff18 39px 42px);
}

.rover-icon {
    font-size: 110px;
    z-index: 1;
    filter: drop-shadow(0 9px 7px #163b1c66);
}

.rover-status {
    position: absolute;
    bottom: 8px;
    left: 8px;
    right: 8px;
    background: #f7fff2ed;
    color: #102b16;
    padding: 10px;
    text-align: center;
    border-radius: 10px;
    font-weight: 800;
    z-index: 2;
}

.pill {
    display: inline-block;
    background: #07821f;
    color: white;
    padding: 5px 14px;
    border-radius: 30px;
}

.note {
    text-align: center;
    color: #55705a;
    font-size: 11px;
    margin-top: 8px;
}

div.st-key-move_f button,
div.st-key-move_l button,
div.st-key-move_s button,
div.st-key-move_r button,
div.st-key-move_b button {
    min-height: 65px;
    font-weight: 800;
    border-radius: 14px;
    background: linear-gradient(145deg,#087d24,#004817);
    color: white;
    border: 2px solid #159b2b;
}

div.st-key-move_s button {
    background: linear-gradient(145deg,#ff4035,#c90000);
    border-color: #ff9a8f;
}

div.st-key-emergency button {
    min-height: 55px;
    background: linear-gradient(180deg,#ff4035,#c90000);
    color: white;
    border: 3px solid #ff9a8f;
    font-weight: 900;
}

@media(max-width: 760px) {
    .hero {
        justify-content: center;
        text-align: center;
    }
    .rover-stage {
        height: 270px;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER - RENDERED ONLY ONCE
# =====================================================

header_html = f"""
<div class="hero">
    <div>
        <div class="brand">🌿 Agricultural Rover</div>
        <div class="sub">━━ Control System ━━</div>
    </div>
    <div class="connection">
        <span style="color:{connection_color}">
            {connection_text}
        </span>
    </div>
</div>
"""

st.html(header_html)


# =====================================================
# MAIN DASHBOARD - RENDERED ONLY ONCE
# =====================================================

left, center, right = st.columns([1, 1.12, 1], gap="small")


# -----------------------------------------------------
# LEFT: ROVER MOVEMENT
# -----------------------------------------------------

with left:
    with st.container(border=True):

        st.markdown(
            '<div class="panel-title">🎮 Rover Movement</div>',
            unsafe_allow_html=True
        )

        _, up, _ = st.columns(3)

        with up:
            if st.button("⬆️ Forward", key="move_f", use_container_width=True):
                movement("F", "Moving Forward", "Forward")

        a, b, c = st.columns(3)

        with a:
            if st.button("⬅️ Left", key="move_l", use_container_width=True):
                movement("L", "Turning Left", "Left")

        with b:
            if st.button("■ STOP", key="move_s", use_container_width=True):
                movement("S", "Stopped", "Stop")

        with c:
            if st.button("➡️ Right", key="move_r", use_container_width=True):
                movement("R", "Turning Right", "Right")

        _, down, _ = st.columns(3)

        with down:
            if st.button("⬇️ Backward", key="move_b", use_container_width=True):
                movement("B", "Moving Backward", "Backward")

        st.markdown(
            '<div class="note">Movement controls</div>',
            unsafe_allow_html=True
        )


# -----------------------------------------------------
# CENTER: ROVER VIEW
# -----------------------------------------------------

with center:
    with st.container(border=True):

        st.markdown(
            '<div class="panel-title">🚜 Rover View</div>',
            unsafe_allow_html=True
        )

        rover_html = f"""
        <div class="rover-stage">
            <div class="rover-icon">🚜</div>
            <div class="rover-status">
                🚜 Rover Status:
                <span class="pill">{st.session_state.rover_status}</span>
            </div>
        </div>
        """

        st.html(rover_html)

        st.markdown(
            '<div class="note">3D rover model and free camera view will be integrated next.</div>',
            unsafe_allow_html=True
        )


# -----------------------------------------------------
# RIGHT: AGRICULTURAL FUNCTIONS
# -----------------------------------------------------

with right:
    with st.container(border=True):

        st.markdown(
            '<div class="panel-title">🌱 Agricultural Functions</div>',
            unsafe_allow_html=True
        )

        function_rows = [
            ("Cutter", "⚙️"),
            ("Pump", "💧"),
            ("Seed", "🌾"),
            ("Plough", "⚒️")
        ]

        for index in range(0, 4, 2):
            c1, c2 = st.columns(2)

            for col, item in zip(
                (c1, c2),
                function_rows[index:index + 2]
            ):
                name, icon = item

                with col:
                    active = st.session_state.functions[name]
                    label = f"{icon} {name} {'ON' if active else 'OFF'}"

                    if st.button(
                        label,
                        key=f"func_{name.lower()}",
                        type="primary" if active else "secondary",
                        use_container_width=True
                    ):
                        toggle_function(name)
                        st.rerun()

        st.markdown(
            '<div class="note">Tap once to activate · tap again to deactivate</div>',
            unsafe_allow_html=True
        )


# =====================================================
# BOTTOM STATUS PANEL
# =====================================================

with st.container(border=True):

    s1, s2, s3 = st.columns([1.1, 1.2, 1])

    with s1:
        st.markdown(
            f"**📋 System Status:** {connection_text}"
        )

    with s2:
        if st.button(
            "⚠️ EMERGENCY STOP",
            key="emergency",
            use_container_width=True
        ):
            emergency_stop()
            st.rerun()

    with s3:
        with st.expander("📄 Activity Log"):
            for entry in st.session_state.activity:
                st.write("• " + entry)


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Dashboard commands are sent to the backend and queued for the ESP32. "
    "Use a physical power cutoff for hardware emergencies."
)

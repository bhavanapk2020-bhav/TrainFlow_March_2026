import streamlit as st
import cv2
from ultralytics import YOLO
import time
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TrainFlow Global", layout="wide", initial_sidebar_state="collapsed")

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>
    [data-testid="block-container"] { padding-top: 1rem; padding-bottom: 5rem; }
    div[data-testid="stNotification"] { display: none; }
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    .stApp { background: radial-gradient(circle at 20% 10%, #0f172a 0%, #020617 100%); color: #e2e8f0; font-family: 'Outfit', sans-serif; }
    
    .metric-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; margin-top: 10px; backdrop-filter: blur(10px); }
    .progress-bg { background: #1e293b; height: 8px; border-radius: 4px; margin: 12px 0; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
    
    .m-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; color: #64748b; }
    .m-value { font-size: 1.2rem; font-weight: 700; color: #f8fafc; }
    .c-low { color: #34d399; } .c-med { color: #fbbf24; } .c-high { color: #f87171; }

    .footer-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.95); padding: 10px 20px; display: flex; gap: 30px; border-top: 1px solid #334155; font-size: 0.75rem; color: #94a3b8; z-index: 1000; }
    .prime-rec { background: linear-gradient(90deg, #0ea5e9, #2563eb); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3); }
    
    .standby-box { text-align: center; padding: 100px 20px; border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; color: #94a3b8; }

            /* Style for START button */
div.stButton > button:first-child {
    background-color: white !important; /* Emerald Green */
    color: black !important;
    border: none !important;
}

/* Optional: Add hover effect for a premium feel */
div.stButton > button:hover {
    filter: brightness(1.2);
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER & CONTROLS ----------------
st.markdown("## TRAINFLOW <span style='font-weight:300; color:#64748b;'>PREMIUM</span>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([2, 1, 1])
with c1: selected_train = st.selectbox("", ["12625 Kerala Express", "16347 Mangalore Express"], label_visibility="collapsed")
with c2: performance_mode = st.checkbox("Performance Mode (Data Only)")
with c3:
    sc1, sc2 = st.columns(2)
    start_trigger = sc1.button("START", use_container_width=True)
    stop_trigger = sc2.button("STOP", use_container_width=True)

st.markdown("---")

# ---------------- LOGIC ----------------
@st.cache_resource
def get_model(): return YOLO("yolov8l.pt")
model = get_model()

# Handle State Transition
if not start_trigger:
    st.markdown('<div class="standby-box"><h3>SYSTEM STANDBY</h3><p>Select a train and click START to initialize real-time monitoring.</p></div>', unsafe_allow_html=True)
else:
    # Build grid only when started
    rec_slot = st.empty()
    cols = st.columns(3, gap="large")
    slots = []
    for i in range(3):
        with cols[i]:
            st.markdown(f"<p style='margin-bottom:10px; font-weight:600; color:#94a3b8;'>UNIT GS-{i+1}</p>", unsafe_allow_html=True)
            slots.append({"video": st.empty(), "metrics": st.empty()})

    trains = {
        "12625 Kerala Express": [r"C:\Users\ASUS\Desktop\DL_Projects\Train\Medium Crowd.mp4", r"C:\Users\ASUS\Desktop\DL_Projects\Train\Low Crowd.mp4", "Very Low.mp4"],
        "16347 Mangalore Express": [r"C:\Users\ASUS\Desktop\DL_Projects\Train\AnotherCrowd.mp4", r"C:\Users\ASUS\Desktop\DL_Projects\Train\DifferentCrowd.mp4", r"C:\Users\ASUS\Desktop\DL_Projects\Train\SampleVideo.mp4"]
    }
    caps = [cv2.VideoCapture(p) for p in trains[selected_train]]
    
    while True:
        current_data = []
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret: cap.set(cv2.CAP_PROP_POS_FRAMES, 0); continue
            
            res = model(frame, verbose=False, classes=[0])
            people = len(res[0].boxes)
            
            occ = int(min((people / 30) * 100, 100))
            c_label = "LOW" if occ < 20 else ("MEDIUM" if occ < 30 else "HIGH")
            c_class = "c-low" if occ < 20 else ("c-med" if occ < 30 else "c-high")
            bar_color = "#34d399" if occ < 20 else ("#fbbf24" if occ < 30 else "#f87171")

            if not performance_mode:
                annotated = res[0].plot(labels=False, boxes=True)
                if occ > 70: cv2.putText(annotated, "ALERT: HIGH CAPACITY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                slots[i]["video"].image(annotated, channels="BGR", use_container_width=True)
            else:
                slots[i]["video"].empty()
            
            slots[i]["metrics"].markdown(f"""
                <div class="metric-card">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span class="m-label">Occupancy</span><span class="m-value">{occ}%</span>
                    </div>
                    <div class="progress-bg"><div class="progress-fill" style="width:{occ}%; background:{bar_color};"></div></div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top:10px;">
                        <div><div class="m-label">Passengers</div><div class="m-value">{people}</div></div>
                        <div><div class="m-label">Seats Avail</div><div class="m-value">{max(30 - people, 0)}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            current_data.append({"id": i+1, "count": people})

        if current_data:
            best = min(current_data, key=lambda x: x['count'])
            rec_slot.markdown(f'<div class="prime-rec"><h2>OPTIMAL BOARDING: GS-{best["id"]}</h2></div>', unsafe_allow_html=True)

        if stop_trigger:
            for c in caps: c.release()
            st.rerun()
            break
        time.sleep(0.01)

# Footer
# 1. Create a placeholder at the bottom
footer_slot = st.empty()

# 2. Inside your while loop, update it:
while True:
    # ... your existing logic ...
    
    # 3. Refresh the footer with the new time
    footer_slot.markdown(f"""
    <div class="footer-bar">
        <span>🟢 ACTIVE</span>
        <span>⏰ {datetime.now().strftime("%H:%M:%S")}</span>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import cv2
from ultralytics import YOLO
import time
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TrainFlow Premium", layout="wide", initial_sidebar_state="collapsed")

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def go_to_dashboard():
    st.session_state.page = 'dashboard'

def go_to_landing():
    st.session_state.page = 'landing'

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>
.type-container {
    position: relative;
    display: inline-block;
    height: 3.2rem;
    animation: fadeAll 5s infinite;
}

/*Fade entire block together */
@keyframes fadeAll {
    0%, 70%   { opacity: 1; }
    85%, 100% { opacity: 0; }
}

/* Text lines */
.type-line {
    display: block;
    overflow: hidden;
    white-space: nowrap;
    width: 100%;     /*prevent shrinking */
}

/* Line 1 */
.line1 {
    color: #088F8F;
    animation: typing1 5s steps(25, end) infinite;
}

/* Line 2 */
.line2 {
    color: #020617;
    animation: typing2 5s steps(20, end) infinite;
}

/* Single cursor */
.type-container::after {
    content: "";
    position: absolute;
    width: 3px;
    height: 1.2em;
    background: #088F8F;
    animation: cursorMove 5s infinite, blink 0.5s infinite;
}

/* Typing animations */
@keyframes typing1 {
    0%   { width: 0 }
    30%  { width: 100% }
    100% { width: 100% }
}

@keyframes typing2 {
    0%   { width: 0 }
    35%  { width: 0 }
    65%  { width: 100% }
    100% { width: 100% }
}

/* Cursor movement */
@keyframes cursorMove {
    0%   { top: 0; left: 0; opacity: 1; }
    30%  { top: 0; left: 100%; opacity: 1; }
    35%  { top: 1.6em; left: 0; opacity: 1; }
    65%  { top: 1.6em; left: 100%; opacity: 1; }
    80%  { opacity: 0; }   /* fade with text */
    100% { top: 0; left: 0; opacity: 0; }
}

/* Blink */
@keyframes blink {
    50% { opacity: 0; }
}

    #stHeader { display: none !important; }
    [data-testid="block-container"] { padding-top: 2rem !important; }
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Outfit', sans-serif; }

    /* The Glowing Box on the Right */
    .hero-card-right {
        background: #ffffff; 
        padding: 50px; 
        border-radius: 40px; 
        border: 0px solid #ffffff; 
        /* Light Blue Glow Effect */
        box-shadow: 0 0 20px 5px #6cb0af;
        transition: transform 0.3s ease;
    }
    .square-frame {
    width: 100%;
    aspect-ratio: 1 / 1;   /* makes it square */
    overflow: hidden;
    border-radius: 16px;
    background: #000;
}

.square-frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;   /* crop nicely */
}
    /* Force square video frames */
[data-testid="stImage"] img {
    aspect-ratio: 1 / 1;
    object-fit: cover;
    border-radius: 16px;
}

    .metric-card { 
        background: #f8fafc; 
        border: 1px solid #e2e8f0; 
        border-radius: 20px; 
        padding: 20px; 
        margin-top: 15px; 
    }

    .progress-bg { background: #e2e8f0; height: 10px; border-radius: 10px; margin: 15px 0; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 10px; transition: width 0.8s ease; }
    
    .m-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #64748b; font-weight: 500; }
    .m-value { font-size: 1.4rem; font-weight: 800; color: #020617; }
    
    .prime-rec { 
        background: #f0fdfa;
        border: 2px solid #088F8F;
        color: #020617;
        padding: 15px; 
        border-radius: 15px; 
        text-align: center; 
        margin-bottom: 1.5rem; 
    }

    /* Professional Button Styling */
    div.stButton > button {
        background: #088F8F !important; 
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.8rem 2.5rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        background: #020617 !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION LOGIC ----------------

if st.session_state.page == 'landing':
    col1, col2 = st.columns([1, 1.3], gap="large")
    
    with col1:
        # Left Side: Project Description & Entry Point
        st.markdown("""
            <div style="margin-top: 50px;">
    <span style="background: #f1f5f9; padding: 5px 15px; border-radius: 50px; color: #64748b; font-weight: 600; font-size: 0.8rem; letter-spacing: 1px;">
        AI Crowd Intelligence
    </span>
    <!-- FIXED HEADING -->
    <h2 style="font-size: 2.5rem; font-weight: 800; margin-top: 20px; line-height: 1.2;">
    <span class="type-container">
                            <span class="type-line line1" style="color:#088F8F;"><i>Better boarding</i></span>
        <span class="type-line line2" style="color:#020617;"><i>starts here...</i></span>
    </div>
    <p style="font-size: 1.1rem; color: #475569; margin: 25px 0; line-height: 1.6;">
        TrainFlow gives you real-time visibility into train crowd levels, helping you choose the best coach and avoid unnecessary stress during boarding.
    </p>

</div>
            
        """, unsafe_allow_html=True)
        
        # Center the button on the left side
        st.button("LAUNCH DASHBOARD", on_click=go_to_dashboard)

    with col2:
        # RIGHT SIDE: YOUR HERO BLOCK WITH GLOW
        st.markdown("""
            <div class="hero-card-right">
                <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
                    <video width="90" autoplay loop muted playsinline>
                        <source src="https://cdn-icons-mp4.flaticon.com/512/7308/7308523.mp4" type="video/mp4">
                    </video>
                    <h1 style="font-size: 5.5rem; font-weight: 800; margin-bottom: 0; letter-spacing: -4px; text-align: center;">
                        <span style="color:#020617;">TRAIN</span><span style="color:#088F8F;">FLOW</span>
                    </h1>
                </div>
                <p style="font-size: 1.6rem; font-weight: 300; color: #64748b; margin-top: -10px; font-style: italic; text-align: center;">
                    Board Smarter with AI
                </p>
                <p style="max-width: 500px; margin: 30px auto; color: #020617; line-height: 1.6; text-align: center; font-size: 1rem; opacity: 0.8;">
                    AI Powered Real Time Train Crowd Monitoring & Smart Boarding Recommendation
                </p>
            </div>
        """, unsafe_allow_html=True)

else:
    # ---------------- DASHBOARD PAGE ----------------

    # 2. Main Dashboard Header
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 2rem; margin-top: -80px;">
        <div style="background: #ffffff; padding: 12px; border-radius: 16px; margin-right: 20px;">
        <video width="80" autoplay loop muted playsinline>
            <source src="https://cdn-icons-mp4.flaticon.com/512/7308/7308523.mp4" type="video/mp4">
        </video>
        </div>
        <div>
            <h2 style="margin:0; line-height:1; letter-spacing:-1px;">
                <span style="font-weight:800; font-size: 2.5rem; color:#020617;">TRAIN<span style="color:#088F8F;">FLOW</span></span>
                <span style="font-weight:300; font-size: 2.5rem; color:#64748b; margin-left:10px;"><i>Board Smarter with AI</i></span>
            </h2>
            <p style="margin:0; color:#020617; font-weight:400; letter-spacing: 1px; font-size: 0.8rem;">AI Powered Real Time Train Crowd Monitoring & Smart Boarding Recommendation</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: selected_train = st.selectbox("", ["12625 Kerala Express", "16347 Mangalore Express"], label_visibility="collapsed")
    with c2: performance_mode = st.checkbox("Video Off")
    with c3:
        sc1, sc2 = st.columns(2)
        start_trigger = sc1.button("START", use_container_width=True)
        stop_trigger = sc2.button("STOP", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- LOGIC ----------------
    @st.cache_resource
    def get_model(): return YOLO("yolov8l.pt")
    model = get_model()

    if not start_trigger:
        st.markdown("""
            <div class="hero-container">
                <div style="text-align:center;">
                    <h1 style="color:white; font-size: 3rem; margin-bottom: 0;">READY FOR DEPLOYMENT</h1>
                    <p style="color:#94a3b8; font-size: 1.2rem;">Select train fleet to begin real-time neural analysis</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        rec_slot = st.empty()
        cols = st.columns(3, gap="large")
        slots = []
        for i in range(3):
            with cols[i]:
                st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 15px; opacity: 0.8;">
                        <div style="width: 8px; height: 8px; background: #020617; border-radius: 50%; margin-right: 10px;"></div>
                        <span style="font-weight: 600; letter-spacing: 2px; font-size: 0.8rem; color: #94a3b8;">COMPARTMENT GS-{i+1}</span>
                    </div>
                """, unsafe_allow_html=True)
                slots.append({"video": st.empty(), "metrics": st.empty()})

        trains = {
            "12625 Kerala Express": [r"C:\Users\ASUS\Desktop\DL_Projects\Train\Medium Crowd.mp4", r"C:\Users\ASUS\Desktop\DL_Projects\Train\Low Crowd.mp4", r"C:\Users\ASUS\Desktop\DL_Projects\Train\Very Low.mp4"],
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
                bar_color = "#10b981" if occ < 20 else ("#f59e0b" if occ < 30 else "#ef4444")

                if not performance_mode:
                    annotated = res[0].plot(labels=False, boxes=True)
                    slots[i]["video"].image(annotated, channels="BGR", use_container_width=True)
                else:
                    slots[i]["video"].empty()
                
                slots[i]["metrics"].markdown(f"""
                    <div class="metric-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                            <div>
                                <div class="m-label">Live Occupancy</div>
                                <div class="m-value">{occ}%</div>
                            </div>
                            <div style="text-align:right;">
                                <div class="m-label">Passengers</div>
                                <div class="m-value" style="color:#088F8F;">{people}</div>
                            </div>
                        </div>
                        <div class="progress-bg"><div class="progress-fill" style="width:{occ}%; background:{bar_color}; box-shadow: 0 0 15px {bar_color}44;"></div></div>
                        <div style="margin-top:10px;">
                            <span class="m-label">Available Seats: </span>
                            <span style="font-weight:700; color:#020617;">{max(30 - people, 0)}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                current_data.append({"id": i+1, "count": people})

            if current_data:
                best = min(current_data, key=lambda x: x['count'])
                rec_slot.markdown(f'<div class="prime-rec"><h2>OPTIMAL BOARDING UNIT: GS-{best["id"]}</h2></div>', unsafe_allow_html=True)

            if stop_trigger:
                for c in caps: c.release()
                st.rerun()
                break
            time.sleep(0.01)

    # Footer (Only on Dashboard)
    st.markdown(f"""
    <div style="position:fixed; bottom:0; left:0; width:100%; background:#ffffff; padding:15px 40px; border-top:1px solid rgba(0,0,0,0.05); display:flex; justify-content:space-between; font-size:0.8rem; color:#64748b; z-index:1000;">
        <div style="display:flex; gap:30px;">
            <span style="color:#10b981;">● SYSTEM ONLINE</span>
            <span>TRAIN : {selected_train if 'selected_train' in locals() else 'STANDBY'}</span>
        </div>
        <span>{datetime.now().strftime("%H:%M:%S")}</span>
    </div>
    """, unsafe_allow_html=True)
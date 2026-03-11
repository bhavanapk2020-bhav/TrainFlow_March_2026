import streamlit as st
import cv2
from ultralytics import YOLO
import time
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TrainFlow Premium", layout="wide", initial_sidebar_state="collapsed")

# Initialize Session State for Page Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def go_to_dashboard():
    st.session_state.page = 'dashboard'

def go_to_landing():
    st.session_state.page = 'landing'

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>

    /* Hides the default Streamlit header/menu space */
    #stHeader {
        display: none !important;
    }

    [data-testid="block-container"] {
        padding-top: 0rem !important; /* Change 1rem to 0rem for zero padding */
        padding-bottom: 0rem !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Optional: Hide the default header/menu if you want even more space */
        #stHeader { display: none !important; }
    
    /* Global Background */
    .stApp { 
        margin-top: 0px !important;
        background-color: #ffffff;
        color: #f8fafc; 
        font-family: 'Outfit', sans-serif; 
    }
    
    /* Landing Page Specific Styles */
    .landing-hero {
        text-align: center;
        padding: 100px 20px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }

    /* Dashboard Glass Cards */
    .metric-card { 
        background: rgba(255, 255, 255, 0.02); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 24px; 
        padding: 24px; 
        margin-top: 15px; 
        backdrop-filter: blur(12px);
    }

    .progress-bg { background: rgba(255,255,255,0.05); height: 6px; border-radius: 10px; margin: 15px 0; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 10px; transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1); }
    
    .m-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #020617; font-weight: 500; }
    .m-value { font-size: 1.4rem; font-weight: 800; color: black; }
    
    .prime-rec { 
    background: transparent !important; /* Removes the color/gradient */
    border: 0.2px solid #088F8F !important; /* Adds a clear outline */
    color: #0f172a !important; /* Changes text to dark for readability */
    padding: 5px; 
    border-radius: 5px; 
    text-align: center; 
    margin-bottom: 1rem; 
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important; 
    
}
    
    .hero-container {
        position: relative; border-radius: 30px; overflow: hidden; height: 400px;
        display: flex; align-items: center; justify-content: center;
        background: url('https://images.unsplash.com/photo-1515165599668-93f4bd3932a2?q=80&w=2070&auto=format&fit=crop') center center;
        background-size: cover; box-shadow: inset 0 0 0 1000px rgba(2, 6, 23, 0.7);
    }

    /* Premium Button Styles */
    div.stButton > button:first-child {
        background: #088F8F !important; 
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.8rem 2.5rem !important;
        border: none !important;
        transition: 0.3s ease;
    }
    
    /* Specific Black Button for Back action */
    .custom-back-btn button {
        background-color: #020617 !important;
        color: #ffffff !important;
        border: 1px solid #020617 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION LOGIC ----------------

if st.session_state.page == 'landing':
    # ---------------- LANDING PAGE ----------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="landing-hero">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
                <video width="80" autoplay loop muted playsinline>
                    <source src="https://cdn-icons-mp4.flaticon.com/512/7308/7308523.mp4" type="video/mp4">
                </video>
                <h1 style="font-size: 5rem; font-weight: 800; margin-bottom: 0; letter-spacing: -3px;">
                    <span style="color:#020617;">TRAIN<span style="color:#088F8F;">FLOW</span>
                </h1>
            </div>
            <p style="font-size: 1.5rem; font-weight: 300; color: #64748b; margin-top: -10px; font-style: italic;">
                Board Smarter with AI
            </p>
            <p style="max-width: 700px; margin: 30px auto; color: #020617; line-height: 1.6;">
                AI Powered Real Time Train Crowd Monitoring & Smart Boarding Recommendation
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 1, 1])
    with col_btn_2:
        st.button("EXPLORE DASHBOARD", on_click=go_to_dashboard, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

else:
    # ---------------- DASHBOARD PAGE ----------------
    
    # 1. Back button in top-right
    col1, col2 = st.columns([0.94, 0.06])
    with col2:
        st.markdown('<div class="custom-back-btn">', unsafe_allow_html=True)
        if st.button("Back", help="Return to Home"):
            go_to_landing()
        st.markdown('</div>', unsafe_allow_html=True)

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
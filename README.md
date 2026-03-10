#OmniRail: GS Occupancy Monitor
OmniRail is a real-time monitoring system designed to track passenger density in General Compartment (GS) coaches. Using computer vision and deep learning, the platform provides station operators with live occupancy data, assisting in crowd management and boarding efficiency.

##Project Overview
General compartments often experience unpredictable passenger density. This project automates the monitoring process by analyzing platform or coach video feeds to determine the occupancy level in real-time. By providing visual and numerical metrics, the system enables more informed decision-making for station staff.

##Technical Specifications
Core Engine: YOLOv8 Object Detection

Framework: Streamlit (Python)

Computer Vision: OpenCV

Latency: ~42ms (optimized for real-time analysis)

UI: Custom CSS-based dark mode dashboard

##Key Features
Multi-Unit Monitoring: Tracks up to three GS units simultaneously to provide a holistic view of the train.

Density Analytics: Calculates the occupancy percentage and identifies the least crowded GS unit.

Operational Modes: Supports a "Performance Mode" (Data-Only) to minimize system resource usage during heavy monitoring loads.

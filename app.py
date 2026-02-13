import streamlit as st

st.set_page_config(page_title="Role-Based Governance Dashboard", layout="wide")

# ======================================================
# USER DATABASE
# ======================================================

users = {
    "Rohan": {"password": "Rohan", "role": "Event Coordinator", "department": "CSE"},
    "Trinadh": {"password": "Trinadh", "role": "HOD", "department": "CSE"},
    "Dhadi": {"password": "dhadi", "role": "Dean", "department": "General"},
    "Reddy": {"password": "Reddy", "role": "Institutional Head", "department": "General"},
    "Naidu": {"password": "Naidu", "role": "Admin", "department": "General"},
}

roles_list = [
    "Event Coordinator",
    "HOD",
    "Dean",
    "Institutional Head",
    "Admin"
]

# ======================================================
# SESSION STATE
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.department = ""

# ======================================================
# LOGIN FUNCTION
# ======================================================

def login():
    st.title("🔐 Role-Based Governance Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    selected_role = st.selectbox("Select Role", roles_list)

    if st.button("Login"):
        if (
            username in users and
            users[username]["password"] == password and
            users[username]["role"] == selected_role
        ):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = selected_role
            st.session_state.department = users[username]["department"]
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials or Role Mismatch")

# ======================================================
# LOGOUT FUNCTION
# ======================================================

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.department = ""
    st.rerun()

# ======================================================
# DATA
# ======================================================

venues = {
    "Auditorium": {"capacity": 200, "occupied": 150, "department": "General"},
    "Seminar Hall": {"capacity": 80, "occupied": 75, "department": "CSE"},
    "Conference Room": {"capacity": 40, "occupied": 20, "department": "ECE"},
    "Lab Hall": {"capacity": 60, "occupied": 60, "department": "CSE"},
}

events = [
    {"name": "AI Workshop", "department": "CSE", "venue": "Seminar Hall", "participants": 75},
    {"name": "Robotics Meetup", "department": "ECE", "venue": "Conference Room", "participants": 20},
    {"name": "Cultural Fest", "department": "General", "venue": "Auditorium", "participants": 150},
]

# ======================================================
# HELPER FUNCTIONS
# ======================================================

def occupancy_percentage(capacity, occupied):
    return round((occupied / capacity) * 100, 2)

def occupancy_status(capacity, occupied):
    if occupied >= capacity:
        return "❌ Fully Occupied"
    elif occupied >= capacity * 0.85:
        return "⚠ Nearly Full"
    else:
        return "✅ Available"

def generate_summary(role):
    full = sum(1 for v in venues.values() if v["occupied"] >= v["capacity"])
    high = sum(1 for v in venues.values() if v["occupied"] >= v["capacity"] * 0.85)

    if role == "Event Coordinator":
        return "Access restricted to your submitted events."
    elif role == "HOD":
        return f"{high} venue(s) nearing capacity in your department."
    elif role == "Dean":
        return f"{full} fully occupied venue(s) across departments."
    elif role == "Institutional Head":
        return f"Institution-wide monitoring active. {high} venue(s) at high occupancy."
    elif role == "Admin":
        return "Administrative control active. You can modify occupancy states."

# ======================================================
# MAIN APP
# ======================================================

if not st.session_state.logged_in:
    login()

else:
    role = st.session_state.role
    department = st.session_state.department

    st.title("🏛 Role-Specific Governance Dashboard")
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.sidebar.info(f"Role: {role}")
    st.sidebar.button("Logout", on_click=logout)

    st.markdown("---")
    st.header("📊 Dashboard Overview")

    # ------------------------------------------------------
    # EVENT COORDINATOR
    # ------------------------------------------------------

    if role == "Event Coordinator":
        st.subheader("📄 Your Submitted Events")

        for event in events:
            if event["department"] == department:
                st.write(f"Event: {event['name']}")
                st.write(f"Venue: {event['venue']}")
                st.write(f"Participants: {event['participants']}")
                st.markdown("---")

        st.warning("Global occupancy data restricted.")

    # ------------------------------------------------------
    # HOD
    # ------------------------------------------------------

    elif role == "HOD":
        st.subheader("🏫 Department Venue Status")

        for venue, data in venues.items():
            if data["department"] == department:
                percent = occupancy_percentage(data["capacity"], data["occupied"])
                status = occupancy_status(data["capacity"], data["occupied"])
                st.metric(venue, f"{percent}% Occupied")
                st.write(status)
                st.markdown("---")

    # ------------------------------------------------------
    # DEAN
    # ------------------------------------------------------

    elif role == "Dean":
        st.subheader("🏛 Cross-Department Venue Overview")

        for venue, data in venues.items():
            percent = occupancy_percentage(data["capacity"], data["occupied"])
            status = occupancy_status(data["capacity"], data["occupied"])
            st.metric(venue, f"{percent}% Occupied")
            st.write(f"Department: {data['department']}")
            st.write(status)
            st.markdown("---")

    # ------------------------------------------------------
    # INSTITUTIONAL HEAD
    # ------------------------------------------------------

    elif role == "Institutional Head":
        st.subheader("👑 Institutional Occupancy Overview")

        total_capacity = sum(v["capacity"] for v in venues.values())
        total_occupied = sum(v["occupied"] for v in venues.values())
        overall_percent = occupancy_percentage(total_capacity, total_occupied)

        st.metric("Overall Institutional Occupancy", f"{overall_percent}%")

        for venue, data in venues.items():
            percent = occupancy_percentage(data["capacity"], data["occupied"])
            st.metric(venue, f"{percent}%")

    # ------------------------------------------------------
    # ADMIN
    # ------------------------------------------------------

    elif role == "Admin":
        st.subheader("🛠 Administrative Control Panel")

        selected_venue = st.selectbox("Select Venue", list(venues.keys()))

        new_occupied = st.slider(
            "Adjust Occupied Count",
            0,
            venues[selected_venue]["capacity"],
            venues[selected_venue]["occupied"]
        )

        venues[selected_venue]["occupied"] = new_occupied

        percent = occupancy_percentage(
            venues[selected_venue]["capacity"],
            venues[selected_venue]["occupied"]
        )

        st.success(f"{selected_venue} updated to {percent}% occupancy.")

    st.markdown("---")
    st.header("📌 System Insight")
    st.info(generate_summary(role))

    st.markdown("---")
    st.caption("Secure Role-Based Governance Dashboard | Hackathon Prototype")

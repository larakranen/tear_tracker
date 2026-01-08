import streamlit as st
import sqlite3
from datetime import datetime

def save_entry(ts, dur, loc, cat, intns, alone, ppl, period, nts):
    # 1. Open the connection
    conn = sqlite3.connect('tears.db')
    c = conn.cursor()
    
    # 2. The SQL logic
    query = '''INSERT INTO crying_logs 
               (timestamp, duration_minutes, location, category, intensity, was_alone, people_involved, is_period, notes) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    c.execute(query, (ts, dur, loc, cat, intns, alone, ppl, period, nts))
    
    # 3. Save and Close
    conn.commit()
    conn.close()

st.title("💧 My cry tracker 2026 💧")

# Define map of locations
locations_map = {
    "Home": ["Bedroom", "Workroom", "Bathroom", "Living Room", "Kitchen", "Garden", "Other"],
    "Public": ["Street", "Park", "Store/Mall", "Other"],
    "Travel": ["Public Transport", "Car", "Plane", "Train Station", "Other"],
    "Other": ["Other"]
}

# Define the category map
category_map = {
    "Sad": ["Video on social media", "Miss my family", "Music", "Sad Movie", "Loneliness", "Other"],
    "Stressed": ["School", "Overwhelmed", "Tired/Burnout", "Other"],
    "Happy": ["Proud moment", "Relief", "Music", "Social media video", "Other"],
    "Other": ["Other"]
}

# In case the cry was not logged on time
is_manual = st.checkbox("Log for a different time? (Back-logging)")
if is_manual:
    col_date, col_time = st.columns(2)
    with col_date:
        manual_date = st.date_input("Date of cry", value=datetime.now())
    with col_time:
        manual_time = st.time_input("Time of cry", value=datetime.now())
    
    # Combine date and time into one string for the database
    timestamp_to_save = f"{manual_date} {manual_time}"
else:
    # Use the current time automatically
    timestamp_to_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.caption(f"Logging at: {timestamp_to_save}")

# Start the form layour. Use columns to make it look nice on mobile
col1, col2 = st.columns(2)

with col1:
    duration = st.number_input("Duration (minutes)", min_value=1, value=5)
    # --- SMART LOCATION LOGIC STARTS HERE ---
    main_loc = st.selectbox("Where did I cry?", options=list(locations_map.keys()))
    if main_loc == "Other":
        custom_loc = st.text_input("Specify location:")
        final_location = f"Other: {custom_loc}"
    else:
        sub_loc = st.selectbox(f"Specific spot in {main_loc}:", options=locations_map[main_loc])
        if sub_loc == "Other":
            specific = st.text_input(f"Where in {main_loc} specifically?")
            final_location = f"{main_loc}: {specific}"
        else:
            final_location = f"{main_loc}: {sub_loc}"
    # --- SMART LOCATION LOGIC ENDS ---
    # --- SMART CATEGORY LOGIC STARTS HERE ---
    main_cat = st.selectbox("Main Emotion", options=list(category_map.keys()))
    sub_cat = st.selectbox(f"Reason for feeling {main_cat}:", options=category_map[main_cat])
    if sub_cat == "Other":
        custom_cat = st.text_input("Please specify the reason:")
        final_category = f"{main_cat}: {custom_cat}"
    else:
        final_category = f"{main_cat}: {sub_cat}"
    # --- SMART CATEGORY LOGIC ENDS ---
    intensity = st.slider("Intensity", 1, 10, 5)

with col2:
    was_alone = st.checkbox("Was I alone?")
    # Only show the "Who" box if was_alone is NOT checked
    people = ""
    if not was_alone:
        people = st.text_input("Who was with me?", placeholder="Names...")
    period = st.checkbox("Was this during my period? 🩸")
    notes = st.text_area("What happened?", placeholder="What triggered it?")

if st.button("Log this cry", use_container_width=True):
    # Here you call the function and pass the data from the screen into it
    save_entry(
        timestamp_to_save,
        duration,
        final_location,
        final_category,
        intensity,
        was_alone,
        people,
        period,
        notes
    )
    st.success("Saved!")
    st.balloons()
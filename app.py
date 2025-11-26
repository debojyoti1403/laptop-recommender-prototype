import streamlit as st
import pandas as pd

# 1. Page Config & Title
st.set_page_config(page_title="Laptop NPD Agent", layout="centered")
st.title("💻 Laptop Preference Analyzer (NPD)")
st.caption("Academic Project: Analyzing User Needs vs Market Availability")

# 2. Load Data Function
@st.cache_data
def load_data():
    try:
        # We load YOUR specific file name
        df = pd.read_csv("laptops.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame() # Return empty if file missing

df = load_data()

# 3. Initialize Memory (Session State)
if "step" not in st.session_state:
    st.session_state.step = 1
if "filters" not in st.session_state:
    st.session_state.filters = {} # Store user answers here
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am the NPD Research Agent. To start, what is your **primary purpose** for this laptop?"}
    ]

# 4. Helper Function to Move to Next Question
def next_step(user_text, bot_response):
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.step += 1
    st.rerun()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- QUESTION 1: PURPOSE ---
if st.session_state.step == 1:
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("Student 🎓"):
        st.session_state.filters['purpose'] = ['student']
        next_step("Student Use", "Got it. Budget is key. What is your **maximum price range**?")
        
    if col2.button("Office 💼"):
        st.session_state.filters['purpose'] = ['office', 'business'] 
        next_step("Office Work", "Reliability is key. What is your **maximum price range**?")
        
    if col3.button("Gaming 🎮"):
        st.session_state.filters['purpose'] = ['gaming']
        next_step("Gaming", "Performance is key. What is your **maximum price range**?")
        
    if col4.button("Creative 🎨"):
        st.session_state.filters['purpose'] = ['content']
        next_step("Content Creation", "Display is key. What is your **maximum price range**?")
        

# --- QUESTION 2: BUDGET (INR) ---
elif st.session_state.step == 2:
    # Slider from 20k to 200k based on your data
    budget = st.slider("Select Max Budget (₹)", 20000, 200000, step=5000, value=60000)
    
    if st.button("Confirm Budget"):
        st.session_state.filters['max_price'] = budget
        next_step(f"Under ₹{budget}", "Noted. Do you have a preference for the **Processor Brand**?")

# --- QUESTION 3: PROCESSOR ---
elif st.session_state.step == 3:
    c1, c2, c3 = st.columns(3)
    
    if c1.button("Intel"):
        st.session_state.filters['processor'] = 'Intel'
        next_step("Intel", "Okay. Lastly, how important is **Screen Quality**?")
        
    if c2.button("AMD"):
        st.session_state.filters['processor'] = 'AMD'
        next_step("AMD", "Okay. Lastly, how important is **Screen Quality**?")
        
    if c3.button("No Preference"):
        st.session_state.filters['processor'] = 'Any'
        next_step("No Preference", "Okay. Lastly, how important is **Screen Quality**?")

# --- QUESTION 4: SCREEN PANEL ---
elif st.session_state.step == 4:
    c1, c2 = st.columns(2)
    
    if c1.button("Best Quality (IPS/OLED)"):
        st.session_state.filters['panel'] = ['IPS', 'OLED']
        next_step("High Quality", "Analyzing database matches now...")
        
    if c2.button("Standard is fine"):
        st.session_state.filters['panel'] = ['IPS', 'OLED', 'TN'] # All types
        next_step("Standard", "Analyzing database matches now...")

# --- FINAL STEP: RESULTS ---
elif st.session_state.step == 5:
    if df.empty:
        st.error("⚠️ Database not loaded. Please upload 'laptops.csv' to GitHub.")
    else:
        # Start with all data
        results = df.copy()
        
        # 1. Filter by Purpose (checking if tag is inside the text)
        tags = st.session_state.filters['purpose']
        results = results[results['purpose_tags'].apply(lambda x: any(t in str(x).lower() for t in tags))]
        
        # 2. Filter by Price
        results = results[results['price_inr'] <= st.session_state.filters['max_price']]
        
        # 3. Filter by Processor
        if st.session_state.filters['processor'] != 'Any':
            results = results[results['processor_brand'] == st.session_state.filters['processor']]
            
        # 4. Filter by Screen Panel
        results = results[results['screen_panel'].isin(st.session_state.filters['panel'])]
        
        # DISPLAY MATCHES
        st.divider()
        if not results.empty:
            st.success(f"✅ Found {len(results)} perfect matches!")
            results = results.sort_values(by='rating', ascending=False)
            
            for index, row in results.head(5).iterrows():
                with st.container():
                    st.subheader(f"{row['brand']} {row['model']}")
                    st.caption(f"Specs: {row['processor_brand']} {row['processor_model']} | {row['ram_gb']}GB RAM")
                    st.write(f"**Price:** ₹{row['price_inr']} | **Rating:** ⭐ {row['rating']}")
                    st.link_button("View Details", row['link'])
                    st.markdown("---")
        else:
            st.warning("😕 No exact matches found. Try increasing your budget.")
            
        if st.button("Start New Search"):
            st.session_state.step = 1
            st.session_state.messages = []
            st.session_state.filters = {}
            st.rerun()

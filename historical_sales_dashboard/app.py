import streamlit as st
import time
from datetime import datetime
import requests
from streamlit_lottie import st_lottie

# === Styles ===
st.markdown("""
<style>
/* GLOBAL CONTAINER */
.section {
    background-color: #ffffff;
    padding: 1.25rem 2rem;
    margin-bottom: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

/* HEADER STYLE */
h3, h2, h1 {
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    text-align: left;
    color: #1e1e1e;
    margin-bottom: 1rem;
}

/* BUTTON ALIGNMENT */
button[kind="primary"] {
    width: 100%;
    font-weight: bold;
    font-size: 16px;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

/* KPI COLUMN METRICS */
[data-testid="stMetric"] {
    text-align: center;
    background-color: #f7fafd;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 0 8px rgba(0,0,0,0.03);
}

/* FLIP CARDS */
.flip-card {
  background-color: transparent;
  width: 280px;
  height: 160px;
  perspective: 1000px;
  display: inline-block;
  margin: 1rem 1rem;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 12px;
  box-shadow: 0 0 8px rgba(0,0,0,0.1);
}
.flip-card-front {
  background-color: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}
.flip-card-back {
  background-color: #eff6ff;
  color: #1e293b;
  transform: rotateY(180deg);
  padding: 1rem;
  font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


# === Navigation Buttons ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 🔀 Navigate Between Pages")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Lifecycle Comparison"):
        st.switch_page("pages/1_Lifecycle_Comparison.py")
with col2:
    if st.button("📈 Weekly Trends"):
        st.switch_page("pages/2_Weekly_Trends.py")
with col3:
    if st.button("📌 Benchmark Model"):
        st.switch_page("pages/3_Benchmark_Model.py")
with col4:
    if st.button("👥 Customer Analysis"):
        st.switch_page("pages/4_Customer_Analysis.py")
st.markdown('</div>', unsafe_allow_html=True)

# === Smart Alert ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.warning("⚠️ WA branch has dropped 5% compared to last week.")
st.markdown('</div>', unsafe_allow_html=True)

# === Lottie Animation ===
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_icon = load_lottieurl("https://lottie.host/dfca40d5-6ae3-49aa-bae7-ef28e881041c/synMYkzwXS.json")
if lottie_icon:
    with st.container():
        st_lottie(lottie_icon, height=200, key="magic")

# === Welcome Typewriter ===
st.markdown('<div class="section">', unsafe_allow_html=True)
with st.empty():
    msg = "✨ Welcome to Your Enhanced Magic Dashboard ✨"
    for i in range(len(msg) + 1):
        st.markdown(f"<h3>{msg[:i]}</h3>", unsafe_allow_html=True)
        time.sleep(0.02)
st.markdown('</div>', unsafe_allow_html=True)

# === Persona Logic ===
st.markdown('<div class="section">', unsafe_allow_html=True)
persona = st.selectbox("🧑 Who are you today?", ["Manager", "Sales Rep", "Customer", "Guest"])
if persona == "Manager":
    st.success("Welcome back, Executive! Here's your company-wide status summary 📊")
elif persona == "Sales Rep":
    st.info("Hello Sales Rep! Time to conquer those leads 🔥")
elif persona == "Customer":
    st.warning("Welcome! Explore your purchase history and rewards 🛍️")
else:
    st.info("Enjoy the dashboard! Let’s explore what's possible 💡")
st.markdown('</div>', unsafe_allow_html=True)

# === Holiday Celebration ===
now = datetime.now()
if now.month == 12:
    st.snow()
    st.markdown("🎄 Happy Holidays!")
elif now.month == 6:
    st.balloons()
    st.markdown("🎉 Mid-Year Motivation! Let’s push to the next level!")

# === KPI Cards ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📊 Key KPIs at a Glance")
kpis = {
    "Monthly Revenue": ("₹1.2M", "+5%"),
    "Customer Growth": ("8,200", "+2.1%"),
    "Retention Rate": ("76%", "-1.2%"),
}
cols = st.columns(len(kpis))
for i, (label, (value, delta)) in enumerate(kpis.items()):
    cols[i].metric(label, value, delta)
st.markdown('</div>', unsafe_allow_html=True)

# === ROI Calculator ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📈 ROI Calculator")
rev = st.number_input("Enter Expected Revenue", value=1200000)
cost = st.number_input("Enter Cost", value=800000)
if cost:
    roi = ((rev - cost) / cost) * 100
    st.success(f"📊 Estimated ROI: {roi:.2f}%")
st.markdown('</div>', unsafe_allow_html=True)


# === Live Conversion Simulator ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("🔄 Conversion Impact Simulator")
traffic = st.slider("Visitors", 1000, 100000, 25000, step=1000)
conversion_rate = st.slider("Conversion Rate (%)", 1.0, 10.0, 3.5)
avg_order_value = st.slider("Avg. Order Value (₹)", 100, 5000, 750)

est_revenue = int((traffic * (conversion_rate / 100)) * avg_order_value)
st.metric("🧾 Estimated Revenue", f"₹{est_revenue:,}")
st.markdown('</div>', unsafe_allow_html=True)


# === Achievement Unlocking ===
roi = ((rev - cost) / cost) * 100 if cost else 0
if roi > 40:
    st.balloons()
    st.success("🎉 Achievement Unlocked: High-ROI Campaign!")


# === Ask-a-Bot ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("🤖 Ask the Dashboard a Question")
q = st.text_input("What would you like to know?")
if q:
    if "sales" in q.lower():
        st.info("💰 Sales this month crossed ₹1.8M")
    elif "growth" in q.lower():
        st.info("📈 Growth rate is steady at 8.5%")
    else:
        st.warning("🤔 I'm still learning. Try asking about 'sales' or 'growth'")
st.markdown('</div>', unsafe_allow_html=True)



# === Countdown ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("⏳ Countdown to Q3 Launch")
launch_date = datetime(2025, 9, 1)
days_left = (launch_date - datetime.now()).days
st.metric("🚀 Days to Launch", f"{days_left} days")
st.markdown('</div>', unsafe_allow_html=True)

# === Revenue Counter ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📈 Quarterly Revenue Count")
target = 18000
placeholder = st.empty()
for i in range(0, target + 1, 800):
    placeholder.metric("Quarterly Revenue", f"${i:,}")
    time.sleep(0.02)
st.markdown('</div>', unsafe_allow_html=True)

# === Branch Progress ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📍 Branch Performance")
st.write("**WA Branch**")
st.progress(0.72)
st.write("**NSW Branch**")
st.progress(0.55)
st.write("**QLD Branch**")
st.progress(0.81)
st.markdown('</div>', unsafe_allow_html=True)



# === Flip Cards ===
st.subheader("🔄 Flip Cards with Smart Tips")
st.markdown("""
<div class="flip-card"><div class="flip-card-inner">
<div class="flip-card-front">💰 Revenue Tip</div>
<div class="flip-card-back">Upselling increases revenue by 30% avg.</div>
</div></div>

<div class="flip-card"><div class="flip-card-inner">
<div class="flip-card-front">📈 Growth Fact</div>
<div class="flip-card-back">Data-driven firms grow 8x faster.</div>
</div></div>

<div class="flip-card"><div class="flip-card-inner">
<div class="flip-card-front">🎯 Targeting</div>
<div class="flip-card-back">Quarter goals = better team focus & forecast.</div>
</div></div>

<div class="flip-card"><div class="flip-card-inner">
<div class="flip-card-front">🤝 Retention Hack</div>
<div class="flip-card-back">Personalized emails improve retention by 18%.</div>
</div></div>

<div class="flip-card"><div class="flip-card-inner">
<div class="flip-card-front">📅 Timing Insight</div>
<div class="flip-card-back">Emails sent on Tuesdays get 20% more responses.</div>
</div></div>

<div class="flip-card"><div class="flip-card-inner">
<div class="flip-card-front">📊 Conversion Trick</div>
<div class="flip-card-back">Using urgency messaging can lift conversions by 12%.</div>
</div></div>
""", unsafe_allow_html=True)


# === Email Button ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📤 Email This Dashboard Summary")
summary = "Check out the dashboard I just viewed. Great insights and KPIs!"
st.markdown(f"""
<a href="mailto:client@example.com?subject=Dashboard Summary&body={summary}" target="_blank">
    📧 <button style='background-color:#4CAF50;color:white;border:none;padding:0.6em 1.2em;border-radius:10px;cursor:pointer;'>Send Summary Email</button>
</a>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# === Feedback Form ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📝 Quick Feedback")
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email (optional)")
    feedback = st.text_area("Your thoughts?")
    rating = st.slider("Rate us", 1, 10, 7)
    if st.form_submit_button("Submit"):
        st.success(f"Thank you, {name or 'Guest'}! 🙏")
st.markdown('</div>', unsafe_allow_html=True)

# === Print Button ===
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("🖨️ Save or Print This Page")
st.markdown('<button onclick="window.print()">🖨️ Print/Save as PDF</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# === Footer ===
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #6b7280;">
    <p>© 2025 Magic Dashboard. All rights reserved.</p>
    <p>Made with ❤️ by Your Nagasai Petnikoti from 
            IFA</p>
</div>
""", unsafe_allow_html=True)    

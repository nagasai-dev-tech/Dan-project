import streamlit as st
import time
from datetime import datetime
import requests
from streamlit_lottie import st_lottie
from PIL import Image

# ==== CSS ====
st.markdown("""
<style>
body::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    background: url('https://raw.githubusercontent.com/anup-a/svg-animation-backgrounds/main/magic/sparkles.svg') repeat;
    animation: moveBackground 60s linear infinite;
    opacity: 0.05;
    z-index: -1;
}
@keyframes moveBackground {
    0% { background-position: 0 0; }
    100% { background-position: 1000px 1000px; }
}
.flip-card {
  background-color: transparent;
  width: 300px;
  height: 180px;
  perspective: 1000px;
  display: inline-block;
  margin: 1em;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 1s;
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
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}
.flip-card-front {
  background-color: #007acc;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}
.flip-card-back {
  background-color: #f0f8ff;
  color: #333;
  transform: rotateY(180deg);
  padding: 1em;
  font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ==== Lottie Animation ====
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_icon = load_lottieurl("https://lottie.host/dfca40d5-6ae3-49aa-bae7-ef28e881041c/synMYkzwXS.json")
if lottie_icon:
    st_lottie(lottie_icon, height=200, key="magic")

# ==== Typewriter Welcome ====
with st.empty():
    msg = "✨ Welcome to Your Enhanced Magic Dashboard ✨"
    for i in range(len(msg) + 1):
        st.markdown(f"<h3>{msg[:i]}</h3>", unsafe_allow_html=True)
        time.sleep(0.03)

# ==== Persona Logic ====
persona = st.selectbox("🧑 Who are you today?", ["Manager", "Sales Rep", "Customer", "Guest"])
if persona == "Manager":
    st.success("Welcome back, Executive! Here's your company-wide status summary 📊")
elif persona == "Sales Rep":
    st.info("Hello Sales Rep! Time to conquer those leads 🔥")
elif persona == "Customer":
    st.warning("Welcome! Explore your purchase history and rewards 🛍️")
else:
    st.info("Enjoy the dashboard! Let’s explore what's possible 💡")

# ==== Holiday Celebration ====
now = datetime.now()
if now.month == 12:
    st.snow()
    st.markdown("🎄 Happy Holidays!")
elif now.month == 6:
    st.balloons()
    st.markdown("🎉 Mid-Year Motivation! Let’s push to the next level!")



# ==== Ask-a-Question Bot ====
st.subheader("🤖 Ask the Dashboard a Question")
q = st.text_input("What would you like to know?")
if q:
    if "sales" in q.lower():
        st.info("💰 Sales this month crossed ₹1.8M")
    elif "growth" in q.lower():
        st.info("📈 Growth rate is steady at 8.5%")
    else:
        st.warning("🤔 I'm still learning. Try asking about 'sales' or 'growth'")




# ==== Countdown to Launch ====
st.subheader("⏳ Countdown to Q3 Launch")
launch_date = datetime(2025, 9, 1)
days_left = (launch_date - datetime.now()).days
st.metric("🚀 Days to Launch", f"{days_left} days")



# ==== Animated KPI Counter ====
st.subheader("📈 Quarterly Revenue Count")
target = 18000
placeholder = st.empty()
for i in range(0, target + 1, 800):
    placeholder.metric("Quarterly Revenue", f"${i:,}")
    time.sleep(0.03)




# ==== Branch Progress ====
st.subheader("📊 Progress by Branch")
st.write("**WA Branch**")
st.progress(0.72)
st.write("**NSW Branch**")
st.progress(0.55)
st.write("**QLD Branch**")
st.progress(0.81)

# ==== Flip Cards ====
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
""", unsafe_allow_html=True)




# ==== Email Yourself Button ====
st.subheader("📤 Email This Dashboard Summary")
summary = "Check out the dashboard I just viewed. Great insights and KPIs!"
st.markdown(f"""
<a href="mailto:client@example.com?subject=Dashboard Summary&body={summary}" target="_blank">
    📧 <button style='background-color:#4CAF50;color:white;border:none;padding:0.6em 1.2em;border-radius:10px;cursor:pointer;'>Send Summary Email</button>
</a>
""", unsafe_allow_html=True)



# ==== Feedback Form ====
st.subheader("📝 Quick Feedback")
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email (optional)")
    feedback = st.text_area("Your thoughts?")
    rating = st.slider("Rate us", 1, 10, 7)
    if st.form_submit_button("Submit"):
        st.success(f"Thank you, {name or 'Guest'}! 🙏")

# ==== Save as PDF ====
st.subheader("🖨️ Save or Print This Page")
st.markdown("""
<button onclick="window.print()">🖨️ Print/Save as PDF</button>
""", unsafe_allow_html=True)

# ==== Celebration ====
st.balloons()
# ==== Footer Message ====  

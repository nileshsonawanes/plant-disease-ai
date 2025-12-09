import streamlit as st
from PIL import Image
import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

# ================= LOAD ENV =================


# Load API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

if not api_key:
    st.error("API key missing")
    st.stop()

client = OpenAI(api_key=api_key)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AIR G | Plant Disease Prediction",
    layout="wide"
)

# ================= BACKGROUND IMAGE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #1d6b3a, #0a2f1c);
}
</style>
""", unsafe_allow_html=True)
  # ✅ farming background image

# ================= CSS =================
st.markdown("""
<style>
.navbar {
    background-color: rgba(0, 80, 0, 0.85);
    padding: 15px;
    border-radius: 12px;
}
.navbar h1 {
    color: #ffffff;
    display: inline;
    margin-right: 30px;
}
.navbar a {
    color: #a8ffb0;
    margin-right: 25px;
    font-size: 18px;
    text-decoration: none;
    font-weight: bold;
}
.card {
    background-color: rgba(0,0,0,0.75);
    padding: 30px;
    border-radius: 20px;
    color: white;
}
.footer {
    text-align: center;
    color: white;
    margin-top: 40px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================
st.markdown("""
<div class="navbar">
    <h1>🌱 AIR G</h1>
    <a>HOME</a>
    <a>PLANT DISEASE DETECTION</a>
    <a>LOGOUT</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= MAIN CONTENT =================
st.markdown("""
<div class="card">
<h1>🌿 Plant Disease Prediction</h1>
<h4>शेतीसाठी AI आधारित रोग ओळख प्रणाली</h4>
<p>
या प्रणालीमध्ये तुम्ही पानाचा फोटो घेतल्यावर,
<b>AI आपोआप रोग ओळख करते</b>.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= IMAGE INPUT =================
camera_image = st.camera_input(
    "Plant Image Capture",
    label_visibility="collapsed"
)

# ================= ANALYSIS FUNCTION =================
def analyze_plant(image_path):
    import base64

    with open(image_path, "rb") as img:
        image_bytes = img.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "तुम्ही कृषी तज्ञ AI आहात. खाली दिलेल्या पानाच्या प्रतिमेवरून "
                            "सविस्तर विश्लेषण करा आणि खालील मुद्द्यांमध्ये उत्तर द्या:\n\n"
                            "1️⃣ पानाचे बाह्य स्वरूप (रंग, डाग, कडा)\n"
                            "2️⃣ वनस्पती निरोगी आहे की रोगग्रस्त?\n"
                            "3️⃣ रोगाचे संभाव्य नाव\n"
                            "4️⃣ रोग होण्याची प्रमुख कारणे\n"
                            "5️⃣ या रोगाचा पिकावर होणारा परिणाम\n"
                            "6️⃣ उपचार व औषधे (सोप्या भाषेत)\n"
                            "7️⃣ भविष्यासाठी प्रतिबंधात्मक उपाय\n\n"
                            "उत्तर स्पष्ट, मुद्देसूद आणि सोप्या मराठी भाषेत द्या. "
                            "हा अहवाल शेतकऱ्यांसाठी आहे, त्यामुळे व्यावहारिक सल्ला द्या."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=700
    )

    return response.choices[0].message.content



# ================= AUTO PROCESS =================
if camera_image:
    image = Image.open(camera_image)
    image.save("plant.jpg")

    st.image(image, caption="Captured Plant Leaf", use_column_width=True)

    with st.spinner("🤖 AI पानाचे विश्लेषण करत आहे..."):
        result = analyze_plant("plant.jpg")

    st.success("✅ रोग ओळख पूर्ण झाली")
    st.markdown(f"""
    <div class="card">
    <h3>🧪 Disease Analysis Result</h3>
    <p>{result}</p>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<div class="footer">
© 2025 <b>AIR G Foundation</b> | AI for Agriculture 🌱
</div>
""", unsafe_allow_html=True)




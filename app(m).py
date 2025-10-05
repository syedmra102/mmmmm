import streamlit as st
import json
from googletrans import Translator

# Load medicines.json
with open("medicines.json", "r", encoding="utf-8") as f:
    medicines = json.load(f)

translator = Translator()

st.title("💊 Medicine Recognition & Info App")
st.write("Upload a medicine image OR enter imprint/name to see its uses and benefits.")

# Upload Section (for now: simulate detection by name input)
uploaded_file = st.file_uploader("Upload medicine image (simulated)", type=["jpg", "png", "jpeg"])
imprint = st.text_input("Or type medicine name / imprint code:")

if imprint:
    # Search in database
    results = [m for m in medicines if imprint.lower() in m["display_name"].lower() 
               or any(imprint.lower() in n.lower() for n in m["names"]) 
               or any(imprint.lower() in i.lower() for i in m["imprints"])]
    
    if results:
        med = results[0]
        st.subheader(med["display_name"])
        st.write(f"**Uses:** {med['uses']}")
        st.write(f"**Benefits:** {med['benefits']}")

        # Translator
        lang = st.text_input("Enter language code for translation (e.g., 'ur' for Urdu, 'es' for Spanish):")
        if lang:
            translated_uses = translator.translate(med["uses"], dest=lang).text
            translated_benefits = translator.translate(med["benefits"], dest=lang).text
            st.write(f"**Uses ({lang}):** {translated_uses}")
            st.write(f"**Benefits ({lang}):** {translated_benefits}")
    else:
        st.error("Medicine not found in database.")

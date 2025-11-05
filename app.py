import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Paystub Donation Recommender", layout="centered")

st.title("💰 Paystub Donation Recommender (Demo)")
st.caption("Upload a **dummy paystub PDF** to test donation suggestions. All processing happens in memory — no data is stored.")

uploaded_file = st.file_uploader("📄 Upload your paystub (PDF only)", type=["pdf"])

def extract_values_from_pdf(file):
    """Extract gross and net pay from a PDF using regex."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    gross = re.search(r"Gross\s*Pay.*?\$([\d,]+\.\d{2})", text, re.IGNORECASE)
    net = re.search(r"Net\s*Pay.*?\$([\d,]+\.\d{2})", text, re.IGNORECASE)
    ytd = re.search(r"YTD\s*Gross.*?\$([\d,]+\.\d{2})", text, re.IGNORECASE)

    return {
        "gross_pay": float(gross.group(1).replace(",", "")) if gross else None,
        "net_pay": float(net.group(1).replace(",", "")) if net else None,
        "ytd_gross": float(ytd.group(1).replace(",", "")) if ytd else None,
    }

if uploaded_file:
    st.info("✅ File uploaded successfully. Parsing data...")
    values = extract_values_from_pdf(uploaded_file)

    st.subheader("📊 Extracted Pay Data")
    st.write(values)

    st.subheader("💡 Donation Calculator")
    percentage = st.slider("Select donation percentage", 1, 15, 5)
    pct = percentage / 100.0

    if values["gross_pay"]:
        st.write(f"- {percentage}% of Gross Pay: **${values['gross_pay'] * pct:.2f}**")
    if values["net_pay"]:
        st.write(f"- {percentage}% of Net Pay: **${values['net_pay'] * pct:.2f}**")
    if values["ytd_gross"]:
        st.write(f"- {percentage}% of YTD Gross: **${values['ytd_gross'] * pct:.2f}**")

else:
    st.info("👆 Upload a dummy paystub PDF to begin.")

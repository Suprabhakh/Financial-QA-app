import streamlit as st
import pandas as pd
import PyPDF2

st.set_page_config(page_title="Financial Q&A App", layout="wide")

st.title("📊 Financial Document Q&A Assistant")

uploaded_file = st.file_uploader("Upload a financial document (PDF or Excel)", type=["pdf", "xlsx", "xls"])

data = None

# --- Handle Excel ---
def read_excel(file):
    return pd.read_excel(file)

# --- Handle PDF (text extraction) ---
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["xlsx", "xls"]:
        data = read_excel(uploaded_file)
        st.success("Excel file uploaded successfully ✅")
        st.dataframe(data.head())

    elif file_type == "pdf":
        pdf_text = read_pdf(uploaded_file)
        st.success("PDF file uploaded successfully ✅")
        st.text_area("Extracted PDF Text", pdf_text[:2000], height=300)

# --- Simple Q&A ---
st.subheader("💬 Ask a financial question")

user_query = st.text_input("Type your question here (e.g., 'total revenue', 'profit', 'expenses'):")

if user_query and data is not None:
    query = user_query.lower()

    if "revenue" in query:
        if "Revenue" in data.columns:
            total = data["Revenue"].sum()
            st.write(f"**Total Revenue:** {total}")
        else:
            st.warning("No 'Revenue' column found in the Excel file.")

    elif "expense" in query or "cost" in query:
        if "Expenses" in data.columns:
            total = data["Expenses"].sum()
            st.write(f"**Total Expenses:** {total}")
        else:
            st.warning("No 'Expenses' column found in the Excel file.")

    elif "profit" in query:
        if "Revenue" in data.columns and "Expenses" in data.columns:
            profit = data["Revenue"].sum() - data["Expenses"].sum()
            st.write(f"**Total Profit:** {profit}")
        else:
            st.warning("Need both 'Revenue' and 'Expenses' columns to calculate profit.")

    else:
        st.info("Currently, I can answer about revenue, expenses, and profit.")

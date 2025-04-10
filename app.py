import streamlit as st
from utils.extractor import read_txt_file, extract_text_from_pdf
from utils.preprocessor import preprocess
from utils.scorer import score_resumes

st.set_page_config(page_title="Resume Ranker", layout="wide")
st.title("📄 Resume Ranker")

# Upload files
jd_file = st.file_uploader("📌 Upload Job Description (.txt)", type=["txt"])
resume_files = st.file_uploader("📂 Upload Resumes (.pdf)", type=["pdf"], accept_multiple_files=True)

# Proceed only if both JD and resumes are uploaded
if jd_file and resume_files:
    jd_text = read_txt_file(jd_file)
    jd_clean = preprocess(jd_text)

    resumes = []
    for file in resume_files:
        resume_text = extract_text_from_pdf(file)
        resumes.append({
            "filename": file.name,
            "text": resume_text,
            "clean_text": preprocess(resume_text)
        })

    # Calculate similarity scores
    resume_clean_texts = [res["clean_text"] for res in resumes]
    scores = score_resumes(jd_clean, resume_clean_texts)

    for i, score in enumerate(scores):
        resumes[i]["score"] = round(score * 100, 2)  # Convert to percentage

    # Sort resumes by score (descending)
    resumes_sorted = sorted(resumes, key=lambda r: r["score"], reverse=True)
    best_resume = resumes_sorted[0]  # First one is the best

    # Display ranked list
    st.header("📊 Ranked Resumes (High to Low)")
    for res in resumes_sorted:
        st.markdown(f"**{res['filename']}** — Score: `{res['score']}%`")

    # Display best resume separately
    st.markdown("---")
    st.subheader("🏆 Best Matching Resume")
    st.success(f"**Filename**: {best_resume['filename']}")
    st.write(f"**Score**: {best_resume['score']}%")

    with st.expander("📄 Preview Best Resume Text"):
        st.write(best_resume["text"][:2000] + "..." if len(best_resume["text"]) > 2000 else best_resume["text"])

    import base64

# Add Download Button for Best Resume
def get_pdf_download_link(file):
    file.seek(0)
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{file.name}">📥 Download Best Resume ({file.name})</a>'
    return href

# Find the original uploaded file that matches best resume
for file in resume_files:
    if file.name == best_resume['filename']:
        st.markdown(get_pdf_download_link(file), unsafe_allow_html=True)
        break

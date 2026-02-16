import streamlit as st
import json
from app.email_agent import analyze_email
from app.thread_scaler import compress_thread

st.set_page_config(page_title="AI Email Triage Assistant", layout="wide")

st.title("EMAIL TRIAGE ASSISSTANT")
st.write("Local AI-powered inbox organization prototype (Student MVP)")

with open("data/sample_emails.json", "r") as file:
    emails = json.load(file)

if st.button("Analyze Inbox"):

    results = []
    total_original_chars = 0
    total_compressed_chars = 0
    total_time = 0

    with st.spinner("Analyzing inbox using local LLM..."):

        for email in emails:
            original_text = " ".join(email["thread"])
            compressed_text = compress_thread(email["thread"])

            total_original_chars += len(original_text)
            total_compressed_chars += len(compressed_text)

            analysis = analyze_email(email["subject"], email["thread"])

            total_time += analysis["processing_time_seconds"]

            results.append({
                "subject": email["subject"],
                "analysis": analysis["result"],
                "processing_time": analysis["processing_time_seconds"]
            })

    
    st.subheader("PRODUCTIVITY METRICS")

    if total_original_chars > 0:
        compression_percent = round(
            (1 - total_compressed_chars / total_original_chars) * 100, 2
        )
    else:
        compression_percent = 0

    st.write("Total Emails Processed:", len(results))
    st.write("Average Processing Time (seconds):", round(total_time / len(results), 2))
    st.write("Context Compression:", f"{compression_percent}%")

    
    
    folders = {
        "Urgent": [],
        "Work": [],
        "Personal": [],
        "Spam": []
    }

    for r in results:
        category = r["analysis"].get("category", "Work")

        # If priority high → treat as urgent
        if r["analysis"].get("priority", 1) >= 4:
            folders["Urgent"].append(r)
        elif category in folders:
            folders[category].append(r)
        else:
            folders["Work"].append(r)

    st.subheader("📂 Smart Folders")

    for folder_name, emails_in_folder in folders.items():

        st.markdown(f"### {folder_name}")

        if not emails_in_folder:
            st.write("No emails in this folder.")
            continue

        sorted_emails = sorted(
            emails_in_folder,
            key=lambda x: x["analysis"].get("priority", 1),
            reverse=True
        )

        for item in sorted_emails:
            analysis = item["analysis"]

            st.markdown(f"**Subject:** {item['subject']}")
            st.write("Priority:", analysis.get("priority"))
            st.write("Summary:", analysis.get("summary"))

            if analysis.get("meeting_detected"):
                st.write("MEETING DETECTED")

            if analysis.get("unsubscribe_suggested"):
                st.write("UNSUBSCRIBE SUGGESTED")

            with st.expander("View Draft Reply"):
                st.write(analysis.get("draft_reply"))

            with st.expander("View Full AI Output"):
                st.json(analysis)
                st.write("Processing Time:", item["processing_time"], "seconds")

            st.divider()
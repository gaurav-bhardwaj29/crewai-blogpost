import streamlit as st
from datetime import datetime
import time
import base64

# Import your Blogpost class (update the import path if needed)
from src.blogpost.crew import Blogpost

st.set_page_config(page_title="CrewAI Blogpost Generator", layout="wide")

st.title("📝 CrewAI Blogpost Generator")
st.markdown(
    "Generate high-quality financial blog content using a multi-agent CrewAI system."
)

# Input form for blog topic and year
with st.form("blog_form"):
    topic = st.text_input(
        "Enter Blog Topic",
        "The growth of solar energy production in India and its impact on the economy in 2020-2024"
    )
    year = st.text_input(
        "Current Year", str(datetime.now().year)
    )
    submitted = st.form_submit_button("GENERATE REPORT")

# Show a loader and run the agent workflow when the button is pressed
if submitted:
    with st.spinner("⚙️ Running CrewAI agents to generate your blogpost..."):
        status_placeholder = st.empty()
        try:
            inputs = {
                "topic": topic,
                "current_year": year
            }
            status_placeholder.info("Step 1/3: Initializing agents...")
            time.sleep(1)
            status_placeholder.info("Step 2/3: Agents collaborating on research and content creation...")
            crew = Blogpost()
            result = crew.crew().kickoff(inputs=inputs)
            status_placeholder.info("Step 3/3: Finalizing and reviewing content...")
            time.sleep(1)

            if result and isinstance(result, str) and len(result.strip()) > 0:
                content = result
            else:
                with open("report.md", "r", encoding="utf-8") as f:
                    content = f.read()
            status_placeholder.success("✅ Blogpost generated successfully!")

            st.markdown("### 📄 Generated Blogpost Report")
            st.markdown(content)

            b64 = base64.b64encode(content.encode()).decode()
            href = f'<a href="data:text/markdown;base64,{b64}" download="report.md">⬇️ Download Report as Markdown</a>'
            st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            status_placeholder.error(f"❌ An error occurred: {e}")
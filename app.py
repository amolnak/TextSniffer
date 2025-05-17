import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Simple Web Crawler", layout="wide")
st.title("🌐 Simple Web Crawler")
st.markdown("Enter a URL to extract **page title**, **H1 headings**, **links**, and **main text**.")

url = st.text_input("🔗 Enter URL", "https://www.nbcnews.com/business")

def simple_crawl(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract elements
        title = soup.title.string.strip() if soup.title else "No title found"
        h1_tags = [h.text.strip() for h in soup.find_all("h1") if h.text.strip()]
        links = [(a.text.strip() or a["href"], a["href"]) for a in soup.find_all("a", href=True)]

        # Clean text
        raw_text = soup.get_text(separator=' ', strip=True)

        return {
            "title": title,
            "headings": h1_tags,
            "links": links,
            "raw_text": raw_text
        }
    except Exception as e:
        return {"error": str(e)}

if st.button("🚀 Crawl Now"):
    if url.strip():
        with st.spinner("Crawling the website..."):
            result = simple_crawl(url.strip())

            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                st.success("✅ Crawl completed successfully!")

                st.subheader("📌 Page Title:")
                st.write(result["title"])

                st.subheader(f"📖 H1 Headings ({len(result['headings'])} found):")
                if result["headings"]:
                    for h in result["headings"]:
                        st.markdown(f"- {h}")
                else:
                    st.info("No H1 headings found.")

                st.subheader(f"🔗 Links (showing first 10 of {len(result['links'])}):")
                if result["links"]:
                    for text, link in result["links"][:10]:
                        st.markdown(f"- [{text}]({link})")
                else:
                    st.info("No links found.")

                st.subheader("📝 Full Page Text (first 1000 characters):")
                st.text(result["raw_text"])
                # st.text(result["raw_text"][:1000] + "..." if len(result["raw_text"]) > 1000 else result["raw_text"])
    else:
        st.warning("Please enter a valid URL.")

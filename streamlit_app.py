import streamlit as st
from frontend_generator import get_component_code
import html

def create_component_preview(raw_code: str) -> str:
    clean_code = raw_code.strip()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f0f4f8;
            }}
            .preview-container {{
                width: 100%;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                box-sizing: border-box;
            }}
            .component-wrapper {{
                width: 100%;
                max-width: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
        </style>
    </head>
    <body>
        <div class="preview-container">
            <div class="component-wrapper">
                {clean_code}
            </div>
        </div>
    </body>
    </html>
    """

st.set_page_config(page_title="UI Generator", layout="centered")

st.markdown("## Generate UI Components with AI")

prompt = st.text_input("Describe your component", value="A red button with Hello text")

if st.button("⚡ Generate"):
    try:
        code = get_component_code(prompt)
        st.subheader("Generated Code")
        st.code(code, language="html")

        preview_html = create_component_preview(code)
        iframe_html = f'<iframe srcdoc="{html.escape(preview_html)}" width="100%" height="300" style="border:none;"></iframe>'
        
        st.subheader("Live Preview")
        st.components.v1.html(iframe_html, height=320)

    except Exception as e:
        st.error(f"Error generating component: {str(e)}")

"""
Universal Elevator/Lift Inspection Report Analyzer - Streamlit Version
Analyzes ANY elevator inspection report and classifies defects intelligently
"""

import streamlit as st
import fitz  # PyMuPDF
import base64
import io
from PIL import Image
from openai import OpenAI
from typing import List, Dict
import pandas as pd
from datetime import datetime
import json
import re
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Elevator Inspection Analyzer",
    page_icon="🏗️",
    layout="wide"
)

class InspectionAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Convert PDF pages to images using PyMuPDF"""
        try:
            images = []
            pdf_document = fitz.open(pdf_path)

            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                # Render page to image at 300 DPI (zoom factor 4.0 ≈ 300 DPI)
                mat = fitz.Matrix(4.0, 4.0)
                pix = page.get_pixmap(matrix=mat)

                # Convert to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)

            pdf_document.close()
            return images
        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")

    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    def extract_defects_from_image(self, image: Image.Image, progress_callback=None) -> List[Dict]:
        """Use GPT-4 Vision to intelligently extract defects from any inspection report"""
        try:
            if progress_callback:
                progress_callback("🔍 Analyzing page with AI Vision...")

            base64_image = self.image_to_base64(image)

            prompt = """
            You are analyzing an elevator/lift inspection report. This could be from ANY inspection company
            (TÜV, DEKRA, or others) and in any language.

            Your task is to intelligently identify and extract ALL defects/issues/findings listed in this document.

            Look for sections that typically contain defect lists, such as:
            - "Mängelliste" (German for defect list)
            - "Defects", "Issues", "Findings"
            - Tables or lists with problems/issues
            - Any numbered or bulleted items describing problems

            For EACH defect you find, extract:
            1. A reference number (if present - could be sequential, a code, or identifier)
            2. The complete description of the defect
            3. Any severity/rating (if present - like "minor", "major", "geringfügig", "erheblich", etc.)
            4. Any defect code or category number (if present)

            Return results as a JSON array. Use null for missing fields:
            [
                {
                    "number": "1" or "A1" or any identifier found,
                    "code": "704" or similar code if present, else null,
                    "description": "Full defect description in original language",
                    "severity": "minor" or "major" or original severity term, else null
                },
                ...
            ]

            IMPORTANT RULES:
            - Be flexible - defects can be in tables, lists, or paragraphs
            - Extract ALL defects found on this page
            - Keep original language - don't translate
            - If no defects found on this page, return empty array: []
            - Return ONLY valid JSON, no additional text or markdown

            Examples of what defects look like:
            - "Der Antrieb verliert Öl" (The drive is leaking oil)
            - "Missing emergency certificate"
            - "Circuit diagram not available at facility"
            - "Brake pads worn"
            """

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2500
            )

            content = response.choices[0].message.content.strip()
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*$', '', content)
            content = content.strip()

            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                defects = json.loads(json_match.group())
                return defects if isinstance(defects, list) else []
            else:
                return []

        except Exception as e:
            st.error(f"Error extracting defects: {str(e)}")
            return []

    def classify_defect(self, defect_description: str, defect_code: str = None, progress_callback=None) -> Dict:
        """Use GPT-4 to intelligently classify defect"""
        try:
            if progress_callback:
                progress_callback("🤖 Classifying with AI...")

            context = f"Defect Description: {defect_description}"
            if defect_code:
                context += f"\nDefect Code: {defect_code}"

            prompt = f"""
            You are analyzing a defect from an elevator/lift inspection report.

            {context}

            Classify this defect as either:
            - "Bauseitiger Mangel" (site-related defect - related to the building/structure)
            - "Nicht-Bauseitiger Mangel" (non-site-related defect - related to the lift equipment itself or documentation)

            Use your understanding of what constitutes a site defect versus a lift equipment defect.

            Also provide an English translation of the defect description.

            Return JSON:
            {{
                "classification": "Bauseitiger Mangel" or "Nicht-Bauseitiger Mangel",
                "confidence": "High" or "Medium" or "Low",
                "reasoning": "Brief explanation of why you classified it this way",
                "english_translation": "English translation of the defect description"
            }}

            Return ONLY valid JSON.
            """

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in elevator safety inspections. Classify defects intelligently based on their nature."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*$', '', content)
            content = content.strip()

            result = json.loads(content)

            if 'classification' not in result:
                result['classification'] = 'Unklassifiziert'
            if 'confidence' not in result:
                result['confidence'] = 'Low'
            if 'reasoning' not in result:
                result['reasoning'] = 'Unable to determine'

            return result

        except Exception as e:
            return {
                'classification': 'Klassifizierungsfehler',
                'confidence': 'Low',
                'reasoning': f'Error: {str(e)}'
            }

    def process_pdf(self, pdf_path: str, filename: str, progress_bar=None, status_text=None) -> List[Dict]:
        """Process a single PDF file"""
        all_defects = []

        try:
            # Convert PDF to images
            if status_text:
                status_text.text(f"📄 Converting {filename} to images...")
            images = self.pdf_to_images(pdf_path)

            total_pages = len(images)
            for page_num, image in enumerate(images, 1):
                if progress_bar:
                    progress_bar.progress(page_num / total_pages)

                if status_text:
                    status_text.text(f"🔍 Analyzing page {page_num}/{total_pages} of {filename}...")

                # Extract defects
                defects = self.extract_defects_from_image(image,
                    lambda msg: status_text.text(msg) if status_text else None)

                if not defects:
                    continue

                # Classify each defect
                for defect in defects:
                    if status_text:
                        status_text.text(f"🤖 Classifying defect {defect.get('number', '?')} from {filename}...")

                    classification_result = self.classify_defect(
                        defect.get('description', ''),
                        defect.get('code'),
                        lambda msg: status_text.text(msg) if status_text else None
                    )

                    all_defects.append({
                        'file': filename,
                        'page': page_num,
                        'number': defect.get('number', ''),
                        'code': defect.get('code', ''),
                        'description': defect.get('description', ''),
                        'english_translation': classification_result.get('english_translation', ''),
                        'severity': defect.get('severity', ''),
                        'classification': classification_result.get('classification', 'Unklassifiziert'),
                        'confidence': classification_result.get('confidence', 'Low'),
                        'reasoning': classification_result.get('reasoning', '')
                    })

            return all_defects

        except Exception as e:
            st.error(f"Error processing {filename}: {str(e)}")
            return []


def main():
    # Header
    st.title("🏗️ Universal Elevator Inspection Analyzer")
    st.markdown("### AI-Powered Defect Classification: Bauseitige vs. Nicht-Bauseitige Mängel")

    st.divider()

    # Get API key from Streamlit secrets (for deployment) or use input field (for local testing)
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key (get one from https://platform.openai.com/api-keys)"
        )
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key above")
            st.stop()

    # File upload
    uploaded_files = st.file_uploader(
        "📁 Upload Inspection Report PDFs",
        type=['pdf'],
        accept_multiple_files=True,
        help="Select one or more PDF inspection reports from any company"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

        # Show uploaded files
        with st.expander("📋 Uploaded Files"):
            for file in uploaded_files:
                st.write(f"- {file.name}")

        # Analyze button
        if st.button("🤖 Analyze Reports", type="primary"):
            analyzer = InspectionAnalyzer(api_key)

            all_results = []

            # Progress tracking
            overall_progress = st.progress(0)
            status_text = st.empty()

            # Process each file
            for idx, uploaded_file in enumerate(uploaded_files):
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                try:
                    status_text.text(f"Processing file {idx+1}/{len(uploaded_files)}: {uploaded_file.name}")

                    # Create progress bar for this file
                    file_progress = st.progress(0)
                    file_status = st.empty()

                    # Process PDF
                    results = analyzer.process_pdf(
                        tmp_path,
                        uploaded_file.name,
                        file_progress,
                        file_status
                    )

                    all_results.extend(results)

                    # Update overall progress
                    overall_progress.progress((idx + 1) / len(uploaded_files))

                finally:
                    # Clean up temp file
                    os.unlink(tmp_path)

            status_text.text("✅ Analysis complete!")

            # Store results in session state
            st.session_state['results'] = all_results

    # Display results if available
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']

        st.divider()
        st.header("📊 Analysis Results")

        # Summary statistics
        total_defects = len(results)
        bauseitig_count = sum(1 for r in results if 'Bauseitiger' in r['classification'])
        nicht_bauseitig_count = sum(1 for r in results if 'Nicht-Bauseitiger' in r['classification'])
        high_conf_count = sum(1 for r in results if r['confidence'] == 'High')

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Defects", total_defects)
        with col2:
            st.metric("🔧 Bauseitige", bauseitig_count,
                     f"{bauseitig_count/total_defects*100:.1f}%")
        with col3:
            st.metric("📄 Nicht-Bauseitige", nicht_bauseitig_count,
                     f"{nicht_bauseitig_count/total_defects*100:.1f}%")
        with col4:
            st.metric("High Confidence", high_conf_count,
                     f"{high_conf_count/total_defects*100:.1f}%")

        st.divider()

        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_class = st.multiselect(
                "Filter by Classification",
                ['Bauseitiger Mangel', 'Nicht-Bauseitiger Mangel'],
                default=['Bauseitiger Mangel', 'Nicht-Bauseitiger Mangel']
            )
        with col2:
            filter_conf = st.multiselect(
                "Filter by Confidence",
                ['High', 'Medium', 'Low'],
                default=['High', 'Medium', 'Low']
            )

        # Filter results
        filtered_results = [
            r for r in results
            if r['classification'] in filter_class and r['confidence'] in filter_conf
        ]

        # Display results table grouped by file
        df = pd.DataFrame(filtered_results)

        # Group by file
        unique_files = df['file'].unique()

        for file_name in unique_files:
            file_df = df[df['file'] == file_name].copy()

            # Show file name as header
            st.subheader(f"📄 {file_name}")

            # Reorder columns - remove file column since it's in the header
            column_order = ['page', 'number', 'code', 'description', 'english_translation',
                           'severity', 'classification', 'confidence', 'reasoning']
            file_df = file_df[column_order]

            # Color code the dataframe with darker, more visible colors
            def color_classification(val):
                if 'Bauseitiger' in val:
                    return 'background-color: #ffcccc; color: #000000'  # Dark red background
                elif 'Nicht-Bauseitiger' in val:
                    return 'background-color: #cce5ff; color: #000000'  # Dark blue background
                return ''

            styled_df = file_df.style.applymap(color_classification, subset=['classification'])
            st.dataframe(styled_df, use_container_width=True, height=300)

            st.markdown("---")  # Separator between files

        # Detailed view with reasoning
        st.divider()
        st.subheader("🔍 Detailed Defect View")

        selected_idx = st.selectbox(
            "Select a defect to view details:",
            range(len(filtered_results)),
            format_func=lambda i: f"#{i+1}: {filtered_results[i]['description'][:50]}..."
        )

        if selected_idx is not None:
            defect = filtered_results[selected_idx]

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**File:** {defect['file']}")
                st.markdown(f"**Number:** {defect['number']}")
                st.markdown(f"**Code:** {defect['code']}")
                st.markdown(f"**Severity:** {defect['severity']}")

            with col2:
                st.markdown(f"**Classification:** {defect['classification']}")
                st.markdown(f"**Confidence:** {defect['confidence']}")
                st.markdown(f"**Page:** {defect['page']}")

            st.markdown("**Description:**")
            st.info(defect['description'])

            st.markdown("**AI Reasoning:**")
            st.success(defect['reasoning'])

        # Export to Excel
        st.divider()
        st.subheader("💾 Export Results")

        # Prepare dataframe for export with all columns in proper order
        export_df = df.copy()
        column_order = ['file', 'page', 'number', 'code', 'description', 'english_translation',
                       'severity', 'classification', 'confidence', 'reasoning']
        export_df = export_df[column_order]

        # Excel export
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='All Defects', index=False)

            # Separate sheets
            export_df[export_df['classification'].str.contains('Bauseitiger', na=False)].to_excel(
                writer, sheet_name='Bauseitige Mängel', index=False
            )
            export_df[export_df['classification'].str.contains('Nicht-Bauseitiger', na=False)].to_excel(
                writer, sheet_name='Nicht-Bauseitige Mängel', index=False
            )

        excel_buffer.seek(0)
        st.download_button(
            label="📥 Download Excel Report",
            data=excel_buffer,
            file_name=f"inspection_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


if __name__ == "__main__":
    main()

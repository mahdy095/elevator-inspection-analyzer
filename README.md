# Universal Elevator Inspection Report Analyzer

AI-Powered desktop application that automatically analyzes elevator/lift inspection reports from **ANY inspection company** (TÜV, DEKRA, or others) and intelligently classifies defects as:

- 🔧 **Bauseitige Mängel** (Site-Related/Physical defects)
- 📄 **Nicht-Bauseitige Mängel** (Non-Site-Related/Administrative defects)

## Key Features

✅ **Company-Agnostic**: Works with inspection reports from any company
✅ **AI-Powered**: Uses GPT-4 Vision to intelligently read and understand reports
✅ **Smart Classification**: AI determines defect types based on nature, not keywords
✅ **Batch Processing**: Analyze multiple PDF reports at once
✅ **Confidence Scoring**: See how confident the AI is about each classification
✅ **Reasoning Display**: Double-click any defect to see why AI classified it that way
✅ **Export Options**: Export results to CSV or Excel with separate sheets
✅ **Visual Results**: Color-coded tree view for easy analysis

## How It Works

1. **PDF → Images**: Converts each PDF page to high-quality images
2. **AI Extraction**: GPT-4 Vision intelligently identifies and extracts all defects from images
3. **Smart Classification**: GPT-4 analyzes each defect's description and classifies it based on its nature:
   - Physical/mechanical issues → Bauseitig
   - Documentation/administrative issues → Nicht-Bauseitig
4. **Results Display**: Shows all defects with classifications, confidence scores, and AI reasoning

## Installation

### Prerequisites

- **Python 3.8+**
- **Windows** (tested on Windows, should work on macOS/Linux with minor adjustments)
- **poppler** (for PDF to image conversion)

### Windows Setup

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Poppler** (required for PDF conversion):
   ```bash
   # Using Chocolatey (recommended)
   choco install poppler

   # Or download manually from: https://github.com/oschwartz10612/poppler-windows/releases/
   # Extract and add the 'bin' folder to your system PATH
   ```

3. **Clone or download this repository**

4. **Install Python dependencies**:
   ```bash
   cd /path/to/project
   pip install -r requirements.txt
   ```

5. **Configure your OpenAI API key** (IMPORTANT):
   - Open `elevator_inspection_analyzer.py`
   - Replace the API key on line 26 with your own OpenAI API key:
     ```python
     self.api_key = "your-actual-api-key-here"
     ```
   - Get your API key from: https://platform.openai.com/api-keys

### Linux/macOS Setup

1. **Install poppler**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install poppler-utils

   # macOS
   brew install poppler
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key** (same as Windows step 5)

## Usage

### Running the Application

```bash
python elevator_inspection_analyzer.py
```

### Step-by-Step Guide

1. **Launch the application**
   - Run the Python script above
   - The GUI window will open

2. **Add PDF files**
   - Click "📁 Add PDF Files"
   - Select one or more inspection report PDFs
   - Files from ANY inspection company will work

3. **Analyze reports**
   - Click "🤖 Analyze Reports"
   - Wait while the AI processes each file
   - Progress is shown in real-time

4. **Review results**
   - Results are displayed in a color-coded tree:
     - 🔧 Red background = Bauseitige Mängel (Physical)
     - 📄 Blue background = Nicht-Bauseitige Mängel (Administrative)
   - Each defect shows:
     - Number, Code, Description
     - Severity (if available)
     - Classification
     - Confidence level (High/Medium/Low)

5. **View AI reasoning**
   - Double-click any defect to see why the AI classified it that way
   - Understand the decision-making process

6. **Export results**
   - Click "💾 Export to CSV" for simple export
   - Click "📊 Export to Excel" for organized export with separate sheets:
     - All Defects
     - Bauseitige Mängel only
     - Nicht-Bauseitige Mängel only

## Classification Logic

The AI uses intelligent reasoning, not rigid rules:

### Bauseitige Mängel (Site-Related)
**Physical defects you can see, touch, or repair on-site:**
- Wear, damage, corrosion, rust
- Oil leaks, fluid leaks
- Loose bolts, broken parts
- Worn cables, brake pads, belts
- Dirty/contaminated components
- Malfunctioning sensors, switches, buttons
- Door problems, alignment issues
- Motor/gearbox problems

**Examples:**
- ✓ "Drive leaking oil"
- ✓ "Brake pads worn"
- ✓ "Outlet in shaft pit not working"
- ✓ "Catch dirty and must be cleaned"

### Nicht-Bauseitige Mängel (Non-Site-Related)
**Paperwork and administrative issues:**
- Missing certificates, permits, licenses
- Missing inspection reports
- Missing technical documentation
- Circuit diagrams not available
- Required inspections not performed
- Test protocols missing

**Examples:**
- ✓ "No modification inspection performed"
- ✓ "Circuit diagram not available"
- ✓ "Manufacturer certificate missing"
- ✓ "Safety assessment not conducted"

## API Costs

This application uses OpenAI's GPT-4 Vision API:
- **Cost per page**: Approximately $0.03-0.10 depending on image size
- **Typical inspection report** (5-10 pages): $0.15-1.00
- Monitor your usage at: https://platform.openai.com/usage

## Troubleshooting

### "PDF conversion failed"
- Make sure poppler is installed correctly
- Windows: Check that poppler's `bin` folder is in your PATH
- Linux/macOS: Install using package manager

### "OpenAI API Error"
- Check that your API key is valid
- Ensure you have sufficient API credits
- Check your internet connection

### "No defects found"
- The AI might not have detected defects on that page
- Try adjusting PDF quality (300 DPI is standard)
- Some pages might be cover pages or don't contain defect lists

### GUI doesn't appear
- Make sure tkinter is installed with Python
- On Linux, you may need: `sudo apt-get install python3-tk`

## Limitations

- Requires active internet connection for AI processing
- Processing time depends on number of pages and defects
- AI accuracy depends on PDF quality and clarity
- Best results with typed text; handwritten reports may be less accurate

## Privacy & Security

- PDFs are converted to images locally
- Only images are sent to OpenAI API for processing
- No data is stored by the application
- OpenAI API privacy policy: https://openai.com/policies/privacy-policy

## Support

For issues, questions, or suggestions:
- Check the troubleshooting section above
- Review OpenAI API documentation: https://platform.openai.com/docs
- Ensure your API key has GPT-4 Vision access

## License

This application is provided as-is for internal use.

## Version History

- **v1.0** (2025-01-20): Initial release
  - Company-agnostic AI-powered analysis
  - GPT-4 Vision integration
  - Smart classification with confidence scoring
  - Batch processing and export features

# Diversicare Reports & NeedGod Script Platform

A unified Streamlit platform combining Diversicare contract analysis and NeedGod script flow functionality.

## Features

### 📊 Diversicare Contracts Analysis
- **Data Processing**: Import and process Excel and CSV contract files
- **Contract Analysis**: Analyze contract data by dealer, date, and financial metrics
- **HTML Report Generation**: Generate comprehensive HTML reports
- **Visual Analytics**: Charts and trends for contract data
- **Dealer Summaries**: Top dealers by contract count and volume

### 📖 NeedGod Script Flow
- **Script Flow Navigation**: Automatically determines next questions based on answers
- **Quick Answer Buttons**: Common responses (Yes, No, Maybe) for faster interaction
- **Custom Answers**: Type your own responses when needed
- **Conversation History**: Track all questions and answers
- **Progress Tracking**: Visual progress through the script
- **Reset Functionality**: Start over at any time

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jeff99jackson99/scriptanalyzer.git
   cd scriptanalyzer
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Data Files**:
   - Place your Diversicare contract files in the project directory:
     - `AllPending-09292025.xlsx`
     - `Diversicare_Contracts_Sorted_by_Dealer_Name.csv`
     - `Diversicare_Contracts_Sorted_by_Dealer_Name_then_Effective_Date.csv`
   - For NeedGod script: Place your `needgodscript.pdf` file in the project directory

4. **Extract PDF Content** (for NeedGod script):
   ```bash
   python extract_pdf.py
   ```

5. **Run the Main App**:
   ```bash
   streamlit run main_app.py
   ```

6. **Open Browser**: Navigate to the URL provided in the terminal (usually `http://localhost:8501`)

## Individual Apps

You can also run individual applications:

- **Diversicare Contracts Only**: `streamlit run diversicare_app.py`
- **NeedGod Script Only**: `streamlit run needgod_enhanced_app.py`

## Usage

### Diversicare Contracts Analysis
1. **Upload Data**: Ensure your contract files are in the project directory
2. **View Summary**: Check total contracts, dealers, and financial metrics
3. **Analyze Data**: Explore dealer summaries and monthly trends
4. **Generate Reports**: Create comprehensive HTML reports
5. **Export Data**: Download processed data and reports

### NeedGod Script Flow
1. **Start the Conversation**: The app will show the first question from your script
2. **Answer Questions**: Use quick answer buttons or type custom responses
3. **Follow the Flow**: The app automatically determines the next question based on your answers
4. **Track Progress**: Monitor your progress in the sidebar
5. **View History**: See all previous questions and answers
6. **Reset**: Start over anytime using the reset button

## File Structure

```
scriptanalyzer/
├── main_app.py                # Main unified application
├── diversicare_app.py         # Diversicare contracts analysis
├── needgod_enhanced_app.py    # Enhanced NeedGod script flow
├── needgod_app.py             # Original NeedGod script flow
├── extract_pdf.py             # PDF extraction script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── AllPending-09292025.xlsx   # Diversicare pending contracts data
├── Diversicare_Contracts_Sorted_by_Dealer_Name.csv
├── Diversicare_Contracts_Sorted_by_Dealer_Name_then_Effective_Date.csv
├── needgodscript.pdf          # Your script PDF (add this)
└── script_content.txt         # Extracted text (generated)
```

## Customization

The app is designed to work with any script that follows a numbered question format. To customize for your specific script:

1. **Modify Flow Logic**: Update the `get_next_question()` method in `needgod_app.py` to match your script's decision tree
2. **Add Quick Answers**: Customize the quick answer buttons based on common responses in your script
3. **Enhance Parsing**: Improve the `parse_script()` method to better extract questions and flow logic from your specific script format

## Requirements

- Python 3.7+
- Streamlit
- PyPDF2
- pandas

## Troubleshooting

- **PDF not found**: Ensure `needgodscript.pdf` is in the project directory
- **Import errors**: Run `pip install -r requirements.txt`
- **Script not loading**: Check that `script_content.txt` was created successfully
- **Flow not working**: Verify the script parsing logic matches your PDF format

## GitHub Repository

This project is hosted at: https://github.com/jeff99jackson99/scriptanalyzer

## License

This project is for personal use with the NeedGod script.

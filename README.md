# NeedGod Script Flow App

A Streamlit application that follows a script flow based on user answers, automatically determining the next question to ask.

## Features

- 📖 **Script Flow Navigation**: Automatically determines next questions based on answers
- ⚡ **Quick Answer Buttons**: Common responses (Yes, No, Maybe) for faster interaction
- 📝 **Custom Answers**: Type your own responses when needed
- 📚 **Conversation History**: Track all questions and answers
- 📊 **Progress Tracking**: Visual progress through the script
- 🔄 **Reset Functionality**: Start over at any time

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

3. **Add Your Script PDF**:
   - Place your `needgodscript.pdf` file in the project directory

4. **Extract PDF Content**:
   ```bash
   python extract_pdf.py
   ```

5. **Run the App**:
   ```bash
   streamlit run needgod_app.py
   ```

6. **Open Browser**: Navigate to the URL provided in the terminal (usually `http://localhost:8501`)

## Usage

1. **Start the Conversation**: The app will show the first question from your script
2. **Answer Questions**: Use quick answer buttons or type custom responses
3. **Follow the Flow**: The app automatically determines the next question based on your answers
4. **Track Progress**: Monitor your progress in the sidebar
5. **View History**: See all previous questions and answers
6. **Reset**: Start over anytime using the reset button

## File Structure

```
scriptanalyzer/
├── needgodscript.pdf          # Your script PDF (add this)
├── script_content.txt         # Extracted text (generated)
├── needgod_app.py             # Main Streamlit application
├── extract_pdf.py             # PDF extraction script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
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

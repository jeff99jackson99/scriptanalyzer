.PHONY: setup install run dev clean help

# Default target
help:
	@echo "NeedGod Script Flow App - Available Commands:"
	@echo "  setup    - Extract PDF and install dependencies"
	@echo "  install  - Install Python dependencies"
	@echo "  run      - Run the Streamlit app"
	@echo "  dev      - Run in development mode with auto-reload"
	@echo "  clean    - Clean generated files"
	@echo "  help     - Show this help message"

# Setup project (extract PDF and install deps)
setup:
	@echo "🚀 Setting up NeedGod Script Flow App..."
	python extract_pdf.py
	pip install -r requirements.txt

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run the Streamlit app
run:
	@echo "🌐 Starting Streamlit app..."
	streamlit run needgod_app.py

# Run in development mode
dev:
	@echo "🔧 Starting development server..."
	streamlit run needgod_app.py --server.runOnSave true

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -f script_content.txt
	rm -rf __pycache__/
	rm -rf .streamlit/

# Check if PDF exists
check-pdf:
	@if [ ! -f "needgodscript.pdf" ]; then \
		echo "❌ needgodscript.pdf not found!"; \
		echo "Please ensure the PDF file is in the project directory."; \
		exit 1; \
	fi
	@echo "✅ PDF file found"

# Full setup with checks
setup-full: check-pdf setup
	@echo "✅ Full setup complete!"

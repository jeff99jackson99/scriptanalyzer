#!/usr/bin/env python3
"""
PDF Content Extractor for NeedGod Script
Extracts text from PDF and saves it for analysis
"""

import os
import sys
import subprocess

def install_pypdf2():
    """Install PyPDF2 if not available"""
    try:
        import PyPDF2
        return True
    except ImportError:
        print("Installing PyPDF2...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
            import PyPDF2
            return True
        except Exception as e:
            print(f"Error installing PyPDF2: {e}")
            return False

def extract_pdf_content():
    """Extract text content from the PDF"""
    if not install_pypdf2():
        return False
    
    import PyPDF2
    
    pdf_path = "needgodscript.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found!")
        return False
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"Found {len(reader.pages)} pages in PDF")
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += f"\n--- PAGE {i+1} ---\n{page_text}\n"
                print(f"Extracted page {i+1}")
            
            # Save to text file
            with open("script_content.txt", "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"✅ Successfully extracted {len(text)} characters")
            print("📄 Saved to: script_content.txt")
            
            # Show preview
            print("\n" + "="*50)
            print("PREVIEW (first 1000 characters):")
            print("="*50)
            print(text[:1000])
            
            return True
            
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return False

if __name__ == "__main__":
    print("🚀 NeedGod Script PDF Extractor")
    print("=" * 40)
    
    if extract_pdf_content():
        print("\n✅ PDF extraction completed successfully!")
        print("📄 Content saved to script_content.txt")
    else:
        print("\n❌ PDF extraction failed!")

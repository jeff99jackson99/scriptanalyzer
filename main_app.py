#!/usr/bin/env python3
"""
Main Application - Diversicare Reports & NeedGod Script
A unified Streamlit app for both Diversicare contract analysis and NeedGod script flow
"""

import streamlit as st
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Diversicare Reports & NeedGod Script",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏢 Diversicare Reports & NeedGod Script")
    st.markdown("*Unified platform for contract analysis and script flow*")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        
        # App selection
        app_choice = st.radio(
            "Choose Application:",
            ["📊 Diversicare Contracts", "📖 NeedGod Script Flow"],
            index=0
        )
        
        st.divider()
        
        # Quick info
        st.header("ℹ️ Quick Info")
        st.info("""
        **Diversicare Contracts**: Process and analyze contract data from Excel and CSV files
        
        **NeedGod Script Flow**: Interactive script flow for evangelism conversations
        """)
        
        # File status
        st.header("📁 File Status")
        
        # Check for data files
        data_files = [
            "AllPending-09292025.xlsx",
            "Diversicare_Contracts_Sorted_by_Dealer_Name.csv",
            "Diversicare_Contracts_Sorted_by_Dealer_Name_then_Effective_Date.csv"
        ]
        
        for file in data_files:
            if os.path.exists(file):
                st.success(f"✅ {file}")
            else:
                st.error(f"❌ {file}")
        
        # Check for script files
        script_files = [
            "script_content.txt",
            "needgodscript.pdf"
        ]
        
        for file in script_files:
            if os.path.exists(file):
                st.success(f"✅ {file}")
            else:
                st.warning(f"⚠️ {file}")
    
    # Main content area
    if app_choice == "📊 Diversicare Contracts":
        st.header("📊 Diversicare Contracts Analysis")
        
        # Import and run the Diversicare app
        try:
            from diversicare_app import DiversicareDataProcessor, main as diversicare_main
            diversicare_main()
        except ImportError as e:
            st.error(f"Error importing Diversicare app: {e}")
            st.info("Please ensure all required dependencies are installed.")
        except Exception as e:
            st.error(f"Error running Diversicare app: {e}")
    
    elif app_choice == "📖 NeedGod Script Flow":
        st.header("📖 NeedGod Script Flow")
        
        # Import and run the NeedGod app
        try:
            from needgod_enhanced_app import NeedGodScriptFlow, main as needgod_main
            needgod_main()
        except ImportError as e:
            st.error(f"Error importing NeedGod app: {e}")
            st.info("Please ensure all required dependencies are installed.")
        except Exception as e:
            st.error(f"Error running NeedGod app: {e}")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 20px;'>
        <p>Diversicare Reports & NeedGod Script Platform | Generated on {}</p>
    </div>
    """.format(datetime.now().strftime('%B %d, %Y at %I:%M %p')), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

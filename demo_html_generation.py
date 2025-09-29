#!/usr/bin/env python3
"""
Demo script to generate HTML report for Diversicare contracts
"""

from diversicare_app import DiversicareDataProcessor
import os
from datetime import datetime

def main():
    print("🏢 Diversicare Contracts HTML Report Generator")
    print("=" * 50)
    
    # Initialize processor
    print("📊 Loading and processing data...")
    processor = DiversicareDataProcessor()
    
    if processor.processed_data is None:
        print("❌ No data available. Please ensure data files are present.")
        return
    
    print(f"✅ Loaded {len(processor.processed_data)} contracts from {processor.processed_data['Dealer Name'].nunique()} dealers")
    
    # Get summary stats
    stats = processor.get_summary_stats()
    print(f"💰 Total loan amount: ${stats['total_loan_amount']:,.2f}")
    print(f"📈 Average loan amount: ${stats['average_loan_amount']:,.2f}")
    
    # Generate HTML report
    print("\n📄 Generating HTML report...")
    html_content = processor.generate_html_report()
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diversicare_report_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML report generated: {filename}")
    print(f"📁 File size: {os.path.getsize(filename)} bytes")
    print(f"🌐 Open the file in your browser to view the report")
    
    # Show sample of dealer summary
    print("\n📋 Top 5 Dealers by Contract Count:")
    dealer_summary = processor.get_dealer_summary()
    for i, (dealer, row) in enumerate(dealer_summary.head(5).iterrows(), 1):
        print(f"{i}. {dealer}: {row['Contract Count']} contracts, ${row['Total Loan Amount']:,.2f} total")

if __name__ == "__main__":
    main()

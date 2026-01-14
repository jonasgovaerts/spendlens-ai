#!/usr/bin/env python3
"""
SpendLens AI Transaction Categorizer
Processes unprocessed_records from PostgreSQL database and categorizes them
using keyword matching or AI via LM Studio.
"""

import os
import time
from src.database import DatabaseConnection
from src.category_matcher import CategoryMatcher
from src.ai_processor import AIProcessor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def process_records():
    """Main function to process all unprocessed records"""
    print("Starting transaction categorization process...")
    
    # Initialize components
    db = DatabaseConnection()
    matcher = CategoryMatcher()
    ai_processor = AIProcessor()
    
    # Create processed_records table if it doesn't exist
    print("Ensuring processed_records table exists...")
    db.create_processed_records_table()
    
    # Fetch all unprocessed records
    records = db.get_unprocessed_records()
    
    if not records:
        print("No unprocessed records found.")
        return
    
    print(f"Found {len(records)} unprocessed records to categorize.")
    
    # Process each record
    processed_count = 0
    successful_inserts = 0
    
    for record in records:
        try:
            record_id = record['record_id_bank']
            description = record['description'] or ""
            account = record['account'] or ""
            
            print(f"\nProcessing record {record_id}...")
            print(f"Description: {description}")
            print(f"Account: {account}")
            
            # Try keyword-based matching first
            category = matcher.get_category_from_keywords(description, account)
            
            # If no keyword match, use AI
            if not category:
                print("No keyword match found. Using AI for categorization...")
                category = ai_processor.get_category_from_ai(description, account)
            
            # If still no category, set to "Other"
            if not category:
                category = "Other"
                print("No category found, defaulting to 'Other'")
            
            # Insert the processed record into the new table
            success = db.insert_processed_record(record, category)
            if success:
                print(f"✓ Inserted record {record_id} with category: {category}")
                successful_inserts += 1
            else:
                print(f"✗ Failed to insert record {record_id}")
            
            processed_count += 1
            
        except Exception as e:
            print(f"✗ Error processing record {record.get('record_id_bank', 'unknown')}: {e}")
            continue
    
    # Summary
    print(f"\nProcessing complete!")
    print(f"Processed: {processed_count} records")
    print(f"Successfully inserted: {successful_inserts} records")

def main():
    """Main loop to run processing every minute"""
    while True:
        try:
            process_records()
            print("\nWaiting 1 minute before next processing cycle...")
            time.sleep(60)
        except KeyboardInterrupt:
            print("\nProcessing stopped by user.")
            break
        except Exception as e:
            print(f"\nError in main loop: {e}")
            print("Continuing after 1 minute...")
            time.sleep(60)

if __name__ == "__main__":
    main()
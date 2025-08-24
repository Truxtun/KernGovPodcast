#!/usr/bin/env python3
"""
Kern County Weekly Podcast Content Generator
Scrapes government meetings and generates NotebookLM files
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from kern_scraper import KernCountyScraper
from ai_processor import AIProcessor
from notebooklm_generator import NotebookLMGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main scraper execution"""
    try:
        logger.info("🚀 Starting Kern County weekly podcast generation...")
        
        # Initialize components
        scraper = KernCountyScraper()
        ai_processor = AIProcessor(api_key=os.getenv('OPENAI_API_KEY'))
        notebooklm_gen = NotebookLMGenerator()
        
        # Get date range for this week
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())  # Monday
        week_end = week_start + timedelta(days=6)  # Sunday
        
        logger.info(f"📅 Processing week: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}")
        
        # Step 1: Scrape meetings
        logger.info("🔍 Scraping government meetings...")
        meetings_data = scraper.scrape_weekly_meetings(week_start, week_end)
        
        if not meetings_data:
            logger.warning("⚠️ No meetings found for this week")
            return
            
        logger.info(f"✅ Found {len(meetings_data)} meetings")
        
        # Step 2: Process with AI
        logger.info("🤖 Processing content with AI...")
        processed_data = ai_processor.process_meetings(meetings_data)
        
        # Step 3: Generate NotebookLM files
        logger.info("📝 Generating NotebookLM files...")
        notebooklm_gen.generate_files(processed_data)
        
        # Step 4: Save raw data
        data_dir = Path("../data")
        data_dir.mkdir(exist_ok=True)
        
        with open(data_dir / "latest-meetings.json", "w") as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "week_range": f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}",
                "meetings": meetings_data,
                "processed": processed_data
            }, f, indent=2)
            
        # Step 5: Update website data
        logger.info("🌐 Updating website with latest data...")
        update_website_data(processed_data, week_start, week_end)
        
        logger.info("🎉 Weekly podcast generation complete!")
        
    except Exception as e:
        logger.error(f"❌ Error in main execution: {str(e)}")
        raise

def update_website_data(processed_data, week_start, week_end):
    """Update the website's JavaScript data with latest results"""
    
    # Generate JavaScript data file
    js_data = f"""
// Auto-generated on {datetime.now().isoformat()}
// Week: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}

window.LATEST_PODCAST_DATA = {{
    weekRange: "{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}",
    generatedDate: "{datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
    upcomingMeetings: {json.dumps(processed_data.get('upcoming_meetings', []), indent=4)},
    recentMinutes: {json.dumps(processed_data.get('recent_minutes', []), indent=4)},
    commonThemes: {json.dumps(processed_data.get('themes', []), indent=4)},
    notebookFiles: [
        {{
            name: "meeting-summaries.txt",
            description: "Comprehensive meeting summaries in conversational format",
            downloadUrl: "data/notebooklm-files/meeting-summaries.txt"
        }},
        {{
            name: "themes-connections.txt", 
            description: "Cross-meeting themes and their local impact",
            downloadUrl: "data/notebooklm-files/themes-connections.txt"
        }},
        {{
            name: "podcast-guidelines.txt",
            description: "Instructions for podcast tone and focus areas", 
            downloadUrl: "data/notebooklm-files/podcast-guidelines.txt"
        }}
    ]
}};
"""
    
    # Write to website directory
    with open("../latest-data.js", "w") as f:
        f.write(js_data)

if __name__ == "__main__":
    main()

"""
AI-powered meeting content processor
Uses OpenAI to summarize and analyze government meetings
"""

import openai
import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class AIProcessor:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        
    def process_meetings(self, meetings_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process raw meeting data into podcast-ready content"""
        
        # Separate upcoming vs recent meetings
        upcoming = [m for m in meetings_data if self._is_upcoming(m)]
        recent = [m for m in meetings_data if not self._is_upcoming(m)]
        
        # Process each category
        processed_upcoming = self._process_upcoming_meetings(upcoming)
        processed_recent = self._process_recent_meetings(recent)
        themes = self._find_common_themes(meetings_data)
        
        return {
            'upcoming_meetings': processed_upcoming,
            'recent_minutes': processed_recent,
            'themes': themes,
            'total_meetings': len(meetings_data)
        }
    
    def _is_upcoming(self, meeting: Dict[str, Any]) -> bool:
        """Determine if meeting is upcoming or past"""
        from datetime import datetime
        try:
            meeting_date = datetime.fromisoformat(meeting['date'].replace('Z', '+00:00'))
            return meeting_date > datetime.now()
        except:
            return False
    
    def _process_upcoming_meetings(self, meetings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate summaries for upcoming meetings"""
        processed = []
        
        for meeting in meetings:
            try:
                summary = self._summarize_agenda(meeting)
                processed.append({
                    'agency': meeting['agency'],
                    'date': meeting['date'],
                    'type': meeting.get('type', 'Regular Meeting'),
                    'summary': summary,
                    'agenda_url': meeting.get('agenda_url')
                })
            except Exception as e:
                logger.error(f"Error processing upcoming meeting: {str(e)}")
                
        return processed
    
    def _process_recent_meetings(self, meetings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate summaries for recent meeting minutes"""
        processed = []
        
        for meeting in meetings:
            try:
                summary = self._summarize_minutes(meeting)
                processed.append({
                    'agency': meeting['agency'],
                    'date': meeting['date'],
                    'type': meeting.get('type', 'Regular Meeting'),
                    'summary': summary
                })
            except Exception as e:
                logger.error(f"Error processing recent meeting: {str(e)}")
                
        return processed
    
    def _summarize_agenda(self, meeting: Dict[str, Any]) -> str:
        """Use AI to summarize agenda items for upcoming meetings"""
        
        prompt = f"""
        Summarize this government meeting agenda in a conversational, podcast-friendly way:
        
        Agency: {meeting['agency']}
        Date: {meeting['date']}
        Raw content: {meeting.get('raw_content', 'No content available')}
        
        Focus on:
        - What decisions will be made
        - How they affect local residents
        - Why people should care
        - Keep it under 100 words
        - Use everyday language
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"AI summarization error: {str(e)}")
            return "Summary unavailable - please check the agenda directly."
    
    def _summarize_minutes(self, meeting: Dict[str, Any]) -> str:
        """Use AI to summarize meeting minutes for recent meetings"""
        
        prompt = f"""
        Summarize what happened in this government meeting in a podcast-friendly way:
        
        Agency: {meeting['agency']}
        Date: {meeting['date']}
        Content: {meeting.get('raw_content', 'No content available')}
        
        Focus on:
        - What decisions were made
        - Key votes and outcomes
        - Impact on residents
        - Keep it under 100 words
        - Use past tense
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"AI summarization error: {str(e)}")
            return "Summary unavailable."
    
    def _find_common_themes(self, meetings_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify themes that span multiple meetings"""
        
        # Combine all meeting content
        all_content = "\n\n".join([
            f"{m['agency']}: {m.get('raw_content', '')}" 
            for m in meetings_data
        ])
        
        prompt = f"""
        Analyze these government meetings and identify 2-3 major themes that connect across multiple agencies:
        
        {all_content}
        
        For each theme, provide:
        - Theme name
        - Brief description
        - Which meetings/agencies are involved
        - Why it matters to residents
        
        Format as JSON array.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            # Try to parse as JSON, fallback to structured text
            content = response.choices[0].message.content.strip()
            try:
                return json.loads(content)
            except:
                # Fallback: return as single theme
                return [{"theme": "Multi-Agency Coordination", "description": content}]
                
        except Exception as e:
            logger.error(f"Theme analysis error: {str(e)}")
            return []

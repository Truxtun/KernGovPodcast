"""
Generate NotebookLM-ready files for podcast creation
"""

from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class NotebookLMGenerator:
    def __init__(self):
        self.output_dir = Path("../data/notebooklm-files")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_files(self, processed_data: dict):
        """Generate all NotebookLM files"""
        
        # Generate each file
        self._generate_meeting_summaries(processed_data)
        self._generate_themes_connections(processed_data)
        self._generate_podcast_guidelines(processed_data)
        
        logger.info(f"✅ Generated NotebookLM files in {self.output_dir}")
    
    def _generate_meeting_summaries(self, data: dict):
        """Generate meeting summaries file"""
        
        content = f"""KERN COUNTY GOVERNMENT MEETING SUMMARIES
Week of {datetime.now().strftime('%B %d, %Y')}

This document contains summaries of government meetings in Kern County, prepared for podcast discussion.

UPCOMING MEETINGS - What's Coming This Week:

"""
        
        for meeting in data.get('upcoming_meetings', []):
            content += f"""{meeting['agency']} - {datetime.fromisoformat(meeting['date']).strftime('%A, %B %d')}

Meeting Type: {meeting['type']}

What to Expect:
{meeting['summary']}

Why This Matters:
These decisions directly impact Kern County residents through changes to local services, infrastructure, and regulations.

Public Participation:
Residents can attend in person or watch online. Public comment periods are available.
{f"Agenda: {meeting.get('agenda_url', 'Check agency website')}" if meeting.get('agenda_url') else ''}

---

"""

        content += """
RECENT DECISIONS - What Just Happened:

"""
        
        for meeting in data.get('recent_minutes', []):
            content += f"""{meeting['agency']} - {datetime.fromisoformat(meeting['date']).strftime('%A, %B %d')}

Decisions Made:
{meeting['summary']}

Impact on Community:
These decisions will affect residents through changes to local services, development, and governance.

---

"""
        
        # Write file
        with open(self.output_dir / "meeting-summaries.txt", "w", encoding="utf-8") as f:
            f.write(content)
    
    def _generate_themes_connections(self, data: dict):
        """Generate themes and connections file"""
        
        content = f"""CROSS-MEETING THEMES AND CONNECTIONS
Kern County Government Weekly Analysis

Generated: {datetime.now().strftime('%B %d, %Y')}

This document identifies themes that span multiple government meetings, showing how different agencies are addressing related challenges.

"""
        
        for i, theme in enumerate(data.get('themes', []), 1):
            theme_name = theme.get('theme', f'Theme {i}')
            description = theme.get('description', 'No description available')
            
            content += f"""MAJOR THEME #{i}: {theme_name.upper()}

What's Happening:
{description}

Why This Coordination Matters:
When multiple agencies address similar issues simultaneously, it often indicates a coordinated response to regional challenges. Understanding these connections helps residents see the bigger picture of local governance.

Resident Impact:
These coordinated efforts typically result in more comprehensive solutions but may also mean broader changes to services, regulations, or costs.

Discussion Points:
- How do these related decisions affect different parts of the community?
- What are the potential unintended consequences?
- How can residents provide input across multiple agencies?

---

"""
        
        content += """
CONNECTIONS BETWEEN MEETINGS:

The themes above aren't isolated issues - they represent interconnected challenges that require coordinated solutions. When analyzing local government, it's important to understand how decisions in one meeting may influence or depend on decisions in another.

Key Questions for Discussion:
- Which agencies are working together on shared challenges?
- How do timing and sequencing of decisions matter?
- What are the cumulative effects on residents?
- Where are there opportunities for greater coordination?

Understanding these connections helps residents engage more effectively with local government and see how individual decisions fit into broader community planning.
"""
        
        # Write file
        with open(self.output_dir / "themes-connections.txt", "w", encoding="utf-8") as f:
            f.write(content)
    
    def _generate_podcast_guidelines(self, data: dict):
        """Generate podcast guidelines file"""
        
        meeting_count = len(data.get('upcoming_meetings', [])) + len(data.get('recent_minutes', []))
        
        content = f"""PODCAST GENERATION GUIDELINES
Kern County Weekly Government Roundup

EPISODE INFORMATION:
Episode Date: {datetime.now().strftime('%B %d, %Y')}
Meetings Covered: {meeting_count}
Target Length: 12-15 minutes

TONE AND STYLE GUIDELINES:
- Maintain a conversational, accessible tone
- Explain government processes in everyday language
- Focus on practical impacts for residents
- Make connections between different meetings and agencies
- Encourage civic engagement without being preachy

DISCUSSION FOCUS AREAS:
1. Connect related agenda items across different agencies
2. Translate government language into clear resident impacts  
3. Explain timing - why these issues are coming up now
4. Highlight opportunities for public participation
5. Put local decisions in regional/state context when relevant

STRUCTURE SUGGESTIONS:
- Open with the week's most significant theme or surprising connection
- Use transitions like "Speaking of [topic]..." to connect related items
- Spend 2-3 minutes maximum on any single topic
- End with concrete next steps for engaged citizens
- Include a brief preview of next week if major items are known

RESIDENT ENGAGEMENT REMINDERS:
- Most meetings include public comment periods
- Agendas are posted 72 hours in advance on agency websites
- Many meetings are live-streamed or recorded
- Contact information for officials is available on websites
- Local government decisions often have more direct impact than state/federal

AVOID:
- Reading agenda items verbatim or getting lost in procedural details
- Making partisan political commentary
- Overwhelming listeners with too many numbers, dates, or bureaucratic terms
- Assuming listeners know government processes or local history

DISCUSSION PROMPTS:
- "What's interesting about this timing is..."
- "Here's why this matters to residents..."
- "The connection between these two decisions is..."
- "If you're wondering how to get involved..."
- "Looking ahead, this could mean..."

TONE EXAMPLES:
✅ Good: "The county's water restrictions and the city's infrastructure funding aren't separate issues - they're two parts of the same strategy."

❌ Avoid: "Agenda item 47 under new business involves Resolution 2024-089 regarding amendments to the professional services agreement..."

MAKE IT CONVERSATIONAL:
Imagine you're explaining these decisions to a neighbor who cares about the community but doesn't follow government meetings closely. What would they want to know? How would you help them understand why it matters?
"""
        
        # Write file
        with open(self.output_dir / "podcast-guidelines.txt", "w", encoding="utf-8") as f:
            f.write(content)

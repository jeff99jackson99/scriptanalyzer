#!/usr/bin/env python3
"""
NeedGod Script Flow App
A Streamlit app that follows the script flow based on user answers
"""

import streamlit as st
import json
import re
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="NeedGod Script Flow",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ScriptFlow:
    """Manages the script flow logic"""
    
    def __init__(self):
        self.script_data = {}
        self.current_question = None
        self.conversation_history = []
        self.load_script_data()
    
    def load_script_data(self):
        """Load script data from text file"""
        try:
            if os.path.exists("script_content.txt"):
                with open("script_content.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                self.parse_script(content)
            else:
                st.error("Script content file not found. Please run extract_pdf.py first.")
        except Exception as e:
            st.error(f"Error loading script: {e}")
    
    def parse_script(self, content: str):
        """Parse the script content to extract questions and flow logic"""
        # Multiple patterns to catch different question formats
        patterns = [
            r'(\d+)\s*[\.\)]\s*(.+?)(?=\n\d+|\n\n|$)',  # 1. Question text
            r'Question\s*(\d+)[:\.]\s*(.+?)(?=\nQuestion|\n\n|$)',  # Question 1: text
            r'Q(\d+)[:\.]\s*(.+?)(?=\nQ\d+|\n\n|$)',  # Q1: text
        ]
        
        self.script_data = {
            "questions": {},
            "flow_logic": {},
            "raw_content": content
        }
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            for match in matches:
                q_num = int(match[0])
                q_text = match[1].strip()
                
                # Clean up the question text
                q_text = re.sub(r'\s+', ' ', q_text)  # Normalize whitespace
                q_text = q_text.replace('\n', ' ').strip()
                
                if q_num not in self.script_data["questions"]:
                    self.script_data["questions"][q_num] = {
                        "text": q_text,
                        "answers": {},
                        "next_questions": [],
                        "keywords": self.extract_keywords(q_text)
                    }
        
        # Look for flow indicators (if/then, go to, next question, etc.)
        self.analyze_flow_logic()
        
        st.success(f"✅ Loaded {len(self.script_data['questions'])} questions from script")
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from question text"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords[:10]  # Top 10 keywords
    
    def analyze_flow_logic(self):
        """Analyze the script for flow logic patterns"""
        # Look for patterns like "if yes, go to question X" or "if no, continue to question Y"
        flow_patterns = [
            r'if\s+(yes|no|maybe|true|false)\s*[,\.]\s*(?:go\s+to|continue\s+to|next\s+question)\s*(\d+)',
            r'(?:go\s+to|continue\s+to|next\s+question)\s*(\d+)\s*if\s+(yes|no|maybe|true|false)',
            r'answer\s+(yes|no|maybe|true|false)[:\.]\s*(?:go\s+to|continue\s+to|next\s+question)\s*(\d+)',
        ]
        
        for pattern in flow_patterns:
            matches = re.findall(pattern, self.script_data["raw_content"], re.IGNORECASE)
            for match in matches:
                answer = match[0].lower()
                next_q = int(match[1])
                # This would need more sophisticated parsing based on actual script structure
                pass
    
    def get_question(self, question_num: int) -> Optional[Dict]:
        """Get question data by number"""
        return self.script_data["questions"].get(question_num)
    
    def get_next_question(self, current_q: int, answer: str) -> Optional[int]:
        """Determine next question based on current question and answer"""
        # For now, implement simple sequential flow
        # This should be enhanced based on actual script logic
        
        # Look for explicit flow instructions in the content
        answer_lower = answer.lower()
        
        # Simple keyword-based flow (can be enhanced)
        if any(word in answer_lower for word in ['yes', 'true', 'correct', 'agree']):
            # Positive answer - might skip some questions
            return current_q + 1
        elif any(word in answer_lower for word in ['no', 'false', 'incorrect', 'disagree']):
            # Negative answer - might go to different path
            return current_q + 1
        else:
            # Default: next question
            return current_q + 1 if current_q + 1 in self.script_data["questions"] else None

def main():
    st.title("📖 NeedGod Script Flow App")
    st.markdown("*Follow the script flow based on your answers*")
    
    # Initialize session state
    if "script_flow" not in st.session_state:
        st.session_state.script_flow = ScriptFlow()
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = 1
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    script_flow = st.session_state.script_flow
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.current_question = 1
            st.session_state.conversation_history = []
            st.rerun()
        
        if st.button("📄 View Full Script"):
            st.session_state.show_full_script = not st.session_state.get("show_full_script", False)
        
        st.header("📊 Progress")
        total_questions = len(script_flow.script_data.get("questions", {}))
        if total_questions > 0:
            progress = st.session_state.current_question / total_questions
            st.progress(progress)
            st.write(f"Question {st.session_state.current_question} of {total_questions}")
            
            # Show question list
            st.subheader("📋 All Questions")
            for q_num in sorted(script_flow.script_data["questions"].keys()):
                status = "🟢" if q_num == st.session_state.current_question else "⚪"
                if q_num < st.session_state.current_question:
                    status = "✅"
                st.write(f"{status} Q{q_num}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Current Question")
        
        # Get current question
        current_q_data = script_flow.get_question(st.session_state.current_question)
        
        if current_q_data:
            st.subheader(f"Question {st.session_state.current_question}")
            st.info(current_q_data["text"])
            
            # Show keywords for context
            if current_q_data["keywords"]:
                st.caption(f"Keywords: {', '.join(current_q_data['keywords'][:5])}")
            
            st.divider()
            
            # Answer section
            st.subheader("Your Answer")
            
            # Quick answer buttons
            col_yes, col_no, col_maybe = st.columns(3)
            
            with col_yes:
                if st.button("✅ Yes", use_container_width=True, type="primary"):
                    process_answer("Yes")
            
            with col_no:
                if st.button("❌ No", use_container_width=True):
                    process_answer("No")
            
            with col_maybe:
                if st.button("🤔 Maybe", use_container_width=True):
                    process_answer("Maybe")
            
            # Custom answer input
            st.subheader("Custom Answer")
            custom_answer = st.text_input(
                "Type your answer:",
                placeholder="Enter your detailed answer here...",
                key=f"answer_{st.session_state.current_question}"
            )
            
            if st.button("Submit Custom Answer", type="secondary"):
                if custom_answer.strip():
                    process_answer(custom_answer.strip())
                else:
                    st.warning("Please enter an answer.")
        
        else:
            # End of conversation
            st.header("🎉 Conversation Complete!")
            st.success("You've completed all questions in the script.")
            
            if st.session_state.conversation_history:
                st.subheader("📋 Final Summary")
                for i, entry in enumerate(st.session_state.conversation_history, 1):
                    with st.expander(f"Q{entry['question_num']} - {entry.get('timestamp', '')}"):
                        st.write(f"**Question:** {entry['question_text']}")
                        st.write(f"**Answer:** {entry['answer']}")
    
    with col2:
        st.header("📚 Conversation History")
        
        if st.session_state.conversation_history:
            for entry in reversed(st.session_state.conversation_history[-10:]):  # Show last 10
                with st.container():
                    st.markdown(f"**Q{entry['question_num']}** ({entry.get('timestamp', '')})")
                    st.markdown(f"*{entry['question_text'][:50]}...*")
                    st.markdown(f"**A:** {entry['answer']}")
                    st.divider()
        else:
            st.info("No conversation history yet.")
        
        # Script info
        st.header("📄 Script Info")
        if script_flow.script_data:
            st.write(f"**Total Questions:** {len(script_flow.script_data['questions'])}")
            st.write(f"**Questions Found:** {sorted(script_flow.script_data['questions'].keys())}")
            
            # Show sample questions
            st.subheader("Sample Questions")
            sample_questions = list(script_flow.script_data["questions"].items())[:3]
            for q_num, q_data in sample_questions:
                st.write(f"**Q{q_num}:** {q_data['text'][:100]}...")

def process_answer(answer: str):
    """Process the user's answer and move to next question"""
    script_flow = st.session_state.script_flow
    
    # Add answer to history
    current_q_data = script_flow.get_question(st.session_state.current_question)
    if current_q_data:
        st.session_state.conversation_history.append({
            "question_num": st.session_state.current_question,
            "question_text": current_q_data["text"],
            "answer": answer,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    # Determine next question
    next_q = script_flow.get_next_question(st.session_state.current_question, answer)
    
    if next_q and next_q in script_flow.script_data["questions"]:
        st.session_state.current_question = next_q
        st.success(f"✅ Answer recorded. Moving to Question {next_q}")
    else:
        st.success("✅ Answer recorded. Conversation complete!")
    
    st.rerun()

if __name__ == "__main__":
    main()

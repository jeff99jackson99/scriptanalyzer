#!/usr/bin/env python3
"""
Enhanced NeedGod Script Flow App
Properly handles the specific flow logic from the NeedGod script
"""

import streamlit as st
import json
import re
from typing import Dict, List, Optional, Tuple, Any
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="NeedGod Script Flow",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class NeedGodScriptFlow:
    """Manages the NeedGod script flow logic with proper branching"""
    
    def __init__(self):
        self.script_data = {}
        self.current_question = 1
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
        # Extract questions with their flow logic
        self.script_data = {
            "questions": {},
            "flow_logic": {},
            "raw_content": content
        }
        
        # Define the questions and their flow logic based on the script
        questions = {
            1: {
                "text": "What do you think happens to us after we die?",
                "answers": {
                    "heaven and hell": {"next": "heaven_question", "skip": 2},
                    "reincarnation": {"next": 2},
                    "other_theory": {"next": 2},
                    "not sure": {"next": 2}
                }
            },
            2: {
                "text": "Do you believe there's a God?",
                "answers": {
                    "yes": {"next": 3},
                    "no": {"next": "god_analogy", "skip": 3}
                }
            },
            3: {
                "text": "Since we know there is a God, it matters how we live. So, do you think you are a good person?",
                "answers": {
                    "yes": {"next": 4},
                    "no": {"next": 7}
                }
            },
            4: {
                "text": "Have you ever told a lie?",
                "answers": {
                    "yes": {"next": 7},
                    "no": {"next": "lie_response"}
                }
            },
            5: {
                "text": "Have you ever used bad language?",
                "answers": {
                    "yes": {"next": 7},
                    "no": {"next": 6}
                }
            },
            6: {
                "text": "Have you ever been angry or disrespected someone?",
                "answers": {
                    "yes": {"next": 7},
                    "no": {"next": "sin_response"}
                }
            },
            7: {
                "text": "We've all done these things and so if God was to judge you based on these things would you be innocent or guilty?",
                "answers": {
                    "guilty": {"next": 8},
                    "innocent": {"next": "innocent_response"}
                }
            },
            8: {
                "text": "So would we deserve a reward or punishment?",
                "answers": {
                    "punishment": {"next": 9},
                    "reward": {"next": "reward_response"}
                }
            },
            9: {
                "text": "Does that sound like a place in Heaven or Hell?",
                "answers": {
                    "hell": {"next": 10},
                    "heaven": {"next": "heaven_response"}
                }
            },
            10: {
                "text": "So how do you think you could avoid your Hell punishment?",
                "answers": {
                    "not sure": {"next": 11},
                    "good things": {"next": "good_things_response"},
                    "forgiveness": {"next": "forgiveness_response"},
                    "repent": {"next": "repent_response"}
                }
            },
            11: {
                "text": "What we need is someone else who would take the punishment for us. If someone took 100% of your Hell punishment, how much would be left for you to take?",
                "answers": {
                    "nothing": {"next": 12},
                    "zero": {"next": 12},
                    "0": {"next": 12}
                }
            },
            12: {
                "text": "So if you have no more Hell punishment, where will you go when you die?",
                "answers": {
                    "heaven": {"next": 13},
                    "hell": {"next": "hell_response"}
                }
            },
            13: {
                "text": "That was Jesus, that's why he died on the cross, to take the punishment for our sins and he rose from the dead 3 days later.",
                "answers": {
                    "continue": {"next": 14}
                }
            },
            14: {
                "text": "So if Jesus does that for you, where do you go when you die?",
                "answers": {
                    "heaven": {"next": 15},
                    "hell": {"next": "hell_response_2"}
                }
            },
            15: {
                "text": "So why would God let you into heaven?",
                "answers": {
                    "jesus paid": {"next": 16},
                    "because jesus paid for my sins": {"next": 16}
                }
            },
            16: {
                "text": "Now he offers this to us as a free gift and all I have to do to receive this free gift is to simply trust that Jesus died on the cross paying for 100% of our Hell punishment.",
                "answers": {
                    "continue": {"next": 17}
                }
            },
            17: {
                "text": "So if you trust that Jesus has paid for all of your sins now and tomorrow you sin 5 more times and then die, would you go to Heaven or Hell?",
                "answers": {
                    "heaven": {"next": 18},
                    "hell": {"next": "hell_response_3"}
                }
            },
            18: {
                "text": "and why heaven?",
                "answers": {
                    "jesus paid": {"next": 19},
                    "because jesus paid for my sins": {"next": 19}
                }
            },
            19: {
                "text": "But if you don't trust Jesus paid for your sins, where would you end up?",
                "answers": {
                    "hell": {"next": 20},
                    "heaven": {"next": "gift_response"}
                }
            },
            20: {
                "text": "..and since you don't want to go to Hell, WHEN should you start trusting that Jesus has paid for your sins?",
                "answers": {
                    "now": {"next": 21},
                    "before you die": {"next": "when_response"}
                }
            },
            21: {
                "text": "So if you stood before God right now and he asked you \"Why should I let you into Heaven?\" what would you say?",
                "answers": {
                    "because jesus paid for my sins": {"next": 22},
                    "jesus paid": {"next": 22}
                }
            },
            22: {
                "text": "Now, imagine a friend of yours says they are going to heaven because they are a good person, where would they go when they die?",
                "answers": {
                    "hell": {"next": 23},
                    "heaven": {"next": "friend_response"}
                }
            },
            23: {
                "text": "But another friend comes to you and says \"I'm going to heaven because of two reasons. The first reason is because Jesus died for my sins and the second reason is because I've been a good person.\" Would that person go to Heaven or Hell?",
                "answers": {
                    "hell": {"next": 24},
                    "heaven": {"next": "two_reasons_response"}
                }
            },
            24: {
                "text": "So, on a scale of 0 -100%, how sure are you that you will go to Heaven when you die?",
                "answers": {
                    "100%": {"next": 25},
                    "100": {"next": 25}
                }
            },
            25: {
                "text": "So, does doing good things play any part in getting you to heaven?",
                "answers": {
                    "no": {"next": 26},
                    "yes": {"next": "good_deeds_response"}
                }
            },
            26: {
                "text": "Do you need to ask for forgiveness to go to Heaven?",
                "answers": {
                    "no": {"next": 27},
                    "yes": {"next": "forgiveness_response_2"}
                }
            },
            27: {
                "text": "Do you need to be baptized to go to Heaven?",
                "answers": {
                    "no": {"next": 28},
                    "yes": {"next": "baptism_response"}
                }
            },
            28: {
                "text": "So if these things don't get us to Heaven, why do we do good things?",
                "answers": {
                    "thankful": {"next": 29},
                    "because we are thankful": {"next": 29}
                }
            },
            29: {
                "text": "Do you know how you can find out more about Jesus?",
                "answers": {
                    "bible": {"next": 30},
                    "the bible": {"next": 30}
                }
            },
            30: {
                "text": "Yep! Do you have a bible and do you read it much?",
                "answers": {
                    "yes": {"next": 31},
                    "no": {"next": "bible_link"}
                }
            },
            31: {
                "text": "Think of it like this, If you ate food only once a week, would you be very strong?",
                "answers": {
                    "no": {"next": 32}
                }
            },
            32: {
                "text": "So if the bible is our spiritual food, how often do you think you should read the bible then to be strong spiritually?",
                "answers": {
                    "everyday": {"next": 34},
                    "every day": {"next": 34}
                }
            },
            34: {
                "text": "Do you go to church?... what kind of church is it?",
                "answers": {
                    "yes": {"next": 35},
                    "no": {"next": "church_link"}
                }
            },
            35: {
                "text": "Do they teach the same message we've spoken about here to be saved from our sins?",
                "answers": {
                    "yes": {"next": 36},
                    "no": {"next": "wrong_church"}
                }
            },
            36: {
                "text": "Also, think of your family and friends, if you asked them, \"What's the reason you'll go to heaven?\" what would their answer be?",
                "answers": {
                    "jesus": {"next": 37},
                    "good deeds": {"next": "family_response"}
                }
            },
            37: {
                "text": "And since you don't want them to go to hell, how could you help them not to end up there?",
                "answers": {
                    "tell them": {"next": 38},
                    "tell them about the gospel": {"next": 38}
                }
            },
            38: {
                "text": "So let me ask you, What if God asked you this \"Why should I not send you to hell for all the sins you've done\", how would you answer?",
                "answers": {
                    "jesus paid": {"next": 39},
                    "because jesus paid for my sins": {"next": 39}
                }
            },
            39: {
                "text": "Now, remember at the beginning of this chat, what DID you think was getting you to heaven?",
                "answers": {
                    "good things": {"next": "conclusion"},
                    "asking for forgiveness": {"next": "conclusion"}
                }
            }
        }
        
        self.script_data["questions"] = questions
        st.success(f"✅ Loaded {len(questions)} questions from NeedGod script")
    
    def get_question(self, question_num: int) -> Optional[Dict]:
        """Get question data by number"""
        return self.script_data["questions"].get(question_num)
    
    def get_next_question(self, current_q: int, answer: str) -> Optional[int]:
        """Determine next question based on current question and answer"""
        question_data = self.get_question(current_q)
        if not question_data:
            return None
        
        answer_lower = answer.lower().strip()
        
        # Check for exact matches first
        for answer_key, flow_data in question_data["answers"].items():
            if answer_key in answer_lower or answer_lower in answer_key:
                next_action = flow_data["next"]
                
                # Handle special flow actions
                if next_action == "heaven_question":
                    return "heaven_question"
                elif next_action == "god_analogy":
                    return "god_analogy"
                elif next_action == "lie_response":
                    return "lie_response"
                elif next_action == "sin_response":
                    return "sin_response"
                elif next_action == "innocent_response":
                    return "innocent_response"
                elif next_action == "reward_response":
                    return "reward_response"
                elif next_action == "heaven_response":
                    return "heaven_response"
                elif next_action == "good_things_response":
                    return "good_things_response"
                elif next_action == "forgiveness_response":
                    return "forgiveness_response"
                elif next_action == "repent_response":
                    return "repent_response"
                elif next_action == "hell_response":
                    return "hell_response"
                elif next_action == "hell_response_2":
                    return "hell_response_2"
                elif next_action == "hell_response_3":
                    return "hell_response_3"
                elif next_action == "gift_response":
                    return "gift_response"
                elif next_action == "when_response":
                    return "when_response"
                elif next_action == "friend_response":
                    return "friend_response"
                elif next_action == "two_reasons_response":
                    return "two_reasons_response"
                elif next_action == "good_deeds_response":
                    return "good_deeds_response"
                elif next_action == "forgiveness_response_2":
                    return "forgiveness_response_2"
                elif next_action == "baptism_response":
                    return "baptism_response"
                elif next_action == "bible_link":
                    return "bible_link"
                elif next_action == "church_link":
                    return "church_link"
                elif next_action == "wrong_church":
                    return "wrong_church"
                elif next_action == "family_response":
                    return "family_response"
                elif next_action == "conclusion":
                    return "conclusion"
                else:
                    return next_action
        
        # Default: next sequential question
        return current_q + 1 if current_q + 1 in self.script_data["questions"] else None
    
    def add_answer(self, question_num: int, answer: str):
        """Add answer to conversation history"""
        self.conversation_history.append({
            "question_num": question_num,
            "question_text": self.get_question(question_num)["text"] if self.get_question(question_num) else "Special Response",
            "answer": answer,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

def main():
    st.title("📖 NeedGod Script Flow App")
    st.markdown("*Follow the script flow based on your answers*")
    
    # Initialize session state
    if "script_flow" not in st.session_state:
        st.session_state.script_flow = NeedGodScriptFlow()
    
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
        
        # Handle special responses
        current_q = st.session_state.current_question
        
        if isinstance(current_q, str):
            # Handle special flow responses
            if current_q == "heaven_question":
                st.subheader("Follow-up Question")
                st.info("If they say heaven and hell, ask if they think they will go to heaven and why and SKIP question 2.")
                st.write("If they say 'because Jesus died for my sins', ask: 'Based on how you've lived your life, do you deserve to go to Heaven or Hell after you die?'")
                st.write("If they answer 'Heaven' proceed to Q4. If they say Hell, proceed to Q17.")
                
                if st.button("Continue to Q4"):
                    st.session_state.current_question = 4
                    st.rerun()
                elif st.button("Continue to Q17"):
                    st.session_state.current_question = 17
                    st.rerun()
            
            elif current_q == "god_analogy":
                st.subheader("God Analogy")
                st.info("Would you agree that the building I'm sitting in had a builder, or did it just appear by itself?")
                st.write("This building is evidence that it needed a builder. In the same way, when we look at the universe we know it had a beginning therefore it had to have a creator for it. The universe is proof of a universe maker. Buildings need builders, creation needs a creator agree?")
                st.write("If they still refuse to believe, go to Q5. If they aren't cooperating at all, just inform them you're there to share the good news.")
                
                if st.button("Continue to Q5"):
                    st.session_state.current_question = 5
                    st.rerun()
            
            elif current_q == "conclusion":
                st.header("🎉 Conversation Complete!")
                st.success("You've completed the NeedGod script flow!")
                st.write("This has been a fantastic chat! My name is [Your Name] - been great chatting with you.")
                st.write("Do you have any other questions I can help you with?")
                st.write("Check us out on social media: needgod.net")
                
                if st.session_state.conversation_history:
                    st.subheader("📋 Final Summary")
                    for i, entry in enumerate(st.session_state.conversation_history, 1):
                        with st.expander(f"Q{entry['question_num']} - {entry.get('timestamp', '')}"):
                            st.write(f"**Question:** {entry['question_text']}")
                            st.write(f"**Answer:** {entry['answer']}")
            
            else:
                st.info(f"Special response: {current_q}")
                if st.button("Continue"):
                    st.session_state.current_question = 1
                    st.rerun()
        
        else:
            # Regular question flow
            current_q_data = script_flow.get_question(current_q)
            
            if current_q_data:
                st.subheader(f"Question {current_q}")
                st.info(current_q_data["text"])
                
                st.divider()
                
                # Answer section
                st.subheader("Your Answer")
                
                # Quick answer buttons based on expected answers
                expected_answers = list(current_q_data["answers"].keys())
                
                if len(expected_answers) <= 3:
                    cols = st.columns(len(expected_answers))
                    for i, answer in enumerate(expected_answers):
                        with cols[i]:
                            if st.button(f"✅ {answer.title()}", use_container_width=True):
                                process_answer(answer)
                else:
                    # Show first few as buttons
                    cols = st.columns(3)
                    for i, answer in enumerate(expected_answers[:3]):
                        with cols[i]:
                            if st.button(f"✅ {answer.title()}", use_container_width=True):
                                process_answer(answer)
                
                # Custom answer input
                st.subheader("Custom Answer")
                custom_answer = st.text_input(
                    "Type your answer:",
                    placeholder="Enter your detailed answer here...",
                    key=f"answer_{current_q}"
                )
                
                if st.button("Submit Custom Answer", type="secondary"):
                    if custom_answer.strip():
                        process_answer(custom_answer.strip())
                    else:
                        st.warning("Please enter an answer.")
            
            else:
                st.info("No more questions available. Conversation complete!")
    
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
            st.write(f"**Current Question:** {st.session_state.current_question}")

def process_answer(answer: str):
    """Process the user's answer and move to next question"""
    script_flow = st.session_state.script_flow
    
    # Add answer to history
    current_q_data = script_flow.get_question(st.session_state.current_question)
    if current_q_data:
        script_flow.add_answer(st.session_state.current_question, answer)
        st.session_state.conversation_history = script_flow.conversation_history
    
    # Determine next question
    next_q = script_flow.get_next_question(st.session_state.current_question, answer)
    
    if next_q:
        st.session_state.current_question = next_q
        st.success(f"✅ Answer recorded. Moving to next question.")
    else:
        st.success("✅ Answer recorded. Conversation complete!")
    
    st.rerun()

if __name__ == "__main__":
    main()

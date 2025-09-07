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
        self.script_data = {"questions": {}, "flow_logic": {}, "raw_content": ""}
        self.current_question = 1
        self.conversation_history = []
        try:
            self.load_script_data()
        except Exception as e:
            st.error(f"Error initializing script flow: {e}")
            # Load embedded script as fallback
            self.load_embedded_script()
    
    def load_script_data(self):
        """Load script data from text file"""
        try:
            if os.path.exists("script_content.txt"):
                with open("script_content.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                self.parse_script(content)
            else:
                # Use embedded script content if file not found
                self.load_embedded_script()
        except Exception as e:
            st.error(f"Error loading script: {e}")
            # Fallback to embedded script
            self.load_embedded_script()
    
    def load_embedded_script(self):
        """Load embedded script content"""
        # Embedded script content from the PDF
        embedded_content = """
SCRIPT (v4.1) 
The following is a guide to your questions during a conversation. The bold text is what you need to say, 
the italic answers are the anticipated answers and guidance, DO NOT progress to further questions until 
the correct answer is given. Enjoy!  

Hey I have a question for you  
Sure..  

1. What do you think happens to us after we die?  
Not sure.  

If they say reincarnation or any other theory, usually it's best to go straight on to asking them the next 
question so as to not get bogged down or offend them right at the start.  

If they say heaven and hell, ask if they think they will go to heaven and why and SKIP question 2. If they 
say "because Jesus died for my sins", Ask: "Based on how you've lived your life, do you deserve to go to 
Heaven or Hell after you die? If they answer "Heaven" proceed to Q4. If they say Hell, proceed to Q17.  

2. Do you believe there's a God?  
Yes..  

If they say no, ask: "Would you agree that the building I'm sitting in had a builder, or did it just appear 
by itself? {wait for an answer} This building is evidence that it needed a builder. In the same way, when 
we look at the universe we know it had a beginning therefore it had to have a creator for it. The 
universe is proof of a universe maker. Buildings need builders, creation needs a creator agree?" 

Note: the next questions won't make sense to them if they don't believe in a God or creator so stick with 
it until they do. If they still refuse to believe, go to Q5. If they aren't cooperating at all, just inform them 
you're there to share the good news on how they can avoid their hell punishment but wish them well and 
pass on the socials links for them to see in case they change their mind.  

3. Since we know there is a God, it matters how we live. So, do you think you 
are a good person?  
Yes..  

If they say No, you can thank them for their honesty and explain how we have all done things wrong - 
give examples: lying, taking things we shouldn't have, being angry, using bad language. Then move to 
question 7.  

4. Have you ever told a lie?  
Yes..  

If they say no, you could say that they're telling you a lie right now as everybody alive has lied.  

5. Have you ever used bad language?  
Yes..  

6. Have you ever been angry or disrespected someone? 
Yes..  

Always make sure before moving forward you get a "YES" answer to either Q4, 5 or 6. If they persist on 
saying no, ask if they have ever sinned against God. If they say Yes, continue on. If they still say no, Say 
"Romans 3:23 tells us – for all have sinned and fall short of the Glory of God" Would you agree you're 
a sinner before God? If YES, then move on. If they still say No, you say them they have just committed 
the sin of pride. See if that humbles them, if not since they don't want to take the chat seriously, wish 
them well and send socials for them to contact us when they're ready for a serious chat.  

7. We've all done these things and so if God was to judge you based on these 
things would you be innocent or guilty?  
Guilty..  

If they say innocent, give them the definition: Innocent means you've never done anything wrong your 
whole life, and guilty means you've done at least one bad thing - so which one would you be?  

Some people will try and squeeze out of their situation either here or the next question by giving a 
solution like 'but I make sure to ask for forgiveness' or 'But God is forgiving' or 'But I am trying to do 
better'. Which you could respond with giving the courtroom analogy, or simply 'but we are still guilty of 
what we have done wrong and so...(move to next question).  

8. So would we deserve a reward or punishment?  
Punishment..  

If they say Reward (some do) ask, "Would a policeman give me a bunch of flowers for speeding OR a 
penalty notice?" If they say Reward, ask them what country would give flowers for speeding…  

9. Does that sound like a place in Heaven or Hell?  
Hell..  

If they say Heaven, ask them "Does heaven sound like punishment or would it be hell?" You could also 
ask them if a Judge would send a criminal to Disneyland or Prison  

10. So how do you think you could avoid your Hell punishment?  
Not sure..  

If they answer do good things, "Imagine if you did 5 serious crimes today and then tomorrow you did 
no more crimes and instead did 10 good things, would the police ignore your crimes?" 

"Right, same with God. Stopping sin and doing good doesn't take away the sins we have done, we still 
deserve the punishment which is hell.." 

If they answer ask for forgiveness/prayer, "Imagine you break a serious law in society and standing 
before the judge you ask for forgiveness. Will the judge let you go free?" {wait for an answer}  

"Right, same with God. Asking for forgiveness doesn't take away the punishment for breaking God's 
laws. Good to do but doesn't pay our hell fine." 

If they say Repent, ask them what they mean by repent. If they say: "Ask for forgiveness", refer to the 
analogy above. Many people will think it means ask for forgiveness, so you need to explain that it is a 
change of mind to trusting in Christ instead of NOT trusting in Christ, asking for forgiveness and turning 
from sin is the "result" of repentance.  

11. What we need is someone else who would take the punishment for us. If 
someone took 100% of your Hell punishment, how much would be left for you 
to take?  
Nothing..  

If they still struggle with saying nothing or zero, ask: "If someone chops off all of your fingers, do you 
have any left?" ..then repeat the question  

12. So if you have no more Hell punishment, where will you go when you die? 
Heaven..  

If they still say Hell, ask them again how our Hell punishment is paid for. (By having someone take it for 
us) 

If they are struggling to understand this concept, use the example of the speeding fine analogy.  
"Think of it like this: If you had a $1000 speeding fine and someone pays all $1000 for you as a gift. 
How much is left for you to pay?" "(zero)  
"In the same way, we deserve hell that is our fine (punishment) for our sins, but if Jesus pays 100% of 
our hell fine there would none left, so where would you get to go? And why?" 

13. That was Jesus, that's why he died on the cross, to take the punishment for 
our sins and he rose from the dead 3 days later.  

14. So if Jesus does that for you, where do you go when you die?  
Heaven..  

If they still say Hell, repeat the question like this "If Jesus takes ALL of your hell punishment, then how 
much is left for you to get in hell?" ... none.' Then repeat question 14 again.  

15. So why would God let you into heaven?  
Because Jesus paid for my sins..  

If they still think because of their actions, go back to Question 10  

16. Now he offers this to us as a free gift and all I have to do to receive this free 
gift is to simply trust that Jesus died on the cross paying for 100% of our Hell 
punishment.  

17. So if you trust that Jesus has paid for all of your sins now and tomorrow you 
sin 5 more times and then die, would you go to Heaven or Hell?  
Heaven..  

If they say Hell, Ask them: "What was getting you into heaven again? ... Jesus. And does Jesus pay for 
just your past sins or also your future sins?" Future .. Then repeat the initial question.  

If they say past only, say: "If Jesus died for 100% of your sins, that would have to include your future sins 
right?"  

18. and why heaven?  
Because Jesus paid for my sins..  

If they again think because of good works or asking for forgiveness, go back to Q10. 

Good answer, you'd still get to Heaven as Jesus has paid for your past, present, 
and future sins.  

19. But if you don't trust Jesus paid for your sins, where would you end up? 
Hell..  

If they say heaven, say: "If I offered you a gift today, but you didn't accept it from me, have you 
actually received that gift?" No. 

"In the same way, Jesus is offering to pay for our sins as a gift but if we don't accept it, we won't 
receive it and so where would we end up?" 

20. ..and since you don't want to go to Hell, WHEN should you start trusting that 
Jesus has paid for your sins? 
Now..  

If they say before you die, ask "Do you know when you will die? If not, when should you start trusting 
that Jesus paid for your sins?" 

21. So if you stood before God right now and he asked you "Why should I let 
you into Heaven?" what would you say?  
"Because Jesus paid for my sins.."  

If they say "I don't know" Ask, what was the reason you could go to heaven again? If they get that 
right, then return to re-ask Q21.  

If they answer anything beginning with "I accept or I believe…" Ask: "Now do we go to heaven because 
of what WE have done for God, or because of what HE has done for us? (He has done) Right, and so if 
our answer to God starts in the first person "I" we are about to point to what WE have done for God 
rather than what Jesus has done for us in dying for our sins. Make sense? So How would you re-
answer the question.." 

If they say "Both" (Is it what He does or we do) Say: "If Jesus takes 100% of our hell punishment, we get 
to go to heaven. So are you going to heaven because of YOU or because of HIM?" (Him)  

"Our answer shouldn't start with "Because I", but in the third person "Because Jesus...".  
So how would you re-word your answer to God's question as to why he should let you into heaven?" 

If they want a bible verse to support this, use: Matthew 7:22-23 - On that day many will say to me, 'Lord, 
Lord, did we not prophesy in your name, and cast out demons in your name, and do many mighty works 
in your name?'*23+ And then will I declare to them, 'I never knew you; depart from me, you workers of 
lawlessness.'  

22. Now, imagine a friend of yours says they are going to heaven because they 
are a good person, where would they go when they die?  
Hell.  

If they say Heaven, ask them "what's the reason why God would let someone into heaven?" ... Jesus. 
"Yep, so then is your friend trusting in Jesus to get them to heaven, or their own actions?" ... their own 
actions. "Right, and because they are trusting in their own actions where would they end up?"... hell. 

That's right, and why?  

23. But another friend comes to you and says "I'm going to heaven because of 
two reasons. The first reason is because Jesus died for my sins and the second 
reason is because I've been a good person." Would that person go to Heaven or 
Hell?  
Hell..  

If they say Heaven, Say: "By trusting in two things they aren't trusting 100% in Jesus to save them. It 
would be 50% Jesus and 50% their actions. So if Jesus only contributes 50%, where do they end up? 
Again, we have to trust that Jesus is the ONLY reason we are saved, not our actions." 

Exactly, because they are still trusting partly in themselves, and not ONLY in 
Jesus to save them. Makes sense?  
Yes..  

24. So, on a scale of 0 -100%, how sure are you that you will go to Heaven when 
you die?  
100%..  

If they say anything less, then ask "What was the reason you would go to heaven again? ... Jesus. Right, 
and how much of your punishment did Jesus take for you?" {wait for an answer} "So how much 
punishment is then left for you to still get in hell?" None …. "So if you trust in that, on a scale of 0 -
100%, how sure could you be that you will go to Heaven?"  

If they are still unsure, ask them what makes them less than 100% sure and deal with their 
answer. Reminding them that Jesus paid for past, present and future sins. 

25. So, does doing good things play any part in getting you to heaven?  
No.. 

If they say yes, again, ask them if it is our good deeds/things that saves us or Jesus dying on the cross.  
Refer to good deeds analogy in Q10 if needed.  

26. Do you need to ask for forgiveness to go to Heaven?  
No.. 

If they say yes, ask them if it is our asking for forgiveness that saves us or Jesus dying on the cross. Refer 
to good deeds analogy in Q10 if needed.  

27. Do you need to be baptized to go to Heaven?  
No..  

If they say yes, again, ask them if it is our baptism that saves us or Jesus dying on the cross.  

28. So if these things don't get us to Heaven, why do we do good things?  
Because we are thankful..  

If they can't answer this, say "If you are in a burning building and a fireman risks his life to bring you 
out to safety, what would you want to do for that fireman who saved you?" {wait for an answer} 
"Yeah, and you definitely don't want to punch him in the face, right? Same with Jesus, if He has laid 
his life down to save you from hell, what would you want to do for Jesus?" 

"If you're unconscious in the fire, you're relying on the fireman to do all the work as you can't help him 
at all because you're unconscious, Same for Jesus, we are dead in our sins and can't assist Jesus in 
saving us from the eternal Hell fire, He does all the work by dying on the cross for our sins, make 
sense?" 

And because we are thankful to Jesus for what he has done for us, that 
motivates us now to live our lives for him and avoid sinning. Does that make 
sense?  

We don't stop our sins and do good things for Jesus to save us, we do good 
things for him and desire to live better because he HAS saved us. Make sense?  
Yes..  

29. Do you know how you can find out more about Jesus?  
The Bible 

30. Yep! Do you have a bible and do you read it much?  

If they say No, you can share a link with them to get one.  

31. Think of it like this, If you ate food only once a week, would you be very 
strong?  
no.. 

Right. We eat food everyday to stay strong physically. Our bible is like our 
spiritual food.  

32. So if the bible is our spiritual food, how often do you think you should read 
the bible then to be strong spiritually? 
Everyday .. 

34. Do you go to church?... what kind of church is it?  
Yes..  

If they answer no, then say "Church is where you'll be able to hear God's word being preached and 
where you'll meet other Christians who can help you in your faith. Does that sound good?" 

Here's a link you can use to find a great church in your area (send church link)  

35. Do they teach the same message we've spoken about here to be saved from 
our sins?  
If they answer yes, then that's great. If they answer not really. Ask "So do you think it's a good 
idea to keep attending a church that teaches the wrong way to heaven?"  

Ask if they are able to get to another church on their own but if they can't, Suggest the following:  

- Spend time in personal prayer and reading the Bible to strengthen your faith on your own.  
- Think about who you could share the gospel with at your church, because you want them to be 
saved.  
- Make sure to check anything you are hearing at church, with the Bible.  
- Don't be bowing down to any statues/pictures or praying to anyone other than God.  
- Listen in to some good preachers online, such as Alistair Begg (search his name on YouTube).  

36. Also, think of your family and friends, if you asked them, "What's the reason 
you'll go to heaven?" what would their answer be?  
I'm not sure.. or they may say they'll go to heaven because of Jesus..  

If they answer with doing good deeds gets them to heaven then ask: "So where would they end 
up?"(Hell) Refer to good deeds analogy in Q10 if needed.  

37. And since you don't want them to go to hell, how could you help them not 
to end up there?  
Tell them about the Gospel..  

38. So let me ask you, What if God asked you this "Why should I not send you to 
hell for all the sins you've done", how would you answer?  
should be the same answer as for Q21. If it's not the same answer as Q21 you may need to refer 
to analogies again in Q10. 

39. Now, remember at the beginning of this chat, what DID you think was 
getting you to heaven?  
Doing good/asking for forgiveness etc.   

If they answer with "Because Jesus died for my sins", you may need to remind them at the start they 
weren't pointing to their actions (if they were) and ask them to remind you of why we get to heaven 
again. 
So, since you were trusting in yourself to get you to heaven, if you had died 
before this chat, where would you have ended up?  
Hell..  

If they say heaven, ask them "But what should we be trusting in as the ONLY reason we go to heaven?" 
…Jesus. "So, you weren't trusting in Jesus but in your own actions and by trusting in your own actions 
where would you have gone?" ... hell 

39. But if you died right now, where will you end up?  
Heaven..  

If they still think hell, then ask them why and see what they are still trusting in to get them to heaven..  

So awesome you understand all this, if you'd like to see some more awesome 
stuff, check us out on the social media platforms: needgod.net (press Socials button)  

Do you have any other questions I can help you with?  

This has been a fantastic chat! My name is …… been great chatting with you.  
"""
        self.parse_script(embedded_content)
    
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
        
        # Special handling for question 1 - "heaven and hell" should go to special flow
        if current_q == 1 and ("heaven" in answer_lower and "hell" in answer_lower):
            return "heaven_question"
        
        # Special handling for question 1 - "reincarnation" or other theories should go to Q2
        if current_q == 1 and ("reincarnation" in answer_lower or "other" in answer_lower or "not sure" in answer_lower):
            return 2
        
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
    
    # Ensure current_question is always a number
    if not isinstance(st.session_state.current_question, (int, float)):
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
        if total_questions > 0 and isinstance(st.session_state.current_question, (int, float)):
            try:
                progress = st.session_state.current_question / total_questions
                st.progress(progress)
                st.write(f"Question {st.session_state.current_question} of {total_questions}")
                
                # Show question list
                st.subheader("📋 All Questions")
                for q_num in sorted(script_flow.script_data["questions"].keys()):
                    status = "🟢" if q_num == st.session_state.current_question else "⚪"
                    if isinstance(st.session_state.current_question, (int, float)) and q_num < st.session_state.current_question:
                        status = "✅"
                    st.write(f"{status} Q{q_num}")
            except (TypeError, ZeroDivisionError):
                st.write("Progress calculation error - starting fresh")
                st.session_state.current_question = 1
        else:
            st.write("Loading questions...")
    
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
        if isinstance(next_q, str):
            st.success(f"✅ Answer recorded. Moving to special response.")
        else:
            st.success(f"✅ Answer recorded. Moving to Question {next_q}.")
    else:
        st.success("✅ Answer recorded. Conversation complete!")
    
    st.rerun()

if __name__ == "__main__":
    main()

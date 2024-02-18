import os
import sys
import subprocess
import re
import uuid

# Get the directory of your script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_p_dir = os.path.dirname(parent_dir)

sys.path.append(parent_p_dir)

from database.database import db, Segments, Session, Dialogue
from app import app
from dotenv import load_dotenv
from gpt_engine.request import process_gpt_response

load_dotenv()

# speech2video.py
class ASR_Engine:
    def get_response_transcription(self, path: str, session_id: str):
        from openai import OpenAI
        client = OpenAI()

        audio_file= open(path, "rb")
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        
        with app.app_context():
            human_response = Dialogue(
                id=str(uuid.uuid4()), 
                session_id=session_id,
                text=transcript.text,
                is_human=True,
            )
            db.session.add(human_response)
            db.session.commit()
        
        return transcript.text
    
    
    def generate_new_question(self, session_id: str):
        job_position, job_description = "SWE Engineer", "Cadence: Currently pursuing MS degree in CE, EE, CS or equivalent with courses in design/verification using Verilog"
        previous_conversation = "  Interviewer: 'Can you give us a detailed example of a time when you led your team through a challenging project with a very tight deadline?' Candidate: Absolutely. Last year, I was leading a project aimed at developing a new encryption feature for our companys flagship messaging app, SecureTalk. The feature was critical for the next version release, scheduled for the end of Q2, to ensure compliance with new data protection regulations. We had exactly six weeks to go from concept to deployment, which was a significantly shorter timeline than usual for such a complex feature."
        
        Job = {
            "job_position": job_position,
            "job_description": job_description,
            "previous_conversation": previous_conversation
        }
        
        response = process_gpt_response(prompt_name = "amazon_interview", user_input=Job, required_fields={})
        
        dialogue_id = -1
        
        with app.app_context():
            ai_response = Dialogue(
                id=str(uuid.uuid4()),  
                session_id=session_id,
                text=response[0],
                is_human=False,
            )
            dialogue_id = ai_response.id
            db.session.add(ai_response)
            db.session.commit()
        
        return {
            "content": response[0],
            "dialogue_id": dialogue_id,
        }
        

if __name__ == "__main__":
    a = ASR_Engine()
    print(a.get_response_transcription("/root/src/flask_src/cache/response/test.mp3", "123"))
    print(a.generate_new_question("123"))
    
    
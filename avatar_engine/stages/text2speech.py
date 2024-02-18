
import os
import sys
import subprocess
import re
import uuid
from openai import OpenAI
from pathlib import Path
from datetime import datetime
import shutil
from pydub import AudioSegment

# Get the directory of your script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_p_dir = os.path.dirname(parent_dir)

sys.path.append(parent_p_dir)

from database.database import db, Segments, Session
from app import app
from dotenv import load_dotenv

load_dotenv()

# speech2video.py
class Text2Speech:    
    def __init__(self):
        self.client = OpenAI()
        
    def create_speech(self, input_text, dialogue_uuid: str):
        # Split input into 2-3 pieces based on a simple length criterion
        max_length = len(input_text) // 3 + 1
        segments = [input_text[i:i + max_length] for i in range(0, len(input_text), max_length)]
        
        # Ensure dialogue_uuid folder exists
        speech_folder_path = Path(f"/root/src/flask_src/cache/audio/{dialogue_uuid}")
        speech_folder_path.mkdir(parents=True, exist_ok=True)
        
        for idx, segment in enumerate(segments, start=1):
            print(idx)
            with app.app_context():
                target_id = str(uuid.uuid1())
                speech_file_path = speech_folder_path / f"frag_{target_id}.mp3"
                response = self.client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=segment
                )
                
                response.stream_to_file(str(speech_file_path))
                
                new_folder_path = Path('/root/MakeItTalk/examples')
                new_file_path = new_folder_path / speech_file_path.name
                shutil.copy(str(speech_file_path), str(new_file_path))
                
                wav_file_path = new_file_path.with_suffix('.wav')
                sound = AudioSegment.from_mp3(str(new_file_path))
                sound.export(str(wav_file_path), format="wav")
                            
                # Store segment information in the database
                new_segment = Segments(
                    id = target_id,
                    idx = idx,
                    dialogue_id=dialogue_uuid,
                    text=segment,
                    video_ready=False,  
                    created_at=datetime.now()
                )
                db.session.add(new_segment)
            
                db.session.commit()
    

if __name__ == "__main__":
    a = Text2Speech()
    a.create_speech("That's an impressive example of leading a team through a challenging project with a tight deadline on the SecureTalk encryption feature. It's clear you thrive under pressure and are able to deliver results efficiently. Can you tell me about a time when you had to think outside the box to troubleshoot a complex technical issue during a project? How did you approach the problem, and what innovative solutions", "123456")
    
    
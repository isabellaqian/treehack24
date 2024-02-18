
import os
import sys
import subprocess
import re
from pathlib import Path
import shutil

# Get the directory of your script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_p_dir = os.path.dirname(parent_dir)

sys.path.append(parent_p_dir)

from database.database import db, Segments, Session
from app import app

# speech2video.py
class SpeechEngine:
    # Get next uuid of segment to turn it into the video
    def priority_scheduler(self) -> str:
        with app.app_context():
            oldest_segment = Segments.query.filter(Segments.video_ready == False).order_by(Segments.created_at).first()
        
        return oldest_segment
    
    def get_gpu_memory_usage(self):
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')

        memory_usage_values = re.findall(r'\d+', output)
        memory_usage_values = [int(x) for x in memory_usage_values]  # Convert string to int
        return memory_usage_values

    def process_single_fragment(self):
        memory_usage_values = self.get_gpu_memory_usage()
        item = self.priority_scheduler()
        
        if memory_usage_values and memory_usage_values[0] < 1024 and item != None:  # Check if less than 1GB
            print("GPU memory usage is less than 1GB, running the command.")
            print(f"Convert {item.id}")
            with app.app_context():
                segment = Segments.query.filter(Segments.id == item.id).first()
                segment.video_ready = True
                db.session.commit()
                
            subprocess.run(
                ['python', 'main_end2end.py', '--jpg', 'scarlett.jpg', '--audio', f"frag_{item.id}.wav"],
                cwd='/root/MakeItTalk'
            )
            
            source_dir = Path("/root/MakeItTalk/examples")
        
            base_destination_path = Path(f"/root/src/flask_src/cache/avatar_video/{item.dialogue_id}")
            base_destination_path.mkdir(parents=True, exist_ok=True)

            # Now directly using item_id in the search without compiling a new pattern each time
            for file_path in source_dir.iterdir():
                if file_path.is_dir():
                    continue

                expected_filename = f"scarlett_pred_fls_frag_{item.id}"
                if expected_filename in file_path.name:                    
                    destination_file_path = base_destination_path / file_path.name
                    shutil.move(str(file_path), str(destination_file_path))
                    print(f"Moved {file_path} to {destination_file_path}")

        else:
            print("GPU memory usage is 1GB or more, not running the command.")
    

if __name__ == "__main__":
    a = SpeechEngine()
    item = a.priority_scheduler()
    print(item)
    print(a.process_single_fragment())
    
    
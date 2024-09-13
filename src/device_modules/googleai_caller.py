import google.generativeai as genai
from configurations.config_dataclasses import UserCfg


class GoogleAICaller:
    def __init__(self, usercfg: UserCfg):
        # Public attributes
        self.GOOGLE_AI_ID = usercfg.google_ai_cfg.google_ai_id
        genai.configure(api_key=self.GOOGLE_AI_ID)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def get_new_workout(self):
        """Generates a workout using Gemini AI. The prompt is designed to produce a relevant workout."""
        prompt = """Generate a workout plan consisting of three weight lifting exercises.
        The plan should include the name of the exercise, the weight to lift, the number of sets to perform, and the number of repeitions in each set.
        
        Here's an example workout:
        
        Bench press: 80 kg. 3 sets, 5 repetions in each set.
        Shoulder press: 15 kg. 3 sets, 8 repetions in each set.
        Tricep extensions: 5 kg. 5 sets, 5 repetions in each set. 
        """
        return self.get_response(prompt=prompt)

import google.generativeai as genai
from configurations.config_dataclasses import UserCfg


class GoogleAICaller:
    def __init__(self, user_cfg: UserCfg):
        # Public attributes
        self.GOOGLE_AI_ID = user_cfg.google_ai_cfg.googleai_id
        genai.configure(api_key=self.GOOGLE_AI_ID)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

import google.generativeai as genai
from configurations.config_dataclasses import UserCfg
from device_modules.identity_manager import IdentityManager


class GoogleAICaller:
    def __init__(self, user_id: IdentityManager, usercfg: UserCfg):
        # Public attributes
        self.usercfg = usercfg
        self.user_id = user_id
        self.GOOGLE_AI_ID = usercfg.google_ai_cfg.google_ai_id
        genai.configure(api_key=self.GOOGLE_AI_ID)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def get_new_workout(self):
        """Generates a workout using Gemini AI. The prompt is designed to produce a relevant workout."""

        # Get past workouts from Google Calendar
        from device_modules.googlecalendar_manager import GcalendarManager

        gcm = GcalendarManager(user_id=self.user_id, usercfg=self.usercfg)
        last_workout = gcm.get_last_workout()

        # Handle the case for the first time generating a workout
        no_last_workout = False
        if last_workout is None or last_workout == "":
            no_last_workout = True

        # Identify the type of the most recent workout (push OR pull) by similarity search with database
        # For now, similarity is measured by keyword frequency counts. A cosine similarity metric from a vector embedding would be more sophisticated.
        if not no_last_workout:
            import json

            db_path = "src/exercises.json"
            with open(db_path) as f:
                exercise_db = json.load(f)
            push_score, pull_score = 0, 0
            for kw in exercise_db["push"]:
                push_score += last_workout.count(kw)
            for kw in exercise_db["pull"]:
                pull_score += last_workout.count(kw)
            if push_score > pull_score:
                workout_type = "push"
            else:
                workout_type = "pull"
        else:
            workout_type = "push"
        # Retrieve user's strength information to provide as context to LLM
        bp_weight = self.usercfg.baseline_weights_cfg.bp_weight
        sq_weight = self.usercfg.baseline_weights_cfg.sq_weight
        dl_weight = self.usercfg.baseline_weights_cfg.dl_weight

        # Build prompt
        prompt = "Generate a workout plan incorporating three weight lifting exercises. The plan should include the name of the exercise, the weight to lift, the number of sets to perform, and the number of repeitions in each set."
        prompt += f" The workout should be a {workout_type}-type workout, meaning that it should incorporate exercises that require {workout_type}ing motions."
        prompt += f""" For context, the following are reasonable weights for some example exercises:
            Bench Press: {bp_weight} kg.
            Squat: {sq_weight} kg.
            Deadlift: {dl_weight} kg."""
        prompt += """
        Here's an example workout:

        Bench press: 80 kg. 3 sets, 5 repetions in each set.
        Shoulder press: 15 kg. 3 sets, 8 repetions in each set.
        Tricep extensions: 5 kg. 5 sets, 5 repetions in each set.
        """

        return self.get_response(prompt=prompt)

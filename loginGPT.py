import openai

class GPT2:
    def __init__(self, api_key="YOUR-API-KEY-HERE", model="gpt-4o-mini"):
        openai.api_key = api_key
        self.model = model
    def chat(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Exercise advisor: 5-6 exercises with names and Exact number of reps, based on bmi given in form of PYTHON'S LIST OF LISTS, no other text, no ```python. Dont use curly \" for this."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    

    

import openai

class GPT2:
    def __init__(self, api_key="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", model="gpt-4o-mini"):
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
    

    
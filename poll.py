class Poll:
    """A simple poll class"""

    def __init__(self, id = -1, question = "How was your day?", answers = ["Good", "So so", "Bad"]):
        self.id = id
        self.question = question
        self.answers = answers

    def __str__(self):
        # answ = [f"{i+1}. {self.answers[i]}" for i in range(len(self.answers))]
        return f"Poll ID:\t{self.id}\nPoll question:\t{self.question}\nPoll answers:\n{self.answers}"

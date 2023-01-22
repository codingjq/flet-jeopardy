from requests import request
import html

class TriviaAPI:

    def __init__(self, url=""):
        self.url = url
        self.raw_data = None
        self.data = None
        self.number_of_questions = None

    def set_url(self, url):
        self.url = url

    def initialize_api(self, category:str, difficulty:int=2, num_questions:str|int=5, type_question="multiple"):
        
        num_questions = str(num_questions)
        categories = {
                "Mythology": "20",
                "Sports": "21",
                "History": "23",
                "Politics": "24",
                "Art": "25",
                "Animals": "27"
                }
        difficulties = {
            1: "easy",
            2: "medium",
            3: "hard"
        }   
        self.set_url(f"https://opentdb.com/api.php?amount={num_questions}&category={categories[category]}&difficulty={difficulties[difficulty]}&type=multiple")
        self.get_data()

    def get_data(self):
        raw_data = request("GET", self.url).json()
        self.raw_data = raw_data
        self.data = raw_data["results"]
        self.number_of_questions = len(self.data)

    def get_question(self, number:int):
        return html.unescape(self.data[number]["question"])

    def get_answer(self, number:int):
        return html.unescape(self.data[number]["correct_answer"])

    def get_category(self, number:int):
        return html.unescape(self.data[number]["category"])

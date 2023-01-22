import flet as ft
from apis.trivia_getter import TriviaAPI
from math import floor

class ClueBox(ft.UserControl):
    __states = ["hidden", "value", "clue", "question", "complete"]
    __money_text_color = ft.colors.YELLOW_800
    __clue_text_color = ft.colors.WHITE
    __money_font_size = 26
    __clue_font_size = 12
    __font_family = "Arial"

    def __init__(self, value:str, answer:str, question:str, category:bool=False):
        super().__init__()
        ## Question Box
        self.width = floor(133.33-5)
        self.height = floor(self.width/1.6)
        self.bgColor = ft.colors.BLUE_900
        self.category = category
        self.state = "value"

        ## Clue 
        self.__font_color = self.__money_text_color
        self.__font_size = self.__money_font_size
        self.__value = value
        self.__answer = answer
        self.__question = question
        self.__current_display = ""


    def build(self):
        if self.category == True:
            return ft.Container(
                content=self.clue_text(),
                width=self.width,
                height=self.height,
                bgcolor=self.bgColor,
                border=ft.border.all(
                        width=2, 
                        color=ft.colors.BLACK,
                        ),
                border_radius=0,
                alignment=ft.alignment.center,
                on_click=self.handle_click,
                opacity=0
                )

        return ft.Container(
                content=self.value_text(),
                width=self.width,
                height=self.height,
                bgcolor=self.bgColor,
                border=ft.border.all(
                        width=2, 
                        color=ft.colors.BLACK,
                        ),
                border_radius=0,
                alignment=ft.alignment.center,
                on_click=self.handle_click,
                opacity=0
                )
        

    def did_mount(self):
        clue_box = self.controls[0]
        clue_box.opacity = 0
        clue_box.animate_opacity = ft.animation.Animation(900, "easeIn")
        clue_box.update()

        def animate_opacity():
            from time import sleep
            sleep(0.05)
            clue_box.opacity = 1
            clue_box.update()
        animate_opacity()
    
        return super().did_mount()

    
        
    def handle_click(self, e):
        match self.state:
            case "value":
                self.set_state("question", e)
            case "question":
                self.set_state("clue", e)
            case _:
                self.set_state("complete", e)
        self.update()

    def value_text(self):
        return ft.Text(
                self.__value, 
                color=self.__money_text_color,
                font_family=self.__font_family,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                size=self.__money_font_size)

    def clue_text(self):
        return ft.Text(
                self.__answer, 
                color=self.__clue_text_color,
                font_family=self.__font_family,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                size=self.__clue_font_size)

    def question_text(self):
        return ft.Text(
                self.__question, 
                color=self.__clue_text_color,
                font_family=self.__font_family,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                size=self.__clue_font_size)

    def complete_text(self):
        return ft.Text("")

    def set_state(self, state, e):
            if type(state) == str:
                try:
                    self.state = self.__states[self.__states.index(state)]
                except Exception as e: 
                    print(e + "\n" + "invalid state string")
            if type(state) == int:
                try:
                    self.state = self.__states[state]
                except Exception as err: 
                    print(err + "\n" + "invalid state integer")
            match self.state:
                case "hidden":
                    e.control.content = self.complete_text()
                    e.control.bgcolor = ft.colors.BLACK
                case "value":
                    e.control.content = self.value_text()
                    e.control.bgcolor = self.bgColor
                case "clue":
                    e.control.content = self.clue_text()
                    e.control.bgcolor = self.bgColor
                case "question":
                    e.control.content = self.question_text()
                    e.control.bgcolor = self.bgColor
                case "complete":
                    e.control.content = self.complete_text()
                    e.control.bgcolor = self.bgColor  
                case _:
                    print("something wrong with set state") 
            self.font_sizer(e)


    def font_sizer(self, e):
        if len(e.control.content.value) > 65:
            e.control.content.size = 8
            return self.update()
        if len(e.control.content.value) > 50:
            e.control.content.size = 10
            self.update()

class ClueCategory:
    def __init__(self, api):
        self.api = api
        self.category = self.build_column()

    def build_column(self):
        boxes = []
        for i in range(0,6):
            if i == 0:
                boxes.append(ClueBox(self.api.get_category(i), self.api.get_category(i),self.api.get_category(i), True))
            else:
                boxes.append(ClueBox("$"+str(i*200), self.api.get_answer(i-1), self.api.get_question(i-1)))
        return boxes
        
class GameBoard:
    def __init__(self):
        self.game_board = self.build_game()

    def build_game(self):
        subjects = [
            "Politics",
            "Sports",
            "History",
            "Animals",
            "Mythology",
            "Art",
            
        ]

        columns = []
        for subject in subjects:
            api = TriviaAPI()
            api.initialize_api(subject)
            column = ClueCategory(api)
            columns.append(ft.Column(column.category, spacing=1))
        return columns



if __name__ == "__main__":
    def main(page: ft.Page):
        
        page.title = "Quiz Show"
        page.theme_mode = "light"
        page.window_width = 800
        page.window_height = 600
        page.bgcolor = ft.colors.BLACK
    
        clue_box = ClueBox("200", "Home of the Lincoln, Washington and Jefferson Memorials.", 
                            "What is Washington D.C.?")

        page.add(
            clue_box
        )

    ft.app(target=main)
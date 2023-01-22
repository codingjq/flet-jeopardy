import flet as ft

from user_controls.quiz_game import GameBoard

def main(page: ft.Page):

    page.theme_mode = "light"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = "black"


    header = ft.Text("Quiz Show", color="white", size=26, weight=ft.FontWeight.BOLD)
    game = GameBoard()

    quiz = ft.Column([
        ft.Row([header], alignment="center"),
        ft.Row(game.game_board, spacing=0)
    ])

    page.add(
        quiz
    )

    page.go('/')


ft.app(target=main, assets_dir="assets")
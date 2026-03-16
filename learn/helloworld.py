import flet as ft

def main(page: ft.Page):
    page.title = "Hello World"
    page.add(ft.Text("Hello World!"))

ft.app(target=main)
import flet as ft

def main(page: ft.Page):
    page.title = "我的第一个Flet应用"
    #创建文本框
    text_field = ft.TextField(label="请输入文本")

    #创建按钮点击事件
    def button_click(e):
        page.add(ft.Text(f"你输入的内容是: {text_field.value}"))

    #创建按钮
    submit_button = ft.ElevatedButton(content="提交", on_click=button_click)
    page.add(text_field, submit_button)


ft.app(target=main)
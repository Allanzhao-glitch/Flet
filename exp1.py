import flet as ft

def main(page: ft.Page):  #函数接收一个类型为 ft.Page 的参数 page，这是 Flet 框架中的页面对象
    page.title = "Hello, Flet!"     #将应用窗口的标题设置为 "Hello, Flet!"
    page.add(ft.Text("Welcome to Flet!")) #向页面添加一个文本控件，显示 "Welcome to Flet!" 文本

ft.app(target=main)  
'''
调用 ft.app() 函数启动应用，并将 main 函数作为 target 参数传递
这告诉 Flet 框架，当应用启动时，执行 main 函数来初始化界面
'''
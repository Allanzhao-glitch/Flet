# 一、第一个Flet程序

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Hello World"
    page.add(ft.Text("Hello World!"))

ft.app(target=main)
```

![](C:\Users\Allan\AppData\Roaming\marktext\images\2026-03-16-11-23-14-image.png)

import os
import flet as ft

def convert_encoding(file_path, from_encoding, to_encoding):
    try:
        #读取文件内容
        with open(file_path, 'r', encoding=from_encoding) as file:
            content = file.read()
        
        #写入文件内容
        with open(file_path, 'w', encoding=to_encoding) as file:
            file.write(content)

        return f"文件 {file_path} 的编码已成功从 {from_encoding} 转换为 {to_encoding}"
    except Exception as e:
        return f"转换 {file_path} 时出错：{str(e)}"
    


def batch_convert(folder_path, from_encoding, to_encoding):
    if not os.path.isdir(folder_path):
        return f"无效的文件夹路径: {folder_path}"
    
    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):  # 只转换 .txt 文件
                file_path = os.path.join(root, file)
                result = convert_encoding(file_path, from_encoding, to_encoding)
                results.append(result)
    return results

def main(page: ft.Page):
    page.title = "文件编码转换工具"
    folder_input = ft.TextField(label="选择文件夹路径", width=400)
    from_encoding_select = ft.Dropdown(label="选择源编码", options=[
        ft.dropdown.Option("gbk"),
        ft.dropdown.Option("utf-8"),
        ft.dropdown.Option("iso-8859-1")
    ], value="gbk")
    to_encoding_select = ft.Dropdown(label="选择目标编码", options=[
        ft.dropdown.Option("utf-8"),
        ft.dropdown.Option("gbk"),
        ft.dropdown.Option("iso-8859-1")
    ], value="utf-8")



    result_area = ft.Column()

    def on_convert_click(e):
        folder_path = folder_input.value
        from_encoding = from_encoding_select.value
        to_encoding = to_encoding_select.value

        results = batch_convert(folder_path, from_encoding, to_encoding)
            # 清空结果区域
        result_area.controls.clear()
            # 显示结果
        for result in results:
            result_area.controls.append(ft.Text(result))
        page.update()


    convert_button = ft.ElevatedButton(content="转换编码", on_click=on_convert_click)
    # 将组件添加到页面
    page.add(
        folder_input,
        from_encoding_select,
        to_encoding_select,
        convert_button,
        result_area
    )



ft.app(target=main)
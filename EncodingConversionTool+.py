import os
import flet as ft
from flet import FilePicker, FilePickerUploadEvent  # 显式导入需要的类

def convert_encoding(file_path, from_encoding, to_encoding):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding=from_encoding) as file:
            content = file.read()
        
        # 写入文件内容
        with open(file_path, 'w', encoding=to_encoding) as file:
            file.write(content)

        return f"✅ 文件 {os.path.basename(file_path)} 的编码已成功从 {from_encoding} 转换为 {to_encoding}"
    except Exception as e:
        return f"❌ 转换 {os.path.basename(file_path)} 时出错：{str(e)}"

def batch_convert(folder_path, from_encoding, to_encoding):
    if not os.path.isdir(folder_path):
        return [f"❌ 无效的文件夹路径: {folder_path}"]
    
    results = []
    converted_count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):  # 只转换 .txt 文件
                file_path = os.path.join(root, file)
                result = convert_encoding(file_path, from_encoding, to_encoding)
                results.append(result)
                converted_count += 1
    
    if converted_count == 0:
        results.append("⚠️ 未找到任何 .txt 文件")
    else:
        results.insert(0, f"📊 共转换 {converted_count} 个文件")
    
    return results

def main(page: ft.Page):
    page.title = "文件编码转换工具"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # 显示选中文件夹路径的文本框（现在只读）
    folder_input = ft.TextField(
        label="已选择的文件夹路径", 
        width=500,
        read_only=True,
        hint_text="请点击'选择文件夹'按钮选择文件夹"
    )
    
    # 创建文件选择器 - 使用更通用的方式
    def pick_folder_result(e):
        if e.path:
            folder_input.value = e.path
            folder_input.update()
    
    # 创建 FilePicker 实例
    pick_folder_dialog = ft.FilePicker(on_upload=pick_folder_result)
    page.overlay.append(pick_folder_dialog)
    
    # 选择文件夹按钮
    select_folder_btn = ft.ElevatedButton(
        content="📁 选择文件夹",

        on_click=lambda _: pick_folder_dialog.get_directory_path()
    )
    
    # 文件夹路径行
    folder_row = ft.Row(
        [select_folder_btn, folder_input],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )
    
    # 源编码选择
    from_encoding_select = ft.Dropdown(
        label="选择源编码",
        options=[
            ft.dropdown.Option("gbk"),
            ft.dropdown.Option("utf-8"),
            ft.dropdown.Option("utf-8-sig"),  # 带BOM的UTF-8
            ft.dropdown.Option("iso-8859-1"),
            ft.dropdown.Option("big5"),
            ft.dropdown.Option("shift_jis"),
        ],
        value="gbk",
        width=200
    )
    
    # 目标编码选择
    to_encoding_select = ft.Dropdown(
        label="选择目标编码",
        options=[
            ft.dropdown.Option("utf-8"),
            ft.dropdown.Option("utf-8-sig"),  # 带BOM的UTF-8
            ft.dropdown.Option("gbk"),
            ft.dropdown.Option("iso-8859-1"),
            ft.dropdown.Option("big5"),
            ft.dropdown.Option("shift_jis"),
        ],
        value="utf-8",
        width=200
    )
    
    # 进度指示器
    progress_bar = ft.ProgressBar(width=500, visible=False)
    progress_text = ft.Text("")
    
    # 结果显示区域
    result_area = ft.Column(scroll=ft.ScrollMode.AUTO, height=300)
    
    # 转换按钮点击事件
    def on_convert_click(e):
        if not folder_input.value:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("请先选择文件夹！")))
            return
        
        # 显示进度
        progress_bar.visible = True
        progress_text.value = "正在转换中..."
        result_area.controls.clear()
        page.update()
        
        folder_path = folder_input.value
        from_encoding = from_encoding_select.value
        to_encoding = to_encoding_select.value
        
        # 执行转换
        results = batch_convert(folder_path, from_encoding, to_encoding)
        
        # 显示结果
        for result in results:
            # 根据结果类型设置不同颜色
            if result.startswith('✅'):
                color = ft.colors.GREEN
            elif result.startswith('❌'):
                color = ft.colors.RED
            else:
                color = ft.colors.BLUE
            result_area.controls.append(ft.Text(result, color=color))
        
        # 隐藏进度
        progress_bar.visible = False
        progress_text.value = f"转换完成！共处理 {len([r for r in results if r.startswith('✅')])} 个文件"
        page.update()
    
    # 转换按钮
    convert_button = ft.ElevatedButton(
        content="🔄 开始转换",

        on_click=on_convert_click,
    )
    
    # 清空按钮
    def on_clear_click(e):
        folder_input.value = ""
        result_area.controls.clear()
        progress_text.value = ""
        progress_bar.visible = False
        page.update()
    
    clear_button = ft.OutlinedButton(
        content="🗑️ 清空",

        on_click=on_clear_click
    )
    
    # 按钮行
    button_row = ft.Row(
        [convert_button, clear_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    # 将组件添加到页面
    page.add(
        ft.Text("文件编码批量转换工具", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        folder_row,
        ft.Divider(height=10),
        ft.Row([from_encoding_select, to_encoding_select], spacing=20),
        ft.Divider(height=20),
        button_row,
        progress_bar,
        progress_text,
        ft.Divider(height=20),
        ft.Text("转换结果:", size=16, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=result_area,

            border_radius=10,
            padding=10,
            height=300,
        )
    )
    
    # 页面更新
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
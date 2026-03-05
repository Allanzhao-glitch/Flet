import flet as ft
import serial
import serial.tools.list_ports
import threading
import time

class SeriaAssistant:
    def __init__(self):
        self.serial_port = None
        self.running = False
    
    def list_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def open_port(self, port, baudrate):
        try:
            self.serial_port = serial.Serial(port, baudrate,timeout=1)
            self.running = True
            return True,"串口打开成功"
        
        except Exception as e:
            return False,f"串口打开失败: {str(e)}"
        
    def close_port(self):
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.serial_port = None
            return True,"串口关闭成功"
        return False,"串口未打开"
    
    def send_data(self, data):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(data.encode('utf-8'))
            return True,"数据发送成功"
        return False,"串口未打开"

    def read_data(self):
        if self.serial_port and self.serial_port.is_open:
            if self.serial_port.in_waiting > 0:
                return self.serial_port.read(self.serial_port.in_waiting)
        return b""

def bytes_to_hex(byte_data):
    return ' '.join(f'{b:02x}' for b in byte_data)


# 列出所有可用的串口
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def main(page: ft.Page):
    page.title = "串口助手工具"
    print("可用的串口:",list_serial_ports())
    assistant = SeriaAssistant()
    ports = assistant.list_ports()

    port_dropdown = ft.Dropdown(label="选择串口", options=[ft.dropdown.Option(port) for port in ports])

    baudrate_input = ft.TextField(label="波特率", value="9600")

    send_input = ft.TextField(label="发送数据")


    read_output = ft.TextField(label="接收数据",
                                multiline=True,
                                min_lines=6,
                                max_lines=10,
                                height=200)
    # 状态栏，用于显示操作反馈
    status_bar = ft.Text("状态", size=15)
    def read_from_serial():
        while assistant.running:
            data = assistant.read_data()
            if data:
                try:
                    decoded_data = data.decode('utf-8')
                    read_output.value += decoded_data  # 更新接收数据
                except UnicodeDecodeError:
                    hex_data = bytes_to_hex(data)
                read_output.value += f"接收到的16进制数据: {hex_data}\n"
                page.update()  # 更新页面显示
        
        time.sleep(0.1)  # 避免CPU占用过高

    def on_open_click(e):
        port = port_dropdown.value
        baudrate = int(baudrate_input.value)
        success, msg = assistant.open_port(port, baudrate)
        status_bar.value = msg  # 更新状态栏内容
        page.update()  # 更新页面显示
        if success:
            threading.Thread(target=read_from_serial).start()
            page.update()
    def on_close_click(e):
        msg = assistant.close_port()
        status_bar.value = msg  # 更新状态栏内容
        page.update()  # 更新页面显示

    def on_send_click(e):
        data = send_input.value
        msg = assistant.send_data(data)
        status_bar.value = msg  # 更新状态栏内容
        send_input.value = ""
        page.update()

    open_button = ft.ElevatedButton(content="打开串口", on_click=on_open_click)
    close_button = ft.ElevatedButton(content="关闭串口", on_click=on_close_click)
    send_button = ft.ElevatedButton(content="发送", on_click=on_send_click)

    page.add(
        port_dropdown,
        baudrate_input,
        open_button,
        close_button,
        send_input,
        send_button,
        read_output,
		status_bar  # 添加状态栏
    )



ft.app(target=main)
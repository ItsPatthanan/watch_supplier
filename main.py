import PySimpleGUI as sg

def create_gui_layout():
    layout = [
        [sg.Text('รหัสสินค้า'), sg.InputText(key='prod_id')],
        [sg.Text('ชื่อสินค้า'), sg.InputText(key='part_name')],
        [sg.Text('จำนวนคงคลัง'), sg.InputText(key='qty')],
        [sg.Text('ราคา'), sg.InputText(key='price')],
        [sg.Button('เพิ่มสินค้า'), sg.Button('ค้นหาสินค้า'), sg.Button('แก้ไขสินค้า'), sg.Button('ลบสินค้า')],
        [sg.Table(values=[], headings=['รหัสสินค้า', 'ชื่อสินค้า', 'จำนวนคงคลัง', 'ราคา'], auto_size_columns=False,
                  justification='right', key='table', enable_events=True)],
        [sg.Button('ออก')],
    ]
    return layout

def main():
    sg.theme('LightGreen')
    window = sg.Window('ระบบคลังสินค้า', create_gui_layout(), resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'ออก':
            break

    window.close()

if __name__ == '__main__':
    main()

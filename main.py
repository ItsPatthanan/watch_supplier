import PySimpleGUI as sg
import pandas as pd
import os

# กำหนดโครงสร้างข้อมูลใน DataFrame
columns = ['prod_id', 'part_name', 'price', 'qty']
file_path = os.path.join(os.getcwd(), 'inventory.xlsx')

# ตรวจสอบว่ามีไฟล์ inventory.xlsx อยู่หรือไม่
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=columns)
# สร้าง GUI
sg.theme('Dark Blue17')
layout = [
    [sg.Text('ระบบคลังสินค้า', font=('Helvetica', 20))],
    [sg.Button('เพิ่มสินค้า'), sg.Button('ค้นหาสินค้า'), sg.Button('แก้ไขข้อมูลสินค้า'), sg.Button('ลบข้อมูลสินค้า')],
    [sg.Table(values=df.values.tolist(), headings=columns, auto_size_columns=False, justification='right',
              key='-TABLE-', display_row_numbers=False, col_widths=[10, 20, 10, 10])],
]
window = sg.Window('Inventory System', layout)

def add_product(values):
    global df

    # ตรวจสอบข้อมูลไม่ครบ
    if not all(values.values()):
        sg.popup_error('กรุณากรอกข้อมูลให้ครบทุกช่อง')
        return

    new_prod_id = values['prod_id']

    # ตรวจสอบว่า ID ซ้ำหรือไม่
    if new_prod_id in df['prod_id'].values:
        sg.popup_error('รหัสสินค้านี้มีอยู่แล้ว กรุณาใส่รหัสสินค้าที่ไม่ซ้ำกัน')
        return

    new_product = pd.DataFrame([values], columns=columns)
    df = pd.concat([df, new_product], ignore_index=True)

    try:
        df.to_excel(file_path, index=False)
        window['-TABLE-'].update(values=df.values.tolist())
        sg.popup('บันทึกสินค้าเรียบร้อยแล้ว!')
    except (ValueError, FileNotFoundError):
        sg.popup_error('กรุณากรอกข้อมูลที่ถูกต้อง')

def search_product(search_term):
    global df
    # Convert relevant columns to strings before using .str.contains
    string_columns = ['prod_id', 'part_name']
    df[string_columns] = df[string_columns].astype(str)

    result_df = df[(df['prod_id'] == search_term) | (df['part_name'] == search_term)]
    # Select only specific columns for display
    result_df = result_df[['prod_id', 'part_name', 'price', 'qty']]
    return result_df
def update_product(values):
    global df
    prod_id = values['prod_id']
    update_mask = df['prod_id'] == prod_id
    df.loc[update_mask, ['part_name', 'price', 'qty']] = values['part_name'], values['price'], values['qty']
    df.to_excel(file_path, index=False)
    window['-TABLE-'].update(values=df.values.tolist())
    sg.popup('แก้ไขข้อมูลสินค้าเรียบร้อยแล้ว!')

def delete_product(prod_id):
    global df
    df = df[df['prod_id'] != prod_id]
    df.to_excel(file_path, index=False)
    window['-TABLE-'].update(values=df.values.tolist())
    sg.popup('ลบข้อมูลสินค้าเรียบร้อยแล้ว!')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'เพิ่มสินค้า':
        add_layout = [
            [sg.Text('รหัสสินค้า:'), sg.Input(key='prod_id')],
            [sg.Text('ชื่อสินค้า:'), sg.Input(key='part_name')],
            [sg.Text('ราคา:'), sg.Input(key='price')],
            [sg.Text('จำนวนคงคลัง:'), sg.Input(key='qty')],
            [sg.Button('บันทึก'), sg.Button('ยกเลิก')]
        ]
        add_window = sg.Window('เพิ่มสินค้า', add_layout)

        while True:
            add_event, add_values = add_window.read()

            if add_event == sg.WIN_CLOSED or add_event == 'ยกเลิก':
                add_window.close()
                break
            elif add_event == 'บันทึก':
                add_product(add_values)
                add_window.close()

    elif event == 'ค้นหาสินค้า':
        search_layout = [
            [sg.Text('ค้นหา (รหัสสินค้า หรือ ชื่อสินค้า):'), sg.Input(key='search_term')],
            [sg.Button('ค้นหา'), sg.Button('ยกเลิก')]
        ]
        search_window = sg.Window('ค้นหาสินค้า', search_layout)
        while True:
            search_event, search_values = search_window.read()
            if search_event == sg.WIN_CLOSED or search_event == 'ยกเลิก':
                break
            elif search_event == 'ค้นหา':
                if not search_values['search_term']:
                    sg.popup_error('กรุณากรอกข้อมูลค้นหา')
                    continue
                result = search_product(search_values['search_term'])
                if result.empty:
                    sg.popup_error('ไม่พบข้อมูลสินค้าที่ค้นหา')
                    continue
                # Convert DataFrame to string without index
                result_str = result.to_string(index=False)
                sg.popup(result_str)
                search_window.close()

    elif event == 'แก้ไขข้อมูลสินค้า':
        update_layout = [
            [sg.Text('รหัสสินค้าที่ต้องการแก้ไข:'), sg.Input(key='prod_id')],
            [sg.Text('ชื่อสินค้า:'), sg.Input(key='part_name')],
            [sg.Text('ราคา:'), sg.Input(key='price')],
            [sg.Text('จำนวนคงคลัง:'), sg.Input(key='qty')],
            [sg.Button('บันทึก'), sg.Button('ยกเลิก')]
        ]
        update_window = sg.Window('แก้ไขข้อมูลสินค้า', update_layout)

        while True:
            update_event, update_values = update_window.read()

            if update_event == sg.WIN_CLOSED or update_event == 'ยกเลิก':
                break
            elif update_event == 'บันทึก':
                update_product(update_values)
                update_window.close()

    elif event == 'ลบข้อมูลสินค้า':
        delete_layout = [
            [sg.Text('รหัสสินค้าที่ต้องการลบ:'), sg.Input(key='delete_prod_id')],
            [sg.Button('ลบ'), sg.Button('ยกเลิก')]
        ]
        delete_window = sg.Window('ลบข้อมูลสินค้า', delete_layout)

        while True:
            delete_event, delete_values = delete_window.read()

            if delete_event == sg.WIN_CLOSED or delete_event == 'ยกเลิก':
                break
            elif delete_event == 'ลบ':
                delete_product(delete_values['delete_prod_id'])
                delete_window.close()

window.close()

import PySimpleGUI as sg
import pandas as pd

def get_next_prod_id():
    try:
        df = pd.read_excel('inventory.xlsx')
        if not df.empty:
            return df['prod_id'].max() + 1
        else:
            return 1
    except FileNotFoundError:
        return 1

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
    window = sg.Window('ระบบคลังสินค้า', create_gui_layout(), resizable=True, finalize=True)

    update_table(window)  # อัปเดต Table เมื่อโปรแกรมเริ่มต้น

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'ออก':
            break
        elif event == 'เพิ่มสินค้า':
            add_product(values)
            update_table(window)
        elif event == 'ค้นหาสินค้า':
            search_product(values)
        elif event == 'แก้ไขสินค้า':
            edit_product(values)
            update_table(window)
        elif event == 'ลบสินค้า':
            delete_product(values)
            update_table(window)

    window.close()

def add_product(values):
    data = {'prod_id': [values['prod_id']],
            'part_name': [values['part_name']],
            'qty': [values['qty']],
            'price': [values['price']]}
    df = pd.DataFrame(data)

    try:
        existing_df = pd.read_excel('inventory.xlsx')
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df

    updated_df.to_excel('inventory.xlsx', index=False)

def search_product(values):
    try:
        df = pd.read_excel('inventory.xlsx')
        result = df[(df['prod_id'] == values['prod_id']) | (df['part_name'] == values['part_name'])]
        sg.popup_ok('ผลลัพธ์การค้นหา:\n\n' + result.to_string(index=False))
    except FileNotFoundError:
        sg.popup_error('ไม่พบไฟล์ inventory.xlsx')

def edit_product(values):
    try:
        df = pd.read_excel('inventory.xlsx')
        index_to_edit = df.index[(df['prod_id'] == values['prod_id']) | (df['part_name'] == values['part_name'])].tolist()[0]

        column_to_edit = sg.popup_get_text('กรุณาเลือกคอลัมน์ที่ต้องการแก้ไข (prod_id, part_name, qty, price)')
        new_value = sg.popup_get_text('กรุณาใส่ค่าใหม่')

        df.at[index_to_edit, column_to_edit] = new_value
        df.to_excel('inventory.xlsx', index=False)

        sg.popup_ok('แก้ไขข้อมูลสินค้าเรียบร้อยแล้ว')
    except (FileNotFoundError, IndexError):
        sg.popup_error('ไม่พบข้อมูลสินค้าหรือข้อมูลที่ใส่ไม่ถูกต้อง')

def delete_product(values):
    try:
        df = pd.read_excel('inventory.xlsx')
        index_to_delete = df.index[(df['prod_id'] == values['prod_id']) | (df['part_name'] == values['part_name'])].tolist()[0]

        df = df.drop(index_to_delete)
        df.to_excel('inventory.xlsx', index=False)

        sg.popup_ok('ลบข้อมูลสินค้าเรียบร้อยแล้ว')
    except (FileNotFoundError, IndexError):
        sg.popup_error('ไม่พบข้อมูลสินค้าหรือข้อมูลที่ใส่ไม่ถูกต้อง')

def update_table(window):
    try:
        df = pd.read_excel('inventory.xlsx')
        window['table'].update(values=df.values.tolist())
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    main()
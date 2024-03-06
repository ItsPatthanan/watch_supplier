PySimpleGUI_License=''
import PySimpleGUI as sg
import pandas as pd
import os

columns = ['prod_id', 'part_name', 'category', 'price', 'qty']
file_path = os.path.join(os.getcwd(), 'inventory.csv')

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=columns)

P_font = ("prompt", 12)
H_font = ("prompt", 16, "bold")
input_w = 20
sg.theme('DarkBlue14')
btn_color_critical = "red"
btn_color_success = "green"
btn_color_warning = "orange"

frame_main = [
    [sg.HorizontalSeparator(color='red')],
    [sg.Button('เพิ่มสินค้า', font=P_font), sg.Button('ค้นหาสินค้า', font=P_font),
     sg.Button('แก้ไขข้อมูลสินค้า', font=P_font), sg.Button('ขายสินค้า', font=P_font, button_color=btn_color_warning),
     sg.Button('ลบข้อมูลสินค้า', font=P_font, button_color=btn_color_critical)],
    [sg.HorizontalSeparator(color='red')],
    [sg.Table(values=df.values.tolist(), headings=columns, auto_size_columns=False, justification='right',
              key='-TABLE-', display_row_numbers=False, col_widths=[10, 20, 10, 10, 10], font=P_font)]
]
frame_outline = [[sg.Frame('', frame_main, element_justification='center', border_width=0)]]
layout = [[sg.Frame('ระบบสต๊อกสินค้าอะไหล่นาฬิกา', frame_outline, font=H_font)]]
window = sg.Window('Watch spare parts', layout)

def add_product(values):
    global df
    if not all(values.values()):
        sg.popup_error('กรุณากรอกข้อมูลให้ครบทุกช่อง')
        return

    new_prod_id = values['prod_id']
    if new_prod_id in df['prod_id'].astype(str).values:
        sg.popup_error('รหัสสินค้านี้มีอยู่แล้ว กรุณาใส่รหัสสินค้าที่ไม่ซ้ำกัน')
        return

    new_product = pd.DataFrame([values], columns=columns)
    new_product['qty'] = new_product['qty'].astype(int)
    df = pd.concat([df, new_product], ignore_index=True)

    try:
        df['prod_id'] = df['prod_id'].astype(int)
        df = df.sort_values(by='prod_id')
        df.to_csv(file_path, index=False)
        update_table(window['-TABLE-'], df)
        sg.popup('บันทึกสินค้าเรียบร้อยแล้ว!')
    except (ValueError, FileNotFoundError):
        sg.popup_error('กรุณากรอกข้อมูลที่ถูกต้อง')
def search_product(search_term):
    global df
    string_columns = ['prod_id', 'part_name']
    df[string_columns] = df[string_columns].astype(str)
    result_df = df[(df['prod_id'] == search_term) | (df['part_name'] == search_term)]
    result_df = result_df[['prod_id', 'part_name', 'category', 'price', 'qty']]
    return result_df
def update_product(values):
    global df
    prod_id = values['prod_id']
    update_mask = df['prod_id'].astype(str) == prod_id
    if not update_mask.any():
        sg.popup_error('ไม่พบข้อมูลสินค้าที่ต้องการแก้ไข')
        return
    if any(value == '' for value in values.values()):
        sg.popup_error('กรุณากรอกข้อมูลให้ครบทุกช่อง')
        return
    part_name = str(values['part_name'])
    category = str(values['category'])
    price = int(values['price'])
    qty = int(values['qty'])
    df.loc[update_mask, ['part_name', 'category', 'price', 'qty']] = part_name, category, price, qty
    df = df.sort_values(by='prod_id')
    df.to_csv(file_path, index=False)
    update_table(window['-TABLE-'], df)
    sg.popup('แก้ไขข้อมูลสินค้าเรียบร้อยแล้ว!')
def delete_product(values):
    global df
    try:
        df = pd.read_csv(file_path)
        matching_rows = df['prod_id'].astype(str) == values['delete_prod_id']
        if matching_rows.any():
            index_to_delete = df.index[matching_rows].tolist()[0]
            df = df.drop(index_to_delete)
            df = df.sort_values(by='prod_id')
            df.to_csv(file_path, index=False)
            update_table(window['-TABLE-'], df)
            sg.popup_ok('ลบข้อมูลสินค้าเรียบร้อยแล้ว')
        else:
            sg.popup_error('ไม่พบข้อมูลสินค้าที่ต้องการลบ')
    except (FileNotFoundError, IndexError):
        sg.popup_error('ไม่พบข้อมูลสินค้าหรือข้อมูลที่ใส่ไม่ถูกต้อง')
def sell_product(values):
    global df
    try:
        prod_id = int(values['sell_prod_id'])
        qty_to_sell = int(values['sell_qty'])
        df = pd.read_csv(file_path)
        matching_rows = df['prod_id'] == prod_id
        if matching_rows.any():
            current_qty = df.loc[matching_rows, 'qty'].iloc[0]
            if qty_to_sell <= current_qty:
                new_qty = current_qty - qty_to_sell
                if new_qty > 0:
                    df.loc[matching_rows, 'qty'] = new_qty
                else:
                    df = df.drop(df.index[matching_rows])
                df = df.sort_values(by='prod_id')
                df.to_csv(file_path, index=False)
                update_table(window['-TABLE-'], df)
                sg.popup('การขายสินค้าเสร็จสิ้น!')
            else:
                sg.popup_error('จำนวนสินค้าไม่เพียงพอสำหรับการขาย')
        else:
            sg.popup_error('ไม่พบสินค้าที่ต้องการขาย')
    except ValueError:
        sg.popup_error('กรุณากรอกรหัสสินค้าและจำนวนที่ต้องการขายให้ถูกต้อง')
def update_table(table_elem, data_frame):
    table_elem.update(values=data_frame.values.tolist())

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'เพิ่มสินค้า':
        category_choices = ['part', 'automatic', 'quartz', 'strap']
        add_layout = [
            [sg.Text('รหัสสินค้า:', size=(15, 1)), sg.Input(key='prod_id', size=(input_w, 1))],
            [sg.Text('ชื่อสินค้า:', size=(15, 1)), sg.Input(key='part_name', size=(input_w, 1))],
            [sg.Text('หมวดหมู่:', size=(15, 1)), sg.Combo(category_choices, key='category', size=(input_w, 1))],
            [sg.Text('ราคา:', size=(15, 1)), sg.Input(key='price', size=(input_w, 1))],
            [sg.Text('จำนวนคงคลัง:', size=(15, 1)), sg.Input(key='qty', size=(input_w, 1))],
            [sg.Button('บันทึก', button_color=btn_color_success), sg.Button('ยกเลิก', button_color=btn_color_critical)]
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
            [sg.Text('ค้นหา (รหัสสินค้า หรือ ชื่อสินค้า):'), sg.Input(key='search_term', size=(input_w, 1))],
            [sg.Button('ค้นหา', button_color=btn_color_success), sg.Button('ยกเลิก', button_color=btn_color_critical)]
        ]
        search_window = sg.Window('ค้นหาสินค้า', search_layout)
        while True:
            search_event, search_values = search_window.read()
            if search_event == sg.WIN_CLOSED or search_event == 'ยกเลิก':
                search_window.close()
                break
            elif search_event == 'ค้นหา':
                if not search_values['search_term']:
                    sg.popup_error('กรุณากรอกข้อมูลค้นหา')
                    continue
                result = search_product(search_values['search_term'])
                if result.empty:
                    sg.popup_error('ไม่พบข้อมูลสินค้าที่ค้นหา')
                    continue
                result_str = result.to_string(index=False)
                sg.popup(result_str)
                search_window.close()

    elif event == 'แก้ไขข้อมูลสินค้า':
        category_choices = ['part', 'automatic', 'quartz', 'strap']
        update_layout = [
            [sg.Text('รหัสสินค้าที่ต้องการแก้ไข:', size=(15, 1)), sg.Input(key='prod_id', size=(input_w, 1))],
            [sg.Text('ชื่อสินค้า:', size=(15, 1)), sg.Input(key='part_name', size=(input_w, 1))],
            [sg.Text('หมวดหมู่:', size=(15, 1)), sg.Combo(category_choices, key='category', size=(input_w, 1))],
            [sg.Text('ราคา:', size=(15, 1)), sg.Input(key='price', size=(input_w, 1))],
            [sg.Text('จำนวนคงคลัง:', size=(15, 1)), sg.Input(key='qty', size=(input_w, 1))],
            [sg.Button('บันทึก', button_color=btn_color_success), sg.Button('ยกเลิก', button_color=btn_color_critical)]
        ]
        update_window = sg.Window('แก้ไขข้อมูลสินค้า', update_layout)

        while True:
            update_event, update_values = update_window.read()
            if update_event == sg.WIN_CLOSED or update_event == 'ยกเลิก':
                update_window.close()
                break
            elif update_event == 'บันทึก':
                update_product(update_values)
                update_window.close()

    elif event == 'ลบข้อมูลสินค้า':
        delete_layout = [
            [sg.Text('รหัสสินค้าที่ต้องการลบ:'), sg.Input(key='delete_prod_id', size=(input_w, 1))],
            [sg.Button('ลบ', button_color=btn_color_warning), sg.Button('ยกเลิก', button_color=btn_color_critical)]
        ]
        delete_window = sg.Window('ลบข้อมูลสินค้า', delete_layout)
        while True:
            delete_event, delete_values = delete_window.read()
            if delete_event == sg.WIN_CLOSED or delete_event == 'ยกเลิก':
                delete_window.close()
                break
            elif delete_event == 'ลบ':
                delete_product(delete_values)
                delete_window.close()
    elif event == 'ขายสินค้า':
        sell_layout = [
            [sg.Text('รหัสสินค้าที่ต้องการขาย:', size=(15, 1)), sg.Input(key='sell_prod_id', size=(input_w, 1))],
            [sg.Text('จำนวนที่ต้องการขาย:', size=(15, 1)), sg.Input(key='sell_qty', size=(input_w, 1))],
            [sg.Button('ขาย', button_color=btn_color_warning), sg.Button('ยกเลิก', button_color=btn_color_critical)]
        ]
        sell_window = sg.Window('ขายสินค้า', sell_layout)

        while True:
            sell_event, sell_values = sell_window.read()
            if sell_event == sg.WIN_CLOSED or sell_event == 'ยกเลิก':
                sell_window.close()
                break
            elif sell_event == 'ขาย':
                sell_product(sell_values)
                sell_window.close()

window.close()
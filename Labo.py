import sqlite3
from tkinter import *
import os
import datetime
import shutil
import sys


fen_principale = Tk()
fen_principale.geometry('1024x768')
fen_principale.resizable(width=0, height=0)
fen_principale.title('Caisse enregistreuse ')
fen_principale.configure(bg = 'grey')

db_name = 'meals.db'
db_path = db_name

###SQLITE FUNCTION###
def connect_to_db(db_path):
  try:
    db_link = sqlite3.connect(db_path)
  except sqlite3.Error as error:
    print("Error while connecting to database : ", error)
  return db_link


def create_cursor(db_link):
  try:
    db_cursor = db_link.cursor()
  except sqlite3.Error as error:
    print("Error while creating database cursor : ", error)
  return db_cursor


def read_from_cursor(db_cursor,sql_query,sql_values=tuple()):
  try:
    db_cursor.execute(sql_query,sql_values)
    query_result = db_cursor.fetchall()
  except sqlite3.Error as error:
    print("Error while reading from cursor : ", error)
  return query_result


def write_to_cursor(db_cursor,sql_query,sql_values=tuple()):
  try:
    db_cursor.execute(sql_query, sql_values)
  except sqlite3.Error as error:
    print("Error while writing to cursor : ", error)


def commit_to_db(db_link):
  try:
    db_link.commit()
  except sqlite3.Error as error:
    print("Error while commiting cursor to database : ", error)


def disconnect_from_db(db_link):
  try:
    db_link.close()
  except sqlite3.Error as error:
    print("Error while disconnecting from database : ", error)


def save_database():
  backup_dir = 'backup'
  if not os.path.isdir(backup_dir):
    os.makedirs(backup_dir)
  date = datetime.datetime.now()
  hour = date.strftime("%H")
  source = db_name
  backup = backup_dir + '/' + db_name + '_' + hour
  shutil.copyfile(source, backup)


def exit_program():
  sys.exit()


def close_window_principal():
    fen_principale.destroy()


###FUNCTION ADD AND MODIFY###
def add_user(first_name, family_name, email_address) :

    db_link = connect_to_db(db_path)
    db_cursor = create_cursor(db_link)
    sql_query = "INSERT INTO employee(first_name,family_name,email_address) VALUES (?,?,?)"
    sql_values = (first_name, family_name, email_address)
    write_to_cursor(db_cursor,sql_query,sql_values)
    commit_to_db(db_link)
    disconnect_from_db(db_link)


def add_menu(description, price) :

    db_link = connect_to_db(db_path)
    db_cursor = create_cursor(db_link)
    sql_query = "INSERT INTO menu(description,price) VALUES (?,?)"
    sql_values = (description, price)
    write_to_cursor(db_cursor,sql_query,sql_values)
    commit_to_db(db_link)
    disconnect_from_db(db_link)


def modify_user(employee_id, new_first_name, new_family_name, new_email_address) :

    db_link = connect_to_db(db_path)
    db_cursor = create_cursor(db_link)
    sql_query = "SELECT first_name,family_name,email_address FROM employee WHERE id=?"
    sql_values = (employee_id,)
    query_result = read_from_cursor(db_cursor,sql_query,sql_values)
    first_name = query_result[0][0]
    family_name = query_result[0][1]
    email_address = query_result[0][2]
    db_cursor.close()


    db_cursor = create_cursor(db_link)
    if new_first_name:
        sql_query = "UPDATE employee SET first_name = ? WHERE id=?"
        sql_values = (new_first_name,employee_id)
        write_to_cursor(db_cursor,sql_query,sql_values)


    if new_family_name:
        sql_query = "UPDATE employee SET family_name = ? WHERE id=?"
        sql_values = (new_family_name,employee_id)
        write_to_cursor(db_cursor,sql_query,sql_values)


    if new_email_address:
        sql_query = "UPDATE employee SET email_address = ? WHERE id=?"
        sql_values = (new_email_address,employee_id)
        write_to_cursor(db_cursor,sql_query,sql_values)


def modify_menu(menu_id, new_description, new_price):

    db_link = connect_to_db(db_path)
    db_cursor = create_cursor(db_link)
    sql_query = "SELECT description,price FROM menu WHERE id=?"
    sql_values = (menu_id,)
    query_result = read_from_cursor(db_cursor,sql_query,sql_values)
    description = query_result[0][0]
    price = query_result[0][1]
    db_cursor.close()

    db_cursor = create_cursor(db_link)
    if new_description:
        sql_query = "UPDATE menu SET description = ? WHERE id=?"
        sql_values = (new_description,menu_id)
        write_to_cursor(db_cursor,sql_query,sql_values)


    if new_price:
        sql_query = "UPDATE menu SET price = ? WHERE id=?"
        sql_values = (new_price,menu_id)
        write_to_cursor(db_cursor,sql_query,sql_values)


###FUNCTION TICKET###
def purchase(employeeid_option, menuid_option):
  purchase_id = get_purchase_id()
  current_date = datetime.datetime.now()
  formated_date = current_date.strftime("%d-%m-%Y %H:%M:%S")

  employee_id = get_employee_id(employeeid_option)
  print(employee_id)
  employee_name = get_employee_name(employee_id)
  ticket_data = [purchase_id,formated_date,employee_name]

  db_link = connect_to_db(db_path)
  db_cursor = create_cursor(db_link)
  sql_query = "INSERT INTO purchase(date,employee_id) VALUES (?,?)"
  sql_values = (formated_date,employee_id)
  write_to_cursor(db_cursor,sql_query,sql_values)

  menu_id_list = get_id_list('menu')

  while True:
    menu_id = menuid_option

    if not menu_id: #TODO if menu_id in menu_id_list:
      break

    os.system('clear')
    menu_id = int(menu_id)
    if menu_id in menu_id_list:
        menu_price = get_menu_price(menu_id) #TODO get_purchase_detail plutôt que get_menu_price?
        sql_query = "INSERT INTO purchase_detail(purchase_id,menu_id,menu_price) VALUES (?,?,?)"
        sql_values = (purchase_id,menu_id,menu_price)
        write_to_cursor(db_cursor,sql_query,sql_values)
        ticket_data.append(sql_values)
        ecranticket.config(text = "purchase ")
    display_ticket(ticket_data)

  confirm = input("Confirm your order (y/n) : ")
  if ((confirm == 'y') and (len(ticket_data) >= 4)):
    commit_to_db(db_link)
    disconnect_from_db(db_link)
    save_database(db_path)
  choose_enquiry()


def display_ticket(ticket_data):
  purchase_line = 'Purchase number : ' + str(ticket_data[0])
  date_line = 'Date : ' + ticket_data[1]
  employee_line = 'Employee : ' + ticket_data[2] + '\n'

  print(purchase_line)
  print(date_line)
  print(employee_line)

  amount = 0.0
  for index in range(3,len(ticket_data)): #[purchase_id,date,employee,(p_id,menu_id,price)]
    menu_id = ticket_data[index][1]
    description = get_menu_description(menu_id)
    price = ticket_data[index][2]
    detail_string = "Menu: {:<18} {:>6} €"
    detail_line = detail_string.format(description,price)
    print(detail_line)
    amount = amount + price #TODO pourquoi 3.3 * 3 donne 9.89999999?
  amount_line = '\nAmount : ' + str(amount) + ' €'
  print(amount_line)


###FUNCTION GET###
def get_purchase_id():
   db_link = connect_to_db(db_path)
   db_cursor = create_cursor(db_link)
   sql_query = "SELECT MAX(id) FROM purchase"
   query_result = read_from_cursor(db_cursor,sql_query)
   disconnect_from_db(db_link)
   if query_result[0][0] != None:
     last_purchase_id = query_result[0][0]
   else:
     last_purchase_id = 0
   purchase_id = last_purchase_id + 1
   return purchase_id


def get_employee_id(): #TODO idem que get_menu_id()?
   employee_id_list = get_id_list('employee')
   #print(employee_id_list) #[1, 2, 3, 4]
   employee_id = 0
   while employee_id not in employee_id_list:
     os.system('clear')
     employee_id = input("Enter the employee ID : ")
     if not employee_id:
       employee_id = 0
     else:
       employee_id = int(employee_id)
   return employee_id


def get_id_list(table_name):
   db_link = connect_to_db(db_path)
   db_cursor = create_cursor(db_link)
   if (table_name == 'employee'): #TODO simlify with ?
     sql_query = "SELECT id FROM employee"
   elif (table_name == 'menu'):
     sql_query = "SELECT id FROM menu"
   query_result = read_from_cursor(db_cursor,sql_query)
   id_list = []
   for id in query_result:
     id_list.append(id[0])
   disconnect_from_db(db_link)
   return id_list


def get_employee_name(user_id):
   employee_id = user_id
   db_link = connect_to_db(db_path)
   db_cursor = create_cursor(db_link)
   sql_query = "SELECT first_name,family_name FROM employee WHERE id=?"
   sql_values = (employee_id,)
   query_result = read_from_cursor(db_cursor,sql_query,sql_values)
   employee_name = query_result[0][0] + ' ' + query_result[0][1]
   disconnect_from_db(db_link)
   return employee_name


def get_menu_price(menu_id):
   db_link = connect_to_db(db_path)
   db_cursor = create_cursor(db_link)
   sql_query = "SELECT price FROM menu WHERE id=?"
   sql_values = (menu_id,)
   query_result = read_from_cursor(db_cursor,sql_query,sql_values)
   menu_price = query_result[0][0]
   disconnect_from_db(db_link)
   return menu_price


def get_menu_description(menu_id):
   db_link = connect_to_db(db_path)
   db_cursor = create_cursor(db_link)
   sql_query = "SELECT description FROM menu WHERE id=?"
   sql_values = (menu_id,)
   query_result = read_from_cursor(db_cursor,sql_query,sql_values)
   description = query_result[0][0]
   disconnect_from_db(db_link)
   return description


###KEYBOARDd###
def create_keyboard():
    "Création d'un clavier virtuel"
    keyboard = Tk()
    keyboard.geometry('850x400')
    keyboard.title('Keyboard')
    keyboard.resizable(width = 0, height = 0)
    keyboard.configure(bg = 'grey')

    def closeWindow():
        keyboard.destroy()


    b1 = Button(keyboard,text = '1',font = ("Arial", 20, "roman","bold"), width = 4)
    b1.grid(sticky = 'w', padx = 3, pady = 3)
    b2 = Button(keyboard,text = '2',font = ("Arial", 20, "roman","bold"), width = 4)
    b2.grid(row = 0, column = 1, sticky = 'w', padx = 3, pady = 3)
    b3 = Button(keyboard,text = '3',font = ("Arial", 20, "roman","bold"), width = 4)
    b3.grid(row = 0, column = 2, sticky = 'w', padx = 3, pady = 3)
    b4 = Button(keyboard,text = '4',font = ("Arial", 20, "roman","bold"), width = 4)
    b4.grid(row = 0, column = 3, sticky = 'w', padx = 3, pady = 3)
    b5 = Button(keyboard,text = '5',font = ("Arial", 20, "roman","bold"), width = 4)
    b5.grid(row = 0, column = 4, sticky = 'w', padx = 3, pady = 3)
    b6 = Button(keyboard,text = '6',font = ("Arial", 20, "roman","bold"), width = 4)
    b6.grid(row = 0, column = 5, sticky = 'w', padx = 3, pady = 3)
    b7 = Button(keyboard,text = '7',font = ("Arial", 20, "roman","bold"), width = 4)
    b7.grid(row = 0, column = 6, sticky = 'w', padx = 3, pady = 3)
    b8 = Button(keyboard,text = '8',font = ("Arial", 20, "roman","bold"), width = 4)
    b8.grid(row = 0, column = 7, sticky = 'w', padx = 3, pady = 3)
    b9 = Button(keyboard,text = '9',font = ("Arial", 20, "roman","bold"), width = 4)
    b9.grid(row = 0, column = 8, sticky = 'w', padx = 3, pady = 3)
    b0 = Button(keyboard,text = '0',font = ("Arial", 20, "roman","bold"), width = 4)
    b0.grid(row = 0, column = 9, sticky = 'w', padx = 3, pady = 3)

    bA = Button(keyboard,text = 'A',font = ("Arial", 20, "roman","bold"), width = 4)
    bA.grid(row = 1, column = 0, sticky = 'w', padx = 3, pady = 3)
    bZ = Button(keyboard,text = 'Z',font = ("Arial", 20, "roman","bold"), width = 4)
    bZ.grid(row = 1, column = 1, sticky = 'w', padx = 3, pady = 3)
    bE = Button(keyboard,text = 'E',font = ("Arial", 20, "roman","bold"), width = 4)
    bE.grid(row = 1, column = 2, sticky = 'w', padx = 3, pady = 3)
    bR = Button(keyboard,text = 'R',font = ("Arial", 20, "roman","bold"), width = 4)
    bR.grid(row = 1, column = 3, sticky = 'w', padx = 3, pady = 3)
    bT = Button(keyboard,text = 'T',font = ("Arial", 20, "roman","bold"), width = 4)
    bT.grid(row = 1, column = 4, sticky = 'w', padx = 3, pady = 3)
    bY = Button(keyboard,text = 'Y',font = ("Arial", 20, "roman","bold"), width = 4)
    bY.grid(row = 1, column = 5, sticky = 'w', padx = 3, pady = 3)
    bU = Button(keyboard,text = 'U',font = ("Arial", 20, "roman","bold"), width = 4)
    bU.grid(row = 1, column = 6, sticky = 'w', padx = 3, pady = 3)
    bI = Button(keyboard,text = 'I',font = ("Arial", 20, "roman","bold"), width = 4)
    bI.grid(row = 1, column = 7, sticky = 'w', padx = 3, pady = 3)
    bO = Button(keyboard,text = 'O',font = ("Arial", 20, "roman","bold"), width = 4)
    bO.grid(row = 1, column = 8, sticky = 'w', padx = 3, pady = 3)
    bP = Button(keyboard,text = 'P',font = ("Arial", 20, "roman","bold"), width = 4)
    bP.grid(row = 1, column = 9, sticky = 'w', padx = 3, pady = 3)

    bQ = Button(keyboard,text = 'Q',font = ("Arial", 20, "roman","bold"), width = 4)
    bQ.grid(row = 2, column = 0, sticky = 'w', padx = 3, pady = 3)
    bS = Button(keyboard,text = 'S',font = ("Arial", 20, "roman","bold"), width = 4)
    bS.grid(row = 2, column = 1, sticky = 'w', padx = 3, pady = 3)
    bD = Button(keyboard,text = 'D',font = ("Arial", 20, "roman","bold"), width = 4)
    bD.grid(row = 2, column = 2, sticky = 'w', padx = 3, pady = 3)
    bF = Button(keyboard,text = 'F',font = ("Arial", 20, "roman","bold"), width = 4)
    bF.grid(row = 2, column = 3, sticky = 'w', padx = 3, pady = 3)
    bG = Button(keyboard,text = 'G',font = ("Arial", 20, "roman","bold"), width = 4)
    bG.grid(row = 2, column = 4, sticky = 'w', padx = 3, pady = 3)
    bH = Button(keyboard,text = 'H',font = ("Arial", 20, "roman","bold"), width = 4)
    bH.grid(row = 2, column = 5, sticky = 'w', padx = 3, pady = 3)
    bJ = Button(keyboard,text = 'J',font = ("Arial", 20, "roman","bold"), width = 4)
    bJ.grid(row = 2, column = 6, sticky = 'w', padx = 3, pady = 3)
    bK = Button(keyboard,text = 'K',font = ("Arial", 20, "roman","bold"), width = 4)
    bK.grid(row = 2, column = 7, sticky = 'w', padx = 3, pady = 3)
    bL = Button(keyboard,text = 'L',font = ("Arial", 20, "roman","bold"), width = 4)
    bL.grid(row = 2, column = 8, sticky = 'w', padx = 3, pady = 3)
    bM = Button(keyboard,text = 'M',font = ("Arial", 20, "roman","bold"), width = 4)
    bM.grid(row = 2, column = 9, sticky = 'w', padx = 3, pady = 3)

    bW = Button(keyboard,text = 'W',font = ("Arial", 20, "roman","bold"), width = 4)
    bW.grid(row = 3, column = 0, sticky = 'w', padx = 3, pady = 3)
    bX = Button(keyboard,text = 'X',font = ("Arial", 20, "roman","bold"), width = 4)
    bX.grid(row = 3, column = 1, sticky = 'w', padx = 3, pady = 3)
    bC = Button(keyboard,text = 'C',font = ("Arial", 20, "roman","bold"), width = 4)
    bC.grid(row = 3, column = 2, sticky = 'w', padx = 3, pady = 3)
    bV = Button(keyboard,text = 'V',font = ("Arial", 20, "roman","bold"), width = 4)
    bV.grid(row = 3, column = 3, sticky = 'w', padx = 3, pady = 3)
    bB = Button(keyboard,text = 'B',font = ("Arial", 20, "roman","bold"), width = 4)
    bB.grid(row = 3, column = 4, sticky = 'w', padx = 3, pady = 3)
    bN = Button(keyboard,text = 'N',font = ("Arial", 20, "roman","bold"), width = 4)
    bN.grid(row = 3, column = 5, sticky = 'w', padx = 3, pady = 3)
    bmail = Button(keyboard,text = '@',font = ("Arial", 20, "roman","bold"), width = 4)
    bmail.grid(row = 3, column = 6, sticky = 'w', padx = 3, pady = 3)
    bpoint = Button(keyboard,text = '.',font = ("Arial", 20, "roman","bold"), width = 4)
    bpoint.grid(row = 3, column = 7, sticky = 'w', padx = 3, pady = 3)
    bunderscore = Button(keyboard,text = '_',font = ("Arial", 20, "roman","bold"), width = 4)
    bunderscore.grid(row = 3, column = 8, sticky = 'w', padx = 3, pady = 3)
    bvirgule = Button(keyboard,text = ',',font = ("Arial", 20, "roman","bold"), width = 4)
    bvirgule.grid(row = 3, column = 9, sticky = 'w', padx = 3, pady = 3)

    bapostrophe = Button(keyboard,text = "'",font = ("Arial", 20, "roman","bold"), width = 4)
    bapostrophe.grid(row = 4, column = 0, sticky = 'w', padx = 3, pady = 3)
    bspace = Button(keyboard, text = 'SPACE', bg = 'Light blue', fg = 'black', font = ("Arial", 20, "roman","bold"), width = 8)
    bspace.grid(row = 4,rowspan =2, column = 1,columnspan = 2, sticky = 'w', padx = 3, pady = 3)
    befface = Button(keyboard,text = u"\u00AB", bg = 'Light blue', fg = 'black', font = ("Arial", 20, "roman","bold"), width = 8)
    befface.grid(row = 4,rowspan =2, column = 3,columnspan = 2, sticky = 'w', padx = 3, pady = 3)


    bcancel = Button(keyboard, text = 'CANCEL', bg = 'red', fg = 'black', font =
    ("Arial", 20, "roman","bold"), width = 8, command = closeWindow)
    bcancel.grid(row = 6,rowspan =2, column = 3,columnspan = 2,  sticky = 'w', padx = 3, pady = 3)
    benter = Button(keyboard, text = 'ENTER', bg = 'green', fg = 'black', font =
    ("Arial", 20, "roman","bold"), width = 8)
    benter.grid(row = 6, column = 5,columnspan = 2, sticky = 'w', padx = 3, pady = 3)

    keyboard.mainloop()


###ADDUSER###
def create_fen_adduser():
    "Création de la fenêtre Add user"
    adduser = Toplevel(fen_principale)
    adduser.geometry('670x150')
    adduser.resizable(width=0, height=0)
    adduser.title('Add User')
    adduser.configure(bg = 'grey')
    adduser.wm_attributes("-topmost", 1)


    def confirm_entry() :
        confirm = Toplevel(adduser)
        confirm.title('Confirm ?')
        confirm.geometry('300x100')
        confirm.resizable(0, 0)
        confirm.configure(bg = 'grey')
        confirm.wm_attributes("-topmost", 1)

        bOUI = Button(confirm, text = "YES", bg = "light blue", font =
        ("Arial", 20, "roman","bold"),width = 8, command = add_user and close_window)
        bOUI.grid(columnspan = 3)

        bNON = Button(confirm, text = "NO", bg = "red", font =
        ("Arial", 20, "roman","bold"), width = 8,command = close_window )
        bNON.grid(row = 0, column = 3, columnspan = 3)


        add_user(first_name.get(), family_name.get(), email_address.get())


    def close_window():
        adduser.destroy()


    first_name_label = Label(adduser, text = 'Enter user first name : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    first_name_label.grid(rowspan = 2, sticky = 'nw')

    first_name = Entry(adduser, width = 50)
    first_name.grid(row = 0, rowspan = 2, column = 1,  sticky = 'nw')


    family_name_label = Label(adduser, text = 'Enter user family name : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    family_name_label.grid(row = 2, rowspan = 2, sticky = 'nw')

    family_name = Entry(adduser, width = 50)
    family_name.grid(row = 2, rowspan = 2, column = 1, sticky = 'nw')

    email_address_label = Label(adduser, text = 'Enter user email adress : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    email_address_label.grid(row = 4, rowspan = 2, sticky = 'nw')

    email_address = Entry(adduser, width = 50)
    email_address.grid(row = 4, column = 1, sticky = 'nw')

    bcancel = Button(adduser, text = 'CANCEL', bg = 'red', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = close_window)
    bcancel.grid(row = 0,rowspan =2, column = 4, sticky = 'e', padx = 5)

    benter = Button(adduser, text = 'ENTER', bg = 'green', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = confirm_entry)
    benter.grid(row = 2, column = 4, sticky = 'e', padx = 5)

    bkeyboard = Button(adduser, text = 'Keyboard', bg = 'light blue', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = create_keyboard)
    bkeyboard.grid(row = 4, column = 4, sticky = 'e', padx = 5)


    adduser.grab_set()
    fen_principale.wait_window(adduser)


###MODIFYUSER###
def create_fen_modifyuser():
    "Création de la fenêtre Modify User"
    modifyuser = Toplevel()
    modifyuser.geometry('670x150')
    modifyuser.resizable(width=0, height=0)
    modifyuser.title('Modify user')
    modifyuser.configure(bg = 'grey')
    modifyuser.wm_attributes("-topmost", 1)


    def confirm_entry() :
        confirm = Toplevel(modifyuser)
        confirm.title('Confirm ?')
        confirm.geometry('300x100')
        confirm.resizable(0, 0)
        confirm.configure(bg = 'grey')
        confirm.wm_attributes("-topmost", 1)

        bOUI = Button(confirm, text = "YES", bg = "light blue", font =
        ("Arial", 20, "roman","bold"), width = 8, command = modify_user and close_window)
        bOUI.grid(columnspan = 3)

        bNON = Button(confirm, text = "NO", bg = "red", font =
        ("Arial", 20, "roman","bold"), width = 8,command = close_window )
        bNON.grid(row = 0, column = 3, columnspan = 3)


        modify_user(employee_id.get(), new_first_name.get(), new_family_name.get(), new_email_address.get())


    def close_window():
        modifyuser.destroy()


    employee_id_label = Label(modifyuser, text = 'Enter ID user\'s to modify : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    employee_id_label.grid(rowspan = 2, sticky = 'nw')

    employee_id = Entry(modifyuser, width = 50)
    employee_id.grid(row = 0, rowspan = 2, column = 1,  sticky = 'nw')

    new_first_name_label = Label(modifyuser, text = 'Modify user first name : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    new_first_name_label.grid(row = 2, rowspan = 2, sticky = 'nw')

    new_first_name = Entry(modifyuser, width = 50)
    new_first_name.grid(row = 2, rowspan = 2, column = 1,  sticky = 'nw')

    new_family_name_label = Label(modifyuser, text = 'Modify user last name : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    new_family_name_label.grid(row = 4, rowspan = 2, sticky = 'nw')

    new_family_name = Entry(modifyuser, width = 50)
    new_family_name.grid(row = 4, rowspan = 2, column = 1, sticky = 'nw')

    new_email_address_label = Label(modifyuser, text = 'Modify user mail adress : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    new_email_address_label.grid(row = 6, rowspan = 2, sticky = 'nw')

    new_email_address = Entry(modifyuser, width = 50)
    new_email_address.grid(row = 6, column = 1, sticky = 'nw')


    bcancel = Button(modifyuser, text = 'CANCEL', bg = 'red', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = close_window)
    bcancel.grid(row = 0,rowspan =2, column = 4, sticky = 'e', padx = 5)

    benter = Button(modifyuser, text = 'ENTER', bg = 'green', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = confirm_entry)
    benter.grid(row = 2, column = 4, sticky = 'e', padx = 5)

    bkeyboard = Button(modifyuser, text = 'Keyboard', bg = 'light blue', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = create_keyboard)
    bkeyboard.grid(row = 4, column = 4, sticky = 'e', padx = 5)


    modifyuser.grab_set()
    fen_principale.wait_window(modifyuser)


###ADDMENU###
def creat_fen_addmenu():
    "Création de la fenêtre Add menu"
    addmenu = Toplevel()
    addmenu.geometry('670x150')
    addmenu.resizable(width=0, height=0)
    addmenu.title('Add menu')
    addmenu.configure(bg = 'grey')
    addmenu.wm_attributes("-topmost", 1)


    def confirm_entry() :
        confirm = Toplevel(addmenu)
        confirm.title('Confirm ?')
        confirm.geometry('300x100')
        confirm.resizable(0, 0)
        confirm.configure(bg = 'grey')
        confirm.wm_attributes("-topmost", 1)

        bOUI = Button(confirm, text = "YES", bg = "light blue", font =
        ("Arial", 20, "roman","bold"), width = 8, command = add_menu and close_window)
        bOUI.grid(columnspan = 3)

        bNON = Button(confirm, text = "NO", bg = "red", font =
        ("Arial", 20, "roman","bold"), command = close_window , width = 8)
        bNON.grid(row = 0, column = 3, columnspan = 3)


        add_menu(description.get(), price.get())

    def close_window():
        addmenu.destroy()


    description_label = Label(addmenu, text = 'Enter menu description : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey').grid(rowspan = 2, sticky = 'nw')

    description = Entry(addmenu, width = 50)
    description.grid(row = 0, rowspan = 2, column = 1,  sticky = 'nw')

    price_label = Label(addmenu, text = 'Enter menu price (ex : 3.5) : ', font =
    ("Arial", 12, "roman","bold"), bg = 'grey').grid(row = 2, rowspan = 2, sticky = 'nw')

    price = Entry(addmenu, width = 50)
    price.grid(row = 2, rowspan = 2, column = 1, sticky = 'nw')

    bcancel = Button(addmenu, text = 'CANCEL', bg = 'red', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = close_window)
    bcancel.grid(row = 0,rowspan =2, column = 4, sticky = 'e', padx = 5)

    benter = Button(addmenu, text = 'ENTER', bg = 'green', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = confirm_entry)
    benter.grid(row = 2, column = 4, sticky = 'e', padx = 5)

    bkeyboard = Button(addmenu, text = 'Keyboard', bg = 'light blue', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = create_keyboard)
    bkeyboard.grid(row = 4, column = 4, sticky = 'e', padx = 5)

    addmenu.grab_set()
    fen_principale.wait_window(addmenu)


###MODIFYMENU###
def create_fen_modifymenu():
     "Création de la fenêtre Modify menu"
     modifymenu = Toplevel()
     modifymenu.geometry('670x150')
     modifymenu.resizable(width=0, height=0)
     modifymenu.title('Modify menu')
     modifymenu.configure(bg = 'grey')
     modifymenu.wm_attributes("-topmost", 1)

     def confirm_entry() :
         confirm = Toplevel(modifymenu)
         confirm.title('Confirm ?')
         confirm.geometry('300x100')
         confirm.resizable(0, 0)
         confirm.configure(bg = 'grey')
         confirm.wm_attributes("-topmost", 1)

         bOUI = Button(confirm, text = "YES", bg = "light blue", font =
         ("Arial", 20, "roman","bold"), width = 8, command = modify_menu and close_window)
         bOUI.grid(columnspan = 3)

         bNON = Button(confirm, text = "NO", bg = "red", font =
         ("Arial", 20, "roman","bold"), width = 8,command = close_window )
         bNON.grid(row = 0, column = 3, columnspan = 3)


         modify_menu(menu_id.get(), new_description.get(), new_price.get())

     def close_window():
         modifymenu.destroy()

     menu_id_label = Label(modifymenu, text = 'Enter ID menu\'s to modify : ', font =
     ("Arial", 12, "roman","bold"), bg = 'grey')
     menu_id_label.grid(rowspan = 2, sticky = 'nw')

     menu_id = Entry(modifymenu, width = 50)
     menu_id.grid(row = 0, rowspan = 2, column = 1,  sticky = 'nw')

     new_description_label= Label(modifymenu, text = 'Enter  new description : ', font =
     ("Arial", 12, "roman","bold"), bg = 'grey')
     new_description_label.grid(row = 2, rowspan = 2, sticky = 'nw')

     new_description = Entry(modifymenu, width = 50)
     new_description.grid(row = 2, rowspan = 2, column = 1, sticky = 'nw')

     new_price_label = Label(modifymenu, text = 'Enter new  price (ex : 3.5) : ', font =
     ("Arial", 12, "roman","bold"), bg = 'grey')
     new_price_label.grid(row = 3, rowspan = 2, sticky = 'nw')

     new_price = Entry(modifymenu, width = 50)
     new_price.grid(row = 3, rowspan = 2, column = 1, sticky = 'nw')

     bcancel = Button(modifymenu, text = 'CANCEL', bg = 'red', fg = 'black', font =
     ("Arial", 12, "roman","bold"), width = 12, height = 1, command = close_window)
     bcancel.grid(row = 0,rowspan =2, column = 4, sticky = 'e', padx = 5)

     benter = Button(modifymenu, text = 'ENTER', bg = 'green', fg = 'black', font =
     ("Arial", 12, "roman","bold"), width = 12, height = 1, command = confirm_entry)
     benter.grid(row = 2, column = 4, sticky = 'e', padx = 5)

     bkeyboard = Button(modifymenu, text = 'Keyboard', bg = 'light blue', fg = 'black', font =
     ("Arial", 12, "roman","bold"), width = 12, height = 1, command = create_keyboard)
     bkeyboard.grid(row = 4, column = 4, sticky = 'e', padx = 5)

     modifymenu.grab_set()
     fen_principale.wait_window(modifymenu)


###PURCHASE###
def create_fen_purchase():
    "Création de la fenêtre purchase"
    purchase = Toplevel()
    purchase.geometry('450x70')
    purchase.resizable(width = 0, height = 0)
    purchase.title('PURCHASE')
    purchase.configure(bg = 'grey')
    purchase.wm_attributes("-topmost", 1)

    def close_window():
        purchase.destroy()

    def create_fen_purchase_menu():
        purchase_menu = Toplevel()
        purchase_menu.geometry('450x70')
        purchase_menu.resizable(width = 0, height = 0)
        purchase_menu.title('PURCHASE')
        purchase_menu.configure(bg = 'grey')
        purchase_menu.wm_attributes("-topmost", 1)


        def close_window():
            purchase_menu.destroy()

        purchase_label = Label(purchase_menu, text = 'Enter menu\'s ID :', font =
        ("Arial", 12, "roman","bold"), bg = 'grey')
        purchase_label.grid(rowspan = 2, sticky = 'nw')

        menu_id = Entry(purchase_menu, width = 50)
        menu_id.grid(row = 0, rowspan = 2, column = 1, columnspan = 6,  sticky = 'nw')

        bcancel = Button(purchase_menu, text = 'CANCEL', bg = 'red', fg = 'black', font =
        ("Arial", 12, "roman","bold"), width = 12, height = 1, command = close_window)
        bcancel.grid(row = 2,rowspan =2, column = 1,columnspan = 3,  sticky = 'w', padx = 5)

        benter = Button(purchase_menu, text = 'ENTER', bg = 'green', fg = 'black', font =
        ("Arial", 12, "roman","bold"), width = 12, height = 1)
        benter.grid(row = 2, column = 4, sticky = 'w', padx = 5)

        purchase.wait_window(purchase_menu)

    purchase_label = Label(purchase, text = 'Enter ID :', font =
    ("Arial", 12, "roman","bold"), bg = 'grey')
    purchase_label.grid(rowspan = 2, sticky = 'nw')

    employee_id = Entry(purchase, width = 50)
    employee_id.grid(row = 0, rowspan = 2, column = 1, columnspan = 6,  sticky = 'nw')

    bcancel = Button(purchase, text = 'CANCEL', bg = 'red', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = close_window)
    bcancel.grid(row = 2,rowspan =2, column = 1,columnspan = 3,  sticky = 'w', padx = 5)

    benter = Button(purchase, text = 'ENTER', bg = 'green', fg = 'black', font =
    ("Arial", 12, "roman","bold"), width = 12, height = 1, command = create_fen_purchase_menu)
    benter.grid(row = 2, column = 4, sticky = 'w', padx = 5)



    fen_principale.wait_window(purchase)


###FRAME ###
framemenu = Frame(fen_principale, width = 1024, height = 92, bg = 'grey')
framemenu.grid(row = 0, rowspan = 3, column = 0, columnspan = 25 )


###MENU BUTTONS###
adduser = Button(framemenu, text = "Add user", bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 16, height = 1, command = create_fen_adduser)
adduser.grid(row = 1, column = 1, columnspan = 5, pady = 15, padx = 18)

modifyuser = Button(framemenu, text = "Modify user", bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 16, height = 1, command = create_fen_modifyuser)
modifyuser.grid(row = 1, column = 7, columnspan = 5, pady = 15, padx = 18)

addmenu = Button(framemenu, text = "Add menu", bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 16, height = 1, command = creat_fen_addmenu)
addmenu.grid(row = 1, column = 13, columnspan = 5, pady = 15, padx = 18)

modifymenu = Button(framemenu, text = "Modify menu", bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 16, height = 1, command = create_fen_modifymenu)
modifymenu.grid(row = 1, column = 19, columnspan = 5, pady = 15, padx = 18)


###CANVAS TICKET###
ecranticket = Text(fen_principale, width = 68, height = 35, bg = 'ivory', font =
("Arial", 12, "roman","bold"))
ecranticket.grid(row = 3, rowspan = 15, column = 0, columnspan = 15, sticky = 'w', padx = 18)


###PAD BUTTONS###
b7 = Button(fen_principale, text = '7', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b7.grid(row = 3, column = 16, columnspan= 2, sticky = 'w')

b8 = Button(fen_principale, text = '8', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b8.grid(row = 3, column = 19, columnspan= 2, sticky = 'w')

b9 = Button(fen_principale, text = '9', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b9.grid(row = 3, column = 22, columnspan= 2, sticky = 'w')

b4 = Button(fen_principale, text = '4', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b4.grid(row = 5, column = 16, columnspan= 2, sticky = 'w')

b5 = Button(fen_principale, text = '5', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b5.grid(row = 5, column = 19, columnspan= 2, sticky = 'w')

b6 = Button(fen_principale, text = '6', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b6.grid(row = 5, column = 22, columnspan= 2, sticky = 'w')

b1 = Button(fen_principale, text = '1', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b1.grid(row = 7, column = 16, columnspan= 2, sticky = 'w')

b2 = Button(fen_principale, text = '2', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b2.grid(row = 7, column = 19, columnspan= 2, sticky = 'w')

b3 = Button(fen_principale, text = '3', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
b3.grid(row = 7, column = 22, columnspan= 2, sticky = 'w')

b0 = Button(fen_principale, text = '0', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 16, height = 3)
b0.grid(row = 9, column = 16, columnspan= 5, sticky = 'w')

bpoint = Button(fen_principale, text = '.', bg = 'light blue', fg = 'white', font =
("Arial", 16, "roman","bold"), width = 8, height = 3)
bpoint.grid(row = 9, column = 22, columnspan= 2, sticky = 'w')

bclose = Button(fen_principale, text = 'CLOSE', bg = 'red', fg = 'black', font =
("Arial", 16, "roman","bold"), width = 12, height = 3, command = close_window_principal)
bclose.grid(row = 13, column = 16, columnspan= 4, sticky = 'w')

bsave = Button(fen_principale, text = 'SAVE', bg = 'green', fg = 'black', font =
("Arial", 16, "roman","bold"), width = 12, height = 3, command = save_database)
bsave.grid(row = 13, column = 20, columnspan= 4, sticky = 'w')

bpurchase = Button(fen_principale, text = 'PURCHASE', bg = 'Light blue', fg = 'black', font =
("Arial", 16, "roman","bold"), width = 25,height = 3, command = create_fen_purchase)
bpurchase.grid(row = 17, column = 16, columnspan= 8, sticky = 'w')


fen_principale.mainloop()

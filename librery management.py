#importing modules
import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb 
import tkinter.simpledialog as sd 
#connecting to database
connector = sqlite3.connect("librery.db")
cursor = connector.cursor()
#Defining all the backend functions
def issuer_card():
    cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')
    if not cid:
        mb.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
    else:
        return cid
def display_record():
    global connector, cursor
    global tree
    tree.delete(*tree.get_children())
    curr = connector.execute("SELECT * FROM Library")
    data = curr.fetchall()
    for records in data:
        tree.insert("", END, values=records)
def clear_fields():
    global bk_status, bk_id, bk_name, author_name, card_id
    bk_status.set('available')
    for i in['bk_id', 'bk_name', 'author_name', 'card_id']:
        exec(f"{i}.set("")")
        bk_id_entery.config(state=normal)
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass
def clear_and_display():
    clear_fields()
    display_record()
def view_record():
    global bk_name,bk_id,bk_status,author_name,card_id
    global free
    if not tree.focus():
        mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return
    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item("values")
    bk_name.set(selection[0]); bk_id.set(selection[1]); bk_status.set(selection[3])
    author_name.set(selection[2])
    #Defining all the data storage and manipulation functions
    def add_record():
        global connector
        global bk_name, bk_id, bk_status, author_name
        if bk_status.get() == "Issued":
            card_id.get(issuer_card())
        else:
            card_id.set("N/A")
        surety = mb.askyesno('Are you sure?','Are you sure this is the data you want to enter?\nPlease note that Book ID cannot be changed in the future')
        if surety:
            try:
                connector.execute('INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?'),(bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(),card_id.get())
                connector.commit()
                clear_and_display()
                mb.showinfo("record added!")
            except sqlite3.IntegrityError:
                mb.showerror("book ID already in use!")
    def update_record():
        def update():
            global bk_status,bk_id,author_name,card_id
            global connector, tree
            if bk_status.get() == "Issued":
                card_id.set(issuer_card())
            else:
                card_id("N/A")
            cursor.execute('UPDATE Library SET BK_NAME=?, BK_STATUS=?, AUTHOR_NAME=?, CARD_ID=? WHERE BK_ID=?',(bk_name.get(), author_name.get(), card_id.get(), bk_id.get()))
            connector.commit()
            clear_and_display()
            edit.destroy()
            bk_id_entery.config(state='normal')
            clear.config(state='normal')
        view_record() 
        bk_id_entery.config(state='disable')
        clear.config(state='disable')
        edit = Button(left_frame, text="update", font=btn_font, bg=btn_hlb_bg, width=20, command=update)
        edit.place(x=50, y=375)
    def remove_record():
        if not tree.selection():
            mb.showerror("please an item from the database")
            return
        currnt_item = tree.focus()
        values = tree.item(currnt_item)
        selection = values['values']
        cursor.execute('DELETE FROM Library WHERE BK_ID=?',(selection[1],))
        connector.commit()
        tree.delete(currnt_item)
        mb.showinfo("the record you wanted deleted was sucsessfully deleted!")
        clear_and_display()
    def delete_inventory():
        if mb.askyesno("are you sure you want to delete the inventory?"):
            tree.delete(*tree.get_children())
            cursor.execute('DELETE FROM Library')
            connector.commit()
        else:
            return
    def chanege_availebility():
        global card_id, tree, connector
        if not tree.selection():
            mb.showerror("please select book from the database")
        return
        current_item = tree.focus()
        values = tree.item(current_item)
        BK_id = values['values'][1]
        BK_status = values['values'][3]
        if BK_status == 'Issued':
            surety = mb.askyesno("has book returned to you?")
            if surety:
                cursor.execute('UPDATE Library SET bk_status=?, card_id=? WHERE bk_id=?', ('Available', 'N/A',Bk_id))
                connector.commit()
            else:
                mb.showinfo('The book status cannot be set to Available unless it has been returned')
        else:
            cursor.execute('UPDATE Library SET bk_status=?, card_id=? where bk_id=?',("Issued", issuer_card(),BK_id))
        clear_and_display()
        #GUI
        lf_bg = "LightSkyBlue"
        rtf_bg = "DeepSkyBlue"
        rbf_bg = "DodgerBlue"
        btn_hlb_bg = "SteelBlue"
        lbl_font = ("Georgia", 13)
        entery_font = ("Times New Roman", 12)
        btn_font = ("Gill Sans MT", 13)
        root = Tk()
        root.title("librery management System")
        root.geometry("1010x530")
        root.resizable(0,0)
        Label(root, text="librery management System", font=("Noto Sans CJK TC", 15, bold), bg=btn_hlb_bg,fg='white').pack(slide=TOP, fill=X)
        bk_status = StringVar()
        bk_name = StringVar()
        bk_id = StringVar()
        author_name = StringVar()
        card_id = StringVar()
        left_frame = Frame(root, bg=lf_bg)
        left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)
        RT_frame = Frame(root, bg=lf_bg)
        RT_frame.place(x=0.3, y=30, relheight=0.2, relwidth=0.96)
        RB_frame = Frame(root)
        RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)
        Label(left_frame, text="Book Name", bg=lf_bg, font=lbl_font).place(x=98, y=25)
        Entry(left_frame, width=25, font=entery_font, text= bk_name).place(x=45, y=55)
        Label(left_frame, text="Book ID",bg=lf_bg, font= lbl_font).place(x=110, y=105)
        bk_id_entery = Entry(left_frame, font=entery_font, text=bk_id)
        bk_id_entery.place(x=45, y=135)
        Label(left_frame, text="Author Name",bg=lf_bg, font= lbl_font).place(x=90, y=185)
        Entry(left_frame, width=25, font=entery_font, text= author_name).place(x=45, y=215)
        Label(left_frame, text="Status Of The Book",bg=lf_bg, font= lbl_font).place(x=75, y=265)
        dd = OptionMenu(left_frame, bk_status, *["Available","Issued"])
        dd.configure(font=entery_font, width=12)
        dd.place(x=50, y=435)
        sumbit = Button(left_frame, text="add new record", font=btn_font, bg=btn_hlb_bg, width=20, command=add_record())
        sumbit.place(x=50, y=375)
        clear = Button(left_frame, text="clear fields", font=btn_font, bg=btn_hlb_bg, width=20, command=clear_fields())
        clear.place(x=50, y=435)
        Button(RT_frame, text="Delete Book Record", font=btn_font, bg=btn_hlb_bg, width=17,command=remove_record()).place(x=8, y=30)
        Button(RT_frame, text="Delete Full Inventory", font=btn_font, bg=btn_hlb_bg, width=17,command=delete_inventory()).place(x=178, y=30)
        Button(RT_frame, text="Update Book details", font=btn_font, bg=btn_hlb_bg, width=17,command=update_record()).place(x=348, y=30)
        Button(RT_frame, text="Change Book Availability", font=btn_font, bg=btn_hlb_bg, width=19,command=chanege_availebility()).place(x=518, y=30)
        Label(RB_frame, text="BOOK INVENTORY", bg=rbf_bg, font=("Noto Sans CJK TC", 15, "bold")).pack(side=TOP, fill=X)
        tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=("Book Name", "Book ID", "Author Status", "Issuer Card ID"))
        XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview())
        YXscrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview())
        XScrollbar.pack(slide=BOTTOM, fill=X)
        YScrollbar.pack(slide=RIGHT, fill=Y)
        tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YXscrollbar.set)
        tree.heading("Book Name", text= "Book Name", anchor=CENTER)
        tree.heading("Book ID", text= "Book ID", anchor=CENTER)
        tree.heading("Anthour", text= "Anthour", anchor=CENTER)
        tree.heading("Status", text= "Status Of The Book", anchor=CENTER)
        tree.heading("Card ID", text= "Card ID of the Issued", anchor=CENTER)
        tree.column("#0", width=0, stretch=NO)
        tree.column("#1", width=225, stretch=NO)
        tree.column("#2", width=70, stretch=NO)
        tree.column("#3", width=150, stretch=NO)
        tree.column("#4", width=105, stretch=NO)
        tree.column("#5", width=132, stretch=NO)
        tree.place(y=30, x=0, relheight=0.9, relwidth=1)
        clear_and_display()
        root.update()
        root.mainloop()

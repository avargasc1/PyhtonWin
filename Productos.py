from tkinter import *
from tkinter import ttk

import sqlite3

class Product:
    db_name='database.db'
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')
        #frame container
        frame=LabelFrame(self.wind, text = 'Register A New Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    
        #Named input
        Label(frame, text='Name: ').grid(row = 1, column = 0)
        self.name= Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        #price
        Label(frame, text='Price: ').grid(row = 2, column = 0)
        self.price= Entry(frame)
        self.price.grid(row = 2, column=1)
        #button
        ttk.Button(frame, text ='Save Produc', command=self.add_product).grid(row =3, columnspan=2, sticky=W+E)

        #table
        self.tree=ttk.Treeview(height=10, columns=("name","price"))
        self.tree.grid(row=4,column=0, columnspan=2)
        self.tree.heading('#0', text='Id', anchor=CENTER)
        self.tree.heading('name', text='Name', anchor=CENTER)
        self.tree.heading('price', text='Price', anchor=CENTER)

        self.get_products()

    def run_query(self, query, parameter=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameter)
            conn.commit()
        return result

    def get_products(self):
        #cleanin table
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #quering data 
        query='SELECT *FROM product ORDER BY id DESC'
        db_rows= self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[0],values=(row[1],row[2]))
            
    def validation(self):
        return len(self.name.get())!=0 and len(self.price.get())!=0
            
    def add_product(self):
        if self.validation():
           query='INSERT INTO product VALUES(NULL,?,?)'
           parameters=(self.name.get(), self.price.get())
           self.run_query(query,parameters)
        else:
            print('Name and price is requiere')
        self.get_products()
     
if __name__=='__main__':
    window= Tk()
    application=Product(window)
    window.mainloop()

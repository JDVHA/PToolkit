import tkinter as tk
from tkinter import ttk


class TkTable(tk.LabelFrame):
    def __init__(self, master, dataframe, text=None):
        super().__init__(master, text=text)
        self.name = text
        self.dataframe = dataframe
        self.columns = ["Index", *list(dataframe.columns)]

        self.treeview  =ttk.Treeview(self, selectmode ='browse',columns=self.columns, show='headings')
        self.treeview.grid(row=0,column=0)
        
        self.horizontalscrollbar = tk.Scrollbar(self)
        self.verticalscrollbar = tk.Scrollbar(self)
        
        self.horizontalscrollbar.config(orient=tk.HORIZONTAL, command=self.treeview.xview)
        self.verticalscrollbar.config(orient=tk.VERTICAL, command=self.treeview.yview)

        self.horizontalscrollbar.grid(row=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.verticalscrollbar.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        
        self.bind('<Enter>', self._Boundscrollwheel)
        self.bind('<Leave>', self._UnBoundscrollwheel)
        self.treeview.bind('<Double Button-1>', self.EditCell)
        self.treeview.config(xscrollcommand=self.horizontalscrollbar.set)
        self.treeview.config(yscrollcommand=self.verticalscrollbar.set)
        self.Update()

        

    def Load_data(self, dataframe):
        self.dataframe = dataframe

    def Update(self):
        self.treeview.delete(*self.treeview.get_children())
        self.column_num = len(self.columns)
        self.rows_num = len(self.dataframe)

        for i in range(self.column_num):
            if i == 0:
                self.treeview.column(self.columns[i], anchor ='c', width=50)
            else:
                self.treeview.column(self.columns[i], anchor ='c', width=150)
            self.treeview.heading(self.columns[i], text =self.columns[i], command=self.test)

        for index, row in self.dataframe.iterrows():
            self.treeview.insert('', tk.END, values=[index, *list(row.values)])
    def test(self):
        print("test")
    def _Boundscrollwheel(self, event):
        self.treeview.bind_all("<MouseWheel>", self._Onscrollwheel)

    def _UnBoundscrollwheel(self, event):
        self.treeview.unbind_all("<MouseWheel>")

    def _Onscrollwheel(self, event):
        self.treeview.yview_scroll(int(-1*(event.delta/120)), "units")

    def EditCell(self, event):
        col = self.columns[int(self.treeview.identify_column(event.x).replace("#", ""))-1]
        row = self.treeview.index(self.treeview.focus())

        entry_cord = self.treeview.bbox(self.treeview.focus(), column=self.treeview.identify_column(event.x))

        var = tk.StringVar()
        E = tk.Entry(self, textvariable=var)
        E.focus_set()
        
        E.select_range(0, 'end')
        var.set(self.dataframe[col][row])
        E.select_range(0, 'end')
        E.icursor('end')
        if entry_cord == None or len(entry_cord) < 4: # Domme bug met .focus method
            pass
        else:
            E.place(x=entry_cord[0], y=entry_cord[1], width=entry_cord[2], height=entry_cord[3])
            E.bind('<FocusOut>', lambda x: self.DestroyCell(E, col, row, var))
            E.bind("<Return>", lambda x: self.DestroyCell(E, col, row, var))
            E.wait_window()
        
    
    def DestroyCell(self, E, col , row, var):
        E.destroy()
        self.dataframe[col][row] = var.get()
        self.Update()
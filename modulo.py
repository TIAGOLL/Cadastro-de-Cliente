from dataclasses import replace
from email import message
import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3
import random
import math
from tkinter import tix
import os
from tkinter import messagebox
from turtle import title

os.system('cls')
root = tix.Tk()

button_font_size=10
bg_button_color='#71849d'
button_font_style='Arial Black'


input_font_style='Arial Black'
input_font_size=10
bg_input_color='White'

bg_label_color='#dfe3ee'
label_font_size=9
label_font_style='Arial Black'


#cor activeback
bg_button_activefore='#187db2'
bg_button_activeback='white'

class gradientFrame(Canvas):#cria efeito de degrade
    def __init__(self, parent, color1='#000076', color2='#6310c0', **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind('<Configure>', self._drawGradient)
    
    def _drawGradient(self, event=None):
        self.delete('gradient')
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1)/limit
        g_ratio = float(g2-g1)/limit
        b_ratio = float(b2-b1)/limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (r_ratio * i))
            nb = int(b1 + (r_ratio * i))
            color = '#%4.4x%4.4x%4.4x' % (nr, ng, nb)
            self.create_line(i,0,i, height, tags=('gradient'), fill=color)
        self.lower('gradient')


class funcs(): #funções usadas pelo aplication
    def variavel(self): #atribui as variaveis
        self.registration = self.registration_input.get()
        self.name = self.name_input.get()
        self.telephone = self.telephone_input.get()
        self.city = self.city_input.get()
        self.cpf_cnpj = self.cpf_cnpj_input.get()
        self.adress = self.adress_input.get()
    
    def limpa_tela(self): #limpa os inputs
        self.registration_input.delete(0, END)
        self.name_input.delete(0, END)
        self.city_input.delete(0, END)
        self.cpf_cnpj_input.delete(0, END)
        self.adress_input.delete(0, END)
        self.telephone_input.delete(0, END)
    
    def connect_database(self): #conecta o banco de dados
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
    
    def desconnect_database(self): #desconecta o banco de dados
        self.conn.close()
    
    def mount_database(self): #monta o banco de dados
        self.connect_database(); print('Conectando ao banco de dados')
        ### criar tabela
        self.cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS clientes(
                registration CHARVAR(20),
                nome_cliente CHARVAR(40) NOT NULL, 
                telefone INTEGER(20),
                cidade CHARVAR(40),
                endereço CHARVAR(40),
                cpf_cnpj CHARVAR(40) NOT NULL
            );
        """)

        self.conn.commit(); print('Banco de dados criado')
        self.desconnect_database()

    def add_client(self): #adiciona cliente
        self.variavel()

        """if self.name == '':
            messagebox.showinfo(title='ERROR', message='Campo "Nome" se encontra vazio!')
            return 0
        elif self.cpf_cnpj == '':
            messagebox.showinfo(title='ERROR', message='Campo "CPF/CNPJ" se encontra vazio!')
            return 0
        elif self.telephone == '':
            messagebox.showinfo(title='ERROR', message='Campo "Telefone" se encontra vazio!')
            return 0"""

        self.math = math.ceil(1000000 * random.random()) #str(round(math.ceil(100 * random.random()), 3)) + '.' + str(round(math.ceil(1000 * random.random()), 4)) + '-' + str(round(math.ceil(10 * random.random()), 1))
        self.registration = self.math
        self.registration = self.format()
        self.connect_database()
        self.cursor.execute(
        f""" 
            INSERT INTO clientes(registration, nome_cliente, telefone, cidade, cpf_cnpj, endereço)
            VALUES('{self.registration}', '{self.name}', '{self.telephone}', '{self.city}', '{self.cpf_cnpj}', '{self.adress}')
        """)

        self.conn.commit()
        self.desconnect_database()
        self.select_list()
        messagebox.showinfo(title='Info', message='Cliente adicionado com suscesso!')

    def select_list(self): #seleciona dados do bd e coloca na trueview
        self.clientTrueview.delete(*self.clientTrueview.get_children())
        self.connect_database()
        
        list = self.cursor.execute(
        """ 
            SELECT registration, nome_cliente, telefone, cidade, cpf_cnpj, endereço FROM clientes 
            ORDER BY nome_cliente ASC; 
        """) # cod, nome_cliente, telefone, cidade
        for i in list:
            self.clientTrueview.insert("", END, values=i) 
        self.desconnect_database()
        self.limpa_tela()

    def search_cliente(self):#busca os clientes
        self.connect_database()

        self.clientTrueview.delete(*self.clientTrueview.get_children())
        
        self.name_input.insert(END, '%')
        name = self.name_input.get()
        self.cursor.execute(
            """ SELECT registration, nome_cliente, telefone, cidade, endereço, cpf_cnpj FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % name)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.clientTrueview.insert('', END, values=i)
        self.limpa_tela()
        self.desconnect_database()

    def onDoubleClick(self, event): #joga dados da trueview para os campos de inserção
        self.limpa_tela()
        self.clientTrueview.selection()

        for n in self.clientTrueview.selection():
            col1, col2, col3, col4, col5, col6 = self.clientTrueview.item(n, 'values')
            self.registration_input.insert(END, col1)
            self.name_input.insert(END, col2)
            self.telephone_input.insert(END, col3)
            self.city_input.insert(END, col4)
            self.cpf_cnpj_input.insert(END, col5)
            self.adress_input.insert(END, col6)

    def delete_client(self): #deleta um cliente
        self.variavel()
        self.connect_database()
        self.cursor.execute(f"""DELETE FROM clientes WHERE registration = '{self.registration}'""")
        self.conn.commit()
        self.desconnect_database()
        self.limpa_tela()
        self.select_list()

    def change_client(self):#muda as informações dos clientes
        self.variavel()
        self.connect_database()
        self.cursor.execute(
            f""" UPDATE clientes SET nome_cliente = '{self.name}', telefone = '{self.telephone}', cidade = '{self.city}', cpf_cnpj = '{self.cpf_cnpj}', endereço = '{self.adress}'
            WHERE registration = '{self.registration}'""")
        self.conn.commit()
        self.desconnect_database()
        self.select_list()
        self.limpa_tela()

class application(funcs):
    #self = método de construção
    def __init__(self): #chamada inicial
        self.root = root
        self.first_window()
        self.frames_first_window()
        self.widgets_frame1()
        self.widgets_frame2()
        self.mount_database()
        self.select_list()
        self.menus()
        root.mainloop()

    def format(self): #fomata a matricula no db
        times = 0
        new = ""
        self.registration = f'{self.registration}'
        for i in range(6):
            number = self.registration[i]
            new += number
            times += 1
            if(i == 4):
                new += "-"
            if(times == 2):
                new += "."
        return new

    def format_registration(self, event = None):#validação de entrada
        
        text = self.registration_input.get().replace(".", "").replace("-", "")[:6]
        new_text = ""
        
        if event.keysym.lower() == "backspace": return
        
        for index in range(len(text)):
            
            if not text[index] in "0123456789": continue
            if index in [1]: new_text += text[index] + "."
            elif index == 4: new_text += text[index] + "-"
            else: new_text += text[index]

        self.registration_input.delete(0, "end")
        self.registration_input.insert(0, new_text)
        print(new_text)

    def first_window(self): #configuração da primeira tela
        self.root.title('Cadastro de clientes')
        self.root.configure(background='#d3c6cc')
        self.root.geometry('1280x720')
        self.root.resizable(True, True)
        self.root.minsize(width=950, height=550)
        self.root.maxsize(width=1920, height=1080)
    
    def frames_first_window(self): #frames da primeira janela
        
        self.frame1 = Frame(self.root, bd=4,bg='#dfe3ee', highlightbackground='#187db2', highlightthickness=3)
        self.frame1.place(relx=0.005, rely=0.008, relwidth=0.99, relheight=0.48 )
        #frame 2 da primeira tela
        self.frame2 = Frame(self.root, bd=4,bg='#dfe3ee', highlightbackground='#187db2', highlightthickness=3)
        self.frame2.place(relx=0.005, rely=0.5, relwidth=0.99, relheight=0.49 )

    def widgets_frame1(self): #Widgets do frame 1
        #setando abas
        self.abas = ttk.Notebook(self.frame1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background='#dfe3ee')
        self.aba2.configure(background='lightgray')

        self.abas.add(self.aba1, text='Aba 1')
        self.abas.add(self.aba2, text='Aba 2')
        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)
        
        #bordas
        self.canvas_bt = Canvas(self.aba1, bd=0, bg='black', highlightbackground='gray', highlightthickness=3)
        self.canvas_bt.place(relx=0.017, rely=0.08, relheight=0.094, relwidth=0.157)
        #botão limpar
        self.bt_clean = Button(self.aba1, text='Limpar', bd=3, bg=bg_button_color, fg='White', font=(button_font_style, button_font_size, 'bold'), command=self.limpa_tela, activebackground=bg_button_activeback, activeforeground=bg_button_activefore)
        self.bt_clean.place(relx=0.26, rely=0.07, relheight=0.1, relwidth=0.1)
        #botão buscar
        self.bt_search = Button(self.aba1, text='Buscar', bd=3, bg=bg_button_color, fg='White', font=(button_font_style, button_font_size, 'bold'), command=self.search_cliente, activebackground=bg_button_activeback, activeforeground=bg_button_activefore)
        self.bt_search.place(relx=0.37, rely=0.07, relheight=0.1, relwidth=0.1)
        self.search_balloon = tix.Balloon(self.aba1)
        self.search_balloon.bind_widget(self.bt_search, balloonmsg='Digite no campo "Nome" e clique em buscar para efetuar a pesquisa')
        #botão novo
        self.bt_new = Button(self.aba1, text='Novo',background='Black', bd=3, bg=bg_button_color, fg='White', font=(button_font_style, button_font_size, 'bold'), command=self.add_client, activebackground=bg_button_activeback, activeforeground=bg_button_activefore)
        self.bt_new.place(relx=0.6, rely=0.07, relheight=0.1, relwidth=0.1)
        #botão alterar
        self.bt_change = Button(self.aba1, text='Alterar', bd=3, bg=bg_button_color, fg='White', font=(button_font_style, button_font_size, 'bold'), command=self.change_client, activebackground=bg_button_activeback, activeforeground=bg_button_activefore)
        self.bt_change.place(relx=0.71, rely=0.07, relheight=0.1, relwidth=0.1)
        #botão apagar
        self.bt_delete = Button(self.aba1, text='Deletar', bd=3, bg=bg_button_color, fg='White', font=(button_font_style, button_font_size, 'bold'), command=self.delete_client, activebackground=bg_button_activeback, activeforeground=bg_button_activefore)
        self.bt_delete.place(relx=0.82, rely=0.07, relheight=0.1, relwidth=0.1)
        
        
        #criação da label e entrada do codigo
        #label do codigo do cliente
        self.lb_registration = Label(self.aba1, text='Matrícula', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_registration.place(relx=0.0179, rely=0.005)
        #input
        self.registration_input = Entry(self.aba1, font=(input_font_style, input_font_size), bg=bg_input_color)
        self.registration_input.place(relx=0.02, rely=0.09, relheight=0.07)
        self.registration_input.bind('<KeyRelease>', self.format_registration)
        #label nome cliente
        self.lb_name = Label(self.aba1, text='Nome', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_name.place(relx=0.0179, rely=0.23)
        #input
        self.name_input = Entry(self.aba1)
        self.name_input.place(relx=0.02, rely=0.3, relheight=0.07, relwidth=0.3)
        #label CPF/CNPJ
        self.lb_cpf_cnpj = Label(self.aba1, text='CPF/CNPJ', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_cpf_cnpj.place(relx=0.348, rely=0.23)
        #input
        self.cpf_cnpj_input = Entry(self.aba1)
        self.cpf_cnpj_input.place(relx=0.35, rely=0.3, relheight=0.07, relwidth=0.2)
        #label Cidade
        self.lb_city = Label(self.aba1, text='Cidade', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_city.place(relx=0.348, rely=0.45)
        #input
        self.city_input = Entry(self.aba1)
        self.city_input.place(relx=0.35, rely=0.52, relheight=0.07, relwidth=0.2)
        #label Endereço
        self.lb_adress = Label(self.aba1, text='Endereço', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_adress.place(relx=0.0179, rely=0.45)
        #input
        self.adress_input = Entry(self.aba1)
        self.adress_input.place(relx=0.02, rely=0.52, relheight=0.07, relwidth=0.3)
        #label Telefone
        self.lb_telephone = Label(self.aba1, text='Telefone', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_telephone.place(relx=0.0179, rely=0.67)
        #input
        self.telephone_input = Entry(self.aba1)
        self.telephone_input.place(relx=0.02, rely=0.74, relheight=0.07, relwidth=0.3)
        #Número casa
        self.lb_house_number = Label(self.aba1, text='Número', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_house_number.place(relx=0.5789, rely=0.45)
        #input
        self.house_number_input = Entry(self.aba1)
        self.house_number_input.place(relx=0.58, rely=0.52, relheight=0.07, relwidth=0.2)
        #genero
        self.lb_name = Label(self.aba1, text='Gênero', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_name.place(relx=0.58, rely=0.23)
        #input
        self.tipvar = StringVar(self.aba1)
        self.tipv = ('Masculino', 'Feminino')
        self.popupMenu = OptionMenu(self.aba1, self.tipvar, *self.tipv)
        self.popupMenu.place(relx=0.58, rely=0.3, relheight=0.08, relwidth=0.2)
        self.popupMenu.config(background='White', highlightbackground='Gray', highlightthickness=0.5)
   
    def widgets_frame2(self): #widgets do frame 2
        #lista Treeview
        self.clientTrueview = ttk.Treeview(self.frame2, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.clientTrueview.heading('#0', text='')
        self.clientTrueview.heading('#1', text='Matrícula')
        self.clientTrueview.heading('#2', text='Nome')
        self.clientTrueview.heading('#3', text='Telefone')
        self.clientTrueview.heading('#4', text='Cidade')
        self.clientTrueview.heading('#5', text='CPF/CNPJ')
        self.clientTrueview.heading('#6', text='Endereço')

        self.clientTrueview.column('#0', stretch=NO, minwidth=30, width=0, anchor="center")
        self.clientTrueview.column('#1', stretch=YES, minwidth=50, width=50, anchor="center")
        self.clientTrueview.column('#2', stretch=YES, minwidth=100, width=200, anchor="center")
        self.clientTrueview.column('#3', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#4', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#5', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#6', stretch=YES, minwidth=100, width=100, anchor="center")

        self.clientTrueview.place(relx=0.01, rely=0.03, relwidth=0.95, relheight=0.95)

        self.scroolLista = Scrollbar(self.frame2, orient='vertical')
        self.clientTrueview.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.03, relwidth=0.02, relheight=0.95)
        self.clientTrueview.bind('<Double-1>', self.onDoubleClick)

    def menus(self):#adiciona um menu bar na janela
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def quit(): self.root.destroy()

        menubar.add_cascade(label='Opções', menu=filemenu)
        menubar.add_cascade(label='Sobre', menu=filemenu2)

        filemenu.add_command(label='Sair', command=quit)
        filemenu2.add_command(label='Limpar Cliente', command=self.limpa_tela)

        '''filemenu2.add_command(label='Relatórios', command=self.gerarRelatcliente)'''

    def second_window(self):#segunda janela
        self.root2 = Toplevel()
        self.root2.title('Janela 2')
        self.root2.configure(background='#b7bfc4')
        self.root2.geometry('400x200')
        self.root2.resizable(False, False)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()

    
#chamada da classe
application()
from tkinter import ttk
from tkinter import *
import sqlite3
import random
import os
import math
from tkinter import tix
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import time
from threading import Timer

os.system('clear')
root2 = tix.Tk()

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
bg_button_activefore='Black'
bg_button_activeback='white'

class funcs(): #funções usadas pelo aplication
    def variavel(self): #atribui as variaveis
        self.registration = self.registration_input.get()
        self.name = self.name_input.get()
        self.telephone = self.telephone_input.get()
        self.city = self.city_input.get()
        self.cpf_cnpj = self.cpf_cnpj_input.get()
        self.adress = self.adress_input.get()
        self.genre = self.tipvar.get()
        self.number = self.house_number_input.get()
    
    def limpa_tela(self): #limpa os inputs
        self.registration_input.delete(0, END)
        self.name_input.delete(0, END)
        self.city_input.delete(0, END)
        self.cpf_cnpj_input.delete(0, END)
        self.adress_input.delete(0, END)
        self.telephone_input.delete(0, END)
        self.house_number_input.delete(0, END)
        self.tipvar.set('')
    
    def connect_database(self): #conecta o banco de dados
        self.conn = sqlite3.connect("F:/Documentos/Python Projects/Cadastro de Clientes/DataBase/app.db")
        self.cursor = self.conn.cursor()

    def desconnect_database(self): #desconecta o banco de dados
        self.conn.close()
    
    def mount_table_clientes(self): #monta o banco de dados
        self.connect_database(); print('Conectando ao banco de dados')
        #criar tabela
        self.cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS clientes(
                registration CHARVAR(20),
                nome_cliente CHARVAR(40) NOT NULL, 
                telefone INTEGER(20),
                cidade CHARVAR(40),
                endereço CHARVAR(40),
                cpf_cnpj CHARVAR(40) NOT NULL,
                numero CHARVAR(40),
                genero CHARVAR(40)
            );
        """)

        self.conn.commit(); print('Banco de dados criado')
        self.desconnect_database()
    
    def mount_table_psswd(self):
        self.connect_database()
        self.cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS senhas(
                senha CHARVAR(40),
                login CHARVAR(15)
            );
        """)
        self.conn.commit()
        self.desconnect_database()

    def add_client(self): #adiciona cliente
        self.variavel()

        if self.name == '':
            messagebox.showinfo(title='ERROR', message='Campo "Nome" se encontra vazio!')
            return 0
        elif self.cpf_cnpj == '':
            messagebox.showinfo(title='ERROR', message='Campo "CPF/CNPJ" se encontra vazio!')
            return 0
        elif self.telephone == '':
            messagebox.showinfo(title='ERROR', message='Campo "Telefone" se encontra vazio!')
            return 0

        self.math = math.ceil(1000000 * random.random()) #str(round(math.ceil(100 * random.random()), 3)) + '.' + str(round(math.ceil(1000 * random.random()), 4)) + '-' + str(round(math.ceil(10 * random.random()), 1))
        self.registration = self.math
        self.registration = self.format()
        self.connect_database()
        self.cursor.execute(
        f""" 
            INSERT INTO clientes(registration, nome_cliente, telefone, cidade, cpf_cnpj, endereço, numero, genero)
            VALUES('{self.registration}', '{self.name}', '{self.telephone}', '{self.city}', '{self.cpf_cnpj}', '{self.adress}', '{self.number}', '{self.genre}')
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
            SELECT registration, nome_cliente, telefone, cidade, cpf_cnpj, endereço, numero, genero FROM clientes 
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
            """ SELECT registration, nome_cliente, telefone, cidade, cpf_cnpj, endereço, numero, genero FROM clientes
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
            col1, col2, col3, col4, col5, col6, col7, col8 = self.clientTrueview.item(n, 'values')
            self.registration_input.insert(END, col1)
            self.name_input.insert(END, col2)
            self.telephone_input.insert(END, col3)
            self.city_input.insert(END, col4)
            self.cpf_cnpj_input.insert(END, col5)
            self.adress_input.insert(END, col6)
            self.house_number_input.insert(END, col7)
            self.tipvar.set(str(col8))

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

    def calendar(self):
        self.calendario1 = Calendar(self.aba2, fg='gray75', bg='blue', font=('Arial Black', '9', 'bold'), locale='pt_br')
        self.calendario1.place(relx=0.5, rely=0.1)
        self.calDate = Button(self.aba2, text='Inserir data', command=self.print_calendar)
        self.calDate.place(relx=0.55, rely=0.85, height=25, width=100)

    def print_calendar(self):
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entry_data.delete(0, END)
        self.entry_data.insert(END, dataIni)
        self.calDate.destroy()

    def format_cpf(self, event = None):
       text = self.cpf_cnpj_input.get().replace(".", "").replace("-", "")[:11]
       new_text = ""
 
       if event.keysym.lower() == "backspace": return
     
       for index in range(len(text)):
         
           if not text[index] in "0123456789": continue
           if index in [2, 5]: new_text += text[index] + "."
           elif index == 8: new_text += text[index] + "-"
           else: new_text += text[index]
 
       self.cpf_cnpj_input.delete(0, "end")
       self.cpf_cnpj_input.insert(0, new_text)

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

    def progress_bar(self):#configs da barra
        self.progress1['value'] += 10
        self.porcent = self.progress1['value']
        self.progress_lb['text'] = str(round(self.porcent)) + '%'
        self.time()

    def time(self):#seta o tempo de atualização
        if self.progress1['value'] == 100:
            return 0
        self.t = Timer(2, self.progress_bar)
        self.t.start()

        
class application(funcs):
    #self = método de construção
    def __init__(self): #chamada inicial
        self.root = Toplevel()
        self.root.withdraw()
        self.root2 = root2
        self.app()
        self.login_window()
        self.widgets_login()
        self.frames_app()
        self.widgets_frame1()
        self.widgets_frame2()
        self.mount_table_clientes()
        self.mount_table_psswd()
        self.menus()
        self.select_list()
        root2.mainloop()
    
    def app(self): #configuração da primeira tela
        self.root.title('Cadastro de clientes')
        self.root.configure(background='#d3c6cc')
        self.root.geometry('1280x720')
        self.root.resizable(True, True)
        self.root.minsize(width=950, height=550)
        self.root.maxsize(width=1920, height=1080)
  
    def frames_app(self): #frames da primeira janela
        
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
        
        #barra de progresso
        self.porcent = 0
        self.progress1 = ttk.Progressbar(self.aba2, orient=HORIZONTAL, length=300, mode='determinate')
        self.progress1.place(relx=0.1, rely=0.001, height=10, width=300)
        self.progress_button = Button(self.aba2, text='progress', bd=3, bg=bg_button_color, fg='white', command=self.time)
        self.progress_button.place(relx=0.1, rely=0.1, height=100, width=100)
        self.progress_lb = Label(self.aba2, text=f'{self.porcent}' + "%", bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.progress_lb.place(relx=0.5, rely=0.5, relheight=0.1, relwidth=0.1)
        #calendario
        self.bt_calendar = Button(self.aba2, text='Data', bd=3, bg=bg_button_color, fg='White', font=(button_font_style, button_font_size, 'bold'), command=self.calendar, activebackground=bg_button_activeback, activeforeground=bg_button_activefore)
        self.bt_calendar.place(relx=0.5, rely=0.02)
        self.entry_data = Entry(self.aba2, width=10)
        self.entry_data.place(relx=0.5, rely=0.2)
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
        self.lb_name = Label(self.aba1, text='Nome*', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_name.place(relx=0.0179, rely=0.23)
        #input
        self.name_input = Entry(self.aba1)
        self.name_input.place(relx=0.02, rely=0.3, relheight=0.07, relwidth=0.3)
        #label CPF/CNPJ
        self.lb_cpf_cnpj = Label(self.aba1, text='CPF/CNPJ*', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
        self.lb_cpf_cnpj.place(relx=0.348, rely=0.23)
        #input
        self.cpf_cnpj_input = Entry(self.aba1)
        self.cpf_cnpj_input.place(relx=0.35, rely=0.3, relheight=0.07, relwidth=0.2)
        self.cpf_cnpj_input.bind('<KeyRelease>', self.format_cpf)
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
        self.lb_telephone = Label(self.aba1, text='Telefone*', bg=bg_label_color, font=(label_font_style, label_font_size, 'bold'))
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
        self.clientTrueview = ttk.Treeview(self.frame2, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8'))
        self.clientTrueview.heading('#0', text='')
        self.clientTrueview.heading('#1', text='Matrícula')
        self.clientTrueview.heading('#2', text='Nome')
        self.clientTrueview.heading('#3', text='Telefone')
        self.clientTrueview.heading('#4', text='Cidade')
        self.clientTrueview.heading('#5', text='CPF/CNPJ')
        self.clientTrueview.heading('#6', text='Endereço')
        self.clientTrueview.heading('#7', text='Número')
        self.clientTrueview.heading('#8', text='Gênero')

        self.clientTrueview.column('#0', stretch=NO, minwidth=30, width=0, anchor="center")
        self.clientTrueview.column('#1', stretch=YES, minwidth=50, width=50, anchor="center")
        self.clientTrueview.column('#2', stretch=YES, minwidth=100, width=200, anchor="center")
        self.clientTrueview.column('#3', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#4', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#5', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#6', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#7', stretch=YES, minwidth=100, width=100, anchor="center")
        self.clientTrueview.column('#8', stretch=YES, minwidth=100, width=100, anchor="center")

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

    def login_open(self):#abre o app e fecha o login
        self.root.deiconify()
        self.root2.withdraw()
    
    def login_window(self):#segunda janela
        self.root2 = self.root2
        self.root2.title('Login')
        self.root2.configure(background='#d3c6cc', bg='#3d4561', bd=4, highlightbackground='#187db2', highlightthickness=3)
        self.root2.geometry('500x500')
        self.root2.resizable(False, False)
        self.root2.focus_force()
        self.root2.grab_set()

    def widgets_login(self):
        #frame
        self.frame1 = Frame(self.root2, bd=0,bg='#3d4561', highlightbackground='#187db2', highlightthickness=0)
        self.frame1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        #login input
        self.login_input = Entry(self.frame1, bd=0, font=('Insert', 10), bg='#3d4561', background='#3d4561', highlightbackground='#3d4561', highlightthickness=0)
        self.login_input.place(relx=0.05, rely=0.45, relheight=0.07, relwidth=0.9)
        self.login_input.focus()
        #senha input
        self.senha_input = Entry(self.frame1, bd=0, font=('Insert', 10), bg='#3d4561', background='#3d4561', highlightbackground='#3d4561', highlightthickness=0)
        self.senha_input.place(relx=0.05, rely=0.6, relheight=0.07, relwidth=0.9)
        #botao entrar
        self.bt_entry = Button(self.frame1,font=('Fira Code', 10, 'bold'), bd=0, text='Entrar', background='#a84b60', foreground='White', bg='#a84b60', highlightthickness=0, command=self.login_open)
        self.bt_entry.place(relx=0.05, rely=0.75, relheight=0.1, relwidth=0.9)
        #label senha
        self.lb_senha = Label(self.frame1, text='Senha', background='#3d4561',bg='#3d4561', font=('Ramaraja', 14), foreground='White')
        self.lb_senha.place(relx=0.05, rely=0.53)
        #label login
        self.lb_login = Label(self.frame1, text='Usuario', background='#3d4561',bg='#3d4561', font=('Ramaraja', 14), foreground='White')
        self.lb_login.place(relx=0.05, rely=0.38)
        #Label titulo
        self.lb_login = Label(self.frame1, text='Login', background='#3d4561',bg='#3d4561', font=('Ramaraja', 30), foreground='White')
        self.lb_login.place(relx=0.05, rely=0.15)

#chamada da classe
application()
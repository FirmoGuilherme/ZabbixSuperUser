#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from src.Zabbix.API.Graph import Graph
from tkcalendar import  DateEntry
from src.Zabbix.ZabbixHandler import ZabbixHandler
from src.Constants.Constants import CONSTANTS
from src.Utils import Thread
from datetime import datetime
from calendar import monthrange


class ParentWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.CONSTANTS = CONSTANTS
        self.ZabbixHandler = ZabbixHandler()
        # White and Light Blue, respectively
        self.colors = ("#FFFFFF", "#3A7FF6")
        self.parent_window = parent
        self.geometry = (862, 519)
        self.parent_window.title("Main")
        self.parent_window.geometry(f"{self.geometry[0]}x{self.geometry[1]}")
        self.parent_window.configure(bg=self.colors[1])
        self.parent_window.resizable(False, False)
        self.__load_images()
        self.__init_configs_window()
        if self.ZabbixHandler.gerar_lista_servidores() == AttributeError:
            self.toggle_configs_window()
            messagebox.showerror(title="Erro", message="Usuário ou senha incorreto do zabbix!\
                \nVocê será redirecionado para a tela de configurações para verificar tais valores\
                \nApós isso, reinicie o aplicativo.")
        else:
            self.__init_run_window()
            self.toggle_run_window()     

    def __load_images(self):
        self.img_logo = PhotoImage(
            data= self.CONSTANTS.LOGO_B64)
        self.configuracoes_img = PhotoImage(
            data=self.CONSTANTS.CONFIGS_B64)
        self.voltar_img = PhotoImage(
            data=self.CONSTANTS.VOLTAR_B64)
        self.salvar_img = PhotoImage(
            data=self.CONSTANTS.SALVAR_B64)
        self.executar_img = PhotoImage(
            data=self.CONSTANTS.EXECUTAR_B64)

    def __init_configs_window(self):
        configuracoes = {key:value for key, value in zip(list(self.CONSTANTS.CONFIGS.__dict__.keys())[:], 
            list(self.CONSTANTS.CONFIGS.__dict__.values())[:])}
        configs_blacklist = ["url", "relatorios_storage"]
        
        [configuracoes.pop(var) for var in configs_blacklist]

        # Left Canvas
        self.left_canvas_configs = Canvas(
            self.parent_window, bg=self.colors[1], width=self.geometry[0] / 2, height=self.geometry[1], bd=0, highlightthickness=0, relief="ridge")
        self.__load_logo(self.left_canvas_configs)
        # Right Canvas
        self.right_canvas_configs = Canvas(
            self.parent_window, bg=self.colors[0], width=self.geometry[0] / 2, height=self.geometry[1], bd=0, highlightthickness=0, relief="ridge")
        self.__set_title(self.right_canvas_configs, title="Configurações")

        # Botao Voltar
        trocar_button_obj = Button(image=self.voltar_img, borderwidth=0, highlightthickness=0, command=lambda: [
            self.toggle_run_window(), self.toggle_configs_window()], relief="flat")
        self.right_canvas_configs.create_window(
            self.geometry[0] / 2 - 30,  self.geometry[1] - 70, anchor=NE, window=trocar_button_obj)
        # Botao Salvar
        salvar_button_obj = Button(image=self.salvar_img, borderwidth=0, highlightthickness=0,
            command=lambda: self.salvar_configuracoes(), relief="flat")
        self.right_canvas_configs.create_window(
            self.geometry[0] / 2 - 250,  self.geometry[1] - 70, anchor=NE, window=salvar_button_obj)

        count = 0
        for key, value in configuracoes.items():
            var = self.CONSTANTS.CONFIGS.translate(key)
            count += 1
            input_window = Entry(width=30, font=("Arial", int(13.0)))
            setattr(self, f"input_configs_{var}", input_window)
            if count % 2 == 0:
                self.right_canvas_configs.create_text(self.geometry[0] / 4, self.geometry[1] - self.geometry[1] / (
                    len(configuracoes.values()) + 2) * (count), text=var, fill="#515486", font=("Arial", int(13.0)))
                self.right_canvas_configs.create_window(self.geometry[0] / 4, self.geometry[1] - self.geometry[1] / (
                    len(configuracoes.values()) + 2) * (count) + 25, window=input_window)
                if key != "password":
                    input_window.insert(0, value)
            elif count % 2 != 0:
                self.left_canvas_configs.create_text(self.geometry[0] / 4, self.geometry[1] - self.geometry[1] / (len(
                    configuracoes.values()) + 2) * (count + 1), text=var, fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
                self.left_canvas_configs.create_window(self.geometry[0] / 4, self.geometry[1] - self.geometry[1] / (
                    len(configuracoes.values()) + 2) * (count + 1) + 25, window=input_window)
                if key != "password":
                    input_window.insert(0, value)

    def __init_run_window(self):
        # Left Canvas
        self.left_canvas_run = Canvas(
            self.parent_window, bg=self.colors[1], width=self.geometry[0] / 2, height=self.geometry[1], bd=0, highlightthickness=0, relief="ridge")
        self.__load_logo(self.left_canvas_run)
        # Right Canvas
        self.right_canvas_run = Canvas(
            self.parent_window, bg=self.colors[0], width=self.geometry[0] / 2, height=self.geometry[1], bd=0, highlightthickness=0, relief="ridge")
        self.__set_title(self.right_canvas_run, title="Relatórios")

        # DatePicker from
        self.right_canvas_run.create_text(
            240, 140, text="Dia início", fill=self.colors[1], font=("Arial-BoldMT", int(13.0)))
        self.calendar_from = DateEntry(self.right_canvas_run, width=12, background='darkblue',
                    foreground='white', borderwidth=2,
                    month=datetime.now().month - 1,
                    day=1)
        self.calendar_from.place(x=200, y=150)


        # DatePicker to
        self.right_canvas_run.create_text(
            240, 270, text="Dia Final", fill=self.colors[1], font=("Arial-BoldMT", int(13.0)))
        self.calendar_to = DateEntry(self.right_canvas_run, width=12, background='darkblue',
                    foreground='white', borderwidth=2,
                    month=self.calendar_from.get_date().month,
                    day=monthrange(datetime.now().year, self.calendar_from.get_date().month)[1])
        self.calendar_to.place(x=200, y=280)

        # Botao Voltar
        trocar_button_obj = Button(image=self.voltar_img, borderwidth=0, highlightthickness=0, command=lambda: [
            self.toggle_run_window(), self.toggle_configs_window()], relief="flat")
        self.right_canvas_run.create_window(
            self.geometry[0] / 2 - 30,  self.geometry[1] - 70, anchor=NE, window=trocar_button_obj)
        # Botao Salvar
        executar_button_obj = Button(image=self.executar_img, borderwidth=0,
                highlightthickness=0, command=self.gerar_relatorio, relief="flat")
        self.right_canvas_run.create_window(
            self.geometry[0] / 2 - 250,  self.geometry[1] - 70, anchor=NE, window=executar_button_obj)

        self.left_canvas_run.create_text(
            140, 140, text="Gerar Relatórios de", fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
        presentation_text = ["Todos", "Grupo de Hosts", "Host único"]
        self.clicked_menu = StringVar()
        self.clicked_menu.set(presentation_text[0])
        self.dropdown_meio_procura = OptionMenu(
            self.left_canvas_run, self.clicked_menu, *presentation_text, command=self.update_dropdowns)
        self.dropdown_meio_procura.config(width=30)
        self.dropdown_meio_procura.place(x=100, y=150)

        # Meio de Procura
        self.left_canvas_run.create_text(
            140, 270, text="Sub-Menu", fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
        presentation_text = self.ZabbixHandler.get_sub_menu_presentation_list(
            self.clicked_menu.get())
        self.clicked_sub_menu = StringVar()
        self.clicked_sub_menu.set(presentation_text[0])
        self.dropdown_window_test_case_sub_menu = OptionMenu(
            self.left_canvas_run, self.clicked_sub_menu, *presentation_text)
        self.dropdown_window_test_case_sub_menu.config(width=30)
        self.dropdown_window_test_case_sub_menu.place(x=100, y=280)

    def update_dropdowns(self, *args):
        menu = self.dropdown_window_test_case_sub_menu["menu"]
        menu.delete(0, "end")
        presentation_text = self.ZabbixHandler.get_sub_menu_presentation_list(
            self.clicked_menu.get())
        for text in presentation_text:
            menu.add_command(label=text, command=lambda value=text: (
                        self.clicked_sub_menu.set(value)))
        if args:
            self.clicked_sub_menu.set(presentation_text[0])

    def toggle_run_window(self):
        if self.left_canvas_run.winfo_manager() == "place":
            self.left_canvas_run.place_forget()
            self.right_canvas_run.place_forget()
        else:
            self.left_canvas_run.place(x=0, y=0)
            self.right_canvas_run.place(x=self.geometry[0] / 2, y=0)
            self.parent_window.title("Relatórios")

    def toggle_configs_window(self):
        if self.left_canvas_configs.winfo_manager() == "place":
            self.left_canvas_configs.place_forget()
            self.right_canvas_configs.place_forget()
        else:
            self.left_canvas_configs.place(x=0, y=0)
            self.right_canvas_configs.place(x=self.geometry[0] / 2, y=0)
            self.parent_window.title("Configuracoes")

    def __load_logo(self, canvas):
        canvas.create_image(30, 30, anchor=NW, image=self.img_logo)

    def __set_title(self, canvas, title):
        canvas.create_text(self.geometry[0] / 4, self.geometry[1] - (
            self.geometry[1] * 0.86), text=title, fill=self.colors[1], font=("Arial-BoldMT", int(22.0)))

    def gerar_relatorio(self):
        if self.clicked_sub_menu.get() == "BBFUELS LINKS":
            th = Thread(target=self.ZabbixHandler.gerar_relatorio_bbf_links,
                start_date=self.calendar_from.get_date(), end_date=self.calendar_to.get_date()).start()
            messagebox.showinfo(title="Informação", message="Gerando relatórios de BBFUELS LINKS")
        elif self.clicked_menu.get() == "Todos":
            th = Thread(target = self.ZabbixHandler.gerar_relatorio, start_date=self.calendar_from.get_date(), end_date=self.calendar_to.get_date(), todos = True).start()
            messagebox.showinfo(title="Informação", message="Gerando relatórios da planilha")
        elif self.clicked_menu.get() == "Grupo de Hosts":
            th = Thread(target = self.ZabbixHandler.gerar_relatorio, start_date=self.calendar_from.get_date(), end_date=self.calendar_to.get_date(), host_group=self.clicked_sub_menu.get()).start()
            messagebox.showinfo(title="Informação", message=f"Gerando relatórios do grupo  {self.clicked_sub_menu.get()}")
        else:
            name = self.clicked_sub_menu.get()
            if all(char in "1234567890" for char in name):
                th = Thread(target = self.ZabbixHandler.gerar_relatorio, start_date=self.calendar_from.get_date(), end_date=self.calendar_to.get_date(), id=int(name)).start()
            else:
                th = Thread(target = self.ZabbixHandler.gerar_relatorio, start_date=self.calendar_from.get_date(), end_date=self.calendar_to.get_date(), name=name).start()
            messagebox.showinfo(title="Informação", message=f"Gerando relatórios de {name}")
        Thread(target = self.__thread_notif, th = th).start()

    def __thread_notif(self, th):
        try:
            result = th.result()
        except Exception as excp:
            if type(excp) == FileNotFoundError:
                messagebox.showerror(title="Erro", message="Planilha do Excel não encontrada!\
                    \nVerifique as configurações.")
            return
        if result:
            messagebox.showerror(title="Erro", message="\n".join(result))

    def salvar_configuracoes(self):
        # Extrai todos os inputs e os traduz para nome encontrado no Json
        # Utilizando método translate da classe Configs
        configs = {self.CONSTANTS.CONFIGS.translate(key.split("_")[-1], reverse=True): value.get() for (
            key, value) in self.__dict__.items() if "input_configs" in key and len(value.get()) > 0}
        # Para cada config, checa se é um valor numérico
        for key, value in configs.items():
            if all(char in "1234567890" for char in value):
                configs[key] = int(value)
        self.CONSTANTS.CONFIGS.save_configs(configs)

window = Tk()
main = ParentWindow(window)
main.pack()
try:
    main.mainloop()
finally:
    Thread.exit()

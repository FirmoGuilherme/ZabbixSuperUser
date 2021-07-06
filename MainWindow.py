#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from os import system
from os.path import join
from src.Zabbix.ZabbixHandler import ZabbixHandler
from src.Constants.Constants import CONSTANTS
from threading import Thread


class ParentWindow(Frame):

    def __init__(self, parent):
        self.CONSTANTS = CONSTANTS
        self.ZabbixHandler = ZabbixHandler()
        Frame.__init__(self, parent)
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
        self.__init_run_window()
        self.toggle_run_window()

    def __load_images(self):
        self.img_logo = PhotoImage(
            file=join("src", "Images", "logo-work-db.png"))
        self.test_cases_img = PhotoImage(
            file=join("src", "Images", "Test_cases.png"))
        self.configuracoes_img = PhotoImage(
            file=join("src", "Images", "Configuracoes.png"))
        self.voltar_img = PhotoImage(file=join("src", "Images", "Voltar.png"))
        self.salvar_img = PhotoImage(file=join("src", "Images", "Salvar.png"))
        self.executar_img = PhotoImage(
            file=join("src", "Images", "Executar.png"))
        self.updte_src_img = PhotoImage(
            file=join("src", "Images", "Reload_src.png"))

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
        self.__set_title(self.right_canvas_configs, title="Configuracoes")

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
        if self.clicked_menu.get() == "Todos":
            Thread(self.ZabbixHandler.gerar_relatorio(todos = True)).start()
        elif self.clicked_menu.get() == "Grupo de Hosts":
            Thread(self.ZabbixHandler.gerar_relatorio(host_group=self.clicked_sub_menu.get())).start()
        else:
            name = self.clicked_sub_menu.get()
            if all([char in "1234567890" for char in name]):
                Thread(self.ZabbixHandler.gerar_relatorio(id = int(name))).start()
            else:
                Thread(self.ZabbixHandler.gerar_relatorio(name = name)).start()

    def salvar_configuracoes(self):
        # Extrai todos os inputs e os traduz para nome encontrado no Json
        # Utilizando método translate da classe Configs
        configs = {self.CONSTANTS.CONFIGS.translate(key.split("_")[-1], reverse=True): value.get() for (
            key, value) in self.__dict__.items() if "input_configs" in key and len(value.get()) > 0}
        # Para cada config, checa se é um valor numérico
        for key, value in configs.items():
            if all([char in "1234567890" for char in value]):
                configs[key] = int(value)
        self.CONSTANTS.CONFIGS.save_configs(configs)

window = Tk()
main = ParentWindow(window)
main.pack()
main.mainloop()

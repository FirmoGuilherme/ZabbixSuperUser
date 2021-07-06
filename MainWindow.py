#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from os import system
from os.path import join
from src.Configs.Configs import ConfigsHandler
from src.TestCaseRunner import TestCaseRunner
from src.Utils import Thread, is_unix
import concurrent.futures


class ParentWindow(Frame):

    def __init__(self, parent):
        self.Configs = ConfigsHandler()
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
        self.__init_run_window()
        self.__previous_menu = self.clicked_menu.get()
        self.__previous_sub_menu = self.clicked_sub_menu.get()

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
        configs_blacklist = [""]
        configuracoes = self.Configs.__dict__
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
        voltar_button_obj = Button(image=self.voltar_img, borderwidth=0, highlightthickness=0, command=lambda: [
                                   self.toggle_configs_window(), self.toggle_main_window()], relief="flat")
        self.right_canvas_configs.create_window(
            self.geometry[0] / 2 - 30,  self.geometry[1] - 70, anchor=NE, window=voltar_button_obj)
        # Botao Salvar
        salvar_button_obj = Button(image=self.salvar_img, borderwidth=0, highlightthickness=0,
                                   command=lambda: self.salvar_configuracoes(), relief="flat")
        self.right_canvas_configs.create_window(
            self.geometry[0] / 2 - 250,  self.geometry[1] - 70, anchor=NE, window=salvar_button_obj)

        count = 0
        for key, value in configuracoes.items():
            var = self.Configs.translate(key)
            count += 1
            if var != "Browser":
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
            elif var == "Browser":
                if count % 2 == 0:
                    self.left_canvas_configs.create_text(self.geometry[0] / 4, self.geometry[1] - self.geometry[1] / (len(
                        configuracoes.values()) + 2) * (count), text=var, fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
                    clicked = StringVar()
                    clicked.set(supported_browsers[0])
                    dropdown_window = OptionMenu(
                        self.left_canvas_configs, clicked, *supported_browsers)
                    dropdown_window.config(width=30)
                    dropdown_window.place(
                        x=self.geometry[0] / 4 - 105, y=self.geometry[1] - self.geometry[1] / 8 * (count + 1) + 10)
                elif count % 2 != 0:
                    self.left_canvas_configs.create_text(self.geometry[0] / 4, self.geometry[1] - self.geometry[1] / (len(
                        configuracoes.values()) + 2) * (count + 1), text=var, fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
                    clicked = StringVar()
                    clicked.set(supported_browsers[0])
                    dropdown_window = OptionMenu(
                        self.left_canvas_configs, clicked, *supported_browsers)
                    dropdown_window.config(width=30)
                    dropdown_window.place(x=self.geometry[0] / 4 - 105, y=self.geometry[1] - self.geometry[1] / (
                        len(configuracoes.values()) + 2) * (count + 1) + 10)
                setattr(self, f"dropdown_configs_{var}", clicked)

    def __init_run_window(self):
        # Left Canvas
        self.left_canvas_test_cases = Canvas(
            self.parent_window, bg=self.colors[1], width=self.geometry[0] / 2, height=self.geometry[1], bd=0, highlightthickness=0, relief="ridge")
        self.__load_logo(self.left_canvas_test_cases)
        # Right Canvas
        self.right_canvas_test_cases = Canvas(
            self.parent_window, bg=self.colors[0], width=self.geometry[0] / 2, height=self.geometry[1], bd=0, highlightthickness=0, relief="ridge")
        self.__set_title(self.right_canvas_test_cases, title="Test Cases")

        # Botao Voltar
        voltar_button_obj = Button(image=self.voltar_img, borderwidth=0, highlightthickness=0, command=lambda: [
            self.toggle_test_cases_window(), self.toggle_main_window()], relief="flat")
        self.right_canvas_test_cases.create_window(
            self.geometry[0] / 2 - 30,  self.geometry[1] - 70, anchor=NE, window=voltar_button_obj)
        # Botao Salvar
        executar_button_obj = Button(image=self.executar_img, borderwidth=0,
                highlightthickness=0, command=self.add_test_case_to_queue, relief="flat")
        self.right_canvas_test_cases.create_window(
            self.geometry[0] / 2 - 250,  self.geometry[1] - 70, anchor=NE, window=executar_button_obj)
        # Botao Atualizar Testes
        update_src_button_obj = Button(image=self.updte_src_img, borderwidth=0,
                highlightthickness=0, command=self.TestCaseRunner.update_src, relief="flat")
        self.right_canvas_test_cases.create_window(
            self.geometry[0] / 2 - 30,  self.geometry[1] - 170, anchor=NE, window=update_src_button_obj)

        # Menu
        self.left_canvas_test_cases.create_text(
            140, 140, text="Menu", fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
        presentation_text = self.TestCaseRunner.get_menus_presentation_list()
        self.clicked_menu = StringVar()
        self.clicked_menu.set(presentation_text[0])
        self.dropdown_window_test_case_menu = OptionMenu(
            self.left_canvas_test_cases, self.clicked_menu, *presentation_text, command=self.__update_dropdowns_test_case)
        self.dropdown_window_test_case_menu.config(width=30)
        self.dropdown_window_test_case_menu.place(x=100, y=150)

        # Sub-Menu
        self.left_canvas_test_cases.create_text(
            140, 270, text="Sub-Menu", fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
        presentation_text = self.TestCaseRunner.get_sub_menus_presentation_list(
            self.clicked_menu.get())
        self.clicked_sub_menu = StringVar()
        self.clicked_sub_menu.set(presentation_text[1])
        self.dropdown_window_test_case_sub_menu = OptionMenu(
            self.left_canvas_test_cases, self.clicked_sub_menu, *presentation_text, command=self.__update_dropdowns_test_case)
        self.dropdown_window_test_case_sub_menu.config(width=30)
        self.dropdown_window_test_case_sub_menu.place(x=100, y=280)

        # Test Case
        self.left_canvas_test_cases.create_text(
            140, 400, text="Teste", fill=self.colors[0], font=("Arial-BoldMT", int(13.0)))
        presentation_text = self.TestCaseRunner.get_test_cases_presentation_list(
            self.clicked_menu.get(), self.clicked_sub_menu.get())
        self.clicked_test_case = StringVar()
        self.clicked_test_case.set(presentation_text[0])
        self.dropdown_window_test_case = OptionMenu(
            self.left_canvas_test_cases, self.clicked_test_case, *presentation_text)
        self.dropdown_window_test_case.config(width=30)
        self.dropdown_window_test_case.place(x=100, y=410)

    def __update_dropdowns_test_case(self, *args):
        '''
        args nunca é utilizado
        Implementado apenas pois update de botão passa botão escolhido como variável
        caso função não recebesse argumentos, iria gerar erro
        '''

        def update_sub_menu(force_sub_menu=False):
            menu = self.dropdown_window_test_case_sub_menu["menu"]
            menu.delete(0, "end")
            if self.clicked_menu.get() != "Todos":
                presentation_text = self.TestCaseRunner.get_sub_menus_presentation_list(
                    self.clicked_menu.get())
                for text in presentation_text:
                    menu.add_command(label=text, command=lambda value=text: (
                        self.clicked_sub_menu.set(value), self.__update_dropdowns_test_case()))
                if force_sub_menu:
                    self.clicked_sub_menu.set(presentation_text[0])
                    self.__previous_sub_menu = presentation_text[0]
            else:
                self.clicked_sub_menu.set(f"{self.TestCaseRunner.get_category_amount()} Categorias")

        def update_test_case(force_test_case=False):
            menu = self.dropdown_window_test_case["menu"]
            menu.delete(0, "end")
            if self.clicked_sub_menu.get() != "Todos" and "Categoria" not in self.clicked_sub_menu.get():
                presentation_text = self.TestCaseRunner.get_test_cases_presentation_list(
                    self.clicked_menu.get(), self.clicked_sub_menu.get())
                for text in presentation_text:
                    menu.add_command(label=text, command=lambda value=text: (
                        self.clicked_test_case.set(value)))
                if force_test_case:
                    self.clicked_test_case.set(presentation_text[0])
                    self.__previous_test_case = presentation_text[0]

            # Se opção do Sub-Menu for "Todos", campo de Test Case mostra quantidade de testes que iram rodar
            elif self.clicked_sub_menu.get() == "Todos":
                presentation_text = self.TestCaseRunner.get_test_cases_presentation_list(
                    self.clicked_menu.get(), self.clicked_sub_menu.get())
                self.clicked_test_case.set(f"{len(presentation_text)} Testes")
            elif self.clicked_menu.get() == "Todos":
                self.clicked_test_case.set(f"{self.TestCaseRunner.total_tests} Testes")

        # Se menu selecionado for diferente do último menu, força a alteração do sub_menu e também do test_case
        if self.clicked_menu.get() != self.__previous_menu:
            update_sub_menu(True)
            self.__previous_menu = self.clicked_menu.get()
            update_test_case(True)
        # Se sub_menu selecionado for diferente do último sub_menu, força a alteração do test_case
        elif self.clicked_sub_menu.get() != self.__previous_sub_menu:
            update_test_case(True)
            self.__previous_sub_menu = self.clicked_sub_menu.get()

    def toggle_main_window(self):
        if self.left_canvas.winfo_manager() == "place":
            self.left_canvas.place_forget()
            self.right_canvas.place_forget()
        else:
            self.left_canvas.place(x=0, y=0)
            self.right_canvas.place(x=self.geometry[0] / 2, y=0)
            self.parent_window.title("Main")

    def toggle_test_cases_window(self):
        if self.left_canvas_test_cases.winfo_manager() == "place":
            self.left_canvas_test_cases.place_forget()
            self.right_canvas_test_cases.place_forget()
        else:
            self.left_canvas_test_cases.place(x=0, y=0)
            self.right_canvas_test_cases.place(x=self.geometry[0] / 2, y=0)
            self.parent_window.title("Test Cases")

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

    def salvar_configuracoes(self):
        # Extrai todos os inputs e os traduz para nome encontrado no Json
        # Utilizando método translate da classe Configs
        configs = {self.Configs.translate(key.split("_")[-1], reverse=True): value.get() for (
            key, value) in self.__dict__.items() if "input_configs" in key and len(value.get()) > 0}
        for dropdown_name, dropdown_text in {key: value.get() for (key, value) in self.__dict__.items() if "dropdown_configs" in key}.items():
            configs[self.Configs.translate(dropdown_name.split(
                "_")[-1], reverse=True)] = dropdown_text
        # Para cada config, checa se é um valor numérico
        for key, value in configs.items():
            if all([char in "1234567890" for char in value]):
                configs[key] = int(value)
        self.Configs.save_configs(configs)

    def add_test_case_to_queue(self):
        menu = self.clicked_menu.get()
        sub_menu = self.clicked_sub_menu.get()
        chosen_test = self.clicked_test_case.get()
        self.TestCaseRunner.add_test_case_to_queue(menu, sub_menu, chosen_test)

    def exit(self):
        Thread.exit()
        self.running = False
        if not is_unix():
            system(""" powershell.exe -c "Stop-Process -name Chrome" """)
            system(""" powershell.exe -c "Stop-Process -name ChromeDriver" """)
        else:
            system(
                """ pid=$(ps -ef | grep "python3 MainWindow.py" | awk '{ print $2 }' | head -n 1) && kill $pid """)


window = Tk()
main = ParentWindow(window)
main.pack()
try:
    main.mainloop()
finally:
    main.exit()

# pylint: disable=missing-module-docstring

import subprocess
from datetime import datetime
import customtkinter as ctk

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')

class Home:
    """
    Classe que contém as funções que inicializam toda a tela
    (textos, campos, botões, comandos, etc.)
    """

    def open_main_window(self):
        """Inicializa a janela principal
        """
        main_window = ctk.CTk()

        mw_width = 500
        mw_height = 300

        main_window.title("Menu Principal")

        pos_x = (main_window.winfo_screenwidth() - mw_width) // 2
        pos_y = (main_window.winfo_screenheight() - mw_height) // 2

        main_window.geometry(f"{mw_width}x{mw_height}+{pos_x}+{pos_y}")

        self.create_widgets(main_window)

        main_window.mainloop()


    def create_widgets(self, window_master):
        """Cria todos os Widgets da tela principal

        Args:
            window_master: Janela "master" dos Widgets
        """

        # Definir Widgets
        label_file_path = ctk.CTkLabel(
            window_master, text="Caminho da pasta onde será feito o Backup:"
        )
        label_vm_name = ctk.CTkLabel(
            window_master, text="Nome da VM (Exemplo: Debian, Ubuntu20.04.6)"
        )
        label_list = ctk.CTkLabel(window_master, text='VMs encontradas:')
        label_vms = ctk.CTkLabel(window_master, text=self.get_vm_list())

        entry_file_path = ctk.CTkEntry(window_master, width=200)
        entry_vm_name = ctk.CTkEntry(window_master, width=200)

        btn_create_backup = ctk.CTkButton(
            window_master,
            text="Fazer Backup",
            command=lambda: self.create_backup(
                entry_file_path.get(),
                entry_vm_name.get()
            )
        )

        # Exibir widgets
        label_file_path.pack(pady=10)
        entry_file_path.pack()
        label_vm_name.pack(pady=10)
        entry_vm_name.pack()
        btn_create_backup.pack(pady=(20, 10))
        label_list.pack()
        label_vms.pack()

    def create_backup(self, file_path: str, vm_name: str):
        """Evento que irá iniciar o backup caso o caminho e VM informados existam

        Args:
            file_path (str): caminho onde será salvo o backup
            vm_name (str): nome da VM WSL
        """
        file_name = f"wsl-backup-{vm_name.lower().replace('.', '_').replace('-', '_')}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar"

        command = ['wsl', '--export', vm_name, file_path + '\\' + file_name]

        # Acessa o caminho informado
        path_to_save = subprocess.run(
            ['cd', file_path],
            check=False,
            capture_output=True,
            text=True,
            shell=True
        )

        # Retorna caso o caminho informado não exista
        if path_to_save.returncode:
            print("O caminho não existe!")
            return

        wsl_export = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True
        )

        if wsl_export.returncode:
            print(f"Erro ao exportar VM: {wsl_export.returncode}")
            print(wsl_export)

        print("Backup finalizado!")

    def get_vm_list(self) -> str:
        """Retorna as VMs instaladas

        Returns:
            str: VMs instaladas
        """
        wsl_list = subprocess.run(
            ['wsl', '--list'],
            check=False,
            capture_output=True,
            text=True
        )

        wsl_list = wsl_list.stdout.replace('\x00', '').strip().split('\n\n')[1:]
        wsl_list = list(filter(lambda x: 'docker' not in x, wsl_list))

        return '\n'.join(wsl_list)

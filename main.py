from app.home import Home

# cd <caminho completo onde será salvo o backup>
# wsl --export <Nome da VM> <nome do arquivo>.tar

def main():
    """__main__
    """
    home = Home()
    home.open_main_window()

if __name__ == "__main__":
    main()

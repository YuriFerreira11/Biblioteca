from ui.login_ui import LoginUI
from database.ConnectionFactory import ConnectionFactory

def main():
    ConnectionFactory.testar()  # opcional, só debug

    tela = LoginUI()
    tela.executar()

if __name__ == "__main__":
    main()
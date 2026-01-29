import os
import json
from model.Usuario import Usuario

class UsuarioDAO:

    lista = []
    arquivo = "Nomes.json"

    @classmethod
    def carregar_usuarios(cls):
        if os.path.exists(cls.arquivo):
            try:
                with open(cls.arquivo, "r", encoding="utf-8") as f:
                    cls.lista = json.load(f)
            except json.JSONDecodeError:
                cls.lista = []

    @classmethod
    def gerar_id(cls):
        if not cls.lista:
            return "0001"
        ultimo_id = cls.lista[-1]["ID"]
        novo_id = int(ultimo_id) + 1
        return f"{novo_id:04d}"

    def registrar_usuario(self):
        if Usuario.procurar_usuario(self.nome):
            print("Usuário ja cadastrado")
            return
        usuario = {
            "Nome": self.nome,
            "Idade": self.idade,
            "ID": Usuario.gerar_id()
        }
        Usuario.lista.append(usuario)
        Usuario.salvar_usuarios()

    @classmethod
    def salvar_usuarios(cls):
        with open(cls.arquivo, "w", encoding="utf-8") as f:
            json.dump(cls.lista, f, ensure_ascii=False, indent=4)

    @classmethod
    def procurar_usuario(cls, chave):
        chave_lower = chave.lower()
        for usuario in cls.lista:
            if usuario["Nome"].lower() == chave_lower:
                return usuario
        return None

    @classmethod
    def listar_usuarios(cls):
        return cls.lista

    @classmethod
    def verificar_usuario(cls, user_id):
        for usuario in cls.lista:
            if usuario["ID"] == user_id:
                return usuario
        return None

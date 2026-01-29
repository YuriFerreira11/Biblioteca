import json
import os

import mysql.connector

# 1️⃣ Conectar ao MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="biblioteca"
)

cursor = conn.cursor()

# 2️⃣ Abrir o JSON
with open("Nomes.json", "r", encoding="utf-8") as f:
    usuarios = json.load(f)

# 3️⃣ Inserir no banco
sql = "INSERT INTO usuarios (id, nome, idade) VALUES (%s, %s, %s)"

for u in usuarios:
    try:
        cursor.execute(sql, (u["ID"], u["Nome"], u["Idade"]))
    except mysql.connector.errors.IntegrityError:
        print(f"Usuário {u['ID']} já existe, pulando...")

conn.commit()

cursor.close()
conn.close()

print("Migração concluída!")

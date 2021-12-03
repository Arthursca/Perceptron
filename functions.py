import tkinter as tk
from tkinter import messagebox
import pandas as pd


#Carrega os dados do Excel
def LoadExcel(tb, file_path = None, df = None):
    if df is None:
        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".csv":
                df = pd.read_csv(excel_filename)
            else:
                df = pd.read_excel(excel_filename)

        #Caso o arquivo seja invalido
        except ValueError:
            tk.messagebox.showerror("Information", "Arquivo invalido")
            return None

        #Caso não enconre o arquivo
        except FileNotFoundError:
            tk.messagebox.showerror("Information", f"Arquivo não encontrado em {file_path}")
            return None

    #Limpa a tabela
    clear_data(tb)

    #Preenche os novos dados da Tabela
    tb["column"] = list(df.columns)
    tb["show"] = "headings"
    for column in tb["columns"]:
        tb.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tb.insert("", "end", values=row)
    return None

#Limpa a tabela
def clear_data(tb):
    tb.delete(*tb.get_children())
    return None
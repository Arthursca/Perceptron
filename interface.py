import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import functions as gr
import perceptron as pc


# Inicia a Interface
app = tk.Tk()
app.title('Perceptron')
app.geometry("500x500")
app.pack_propagate(False)
app.resizable(0, 0)

# Area da Tabela de Excel
frame1 = tk.LabelFrame(app, text="Excel Data")
frame1.place(height=400, width=250 , relx = 0.5)
tb = ttk.Treeview(frame1)
tb.place(relheight=1, relwidth=1)
treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tb.yview)
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tb.xview)
tb.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")

#Area do arquivo a ser recebido pelo usuario
dados = tk.LabelFrame(app, text="Arquivo")
dados.place(height=100, width=500, rely=0.80, relx=0)

#Botão de buscar o arquivo excel
b1 = tk.Button(dados, text="Browse", command=lambda: OpenFile(tb))
b1.place(rely=0.65, relx=0.30)

#mostra o caminho ate o arquivo
path = ttk.Label(dados, text="Path")
path.place(rely=0, relx=0)

#Carrega a tela com o resultado do Perceptron
b2 = tk.Button(dados, text="Load")
b2.place(rely=0.65, relx=0.50)
b2.bind("<Button>",
        lambda e: Results(app))

#Area das variaveis a ser recebido pelo usuario
dados = tk.LabelFrame(app, text="Variaveis")
dados.place(height=400, width=250, rely=0, relx=0)

#x0
x0Label = ttk.Label(dados, text="x0: ")
x0Label.place(rely=0.1, relx=0.1)
x0 = tk.Spinbox(
    dados,
    from_=-1,
    to=1,
    increment=0.1,
    format='%1.1f',
)
x0.place(rely=0.1, relx=0.2)

#alfaLabel
alfaLabel = ttk.Label(dados, text="alfa: ")
alfaLabel.place(rely=0.4, relx=0.1)
alfa = tk.Spinbox(
    dados,
    from_=-1,
    to=1,
    increment=0.1,
    format='%1.1f'
)
alfa.place(rely=0.4, relx=0.22)

#Θ
tetaLabel = ttk.Label(dados, text="Θ: ")
tetaLabel.place(rely=0.7, relx=0.1)
teta = tk.Spinbox(
    dados,
    from_=-1,
    to=1,
    increment=0.1,
    format='%1.1f'
)
teta.place(rely=0.7, relx=0.2)

#Tela com o resultado
class Results(tk.Toplevel):

    def __init__(self, master=None):

        #pega os dados do perceptron
        dados, W, target = pc.getDados(path["text"],float(x0.get()))
        df = pc.getResult(dados,W,target,float(alfa.get()), float(teta.get()))

        # Inicia a Tela
        super().__init__(master=master)
        self.title("Resultado")
        self.geometry("500x500")

        nb = ttk.Notebook(self)
        nb.place(relx=0, rely=0, width=1280, height=600)

        janela1 = tk.Frame(nb)
        nb.add(janela1,text= "Tabela")


        # Mosta a tabela com o resultado
        frame2 = tk.LabelFrame(janela1, text="Excel Data")
        frame2.place(height=580, width=1280, rely=0)
        tb2 = ttk.Treeview(frame2)
        tb2.place(relheight=1, relwidth=1)
        treescrolly2 = tk.Scrollbar(frame2, orient="vertical", command=tb2.yview)
        treescrollx2 = tk.Scrollbar(frame2, orient="horizontal", command=tb2.xview)
        tb2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
        treescrollx2.pack(side="bottom", fill="x")
        treescrolly2.pack(side="right", fill="y")
        gr.LoadExcel(tb= tb2, df= df)

        janela2 = tk.Frame(nb)
        nb.add(janela2, text="Grafico")



#Busca o arquivo Excel e carrega seus Dados
def OpenFile(tb):
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    path["text"] = filename
    gr.LoadExcel(tb=tb ,file_path= filename)
    return None

app.mainloop()
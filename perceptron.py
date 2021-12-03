import pandas as pd
import numpy as np

#Pega os Dados , os pesos inicias e o target
def getDados(path, x0):

    dados = pd.read_excel(path)
    target = dados.pop('target')
    dados['x0'] = x0
    dados = dados.reindex(sorted(dados.columns), axis=1)
    W = np.array([0 for i in range(len(dados.columns))])
    return dados , W, target

#Calcula a soma dos produtos entre as variaveis e seus respectivos pesos
def weightedSum(line, W):
    s = 0
    if(len(line) == len(W)):
        for i in range(len(line)):
            s += line[i]*W[i]
    return s

#Calcula o valor do Network
def getNetwork(s, t):
    if s > t:
        return 1
    else:
        return 0

#Calcula o Valor do Erro
def getErro(z, n):
    return z - n

#Calcula o valor da correção
def getCorrection(e, A):
    return e*A

#Calcula o valor dos novos pesos
def newWeights(line, W, correction):
    new_W = list()
    for i in range(len(line)):
        new_W.append(W[i] + correction * line[i] )
    return new_W

#Escreve uma linha com os dados Obtidos
def getOutput(line, W, target, s, n, e, c, new_W):
    output = dict()

    for i in range(len(line)):
        output['X' + str(i)] = line[i]

    for i in range(len(W)):
        output['W_inicial ' + str(i)] = W[i]

    output['Target'] = target
    output['Soma'] = s
    output['Network'] = n
    output['Erro'] = e
    output['Correção'] = c
    for i in range(len(new_W)):
        output['W_final ' + str(i)] = new_W[i]

    return [output]

#Retorna a tabela com todos os passos feitos para chegar no resultado
def getResult(dados, W, y, A, t):
    df = pd.DataFrame()
    check = len(dados.index)
    count = 100
    while check != 0:
        for i in range(len(dados.index)):
            line = dados.loc[i, :].values
            s = weightedSum(line, W)
            n = getNetwork(s, t)
            e = getErro(y[i], n)
            c = getCorrection(e, A)
            new_W = newWeights(line, W, c)
            o = getOutput(line, W, y[i], s, n, e, c, new_W)
            df = df.append(o, ignore_index=True)
            W = new_W
            if e == 0:
                check -= 1

            else:
                check = len(dados.index)

            if check == 0:
                break

        count -= 1
        if count == 0:
            break
    print(df)
    return df

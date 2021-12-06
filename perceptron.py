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
    p = np.multiply(line, W)
    s = np.sum(p)
    return s
#Calcula o valor do Network
def getNetwork(s, threshold):
    if s > threshold:
        return 1
    else:
        return -1

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
def getOutput(line, W, target, s, network, erro, correction, new_W):
    output = dict()
    for i in range(len(line)):
        output['X' + str(i)] = line[i]
    for i in range(len(W)):
        output['Wi' + str(i)] = W[i]
    output['Alvo'] = target
    output['Soma'] = s
    output['Network'] = network
    output['Erro'] = erro
    output['Correção'] = correction
    for i in range(len(new_W)):
        output['Wf' + str(i)] = new_W[i]
    return [output]

#Retorna a tabela com todos os passos feitos para chegar no resultado
def getResult(dados, W, target, alpha, threshold):
    df = pd.DataFrame()
    check = 0
    while check < len(dados):

        for i in range(len(dados.index)):
            line = dados.loc[i].values
            s = weightedSum(line, W)
            network = getNetwork(s, threshold)
            erro = getErro(target[i], network)
            correction = getCorrection(erro, alpha)
            new_W = newWeights(line, W, correction)
            output = getOutput(line, W, target[i], s, network, erro, correction, new_W)
            df = df.append(output, ignore_index=True)
            W = new_W
            if erro == 0:
                check += 1
            else:
                check = 0
            if check == len(dados):
                break
    return df, W

def separator(dados, slope, intercept):
    g1 = dict()
    g1['x'] = list()
    g1['y'] = list()
    g2 = dict()
    g2['x'] = list()
    g2['y'] = list()
    y_f = list()
    for d in dados.iterrows():
        data = d[1]
        y_t1 = -(slope*data['x1']) + (intercept)*data['x0']
        y_f.append(-y_t1)

        if data['x2'] < y_t1:

            g1['x'].append(data['x1'])
            g1['y'].append(data['x2'])
        else:
            g2['x'].append(data['x1'])
            g2['y'].append(data['x2'])
    return g1, g2, y_f
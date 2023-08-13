import requests
import json

def lista_moedas():
    with open('moedas.json','r',encoding='utf-8') as arquivo:
        moedas = json.load(arquivo)
        lista = [valor.split('/')[0] for chave,valor in moedas.items()]
        lista_organizada = sorted(list(set(lista)))
    return lista_organizada

def combinacoes_disponiveis(moeda):
    with open('moedas.json','r',encoding='utf-8') as arquivo:
        moedas = json.load(arquivo)
        combinacoes = [valor.split('/')[1] for valor in moedas.values() if valor.split('/')[0] == moeda]
        combinacoes_ordenadas = sorted(combinacoes)
    
    return combinacoes_ordenadas

def sigla_cotacao(moeda_1, moeda_2):
    with open('moedas.json','r',encoding='utf-8') as arquivo:
        moedas = json.load(arquivo)
        try:
            moeda_procurada = moeda_1 + '/' + moeda_2
            sigla = [sigla for sigla,moeda in moedas.items() if moeda == moeda_procurada]
            return {'sigla':sigla[0]}
        except IndexError:            
            try:
                moeda_procurada_invertida = moeda_2 + '/' + moeda_1
                sigla_invertida = [sigla for sigla,moeda in moedas.items() if moeda == moeda_procurada_invertida]
                return {'sigla invertida':sigla_invertida[0]}
            except IndexError:
                return None

def cotacao_moeda(window, sigla_moeda, quantidade):
    try:
        chave = list(sigla_moeda.keys())[0]
        sigla = list(sigla_moeda.values())[0]
        url = f'http://economia.awesomeapi.com.br/json/last/{sigla}'
        cotacao = requests.get(url).json()[sigla.replace('-','')]['ask']
        if chave == 'sigla':
            resultado = float(cotacao)*float(quantidade)
            resposta = f'{"{:.2f}".format(resultado) if not resultado < 0.01 else "{:.5f}".format(resultado)}'
            window.write_event_value('finalizado',resposta)
        else:
            resultado = float(quantidade)/float(cotacao)
            resposta = f'{"{:.2f}".format(resultado) if not resultado < 0.01 else "{:.5f}".format(resultado)}'
            window.write_event_value('finalizado',resposta)
    except AttributeError:
        window.write_event_value('Liberar','')
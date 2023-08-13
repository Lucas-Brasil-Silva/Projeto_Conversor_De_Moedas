import PySimpleGUI as sg
from os import linesep
from utiliti import cotacao_moeda, lista_moedas, sigla_cotacao, combinacoes_disponiveis
from threading import Thread

sg.theme('Topanga')

def window_inicial():
    layout = [
        [sg.Text('Digite o valor que será convertido')],
        [sg.Input(size=(27,1), key='Valor')],
        [sg.Text(f'Escolha a primeira moeda,depois\nClique no botão 2° Moeda')],
        [sg.Combo(values=lista_moedas(),default_value='1° Moeda',size=(25,1), key='Moeda 1', readonly=True)],
        [sg.Button('2° Moeda', key='Liberar'),sg.Text(),sg.Button('⬇⬆', key='Inverter', disabled=True)],
        [sg.Combo(values=[],size=(25,1),disabled=True, key='Moeda 2',default_value='2° Moeda', readonly=True)],
        [sg.Button('Converter', disabled=False)],
        [sg.Text(key='Resultado')]
    ]

    return sg.Window('Conversor de Moedas', layout, finalize=True)

window = window_inicial()

def main():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Liberar':
            if not values['Moeda 1'] in ['1° Moeda','']:
                window['Moeda 2'].update(disabled=False)
                window['Inverter'].update(disabled=False)
                window['Converter'].update(disabled=False)
                window['Moeda 2'].update(values=combinacoes_disponiveis(values['Moeda 1']))
            else:
                sg.popup('Escolha alguma moeda no campo 1° Moeda!', title='Escolher 1° Moeda')

        elif event == 'Converter':
            try:
                if values['Moeda 2']:
                    primeira_moeda = values['Moeda 1']
                    segunda_moeda = values['Moeda 2']
                    valor = f"{float(values['Valor'].replace(',','.')) if not values['Valor'] in ['','0'] and float(values['Valor'].replace(',','.')) else 1}"
                    sigla = sigla_cotacao(primeira_moeda,segunda_moeda)
                    funcao = Thread(target=cotacao_moeda,args=(window,sigla,valor),daemon=True)
                    funcao.start()
                else:
                    sg.popup('Clique no campo 2° Moeda para escolher uma 2° Moeda',title='Escolha a 2° Moeda')
            except ValueError:
                sg.popup('Digite apenas números no campo valor!',title='Número Invalido')
                window['Valor'].update('')

        elif event == 'finalizado':
            if not values['Moeda 2'] in ['2° Moeda',''] and not values['Moeda 1'] in ['1° Moeda','']:
                window['Resultado'].update(
                f'{values["Valor"].replace(",",".")} {primeira_moeda} corresponde a{linesep}{values["finalizado"]} {segunda_moeda}', text_color='white')
            else:
                window['Resultado'].update(
                f'1 Dólar americano corresponde a{linesep}{values["finalizado"]} Real brasileiro', text_color='white')
        
        elif event == 'Inverter':
            window['Moeda 1'].update(values['Moeda 2'])
            window['Moeda 2'].update(values['Moeda 1'])

if __name__ == '__main__':
    main()
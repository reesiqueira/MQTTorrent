from main.configs.broker_configs import mqtt_broker_configs
import json
import glob
import base64
import os
import math

# Supondo que este arquivo está em "programa/main/mqtt_connection, volta 2 pastas para pegar o dir"
dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Variáveis globais
part_size = 1000 * 1024 # 1 Mb por parte
received_parts = {}

# Funções callback
def on_connect_all_response(client, userdata, flags, rc):
    if rc == 0:
        print(f'Cliente conectado com Sucesso')
    else:
        print(f'Erro ao me conectar, codigo: {rc}')

def on_message_all_response(client, userdata, message):
    # Salva a mensagem em json e divide o tópico em partes
    message_payload = json.loads(message.payload.decode('utf-8'))
    topico = message.topic
    reqOuRes = topico.split('/')[0]
    tipo = topico.split('/')[1]
    nome = topico.split('/')[2]
    ext = topico.split('/')[3]

    if reqOuRes == "request":
        # Define o cliente solicitante
        client_id = message_payload['client_id']

        # Procura o arquivo no dir+tipo, com o nome e extensão
        search_path = os.path.join(dir, tipo, nome + '.' + ext)
        file_list = glob.glob(search_path)

        # Se o arquivo existir
        if file_list:
            # Pega o primeiro arquivo que foi encontrado
            filepath = file_list[0]
            # Lê o arquivo
            with open(filepath, "rb") as file:
                file_data = file.read()
            # Calcula quantas partições de 1 Mb serão feitas
            total_parts = math.ceil(len(file_data) / part_size)
            # Para cada partição
            for part_num in range(total_parts):
                # Configura o inicio e o fim da partição
                start = part_num * part_size
                end = start + part_size
                file_part = file_data[start:end]
                # Codifica os dados da partição
                encoded_part = base64.b64encode(file_part).decode('utf-8')
                # Adiciona tudo em um json
                part_message = {
                    'total_parts': total_parts,
                    'part_num': part_num + 1,
                    'data': encoded_part
                }
                # Publica no canal do solicitante
                client.publish(
                    f"response/{tipo}/{nome}/{ext}/{client_id}", 
                    json.dumps(part_message)
                )
    elif reqOuRes == "response":
        # Extraindo dados do payload
        total_parts = message_payload['total_parts']
        part_num = message_payload['part_num']
        # Decodificando o conteúdo da mensagem
        data = base64.b64decode(message_payload['data'])

        # Construção da chave do arquivo
        file_key = f"{tipo}/{nome}.{ext}"
        
        # Criando um local para o arquivo ser armazenado
        if file_key not in received_parts:
            received_parts[file_key] = [None] * total_parts

        # Armazenando a parte recebida
        received_parts[file_key][part_num - 1] = data

        # Verifica se todas as partes foram recebidas
        if all(part is not None for part in received_parts[file_key]):
            # Remove assinatura do tópico de recebimento do arquivo
            client.unsubscribe(topico)
            # Reconstroi e salva o arquivo
            save_path = os.path.join(dir, tipo, nome + '.' + ext)
            with open(save_path, "wb") as file:
                for part in received_parts[file_key]:
                    file.write(part)
            # Deleta as partes recebidas da variavel global
            del received_parts[file_key]
            # Inscreve no tópico de request para virar um fornecedor
            #print(f'Me inscrevi no tópico request/{tipo}/{nome}/{ext}')
            client.subscribe(f"request/{tipo}/{nome}/{ext}", qos=2)
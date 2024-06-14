# Seminario MQTT - XRSC09 SISTEMAS DISTRIBUIDOS

**Projeto para a disciplina XRSC09 - SISTEMAS DISTRIBUIDOS ministrada pelo professor Rafael de Magalhaes Dias Frinhani**

**Alunos:**

- Breno Sampaio dos Santos
- Renan Siqueira de Oliveira Goncalves


## Instalando dependencias

*Para permitir o funcionamento da aplicacao sera necessario seguir alguns passos, selecione de acordo com seu sistema operacional para conseguir executar a funcionalidade*

### Windows

#### Instalando Python

- Acessar o [Site oficial](https://www.python.org/downloads/) e fazer o download da versao mais recente

#### Instalando o pip

- Caso o pip nao venha instalado com o python, deve seguir os deve se seguir os passos segundo a [Documentacao do pip](https://pip.pypa.io/en/stable/installation/)

### Linux

#### Instalando Python

Executar o seguinte comando no terminal:
```sh
sudo apt update
sudo apt-get install python
```

#### Instalando o pip

Caso o pip nao venha instalado com o python, deve se seguir os passos:

```sh
wget https://bootstrap.pypa.io/get-pip.py
python3 ./get-pip.py
```

Para mais informacoes acesse a [Documentacao do pip](https://pip.pypa.io/en/stable/installation/)

### Instalando bibliotecas com o pip

Executar o seguinte comando:

```sh
python3 pip -m install paho-mqtt
```

## Broker Mosquitto


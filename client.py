from main.publishers.publisher import Publisher
import time
import os

diretorioAtual = os.getcwd()

client = Publisher()

def requestFile():
    print("1 - filme\n2 - animação\n3 - desenho\n4 - logomarca\n")
    fileType = int(input('Escolha uma das opções acima: '))
    if(fileType == 1):
        fileTypeOption = "filme"
    if(fileType == 2):
        fileTypeOption = "animacao"
    if(fileType == 3):
        fileTypeOption = "desenho"
    if(fileType == 4):
        fileTypeOption = "logomarca"
    fileName = str(input('\nQual é o nome do arquivo que você procura?\n'))
    fileExt = str(input('\nQual é a extensão do arquivo que você procura?\n'))
    client.sendToRequestFileTopic(fileTypeOption + "/" + fileName + "/" + fileExt)

def uploadFile():
    print("1 - filme\n2 - animação\n3 - desenho\n4 - logomarca\n")
    fileType = int(input('Escolha uma das opções acima: '))
    if(fileType == 1):
        fileTypeOption = "filme"
    if(fileType == 2):
        fileTypeOption = "animacao"
    if(fileType == 3):
        fileTypeOption = "desenho"
    if(fileType == 4):
        fileTypeOption = "logomarca"
    fileName = str(input('\nDigite o nome do arquivo para o upload:\n'))
    fileExt = str(input('\nDigite a extensão do arquivo para o upload:\n'))
    client.sendToUploadFileTopic(fileTypeOption + "/" + fileName + "/" + fileExt)

opcao = None
while(opcao != 0):
    time.sleep(1)
    print("0 - Finalizar\n1 - Solicitar um arquivo\n2 - Disponibilizar um arquivo\n")
    opcao = int(input('Digite a opção: '))
    if(opcao == 1):
        requestFile()
    if (opcao == 2):
        uploadFile()
print('Até mais camarada!')
client.stop()

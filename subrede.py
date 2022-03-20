TAMANHO_BYTE = 8

class ClasseC:
    CLASSE = "Classe C"
    NUMERO_BYTES_HOST_ID = 1
    NUMERO_BYTES_NET_ID = 3
    
class ClasseB:
    CLASSE = "Classe B"
    NUMERO_BYTES_HOST_ID = 2
    NUMERO_BYTES_NET_ID = 2


class ClasseA:
    CLASSE = "Classe A"
    NUMERO_BYTES_HOST_ID = 3
    NUMERO_BYTES_NET_ID = 1
    

def converte_decimal_binario(numero_decimal):
    binario = "{0:b}".format(int(numero_decimal))
    
    return binario

def descobre_classe(binario):
    if binario.startswith("110"):
        return ClasseC()
    if binario.startswith("10"):
        return ClasseB()
    return ClasseA()

def converte_binario_para_byte(binario):
    return "0" * (8 - len(binario)) + binario

def descobre_endereco_em_binario(classe, endereco):
    endereco_em_binario = ""
    for i in range(classe.NUMERO_BYTES_NET_ID, 4):
        em_binario = converte_decimal_binario(endereco[i])
        endereco_em_binario += converte_binario_para_byte(em_binario)

    return endereco_em_binario
    
def descobre_numero_bits_emprestados(mascara_em_binario):
    numero_emprestados = 0
    for i in mascara_em_binario:
        numero_emprestados += int(i)
    return numero_emprestados

def descobre_host_id_subnet(endereco_ip, numero_bits_emprestados):
    return endereco_ip[numero_bits_emprestados:]

def converte_endereco_em_binario_byte(endereco):
    endereco_em_byte = ''
    for i in endereco:
        em_binario = converte_decimal_binario(i)
        endereco_em_byte += converte_binario_para_byte(em_binario) 
    
    return endereco_em_byte.strip()

def agrupa_em_bytes(endereco):
    return ["".join(endereco[i:i + TAMANHO_BYTE]) for i in range(0, len(endereco), TAMANHO_BYTE)]
def descobre_subrede(classe, endereco, numero_bits_emprestados):
    zerar_inicio = (classe.NUMERO_BYTES_NET_ID * TAMANHO_BYTE) + numero_bits_emprestados
    
    endereco = list(endereco)
    for i in range(zerar_inicio, len(endereco)):
        endereco[i] = "0"

    novo_endereco = agrupa_em_bytes(endereco) 
    return novo_endereco


endereco_ip = input("Endereço IP: ")
mascara     = input("Mascara: ")

endereco_ip = endereco_ip.split(".")
mascara = mascara.split(".")


### Primeiro passo, determinar qual classe que é
### Pego o primeiro byte do endereço IP, converto para binario e olho os primeiros digitos
### 0 = Classe A
### 10 = Classe B
### 110 = Classe C

primeiro_byte_ip_binario = converte_decimal_binario(endereco_ip[0])
classe = descobre_classe(primeiro_byte_ip_binario)

print("{} em binário é {}, portanto é classe {}".format(endereco_ip[0], primeiro_byte_ip_binario, classe.CLASSE))


# ### Descobrir quantos bytes estão sendo emprestados
mascara_em_binario = descobre_endereco_em_binario(classe, mascara)
numero_bits_emprestados = descobre_numero_bits_emprestados(mascara_em_binario)

print("Host id empresta {}".format(numero_bits_emprestados))
print("A organização pode ter até {} subredes".format(2 ** numero_bits_emprestados))

### Descobre qual host da subrede que está sendo endereçado
endereco_host_id_em_binario = descobre_endereco_em_binario(classe, endereco_ip)
host_id_subnet = descobre_host_id_subnet(endereco_host_id_em_binario, numero_bits_emprestados)
print("host id da subnet é {} - {}".format(int(host_id_subnet,2), host_id_subnet))


### Descobre qual é a subrede
endereco_ip_em_binario = converte_endereco_em_binario_byte(endereco_ip)
subrede = descobre_subrede(classe, endereco_ip_em_binario, numero_bits_emprestados)

subrede_em_decimal = []
for i in range(0, 4):
    subrede_em_decimal.append(str(int(subrede[i], 2)))
    
print("O endereço da subrede é {}".format(".".join(subrede_em_decimal)))



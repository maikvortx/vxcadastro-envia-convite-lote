import csv
import re
from herbs.Ok import Ok
from herbs.Err import Err
from cadastro_client import CadastroClient

token = 'WtvQqOSd3DGsw1AGDWQL70OBsRAnnW6alJ3mKMMwLta9VhXYn+tvEPZYZdKrQ87+nDcdwnqoQu8Fvxz9NVIW8sh+4JBz2cgXWnYUiEUvKcZjqCHAdUYwapwzfFnHBGZ+TefB9KiKI5WnRsB7qzlfm1jUUrGn2+2sMC6KpxTbRn39aaEaM3/pxoBnYTHsVP8UiR9yqnZybLAIQpGTUYcDtGo/CLypo5Vr0Ql+970ghj9FQc3Jxwcdk0pbhl+qqnPczXn3zC1RdHb5wDWSXJkAOQGLmQs5fttSkyVW7ieHS+LEkQEvdG8+VPWFXgEdgd6kiRbBSihZph67kiW+nk/DBACofgc4WA4yfGwwYkqO4dxJFunYqaIhZW+LcWDNUsvud+YTS04WnuoVbFi4PKw6YXyciO5OqXZOkM4h8f5wR5agDCpupqC9ZVaUK56+v99MWbFS+024Iq0aeZTT75lUcBcrpE9cIkczgtf1bsOfSxct7I00KKJLbZR2cqnHi0imQoCZNwhHNAak2cXivpmejjoE9s3w/rY8JoBrb0ZqorTG1slu17jnVqzwiJSBgthiHNShLzfuymJpvMsV+Jz/wbaqjdo3jBuPN9ZVs2Cah6YMNyisiyjnqpdZTNtUuwGIzAJpqLymPL+TaN5Dfxn1dSuSQyWK0jeqGduz7MKCuOuI4PifbDJ22YbToNTbGSd3zlynp4Dm/XMVVxvN+4CMxK/ZXjg7P4r5AGVpB/jHWdA3chKHgcPjagfgabs7z/Yh8myfgWP83R+QxsuQ+LyA1eDMki/C3XQkDWmXHIbQgoxWT/nxYmcax3iNctFzwS+IeS7W8s/chpHQ3uhUq06dY8+XY45FWpwNkO6w0M8/g9xn5pr9e9jKX2RoWCitJKcwkWkU/G/DiS5sDTexTQUH/F0nm+aGT6ppRqT7bAFLttOjMtCEGBBECV21UJ/26ruiBlh1is5cIwx1E3QoaP42o49gYW0R0jNevBA0o4gGNRQfYuXVCAaLZIWPmPRjoA4vE5R+WTcgjDGNgPaPl0+Vm2h7qUuGoQ4PM9j4EBj9S+3jLF6h48TcU002jWjFANrrp07d59kbLRZF11Nr43gkCUOy1ViEGieJCubx+iUOTMvBMbK0ZoVedJuu2KzLZf4gVVuNNM33Gkvo47RmaEGjDbdj3jv2LZ0rpXYyd+qThOI='
url_api = 'https://publicservices-stg.vortx.com.br/vxcadastro/api'
user_id = '116f3b57-2ab7-d34c-beb8-22420398be5a'
cadastro_client = CadastroClient(token, url_api, user_id)

def verifica_documento(documento):
    documento = re.sub(r'\D', '', documento)
    if len(documento) == 11:
        return 'Pessoa Física'
    elif len(documento) == 14:
        return 'PJ'
    else:
        return 'INVÁLIDO'


with open('documentos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')    
    for row in reader:
        documento = row['documento']
        email = row['email']
        tipo = verifica_documento(documento)
        if tipo == 'Pessoa Física':
            ret_api = cadastro_client.get_pessoa(documento)
        elif tipo == 'PJ':
            ret_api = cadastro_client.get_empresa(documento)
        else:
            print(f'Documento inválido: {documento}')
            continue        
        if ret_api.is_ok:
            print(f'Enviando atualização cadastral para o email {ret_api.value['email']} referente ao documento {documento}')
            ret_atualizacao_cadastral = cadastro_client.atualizar_cadastro(documento)
        else:
            print(f'Enviando novo convite {email} referente ao documento {documento}')
            ret_envia_convite = cadastro_client.enviar_convite(documento, email, tipo)

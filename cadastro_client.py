import re
import requests
import json
from herbs.Ok import Ok
from herbs.Err import Err

class CadastroClient:
    def __init__(self, token, url_api, user_id):
        self.token = token
        self.url_api = url_api 
        self.user_id = user_id
        self.headers = {
            'Authorization': f'Bearer {token}',         
            'Content-Type': 'Application/json'
        }        

    def get_pessoa(self, cpf):    
        url = f'{self.url_api}/person/person-by-document/{self.__removerMascaraDocumento(cpf)}'   
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Ok(response.json())
        
        return Err(response.json())

    def get_empresa(self, cnpj):    
        url = f'{self.url_api}/company/company-by-document/{self.__removerMascaraDocumento(cnpj)}'    
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Ok(response.json())
        
        return Err(response.json())

    def atualizar_cadastro(self, documento):    
        url = f'{self.url_api}/register/cadastral-update/{self.user_id}'    
        data = '{"funds":[],"investors":["' + self.__removerMascaraDocumento(documento) + '"]}'
        response = requests.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return Ok(response.json())
        
        return Err(response.json())

    def enviar_convite(self, documento, email, tipo):    
        input = {
            "socialNumber": documento,
            "email": email,
            "madeByRepresentative": None,
            "representative": {
                "email": None,
                "socialNumber": None
            },
            "isEscrow": None,
            "type": tipo,
            "distributor": {
                "distributorPersona": "Pessoa Física",
                "name": "VORTX DISTRIBUIDORA DE TITULOS E VALORES MOBILIARIOS LTDA",
                "document": "22.610.500/0001-88"
            },
            "isExternal": True,
            "reSendInvite": False,
            "check": True
        }
        
        url = f'{self.url_api}/invitation/send-invitation/{self.user_id}'
        response = requests.post(url, headers=self.headers, data=json.dumps(input))
        if response.status_code == 200:
            return Ok(response.json())
        
        return Err(response.json())
    
    def __removerMascaraDocumento(self, documento):
        return re.sub(r'\D', '', documento)
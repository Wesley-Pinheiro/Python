#INICIO PROJETO
#Wesley Adriano Pinheiro - pinheirocfc@gmail.com
#Python 3.8.3 32-bit 
#Visual Code 1.50.1
#https://github.com/TadaSoftware/PyNFe

###################################################################################### 0- BIBLIOTECAS - INICIO
#
#

#pip3 install --user https://github.com/TadaSoftware/PyNFe/archive/master.zip
#pip3 install --user -r https://github.com/TadaSoftware/PyNFe/raw/master/requirements-nfse.txt
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from pynfe.processamento.comunicacao import ComunicacaoSefaz

#
#
###################################################################################### 0- BIBLIOTECAS - FIM

###################################################################################### 1- VARIAVEIS GLOBAIS - INICIO
#
#

certificado = "//MeuComputador/meucertificado.pfx"
senha = 'MinhaSenha'
uf = 'sp' #estado
homologacao = False  #true = ambiente de homologacao #false = ambiente de producao 

#
#
###################################################################################### 1- VARIAVEIS GLOBAIS - FIM

###################################################################################### 3- REQUESTS - INICIO
#
#

#EXEMPLO 1 - Verifica Status da Sefaz  
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.status_servico('nfe')
print (xml.text) #mostra a resposta da solicitacao

#EXEMPLO 2 - Manifestacao do Destinatario
manif_dest = EventoManifestacaoDest(
	cnpj='1234567890000',                                # cnpj do destinatário
	chave='06262949502090920920209209209', # chave de acesso da nota
	data_emissao=datetime.datetime.now(),
	uf=uf,
	operacao=1                                                # - numero da operacao 
                                                              # 1=Confirmação da Operação
                                                              # 2=Ciência da Emissão
                                                              # 3=Desconhecimento da Operação
                                                              # 4=Operação não Realizada
    )
# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe_manif = serializador.serializar_evento(manif_dest)
# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe_manif)
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.evento(modelo='nfe', evento=xml)   # modelo='nfce' ou 'nfe'
print (envio.text) #mostra a resposta da solicitacao

#EXEMPLO 3 - Distribuicao NFe - download do XML por chave de acesso
CNPJ = '1234567890000' #Informar o CNPJ do destinatario
CHAVE = '06262949502090920920209209209' #Informar a chave de acesso da NFe
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_distribuicao(cnpj=CNPJ, chave=CHAVE)
resposta = etree.fromstring(xml.content)
ns = {'ns': NAMESPACE_NFE}
zip_resposta = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
des_resposta = DescompactaGzip.descompacta(zip_resposta)
print (etree.tostring(des_resposta).decode('utf-8')) #mostra a resposta da solicitacao

#EXEMPLO 4 - Carta de Correcao
carta_correcao = EventoCartaCorrecao(
	cnpj='1234567890000',                  # cpf ou cnpj do emissor
	chave='06262949502090920920209209209', # chave de acesso da nota
	data_emissao=datetime.datetime.now(),
	uf=uf,
	n_seq_evento=1,                                       #  
        correcao='Correção a ser considerada, texto livre. A correção mais recente substitui as anteriores.'
	)
# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe_cc = serializador.serializar_evento(carta_correcao)
# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe_cc)
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.evento(modelo='nfe', evento=xml) # modelo='nfce' ou 'nfe'
print(envio.text)  #mostra a resposta da solicitacao

#EXEMPLO 5 - Obtem a lista dos proximos 50 NSU comecando a partir do NSU X
CNPJ = '1234567890000' 
CHAVE = '' # deixar a chave de acesso vazia
ULT_NSU = 0
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_distribuicao(cnpj=CNPJ, chave=CHAVE, nsu=ULT_NSU)

#EXEMPLO 6 - Download de um NSU Especifico
CNPJ = '1234567890000' 
CHAVE = '' # deixar a chave de acesso vazia
NSU = 50123 # baixar o xml do NSU especifico
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_distribuicao(cnpj=CNPJ, chave=CHAVE, nsu=NSU)

#
#
###################################################################################### 3- REQUESTS - FIM



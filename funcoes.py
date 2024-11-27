from PyPDF2 import PdfReader, PdfWriter
import base64
import streamlit as st
from var_globais import *
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import  landscape, A4
from PIL import Image

c = canvas.Canvas(my_path, pagesize=landscape(A4), bottomup=0)


def fazerLme(paciente, mae, peso, altura, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6, clinica, cid_geral, medico):

    cid = cid_geral.split()[0]
    doenca = cid_geral.split(" - ")[1]


    
    if remedio1 =="":
        quantidade1=""
    if remedio2 =="":
        quantidade2=""
    if remedio3 =="":
        quantidade3=""
    if remedio4 =="":
        quantidade4=""
    if remedio5 =="":
        quantidade5=""
    if remedio6 =="":
        quantidade6=""

    match doenca:
        case "Doença renal crônica":
            anamnese = "Paciente com doença renal crônica em hemodiálise"
        case _:
            anamnese = f"Paciente com {doenca} em tratamento de manutenção"

    match medico:
        case "Caio Petrola":
            cns = "707.003.835.344.732"
        case _:
            cns =""
   
    match clinica:
        case "Clínica do Rim - Petrolina":
            cnes = "2349833"
        case "HU - Univasf":
            cnes = "6042414"
    # st.write(f"CNS: {cns}")
    # st.write(f"CNES da clínica: {cnes}")

    #iniciando a parte de preencher LMEs
    reader = PdfReader("lme_2022.pdf")
    writer = PdfWriter()

    page = reader.pages[0]
    fields = reader.get_fields()

    writer.add_page(page)

    writer.update_page_form_field_values(
        writer.pages[0], {"Altura": altura, 
                        "Peso": peso,
                        "Nome do paciente": paciente, 
                        "CNES": cnes, 
                        "Nome do estabelecimento de saúde": clinica, 
                        "Nome da mãe do paciente":mae, 
                        "CID": cid, 
                        "Diagnóstico": doenca, 
                        "Anamnese": anamnese,
                        "TextCNS": cns, "Nome do preencher": "preencher",#aparentemente não funciona
                        "Selecao med 1": remedio1,"Selecao med 2": remedio2, "Selecao med 3": remedio3,
                        "Selecao med 4": remedio4, "Selecao med 5": remedio5, "Selecao med 6": remedio6,
                        "Text18": quantidade4,
                        "Text19":quantidade4, "Text20": quantidade4, "Text21": "21","Text46": medico,"Text25b": "",#cpf do paciente = text25b
                        "Text25a": "aa",# aparentemente não funciona
                        "Text6": quantidade1, "Text7": quantidade1, "Text8": quantidade1, "Text10":quantidade2, "Text11":quantidade2, "Text12":quantidade2, "Text14":quantidade3, "Text15":quantidade3, "Text16":quantidade3,
                        "Text22": quantidade5, "Text23": quantidade5, "Text24":quantidade5, 
                        "med5":"26", #Aparentemente não funciona
                        "Text11a":quantidade2, "Text12a": quantidade2, "Text14a":quantidade3, "Text15a":quantidade3, "Text16a":quantidade3, "Text6a":quantidade1, "Text7a":quantidade1, "Text8a":quantidade1,
                        "Text6b":quantidade4, "Text7b":quantidade4, "Text8b":quantidade4, "Text10a":quantidade2, "Text10b":quantidade5, "Text11b":quantidade5, "Text12b":quantidade5,
                        "Text14b":quantidade6, "Text15b":quantidade6, "Text16b":quantidade6, "Text22a":quantidade6, "Text23a":quantidade6, "Text24a":quantidade6}
    )

   
    # write "output" to PyPDF2-output.pdf
    with open(f"{paciente}.pdf", "wb") as output_stream:
        writer.write(output_stream)

    # Fazendo o embeded PDF para visualizar o pdf no próprio site
    with open(f"{paciente}.pdf","rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
    #pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf"></iframe>'
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf"></embed>'

    st.markdown(pdf_display, unsafe_allow_html=True)


def fazerReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6 ):
    lista_remedios = [remedio1, remedio2, remedio3, remedio4, remedio5, remedio6]
    lista_quantidades = [quantidade1, quantidade2, quantidade3, quantidade4, quantidade5, quantidade6]
    aglomerado_inicial = list(zip(lista_remedios, lista_quantidades))
    aglomerado_final = [x for x in aglomerado_inicial if x[0]!="" ]
    dicio_remedios = dict(aglomerado_final)
    #st.write(dicio_remedios["Alfaepoetina 4.000 UI injetável"])
    print(dicio_remedios)
    print (len(dicio_remedios))
    
    #Inicializando as variáveis zeradas
    hemax_total= "   "
    hemax_xsema= "   "
    
    norip_total= "   "
    norip_x15dias= "   "

    calcijex_total= "   "
    calcijex_dose= "   "
    
    paricalcitol_total= "   "
    paricalcitol_dose= "   "
    
    caco3_total= "____ "
    caco3_3xdia= "____ "

    sevelamer_total= "   "
    sevelamer_3xdia= "   "
    
    calcitriol_total= "   "
    calcitriol_dose= "   "
    
    cinacalcete_total= "   "
    cinacalcete_dia= "   "

    mmf_total= "   "
    mmf_dose= "   "
  
    aza_total= "   "
    aza_dose= "   "
  
    hcq_total= "   "
    hcq_dose= "   "
    
    csa100_total= "   "
    csa100_dose= "   "
    
    csa50_total= "   "
    csa50_dose= "   "
  
    csa25_total= "   "
    csa25_dose= "   "

    dapa10_total = "  "
    dapa10_dose = " "
    
    #Definindo parâmetros médicos para fazer o carimbo nas receitas
    if medico ==lista_medicos[0]:
        nome_medico = "Dr Caio Petrola"
        especialidade = "Nefrologista"
        crm = "CRM 15241-PE  21149-BA"
    elif medico ==lista_medicos[1]:
        nome_medico = "Dra Emília Diniz"
        especialidade = "Nefrologista"
        crm = "CRM 4715-PE"
    elif medico ==lista_medicos[2]:
        nome_medico = "Dr Mucio Homero"
        especialidade = "Nefrologista"
        crm = "CRM 12370-PE"
    elif medico ==lista_medicos[3]:
        nome_medico = "Dra Gloriete Vieira"
        especialidade = "Nefrologista"
        crm = "CRM 9766-PE"
     

     #Criando a lógica de preenchimento a partir do dicionario
    if lista_medicamentos[1] in dicio_remedios:
        hemax_total = dicio_remedios[lista_medicamentos[1]]
        hemax_xsema = int(dicio_remedios[lista_medicamentos[1]]/4)
        display_hemax=True
        

    if lista_medicamentos[2] in dicio_remedios:
        print("tem noripurum na área")
        norip_total = dicio_remedios[lista_medicamentos[2]]
        norip_x15dias = int(dicio_remedios[lista_medicamentos[2]]/2)
        display_norip=True
        
    if lista_medicamentos[3] in dicio_remedios:
        calcitriol_total = dicio_remedios[lista_medicamentos[3]]
        calcitriol_dose = int(dicio_remedios[lista_medicamentos[3]]//12)
        display_calcitriol=True

    if lista_medicamentos[4] in dicio_remedios:
        calcijex_total = dicio_remedios[lista_medicamentos[4]]
        calcijex_dose = int(dicio_remedios[lista_medicamentos[4]]/12)
        display_calcijex=True
        
    if lista_medicamentos[5] in dicio_remedios:
        sevelamer_total = dicio_remedios[lista_medicamentos[5]]
        sevelamer_3xdia = int(dicio_remedios[lista_medicamentos[5]]/90)
        display_sevelamer=True

    if lista_medicamentos[6] in dicio_remedios:
        cinacalcete_total = dicio_remedios[lista_medicamentos[6]]
        cinacalcete_dia = int(dicio_remedios[lista_medicamentos[6]]/30)
        display_cinacalcete=True

    if lista_medicamentos[7] in dicio_remedios:
        paricalcitol_total = dicio_remedios[lista_medicamentos[7]]
        paricalcitol_dose = int(dicio_remedios[lista_medicamentos[7]]/12)
        display_paricalcitol=True

    if lista_medicamentos[8] in dicio_remedios:
        mmf_total = dicio_remedios[lista_medicamentos[8]]
        mmf_dose = int(dicio_remedios[lista_medicamentos[8]]/60)
        display_mmf =True

    if lista_medicamentos[9] in dicio_remedios:
        aza_total = dicio_remedios[lista_medicamentos[9]]
        aza_dose = int(dicio_remedios[lista_medicamentos[9]]/30)
        display_aza=True

    if lista_medicamentos[10] in dicio_remedios:
        hcq_total = dicio_remedios[lista_medicamentos[10]]
        hcq_dose = int(dicio_remedios[lista_medicamentos[10]]/30)
        display_hcq=True

    if lista_medicamentos[11] in dicio_remedios:
        csa100_total = dicio_remedios[lista_medicamentos[11]]
        csa100_dose = int(dicio_remedios[lista_medicamentos[11]]/60)
        display_csa100=True

    if lista_medicamentos[12] in dicio_remedios:
        csa50_total = dicio_remedios[lista_medicamentos[12]]
        csa50_dose = int(dicio_remedios[lista_medicamentos[12]]/60)
        display_csa50=True

    if lista_medicamentos[13] in dicio_remedios:
        csa25_total = dicio_remedios[lista_medicamentos[13]]
        csa25_dose = int(dicio_remedios[lista_medicamentos[13]]/60)
        display_csa25=True

    if lista_medicamentos[14] in dicio_remedios:
        dapa10_total = dicio_remedios[lista_medicamentos[14]]
        dapa10_dose = int(dicio_remedios[lista_medicamentos[14]]/30)
        display_dapa10=True


    #Iniciando a parte em que preenche o pdf com as medicações
    #Definindo a altura para iniciar a escrever(x), a distância para a próxima linha(y) e a distância para o próximo item (z), todas em cm.
    x = 7.2
    y = 0.4
    z = 1.2

    # Iniciando a verificação de quais itens estão contidos no dicio_remedios, e produzindo o texto para cada um deles.
    for item in dicio_remedios:
        x = x + z
        linha1 = "" # zerando o texto da receita
        linha2 = "" # zerando o texto da receita
        if item == lista_medicamentos[1]:
            linha1 = f'Alfaepoetina     4.000 UI ______________________________{hemax_total} ampolas'
            linha2 = f'Fazer 01 FA SC {hemax_xsema} x por semana após hemodiálise.'
        elif item == lista_medicamentos[2]:
            linha1 =f'Sacarato de hidróxido de ferro 100 mg___________________ {norip_total} ampolas'
            linha2 =f'Fazer {norip_x15dias} ampola(s) a cada 15 dias.'
    
        elif item == lista_medicamentos[3]:
            linha1 = f'Calcitriol 0,25 mcg _____________________________________{calcitriol_total} caps.'
            linha2 = f'Tomar {calcitriol_dose} cápsula(s) após hemodiálise.'
    
        elif item == lista_medicamentos[4]:
            linha1 = f'fCalcijex 1 mcg   ____________________________________{calcijex_total}  ampolas'
            linha2 = f'Aplicar {calcijex_dose}  amp IV após hemodiálise.'
    
        elif item == lista_medicamentos[5]:
            linha1 = f'Sevelamer__________________________________________{sevelamer_total} comps.'
            linha2 = f'Tomar {sevelamer_3xdia}  comprimido(s) 3 vezes ao dia (junto com as refeições).'
    
        elif item == lista_medicamentos[6]:
            linha1 = f'Cloridrato de cinacalcete 30mg¬¬¬________________________{cinacalcete_total} comps.' 
            linha2 = f'Tomar {cinacalcete_dia} comprimido(s) 1x ao dia.'
    
        elif item == lista_medicamentos[7]:
            linha1 = f'Paricalcitol 5mcg/ml__________________________________{paricalcitol_total} ampolas'
            linha2 = f'Fazer   {paricalcitol_dose}   amp IV após hemodiálise.'
    
        elif item == lista_medicamentos[8]:
            linha1 = f'Micofenolato de mofetila  500mg ____________________{mmf_total} comprs'
            linha2 =f'Tomar {mmf_dose} comprimido(s) 12/12h.'
    
        elif item == lista_medicamentos[9]:
            linha1 = f'Azatioprina 50mg ________________________________{aza_total} comprs'
            linha2 = f'Tomar {aza_dose} comprimido(s) 1 x ao dia.'
    
        elif item == lista_medicamentos[10]:
            linha1 = f'Hidroxicloroquina 400mg __________________________{hcq_total} comprs'
            linha2 = f'Tomar {hcq_dose} comprimido 1 vez ao dia.'
    
        elif item == lista_medicamentos[11]:
            linha1 = f'Ciclosporina 100mg _____________________________{csa100_total} comprs'
            linha2 = f'Tomar {csa100_dose} comprimido(s) 12/12h.'
    
        elif item == lista_medicamentos[12]:
            linha1 = f'Ciclosporina 50mg ______________________________{csa50_total} comprs'
            linha2 = f'Tomar {csa50_dose} comprimido(s) 12/12h.'
    
        elif item == lista_medicamentos[13]:
            linha1 = f'Ciclosporina 25mg ______________________________{csa25_total} comprs'
            linha2 = f'Tomar {csa25_dose} comprimido(s) 12/12h.'
    
        elif item == lista_medicamentos[14]:
            linha1 = f'Dapagliflozina 10mg ______________________________{dapa10_total} comprs'
            linha2 = f'Tomar {dapa10_dose} comprimido(s) 1 vez ao dia.'
    
       
        #iniciar nesse nível o acréscimo do "texto" ao pdf
        c.drawString(1*cm, x*cm, linha1)
        c.drawString(1*cm, (x+y)*cm, linha2)
        c.drawString(16*cm, x*cm, linha1)
        c.drawString(16*cm, (x+y)*cm, linha2)
    c.setFontSize(10)
    c.drawString((centro_direita -3)*cm, (altura_cabecalho+3.2)*cm, paciente)
    c.drawString((centro_esquerda -3)*cm, (altura_cabecalho+3.2)*cm, paciente)
    
    # Fazendo o carimbo no final da página. O motivo do loop é fazer nas duas páginas
    j=0
    for i in range(2):
        c.saveState()
        c.translate((12+j)*cm, 17.5*cm)
        c.rotate(-45)
        c.setFont("Times-Roman",9)
        c.drawCentredString(0,0,nome_medico)
        c.drawCentredString(0,10,especialidade)
        c.setFont("Times-Roman",7)
        c.drawCentredString(0,20,crm)
        c.restoreState()
        j=j+metade_pagina


def gerarPdfReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6):
    #my_path = "receituario_template.pdf"

    #c = canvas.Canvas(my_path, pagesize=landscape(A4), bottomup=0)
    #c.translate(cm, cm)
    c.setTitle("Receituário")
    c.line(15*cm, 0, 15*cm, 21*cm)
    c.setFont("Helvetica", 9)
    #Inserindo imagem do cabeçalho
    #Primeiro, precisa virar a imagem, por causa da configuração bottomup =0
    #A imagem precisa ficar antes das linhas,para evitar que o "branco" da imagem fique por cima das linhas
    def flip_image(image_path):
        img = Image.open(image_path)
        out = img.transpose(Image.FLIP_TOP_BOTTOM)
        
        output_path = "flipped_" + image_path  # Specify the output file path here
        out.save(output_path)  # Save the image using the output file path
        
        return output_path  # Return the output file path


    image = flip_image('cabecalho.jpg')
    c.drawImage(image,1,8)
    c.drawImage(image,15*cm,8)
    #c.drawImage('cabecalho.jpg',6, 8)


    #Cabeçalho do receituário da direita
    c.drawCentredString(centro_direita*cm, (altura_cabecalho+0)*cm, "AMBULATÓRIO")
    c.drawCentredString(centro_direita*cm, (altura_cabecalho+0.4)*cm, "HOSPITAL UNIVERSITARIO")
    c.drawCentredString(centro_direita*cm, (altura_cabecalho+0.8)*cm, "Av. José de Sá Maniçoba, S/n - Centro - 56304-205 Petrolina - PE")
    c.drawCentredString(centro_direita*cm, (altura_cabecalho+1.2)*cm, "(87)2101-6511/2101-6500")
    c.drawCentredString(centro_direita*cm, (altura_cabecalho+2.2)*cm, "RECEITUÁRIO")
    c.drawString((centro_direita-4.5)*cm, (altura_cabecalho+3.2)*cm, "Paciente:")
    c.line((centro_direita-5)*cm, 2.5*cm, (centro_direita+5)*cm, 2.5*cm) #linha de cima
    c.line((centro_direita-5)*cm, 6.7*cm, (centro_direita+5)*cm, 6.7*cm) #linha de baixo
    c.line((centro_direita-5)*cm, 2.5*cm, (centro_direita-5)*cm, 6.7*cm) #linha da direita
    c.line((centro_direita+5)*cm, 2.5*cm, (centro_direita+5)*cm, 6.7*cm) #linha da esquerda

    #Cabeçalho do receituário da esquerda
    c.drawCentredString(centro_esquerda*cm, (altura_cabecalho+0)*cm, "AMBULATÓRIO")
    c.drawCentredString(centro_esquerda*cm, (altura_cabecalho+0.4)*cm, "HOSPITAL UNIVERSITARIO")
    c.drawCentredString(centro_esquerda*cm, (altura_cabecalho+0.8)*cm, "Av. José de Sá Maniçoba, S/n - Centro - 56304-205 Petrolina - PE")
    c.drawCentredString(centro_esquerda*cm, (altura_cabecalho+1.2)*cm, "(87)2101-6511/2101-6500")
    c.drawCentredString(centro_esquerda*cm, (altura_cabecalho+2.2)*cm, "RECEITUÁRIO")
    c.drawString((centro_esquerda-4.5)*cm, (altura_cabecalho+3.2)*cm, "Paciente:")
    c.line((centro_esquerda-5)*cm, 2.5*cm, (centro_esquerda+5)*cm, 2.5*cm) #linha de cima
    c.line((centro_esquerda-5)*cm, 6.7*cm, (centro_esquerda+5)*cm, 6.7*cm) #linha de baixo
    c.line((centro_esquerda-5)*cm, 2.5*cm, (centro_esquerda-5)*cm, 6.7*cm) #linha da direita
    c.line((centro_esquerda+5)*cm, 2.5*cm, (centro_esquerda+5)*cm, 6.7*cm) #linha da esquerda

    




    fazerReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6 )


    c.showPage()
    c.save()

    # Fazendo o embeded PDF para visualizar o pdf no próprio site
    with open('receituario_template.pdf',"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
    pdf_display_receituario = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1200" height="800" type="application/pdf"></embed>'

    st.markdown(pdf_display_receituario, unsafe_allow_html=True)

from PyPDF2 import PdfReader, PdfWriter, generic
import base64
import streamlit as st
from var_globais import *
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import  landscape, A4
from PIL import Image
import io

def set_need_appearances_writer(writer):
    try:
        catalog = writer._root_object
        # AcroForm é onde ficam as informações do formulário
        if '/AcroForm' not in catalog:
            catalog.update({
                generic.NameObject('/AcroForm'): generic.DictionaryObject()
            })
        if '/NeedAppearances' not in catalog['/AcroForm']:
            catalog['/AcroForm'].update({
                generic.NameObject('/NeedAppearances'): generic.BooleanObject(True)
            })
        return writer
    except Exception as e:
        print('Erro ao definir NeedAppearances:', repr(e))
        return writer

def parametros_carimbo(medico):
    # Definindo parâmetros médicos para fazer o carimbo nas receitas
    if medico == lista_medicos[0]:
        nome_medico = "Dr Caio Petrola"
        especialidade = "Nefrologista"
        crm = "CRM 15241-PE  21149-BA"
    elif medico == lista_medicos[1]:
        nome_medico = "Dra Emília Diniz"
        especialidade = "Nefrologista"
        crm = "CRM 4715-PE"
    elif medico == lista_medicos[2]:
        nome_medico = "Dr Mucio Homero"
        especialidade = "Nefrologista"
        crm = "CRM 12370-PE"
    elif medico == lista_medicos[3]:
        nome_medico = "Dra Gloriete Vieira"
        especialidade = "Nefrologista"
        crm = "CRM 9766-PE"
    elif medico == lista_medicos[4]:
        nome_medico = "Dra Rita Duarte"
        especialidade = "Reumatologista"
        crm = "CRM 16629-PE 33562-BA"
    return nome_medico, especialidade, crm

def carimbar(nome_medico, especialidade, crm):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    # Defina o texto do carimbo e sua posição no template
    # Salvar o estado atual do canvas
    can.saveState()
    # Mover a origem para a posição desejada do carimbo
    can.translate(460, 215)
    # Rotacionar o sistema de coordenadas
    can.rotate(10)
    # Desenhar o texto do carimbo rotacionado
    can.setFont("Times-Roman", 9)
    can.drawCentredString(0, 0, f"{nome_medico}")
    can.drawCentredString(0, -10, f"{especialidade}")
    can.drawCentredString(0, -20, f"{crm}")
    # Restaurar o estado original do canvas
    can.restoreState()
    # Salvar o carimbo em memória
    can.save()
    packet.seek(0)
    # Retornar o buffer em memória que contém o carimbo
    return packet

def fazerLme(paciente, mae, peso, altura, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6, clinica, cid_geral, medico):
    cid = cid_geral.split()[0]
    doenca = cid_geral.split(" - ")[1]

    if remedio1 == "":
        quantidade1 = ""
    if remedio2 == "":
        quantidade2 = ""
    if remedio3 == "":
        quantidade3 = ""
    if remedio4 == "":
        quantidade4 = ""
    if remedio5 == "":
        quantidade5 = ""
    if remedio6 == "":
        quantidade6 = ""

    match doenca:
        case "Doença renal crônica":
            anamnese = "Paciente com doença renal crônica em hemodiálise"
        case _:
            anamnese = f"Paciente com {doenca} em tratamento de manutenção"

    match medico:
        case "Caio Petrola":
            cns = "707.0038.3534.4732"
            index_lista_medicos = 0
        case "Maria Emilia Diniz":
            cns = "709.8090.1955.9991"
            index_lista_medicos = 1
        case "Mucio Homero L. R. Ribeiro":
            cns = "704.8030.4895.4848"
            index_lista_medicos = 2
        case "Gloriete Vieira de Oliveira":
            cns = "707.4000.8208.5577"
            index_lista_medicos = 3
        case "Rita Marina Soares de Castro Duarte":
            cns = "708.4037.3810.1264"
            index_lista_medicos = 4
        case _:
            cns = ""
            index_lista_medicos = None

    match clinica:
        case "Clínica do Rim - Petrolina":
            cnes = "2349833"
        case "HU - Univasf":
            cnes = "6042414"

    # Iniciando a parte de preencher LMEs
    reader = PdfReader("lme_2022.pdf")
    writer = PdfWriter()

    # Comando para tentar não dar erro ao imprimir no Firefox
    set_need_appearances_writer(writer)

    page = reader.pages[0]
    fields = reader.get_fields()

    writer.add_page(page)

    writer.update_page_form_field_values(
        writer.pages[0], {"Altura": altura,
                          "Peso": peso,
                          "Nome do paciente": paciente,
                          "CNES": cnes,
                          "Nome do estabelecimento de saúde": clinica,
                          "Nome da mãe do paciente": mae,
                          "CID": cid,
                          "Diagnóstico": doenca,
                          "Anamnese": anamnese,
                          "TextCNS": cns, "Nome do preencher": "preencher",  # aparentemente não funciona
                          "Selecao med 1": remedio1, "Selecao med 2": remedio2, "Selecao med 3": remedio3,
                          "Selecao med 4": remedio4, "Selecao med 5": remedio5, "Selecao med 6": remedio6,
                          "Text18": quantidade4,
                          "Text19": quantidade4, "Text20": quantidade4, "Text21": "21", "Text46": medico, "Text25b": "",  # cpf do paciente = text25b
                          "Text25a": "aa",  # aparentemente não funciona
                          "Text6": quantidade1, "Text7": quantidade1, "Text8": quantidade1, "Text10": quantidade2, "Text11": quantidade2, "Text12": quantidade2, "Text14": quantidade3, "Text15": quantidade3, "Text16": quantidade3,
                          "Text22": quantidade5, "Text23": quantidade5, "Text24": quantidade5,
                          "med5": "26",  # Aparentemente não funciona
                          "Text11a": quantidade2, "Text12a": quantidade2, "Text14a": quantidade3, "Text15a": quantidade3, "Text16a": quantidade3, "Text6a": quantidade1, "Text7a": quantidade1, "Text8a": quantidade1,
                          "Text6b": quantidade4, "Text7b": quantidade4, "Text8b": quantidade4, "Text10a": quantidade2, "Text10b": quantidade5, "Text11b": quantidade5, "Text12b": quantidade5,
                          "Text14b": quantidade6, "Text15b": quantidade6, "Text16b": quantidade6, "Text22a": quantidade6, "Text23a": quantidade6, "Text24a": quantidade6}
    )

    lme_pdf_filename = f"{paciente}.pdf"
    # write "output" to PyPDF2-output.pdf
    with open(lme_pdf_filename, "wb") as output_stream:
        writer.write(output_stream)

    # Só faça o carimbo se o índice do médico for válido (não for None)
    if index_lista_medicos is not None:
        nome_medico, especialidade, crm = parametros_carimbo(lista_medicos[index_lista_medicos])
        packet = carimbar(nome_medico, especialidade, crm)

        # Ler o PDF existente e o carimbo gerado
        original_pdf = PdfReader(lme_pdf_filename)
        overlay_pdf = PdfReader(packet)
        writer = PdfWriter()

        # Mesclar o carimbo com o PDF original
        for page_num in range(len(original_pdf.pages)):
            original_page = original_pdf.pages[page_num]
            if page_num == 0:  # Adiciona o carimbo apenas na primeira página
                overlay_page = overlay_pdf.pages[0]
                original_page.merge_page(overlay_page)
            writer.add_page(original_page)

        # Salvar o PDF final com o carimbo incluído
        final_pdf_filename = f"{paciente}_lme_carimbo.pdf"
        with open(final_pdf_filename, "wb") as output_stream:
            writer.write(output_stream)
    else:
        # Se não houver carimbo, continue com o arquivo original
        final_pdf_filename = lme_pdf_filename

    # Fazendo o embeded PDF para visualizar o pdf no próprio site
    with open(final_pdf_filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf"></iframe>'
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf"></embed>'

    st.markdown(pdf_display, unsafe_allow_html=True)
    # -------------------------------------------------------------
    # ADDED: botão de download para o PDF da LME
    # -------------------------------------------------------------
    st.download_button(
        label="Download LME (PDF)",
        data=base64.b64decode(base64_pdf),   # Convertemos de volta para bytes
        file_name=final_pdf_filename,        # Nome do arquivo de download
        mime="application/pdf"
    )


def fazerReceita(c, paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6):
    lista_remedios = [remedio1, remedio2, remedio3, remedio4, remedio5, remedio6]
    lista_quantidades = [quantidade1, quantidade2, quantidade3, quantidade4, quantidade5, quantidade6]
    aglomerado_inicial = list(zip(lista_remedios, lista_quantidades))
    aglomerado_final = [x for x in aglomerado_inicial if x[0] != ""]
    dicio_remedios = dict(aglomerado_final)

    # Inicializando as variáveis zeradas
    hemax_total = "   "
    hemax_xsema = "   "

    norip_total = "   "
    norip_x15dias = "   "

    calcijex_total = "   "
    calcijex_dose = "   "

    paricalcitol_total = "   "
    paricalcitol_dose = "   "

    caco3_total = "____ "
    caco3_3xdia = "____ "

    sevelamer_total = "   "
    sevelamer_3xdia = "   "

    calcitriol_total = "   "
    calcitriol_dose = "   "

    cinacalcete_total = "   "
    cinacalcete_dia = "   "

    mmf_total = "   "
    mmf_dose = "   "

    aza_total = "   "
    aza_dose = "   "

    hcq_total = "   "
    hcq_dose = "   "

    csa100_total = "   "
    csa100_dose = "   "

    csa50_total = "   "
    csa50_dose = "   "

    csa25_total = "   "
    csa25_dose = "   "

    dapa10_total = "  "
    dapa10_dose = " "

    # Definindo parâmetros médicos para fazer o carimbo nas receitas
    if medico == lista_medicos[0]:
        nome_medico = "Dr Caio Petrola"
        especialidade = "Nefrologista"
        crm = "CRM 15241-PE  21149-BA"
    elif medico == lista_medicos[1]:
        nome_medico = "Dra Emília Diniz"
        especialidade = "Nefrologista"
        crm = "CRM 4715-PE"
    elif medico == lista_medicos[2]:
        nome_medico = "Dr Mucio Homero"
        especialidade = "Nefrologista"
        crm = "CRM 12370-PE"
    elif medico == lista_medicos[3]:
        nome_medico = "Dra Gloriete Vieira"
        especialidade = "Nefrologista"
        crm = "CRM 9766-PE"
    elif medico == lista_medicos[4]:
        nome_medico = "Dra Rita Duarte"
        especialidade = "Reumatologista"
        crm = "CRM 16629-PE 33562-BA"

    # Criando a lógica de preenchimento a partir do dicionario
    if lista_medicamentos[1] in dicio_remedios:
        hemax_total = dicio_remedios[lista_medicamentos[1]]
        hemax_xsema = int(dicio_remedios[lista_medicamentos[1]] / 4)

    if lista_medicamentos[2] in dicio_remedios:
        norip_total = dicio_remedios[lista_medicamentos[2]]
        norip_x15dias = int(dicio_remedios[lista_medicamentos[2]] / 2)

    if lista_medicamentos[3] in dicio_remedios:
        calcitriol_total = dicio_remedios[lista_medicamentos[3]]
        calcitriol_dose = int(dicio_remedios[lista_medicamentos[3]] // 12)

    if lista_medicamentos[4] in dicio_remedios:
        calcijex_total = dicio_remedios[lista_medicamentos[4]]
        calcijex_dose = int(dicio_remedios[lista_medicamentos[4]] / 12)

    if lista_medicamentos[5] in dicio_remedios:
        sevelamer_total = dicio_remedios[lista_medicamentos[5]]
        sevelamer_3xdia = int(dicio_remedios[lista_medicamentos[5]] / 90)

    if lista_medicamentos[6] in dicio_remedios:
        cinacalcete_total = dicio_remedios[lista_medicamentos[6]]
        cinacalcete_dia = int(dicio_remedios[lista_medicamentos[6]] / 30)

    if lista_medicamentos[7] in dicio_remedios:
        paricalcitol_total = dicio_remedios[lista_medicamentos[7]]
        paricalcitol_dose = int(dicio_remedios[lista_medicamentos[7]] / 12)

    if lista_medicamentos[8] in dicio_remedios:
        mmf_total = dicio_remedios[lista_medicamentos[8]]
        mmf_dose = int(dicio_remedios[lista_medicamentos[8]] / 60)

    if lista_medicamentos[9] in dicio_remedios:
        aza_total = dicio_remedios[lista_medicamentos[9]]
        aza_dose = int(dicio_remedios[lista_medicamentos[9]] / 30)

    if lista_medicamentos[10] in dicio_remedios:
        hcq_total = dicio_remedios[lista_medicamentos[10]]
        hcq_dose = int(dicio_remedios[lista_medicamentos[10]] / 30)

    if lista_medicamentos[11] in dicio_remedios:
        csa100_total = dicio_remedios[lista_medicamentos[11]]
        csa100_dose = int(dicio_remedios[lista_medicamentos[11]] / 60)

    if lista_medicamentos[12] in dicio_remedios:
        csa50_total = dicio_remedios[lista_medicamentos[12]]
        csa50_dose = int(dicio_remedios[lista_medicamentos[12]] / 60)

    if lista_medicamentos[13] in dicio_remedios:
        csa25_total = dicio_remedios[lista_medicamentos[13]]
        csa25_dose = int(dicio_remedios[lista_medicamentos[13]] / 60)

    if lista_medicamentos[14] in dicio_remedios:
        dapa10_total = dicio_remedios[lista_medicamentos[14]]
        dapa10_dose = int(dicio_remedios[lista_medicamentos[14]] / 30)

    # Iniciando a parte em que preenche o pdf com as medicações
    # Definindo a altura para iniciar a escrever(x), a distância para a próxima linha(y) e a distância para o próximo item (z), todas em cm.
    x = 7.2
    y = 0.4
    z = 1.2

    # Iniciando a verificação de quais itens estão contidos no dicio_remedios, e produzindo o texto para cada um deles.
    for item in dicio_remedios:
        x = x + z
        linha1 = ""  # zerando o texto da receita
        linha2 = ""  # zerando o texto da receita
        if item == lista_medicamentos[1]:
            linha1 = f'Alfaepoetina     4.000 UI ______________________________{hemax_total} ampolas'
            linha2 = f'Fazer 01 FA SC {hemax_xsema} x por semana após hemodiálise.'
        elif item == lista_medicamentos[2]:
            linha1 = f'Sacarato de hidróxido de ferro 100 mg___________________ {norip_total} ampolas'
            linha2 = f'Fazer {norip_x15dias} ampola(s) a cada 15 dias.'
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
            linha2 = f'Tomar {mmf_dose} comprimido(s) 12/12h.'
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

        # Iniciar nesse nível o acréscimo do "texto" ao pdf
        c.drawString(1 * cm, x * cm, linha1)
        c.drawString(1 * cm, (x + y) * cm, linha2)
        c.drawString(16 * cm, x * cm, linha1)
        c.drawString(16 * cm, (x + y) * cm, linha2)
    c.setFontSize(10)
    c.drawString((centro_direita - 3) * cm, (altura_cabecalho + 3.2) * cm, paciente)
    c.drawString((centro_esquerda - 3) * cm, (altura_cabecalho + 3.2) * cm, paciente)

    # Fazendo o carimbo no final da página. O motivo do loop é fazer nas duas páginas
    j = 0
    for i in range(2):
        c.saveState()
        c.translate((12 + j) * cm, 17.5 * cm)
        c.rotate(-45)
        c.setFont("Times-Roman", 9)
        c.drawCentredString(0, 0, nome_medico)
        c.drawCentredString(0, 10, especialidade)
        c.setFont("Times-Roman", 7)
        c.drawCentredString(0, 20, crm)
        c.restoreState()
        j = j + metade_pagina

def gerarPdfReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6):
    # Definir o caminho do arquivo PDF
    my_path = "receituario_template.pdf"

    # Criar um novo canvas
    c = canvas.Canvas(my_path, pagesize=landscape(A4), bottomup=0)

    c.setTitle("Receituário")
    c.line(15 * cm, 0, 15 * cm, 21 * cm)
    c.setFont("Helvetica", 9)

    # Inserindo imagem do cabeçalho
    # Primeiro, precisa virar a imagem, por causa da configuração bottomup =0
    # A imagem precisa ficar antes das linhas, para evitar que o "branco" da imagem fique por cima das linhas
    def flip_image(image_path):
        img = Image.open(image_path)
        out = img.transpose(Image.FLIP_TOP_BOTTOM)

        output_path = "flipped_" + image_path  # Specify the output file path here
        out.save(output_path)  # Save the image using the output file path

        return output_path  # Return the output file path

    image = flip_image('cabecalho.jpg')
    c.drawImage(image, 1, 8)
    c.drawImage(image, 15 * cm, 8)

    # Cabeçalho do receituário da direita
    c.drawCentredString(centro_direita * cm, (altura_cabecalho + 0) * cm, "AMBULATÓRIO")
    c.drawCentredString(centro_direita * cm, (altura_cabecalho + 0.4) * cm, "HOSPITAL UNIVERSITARIO")
    c.drawCentredString(centro_direita * cm, (altura_cabecalho + 0.8) * cm, "Av. José de Sá Maniçoba, S/n - Centro - 56304-205 Petrolina - PE")
    c.drawCentredString(centro_direita * cm, (altura_cabecalho + 1.2) * cm, "(87)2101-6511/2101-6500")
    c.drawCentredString(centro_direita * cm, (altura_cabecalho + 2.2) * cm, "RECEITUÁRIO")
    c.drawString((centro_direita - 4.5) * cm, (altura_cabecalho + 3.2) * cm, "Paciente:")
    c.line((centro_direita - 5) * cm, 2.5 * cm, (centro_direita + 5) * cm, 2.5 * cm)  # linha de cima
    c.line((centro_direita - 5) * cm, 6.7 * cm, (centro_direita + 5) * cm, 6.7 * cm)  # linha de baixo
    c.line((centro_direita - 5) * cm, 2.5 * cm, (centro_direita - 5) * cm, 6.7 * cm)  # linha da direita
    c.line((centro_direita + 5) * cm, 2.5 * cm, (centro_direita + 5) * cm, 6.7 * cm)  # linha da esquerda

    # Cabeçalho do receituário da esquerda
    c.drawCentredString(centro_esquerda * cm, (altura_cabecalho + 0) * cm, "AMBULATÓRIO")
    c.drawCentredString(centro_esquerda * cm, (altura_cabecalho + 0.4) * cm, "HOSPITAL UNIVERSITARIO")
    c.drawCentredString(centro_esquerda * cm, (altura_cabecalho + 0.8) * cm, "Av. José de Sá Maniçoba, S/n - Centro - 56304-205 Petrolina - PE")
    c.drawCentredString(centro_esquerda * cm, (altura_cabecalho + 1.2) * cm, "(87)2101-6511/2101-6500")
    c.drawCentredString(centro_esquerda * cm, (altura_cabecalho + 2.2) * cm, "RECEITUÁRIO")
    c.drawString((centro_esquerda - 4.5) * cm, (altura_cabecalho + 3.2) * cm, "Paciente:")
    c.line((centro_esquerda - 5) * cm, 2.5 * cm, (centro_esquerda + 5) * cm, 2.5 * cm)  # linha de cima
    c.line((centro_esquerda - 5) * cm, 6.7 * cm, (centro_esquerda + 5) * cm, 6.7 * cm)  # linha de baixo
    c.line((centro_esquerda - 5) * cm, 2.5 * cm, (centro_esquerda - 5) * cm, 6.7 * cm)  # linha da direita
    c.line((centro_esquerda + 5) * cm, 2.5 * cm, (centro_esquerda + 5) * cm, 6.7 * cm)  # linha da esquerda

    fazerReceita(c, paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4,
                 quantidade4, remedio5, quantidade5, remedio6, quantidade6)

    c.showPage()
    c.save()

    # Fazendo o embeded PDF para visualizar o pdf no próprio site
    with open('receituario_template.pdf', "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display_receituario = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1200" height="800" type="application/pdf"></embed>'

    st.markdown(pdf_display_receituario, unsafe_allow_html=True)
    # -------------------------------------------------------------
    # ADDED: botão de download para o PDF da Receita
    # -------------------------------------------------------------
    st.download_button(
        label="Download Receita (PDF)",
        data=base64.b64decode(base64_pdf),      # Volta para bytes
        file_name="receituario_template.pdf",   # Nome para o download
        mime="application/pdf"
    )

import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import base64
from docxtpl import DocxTemplate
from docx2pdf import convert
import win32com
import pythoncom

#sabe-se lá porque motivo, sem essa linha de código e sem importar pythoncom e win32, o conversor de word para pdf dá erro
xl=win32com.client.Dispatch("Word.Application",pythoncom.CoInitialize())


#Variáveis globais que serão usadas em todas as funções
lista_medicamentos = ["","Alfaepoetina 4.000 UI injetável", "Sacarato de hidróxido férrico 100mg (frasco de 5mL)", "Calcitriol 0,25mg (cápsula)", "Calcitriol 1,0 mcg injetável (ampola)", "Sevelamer 800mg (comprimido)", "Cinacalcete 30mg (comprimido)", "Paricalcitol 5,0 mcg/ml injetável (ampola)", "Micofenolato de mofetila 500mg (comprimido)", "Azatioprina 50mg (comprimido)", "Hidroxicloroquina 400mg (comprimido)", "Ciclosporina 100mg (cápsula)", "Ciclosporina 50mg (cápsula)", "Ciclosporina 25mg (cápsula)"]
lista_medicos = ["Caio Petrola", "Maria Emilia Diniz", "Mucio Homero L. R. Ribeiro","Gloriete Vieira de Oliveira"]
lista_cids = ["N18.0 - Doença renal crônica", "M32.1 - Nefrite lúpica", "N04.1 - GESF", "N04.0 - Doença de lesões mínimas", "N04.3 - Nefropatia Membranosa"]
lista_clinicas = ["Clínica do Rim - Petrolina", "HU - Univasf"]


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
    reader = PdfReader("lme.pdf")
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
    with open(f"PDF/{paciente}.pdf", "wb") as output_stream:
        writer.write(output_stream)

    # Fazendo o embeded PDF para visualizar o pdf no próprio site
    with open(f"PDF/{paciente}.pdf","rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf"></iframe>'

    st.markdown(pdf_display, unsafe_allow_html=True)


def transformarWordPdf(paciente):
    entrada = f"PDF/{paciente}.docx"
    saida = f"PDF/{paciente}-receituario.pdf"

    convert(entrada, saida)

    # Fazendo o embeded PDF para visualizar o pdf no próprio site
    with open(f"PDF/{paciente}-receituario.pdf","rb") as f:
        base64_pdf_receita = base64.b64encode(f.read()).decode('utf-8')
        
    pdf_display_receita = f'<iframe src="data:application/pdf;base64,{base64_pdf_receita}" width="1100" height="850" type="application/pdf"></iframe>'

    st.markdown(pdf_display_receita, unsafe_allow_html=True)


def fazerReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6 ):
    lista_remedios = [remedio1, remedio2, remedio3, remedio4, remedio5, remedio6]
    lista_quantidades = [quantidade1, quantidade2, quantidade3, quantidade4, quantidade5, quantidade6]
    aglomerado_inicial = list(zip(lista_remedios, lista_quantidades))
    aglomerado_final = [x for x in aglomerado_inicial if x[0]!="" ]
    dicio_remedios = dict(aglomerado_final)
    #st.write(dicio_remedios["Alfaepoetina 4.000 UI injetável"])
    
    
    display_hemax=False
    hemax_total= "   "
    hemax_xsema= "   "
    
    display_norip=False
    norip_total= "   "
    norip_x15dias= "   "

    display_calcijex=False
    calcijex_total= "   "
    calcijex_dose= "   "

    display_paricalcitol=False
    paricalcitol_total= "   "
    paricalcitol_dose= "   "

    display_caco3=False
    caco3_total= "____ "
    caco3_3xdia= "____ "

    display_sevelamer=False
    sevelamer_total= "   "
    sevelamer_3xdia= "   "

    display_calcitriol=False
    calcitriol_total= "   "
    calcitriol_dose= "   "

    display_cinacalcete=False
    cinacalcete_total= "   "
    cinacalcete_dia= "   "

    display_mmf=False
    mmf_total= "   "
    mmf_dose= "   "
  
    display_aza=False
    aza_total= "   "
    aza_dose= "   "
  
    display_hcq=False
    hcq_total= "   "
    hcq_dose= "   "
  
    display_csa100=False
    csa100_total= "   "
    csa100_dose= "   "
  
    display_csa50=False
    csa50_total= "   "
    csa50_dose= "   "
  
    display_csa25=False
    csa25_total= "   "
    csa25_dose= "   "


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


    #preenchendo os campos correspondentes no modelo DOCX
    doc = DocxTemplate("modelo_receita_lme.docx")
    context = { 'nome' : paciente, 'hemax_total':hemax_total, 'hemax_xsema': hemax_xsema, 'norip_total':norip_total, 
                'norip_x15dias': norip_x15dias, 'calcijex_total':calcijex_total, 'calcijex_dose':calcijex_dose, 
                'paricalcitol_total':paricalcitol_total, 'paricalcitol_dose':paricalcitol_dose, 'sevelamer_total':sevelamer_total, 
                'sevelamer_3xdia':sevelamer_3xdia, 'calcitriol_total':calcitriol_total, 'calcitriol_dose':calcitriol_dose, 
                'cinacalcete_total':cinacalcete_total, 'cinacalcete_dia':cinacalcete_dia, 'display_hemax':display_hemax, 
                'display_norip':display_norip, 'display_calcijex':display_calcijex, 'display_paricalcitol':display_paricalcitol, 
                'display_sevelamer':display_sevelamer, 'display_calcitriol':display_calcitriol, 'display_cinacalcete':display_cinacalcete,
                'display_mmf':display_mmf, 'mmf_total':mmf_total, 'mmf_dose':mmf_dose,
                'display_aza':display_aza, 'aza_total':aza_total, 'aza_dose':aza_dose,
                'display_hcq':display_hcq, 'hcq_total':hcq_total, 'hcq_dose':hcq_dose,
                'display_csa100':display_csa100, 'csa100_total':csa100_total, 'csa100_dose':csa100_dose,
                'display_csa50':display_csa50, 'csa50_total':csa50_total, 'csa50_dose':csa50_dose,
                'display_csa25':display_csa25, 'csa25_total':csa25_total, 'csa25_dose':csa25_dose,

            }
    doc.render(context)
    doc.save(f"PDF/{paciente}.docx")
       
    transformarWordPdf(paciente)
    


st.header("Preenchedor de LMEs do Caio")



def main():

    with st.form(key="myform", clear_on_submit=False):
        form_a, form_b = st.columns(2)
        

        container_identificacao = form_a.container()
        id_a,id_b = container_identificacao.columns([0.8, 0.2])
        paciente = id_a.text_input("Nome")
        mae = id_a.text_input("Nome da mãe")
        peso = id_b.number_input("Peso(kg)", min_value=0.0)
        altura = id_b.number_input("Altura (cm)", min_value=0)
        form_a.divider()

        #Definindo o CID
        cid_geral = form_a.selectbox("CID",lista_cids)

        #Definindo o médico
        medico = form_a.selectbox("Médico", lista_medicos)

        #Definindo a Clínica
        clinica = form_a.radio("Clínica", lista_clinicas)
    
        container_medicamento = form_b.container()
        med_a, med_b = container_medicamento.columns([0.7, 0.3])
        
        remedio1 = med_a.selectbox("Medicação 1", lista_medicamentos)
        quantidade1 = med_b.number_input("Quantidade 1", step=1)
        remedio2 = med_a.selectbox("Medicação 2", lista_medicamentos)
        quantidade2 = med_b.number_input("Quantidade 2", step=1)
        remedio3 = med_a.selectbox("Medicação 3", lista_medicamentos)
        quantidade3 = med_b.number_input("Quantidade 3", step=1)
        remedio4 = med_a.selectbox("Medicação 4", lista_medicamentos)
        quantidade4 = med_b.number_input("Quantidade 4", step=1)
        remedio5 = med_a.selectbox("Medicação 5", lista_medicamentos)
        quantidade5 = med_b.number_input("Quantidade 5", step=1)
        remedio6 = med_a.selectbox("Medicação 6", lista_medicamentos)
        quantidade6 = med_b.number_input("Quantidade 6", step=1)


        submit_button = st.form_submit_button("Fazer LME")
    if submit_button:
        # st.write(f"Clínica: {clinica}")
        fazerLme(paciente, mae, peso, altura, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6, clinica, cid_geral, medico)
        fazerReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6)
   


if __name__ == "__main__":
    main()

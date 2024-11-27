import streamlit as st
import base64
#importações relativas ao pdf para criação do receituário
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import  landscape, A4
from PIL import Image
from var_globais import *
from funcoes import *





def main():
    st.header("Preenchedor de LMEs do Caio")
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
        gerarPdfReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6)
        #fazerReceita(paciente, medico, remedio1, quantidade1, remedio2, quantidade2, remedio3, quantidade3, remedio4, quantidade4, remedio5, quantidade5, remedio6, quantidade6)
        


if __name__ == "__main__":
    main()

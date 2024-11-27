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
        clinica = form_a.radio("Clínica", lista_clinicas, index=1) # index =1 define o segundo item, no caso HU, como padrão
    
        container_medicamento = form_b.container()
        
        # Listas para armazenar os valores
        remedios = []
        quantidades = []

        # Loop para criar campos de Medicação e Quantidade
        for i in range(1, 7):
            med_col, quant_col = container_medicamento.columns([0.7, 0.3])
            remedio = med_col.selectbox(f"Medicação {i}", lista_medicamentos, key=f"remedio{i}")
            quantidade = quant_col.number_input(f"Quantidade {i}", step=1, key=f"quantidade{i}")
            remedios.append(remedio)
            quantidades.append(quantidade)

        submit_button = st.form_submit_button("Fazer LME")

    if submit_button:
        fazerLme(paciente, mae, peso, altura,
                 remedios[0], quantidades[0],
                 remedios[1], quantidades[1],
                 remedios[2], quantidades[2],
                 remedios[3], quantidades[3],
                 remedios[4], quantidades[4],
                 remedios[5], quantidades[5],
                 clinica, cid_geral, medico)

        gerarPdfReceita(paciente, medico,
                        remedios[0], quantidades[0],
                        remedios[1], quantidades[1],
                        remedios[2], quantidades[2],
                        remedios[3], quantidades[3],
                        remedios[4], quantidades[4],
                        remedios[5], quantidades[5])

if __name__ == "__main__":
    main()
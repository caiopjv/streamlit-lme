#Variáveis globais que serão usadas em todas as funções
lista_medicamentos = ["","Alfaepoetina 4.000 UI injetável", 
                      "Sacarato de hidróxido férrico 100mg (frasco de 5mL)", 
                      "Calcitriol 0,25mg (cápsula)", 
                      "Calcitriol 1,0 mcg injetável (ampola)", 
                      "Sevelamer 800mg (comprimido)", 
                      "Cinacalcete 30mg (comprimido)", 
                      "Paricalcitol 5,0 mcg/ml injetável (ampola)", 
                      "Micofenolato de mofetila 500mg (comprimido)", 
                      "Azatioprina 50mg (comprimido)", 
                      "Hidroxicloroquina 400mg (comprimido)", 
                      "Ciclosporina 100mg (cápsula)", 
                      "Ciclosporina 50mg (cápsula)", 
                      "Ciclosporina 25mg (cápsula)", 
                      "Dapagliflozina 10mg (comprimido)"]
lista_medicos = ["Caio Petrola", 
                 "Maria Emilia Diniz", 
                 "Mucio Homero L. R. Ribeiro",
                 "Gloriete Vieira de Oliveira"]
lista_cids = ["N18.0 - Doença renal crônica", 
              "M32.1 - Nefrite lúpica", 
              "N04.1 - GESF", 
              "N04.0 - Doença de lesões mínimas", 
              "N04.3 - Nefropatia Membranosa"]
lista_clinicas = ["Clínica do Rim - Petrolina", "HU - Univasf"]
# Essas variáveis abaixo ficarão globais para serem usadas em várias funções
my_path = "receituario_template.pdf"

#c = canvas.Canvas(my_path, pagesize=landscape(A4), bottomup=0)

#Determinando valores de referencia em cm
altura_cabecalho = 3
centro_direita = 7.5
centro_esquerda = 22.5
metade_pagina = 14

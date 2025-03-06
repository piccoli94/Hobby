import tkinter as tk
import csv
import os
import re

# Funzione per chiudere la prima finestra e aprire la seconda
def apri_seconda_finestra(nome):
    root.destroy()  # Chiude la prima finestra
    seconda_finestra(nome)

# Funzione per chiudere la seconda finestra e aprire la terza
def apri_terza_finestra():
    seconda_root.destroy()  # Chiude la seconda finestra
    terza_finestra()

def apri_quarta_finestra(nome):
    terza_root.destroy()
    quarta_finestra(nome)

# Prima finestra
def prima_finestra():
    global root

    istart = 0
    iend = len(nuovo_dizionario.keys()) // 2

    root = tk.Tk()
    root.title("Prima Finestra")

    label = tk.Label(root, text="Questa è la prima finestra")
    label.pack(pady=20)


    for nome in list(nuovo_dizionario.keys())[int(istart):int(iend)]:
        checkbutton = tk.Button(root, text=nome, command=apri_seconda_finestra(nome))
        checkbutton.pack(pady=5)

    
    #ok_button = tk.Button(root, text="OK", command=apri_seconda_finestra)
    #ok_button.pack(pady=20)

    root.mainloop()

# Seconda finestra
def seconda_finestra(nome):
    global seconda_root
    seconda_root = tk.Tk()
    seconda_root.title("Seconda Finestra")

    label = tk.Label(seconda_root, text="Seleziona le abilità")
    label.pack(pady=20)
    opzioni=nuovo_dizionario[nome]
    variabili_opzioni = []

    for opzione in opzioni[:-2]:
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(seconda_root, text=opzione, variable=var)
        checkbutton.pack(pady=5)
        variabili_opzioni.append(var)

    ok_button = tk.Button(seconda_root, text="OK", command=check())
    ok_button.pack(pady=20)

    errore_label = tk.Label(seconda_root, text="", fg="red")
    errore_label.pack(pady=5)

    def check():
        selezioni = []
        
        flag_abilita_unica = False
        for i, var in enumerate(variabili_opzioni):
            if i == 0 and var.get() != 1:
                flag_abilita_unica = True
            
            if var.get() == 1:
                selezioni.append(opzioni[i])      

            if (len(selezioni) != 4 or flag_abilita_unica):
                errore_label.config(text="Selezione non valida!")
                return

        print(f"Hai selezionato: {selezioni}")

        apri_terza_finestra()
    #ok_button = tk.Button(seconda_root, text="OK", command=apri_terza_finestra)
    #ok_button.pack(pady=20)

    seconda_root.mainloop()

# Terza finestra
def terza_finestra():
    global terza_root     
    terza_root.title("Terza Finestra")

    label = tk.Label(terza_root, text="Questa è la terza finestra")
    label.pack(pady=20)


    istart = len(nuovo_dizionario.keys()) // 2 
    iend = len(nuovo_dizionario.keys())

    for nome in list(nuovo_dizionario.keys())[int(istart):int(iend)]:
        checkbutton = tk.Button(seconda_root, text=nome, command=apri_quarta_finestra(nome))
        checkbutton.pack(pady=5)


    terza_root.mainloop()

def quarta_finestra(nome):
    global quarta_root
    quarta_root = tk.Tk()
    quarta_root.title("Quarta Finestra")

    label = tk.Label(quarta_root, text="Seleziona le abilità")
    label.pack(pady=20)
    opzioni=nuovo_dizionario[nome]
    variabili_opzioni = []

    for opzione in opzioni[:-2]:
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(quarta_root, text=opzione, variable=var)
        checkbutton.pack(pady=5)
        variabili_opzioni.append(var)

    ok_button = tk.Button(quarta_root, text="OK", command=termina)
    ok_button.pack(pady=20)

    errore_label = tk.Label(quarta_root, text="", fg="red")
    errore_label.pack(pady=5)

    def termina():
        selezioni = []
        
        flag_abilita_unica = False
        for i, var in enumerate(variabili_opzioni):
            if i == 0 and var.get() != 1:
                flag_abilita_unica = True
            
            if var.get() == 1:
                selezioni.append(opzioni[i])      

            if (len(selezioni) != 3 or flag_abilita_unica):
                errore_label.config(text="Selezione non valida!")
                return

        print(f"Hai selezionato: {selezioni}")
        quarta_root.destroy()


    quarta_root.mainloop()



def read_matching_files(csv_path, config_folder):
    if not os.path.exists(config_folder):
        print(f"La cartella {config_folder} non esiste.")
        return {}

    if not os.path.exists(csv_path):
        print(f"Il file CSV {csv_path} non esiste.")
        return {}

    nomi = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row:
                    nomi.append(row[0])
    except Exception as e:
        print(f"Errore nella lettura del file CSV: {e}")
        return {}

    print(f"Nomi trovati nel CSV: {nomi}")

    risultati = {}
    for nome in nomi:
        file_path = os.path.join(config_folder, f"{nome}.txt")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    contenuto = file.read()
                    risultati[nome] = contenuto
                    print(f"Letto il file: {file_path}")
            except Exception as e:
                print(f"Errore nella lettura del file {file_path}: {e}")
        else:
            print(f"File {file_path} non trovato.")
    
    return risultati

def estrai_blocchi_simboli(risultati):
    nuovo_dizionario = {}

    for nome, contenuto in risultati.items():
        pattern = r"(★|❖|Equipaggiamento di base)(.*?)(?=(★|❖|Equipaggiamento di base|$))"
        blocchi = re.findall(pattern, contenuto, re.DOTALL)

        blocchi_estratti = [bloc[0] + bloc[1].strip() for bloc in blocchi]
        
        nuovo_dizionario[nome] = blocchi_estratti

    return nuovo_dizionario

# Avvia il programma con la prima finestra
if __name__ == "__main__":
    csv_path = "classi_e_skill.csv"
    config_folder = "config"
    global nuovo_dizionario
    risultati = read_matching_files(csv_path, config_folder)
    nuovo_dizionario = estrai_blocchi_simboli(risultati)
    prima_finestra()

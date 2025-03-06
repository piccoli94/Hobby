import tkinter as tk
import csv
import os
import re

def apri_nuova_finestra(nome, flag):
    root.destroy()  # Chiude la prima finestra
    interfaccia_scelte_multiple(nome, nuovo_dizionario[nome], flag)  # Apre la nuova finestra con le scelte multiple

def interfaccia_scelte_multiple(nome, opzioni, flag):
    nuova_root = tk.Tk()
    
    switcher = {
        0: f"Scegli le abilità del {nome}",
        1: f"Scegli le abilità del {nome}",
        2: f"Scegli l'equip' del {nome}"
    }
    nuova_root.title(switcher.get(flag, "Selezione"))

    switcher = {
        0: "Seleziona abilità unica e 3 specializzazioni.",
        1: "Seleziona abilità unica e 2 specializzazioni.",
        2: "Seleziona 2 equipaggiamenti."
    }
    label = tk.Label(nuova_root, text=switcher.get(flag, "Seleziona opzioni"))
    label.pack(pady=20)

    variabili_opzioni = []
    
    if flag != 2:
        for opzione in opzioni[:-2]:
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(nuova_root, text=opzione, variable=var)
            checkbutton.pack(pady=5)
            variabili_opzioni.append(var)
    else:
        list_equip = opzioni[:-1].split("-")
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(nuova_root, text=list_equip[1:], variable=var)
        checkbutton.pack(pady=5)
        variabili_opzioni.append(var)

    def termina():
        selezioni = []
        
        if flag == 0 or flag == 1:
            flag_abilita_unica = False
            for i, var in enumerate(variabili_opzioni):
                if i == 0 and var.get() != 1:
                    flag_abilita_unica = True
                
                if var.get() == 1:
                    selezioni.append(opzioni[i])
            
            if (flag == 0 and (len(selezioni) != 4 or flag_abilita_unica)) or \
               (flag == 1 and (len(selezioni) != 3 or flag_abilita_unica)):
                errore_label.config(text="Selezione non valida!")
                return
        
        elif flag == 2:
            for i, var in enumerate(variabili_opzioni):
                if var.get() == 1:
                    selezioni.append(opzioni[i])
            
            if len(selezioni) != 2:
                errore_label.config(text="Seleziona esattamente 2 opzioni!")
                return
        
        print(f"Hai selezionato: {selezioni}")
        nuova_root.destroy()
        
        # Open the next interface based on the current flag
        if flag == 0:
            crea_pulsanti(1)
        elif flag == 1:
            crea_pulsanti(2)

    ok_button = tk.Button(nuova_root, text="OK", command=termina)
    ok_button.pack(pady=20)

    errore_label = tk.Label(nuova_root, text="", fg="red")
    errore_label.pack(pady=5)

    nuova_root.mainloop()

def crea_pulsanti(flag):
    nuova_root = tk.Tk()
    nuova_root.title("Pulsanti Nomi")

    if flag == 0 or flag == 2:
        istart = 0
        iend = len(nuovo_dizionario.keys()) // 2
    elif flag == 1:
        istart = len(nuovo_dizionario.keys()) // 2 + 1
        iend = len(nuovo_dizionario.keys())

    for nome in list(nuovo_dizionario.keys())[int(istart):int(iend)]:
        button = tk.Button(nuova_root, text=nome, command=lambda n=nome: apri_nuova_finestra(n, flag))
        button.pack(pady=5)

    nuova_root.mainloop()

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

if __name__ == "__main__":
    csv_path = "classi_e_skill.csv"
    config_folder = "config"

    risultati = read_matching_files(csv_path, config_folder)
    nuovo_dizionario = estrai_blocchi_simboli(risultati)

    root = tk.Tk()
    root.title("Pulsanti Nomi")
    flag = 0
    crea_pulsanti(flag)

    root.mainloop()
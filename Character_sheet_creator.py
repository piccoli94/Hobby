import pandas as pd
import PyPDF2
import re

def txt_to_dataframe(file_path, delimiter=None, header=None):
    """
    Legge un file di testo e lo converte in un DataFrame pandas.
    
    Parametri:
    file_path (str): Percorso del file di testo da leggere
    delimiter (str, optional): Delimitatore dei campi nel file. Se None, prova a dedurlo automaticamente
    header (int, list, 'infer' o None): Riga da usare come intestazione. 'infer' prova a dedurre l'intestazione
    
    Ritorna:
    pandas.DataFrame: DataFrame contenente i dati del file
    """
    try:
        # Legge il file di testo in un DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter, header=header)
        print(f"File '{file_path}' letto con successo!")
        return df
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        return None



# Funzione principale
def main():
    # Percorsi dei file (da modificare con i tuoi percorsi)
    txt_file_path = "classi_e_skill.csv"
    pdf_file_path = "4_5848283600608303604.pdf"
    
    # Legge il file di testo in un DataFrame
    df = txt_to_dataframe(txt_file_path, delimiter=",")
    
    if df is not None and not df.empty:
        # Prende il primo elemento del DataFrame
        # Se è una serie (prima riga), prende il primo valore
        if isinstance(df.iloc[0], pd.Series):
            first_element = df.iloc[0, 0]
        # Se il DataFrame ha solo una colonna, prende il primo valore
        else:
            first_element = df.iloc[0]
        
        print(f"\nPrimo elemento del DataFrame: {first_element}")
        
        # Cerca nel PDF e trova gli elenchi
        results = search_in_pdf_and_find_lists(pdf_file_path, str(first_element))
        
        # Stampa i risultati
        if results:
            print(f"\nRisultati trovati: {len(results)}")
            for page_num, paragraph, diamond_lists, star_lists in results:
                print(f"\nPagina {page_num}:")
                print("-" * 60)
                print(f"Paragrafo contenente '{first_element}':")
                print(paragraph[:200] + "..." if len(paragraph) > 200 else paragraph)
                
                # Stampa gli elenchi con ❖
                if diamond_lists:
                    print("\nElenchi che iniziano con ❖:")
                    for i, item in enumerate(diamond_lists, 1):
                        print(f"{i}. {item}")
                else:
                    print("\nNessun elenco che inizia con ❖ trovato in questo paragrafo.")
                
                # Stampa gli elenchi con ★
                if star_lists:
                    print("\nElenchi che iniziano con ★:")
                    for i, item in enumerate(star_lists, 1):
                        print(f"{i}. {item}")
                else:
                    print("\nNessun elenco che inizia con ★ trovato in questo paragrafo.")
                
                print("-" * 60)
        else:
            print(f"Nessun paragrafo contenente '{first_element}' trovato nel PDF.")
    else:
        print("Impossibile procedere: DataFrame vuoto o non valido")

if __name__ == "__main__":
    main()
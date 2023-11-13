from pdfminer.high_level import extract_text
import pandas as pd

def no_letters(date):
    for elt in date:
        if elt.isalpha():
            return False
    return len(date.split('/')) == 3

def pdf_to_df(file):
    extracted_text = extract_text(file)
    start_of = extracted_text.find('Presse en ligne')
    articles_list = extracted_text[start_of:].split('\n\n')
    data_dict = { 'Titre' : [], 'Date' : [], 'Lien' : [], 'Description' : [] }

    for article in articles_list:
        splitted = article.split('\n')
        if len(splitted) >= 4:
            for i in range(1,len(splitted)-2):
                if no_letters(splitted[i]):
                    data_dict['Titre'].append(' '.join(splitted[:i]))
                    data_dict['Date'].append(splitted[i])
                    data_dict['Lien'].append(splitted[i+1])
                    data_dict['Description'].append(' '.join(splitted[i+2:]))

    return pd.DataFrame(data_dict)

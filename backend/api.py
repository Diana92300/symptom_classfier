import csv
import json

import google.generativeai as genai
import requests

from constants import TEPROLIN_API, GOOGLE_API_KEY
from schema import TeprolinTokenizationData


def preprocess_input(user_input: str) -> dict:
    ttd = TeprolinTokenizationData(user_input, 'biomedical-named-entity-recognition')
    response = requests.post(f'{TEPROLIN_API}/process', data=vars(ttd))

    if not response.ok:
        # todo
        pass

    response = json.loads(response.text)

    clean_response = sanitize_response(response)

    return {'response': clean_response}


def sanitize_response(response: dict) -> list:
    tokens = response['teprolin-result']['tokenized'][0]
    clean_tokens = []

    for token in tokens:

        if not token['_bner']:
            continue

        clean_tokens.append(token['_lemma'])

    return clean_tokens


def find_recommendations_for_diseases(csv_file, disease_names):
    recommendations_dict = {}

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            rows = rows[1:]

            for disease_name in disease_names:
                found = False
                for row in rows:
                    if len(row) >= 2 and row[0].lower() == disease_name.lower():
                        recommendations_dict[disease_name] = row[1]
                        found = True
                        break
                if not found:
                    recommendations_dict[disease_name] = None

        return recommendations_dict
    except Exception as e:
        return {disease_name: None for disease_name in disease_names}


def generate_patient_response(disease_names, recommendations_dict):
    genai.configure(api_key=GOOGLE_API_KEY)

    first_disease = disease_names.split(',')[0]
    first_recommendations = recommendations_dict.get(first_disease)
    found_diseases = [disease for disease, rec in recommendations_dict.items() if rec is not None]

    prompt = f"""
    Tu esti un ajutor (un chatbot) al unei aplicatii academice care ajuta la clasificarea simptomelor precizate de un utilizator.
    Scopul tau este acela de a formula un raspuns coerent care sa explice rezultatele date de clasificator, incearca sa    
    formulezi acest raspuns intr-un mod formal, scurt si la obiect, care explica recomandarile pentru boala care 
    este considerata de clasificator ca fiind cea mai probabila iar pentru celelalte doar precizeaza faptul ca si ele au
    facut match pe simptomele descrise si ar avea potential sa fie si ele luate in considerare.
    
    Raspunsul trebuie sa fie formatat si coerent, nu include simptomele doar cu ;
    
    Nu scrie in markdown, latex sau orice alta metoda de formatare, doar plain text. Raspunsul trebuie sa fie scurt si
    la obiect fara a preciza disclaimer la final pentru ca oricum nu va fi folosita intr-un scenariu real.
    
    Daca consideri ca este adecvat poti enumera recomandarile cu -
    
    NU INCLUDE RECOMANDARI CARE NU AU TREABA CU MEDICINA, de tipul medicina alternativa.

    Formulează un răspuns pentru un pacient care ar putea suferi de următoarele boli: {disease_names}.

    În răspuns, menționează toate aceste posibile boli: {', '.join(found_diseases)}.

    După ce menționezi toate bolile posibile, concentrează-te doar pe prima boală din listă ({first_disease}) și include următoarele recomandări specifice pentru această boală:
    {first_recommendations}

    Formulează răspunsul într-un limbaj accesibil, organizat în paragrafe.
    """

    if first_recommendations is None:
        prompt = f"""
        Formulează un răspuns pentru un pacient care ar putea suferi de următoarele boli: {disease_names}.

        În răspuns, menționează toate aceste posibile boli: {found_diseases}.

        Din păcate, nu avem recomandări specifice pentru prima boală din listă ({first_disease}) în baza noastră de date.
        Formulează un răspuns general, sugerând pacientului să consulte un medic specialist pentru diagnostic și recomandări personalizate.
        """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    if response.candidates:
        return response.candidates[0].content.parts[0].text.strip()
    else:
        return "Nu s-a putut genera un răspuns personalizat."

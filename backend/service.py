import api
import classifier


def classify_disease(user_input: str) -> dict:
    user_input = user_input.lower()

    diagnosis = api.preprocess_input(user_input)
    disease, sim_factor = classifier.identify_disease(diagnosis['response'])

    recommendations = api.find_recommendations_for_diseases('diseases_recommendations.csv',
                                                            list(disease.lower().split(',')))
    response = api.generate_patient_response(disease.lower(), recommendations)

    return {'response': response, 'sim-factor': sim_factor}

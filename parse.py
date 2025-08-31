# Importation des bibliothèques pour l'intégration avec Ollama et LangChain
from langchain_ollama import OllamaLLM  # Modèle de langage local
from langchain_core.prompts import ChatPromptTemplate  # Pour créer des prompts

# Template de prompt pour l'IA - définit les instructions précises pour l'extraction
template = (
    # Instruction principale : extraction d'informations spécifiques
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    # Règle 1 : Extraire uniquement ce qui correspond à la description
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    # Règle 2 : Pas de contenu supplémentaire dans la réponse
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    # Règle 3 : Retourner une chaîne vide si aucune correspondance
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    # Règle 4 : Sortie uniquement des données demandées
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Configuration du modèle LLM local (Llama 3.2 via Ollama)
model = OllamaLLM(model="llama3.2")

def parse_with_ollama(dom_chunks, parse_description):
    """
    >>> Fonction pour parser le contenu avec l'IA Ollama
    """
    # Création du template de prompt à partir du template défini
    prompt = ChatPromptTemplate.from_template(template)
    
    # Création d'une chaîne de traitement : prompt + modèle
    chain = prompt | model

    # Liste pour stocker les résultats de chaque morceau
    parsed_results = []

    # Traitement de chaque morceau de contenu séparément
    for i, chunk in enumerate(dom_chunks, start=1):
        # Exécution de la chaîne avec les variables de contexte
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        # Affichage de la progression pour le debug
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        # Ajout du résultat à la liste
        parsed_results.append(response)

    # Concaténation de tous les résultats avec des sauts de ligne
    return "\n".join(parsed_results)
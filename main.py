import streamlit as st
from scrape import (
    scrape_website,           # Fonction pour scraper le site web
    split_dom_content,        # Fonction pour découper le contenu en morceaux
    clean_body_content,       # Fonction pour nettoyer le contenu
    extract_body_content      # Fonction pour extraire le body du HTML
)
from parse import parse_with_ollama  # Fonction pour parser avec l'IA

# Configuration de l'interface utilisateur Streamlit
st.title("Ai Web Scraper")  
url = st.text_input("Enter a Website URL: ")  # Champ de saisie pour l'URL

# Bloc d'exécution lorsque l'utilisateur clique sur "Scrape Site"
if st.button("Scrape Site"):
    st.write("Scraping the website")  

    # Étape 1 : Scraping du site web pour obtenir le HTML brut
    result = scrape_website(url)
    
    # Étape 2 : Extraction du contenu de la balise <body> uniquement
    body_content = extract_body_content(result)
    
    # Étape 3 : Nettoyage du contenu (suppression scripts, styles, formatage)
    cleaned_content = clean_body_content(body_content)

    # Stockage du contenu nettoyé dans la session Streamlit pour une utilisation ultérieure
    st.session_state.dom_content = cleaned_content

    # Création d'une section déroulante pour afficher le contenu DOM nettoyé
    with st.expander("View DOM Content"):
        # Zone de texte pour afficher le contenu avec une hauteur de 300 pixels
        st.text_area("DOM Content", cleaned_content, height=300)

# Vérification si du contenu DOM a été stocké dans la session
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")
    
    if st.button("Parse content"):
        # Vérification que l'utilisateur a fourni une description
        if parse_description:
            st.write("Parsing the content")  
            
            # Découpage du contenu en morceaux pour le traitement par lots
            dom_chunks = split_dom_content(st.session_state.dom_content)
            
            # Parsing du contenu avec l'IA Ollama selon la description fournie
            result = parse_with_ollama(dom_chunks, parse_description)
            
            # Affichage des résultats du parsing
            st.write(result)
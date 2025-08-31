# Importation des bibliothèques pour le scraping web et le traitement HTML
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup  # Pour le parsing HTML
from dotenv import load_dotenv  # Pour charger les variables d'environnement
import time  

# Configuration de l'authentification pour le service de proxy Bright Data
AUTH = 'brd-customer-hl_50a190f5-zone-ai_scraper:00g3r8n75bpi'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    """
    >>> Fonction pour scraper un site web en utilisant un navigateur distant
    """
    print("Launching chrome browser...")  # Message de debug

    # Configuration de la connexion au navigateur distant via proxy
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    # Contexte with pour une gestion automatique de la connexion
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print("Navigating to page...")  # Message de debug
        driver.get(website)  # Navigation vers l'URL spécifiée
        time.sleep(5)  # Pause de 5 secondes pour permettre le chargement complet
        html = driver.page_source  # Récupération du code HTML de la page
        print(html)  # Affichage du HTML pour debug
        return html  # Retour du code HTML brut

def extract_body_content(html_content):
    """
    >>> Fonction pour extraire uniquement le contenu de la balise <body>
    """
    # Parsing du HTML avec BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser") 
    body_content = soup.body  # Extraction de la balise <body>
    
    # Vérification que le body existe et retour en tant que chaîne
    if body_content:
        return str(body_content)
    return ""  # Retour d'une chaîne vide si pas de body

def clean_body_content(body_content):
    """
    >>> Fonction pour nettoyer le contenu du body (suppression scripts, styles, etc.)
    """
    # Parsing du contenu avec BeautifulSoup
    soup = BeautifulSoup(body_content, "html.parser")

    # Suppression de toutes les balises <script> et <style>
    for script_or_style in soup(["script", "style"]): 
        script_or_style.extract()  # Méthode pour retirer les éléments du DOM

    # Extraction du texte brut avec des sauts de ligne comme séparateurs
    cleaned_content = soup.get_text(separator="\n")
    
    # Nettoyage avancé : suppression des lignes vides et des espaces superflus
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content  # Retour du contenu nettoyé

def split_dom_content(dom_content, max_length=600):
    """
    >>> Fonction pour découper le contenu DOM en morceaux de taille fixe
    >>> Utile pour le traitement par lots avec l'IA
    """
    return [
        # Découpage en morceaux de max_length caractères
        dom_content[i:i+max_length] 
        for i in range(0, len(dom_content), max_length) 
    ]
import time
import json
import csv
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK resources for sentiment analysis (executar apenas na primeira vez)
nltk.download('vader_lexicon')

class InstagramScraper:
    def __init__(self, username, password, headless=False):
        """
        Inicializa o scraper do Instagram
        
        Args:
            username (str): Nome de usuário do Instagram
            password (str): Senha do Instagram
            headless (bool): Se True, executa o navegador em modo headless
        """
        self.username = username
        self.password = password
        
        # Configurar o driver do Chrome
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        # Inicializar o driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Inicializar o analisador de sentimento
        self.sia = SentimentIntensityAnalyzer()
        
        # Criar diretório para dados
        self.data_dir = "instagram_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def login(self):
        """Faz login no Instagram"""
        try:
            print("Abrindo o Instagram...")
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)  # Aguardar carregamento da página
            
            # Aceitar cookies se o diálogo aparecer
            try:
                print("Tentando aceitar cookies...")
                cookie_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]")
                cookie_button.click()
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao aceitar cookies: {e}")
            
            # Preencher campos de login
            print("Preenchendo campos de login...")
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Clicar no botão de login
            print("Clicando no botão de login...")
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            login_button.click()
            
            # Aguardar login completo
            time.sleep(5)
            
            # Lidar com pop-ups pós-login
            try:
                print("Lidando com pop-ups pós-login...")
                not_now_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
                not_now_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Erro ao lidar com pop-ups: {e}")
                
            try:
                another_not_now = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
                another_not_now.click()
            except Exception as e:
                print(f"Erro ao lidar com outro pop-up: {e}")
                
            print("Login realizado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return False
            
    def search_hashtag(self, hashtag):
        """
        Busca postagens por hashtag
        
        Args:
            hashtag (str): Hashtag a ser buscada (sem o #)
            
        Returns:
            list: Lista de URLs de postagens encontradas
        """
        try:
            self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            time.sleep(5)  # Aguardar carregamento dos resultados
            
            post_links = []
            
            # Pegar links das primeiras 9 postagens (grid 3x3 inicial)
            posts = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
            for post in posts[:9]:  # Limitar para as primeiras 9 postagens
                post_url = post.get_attribute("href")
                if post_url and post_url not in post_links:
                    post_links.append(post_url)
                    
            print(f"Encontradas {len(post_links)} postagens para a hashtag #{hashtag}")
            return post_links
            
        except Exception as e:
            print(f"Erro ao buscar hashtag #{hashtag}: {e}")
            return []
            
    def search_business_accounts(self, nicho, max_accounts=10):
        """
        Busca contas comerciais baseadas no nicho
        
        Args:
            nicho (str): Nicho de mercado a ser buscado
            max_accounts (int): Número máximo de contas a buscar
            
        Returns:
            list: Lista de nomes de usuário de contas comerciais
        """
        try:
            # Buscar pelo nicho
            self.driver.get(f"https://www.instagram.com/explore/search/keyword/?q={nicho}")
            time.sleep(5)
            
            # Clicar na aba "Contas"
            try:
                accounts_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Accounts')]")))
                accounts_tab.click()
                time.sleep(3)
            except:
                print("Aba 'Contas' não encontrada, continuando com resultados atuais")
            
            # Coletar contas
            business_accounts = []
            account_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/') and not(contains(@href, '/explore/'))]")
            
            for account in account_elements:
                try:
                    username = account.get_attribute("href").split("/")[-2]
                    if username and username not in business_accounts and username != "":
                        business_accounts.append(username)
                        if len(business_accounts) >= max_accounts:
                            break
                except:
                    continue
                    
            print(f"Encontradas {len(business_accounts)} contas comerciais para o nicho '{nicho}'")
            return business_accounts
            
        except Exception as e:
            print(f"Erro ao buscar contas comerciais: {e}")
            return []
            
    def get_recent_posts(self, username, max_posts=5):
        """
        Obtém posts recentes de uma conta
        
        Args:
            username (str): Nome de usuário da conta
            max_posts (int): Número máximo de posts a coletar
            
        Returns:
            list: Lista de URLs dos posts recentes
        """
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(3)
            
            # Verificar se é uma conta comercial/de negócios
            try:
                # Procurar por indicadores de conta comercial como "Contact", "Email", etc.
                business_indicators = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Contact') or contains(text(), 'Email') or contains(text(), 'Business')]")
                if not business_indicators:
                    # Verificar se tem link externo ou categoria
                    business_indicators = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'http')]")
                    if not business_indicators:
                        print(f"A conta {username} pode não ser uma conta comercial. Pulando.")
                        return []
            except:
                pass
            
            # Coletar posts
            post_links = []
            post_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
            
            for post in post_elements:
                post_url = post.get_attribute("href")
                if post_url and post_url not in post_links:
                    post_links.append(post_url)
                    if len(post_links) >= max_posts:
                        break
                        
            print(f"Coletados {len(post_links)} posts recentes de @{username}")
            return post_links
            
        except Exception as e:
            print(f"Erro ao coletar posts de @{username}: {e}")
            return []
            
    def is_ad_post(self, post_url):
        """
        Verifica se um post é um anúncio
        
        Args:
            post_url (str): URL do post
            
        Returns:
            bool: True se for um anúncio, False caso contrário
        """
        try:
            self.driver.get(post_url)
            time.sleep(3)
            
            # Verificar palavras-chave na descrição que indicam anúncio
            post_text = self.driver.find_element(By.XPATH, "//div[contains(@class, 'C4VMK')]/span").text.lower()
            
            ad_keywords = [
                "ad", "anúncio", "publicidade", "patrocinado", "parceria paga",
                "sponsored", "promocional", "promoção", "#ad", "#parceriaremunerada",
                "#publi", "link na bio", "compre agora", "shop now"
            ]
            
            # Verificar se há marcadores de parceria paga
            paid_partnership = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Paid partnership') or contains(text(), 'Parceria paga')]")
            
            # Verificar se há botões de ação (Comprar, Saiba mais, etc)
            action_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Shop Now') or contains(text(), 'Learn More') or contains(text(), 'Comprar') or contains(text(), 'Saiba mais')]")
            
            # Verificar se qualquer indicador de anúncio está presente
            is_ad = any(keyword in post_text for keyword in ad_keywords) or paid_partnership or action_buttons
            
            return is_ad
            
        except Exception as e:
            print(f"Erro ao verificar se o post é um anúncio: {e}")
            return False
            
    def analyze_comments(self, post_url, min_comments=10):
        """
        Analisa comentários em um post e extrai perfis com comentários positivos
        
        Args:
            post_url (str): URL do post
            min_comments (int): Número mínimo de comentários a analisar
            
        Returns:
            list: Lista de dicionários com informações de perfis que fizeram comentários positivos
        """
        try:
            self.driver.get(post_url)
            time.sleep(3)
            
            # Expandir comentários se necessário
            try:
                load_more_comments = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'View all comments') or contains(text(), 'View more comments')]")))
                load_more_comments.click()
                time.sleep(3)
            except:
                pass
                
            # Tentar carregar mais comentários para ter uma amostra maior
            try:
                for _ in range(3):  # Tentar expandir mais 3 vezes
                    load_more = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Load more comments')]")
                    load_more.click()
                    time.sleep(2)
            except:
                pass
                
            # Coletar comentários
            comments_data = []
            comment_elements = self.driver.find_elements(By.XPATH, "//ul/li/div/div/div[2]/span")
            username_elements = self.driver.find_elements(By.XPATH, "//ul/li/div/div/div/h3/div/span/a")
            
            # Garantir que temos o mesmo número de elementos para ambos
            min_len = min(len(comment_elements), len(username_elements))
            
            for i in range(min_len):
                try:
                    username = username_elements[i].text
                    comment_text = comment_elements[i].text
                    
                    # Analisar sentimento (VADER funciona melhor para inglês)
                    sentiment = self.sia.polarity_scores(comment_text)
                    
                    # Verificar se o comentário é positivo
                    # Para comentários em português, podemos adicionar heurísticas extras
                    is_positive = sentiment['compound'] > 0.3 or any(word in comment_text.lower() for word in [
                        "amei", "incrível", "excelente", "ótimo", "perfeito", "adorei", 
                        "maravilhoso", "top", "love", "amazing", "great", "perfect", "awesome"
                    ])
                    
                    # Excluir comentários muito curtos ou que são apenas emojis
                    if len(comment_text.strip()) < 3 or comment_text.strip().startswith("@"):
                        continue
                        
                    if is_positive:
                        profile_url = f"https://www.instagram.com/{username}/"
                        
                        comments_data.append({
                            "username": username,
                            "profile_url": profile_url,
                            "comment": comment_text,
                            "sentiment_score": sentiment['compound'],
                            "post_url": post_url
                        })
                        
                except Exception as e:
                    print(f"Erro ao processar comentário: {e}")
                    continue
                    
            print(f"Encontrados {len(comments_data)} comentários positivos no post")
            return comments_data
            
        except Exception as e:
            print(f"Erro ao analisar comentários: {e}")
            return []
            
    def get_profile_info(self, username):
        """
        Obtém informações do perfil de um usuário
        
        Args:
            username (str): Nome de usuário do Instagram
            
        Returns:
            dict: Informações do perfil
        """
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(3)
            
            # Coletar informações básicas
            try:
                bio = self.driver.find_element(By.XPATH, "//div[contains(@class, '-vDIg')]/span").text
            except:
                bio = ""
                
            try:
                followers_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span")
                followers = followers_element.get_attribute("title") or followers_element.text
            except:
                followers = "0"
                
            try:
                following_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]/span")
                following = following_element.text
            except:
                following = "0"
                
            try:
                posts_count_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'g47SY')]")
                posts_count = posts_count_element.text
            except:
                posts_count = "0"
                
            try:
                full_name = self.driver.find_element(By.XPATH, "//h1").text
            except:
                full_name = username
                
            # Verificar se é uma conta privada
            try:
                private_account = self.driver.find_elements(By.XPATH, "//h2[contains(text(), 'This Account is Private') or contains(text(), 'Esta conta é privada')]")
                is_private = len(private_account) > 0
            except:
                is_private = False
                
            # Verificar se tem email na bio
            email = ""
            if "@" in bio and "." in bio:
                import re
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', bio)
                if email_match:
                    email = email_match.group(0)
                    
            profile_info = {
                "username": username,
                "full_name": full_name,
                "bio": bio,
                "followers": followers,
                "following": following,
                "posts_count": posts_count,
                "is_private": is_private,
                "email": email,
                "profile_url": f"https://www.instagram.com/{username}/",
                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return profile_info
            
        except Exception as e:
            print(f"Erro ao obter informações do perfil @{username}: {e}")
            return {
                "username": username,
                "error": str(e),
                "profile_url": f"https://www.instagram.com/{username}/"
            }
            
    def scrape_nicho(self, nicho, max_business_accounts=5, max_posts_per_account=3):
        """
        Executa o fluxo completo de raspagem para um nicho específico
        
        Args:
            nicho (str): Nicho a ser pesquisado
            max_business_accounts (int): Número máximo de contas comerciais a analisar
            max_posts_per_account (int): Número máximo de posts por conta
            
        Returns:
            list: Lista de perfis com comentários positivos
        """
        print(f"\n{'='*50}")
        print(f"Iniciando raspagem para o nicho: {nicho}")
        print(f"{'='*50}\n")
        
        positive_profiles = []
        
        # 1. Buscar contas comerciais do nicho
        business_accounts = self.search_business_accounts(nicho, max_business_accounts)
        
        # 2. Para cada conta comercial
        for account in business_accounts:
            print(f"\nAnalisando conta comercial: @{account}")
            
            # 3. Obter posts recentes
            posts = self.get_recent_posts(account, max_posts_per_account)
            
            # 4. Para cada post
            for post_url in posts:
                print(f"  Analisando post: {post_url}")
                
                # 5. Verificar se é um anúncio
                is_ad = self.is_ad_post(post_url)
                if not is_ad:
                    print("  Este post não parece ser um anúncio. Pulando.")
                    continue
                    
                print("  Post identificado como anúncio!")
                
                # 6. Analisar comentários e extrair perfis com comentários positivos
                positive_comments = self.analyze_comments(post_url)
                
                # 7. Para cada perfil positivo
                for comment_data in positive_comments:
                    username = comment_data["username"]
                    
                    # Verificar se já temos este perfil para evitar duplicatas
                    if any(profile["username"] == username for profile in positive_profiles):
                        continue
                        
                    # 8. Obter informações do perfil
                    print(f"    Coletando informações do perfil: @{username}")
                    profile_info = self.get_profile_info(username)
                    
                    # Mesclar informações do perfil com dados do comentário
                    profile_data = {**profile_info, **comment_data}
                    positive_profiles.append(profile_data)
                    
                    # Adicionar atraso aleatório para evitar bloqueio
                    time.sleep(random.uniform(1.5, 3.5))
                    
                # Adicionar atraso entre posts
                time.sleep(random.uniform(2, 5))
                
            # Adicionar atraso entre contas
            time.sleep(random.uniform(3, 7))
            
        # Salvar resultados
        self.save_results(nicho, positive_profiles)
        
        print(f"\n{'='*50}")
        print(f"Raspagem concluída para o nicho: {nicho}")
        print(f"Total de perfis com comentários positivos: {len(positive_profiles)}")
        print(f"{'='*50}\n")
        
        return positive_profiles
        
    def save_results(self, nicho, profiles):
        """
        Salva os resultados em CSV e JSON
        
        Args:
            nicho (str): Nicho analisado
            profiles (list): Lista de perfis com comentários positivos
        """
        # Criar diretório para o nicho
        nicho_dir = os.path.join(self.data_dir, nicho.replace(" ", "_"))
        os.makedirs(nicho_dir, exist_ok=True)
        
        # Nome dos arquivos com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = os.path.join(nicho_dir, f"perfis_positivos_{timestamp}.csv")
        json_filename = os.path.join(nicho_dir, f"perfis_positivos_{timestamp}.json")
        
        # Salvar como CSV
        if profiles:
            # Usar o primeiro perfil para obter os cabeçalhos
            fieldnames = profiles[0].keys()
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for profile in profiles:
                    writer.writerow(profile)
                    
            # Salvar como JSON
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(profiles, json_file, indent=4, ensure_ascii=False)
                
            print(f"Resultados salvos em:")
            print(f"  CSV: {csv_filename}")
            print(f"  JSON: {json_filename}")
            
    def close(self):
        """Fecha o navegador e libera recursos"""
        if self.driver:
            self.driver.quit()
            print("Navegador fechado.")


def main():
    """Função principal para executar o raspador"""
    # Obter credenciais do usuário
    username = input("Digite seu nome de usuário do Instagram: ")
    password = input("Digite sua senha do Instagram: ")
    
    # Inicializar o raspador
    scraper = InstagramScraper(username, password, headless=False)
    
    try:
        # Fazer login
        if not scraper.login():
            print("Falha ao fazer login. Verificar credenciais.")
            return
            
        # Perguntar ao usuário o nicho a ser analisado
        nicho = input("\nDigite o nicho que deseja analisar (ex: moda, fitness, tecnologia): ")
        
        # Executar raspagem
        scraper.scrape_nicho(nicho)
        
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro não esperado: {e}")
    finally:
        # Fechar o navegador
        scraper.close()


if __name__ == "__main__":
    main()

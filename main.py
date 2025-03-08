import os
import json
import time
import random
import requests
import hashlib
import threading
from fake_useragent import UserAgent
from rich.console import Console
from rich.table import Table
from typing import Dict, Optional

console = Console()

def rainbow_banner():
    os.system("clear" if os.name == "posix" else "cls")
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    banner = """
  _______                          
 |     __|.--.--.---.-.-----.---.-.\n |__     ||  |  |  _  |-- __|  _  |\n |_______||___  |___._|_____|___._|\n          |_____|                   
    """
    for i, char in enumerate(banner):
        color = colors[i % len(colors)]
        console.print(char, style=color, end="")
        time.sleep(0.003)
    console.print("\nPlease wait...", style="bright_yellow")
    time.sleep(2)
    os.system("clear" if os.name == "posix" else "cls")
    for i, char in enumerate(banner):
        color = colors[i % len(colors)]
        console.print(char, style=color, end="")
    console.print(style="bright_yellow")

class KivanetAutomation:
    def __init__(self):
        self.console = Console()
        self.ensure_files_exist()
        self.load_credentials()
        self.load_proxies()
        self.load_headers()
        self.base_url = "https://app.kivanet.com/api"
        self.account_data = {}
    
    def ensure_files_exist(self):
        files_to_create = ['acc.txt', 'proxy.txt', 'headers.json']
        for file in files_to_create:
            if not os.path.exists(file):
                open(file, 'w').close()
                self.console.print(f"[yellow]Created {file} file[/yellow]")
    
    def generate_password_hash(self, password: str) -> str:
        return hashlib.md5(password.encode('utf-8')).hexdigest()
    
    def load_credentials(self):
        try:
            with open('acc.txt', 'r') as f:
                self.accounts = []
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) == 2:
                            email, password = parts
                            encrypted_password = self.generate_password_hash(password)
                            self.accounts.append([email, encrypted_password])
                        else:
                            self.console.print(f"[red]Invalid account format: {line}[/red]")
            if not self.accounts:
                self.console.print("[red]No accounts found in acc.txt[/red]")
        except Exception as e:
            self.console.print(f"[bold red]Error loading accounts: {e}[/bold red]")
            self.accounts = []
    
    def load_proxies(self):
        try:
            with open('proxy.txt', 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            if not self.proxies:
                self.console.print("[yellow]No proxies found. Running without proxy.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error loading proxies: {e}[/red]")
            self.proxies = []
    
    def load_headers(self):
        try:
            with open('headers.json', 'r') as f:
                self.headers_cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.headers_cache = {}
    
    def save_headers(self):
        with open('headers.json', 'w') as f:
            json.dump(self.headers_cache, f, indent=2)
    
    def generate_headers(self, email: str) -> Dict[str, str]:
        try:
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random,
                'Accept': '*/*',
                'Accept-Language': 'id-ID,id;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Content-Type': 'application/json',
                'Origin': 'https://app.kivanet.com',
                'Referer': 'https://app.kivanet.com/',
                'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1'
            }
            self.headers_cache[email] = headers
            self.save_headers()
            return headers
        except Exception as e:
            self.console.print(f"[red]Error generating headers: {e}[/red]")
            return {}
    
    def get_headers(self, email: str) -> Dict[str, str]:
        return self.headers_cache.get(email) or self.generate_headers(email)
    
    def login(self, email: str, encrypted_password: str) -> Optional[str]:
        session = requests.Session()
        headers = self.get_headers(email)
        proxies = None
        if self.proxies:
            proxy = random.choice(self.proxies)
            proxies = {'http': proxy, 'https': proxy}
        
        payload = {"email": email, "password": encrypted_password}
        try:
            response = session.post(
                f"{self.base_url}/user/login",
                json=payload,
                headers=headers,
                proxies=proxies,
                timeout=10
            )
            data = response.json()
            if data.get('state'):
                token = data.get('object')
                self.account_data[email] = {'session': session, 'token': token}
                self.console.print(f"[green]Login successful for {email}[/green]")
                return token
            else:
                self.console.print(f"[red]Login failed for {email}: {data.get('message', 'Unknown error')}[/red]")
                return None
        except requests.RequestException as e:
            self.console.print(f"[red]Network error during login for {email}: {e}[/red]")
            return None
        except json.JSONDecodeError:
            self.console.print(f"[red]Invalid response from server for {email}: {response.text[:100]}[/red]")
            return None
    
    def get_user_info(self, email: str) -> Optional[Dict]:
        data = self.account_data.get(email, {})
        session = data.get('session')
        token = data.get('token')
        headers = self.get_headers(email)
        try:
            response = session.get(
                f"{self.base_url}/user/getUserInfo",
                headers={**headers, 'Authorization': f"Bearer {token}"},
                timeout=10
            )
            data = response.json()
            return data.get('object') if data.get('state') else None
        except Exception as e:
            self.console.print(f"[red]User info retrieval error for {email}: {e}[/red]")
            return None
    
    def get_sign_info(self, email: str) -> Optional[Dict]:
        data = self.account_data.get(email, {})
        session = data.get('session')
        token = data.get('token')
        headers = self.get_headers(email)
        try:
            response = session.get(
                f"{self.base_url}/user/getSignInfo",
                headers={**headers, 'Authorization': f"Bearer {token}"},
                timeout=10
            )
            data = response.json()
            if data.get('state'):
                return data.get('object', {})
            else:
                error_code = data.get('code', 'Unknown')
                if error_code == "0009":
                    self.console.print(f"[yellow]Account {email} may need to sign or activate first (Error 0009)[/yellow]")
                else:
                    self.console.print(f"[yellow]Failed to fetch sign info for {email}: {data.get('message', 'Unknown error')} - Code: {error_code}[/yellow]")
                return {}
        except Exception as e:
            self.console.print(f"[red]Sign info retrieval error for {email}: {e}[/red]")
            return {}
    
    def get_mining_base(self, email: str) -> Optional[Dict]:
        data = self.account_data.get(email, {})
        session = data.get('session')
        token = data.get('token')
        headers = self.get_headers(email)
        try:
            response = session.get(
                f"{self.base_url}/user/getMiningBaseList",
                headers={**headers, 'Authorization': f"Bearer {token}"},
                timeout=10
            )
            data = response.json()
            if data.get('state'):
                return data.get('object', {})
            self.console.print(f"[yellow]Failed to fetch mining base for {email}: {data.get('message', 'Unknown error')}[/yellow]")
            return {}
        except Exception as e:
            self.console.print(f"[red]Mining base retrieval error for {email}: {e}[/red]")
            return {}
    
    def display_account_info(self, user_info: Dict, sign_info: Dict, email: str):
        if not user_info or not isinstance(user_info, dict):
            self.console.print(f"[red]User info is invalid or missing for {email}[/red]")
            return
        
        table = Table(title=f"[bold green]User: {user_info.get('nickName', 'N/A')}[/bold green]")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")
        
        details = {
            "Email": user_info.get('email', 'N/A'),
            "Invite Number": user_info.get('inviteNum', 'N/A'),
            "Created Time": user_info.get('createTime', 'N/A'),
            "Balance": sign_info.get('allAccount', 'N/A') if sign_info else 'N/A',
            "Sign Time": sign_info.get('signTime', 'N/A') if sign_info else 'N/A'
        }
        
        for key, value in details.items():
            table.add_row(key, str(value))
        
        self.console.print(table)
    
    def keep_alive(self, email: str, encrypted_password: str):
        while True:
            token = self.account_data.get(email, {}).get('token')
            if not token:
                token = self.login(email, encrypted_password)
                if not token:
                    self.console.print(f"[red]Initial login failed for {email}, retrying in 60s[/red]")
                    time.sleep(60)
                    continue
            
            user_info = self.get_user_info(email)
            sign_info = self.get_sign_info(email)
            mining_base = self.get_mining_base(email)
            
            if not user_info:  # Jika user_info gagal, coba login ulang
                self.console.print(f"[yellow]Reattempting login for {email} due to user info failure[/yellow]")
                time.sleep(5)
                new_token = self.login(email, encrypted_password)
                if new_token:
                    token = new_token
                else:
                    self.console.print(f"[red]Re-login failed for {email}, skipping this cycle[/red]")
                    time.sleep(60)
                    continue
            
            self.display_account_info(user_info, sign_info, email)
            
            if mining_base:
                self.console.print(f"[green]Heartbeat active - Mining Base Users: {mining_base.get('userNum', 'N/A')}[/green]")
            
            heartbeat_delay = random.uniform(60, 300)  # 1-5 menit
            minutes, seconds = divmod(int(heartbeat_delay), 60)
            formatted_time = f"00:{minutes:02d}:{seconds:02d}"
            self.console.print(f"[cyan]Next heartbeat for {email} in: {formatted_time}[/cyan]")
            time.sleep(heartbeat_delay)
    
    def main_automation(self):
        if not self.accounts:
            self.console.print("[red]No accounts loaded. Please check acc.txt[/red]")
            return

        threads = []
        for email, encrypted_password in self.accounts:
            self.console.print(f"\n{'━' * 40}")
            
            token = self.login(email, encrypted_password)
            if not token:
                self.console.print(f"[red]Skipping {email} due to login failure[/red]")
                continue
            
            thread = threading.Thread(target=self.keep_alive, args=(email, encrypted_password))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

def main():
    rainbow_banner()
    try:
        automation = KivanetAutomation()
        automation.main_automation()
    except KeyboardInterrupt:
        print("\n[Interrupted] Script stopped by user.")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()

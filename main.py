import os
import re
import json
import time
import random
import requests
import hashlib
import hmac
from fake_useragent import UserAgent
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import Dict, List, Optional

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
        # Initialize console for rich output
        self.console = Console()
        
        # Create necessary files if they don't exist
        self.ensure_files_exist()
        
        # Load credentials and configuration
        self.load_credentials()
        self.load_proxies()
        self.load_headers()
        
        # Base URL for API endpoints
        self.base_url = "https://app.kivanet.com/api"
    
    def ensure_files_exist(self):
        """Create necessary files if they don't exist"""
        files_to_create = ['acc.txt', 'proxy.txt', 'headers.json']
        for file in files_to_create:
            if not os.path.exists(file):
                open(file, 'w').close()
                self.console.print(f"[yellow]Created {file} file[/yellow]")
    
    def generate_password_hash(self, password: str) -> str:
        """
        Generate password hash 
        This is a placeholder - you'll need to replace with actual encryption method
        """
        # Example method - may need adjustment based on actual encryption
        return hashlib.md5(password.encode('utf-8')).hexdigest()
    
    def load_credentials(self):
        """Load accounts from acc.txt"""
        try:
            with open('acc.txt', 'r') as f:
                self.accounts = []
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) == 2:
                            email, password = parts
                            # Optional: Apply password hash transformation
                            encrypted_password = self.generate_password_hash(password)
                            self.accounts.append([email, encrypted_password])
                        else:
                            self.console.print(f"[red]Invalid account format: {line}[/red]")
        except Exception as e:
            self.console.print(f"[bold red]Error loading accounts: {e}[/bold red]")
            self.accounts = []
    
    def load_proxies(self):
        """Load proxies from proxy.txt"""
        try:
            with open('proxy.txt', 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            
            if not self.proxies:
                self.console.print("[yellow]No proxies found. Running without proxy.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error loading proxies: {e}[/red]")
            self.proxies = []
    
    def load_headers(self):
        """Load or initialize headers"""
        try:
            with open('headers.json', 'r') as f:
                self.headers_cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.headers_cache = {}
    
    def save_headers(self):
        """Save headers to headers.json"""
        with open('headers.json', 'w') as f:
            json.dump(self.headers_cache, f, indent=2)
    
    def generate_headers(self, email: str) -> Dict[str, str]:
        """Generate headers with fake user agent"""
        try:
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random,
                'Accept': '*/*',
                'Accept-Language': 'id-ID,id;q=0.7',
                'Content-Type': 'application/json',
                'Origin': 'https://app.kivanet.com',
                'Referer': 'https://app.kivanet.com/'
            }
            self.headers_cache[email] = headers
            self.save_headers()
            return headers
        except Exception as e:
            self.console.print(f"[red]Error generating headers: {e}[/red]")
            return {}
    
    def get_headers(self, email: str) -> Dict[str, str]:
        """Get or generate headers for an account"""
        return self.headers_cache.get(email) or self.generate_headers(email)
    
    def login(self, email: str, encrypted_password: str) -> Optional[str]:
        """Login to Kivanet and return bearer token"""
        headers = self.get_headers(email)
        
        # Select a random proxy if available
        proxies = None
        if self.proxies:
            proxy = random.choice(self.proxies)
            proxies = {'http': proxy, 'https': proxy}
        
        try:
            response = requests.post(
                f"{self.base_url}/user/login", 
                json={"email": email, "password": encrypted_password},
                headers=headers,
                proxies=proxies,
                timeout=10
            )
            
            data = response.json()
            
            if data.get('state'):
                return data.get('object')
            else:
                return None
        
        except requests.RequestException as e:
            self.console.print(f"[red]Network error during login: {e}[/red]")
            return None
        except json.JSONDecodeError:
            self.console.print(f"[red]Invalid response from server for {email}[/red]")
            return None
    
    def get_user_info(self, token: str, headers: Dict[str, str]) -> Optional[Dict]:
        """Retrieve user information"""
        try:
            response = requests.get(
                f"{self.base_url}/user/getUserInfo",
                headers={**headers, 'Authorization': token},
                timeout=10
            )
            data = response.json()
            return data.get('object') if data.get('state') else None
        except Exception as e:
            self.console.print(f"[red]User info retrieval error: {e}[/red]")
            return None
    
    def get_task_list(self, token: str, headers: Dict[str, str]) -> List[Dict]:
        """Retrieve list of tasks"""
        try:
            response = requests.post(
                f"{self.base_url}/task/getTaskList",
                headers={**headers, 'Authorization': token},
                json={"status": 1},  # Updated to use actual payload
                timeout=10
            )
            data = response.json()
            return data.get('object', []) if data.get('state') else []
        except Exception as e:
            self.console.print(f"[red]Task list retrieval error: {e}[/red]")
            return []
    
    def do_task(self, token: str, headers: Dict[str, str], task_id: str) -> bool:
        """Complete a specific task"""
        try:
            response = requests.post(
                f"{self.base_url}/task/doTask",
                headers={**headers, 'Authorization': token},
                json={"id": task_id},
                timeout=10
            )
            data = response.json()
            if data.get('state'):
                return True
            else:
                return False
        except Exception as e:
            self.console.print(f"[red]Task completion error: {e}[/red]")
            return False
    
    def complete_tasks(self, token: str, headers: Dict[str, str], tasks: List[Dict]) -> None:
        """Complete available tasks"""
        for task in tasks:
            task_delay = random.uniform(7, 14)
            
            with Progress(console=self.console) as progress:
                task_progress = progress.add_task(
                    f"[cyan]Completing task: {task['taskName']}[/cyan]", 
                    total=task_delay
                )
                
                while not progress.finished:
                    progress.update(task_progress, advance=0.1)
                    time.sleep(0.1)
            
            # Attempt to complete the task
            task_completed = self.do_task(token, headers, task['id'])
    
    def get_account_balance(self, token: str, headers: Dict[str, str]) -> Dict:
        """Retrieve user account balance"""
        try:
            response = requests.get(
                f"{self.base_url}/user/getMyAccountInfo",
                headers={**headers, 'Authorization': token},
                timeout=10
            )
            data = response.json()
            return data.get('object', {}) if data.get('state') else {}
        except Exception as e:
            self.console.print(f"[red]Balance retrieval error: {e}[/red]")
            return {}
    
    def display_account_info(self, user_info: Dict, balance_info: Dict):
        """Display account information in a rich table"""
        table = Table(title=f"[bold green]User: {user_info.get('nickName', 'N/A')}[/bold green]")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")
        
        # Add account details to the table
        details = {
            "Email": user_info.get('email', 'N/A'),
            "Invite Number": user_info.get('inviteNum', 'N/A'),
            "Created Time": user_info.get('createTime', 'N/A'),
            "Balance": balance_info.get('balance', 'N/A'),
            "Chain Address": balance_info.get('chainAddress', 'N/A')
        }
        
        for key, value in details.items():
            table.add_row(key, str(value))
        
        self.console.print(table)
    
    def main_automation(self):
        """Main automation workflow"""
        for email, encrypted_password in self.accounts:
            self.console.print(f"\n{'━' * 40}")
            
            # Login
            token = self.login(email, encrypted_password)
            if not token:
                continue
            
            headers = self.get_headers(email)
            
            # Get User Info
            user_info = self.get_user_info(token, headers)
            if not user_info:
                continue
            
            # Get Balance Info
            balance_info = self.get_account_balance(token, headers)
            
            # Display Account Info
            self.display_account_info(user_info, balance_info)
            
            # Get and Complete Tasks
            tasks = self.get_task_list(token, headers)
            if tasks:
                self.complete_tasks(token, headers, tasks)
        
        # Random sleep between next batch of account processing (1-7 minutes)
        next_run_time = random.uniform(60, 7 * 60) # 60 seconds (1 minute) to 420 seconds (7 minutes)

        # Convert seconds to formatted time
        minutes, seconds = divmod(int(next_run_time), 60)
        formatted_time = f"00:{minutes:02d}:{seconds:02d}"  # Always start with 00 hours

        self.console.print(f"\n[bold yellow]Next run in: {formatted_time}[/bold yellow]")
        time.sleep(next_run_time)

def main():
    rainbow_banner()
    try:
        automation = KivanetAutomation()
        while True:
            automation.main_automation()
    except KeyboardInterrupt:
        print("\n[Interrupted] Script stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

import subprocess
import sqlite3
from tld import get_fld

con = sqlite3.connect("providers.db")


common_providers = [
    {
        "provider": "Google",
        "provider_domain": "https://mail.google.com",
        "domain": ["gmail.com"],
    },
    {
        "provider": "Microsoft",
        "provider_domain": "https://outlook.live.com",
        "domain": [
            "outlook.com", 
            "hotmail.com", 
            "live.com",
            "msn.com"
            ],
    },
    {
        "provider": "Yahoo",
        "provider_domain": "yahoo.com",
        "domain": [
            "yahoo.com",
            "ymail.com",
            "rocketmail.com",
            "yahoo.co.uk",
            "yahoo.ca",
            "yahoo.de",
            "yahoo.fr",
            "yahoo.com.au",
    ],
    }
]

def create_database():
    con = sqlite3.connect("providers.db")
    con.execute("CREATE TABLE IF NOT EXISTS providers (domain TEXT, mx TEXT, provider TEXT)")
    con.close()

def create_common_providers():
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    for provider in common_providers:
        for domain in provider["domain"]:
            cur.execute("INSERT INTO providers (domain, mx, provider) VALUES (?, ?, ?)", (domain, provider["provider_domain"], provider["provider"]))
    con.commit()
    con.close()

def search_provider(domain):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT provider FROM providers WHERE domain = ?", (domain,))
    provider = cur.fetchone()
    con.close()
    if not provider:
        dig_mx(domain)
        mx, fld = get_mx(domain)
        provider = find_provider_by_domain(fld)
        remove_mx_file(domain)
        if provider:
            add_provider(domain, mx, provider)
        else:
            add_provider(domain, mx, "Unknown")
    return provider


def search_mx(domain):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT mx FROM providers WHERE domain = ?", (domain,))
    mx = cur.fetchone()
    con.close()
    return mx


def search_domain(provider):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT domain FROM providers WHERE provider = ?", (provider,))
    domain = cur.fetchone()
    con.close()
    return domain

def search_all():
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM providers")
    all = cur.fetchall()
    con.close()
    return all

def add_provider(domain, mx, provider):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("INSERT INTO providers (domain, mx, provider) VALUES (?, ?, ?)", (domain, mx, provider))
    con.commit()
    con.close()


def remove_provider(domain):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("DELETE FROM providers WHERE domain = ?", (domain,))
    con.commit()
    con.close()


def update_provider(domain, mx, provider):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("UPDATE providers SET mx = ?, provider = ? WHERE domain = ?", (mx, provider, domain))
    con.commit()
    con.close()


def update_mx(domain, mx):
    con = sqlite3.connect("providers.db")
    cur = con.cursor()
    cur.execute("UPDATE providers SET mx = ? WHERE domain = ?", (mx, domain))
    con.commit()
    con.close()


def dig_mx(domain):
    subprocess.Popen(f"dig {domain} MX >> {domain}.txt", shell=True)
    return f"{domain}.txt"


def get_mx(domain):
    with open(f"{domain}.txt") as f:
        lines = f.readlines()
        mx = lines[13].split()[5]
        fld = get_fld(mx, as_object=True)
        return mx, fld

def remove_mx_file(domain):
    subprocess.Popen(f"rm {domain}.txt", shell=True)
    return 


def find_provider_by_domain(search_domain):
    for provider_info in common_providers:
        if search_domain in provider_info["domain"]:
            return provider_info
    return None
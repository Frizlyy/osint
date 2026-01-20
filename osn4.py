#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tool: OSN ULTIMATE (UI + FUNCTION)
# Coded by: r¡xs-bot
# Status: FINAL | NO MISSING FEATURES

import os
import sys
import shutil
import random
import time
import requests
import re

# --- COLORS (CYBERPUNK THEME) ---
P  = "\033[38;5;129m" # Purple Dark
P2 = "\033[38;5;141m" # Purple Light
C  = "\033[38;5;45m"  # Cyan Dark
C2 = "\033[38;5;87m"  # Cyan Light
W  = "\033[0m"        # White/Reset
G  = "\033[32m"       # Green
R  = "\033[31m"       # Red
Y  = "\033[33m"       # Yellow

# --- CONFIG ---
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# --- UI ENGINE ---
def get_cols():
    return shutil.get_terminal_size().columns

def center_text(text):
    cols = get_cols()
    # Strip ansi for len calc (simple approx)
    clean = text.replace(P,"").replace(P2,"").replace(C,"").replace(C2,"").replace(W,"").replace(G,"").replace(R,"").replace(Y,"")
    padding = (cols - len(clean)) // 2
    return " " * padding + text

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    cols = get_cols()
    logo_art = [
        f"{P2}  ██████  ██████  ███    ██ {W}",
        f"{P} ██    ██ ██      ████   ██ {W}",
        f"{C} ██    ██ ███████ ██ ██  ██ {W}",
        f"{C} ██    ██      ██ ██  ██ ██ {W}",
        f"{C2}  ██████  ██████  ██   ████ {W}"
    ]
    print("\n")
    for line in logo_art:
        clean_line = line.replace(P2, "").replace(P, "").replace(C, "").replace(C2, "").replace(W, "")
        padding = (cols - len(clean_line)) // 2
        print(" " * padding + line)
    print(center_text(f"{C2}OSINT & RECONNAISSANCE SUITE{W}"))
    print(center_text(f"{P}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}"))
    print("\n")

def draw_dual_box(left_title, right_title):
    cols = get_cols()
    box_width = 20 
    l_title = left_title[:box_width-2].center(box_width)
    r_title = right_title[:box_width-2].center(box_width)
    
    l_top = f"{P}┌{'─'*box_width}┐{W}"
    l_mid = f"{P}│{W}{l_title}{P}│{W}"
    l_bot = f"{P}└{'─'*box_width}┘{W}"
    
    r_top = f"{C}┌{'─'*box_width}┐{W}"
    r_mid = f"{C}│{W}{r_title}{C}│{W}"
    r_bot = f"{C}└{'─'*box_width}┘{W}"
    
    total_width = (box_width + 2) * 2 + 2
    
    if cols < total_width:
        padding = (cols - (box_width + 2)) // 2
        pad = " " * padding
        print(f"{pad}{l_top}\n{pad}{l_mid}\n{pad}{l_bot}")
        print(f"{pad}{r_top}\n{pad}{r_mid}\n{pad}{r_bot}")
    else:
        padding = (cols - total_width) // 2
        pad = " " * padding
        print(f"{pad}{l_top}  {r_top}")
        print(f"{pad}{l_mid}  {r_mid}")
        print(f"{pad}{l_bot}  {r_bot}")

def draw_single_box(text, color=R):
    cols = get_cols()
    box_width = 20
    title = text[:box_width-2].center(box_width)
    top = f"{color}┌{'─'*box_width}┐{W}"
    mid = f"{color}│{W}{title}{color}│{W}"
    bot = f"{color}└{'─'*box_width}┘{W}"
    padding = (cols - (box_width + 2)) // 2
    pad = " " * padding
    print(f"{pad}{top}\n{pad}{mid}\n{pad}{bot}")

def footer():
    print("\n")
    sig = [
        f"{P}      _             {C} _             _      ",
        f"{P} _ __(_)__  ___{C}   | |_ ___  ___| |____ ",
        f"{P}| '__| \\ \\/ /_  /{C}  | __/ _ \\/ _ \\ |_  / ",
        f"{P}| |  | |>  < / / {C}  | || (_) | (_) | |/ /  ",
        f"{P}|_|  |_/_/\\_/___|{C}   \\__\\___/ \\___/|_/___| "
    ]
    for line in sig: print(center_text(line))
    print(center_text(f"{P2}v3.5 | FULL FUNCTIONAL{W}"))

# --- FEATURES IMPLEMENTATION ---

# 1. DORK DB
def f_dork_db():
    banner()
    print(center_text(f"{P2}:: DORK DATABASE MANAGER ::{W}"))
    try:
        with open("dork.txt", "r", encoding="utf-8") as f:
            dorks = [line.strip() for line in f if line.strip()]
        print(center_text(f"{G}[LOADED] {len(dorks)} Dorks{W}"))
        print("\n")
        print(f"{P}[1] Show All  [2] Random 10  [3] Search{W}")
        c = input(f"\n{P}opt > {W}")
        if c == '1':
            for d in dorks: print(f"{C}-> {W}{d}")
        elif c == '2':
            for d in random.sample(dorks, min(10, len(dorks))): print(f"{C}-> {W}{d}")
        elif c == '3':
            q = input(f"{P}Keyword: {W}")
            matches = [d for d in dorks if q.lower() in d.lower()]
            for m in matches: print(f"{C}-> {W}{m}")
    except FileNotFoundError:
        print(center_text(f"{R}File dork.txt not found!{W}"))
    input(f"\n{center_text('[ ENTER ]')}")

# 2. SUBDOMAIN
def f_subdomain():
    banner()
    print(center_text(f"{C2}:: SUBDOMAIN SCANNER ::{W}"))
    d = input(f"\n{P}Domain (no http): {W}").strip()
    print(f"\n{Y}[*] Scanning crt.sh...{W}")
    try:
        r = requests.get(f"https://crt.sh/?q={d}&output=json", timeout=10)
        data = r.json()
        seen = set()
        for item in data:
            name = item['name_value']
            if name not in seen:
                seen.add(name)
                print(f"{G}-> {name}{W}")
    except Exception as e:
        print(f"{R}Error: {e}{W}")
    input(f"\n{center_text('[ ENTER ]')}")

# 3. SYSTEM WHOIS
def f_whois():
    banner()
    print(center_text(f"{P2}:: SYSTEM WHOIS ::{W}"))
    d = input(f"\n{P}Domain: {W}").strip()
    print(f"\n{C}--------------------------------{W}")
    os.system(f"whois {d}")
    print(f"{C}--------------------------------{W}")
    input(f"\n{center_text('[ ENTER ]')}")

# 4. NMAP
def f_nmap():
    banner()
    print(center_text(f"{C2}:: NMAP SCANNER ::{W}"))
    t = input(f"\n{P}Target IP/Domain: {W}").strip()
    print(f"{P}[1] Fast (-F)  [2] Full (-A)  [3] Vuln{W}")
    m = input(f"Mode > ")
    cmd = f"nmap -F {t}"
    if m == '2': cmd = f"nmap -A {t}"
    elif m == '3': cmd = f"nmap --script vuln {t}"
    os.system(cmd)
    input(f"\n{center_text('[ ENTER ]')}")

# 5. SOCIAL DEEP
def f_social():
    banner()
    print(center_text(f"{P2}:: DEEP SOCIAL SEARCH ::{W}"))
    u = input(f"\n{P}Username: {W}").strip()
    queries = [
        f'site:instagram.com "{u}"',
        f'site:twitter.com "{u}"',
        f'site:facebook.com "{u}"',
        f'site:tiktok.com "{u}"',
        f'site:linkedin.com "{u}"',
        f'site:twitter.com intext:"@{u}"',
        f'site:instagram.com intext:"{u}" "comment"',
        f'site:reddit.com inurl:user "{u}"',
        f'intext:"{u}" filetype:txt'
    ]
    print(f"\n{G}[*] Generated Dorks (Copy & Search):{W}\n")
    for q in queries:
        link = f"https://www.google.com/search?q={q.replace(' ', '+').replace('"', '%22')}"
        print(f"{C}[LINK]{W} {link}")
    input(f"\n{center_text('[ ENTER ]')}")

# 6. HTTP HEADER
def f_header():
    banner()
    print(center_text(f"{C2}:: HTTP HEADER CHECK ::{W}"))
    u = input(f"\n{P}URL (http/s): {W}").strip()
    try:
        r = requests.head(u, headers=HEADERS, timeout=5)
        for k,v in r.headers.items():
            print(f"{Y}{k}: {W}{v}")
    except Exception as e:
        print(f"{R}Error: {e}{W}")
    input(f"\n{center_text('[ ENTER ]')}")

# 7. ROBOTS.TXT
def f_robots():
    banner()
    print(center_text(f"{P2}:: ROBOTS.TXT SCANNER ::{W}"))
    d = input(f"\n{P}Domain: {W}").strip()
    u = f"http://{d}/robots.txt"
    try:
        r = requests.get(u, headers=HEADERS, timeout=5)
        if r.status_code == 200:
            print(f"\n{G}[FOUND]{W}\n{r.text}")
        else:
            print(f"{R}[404] Not Found{W}")
    except:
        print(f"{R}Connection Error{W}")
    input(f"\n{center_text('[ ENTER ]')}")

# 8. DNS ZONE
def f_dns():
    banner()
    print(center_text(f"{C2}:: DNS DIGGER ::{W}"))
    d = input(f"\n{P}Domain: {W}").strip()
    print(f"\n{Y}[ A RECORD ]{W}")
    os.system(f"dig +short A {d}")
    print(f"\n{Y}[ NS RECORD ]{W}")
    os.system(f"dig +short NS {d}")
    print(f"\n{Y}[ MX RECORD ]{W}")
    os.system(f"dig +short MX {d}")
    input(f"\n{center_text('[ ENTER ]')}")

# 9. LINK EXTRACTOR
def f_links():
    banner()
    print(center_text(f"{P2}:: LINK EXTRACTOR ::{W}"))
    u = input(f"\n{P}URL: {W}").strip()
    try:
        r = requests.get(u, headers=HEADERS, timeout=10)
        links = re.findall('href="(http.*?)"', r.text)
        print(f"\n{G}Found {len(links)} links.{W}")
        with open("links_dump.txt", "w") as f:
            for l in links: f.write(l+"\n")
        print(f"{Y}Saved to links_dump.txt{W}")
    except Exception as e:
        print(f"{R}Error: {e}{W}")
    input(f"\n{center_text('[ ENTER ]')}")

# 10. FAKE ID
def f_fakeid():
    banner()
    print(center_text(f"{C2}:: FAKE ID GENERATOR ::{W}"))
    names = ["Agus", "Budi", "Siti", "Dewi", "Reza", "Putri"]
    surnames = ["Pratama", "Santoso", "Wijaya", "Kusuma"]
    cities = ["Jakarta", "Surabaya", "Bandung", "Medan"]
    
    first = random.choice(names)
    last = random.choice(surnames)
    print(f"\n{P}Name      : {W}{first} {last}")
    print(f"{P}Email     : {W}{first.lower()}{random.randint(10,99)}@gmail.com")
    print(f"{P}Phone     : {W}+62 8{random.randint(11,99)}-{random.randint(1000,9999)}")
    print(f"{P}City      : {W}{random.choice(cities)}")
    input(f"\n{center_text('[ ENTER ]')}")

# --- MAIN LOOP ---
def main():
    while True:
        banner()
        draw_dual_box("1. Dork DB", "2. Subdomain")
        draw_dual_box("3. Sys Whois", "4. Nmap Scan")
        draw_dual_box("5. Social Deep", "6. HTTP Header")
        draw_dual_box("7. Robots.txt", "8. DNS Zone")
        draw_dual_box("9. Link Extr", "10. Fake ID")
        print("\n")
        draw_single_box("0. EXIT", R)
        footer()
        
        print("\n")
        try:
            c = input(f"{P}osn{C}@{P}toolz {W}> ")
        except KeyboardInterrupt:
            sys.exit()

        if c == '1': f_dork_db()
        elif c == '2': f_subdomain()
        elif c == '3': f_whois()
        elif c == '4': f_nmap()
        elif c == '5': f_social()
        elif c == '6': f_header()
        elif c == '7': f_robots()
        elif c == '8': f_dns()
        elif c == '9': f_links()
        elif c == '10': f_fakeid()
        elif c == '0': 
            print(f"\n{R}System Shutdown.{W}")
            sys.exit()

if __name__ == "__main__":
    # Auto-create dork file if missing to prevent crash
    if not os.path.exists("dork.txt"):
        with open("dork.txt", "w") as f: f.write("site:go.id inurl:admin\n")
    main()

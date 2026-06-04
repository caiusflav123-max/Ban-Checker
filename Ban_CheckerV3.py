import httpx
import asyncio
import os
import sys
import time

API_URL = "https://checkton.online/backend"
API_KEY = "tKEIiMaaXZiXgBaa-3ytHnSMOWFsG8ZjaiLHJL9t0rs"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

R    = "\033[91m"
G    = "\033[92m"
Y    = "\033[93m"
B    = "\033[94m"
M    = "\033[95m"
C    = "\033[96m"
W    = "\033[97m" 
DG   = "\033[2;32m"
DR   = "\033[2;31m"
BOLD = "\033[1m"
RST  = "\033[0m"

LINE  = f"{DG}{'─' * 58}{RST}"
DLINE = f"{M}{'═' * 58}{RST}"


def clear():
    os.system("cls" if os.name == "nt" else "clear")

async def loading(msg, duration=1.2):
    frames = ["⠋","⠙","⠸","⠴","⠦","⠇"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r  {G}{frames[i % len(frames)]}{RST}  {DG}{msg}{RST}", end="", flush=True)
        await asyncio.sleep(0.08)
        i += 1
    print(f"\r  {G}✓{RST}  {DG}{msg}{RST}   ")


def banner():
    print(f"""
{R}
██████╗  █████╗ ███╗   ██╗
██╔══██╗██╔══██╗████╗  ██║
██████╔╝███████║██╔██╗ ██║
██╔══██╗██╔══██║██║╚██╗██║
██████╔╝██║  ██║██║ ╚████║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
{RST}""")

def menu():
    print(f"{DG}Created By{RST} @Official_Caius1\n")
    print(f"{R}[{RST}{W}1{RST}{R}]{RST}  {G}Check Account{RST}")
    print(f"{R}[{RST}{W}2{RST}{R}]{RST}  {G}Exit!{RST}")
    print()

def after_menu():
    print(f"\n  {DG}root@veriton:~${RST} next action\n")
    print(f"  {R}[{RST}{W}1{RST}{R}]{RST}  {G}Check Another Account{RST}")
    print(f"  {R}[{RST}{W}2{RST}{R}]{RST}  {DR}Exit{RST}")
    print()

def step_header(label):
    print(f"\n{LINE}")
    print(f"  {Y}{label}{RST}")
    print(LINE)
    print()

def status(icon, msg, color=DG):
    print(f"  {color}{icon}{RST}  {color}{msg}{RST}")

def inp(label):
    return input(f"  {DG}>{RST} {C}{label:<20}{RST} : ").strip()

async def post(client, path, payload):
    try:
        r = await client.post(API_URL + path, json=payload, headers=headers, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def extract_block(data):
    d = data.get("data")
    if isinstance(d, list):
        return d[0] if d else None
    if isinstance(d, dict):
        return d
    return None

def show_result(combo, data):
    block = extract_block(data)

    print(f"\n{DLINE}")
    print(f"  {BOLD}{G}VERITON BAN CHECKER RESULT{RST}")
    print(DLINE)

    col_w = 14
    def row(k, v, vc=W):
        print(f"  {DG}{k:<{col_w}}{RST} {DG}│{RST} {vc}{v}{RST}")

    row("COMBO", combo)
    print(f"  {DG}{'─' * col_w}─┼─{'─' * 36}{RST}")

    if block:
        row("STATUS",         "⚠  BANNED",                          R + BOLD)
        row("ACCOUNT ID",     block.get('id', 'N/A'),                R)
        row("REASON",         block.get('reason', 'N/A'),            Y)
        row("VIOLATION TIME", block.get('violation_time', 'N/A'),    Y)
        row("UNLOCK TIME",    block.get('unlock_time', 'N/A'),       C)
    else:
        row("STATUS", "✓  NOT BANNED",   G + BOLD)
        row("REASON", "No Ban Data Found!", DG)

    print(DLINE)

# login success check
def is_login_success(data):
    if isinstance(data.get("error"), str):
        return False
    return bool(data.get("data"))

async def checker():

    step_header("ACCOUNT CREDENTIALS")

    combo = inp("EMAIL:PASSWORD")
    if ":" not in combo:
        print(f"\n  {R}✗  Invalid combo format! Use email:password{RST}")
        return
    email, password = combo.split(":", 1)

    proxy   = inp("PROXY")
    captcha = inp("CN31 CAPTCHA")

    print(f"\n{LINE}")
    print(f"  {Y}PROCESSING...{RST}")
    print(LINE)
    print()

    async with httpx.AsyncClient() as client:

        # LOGIN
        await loading("Logging in...")

        login_data = await post(client, "/check", {
            "login": email,
            "password": password,
            "proxy": proxy,
            "captcha_cn31": captcha,
            "type": "login"
        })

        if not is_login_success(login_data):
            print(f"\n  {R}✗  Login failed.{RST}")
            return

        status("✓", "Login successful.", G)

        raw = login_data.get("data", {})
        if isinstance(raw, list):
            raw = raw[0] if raw else {}
        auto_guid    = raw.get("guid", "")       if isinstance(raw, dict) else ""
        auto_session = raw.get("session_id", "") if isinstance(raw, dict) else ""
        if not auto_session:
            auto_session = raw.get("session", "") if isinstance(raw, dict) else ""

        if auto_guid:
            status("→", f"GUID     : {auto_guid}", C)
        if auto_session:
            status("→", f"SESSION  : {auto_session}", C)

        guid       = auto_guid    if auto_guid    else inp("GUID")
        session_id = auto_session if auto_session else inp("SESSION ID")

        print()
        await loading("Generating JWT token...")

        jwt_data = await post(client, "/getJwt", {
            "guid": guid,
            "session_id": session_id,
            "proxy": proxy
        })

        jwt   = jwt_data.get("jwt")   or jwt_data.get("data", {}).get("jwt")
        token = jwt_data.get("token") or jwt_data.get("data", {}).get("token")

        if not jwt:
            print(f"\n  {R}✗  JWT generation failed.{RST}")
            return

        status("✓", "JWT obtained.", G)
        print(f"  {DG}JWT    │{RST} {C}{str(jwt)[:55]}...{RST}")
        if token:
            print(f"  {DG}TOKEN  │{RST} {C}{str(token)[:55]}...{RST}")

        print(f"\n{LINE}")
        input(f"  {Y}[ Press Enter to Continue ]{RST}")
        print(LINE)
        print()

     
        await loading("Querying ban database...")

        ban_data = await post(client, "/getBanInfo", {
            "jwt": jwt,
            "token": token,
            "proxy": proxy
        })

        show_result(combo, ban_data)

async def run():
    while True:
        clear()
        banner()
        menu()

        choice = input(f"{DG}> {RST}{C}Select Option{RST}: ").strip()

        if choice == "1":
            clear()
            banner()
            await checker()
            after_menu()
            nxt = input(f"{DG}>{RST}{C}Select Option{RST} : ").strip()
            if nxt == "2":
                print(f"\n  {R}Exiting!...{RST}\n")
                sys.exit()

        elif choice == "2":
            print(f"\n  {R}Exiting tool...{RST}\n")
            sys.exit()

        else:
            print(f"\n  {R}✗  Invalid option!{RST}")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(run())

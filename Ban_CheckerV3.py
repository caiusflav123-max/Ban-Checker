import httpx
import asyncio
import os
import sys
import time
import requests

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/caiusflav123-max/Ban-Checker/main/version.txt"
GITHUB_FILE_URL = "https://raw.githubusercontent.com/caiusflav123-max/Ban-Checker/main/Ban_CheckerV3.py"
LOCAL_VERSION = "1.0.0"


def check_update():
    try:
        latest = requests.get(GITHUB_VERSION_URL, timeout=10).text.strip()

        if latest != LOCAL_VERSION:
            print("\n[UPDATE] May bagong version! Updating...\n")

            new_code = requests.get(GITHUB_FILE_URL, timeout=10).text

            with open("Ban_CheckerV3.py", "w", encoding="utf-8") as f:
                f.write(new_code)

            print("[DONE] Updated na! restarting...\n")

            os.execv(sys.executable, [sys.executable, "Ban_CheckerV3.py"])

    except Exception as e:
        print(f"[!] Update check failed: {e}")

BAN_API_URL = "https://checkton.online/backend"
BAN_API_KEY = "jUWCzg1ZhJFOE3v1HY_skHImy-hrJ9CoLQ-awa1rK9w"

V2L_API_URL = "https://checkton.online/backend/v2l"
V2L_API_KEY = "tKEIiMaaXZiXgBaa-3ytHnSMOWFsG8ZjaiLHJL9t0rs"


BAN_HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": BAN_API_KEY
}

V2L_HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": V2L_API_KEY
}

PROXY = "ax_xtteozpg_session_p7gyfrcg:aeqmrej9lsv9@165.245.185.214:25587"

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
    box_top = f"{M}╔{'═' * 35}╗{RST}"
    box_bot = f"{M}╚{'═' * 35}╝{RST}"
    box_mid = f"{M}║{RST}"
    art = [
        f"     {R}██████╗  █████╗ ███╗   ██╗  {RST}  ",
        f"     {R}██╔══██╗██╔══██╗████╗  ██║  {RST}  ",
        f"     {R}██████╔╝███████║██╔██╗ ██║  {RST}  ",
        f"     {R}██╔══██╗██╔══██║██║╚██╗██║  {RST}  ",
        f"     {R}██████╔╝██║  ██║██║ ╚████║  {RST}  ",
        f"     {R}╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  {RST}  ",
        f"     {Y}         C H E C K          {RST}  ",
    ]
    print()
    print(box_top)
    for line in art:
        print(f"{box_mid}{line}{box_mid}")
    print(box_bot)

def menu():
    w = 35
    top = f"{M}╔{'═' * w}╗{RST}"
    mid = f"{M}╠{'═' * w}╣{RST}"
    bot = f"{M}╚{'═' * w}╝{RST}"
    bar = f"{M}║{RST}"

    def row(txt):
        import re
        clean = re.sub(r'\033\[[0-9;]*m', '', txt)
        pad = w - len(clean)
        print(f"{bar} {txt}{' ' * (pad - 1)}{bar}")

    print(top)
    row(f"{DG}Created By{RST} {C}@Official_Caius1{RST}")
    print(mid)
    row(f"{M}[{RST}{W}1{RST}{M}]{RST} {G}Check Account{RST}")
    row(f"{M}[{RST}{W}2{RST}{M}]{RST} {DR}Exit{RST}")
    print(bot)

def after_menu():
    w = 36
    top = f"{M}╔{'═' * w}╗{RST}"
    mid = f"{M}╠{'═' * w}╣{RST}"
    bot = f"{M}╚{'═' * w}╝{RST}"
    bar = f"{M}║{RST}"

    def row(txt):
        import re
        clean = re.sub(r'\033\[[0-9;]*m', '', txt)
        pad = w - len(clean)
        print(f"{bar} {txt}{' ' * (pad - 1)}{bar}")

    print()
    print(top)
    row(f"{DG}root@veriton:~${RST} {Y}Next Action{RST}")
    print(mid)
    row(f"{M}[{RST}{W}1{RST}{M}]{RST}  {G}Check Another Account{RST}")
    row(f"{M}[{RST}{W}2{RST}{M}]{RST}  {DR}Exit{RST}")
    print(bot)
    print()

def status(icon, msg, color=DG):
    print(f"  {color}{icon}{RST}  {color}{msg}{RST}")

def inp(label):
    return input(f"  {DG}>{RST} {C}{label:<20}{RST} : ").strip()

async def post(client, url, payload, hdrs):
    try:
        r = await client.post(url, json=payload, headers=hdrs, timeout=30)
        try:
            body = r.json()
        except Exception:
            body = {"detail": r.text or f"HTTP {r.status_code}"}
        if not isinstance(body, dict):
            body = {"detail": str(body)}
        body["_status_code"] = r.status_code
        return body
    except Exception as e:
        return {"error": str(e), "_status_code": 0}

def extract_block(data):
    d = data.get("data")
    if isinstance(d, list):
        block = d[0] if d else None
    elif isinstance(d, dict):
        block = d
    else:
        return None
    if not block:
        return None
    if not any(block.get(k) for k in ("id", "reason", "violation_time", "unlock_time")):
        return None
    return block

def show_ban_result(combo, data, v2l_data=None):
    block = extract_block(data)

    # Extract V2L info
    v2l_status = "N/A"
    if v2l_data and v2l_data.get("status") == 0:
        v2l_status = v2l_data.get("data", {}).get("v2l", "N/A")

    print(f"\n  {BOLD}{G}Ban Checker Result{RST}")

    col_w = 14
    def row(k, v, vc=W):
        print(f"  {DG}{k:<{col_w}}{RST} {DG}│{RST} {vc}{v}{RST}")

    row("Account Login", combo)

    if block:
        row("Ban Status",     "=> Account Banned",                R + BOLD)
        row("V2L Status",     v2l_status,                         G if v2l_status == "Enabled" else DR)
        row("Account ID",     block.get('id', 'N/A'),             R)
        row("Ban Reason",     block.get('reason', 'N/A'),         Y)
        row("Violation Time", block.get('violation_time', 'N/A'), Y)
        row("Unlock Time",    block.get('unlock_time', 'N/A'),    C)
    else:
        row("Ban Status",     "=> Account Not Banned",            G + BOLD)
        row("V2L Status",     v2l_status,                         G if v2l_status == "Enabled" else DR)
        row("Account ID",     "N/A",                              DG)
        row("Ban Reason",     "No Reason Data Found!",            DG)
        row("Violation Time", "N/A",                              DG)
        row("Unlock Time",    "N/A",                              DG)

def show_v2l_result(combo, data):
    if data.get("_status_code", 200) not in (200, 201):
        print(f"\n  {R}V2L CHECK FAILED{RST}")
        return

    if data.get("status") != 0:
        print(f"\n  {R}INVALID RESPONSE{RST}")
        return

    d = data.get("data", {})
    if not isinstance(d, dict):
        print(f"\n  {R}V2L CHECK FAILED{RST}")
        return

    roles = d.get("roles", {})

    print(f"\n  {BOLD}{G}V2L Checker Result{RST}")

    col_w = 14
    def row(k, v, vc=W):
        print(f"  {DG}{k:<{col_w}}{RST} {DG}│{RST} {vc}{v}{RST}")

    row("Account Login", combo)
    row("V2L Status",    d.get("v2l", "N/A"),         G if d.get("v2l") == "Enabled" else R)
    row("Bind Info",     d.get("bind_info", "N/A"),   C)
    row("Nickname",      roles.get("nickname", "N/A"), W)
    row("Role ID",       str(roles.get("role_id", "N/A")), DG)
    row("Zone ID",       str(roles.get("zone_id", "N/A")), DG)
    row("Level",         str(roles.get("level", "N/A")),   Y)
    row("Last Login",    d.get("last_login", "N/A"),   DG)
    row("Device Count",  str(d.get("device_count", "N/A")), Y)
    row("TTL",           d.get("ttl", "N/A"),          DR)

def is_login_success(data):
    if data.get("_status_code", 200) not in (200, 201):
        return False
    for key in ("error", "detail"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            return False
    if data.get("data"):
        return True
    if data.get("jwt") or data.get("guid") or data.get("session_id") or data.get("session"):
        return True
    if "status" in data and data.get("status") == 0:
        return True
    return False

def get_error_msg(data):
    raw_err = (
        data.get("detail") or
        data.get("error") or
        data.get("message") or
        (data.get("data") if isinstance(data.get("data"), str) else None) or
        ""
    )
    raw_lower = str(raw_err).lower()
    status_code = data.get("_status_code", 200)

    if "insufficient" in raw_lower and "credit" in raw_lower:
        return "API provider credits exhausted."
    if status_code == 402:
        return "API provider credits exhausted."
    if status_code in (401, 403):
        return "API authorization error."
    if "password" in raw_lower or "incorrect" in raw_lower:
        return "Incorrect password."
    if "not found" in raw_lower or "account not found" in raw_lower:
        return "Account not found."
    if "invalid" in raw_lower and ("account" in raw_lower or "moonton" in raw_lower):
        return "Invalid Moonton account."
    if "timeout" in raw_lower or "timed out" in raw_lower:
        return "Request timed out."
    if "network" in raw_lower or "connect" in raw_lower or "proxy" in raw_lower:
        return "Network/proxy error."
    if raw_err:
        return str(raw_err)
    return "Login failed — please try again later."

async def ban_checker():
    combo = inp("Enter Email & Password")
    if ":" not in combo:
        print(f"\n{R}Invalid combo format! Use email:password{RST}")
        return
    email, password = combo.split(":", 1)

    async with httpx.AsyncClient() as client:

        await loading("Logging in...")
        login_data = await post(client, BAN_API_URL + "/check", {
            "login": email,
            "password": password,
            "proxy": PROXY,
            "type": "login"
        }, BAN_HEADERS)

        if not is_login_success(login_data):
            err = get_error_msg(login_data)
            print(f"\n  {R}✗  Login failed.{RST}")
            print(f"  {DR}→  {err}{RST}")
            print(f"  {DR}→  Raw: {login_data}{RST}")
            return

        status("✓", "Login successful.", G)

        raw = login_data.get("data", {})
        if isinstance(raw, list):
            raw = raw[0] if raw else {}
        auto_guid    = raw.get("guid", "")       if isinstance(raw, dict) else ""
        auto_session = raw.get("session_id", "") if isinstance(raw, dict) else ""
        if not auto_session:
            auto_session = raw.get("session", "") if isinstance(raw, dict) else ""

        guid       = auto_guid
        session_id = auto_session

        print()
        await loading("Getting JWT Token...")
        jwt_data = await post(client, BAN_API_URL + "/getJwt", {
            "guid": guid,
            "session_id": session_id,
            "proxy": PROXY,
        }, BAN_HEADERS)

        jwt   = jwt_data.get("jwt")   or jwt_data.get("data", {}).get("jwt")
        token = jwt_data.get("token") or jwt_data.get("data", {}).get("token")

        if not jwt:
            print(f"\n  {R}✗  JWT generation failed.{RST}")
            print(f"  {DR}→  Raw: {jwt_data}{RST}")
            return

        status("✓", "JWT obtained.", G)

        input(f"  {Y}[ Please Enter if you want to Continue]{RST}")

        await loading("Checking...", duration=0.8)

        v2l_data, ban_data = await asyncio.gather(
            post(client, V2L_API_URL, {
                "guid": guid,
                "session": session_id,
                "type": "and",
            }, V2L_HEADERS),
            post(client, BAN_API_URL + "/getBanInfo", {
                "jwt": jwt,
                "token": token,
                "proxy": PROXY,
            }, BAN_HEADERS)
        )

        show_ban_result(combo, ban_data, v2l_data)

async def v2l_checker():
    guid    = inp("GUID")
    session = inp("SESSION")
    v2l_type = inp("Type (and/ios)").lower() or "and"

    if v2l_type not in ("and", "ios"):
        print(f"\n  {R}Invalid type! Use 'and' or 'ios'{RST}")
        return

    async with httpx.AsyncClient() as client:
        await loading("Checking V2L Status...")
        v2l_data = await post(client, V2L_API_URL, {
            "guid": guid,
            "session": session,
            "type": v2l_type,
        }, V2L_HEADERS)

        show_v2l_result(f"{guid[:12]}...", v2l_data)

async def run():
    while True:
        clear()
        banner()
        menu()
        choice = input(f"{DG}> {RST}{C}Please Select{RST} : ").strip()

        if choice == "1":
            clear()
            banner()
            await ban_checker()
            after_menu()
            nxt = input(f"{DG}>{RST}{C}Select Option{RST} : ").strip()
            if nxt == "2":
                print(f"\n  {R}Exiting...{RST}\n")
                time.sleep(2)
                sys.exit()

        elif choice == "2":
            print(f"\n  {R}Exiting...{RST}\n")
            time.sleep(2)
            sys.exit()

        else:
            print(f"{R}✗ Invalid option!{RST}")
            await asyncio.sleep(3)

if __name__ == "__main__":
    check_update()
    asyncio.run(run())

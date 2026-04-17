import os, time, platform, sys
try:
    from telethon.sync import TelegramClient
    from telethon.tl import types
    from telethon import functions
    from prettytable import PrettyTable
except ImportError:
    os.system("pip install telethon prettytable")
    os.execv(sys.executable, [sys.executable] + sys.argv)

rd  = '\033[00;31m'
gn  = '\033[00;32m'
lgn = '\033[01;32m'
lrd = '\033[01;31m'
cn  = '\033[00;36m'
k   = '\033[90m'
g   = '\033[38;5;130m'
yw  = '\033[01;33m'
rs  = '\033[0m'

def re(text, delay=0.001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def banner():
    re(f"""{g}
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
{rs}""")

METODOS = {
    "1":  ("Spam",               types.InputReportReasonSpam,            ""),
    "2":  ("Pornografía",        types.InputReportReasonPornography,      ""),
    "3":  ("Violencia",          types.InputReportReasonViolence,         ""),
    "4":  ("Abuso Infantil",     types.InputReportReasonChildAbuse,       "Este usuario tiene contenido de abuso infantil"),
    "5":  ("Otro",               types.InputReportReasonOther,            None),
    "6":  ("Derechos de Autor",  types.InputReportReasonCopyright,        "Este usuario viola derechos de autor"),
    "7":  ("Falso/Suplantación", types.InputReportReasonFake,             "Este usuario es falso o suplanta identidad"),
    "8":  ("Geo Irrelevante",    types.InputReportReasonGeoIrrelevant,    "Contenido geográficamente irrelevante"),
    "9":  ("Drogas Ilegales",    types.InputReportReasonIllegalDrugs,     "Este usuario promueve drogas ilegales"),
    "10": ("Datos Personales",   types.InputReportReasonPersonalDetails,  "Este usuario filtra datos personales"),
}

def mostrar_tabla():
    t = PrettyTable([f'{cn}Número{lrd}', f'{cn}Método{lrd}'])
    for k_m, v in METODOS.items():
        t.add_row([f'{lgn}{k_m}{lrd}', f'{gn}{v[0]}{lrd}'])
    print(f'{lrd}')
    print(t)

def main():
    if platform.system() == "Windows":
        try:
            from colorama import init; init()
        except: pass

    clear()
    banner()
    re(f"\n{k}         Reportador de Cuentas\n")
    re(f"{lrd}[{lgn}+{lrd}] {gn}Creado por : {lgn}@DarkZFull{rs}\n\n")
    re(f"{yw}⚠️  Todo está bajo tu responsabilidad{rs}\n\n")

    api_id   = input(f"{lrd}[{lgn}+{lrd}] {gn}API ID    : {g}")
    api_hash = input(f"{lrd}[{lgn}+{lrd}] {gn}API Hash  : {g}")
    phone    = input(f"{lrd}[{lgn}+{lrd}] {gn}Teléfono  : {g}")
    password = input(f"{lrd}[{lgn}+{lrd}] {gn}2FA (vacío si no tienes): {g}").strip() or None

    clear()
    banner()
    mostrar_tabla()

    method = input(f"\n{lrd}[{lgn}?{lrd}] {gn}Elige método : {k}").strip()
    if method not in METODOS:
        print(f"{lrd}[!] Método inválido.{rs}"); return

    objetivo = input(f"{lrd}[{lgn}+{lrd}] {gn}@usuario objetivo : {k}").strip()
    try:
        cantidad = int(input(f"{lrd}[{lgn}+{lrd}] {gn}Cantidad de reportes : {k}").strip())
    except ValueError:
        print(f"{lrd}[!] Cantidad inválida.{rs}"); return

    nombre, razon_cls, mensaje_def = METODOS[method]

    if razon_cls == types.InputReportReasonOther:
        mensaje = input(f"{lrd}[{lgn}+{lrd}] {gn}Mensaje del reporte : {k}").strip()
    else:
        mensaje = mensaje_def

    print(f"\n{lrd}[{lgn}+{lrd}] {gn}Conectando...{rs}")

    try:
        with TelegramClient('session_report', api_id, api_hash) as client:
            client.start(phone, password)

            try:
                entity = client.get_entity(objetivo)
                peer   = client.get_input_entity(entity)
            except Exception as e:
                print(f"{lrd}[!] No se encontró el objetivo: {e}{rs}"); return

            print(f"{lrd}[{lgn}+{lrd}] {gn}Objetivo encontrado: {lgn}{entity.username or objetivo}{rs}")
            print(f"{lrd}[{lgn}+{lrd}] {gn}Iniciando {cantidad} reportes de tipo '{nombre}'...{rs}\n")

            enviados = errores = 0
            for i in range(cantidad):
                try:
                    client(functions.account.ReportPeerRequest(
                        peer=peer, reason=razon_cls(), message=mensaje))
                    enviados += 1
                    print(f"{lrd}[{lgn}+{lrd}] {gn}Reporte enviado : {lgn}{i+1}/{cantidad}{rs}")
                except Exception as e:
                    errores += 1
                    print(f"{lrd}[{rd}!{lrd}] {rd}Error en reporte {i+1}: {e}{rs}")

    except Exception as e:
        print(f"{lrd}[!] Error de conexión: {e}{rs}"); return

    print(f"\n{k}{'━'*40}")
    print(f"{lrd}[{lgn}✓{lrd}] {gn}Completado")
    print(f"{lrd}[{lgn}+{lrd}] {gn}Enviados : {lgn}{enviados}")
    print(f"{lrd}[{rd}!{lrd}] {rd}Errores  : {errores}{rs}")
    print(f"{k}{'━'*40}{rs}\n")

if __name__ == "__main__":
    main()

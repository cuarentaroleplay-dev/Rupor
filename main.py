import os, time, platform, sys

# ── Verificar acceso antes de continuar ───────────────────────
try:
    from auth import solicitar_aprobacion
    solicitar_aprobacion()
except SystemExit:
    sys.exit(1)
except Exception as e:
    print(f"\033[01;31m[!] Error en sistema de auth: {e}\033[0m")
    sys.exit(1)

try:
    from prettytable import PrettyTable
except ImportError:
    os.system("pip install prettytable -q")
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

if platform.system() == "Windows":
    try:
        from colorama import init; init()
    except: pass

clear()
re(f"""{g}
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
{rs}""")

re(f"\n{k}         Reportador de Telegram\n")
re(f"{lrd}[{lgn}+{lrd}] {gn}Creado por : {lgn}@DarkZFull{rs}\n")
re(f"{yw}⚠️  Todo está bajo tu responsabilidad{rs}\n\n")

t = PrettyTable([f'{cn}Número{lrd}', f'{cn}Opción{lrd}'])
t.add_row([f'{lgn}1{lrd}', f'{gn}Reportar Canal{lrd}'])
t.add_row([f'{lgn}2{lrd}', f'{gn}Reportar Cuenta{lrd}'])
t.add_row([f'{lgn}3{lrd}', f'{yw}Reportar Grupo {k}[Próximamente]{lrd}'])
print(f'{lrd}')
print(t)

opcion = input(f"\n{lrd}[{lgn}?{lrd}] {gn}Elige una opción : {cn}").strip()

if opcion == "1":
    os.system("python3 reporter.py")
elif opcion == "2":
    os.system("python3 report.py")
elif opcion == "3":
    print(f"\n{yw}Esta función estará disponible próximamente.\n\n{cn}Creado por @DarkZFull{rs}")
else:
    print(f"\n{lrd}[!] Opción inválida.{rs}")

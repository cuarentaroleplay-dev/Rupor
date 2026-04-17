import os, sys, json, time, socket, platform, subprocess, uuid, requests

# ═══════════════════════════════════════════════════
ADMIN_ID  = "7008799336"
BOT_TOKEN = "8615740285:AAFqQ6p9GFswqs1TWCH7Bu9npgrw8NDhjtk"
AUTH_FILE = os.path.expanduser("~/.ltm_auth.json")
API_URL   = f"https://api.telegram.org/bot{BOT_TOKEN}"
# ═══════════════════════════════════════════════════

def instalar_deps():
    pkgs = ["requests"]
    for p in pkgs:
        try: __import__(p)
        except ImportError:
            os.system(f"{sys.executable} -m pip install {p} -q")

def get_ip():
    try: return requests.get("https://api.ipify.org", timeout=5).text.strip()
    except: return "Desconocida"

def get_bateria():
    try:
        # Linux / Termux
        bat_path = "/sys/class/power_supply/battery/capacity"
        if os.path.exists(bat_path):
            return open(bat_path).read().strip() + "%"
        # Termux API
        result = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return f"{data.get('percentage','?')}% ({data.get('status','?')})"
    except: pass
    return "No disponible"

def get_device():
    sistema  = platform.system()
    maquina  = platform.machine()
    nodo     = platform.node()
    version  = platform.version()[:40]
    return f"{sistema} {maquina} | {nodo} | {version}"

def get_uid():
    """ID único del dispositivo para no pedir auth cada vez"""
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0,8*6,8)][::-1])
        return mac
    except: return str(uuid.uuid4())[:16]

def enviar_mensaje(chat_id, texto, reply_markup=None):
    data = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        r = requests.post(f"{API_URL}/sendMessage", json=data, timeout=10)
        return r.json()
    except: return {}

def get_updates(offset=None):
    params = {"timeout": 20, "allowed_updates": ["callback_query"]}
    if offset: params["offset"] = offset
    try:
        r = requests.get(f"{API_URL}/getUpdates", params=params, timeout=25)
        return r.json().get("result", [])
    except: return []

def answer_callback(callback_id, texto=""):
    try:
        requests.post(f"{API_URL}/answerCallbackQuery",
                      json={"callback_query_id": callback_id, "text": texto}, timeout=5)
    except: pass

def cargar_auth():
    if not os.path.exists(AUTH_FILE): return {}
    try: return json.load(open(AUTH_FILE))
    except: return {}

def guardar_auth(data):
    json.dump(data, open(AUTH_FILE, "w"))

def solicitar_aprobacion():
    instalar_deps()

    uid      = get_uid()
    auth     = cargar_auth()

    # Ya fue aprobado antes en este dispositivo
    if auth.get(uid) == "aprobado":
        return True

    # Ya fue rechazado
    if auth.get(uid) == "rechazado":
        print("\033[01;31m[✗] Acceso denegado por el administrador.\033[0m")
        sys.exit(1)

    ip       = get_ip()
    device   = get_device()
    bateria  = get_bateria()

    mensaje = (
        "🔐 *Solicitud de acceso al script*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Dispositivo:* `{device}`\n"
        f"🌐 *IP:* `{ip}`\n"
        f"🔋 *Batería:* `{bateria}`\n"
        f"🔑 *UID:* `{uid}`\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "¿Le das permiso para usar el script?"
    )

    teclado = {
        "inline_keyboard": [[
            {"text": "✅ Aprobar",  "callback_data": f"aprobar_{uid}"},
            {"text": "❌ Rechazar", "callback_data": f"rechazar_{uid}"},
        ]]
    }

    res = enviar_mensaje(ADMIN_ID, mensaje, reply_markup=teclado)
    msg_id = res.get("result", {}).get("message_id")

    print("\033[01;33m[⏳] Esperando aprobación del administrador...\033[0m")

    offset = None
    tiempo = 0
    timeout_max = 300  # 5 minutos

    while tiempo < timeout_max:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            cb = update.get("callback_query")
            if not cb: continue
            data = cb.get("data", "")
            cb_id = cb["id"]

            if data == f"aprobar_{uid}":
                answer_callback(cb_id, "✅ Aprobado")
                # Editar mensaje
                try:
                    requests.post(f"{API_URL}/editMessageText", json={
                        "chat_id": ADMIN_ID,
                        "message_id": msg_id,
                        "text": f"✅ *Acceso aprobado*\n🔑 UID: `{uid}`\n🌐 IP: `{ip}`",
                        "parse_mode": "Markdown"
                    }, timeout=5)
                except: pass
                auth[uid] = "aprobado"
                guardar_auth(auth)
                print("\033[01;32m[✓] Acceso aprobado por el administrador.\033[0m")
                time.sleep(1)
                return True

            elif data == f"rechazar_{uid}":
                answer_callback(cb_id, "❌ Rechazado")
                try:
                    requests.post(f"{API_URL}/editMessageText", json={
                        "chat_id": ADMIN_ID,
                        "message_id": msg_id,
                        "text": f"❌ *Acceso rechazado*\n🔑 UID: `{uid}`\n🌐 IP: `{ip}`",
                        "parse_mode": "Markdown"
                    }, timeout=5)
                except: pass
                auth[uid] = "rechazado"
                guardar_auth(auth)
                print("\033[01;31m[✗] Acceso denegado por el administrador.\033[0m")
                sys.exit(1)

        tiempo += 20

    print("\033[01;31m[✗] Tiempo de espera agotado. Intenta de nuevo.\033[0m")
    sys.exit(1)

if __name__ == "__main__":
    solicitar_aprobacion()
    print("Acceso concedido.")

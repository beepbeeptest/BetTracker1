import os, json, hmac, hashlib, time, urllib.parse
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from db import Database

app = FastAPI()
db = Database("bets.db")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Telegram init_data валидация ──
def validate_init_data(init_data: str) -> Optional[dict]:
    """Проверяет подпись Telegram и возвращает данные пользователя."""
    if not BOT_TOKEN or not init_data:
        return None
    try:
        parsed = dict(urllib.parse.parse_qsl(init_data, strict_parsing=False))
        received_hash = parsed.pop("hash", None)
        if not received_hash:
            return None
        check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(computed, received_hash):
            return None
        # Проверяем что данные не старше 24 часов
        auth_date = int(parsed.get("auth_date", 0))
        if time.time() - auth_date > 86400:
            return None
        user_data = json.loads(parsed.get("user", "{}"))
        return user_data
    except Exception:
        return None

def get_user_id(x_init_data: str = Header(None)) -> int:
    """Извлекает user_id из заголовка X-Init-Data."""
    if not x_init_data or x_init_data.strip() == "":
        # В режиме разработки / десктоп — используем тестового пользователя
        return 0
    user = validate_init_data(x_init_data)
    if not user:
        raise HTTPException(403, "Невалидная подпись Telegram")
    return int(user["id"])


# ── Модели ──
class Bet(BaseModel):
    id: str
    date: str
    book: str = ""
    sport: str = ""
    event: str
    market: str = ""
    pick: str = ""
    odds: float
    stake: float
    result: str = "pending"

class Settings(BaseModel):
    unit: float = 1
    cur: str = "у.е."
    balance: Optional[float] = None


# ── Эндпоинты ставок ──
@app.get("/api/bets")
def get_bets(x_init_data: str = Header(None)):
    uid = get_user_id(x_init_data)
    return db.get_bets(uid)

@app.post("/api/bets")
def add_bet(bet: Bet, x_init_data: str = Header(None)):
    uid = get_user_id(x_init_data)
    db.save_bet(uid, bet.dict())
    return {"ok": True}

@app.put("/api/bets/{bet_id}")
def update_bet(bet_id: str, bet: Bet, x_init_data: str = Header(None)):
    uid = get_user_id(x_init_data)
    ok = db.update_bet(uid, bet_id, bet.dict())
    if not ok:
        raise HTTPException(404, "Ставка не найдена")
    return {"ok": True}

@app.delete("/api/bets/{bet_id}")
def delete_bet(bet_id: str, x_init_data: str = Header(None)):
    uid = get_user_id(x_init_data)
    ok = db.delete_bet(uid, bet_id)
    if not ok:
        raise HTTPException(404, "Ставка не найдена")
    return {"ok": True}


# ── Эндпоинты настроек ──
@app.get("/api/settings")
def get_settings(x_init_data: str = Header(None)):
    uid = get_user_id(x_init_data)
    return db.get_settings(uid)

@app.post("/api/settings")
def save_settings(settings: Settings, x_init_data: str = Header(None)):
    uid = get_user_id(x_init_data)
    db.save_settings(uid, settings.dict())
    return {"ok": True}


# ── Отдаём фронтенд ──
app.mount("/", StaticFiles(directory="static", html=True), name="static")

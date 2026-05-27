from pydantic import BaseModel, Field, model_validator, field_validator, EmailStr
from typing import Optional, Union, Any, Literal
import datetime
from datetime import date, datetime


# ---------------------------------------------- МОДЕЛИ ПРОФИЛЯ ----------------------------------------------






class UserAuthSchema(BaseModel):
    # Разрешены только английские буквы (регистр не важен), цифры и "_"
    # Длина от 3 до 20 символов
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    
    # В пароле разрешаем любые символы, так как bcrypt защитит от SQLi
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=64,
    )

    mail: EmailStr | None = Field()

    phone: str | None = Field(
        pattern=r"^(?:\+7|7|8)\d{10}$",
    )












class StandartPerfs(BaseModel):
    games: int #кол-во игр
    prog: int # прогресс
    rating: int # рейтинг
    rd: int # рейтинговое отклонение
    prov: Optional[bool] = None # признак нестабильного рейтинга
    rank: Optional[int]  = None # глобальный рейтинг только для недавних игроков

class StormPerfs(BaseModel):
    runs: int
    score: int

class PlayTime(BaseModel):
    total: int
    tv: int
    human: Optional[int] = None


class Count(BaseModel):
    all: int #кол-во всех матчей
    bookmark: int
    draw: int
    loss: int
    win: int
    import_: int = Field(alias="import")
    playing: int
    rated: int
    me: int 
    ai: Optional[int] = None
    drawH: Optional[int] = None
    lossH: Optional[int] = None
    winH: Optional[int] = None


class Profile(BaseModel):
    bio: Optional[str] = None
    cfcRating: Optional[int] = None
    dsbRating: Optional[int] = None
    ecfRating: Optional[int] = None
    fideRating: Optional[int] = None
    flag: Optional[str] = None
    location: Optional[str] = None
    rcfRating: Optional[int] = None
    realName: Optional[str] = None
    uscRating: Optional[int] = None

class TwitchInfo(BaseModel):
    channel: Optional[str] = None

class YouTubeInfo(BaseModel):
    channel: Optional[str] = None

class Streamer(BaseModel):
    twitch: Optional[TwitchInfo] = None
    youtube: Optional[YouTubeInfo] = None


class PlayerProfile(BaseModel):
    id: str
    username: str
    url: str # ссылка на профиль игрока
    perfs:  dict[str, Union[StormPerfs, StandartPerfs]]  | None # статистика в каждом отдельном режиме
    createdAt: Optional[int] = None # дата создания профиля
    disabled: Optional[bool] = None # только если акканут юзера закрыт
    fideId: Optional[int] = None 
    flair: Optional[str] = None
    playing: Optional[str] = None
    playTime: PlayTime | None
    profile: Profile | None
    seenAt: Optional[int] = None
    streamer: Optional[Streamer] = None
    tosViolation: Optional[bool] = None
    verified: Optional[bool]= None
    count: Count | None = None


# ---------------------------------------------- РЕЙТИНГ ----------------------------------------------

class RatingPoint(BaseModel):
    year: int
    month: int
    day: int
    rating: int

    @model_validator(mode='before')
    @classmethod
    def validate_date(cls, data: Any) -> dict:
        if isinstance(data, list):
            if len(data) != 4:
                raise ValueError(f"Список содержит {len(data)}")
            return {
                'year': data[0],
                'month': data[1],
                'day': data[2],
                'rating': data[3],
            }
        return data

class RatingHistory(BaseModel):
    name: str
    points: list[RatingPoint]




class Count(BaseModel):
    all: int
    rated: int
    draw: int
    loss: int
    win: int
    bookmark: int
    playing: int
    import_: int = Field(alias="import")   # ключ "import" – используем alias
    me: int

# ---------------------------------------------- Даныые об игре ----------------------------------------------





class LightUser(BaseModel):
    """Минимальная информация о пользователе (оппоненте)."""
    name: str
    id: str
    # некоторые поля могут отсутствовать, поэтому extra=allow
    class Config:
        extra = "allow"

class Player(BaseModel):
    """Игрок (белый или чёрный) в партии."""
    user: Optional[LightUser] = None   # может быть null (например, аноним)
    rating: Optional[int] = None       # рейтинг перед партией
    aiLevel: Optional[int] = None      # если соперник – бот

class Players(BaseModel):
    white: Player
    black: Player

class Opening(BaseModel):
    """Дебют (если данные доступны)."""
    eco: str          # код дебюта, например "B01"
    name: str         # название, например "Scandinavian Defense"

# --- Основная модель игры ---

class GameJson(BaseModel):
    # Служебные поля (будут вычислены)
    id: str
    username: Optional[str] = None   # будет заполнен позже (имя анализируемого игрока)
    rated: bool
    color: Optional[str] = None      # "white" / "black"
    variant: str
    speed: str
    perf: str
    game_createdAt: datetime         # преобразуем из timestamp
    status: str
    win: str                         # строка: "win", "loss", "draw" и т.п.
    oponent: dict                    # json-объект с информацией о сопернике
    opening: str                     # строка с полным описанием дебюта
    debut: str                       # версия opening, можешь хранить то же самое или eco
    source: str                      # пока можно заполнять пустой строкой
    moves: Optional[str] = None
    analysis: Optional[Union[dict, list[dict]]] = None
    clock: Optional[dict] = None
    division: Optional[dict] = None
    timestamp: datetime              # дублирует game_createdAt, можно просто копию

    class Config:
        extra = "allow"

    @field_validator("game_createdAt", mode="before")
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, int):
            return datetime.utcfromtimestamp(v / 1000.0)
        if isinstance(v, datetime):
            return v
        raise ValueError(f"Неподдерживаемый тип для createdAt: {type(v)}")

    @model_validator(mode="before")
    @classmethod
    def extract_fields(cls, data: Any) -> dict:
        """
        На входе — сырой словарь из Lichess JSON.
        Вычисляем недостающие поля для плоской структуры твоей таблицы.
        """
        if not isinstance(data, dict):
            return data

        # Игроки
        players = data.get("players", {})
        white = players.get("white", {})
        black = players.get("black", {})

        # Достаём юзернеймы/ID
        white_user = white.get("user") or {}
        black_user = black.get("user") or {}
        white_name = white_user.get("name") if white_user else None
        black_name = black_user.get("name") if black_user else None
        white_id = white_user.get("id") if white_user else None
        black_id = black_user.get("id") if black_user else None

        # Пытаемся определить, играем ли мы белыми/чёрными
        # (мы ещё не знаем username анализируемого игрока, он будет передан позже)
        # Поэтому пока можно оставить color = None, он будет переопределён в сервисе.
        # Но мы можем хотя бы взять данные для opponent
        winner = data.get("winner")

        # Формируем opponent: тут будет JSON с именем, id, рейтингом
        # Пока кладём туда данные соперника – позже в сервисе можно уточнить.
        oponent = {
            "name": None,
            "id": None,
            "rating": None,
            "color": None
        }

        # Открытие
        opening = data.get("opening", {})
        opening_name = opening.get("name") if opening else None
        opening_eco = opening.get("eco") if opening else None
        # В твоей таблице opening - строка, debut - тоже строка.
        # Я предлагаю в opening записать название, а в debut — eco-код.
        opening_str = opening_name if opening_name else ""
        debut_str = opening_eco if opening_eco else ""

        # source – пока не знаю, что ты хотел хранить. Оставлю пустым.
        source_str = ""

        # win – преобразуем winner в понятный результат
        # Для этого позже в сервисе мы уже знаем, за кого мы играли.
        # Пока оставим пустым, сервис заполнит.
        win = ""

        # Дата
        created_at = data.get("createdAt")

        return {
            **data,
            "username": data.get("username"),  # пока None
            "color": None,
            "win": win,
            "oponent": oponent,
            "opening": opening_str,
            "debut": debut_str,
            "source": source_str,
            "game_createdAt": created_at,
            "timestamp": created_at,    # будет то же, что и game_createdAt после валидации
            "moves": data.get("moves"),
            "analysis": data.get("analysis"),
            "clock": data.get("clock"),
            "division": data.get("division"),
        }



# ---------------------------------------------- Статистика ----------------------------------------------


class OpeningStats(BaseModel):
    """Статистика по одному дебюту."""
    eco: str = Field(..., description="Код дебюта, например B01")
    name: str = Field(..., description="Название дебюта, например Scandinavian Defense")
    total: int = Field(..., description="Общее количество партий этим дебютом")
    wins: int = Field(..., description="Победы (белыми и чёрными суммарно)")
    draws: int = Field(..., description="Ничьи")
    losses: int = Field(..., description="Поражения")
    winrate: float = Field(..., description="Процент побед (0..100)")


class BestWin(BaseModel):
    """Самая яркая победа (над более сильным соперником)."""
    date: date
    opponent: str
    opponent_rating: int
    player_rating: int
    rating_diff: int = Field(..., description="Разница (opponent - player), >0 значит соперник сильнее")
    opening_name: str
    opening_eco: str
    game_id: str


class ColorStats(BaseModel):
    """Статистика отдельно за белых или чёрных."""
    total: int
    wins: int
    draws: int
    losses: int
    winrate: float = Field(..., description="Процент побед (0..100)")


class PlayerStats(BaseModel):
    """Полная агрегированная статистика игрока."""

    username: str

    # Общая
    total_games: int = Field(..., description="Всего партий")
    total_wins: int
    total_draws: int
    total_losses: int
    overall_winrate: float = Field(..., description="Общий процент побед (0..100)")

    # По цветам
    white: ColorStats
    black: ColorStats

    # Топ-10 дебютов (по количеству партий)
    top_openings: list[OpeningStats] = Field(default_factory=list)

    # Активность по дням (для календаря)
    # ключ – строка даты "YYYY-MM-DD", значение – количество партий
    activity_heatmap: dict[str, int] = Field(default_factory=dict)

    # Распределение по дням недели (0=пн, 6=вс)
    week_distribution: dict[int, int] = Field(default_factory=dict)

    # Распределение по часам суток (0-23)
    hour_distribution: dict[int, int] = Field(default_factory=dict)

    # Топ-3 лучших побед
    best_wins: list[BestWin] = Field(default_factory=list)

    # Когда статистика была рассчитана (timestamp сервера)
    last_updated: Optional[int] = None


# ---------------------------------------------- Параметры запроса ----------------------------------------------

class GamesRequestParams(BaseModel):
    max: int = Field(default=20, ge=1, le=500, description="Количество партий (макс. 500)")
    perfType: Optional[str] = Field(
        default=None,
        description="Фильтр по типу: bullet, blitz, rapid, classical, correspondence, chess960, etc."
    )
    opening: Optional[bool] = Field(
        default=True,
        description="Включить информацию о дебюте в ответ"
    )
    # since: Optional[int]   # timestamp для инкрементальной загрузки
    until: Optional[int] = None
    sort: Literal["dateAsc", "dateDesc"] = "dateDesc"
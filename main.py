# ============================================================
# CandyFlood — FINAL KIVY BUILD
# Cross-platform: Windows / Android (with Buildozer)
# ============================================================

# ============================================================
# Candy.flood
# KIVY CROSS-PLATFORM VIRTUAL CASINO
#
# ПК:
#   python main.py
#
# Android:
#   проект можно собрать через Buildozer
#
# ============================================================

import json
import math
import os
import random
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle, Triangle
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import (
    Screen,
    ScreenManager,
    SlideTransition,
)
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


# ============================================================
# НАСТРОЙКИ
# ============================================================

APP_NAME = "Candy.flood"

START_BALANCE = 1000
DAILY_BONUS_BASE = 100
DAILY_BONUS_STEP = 50
DAILY_BONUS_MAX = 1000
DAY_SECONDS = 86400

# Случайные множители для ставок.
# Чем выше множитель, тем ниже его вес выпадения.
RANDOM_MULTIPLIERS = [
    (0.5, 1),
    (1.0, 1),
    (1.5, 1),
    (2.0, 1),
    (3.0, 1),
    (5.0, 1),
    (8.0, 1),
    (10.0, 1),
    (15.0, 1),
    (20.0, 1),
]

def random_multiplier():
    values = [value for value, weight in RANDOM_MULTIPLIERS]
    weights = [weight for value, weight in RANDOM_MULTIPLIERS]
    return random.choices(values, weights=weights, k=1)[0]

BG = "#090A12"
SIDEBAR = "#10111B"
CARD = "#151725"
CARD2 = "#1B1D2D"
CARD_HOVER = "#24283D"

PURPLE = "#7547FF"
PURPLE_HOVER = "#906FFF"

GOLD = "#FFD34E"
GREEN = "#2BD889"
RED = "#FF5570"
BLUE = "#4BA3FF"
CYAN = "#43D9FF"

WHITE = "#FFFFFF"
TEXT = "#DFE1ED"
GRAY = "#85899D"
DARK = "#05060B"

RED_ROULETTE = "#E94560"
BLACK_ROULETTE = "#171922"
GREEN_ROULETTE = "#18A86B"


# ============================================================
# УТИЛИТЫ ЦВЕТОВ
# ============================================================

def hex_color(value):
    value = value.lstrip("#")

    if len(value) == 6:
        return tuple(
            int(value[i:i + 2], 16) / 255
            for i in (0, 2, 4)
        ) + (1,)

    return (1, 1, 1, 1)



def _wheel_scroll(scroll, touch):
    if not scroll.collide_point(*touch.pos):
        return False
    if touch.button == "scrollup":
        scroll.scroll_y = min(1.0, scroll.scroll_y + 0.12)
        return True
    if touch.button == "scrolldown":
        scroll.scroll_y = max(0.0, scroll.scroll_y - 0.12)
        return True
    return False

# ============================================================
# ПЕРСОНАЖИ
# ============================================================

BET_PARAMETERS = [
    "Душа",
    "Неприкосновенность",
    "Сердце",
    "Честь",
    "Решимость",
    "Тайна",
    "Характер",
    "Удача",
    "Репутация",
    "Влияние",
    "Смелость",
    "Доверие",
]


DEFAULT_CHARACTERS = {

    "Дерзкий": {
        "Душа": 72,
        "Неприкосновенность": 100,
        "Сердце": 65,
        "Честь": 81,
        "Решимость": 95,
        "Тайна": 60,
        "Характер": 98,
        "Удача": 70,
        "Репутация": 88,
        "Влияние": 91,
        "Смелость": 97,
        "Доверие": 55,
    },

    "Наташа": {
        "Душа": 91,
        "Неприкосновенность": 100,
        "Сердце": 96,
        "Честь": 90,
        "Решимость": 76,
        "Тайна": 72,
        "Характер": 84,
        "Удача": 68,
        "Репутация": 94,
        "Влияние": 73,
        "Смелость": 71,
        "Доверие": 89,
    },

    "Дима": {
        "Душа": 78,
        "Неприкосновенность": 100,
        "Сердце": 83,
        "Честь": 74,
        "Решимость": 88,
        "Тайна": 67,
        "Характер": 79,
        "Удача": 82,
        "Репутация": 76,
        "Влияние": 80,
        "Смелость": 85,
        "Доверие": 72,
    },

    "Ксюша": {
        "Душа": 87,
        "Неприкосновенность": 100,
        "Сердце": 92,
        "Честь": 86,
        "Решимость": 79,
        "Тайна": 75,
        "Характер": 81,
        "Удача": 69,
        "Репутация": 90,
        "Влияние": 78,
        "Смелость": 74,
        "Доверие": 85,
    },

    "Полина": {
        "Душа": 70,
        "Неприкосновенность": 100,
        "Сердце": 77,
        "Честь": 68,
        "Решимость": 93,
        "Тайна": 88,
        "Характер": 90,
        "Удача": 75,
        "Репутация": 71,
        "Влияние": 86,
        "Смелость": 94,
        "Доверие": 64,
    },

    "Саламандра": {
        "Душа": 82,
        "Неприкосновенность": 100,
        "Сердце": 74,
        "Честь": 80,
        "Решимость": 91,
        "Тайна": 93,
        "Характер": 87,
        "Удача": 79,
        "Репутация": 83,
        "Влияние": 89,
        "Смелость": 92,
        "Доверие": 70,
    },

    "Даня": {
        "Душа": 76,
        "Неприкосновенность": 100,
        "Сердце": 71,
        "Честь": 77,
        "Решимость": 80,
        "Тайна": 64,
        "Характер": 75,
        "Удача": 86,
        "Репутация": 78,
        "Влияние": 62,
        "Смелость": 73,
        "Доверие": 81,
    },

    "Алёна": {
        "Душа": 89,
        "Неприкосновенность": 100,
        "Сердце": 88,
        "Честь": 92,
        "Решимость": 72,
        "Тайна": 79,
        "Характер": 83,
        "Удача": 74,
        "Репутация": 96,
        "Влияние": 80,
        "Смелость": 69,
        "Доверие": 91,
    },

    "Саша": {
        "Душа": 73,
        "Неприкосновенность": 100,
        "Сердце": 79,
        "Честь": 84,
        "Решимость": 86,
        "Тайна": 71,
        "Характер": 78,
        "Удача": 81,
        "Репутация": 82,
        "Влияние": 70,
        "Смелость": 88,
        "Доверие": 79,
    },

    "Мила": {
        "Душа": 94,
        "Неприкосновенность": 100,
        "Сердце": 90,
        "Честь": 87,
        "Решимость": 75,
        "Тайна": 84,
        "Характер": 80,
        "Удача": 91,
        "Репутация": 93,
        "Влияние": 76,
        "Смелость": 72,
        "Доверие": 95,
    },

    "Милфа": {
        "Душа": 68,
        "Неприкосновенность": 100,
        "Сердце": 61,
        "Честь": 73,
        "Решимость": 99,
        "Тайна": 97,
        "Характер": 95,
        "Удача": 89,
        "Репутация": 98,
        "Влияние": 100,
        "Смелость": 96,
        "Доверие": 58,
    },
}


# ============================================================
# ДОПОЛНИТЕЛЬНЫЕ ПЕРСОНАЖИ
# ============================================================

ALL_CHARACTER_NAMES = [

    "Полина",
    "Ксюша",
    "Рита",
    "Алёна",
    "Варя",
    "Анжела",
    "Алиса",
    "Амелия",
    "Наташа",
    "Лера",
    "Милкис",
    "Саламандра",
    "Женя",
    "Соня",
    "Близняшки",

    # ИСПРАВЛЕНО
    "Дакука",

    "Настя",
    "Диана",

    "Сестра Димы (Алина)",
    "Мама Димы (Не родная)",
    "Мама Димы (Родная)",
    "Мама Дани",
    "Мама Милкис",
    "Мама Алёны",
    "Бабушка Димы",

    "Оливия Алексеевна",
    "Александра Юрьевна",
    "Нателла Павлиновна",
    "Рашида Жавдатовна",
    "Софья Андреевна",

    "Малерчук",
    "Кранченко",
    "Дерзкий",
    "Даня",
    "Дима",

    # РОМА/ОМП — ОДИН ПЕРСОНАЖ
    "Рома/ОМП",

    "Герман",
    "Орех",
    "Платон",
    "Саша",
    "Камран",
    "Филл",
    "Серёжа",
    "Волков",
    "Вова",
    "Вадчик",
    "Денис",
    "Дед Инсайд",
    "Сэм",

    "Папа Димы (родной)",
    "Папа Димы (не родной)",
    "Географ (Леопольд Арнольдович)",
    "Алексей Евгеньевич",
    "Лев Анатольевич",
    "Охранник",
    "Физрук",
    "Строитель",
    "Руслан Гладенко",
    "Максим Геннадьевич",

    "Отец Саламандры",
    "Отец Ксюши",
    "Отец Леры",
    "Отец Полины",
    "Отец Дерзкого",
    "Отец Дани",
    "Отец Милкис",

    "Китаец (Мафиози)",
    "Тёма",
    "Глэм",
    "Ника",
]


def create_default_stats():

    return {
        "Душа": random.randint(65, 95),
        "Неприкосновенность": 100,
        "Сердце": random.randint(60, 95),
        "Честь": random.randint(60, 95),
        "Решимость": random.randint(65, 98),
        "Тайна": random.randint(55, 95),
        "Характер": random.randint(65, 98),
        "Удача": random.randint(60, 95),
        "Репутация": random.randint(60, 98),
        "Влияние": random.randint(55, 95),
        "Смелость": random.randint(60, 98),
        "Доверие": random.randint(55, 95),
    }


for character_name in ALL_CHARACTER_NAMES:

    if character_name not in DEFAULT_CHARACTERS:
        DEFAULT_CHARACTERS[character_name] = create_default_stats()


# ============================================================
# СОХРАНЕНИЕ
# ============================================================

def default_data():

    return {
        "balance": START_BALANCE,
        "bonus_time": 0,
        "bonus_streak": 0,
        "bonus_last_date": "",
        "characters": {
            name: stats.copy()
            for name, stats in DEFAULT_CHARACTERS.items()
        },
    }


def get_save_path():

    app = App.get_running_app()

    if app:
        return os.path.join(
            app.user_data_dir,
            "candy_flood_save.json"
        )

    return "candy_flood_save.json"


def load_data():

    path = get_save_path()

    if not os.path.exists(path):
        return default_data()

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            saved = json.load(file)

        base = default_data()

        base["balance"] = saved.get(
            "balance",
            START_BALANCE
        )

        base["bonus_time"] = saved.get(
            "bonus_time",
            0
        )

        base["bonus_streak"] = int(saved.get(
            "bonus_streak",
            0
        ))

        base["bonus_last_date"] = saved.get(
            "bonus_last_date",
            ""
        )

        saved_chars = saved.get(
            "characters",
            {}
        )

        for name in base["characters"]:

            if name in saved_chars:

                for stat in base["characters"][name]:

                    if stat in saved_chars[name]:

                        try:

                            value = int(
                                saved_chars[name][stat]
                            )

                            base["characters"][name][stat] = max(
                                0,
                                min(
                                    100,
                                    value
                                )
                            )

                        except Exception:
                            pass

        return base

    except Exception:

        return default_data()


# ============================================================
# UI КОМПОНЕНТЫ
# ============================================================

class RoundedPanel(BoxLayout):

    def __init__(
        self,
        bg_color=CARD,
        radius=14,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.bg_color = hex_color(bg_color)
        self.radius = radius

        with self.canvas.before:

            Color(
                *self.bg_color
            )

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[
                    dp(radius)
                ]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(
        self,
        *args
    ):

        self.rect.pos = self.pos
        self.rect.size = self.size


class CandyButton(Button):

    def __init__(
        self,
        bg_color=PURPLE,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.background_normal = ""
        self.background_down = ""
        self.background_color = hex_color(
            bg_color
        )

        self.color = hex_color(
            WHITE
        )

        self.font_size = dp(14)

        self.bold = True


class StatCard(RoundedPanel):

    def __init__(
        self,
        title,
        value,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(85),
            padding=dp(10),
            spacing=dp(3),
            bg_color=CARD2,
            **kwargs
        )

        title_label = Label(
            text=title,
            color=hex_color(GRAY),
            font_size=dp(10),
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle"
        )

        title_label.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                (obj.width, None)
            )
        )

        self.add_widget(title_label)

        self.value_label = Label(
            text=str(value),
            color=hex_color(WHITE),
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle"
        )

        self.value_label.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                (obj.width, None)
            )
        )

        self.add_widget(self.value_label)


# ============================================================
# ОСНОВНОЙ SCREEN
# ============================================================

class BaseScreen(Screen):

    title = StringProperty("")

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.background_color = hex_color(BG)

        self.main = BoxLayout(
            orientation="vertical"
        )

        self.add_widget(
            self.main
        )

    def header(
        self,
        title,
        subtitle=None
    ):

        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(85),
            padding=[
                dp(20),
                dp(8),
                dp(20),
                dp(5)
            ],
        )

        title_label = Label(
            text=title,
            color=hex_color(WHITE),
            font_size=dp(25),
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(42),
        )
        box.add_widget(title_label)

        if subtitle:

            subtitle_label = Label(
                text=subtitle,
                color=hex_color(GRAY),
                font_size=dp(11),
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(25),
            )

            subtitle_label.bind(
                size=lambda obj, value:
                setattr(
                    obj,
                    "text_size",
                    (obj.width, None)
                )
            )

            box.add_widget(subtitle_label)

        return box


# ============================================================
# ГЛАВНЫЙ ЭКРАН
# ============================================================

class HomeScreen(BaseScreen):

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="home",
            **kwargs
        )

        self.casino = casino

        self.main.add_widget(
            self.header(
                "Главная"
            )
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter(
                "height"
            )
        )

        welcome = RoundedPanel(
            orientation="vertical",
            size_hint_y=None,
            height=dp(135),
            padding=dp(20),
            spacing=dp(5),
        )

        welcome.add_widget(
            Label(
                text="Добро пожаловать [OK]",
                color=hex_color(WHITE),
                font_size=dp(24),
                bold=True,
                halign="left",
                size_hint_y=None,
                height=dp(40),
            )
        )

        welcome.add_widget(
            Label(
                text=(
                    "Candy.flood — "
                    "игровая комната с виртуальными евро."
                ),
                color=hex_color(GRAY),
                font_size=dp(12),
                halign="left",
            )
        )

        content.add_widget(
            welcome
        )

        stats = GridLayout(
            cols=3,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(90)
        )

        self.balance_stat = StatCard(
            "Виртуальный баланс",
            f"€ {casino.balance:,}"
        )

        stats.add_widget(
            self.balance_stat
        )

        stats.add_widget(
            StatCard(
                "Персонажей",
                str(len(casino.characters))
            )
        )

        stats.add_widget(
            StatCard(
                "Игровых режимов",
                "6"
            )
        )

        content.add_widget(
            stats
        )

        content.add_widget(
            Label(
                text="Быстрый запуск",
                color=hex_color(WHITE),
                font_size=dp(18),
                bold=True,
                size_hint_y=None,
                height=dp(35),
                halign="left",
            )
        )

        quick = GridLayout(
            cols=4,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(100)
        )

        for text, page in [
            ("=)\nСлоты", "slots"),
            (";)\nРулетка", "roulette"),
            (":D\nБлэкджек", "blackjack"),
            ("<3\nСтавки", "bets"),
        ]:

            button = CandyButton(
                text=text
            )

            button.bind(
                on_release=lambda btn, p=page:
                casino.goto(p)
            )

            quick.add_widget(
                button
            )

        content.add_widget(
            quick
        )

        scroll.add_widget(
            content
        )

        self.main.add_widget(
            scroll
        )

    def refresh(self):

        self.balance_stat.value_label.text = (
            f"€ {self.casino.balance:,}"
        )


# ============================================================
# СЛОТЫ
# ============================================================


def _animate_scale(widget, start=1.0, end=1.12, duration=0.18):
    steps = 8
    interval = duration / steps
    state = {"i": 0}
    def tick(_dt):
        state["i"] += 1
        t = state["i"] / steps
        if t <= 0.5:
            scale = start + (end - start) * (t * 2)
        else:
            scale = end + (start - end) * ((t - 0.5) * 2)
        widget.font_size = max(dp(10), widget.font_size * scale / max(start, 0.001))
        if state["i"] >= steps:
            return False
        return True
    Clock.schedule_interval(tick, interval)

class SlotsScreen(BaseScreen):

    # Эмоции вместо emoji: ASCII гарантированно отображается в Kivy/Roboto.
    symbols = [
        ":)", ":D", ";)", ":P", ":O", "XD", "<3", ":|",
        ">:(", ":'(", "^_^", "-_-", "O_O", "8)", "B)",
        ":*", ":/", ":-)", ":-D", ":-P", ":-O", "<33", ":3"
    ]

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="slots",
            **kwargs
        )

        self.casino = casino
        self.running = False
        self.step = 0

        self.main.add_widget(
            self.header(
                "=) Слоты",
                "Соберите одинаковые символы и получите выигрыш."
            )
        )

        scroll = ScrollView()

        card = RoundedPanel(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None,
            height=dp(500)
        )

        self.reels_box = BoxLayout(
            size_hint_y=None,
            height=dp(160),
            spacing=dp(10)
        )

        self.reel_labels = []

        for _ in range(3):

            label = Label(
                text="?",
                color=hex_color(DARK),
                font_size=dp(45),
                bold=True,
                size_hint_x=1,
            )

            with label.canvas.before:

                Color(
                    *hex_color(WHITE)
                )

                label.rect = RoundedRectangle(
                    pos=label.pos,
                    size=label.size,
                    radius=[dp(12)]
                )

            label.bind(
                pos=lambda obj, val:
                self.update_rect(obj),
                size=lambda obj, val:
                self.update_rect(obj),
            )

            self.reel_labels.append(
                label
            )

            self.reels_box.add_widget(
                label
            )

        card.add_widget(
            self.reels_box
        )

        self.result = Label(
            text="Сделайте ставку",
            color=hex_color(GRAY),
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )

        card.add_widget(
            self.result
        )

        self.bet = TextInput(
            text="25",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(48),
            size_hint_x=None,
            width=dp(140),
            pos_hint={"center_x": 0.5},
            background_color=hex_color(CARD2),
            foreground_color=hex_color(WHITE),
            cursor_color=hex_color(WHITE),
            halign="center",
        )

        card.add_widget(
            self.bet
        )

        button = CandyButton(
            text="=)  КРУТИТЬ",
            size_hint_y=None,
            height=dp(55),
        )

        button.bind(
            on_release=self.spin
        )

        card.add_widget(
            button
        )

        scroll.add_widget(
            card
        )

        self.main.add_widget(
            scroll
        )

    def update_rect(
        self,
        label
    ):

        label.rect.pos = label.pos
        label.rect.size = label.size

    def spin(
        self,
        *args
    ):

        if self.running:
            return

        try:
            bet = int(
                self.bet.text
            )
        except ValueError:
            self.casino.notify(
                "Введите корректную ставку."
            )
            return

        if not self.casino.take_bet(
            bet
        ):
            return

        self.running = True

        self.final = [
            random.choice(self.symbols)
            for _ in range(3)
        ]

        self.step = 0

        Clock.schedule_interval(
            self.animate,
            0.06
        )

    def animate(
        self,
        dt
    ):

        self.step += 1

        for i, label in enumerate(
            self.reel_labels
        ):

            if self.step < 35:

                label.text = random.choice(
                    self.symbols
                )

            elif self.step < 45:

                if i == 0:

                    label.text = self.final[0]

                elif i == 1 and self.step >= 40:

                    label.text = self.final[1]

                elif i == 2 and self.step >= 44:

                    label.text = self.final[2]

                else:

                    label.text = random.choice(
                        self.symbols
                    )

            else:

                label.text = self.final[i]

        if self.step >= 50:

            return False

        return True

    def finish(
        self,
        *args
    ):

        pass


# ============================================================
# РУЛЕТКА
# ============================================================

class RouletteWidget(Widget):

    rotation = NumericProperty(0)

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.number = None
        self.highlight = None

        self.bind(
            pos=self.redraw,
            size=self.redraw,
            rotation=self.redraw
        )

        Clock.schedule_once(
            lambda dt: self.redraw(),
            0.1
        )

    def redraw(
        self,
        *args
    ):

        self.canvas.clear()

        cx = self.center_x
        cy = self.center_y

        radius = min(
            self.width,
            self.height
        ) * 0.42

        with self.canvas:

            # Внешнее кольцо
            Color(
                *hex_color(GOLD)
            )

            Line(
                circle=(
                    cx,
                    cy,
                    radius + dp(5)
                ),
                width=2
            )

            step = 360 / 37

            for number in range(37):

                start = (
                    number * step
                    + self.rotation
                )

                if number == 0:

                    color = GREEN_ROULETTE

                elif number in {
                    1, 3, 5, 7, 9,
                    12, 14, 16, 18,
                    19, 21, 23, 25,
                    27, 30, 32, 34, 36
                }:

                    color = RED_ROULETTE

                else:

                    color = BLACK_ROULETTE

                if self.highlight == number:

                    color = GOLD

                Color(
                    *hex_color(color)
                )

                Ellipse(
                    pos=(
                        cx - radius,
                        cy - radius
                    ),
                    size=(
                        radius * 2,
                        radius * 2
                    ),
                    angle_start=start,
                    angle_end=start + step
                )

            # Центр
            Color(
                *hex_color(DARK)
            )

            Ellipse(
                pos=(
                    cx - dp(48),
                    cy - dp(48)
                ),
                size=(
                    dp(96),
                    dp(96)
                )
            )

            Color(
                *hex_color(GOLD)
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(48)
                ),
                width=2
            )

            # Стрелка
            Color(
                *hex_color(WHITE)
            )

            from kivy.graphics import Triangle

            Triangle(
                points=[
                    cx - dp(12),
                    cy + radius + dp(5),

                    cx + dp(12),
                    cy + radius + dp(5),

                    cx,
                    cy + radius - dp(20),
                ]
            )


class RouletteScreen(BaseScreen):

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="roulette",
            **kwargs
        )

        self.casino = casino
        self.running = False

        self.main.add_widget(
            self.header(
                ";) Рулетка",
                "Выберите ставку и запустите вращение."
            )
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter(
                "height"
            )
        )

        card = RoundedPanel(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            size_hint_y=None,
            height=dp(570)
        )

        self.wheel = RouletteWidget(
            size_hint_y=None,
            height=dp(350)
        )

        card.add_widget(
            self.wheel
        )

        self.bet = TextInput(
            text="25",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(45),
            size_hint_x=None,
            width=dp(140),
            pos_hint={"center_x": 0.5},
            background_color=hex_color(CARD2),
            foreground_color=hex_color(WHITE),
            halign="center"
        )

        card.add_widget(
            self.bet
        )

        self.choice = Spinner(
            text="R Красное ×2",
            values=[
                "R Красное ×2",
                "B Чёрное ×2",
                "G Ноль ×36",
                "Чёт ×2",
                "Нечёт ×2",
            ],
            size_hint_y=None,
            height=dp(45),
            background_color=hex_color(CARD2),
            color=hex_color(WHITE),
        )

        card.add_widget(
            self.choice
        )

        self.result = Label(
            text="Выберите ставку",
            color=hex_color(GRAY),
            font_size=dp(15),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )

        card.add_widget(
            self.result
        )

        button = CandyButton(
            text=";)  КРУТИТЬ РУЛЕТКУ",
            size_hint_y=None,
            height=dp(52)
        )

        button.bind(
            on_release=self.spin
        )

        card.add_widget(
            button
        )

        content.add_widget(
            card
        )

        scroll.add_widget(
            content
        )

        self.main.add_widget(
            scroll
        )

    def spin(
        self,
        *args
    ):

        if self.running:
            return

        try:
            bet = int(
                self.bet.text
            )
        except ValueError:
            self.casino.notify(
                "Введите корректную ставку."
            )
            return

        if not self.casino.take_bet(
            bet
        ):
            return

        self.running = True

        self.bet_value = bet

        self.final_number = random.randint(
            0,
            36
        )

        self.frame = 0
        self.total_frames = 100

        self.start_rotation = 0

        step = 360 / 37

        center = (
            self.final_number * step
            + step / 2
        )

        self.target_rotation = (
            90
            - center
            + 360 * random.randint(5, 7)
        )

        Clock.schedule_interval(
            self.animate,
            0.025
        )

    def animate(
        self,
        dt
    ):

        self.frame += 1

        progress = (
            self.frame
            / self.total_frames
        )

        ease = 1 - (
            1 - progress
        ) ** 4

        self.wheel.rotation = (
            self.start_rotation
            + (
                self.target_rotation
                - self.start_rotation
            )
            * ease
        )

        if self.frame >= self.total_frames:

            self.wheel.rotation = (
                self.target_rotation
            )

            self.wheel.highlight = (
                self.final_number
            )

            Clock.schedule_once(
                self.finish,
                0.15
            )

            return False

        return True

    def finish(
        self,
        *args
    ):

        number = self.final_number
        choice = self.choice.text

        if number == 0:

            color = "zero"

        elif number in {
            1, 3, 5, 7, 9,
            12, 14, 16, 18,
            19, 21, 23, 25,
            27, 30, 32, 34, 36
        }:

            color = "red"

        else:

            color = "black"

        multiplier = 0

        if choice.startswith("R") and color == "red":

            multiplier = 2

        elif choice.startswith("B") and color == "black":

            multiplier = 2

        elif choice.startswith("G") and color == "zero":

            multiplier = 36

        elif choice.startswith("Чёт"):

            if number != 0 and number % 2 == 0:
                multiplier = 2

        elif choice.startswith("Нечёт"):

            if number % 2 == 1:
                multiplier = 2

        win = self.bet_value * multiplier

        self.casino.balance += win

        self.casino.update_balance()

        if win:

            self.result.text = (
                f"[WIN] Выпало {number} • "
                f"+€ {win:,}"
            )

            self.result.color = hex_color(
                GREEN
            )

            self.casino.add_history(
                ";) Рулетка",
                win - self.bet_value
            )

        else:

            self.result.text = (
                f"Выпало {number} • "
                "Проигрыш"
            )

            self.result.color = hex_color(
                RED
            )

            self.casino.add_history(
                ";) Рулетка",
                -self.bet_value
            )

        self.running = False


# ============================================================
# ПЕРСОНАЖИ
# ============================================================

class CharacterCard(RoundedPanel):

    def __init__(
        self,
        name,
        stats,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(230),
            bg_color=CARD,
            **kwargs
        )

        title = Label(
            text=f"[USER]  {name}",
            color=hex_color(GOLD),
            font_size=dp(17),
            bold=True,
            size_hint_y=None,
            height=dp(35),
            halign="left"
        )

        self.add_widget(
            title
        )

        grid = GridLayout(
            cols=3,
            spacing=dp(5)
        )

        for stat, value in stats.items():

            cell = RoundedPanel(
                orientation="vertical",
                padding=dp(5),
                spacing=dp(2),
                bg_color=CARD2
            )

            cell.add_widget(
                Label(
                    text=stat,
                    color=hex_color(GRAY),
                    font_size=dp(9)
                )
            )

            cell.add_widget(
                Label(
                    text=f"{value}/100",
                    color=hex_color(WHITE),
                    bold=True,
                    font_size=dp(12)
                )
            )

            grid.add_widget(
                cell
            )

        self.add_widget(
            grid
        )


class CharactersScreen(BaseScreen):

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="characters",
            **kwargs
        )

        self.casino = casino

        self.main.add_widget(
            self.header(
                ":) Персонажи",
                f"Все персонажи • {len(casino.characters)} человек"
            )
        )

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.container = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10),
            size_hint_y=None
        )

        self.container.bind(
            minimum_height=self.container.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.container
        )

        self.main.add_widget(
            scroll
        )

        self.scroll = scroll
        Window.bind(on_mouse_down=lambda win, x, y, button, modifiers:
                    _wheel_scroll(scroll, type("Touch", (), {"pos": (x, y), "button": button})()) or False)

        self.refresh()

    def refresh(self):

        self.container.clear_widgets()

        for name, stats in self.casino.characters.items():

            self.container.add_widget(
                CharacterCard(
                    name,
                    stats
                )
            )


# ============================================================
# СТАВКИ НА ПЕРСОНАЖЕЙ
# ============================================================

class CharacterBetScreen(BaseScreen):

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="bets",
            **kwargs
        )

        self.casino = casino
        self.running = False

        self.main.add_widget(
            self.header(
                "<3 Ставки на персонажей",
                "Шанс удачи 50/50. При победе ставка × множитель, при проигрыше ставка сгорает."
            )
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter(
                "height"
            )
        )

        # ----------------------------------------------------
        # ВЫБОР ПЕРСОНАЖА
        # ----------------------------------------------------

        title = Label(
            text="Персонаж",
            color=hex_color(GRAY),
            font_size=dp(11),
            size_hint_y=None,
            height=dp(25),
            halign="left"
        )

        content.add_widget(
            title
        )

        self.character_spinner = Spinner(
            text=list(
                casino.characters.keys()
            )[0],
            values=list(
                casino.characters.keys()
            ),
            size_hint_y=None,
            height=dp(50),
            background_color=hex_color(CARD2),
            color=hex_color(WHITE),
            font_size=dp(13)
        )

        self.character_spinner.bind(
            text=self.character_changed
        )

        content.add_widget(
            self.character_spinner
        )

        # ----------------------------------------------------
        # ХАРАКТЕРИСТИКИ
        # ----------------------------------------------------

        content.add_widget(
            Label(
                text="Характеристики персонажа",
                color=hex_color(WHITE),
                font_size=dp(18),
                bold=True,
                size_hint_y=None,
                height=dp(35)
            )
        )

        self.stats_grid = GridLayout(
            cols=3,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(330)
        )

        content.add_widget(
            self.stats_grid
        )

        # ----------------------------------------------------
        # ХАРАКТЕРИСТИКА ДЛЯ СТАВКИ
        # ----------------------------------------------------

        content.add_widget(
            Label(
                text="Характеристика для ставки",
                color=hex_color(GRAY),
                font_size=dp(11),
                size_hint_y=None,
                height=dp(25)
            )
        )

        self.parameter_spinner = Spinner(
            text=BET_PARAMETERS[0],
            values=BET_PARAMETERS,
            size_hint_y=None,
            height=dp(50),
            background_color=hex_color(CARD2),
            color=hex_color(WHITE)
        )

        self.parameter_spinner.bind(
            text=self.parameter_changed
        )

        content.add_widget(
            self.parameter_spinner
        )

        # ----------------------------------------------------
        # МНОЖИТЕЛЬ
        # ----------------------------------------------------

        content.add_widget(
            Label(
                text="Множитель",
                color=hex_color(GRAY),
                font_size=dp(11),
                size_hint_y=None,
                height=dp(25)
            )
        )

# ----------------------------------------------------
        # РАЗМЕР СТАВКИ
        # ----------------------------------------------------

        content.add_widget(
            Label(
                text="Размер ставки (€)",
                color=hex_color(GRAY),
                font_size=dp(11),
                size_hint_y=None,
                height=dp(25)
            )
        )

        self.bet_input = TextInput(
            text="25",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(50),
            background_color=hex_color(CARD2),
            foreground_color=hex_color(WHITE),
            cursor_color=hex_color(WHITE),
            halign="center"
        )

        content.add_widget(
            self.bet_input
        )

        # ----------------------------------------------------
        # ИНФОРМАЦИЯ
        # ----------------------------------------------------

        self.info = Label(
            text="",
            color=hex_color(GOLD),
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )

        content.add_widget(
            self.info
        )

        button = CandyButton(
            text="<3  СДЕЛАТЬ СТАВКУ",
            size_hint_y=None,
            height=dp(55)
        )

        button.bind(
            on_release=self.make_bet
        )

        content.add_widget(
            button
        )

        scroll.add_widget(
            content
        )

        self.main.add_widget(
            scroll
        )

        self.scroll = scroll

        self.refresh_stats()

    # --------------------------------------------------------
    # ПРОКРУТКА КОЛЁСИКОМ
    # --------------------------------------------------------

    def on_touch_down(
        self,
        touch
    ):

        if "button" in touch.profile:

            if touch.button == "scrollup":

                self.scroll.scroll_y = min(
                    1,
                    self.scroll.scroll_y + 0.12
                )

                return True

            if touch.button == "scrolldown":

                self.scroll.scroll_y = max(
                    0,
                    self.scroll.scroll_y - 0.12
                )

                return True

        return super().on_touch_down(
            touch
        )

    def character_changed(
        self,
        spinner,
        text
    ):

        self.refresh_stats()

    def parameter_changed(
        self,
        spinner,
        text
    ):

        self.update_info()

    def refresh_stats(self):

        self.stats_grid.clear_widgets()

        name = self.character_spinner.text

        stats = self.casino.characters[name]

        for stat, value in stats.items():

            card = RoundedPanel(
                orientation="vertical",
                padding=dp(5),
                spacing=dp(1),
                bg_color=CARD2
            )

            card.add_widget(
                Label(
                    text=stat,
                    color=hex_color(GRAY),
                    font_size=dp(9)
                )
            )

            card.add_widget(
                Label(
                    text=f"{value}/100",
                    color=hex_color(WHITE),
                    bold=True,
                    font_size=dp(12)
                )
            )

            self.stats_grid.add_widget(
                card
            )

        self.update_info()

    def update_info(self):

        name = self.character_spinner.text

        stat = self.parameter_spinner.text

        value = self.casino.characters[
            name
        ][stat]

        self.info.text = (
            f"{name} • {stat}: {value}/100"
        )

    def make_bet(
        self,
        *args
    ):

        if self.running:
            return

        try:

            bet = int(
                self.bet_input.text
            )

        except ValueError:

            self.casino.notify(
                "Введите корректную ставку."
            )

            return

        if not self.casino.take_bet(
            bet
        ):

            return

        self.running = True

        name = self.character_spinner.text
        stat = self.parameter_spinner.text

        value = self.casino.characters[
            name
        ][stat]

        # Множитель выбирается автоматически по заданным весам.
        multiplier = random_multiplier()

        # Ровно 50/50: один из двух исходов выбирается случайно.
        # Характеристика персонажа и множитель на шанс НЕ влияют.
        won = random.choice((True, False))

        # Множитель уже выбран, но показываем его только в результате.
        if won:

            # Ставка уже списана при начале раунда.
            # При удаче возвращаем ставку, умноженную на выпавший множитель.
            payout = int(
                bet * multiplier
            )

            self.casino.balance += payout

            self.casino.characters[
                name
            ][stat] = min(
                100,
                value + random.randint(
                    1,
                    4
                )
            )

            self.info.text = (
                f"[WIN] ПОБЕДА!\n"
                f"{name} • {stat}: "
                f"{self.casino.characters[name][stat]}/100\n"
                f"×{multiplier:g} • +€ {payout:,}"
            )

            self.info.color = hex_color(
                GREEN
            )

            self.casino.add_history(
                f"{name} — {stat}",
                payout - bet
            )

        else:

            # При неудаче ставка не возвращается — она сгорает.
            self.casino.characters[
                name
            ][stat] = max(
                0,
                value - random.randint(
                    1,
                    4
                )
            )

            self.info.text = (
                f"[LOSE] НЕУДАЧА\n"
                f"{name} • {stat}: "
                f"{self.casino.characters[name][stat]}/100"
            )

            self.info.color = hex_color(
                RED
            )

            self.casino.add_history(
                f"{name} — {stat}",
                -bet
            )

        self.casino.update_balance()

        self.refresh_stats()

        # Множитель показываем только после завершения расчёта,
        # в отдельном анимированном окне.
        self.running = True
        popup = MultiplierRevealPopup(
            multiplier=multiplier,
            won=won,
            payout=(payout if "payout" in locals() else 0)
        )
        popup.bind(
            on_dismiss=lambda *_: setattr(self, "running", False)
        )
        popup.open()



class MultiplierRevealPopup(Popup):
    """Отдельное окно для эффектного раскрытия случайного множителя."""

    def __init__(self, multiplier, won, payout=0, **kwargs):
        super().__init__(
            title="",
            separator_height=0,
            size_hint=(0.82, 0.48),
            auto_dismiss=False,
            background="",
            background_color=(0, 0, 0, 0),
            **kwargs
        )

        self.multiplier = multiplier
        self.won = won

        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(10)
        )

        with root.canvas.before:
            Color(*hex_color(DARK))
            self.bg_rect = RoundedRectangle(
                pos=root.pos,
                size=root.size,
                radius=[dp(24)]
            )

        root.bind(
            pos=lambda obj, value: setattr(self.bg_rect, "pos", value),
            size=lambda obj, value: setattr(self.bg_rect, "size", value)
        )

        self.status = Label(
            text="РЕЗУЛЬТАТ СТАВКИ",
            color=hex_color(GOLD),
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(32)
        )

        self.reveal = Label(
            text="× ?",
            color=hex_color(GOLD),
            font_size=dp(52),
            bold=True,
            opacity=0,
            size_hint_y=None,
            height=dp(90)
        )

        self.result = Label(
            text="Множитель определяется...",
            color=hex_color(GRAY),
            font_size=dp(14),
            size_hint_y=None,
            height=dp(40)
        )

        root.add_widget(self.status)
        root.add_widget(self.reveal)
        root.add_widget(self.result)

        self.content = root

    def on_open(self):
        Clock.schedule_once(self._start_reveal, 0.12)

    def _start_reveal(self, *_):
        # Сначала скрытый множитель слегка "встряхивается",
        # затем появляется увеличением и плавным проявлением.
        self.reveal.text = "× ?"
        self.reveal.opacity = 0.0

        pulse = (
            Animation(opacity=0.25, duration=0.12) +
            Animation(opacity=0.0, duration=0.12)
        )
        pulse.repeat = True

        def stop_pulse(*_):
            pulse.cancel(self.reveal)

        Clock.schedule_once(stop_pulse, 0.85)

        reveal = (
            Animation(opacity=1, font_size=dp(72), duration=0.18) +
            Animation(font_size=dp(58), duration=0.10) +
            Animation(font_size=dp(64), duration=0.08)
        )

        Clock.schedule_once(
            lambda *_: self._show_multiplier(),
            0.92
        )
        reveal.start(self.reveal)

    def _show_multiplier(self):
        self.reveal.text = f"×{self.multiplier:g}"

        if self.won:
            self.reveal.color = hex_color(GREEN)
            self.result.text = "ПОБЕДА!  Множитель выпал!"
            self.result.color = hex_color(GREEN)
        else:
            self.reveal.color = hex_color(RED)
            self.result.text = "НЕУДАЧА  •  Выпавший множитель"
            self.result.color = hex_color(RED)

        # Финальный "прыжок" множителя.
        anim = (
            Animation(font_size=dp(76), duration=0.10) +
            Animation(font_size=dp(62), duration=0.16)
        )
        anim.start(self.reveal)

        Clock.schedule_once(
            lambda *_: self.dismiss(),
            1.45
        )


# ============================================================
# ИСТОРИЯ
# ============================================================

class HistoryScreen(BaseScreen):

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="history",
            **kwargs
        )

        self.casino = casino

        self.main.add_widget(
            self.header(
                ":P История",
                "Последние результаты."
            )
        )

        scroll = ScrollView()

        self.container = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(15),
            size_hint_y=None
        )

        self.container.bind(
            minimum_height=self.container.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.container
        )

        self.main.add_widget(
            scroll
        )

        self.refresh()

    def refresh(self):

        self.container.clear_widgets()

        if not self.casino.history:

            self.container.add_widget(
                Label(
                    text="Пока нет сыгранных партий.",
                    color=hex_color(GRAY),
                    size_hint_y=None,
                    height=dp(50)
                )
            )

            return

        for game, amount in self.casino.history:

            color = (
                GREEN
                if amount >= 0
                else RED
            )

            sign = (
                "+"
                if amount >= 0
                else ""
            )

            row = RoundedPanel(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(50),
                padding=[
                    dp(12),
                    dp(5)
                ],
                bg_color=CARD2
            )

            row.add_widget(
                Label(
                    text=game,
                    color=hex_color(TEXT),
                    halign="left"
                )
            )

            row.add_widget(
                Label(
                    text=f"{sign}€ {amount:,}",
                    color=hex_color(color),
                    bold=True,
                    size_hint_x=0.35
                )
            )

            self.container.add_widget(
                row
            )



# ============================================================
# ВЕКТОРНАЯ ИГРОВАЯ КАРТА
# Без Unicode-мастей: все масти рисуются через Kivy Canvas,
# поэтому квадратики вместо ♠ ♥ ♦ ♣ больше не появляются.
# ============================================================

class PlayingCardWidget(Widget):

    def __init__(self, rank, suit, **kwargs):
        super().__init__(
            size_hint_x=None,
            width=dp(72),
            height=dp(100),
            **kwargs
        )

        self.rank = rank
        self.suit = suit

        self.bind(
            pos=self._redraw,
            size=self._redraw
        )

        self._redraw()

    def _redraw(self, *args):
        self.canvas.clear()

        x, y = self.pos
        w, h = self.size

        red_suit = self.suit in ("H", "D")
        suit_color = hex_color(RED if red_suit else DARK)

        with self.canvas:
            # Основа карты
            Color(*hex_color("#F7F7FA"))
            RoundedRectangle(
                pos=(x, y),
                size=(w, h),
                radius=[dp(8)]
            )

            # Тонкая рамка
            Color(*hex_color("#B9BBC6"))
            Line(
                rounded_rectangle=(
                    x, y, w, h, dp(8)
                ),
                width=1.2
            )

            # Цвет масти
            Color(*suit_color)

            # Масть в центре карты
            self._draw_suit(
                x + w / 2,
                y + h * 0.48,
                min(w, h) * 0.20
            )

        # Русские обозначения карт:
        # J -> В (валет), Q -> д (дама), K -> К (король), A -> Т (туз).
        # Числовые карты 1-9 отображаются как есть. Карты 10 нет.
        display_rank = {
            "J": "В",  # валет
            "Q": "д",  # дама
            "K": "К",  # король
            "A": "Т",  # туз
        }.get(self.rank, self.rank)

        if not hasattr(self, "_rank_label"):
            self._rank_label = Label(
                text=display_rank,
                color=suit_color,
                bold=True,
                font_size=dp(18),
                size_hint=(None, None),
                size=(dp(32), dp(25)),
                halign="center",
                valign="middle"
            )
            self.add_widget(self._rank_label)

        self._rank_label.text = display_rank
        self._rank_label.color = suit_color
        self._rank_label.pos = (
            x + dp(5),
            y + h - dp(29)
        )

    def _draw_suit(self, cx, cy, s):
        """Рисует масть простыми векторными фигурами."""

        if self.suit == "D":       # Diamond
            Triangle(points=[
                cx, cy + s,
                cx + s * 0.72, cy,
                cx, cy - s,
            ])
            Triangle(points=[
                cx, cy + s,
                cx - s * 0.72, cy,
                cx, cy - s,
            ])

        elif self.suit == "H":     # Heart
            Ellipse(
                pos=(cx - s * 0.95, cy + s * 0.05),
                size=(s, s)
            )
            Ellipse(
                pos=(cx - s * 0.05, cy + s * 0.05),
                size=(s, s)
            )
            Triangle(points=[
                cx - s * 0.95, cy + s * 0.35,
                cx + s * 0.95, cy + s * 0.35,
                cx, cy - s
            ])

        elif self.suit == "C":     # Club
            Ellipse(
                pos=(cx - s * 0.95, cy - s * 0.05),
                size=(s * 1.0, s * 1.0)
            )
            Ellipse(
                pos=(cx - s * 0.05, cy - s * 0.05),
                size=(s * 1.0, s * 1.0)
            )
            Ellipse(
                pos=(cx - s * 0.50, cy + s * 0.55),
                size=(s * 1.0, s * 1.0)
            )
            Rectangle(
                pos=(cx - s * 0.18, cy - s * 0.85),
                size=(s * 0.36, s * 1.15)
            )

        else:                      # Spade
            Ellipse(
                pos=(cx - s * 0.95, cy + s * 0.05),
                size=(s, s)
            )
            Ellipse(
                pos=(cx - s * 0.05, cy + s * 0.05),
                size=(s, s)
            )
            Triangle(points=[
                cx - s * 0.95, cy + s * 0.35,
                cx + s * 0.95, cy + s * 0.35,
                cx, cy + s * 1.25
            ])
            Rectangle(
                pos=(cx - s * 0.18, cy - s * 0.80),
                size=(s * 0.36, s * 1.05)
            )


class BlackjackScreen(BaseScreen):

    def __init__(
        self,
        casino,
        **kwargs
    ):

        super().__init__(
            name="blackjack",
            **kwargs
        )

        self.casino = casino

        self.active = False
        self.bet_value = 0

        self.deck = []
        self.player = []
        self.dealer = []

        self.main.add_widget(
            self.header(
                ":D Блэкджек",
                "Наберите больше очков, чем дилер, но не больше 21."
            )
        )

        scroll = ScrollView()

        self.card = RoundedPanel(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(650)
        )

        self.dealer_label = Label(
            text="ДИЛЕР",
            color=hex_color(GRAY),
            bold=True,
            size_hint_y=None,
            height=dp(25)
        )

        self.card.add_widget(
            self.dealer_label
        )

        self.dealer_cards = BoxLayout(
            size_hint_y=None,
            height=dp(110),
            spacing=dp(5)
        )

        self.card.add_widget(
            self.dealer_cards
        )

        self.dealer_score = Label(
            text="Очки: —",
            color=hex_color(WHITE),
            size_hint_y=None,
            height=dp(30)
        )

        self.card.add_widget(
            self.dealer_score
        )

        self.card.add_widget(
            Label(
                text="ИГРОК",
                color=hex_color(GRAY),
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
        )

        self.player_cards = BoxLayout(
            size_hint_y=None,
            height=dp(110),
            spacing=dp(5)
        )

        self.card.add_widget(
            self.player_cards
        )

        self.player_score = Label(
            text="Очки: —",
            color=hex_color(WHITE),
            size_hint_y=None,
            height=dp(30)
        )

        self.card.add_widget(
            self.player_score
        )

        self.bet = TextInput(
            text="25",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(48),
            background_color=hex_color(CARD2),
            foreground_color=hex_color(WHITE),
            halign="center"
        )

        self.card.add_widget(
            self.bet
        )

        self.result = Label(
            text="",
            color=hex_color(WHITE),
            bold=True,
            font_size=dp(15),
            size_hint_y=None,
            height=dp(50)
        )

        self.card.add_widget(
            self.result
        )

        buttons = BoxLayout(
            spacing=dp(5),
            size_hint_y=None,
            height=dp(55)
        )

        for text, command in [
            (":D Новая игра", self.new_game),
            ("+ Карта", self.hit),
            ("[STOP] Стоп", self.stand),
        ]:

            btn = CandyButton(
                text=text
            )

            btn.bind(
                on_release=command
            )

            buttons.add_widget(
                btn
            )

        self.card.add_widget(
            buttons
        )

        scroll.add_widget(
            self.card
        )

        self.main.add_widget(
            scroll
        )

    def create_deck(self):

        deck = []

        for suit in [
            "S",  # Spade
            "H",  # Heart
            "D",  # Diamond
            "C",  # Club
        ]:

            for rank, value in [
                ("1", 1),
                ("2", 2),
                ("3", 3),
                ("4", 4),
                ("5", 5),
                ("6", 6),
                ("7", 7),
                ("8", 8),
                ("9", 9),
                ("J", 10),
                ("Q", 10),
                ("K", 10),
                ("A", 11),
            ]:

                deck.append({
                    "rank": rank,
                    "value": value,
                    "suit": suit
                })

        random.shuffle(deck)

        return deck

    def hand_value(
        self,
        hand
    ):

        total = sum(
            card["value"]
            for card in hand
        )

        aces = sum(
            card["rank"] == "A"
            for card in hand
        )

        while total > 21 and aces:

            total -= 10
            aces -= 1

        return total

    def render_card(
        self,
        parent,
        card
    ):

        parent.add_widget(
            PlayingCardWidget(
                rank=card["rank"],
                suit=card["suit"]
            )
        )

    def render(self):

        self.dealer_cards.clear_widgets()
        self.player_cards.clear_widgets()

        for card in self.dealer:
            self.render_card(
                self.dealer_cards,
                card
            )

        for card in self.player:
            self.render_card(
                self.player_cards,
                card
            )

        self.dealer_score.text = (
            f"Очки: {self.hand_value(self.dealer)}"
        )

        self.player_score.text = (
            f"Очки: {self.hand_value(self.player)}"
        )

    def new_game(
        self,
        *args
    ):

        if self.active:
            return

        try:
            bet = int(
                self.bet.text
            )
        except ValueError:

            self.casino.notify(
                "Введите корректную ставку."
            )

            return

        if not self.casino.take_bet(
            bet
        ):
            return

        self.bet_value = bet

        self.deck = self.create_deck()

        self.player = [
            self.deck.pop(),
            self.deck.pop()
        ]

        self.dealer = [
            self.deck.pop(),
            self.deck.pop()
        ]

        self.active = True

        self.result.text = ""

        self.render()

        if self.hand_value(
            self.player
        ) == 21:

            payout = int(
                bet * 2.5
            )

            self.casino.balance += payout

            self.active = False

            self.result.text = (
                f":D BLACKJACK! +€ {payout:,}"
            )

            self.result.color = hex_color(
                GREEN
            )

            self.casino.add_history(
                ":D Блэкджек",
                payout - bet
            )

            self.casino.update_balance()

    def hit(
        self,
        *args
    ):

        if not self.active:
            return

        self.player.append(
            self.deck.pop()
        )

        self.render()

        if self.hand_value(
            self.player
        ) > 21:

            self.finish(
                "[BUST] Перебор! Вы проиграли.",
                0
            )

    def stand(
        self,
        *args
    ):

        if not self.active:
            return

        while self.hand_value(
            self.dealer
        ) < 17:

            self.dealer.append(
                self.deck.pop()
            )

        self.render()

        player = self.hand_value(
            self.player
        )

        dealer = self.hand_value(
            self.dealer
        )

        if dealer > 21:

            self.finish(
                f"[WIN] Дилер перебрал! +€ {self.bet_value * 2:,}",
                self.bet_value * 2
            )

        elif player > dealer:

            self.finish(
                f"[WIN] Победа! +€ {self.bet_value * 2:,}",
                self.bet_value * 2
            )

        elif player == dealer:

            self.finish(
                "[DRAW] Ничья. Ставка возвращена.",
                self.bet_value
            )

        else:

            self.finish(
                "[LOSE] Дилер победил.",
                0
            )

    def finish(
        self,
        message,
        payout
    ):

        self.active = False

        self.casino.balance += payout

        self.result.text = message

        self.result.color = hex_color(
            GREEN
            if payout
            else RED
        )

        self.casino.add_history(
            ":D Блэкджек",
            payout - self.bet_value
        )

        self.casino.update_balance()


# ============================================================
# ОСНОВНОЕ ПРИЛОЖЕНИЕ
# ============================================================

class CandyFloodApp(App):

    balance = 0
    bonus_time = 0
    bonus_streak = 0
    bonus_last_date = ""

    def build(
        self
    ):

        Window.clearcolor = hex_color(
            BG
        )

        data = load_data()

        self.balance = data["balance"]
        self.bonus_time = data["bonus_time"]
        self.bonus_streak = data.get("bonus_streak", 0)
        self.bonus_last_date = data.get("bonus_last_date", "")

        self.characters = data["characters"]

        self.history = []

        self.sm = ScreenManager(
            transition=SlideTransition(
                duration=0.15
            )
        )

        self.home = HomeScreen(
            self
        )

        self.slots = SlotsScreen(
            self
        )

        self.roulette = RouletteScreen(
            self
        )

        self.blackjack = BlackjackScreen(
            self
        )

        self.characters_screen = CharactersScreen(
            self
        )

        self.bets = CharacterBetScreen(
            self
        )

        self.history_screen = HistoryScreen(
            self
        )

        for screen in [
            self.home,
            self.slots,
            self.roulette,
            self.blackjack,
            self.characters_screen,
            self.bets,
            self.history_screen,
        ]:

            self.sm.add_widget(
                screen
            )

        self.root_layout = BoxLayout(
            orientation="vertical"
        )

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        top = BoxLayout(
            size_hint_y=None,
            height=dp(65),
            padding=[
                dp(15),
                dp(8)
            ]
        )

        top.add_widget(
            Label(
                text=APP_NAME,
                color=hex_color(GOLD),
                font_size=dp(19),
                bold=True
            )
        )

        self.balance_label = Label(
            text=f"€ {self.balance:,}",
            color=hex_color(GOLD),
            font_size=dp(16),
            bold=True,
            size_hint_x=0.35
        )

        top.add_widget(
            self.balance_label
        )

        self.root_layout.add_widget(
            top
        )

        # ----------------------------------------------------
        # КОНТЕНТ
        # ----------------------------------------------------

        body = BoxLayout(
            orientation="horizontal"
        )

        # ----------------------------------------------------
        # МЕНЮ
        # ----------------------------------------------------

        self.sidebar = BoxLayout(
            orientation="vertical",
            size_hint_x=0.25,
            spacing=dp(4),
            padding=dp(8)
        )

        menu = [
            ("^_^  Главная", "home"),
            ("=)  Слоты", "slots"),
            (";)  Рулетка", "roulette"),
            (":D  Блэкджек", "blackjack"),
            (":)  Персонажи", "characters"),
            ("<3  Ставки", "bets"),
            (":P  История", "history"),
        ]

        for text, page in menu:

            btn = CandyButton(
                text=text,
                background_color=hex_color(
                    SIDEBAR
                ),
                size_hint_y=None,
                height=dp(48)
            )

            btn.bind(
                on_release=lambda b, p=page:
                self.goto(p)
            )

            self.sidebar.add_widget(
                btn
            )

        self.sidebar.add_widget(
            Widget()
        )

        bonus = CandyButton(
            text="G  ЕЖЕДНЕВНЫЙ БОНУС",
            bg_color=GOLD,
            size_hint_y=None,
            height=dp(48)
        )

        bonus.background_color = hex_color(
            "#27212D"
        )

        bonus.color = hex_color(
            GOLD
        )

        bonus.bind(
            on_release=self.daily_bonus
        )

        self.sidebar.add_widget(
            bonus
        )

        reset = CandyButton(
            text="↻  Сбросить игру",
            bg_color=SIDEBAR,
            size_hint_y=None,
            height=dp(42)
        )

        reset.background_color = hex_color(
            SIDEBAR
        )

        reset.color = hex_color(
            GRAY
        )

        reset.bind(
            on_release=self.reset_game
        )

        self.sidebar.add_widget(
            reset
        )

        body.add_widget(
            self.sidebar
        )

        body.add_widget(
            self.sm
        )

        self.root_layout.add_widget(
            body
        )

        self.goto(
            "home"
        )

        Clock.schedule_interval(
            self.autosave,
            10
        )

        return self.root_layout

    # ========================================================
    # НАВИГАЦИЯ
    # ========================================================

    def goto(
        self,
        page
    ):

        self.sm.current = page

        if page == "home":

            self.home.refresh()

        elif page == "characters":

            self.characters_screen.refresh()

        elif page == "bets":

            self.bets.refresh_stats()

        elif page == "history":

            self.history_screen.refresh()

    # ========================================================
    # БАЛАНС
    # ========================================================

    def update_balance(
        self
    ):

        self.balance_label.text = (
            f"€ {self.balance:,}"
        )

        self.home.refresh()

        self.save()

    # ========================================================
    # СТАВКА
    # ========================================================

    def take_bet(
        self,
        amount
    ):

        if amount <= 0:

            self.notify(
                "Ставка должна быть больше нуля."
            )

            return False

        if amount > self.balance:

            self.notify(
                "Недостаточно виртуальных евро."
            )

            return False

        self.balance -= amount

        self.update_balance()

        return True

    # ========================================================
    # ИСТОРИЯ
    # ========================================================

    def add_history(
        self,
        game,
        amount
    ):

        self.history.insert(
            0,
            (
                game,
                amount
            )
        )

        if len(self.history) > 50:

            self.history.pop()

        self.history_screen.refresh()

    # ========================================================
    # УВЕДОМЛЕНИЕ
    # ========================================================

    def notify(
        self,
        text
    ):

        popup = Popup(
            title="Candy.flood",
            content=Label(
                text=text,
                color=hex_color(WHITE)
            ),
            size_hint=(0.75, None),
            height=dp(180)
        )

        popup.open()

    # ========================================================
    # БОНУС
    # ========================================================

    def daily_bonus(
        self,
        *args
    ):

        now = time.time()

        remaining = max(
            0,
            int(
                DAY_SECONDS
                - (now - self.bonus_time)
            )
        )

        if self.bonus_time and remaining > 0:

            hours = remaining // 3600

            minutes = (
                remaining % 3600
            ) // 60

            seconds = remaining % 60

            self.notify(
                "Следующий бонус через "
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

            return

        today = time.strftime("%Y-%m-%d", time.localtime(now))
        yesterday = time.strftime(
            "%Y-%m-%d",
            time.localtime(now - DAY_SECONDS)
        )

        if self.bonus_last_date == yesterday:
            self.bonus_streak += 1
        else:
            self.bonus_streak = 1

        bonus_amount = min(
            DAILY_BONUS_MAX,
            DAILY_BONUS_BASE + (self.bonus_streak - 1) * DAILY_BONUS_STEP
        )

        self.balance += bonus_amount
        self.bonus_time = now
        self.bonus_last_date = today

        self.add_history(
            "G Ежедневный бонус",
            bonus_amount
        )

        self.update_balance()

        self.notify(
            f"G Бонус получен!\n"
            f"День серии: {self.bonus_streak}\n"
            f"+€ {bonus_amount}"
        )

    # ========================================================
    # СБРОС
    # ========================================================

    def reset_game(
        self,
        *args
    ):

        self.balance = START_BALANCE

        self.bonus_time = 0
        self.bonus_streak = 0
        self.bonus_last_date = ""

        self.characters = {
            name: stats.copy()
            for name, stats in DEFAULT_CHARACTERS.items()
        }

        self.history.clear()

        self.update_balance()

        self.characters_screen.refresh()

        self.bets.character_spinner.values = list(
            self.characters.keys()
        )

        self.bets.refresh_stats()

        self.history_screen.refresh()

        self.notify(
            "Прогресс полностью сброшен."
        )

    # ========================================================
    # СОХРАНЕНИЕ
    # ========================================================

    def save(
        self
    ):

        try:

            data = {
                "balance": self.balance,
                "bonus_time": self.bonus_time,
                "bonus_streak": self.bonus_streak,
                "bonus_last_date": self.bonus_last_date,
                "characters": self.characters
            }

            path = get_save_path()

            os.makedirs(
                os.path.dirname(path),
                exist_ok=True
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as error:

            print(
                "Ошибка сохранения:",
                error
            )

    def autosave(
        self,
        dt
    ):

        self.save()

    def on_stop(
        self
    ):

        self.save()


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":

    CandyFloodApp().run()
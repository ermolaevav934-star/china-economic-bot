from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import json
import os

# ============================================================
TOKEN = "8956267241:AAFJwoo86GF3mtrQ5p6t_Yh7BDUJbEwN7ms"
# ============================================================

# Файл для сохранения избранного (чтобы не терялось при перезапуске)
FAVORITES_FILE = "favorites.json"

def load_favorites():
    """Загружает избранное из файла"""
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_favorites(favorites):
    """Сохраняет избранное в файл"""
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

# Загружаем избранное при старте
favorites_db = load_favorites()

# ============================================================
# ВСЕ 51 ТЕРМИН
# ============================================================
term_data = {
    1: {"chinese": "流动性", "pinyin": "liú dòng xìng", "tones": "2-4-4", "ru": "Ликвидность", "example_cn": "流动性过剩会导致资产泡沫", "example_ru": "Избыточная ликвидность приводит к образованию пузырей на рынке активов."},
    2: {"chinese": "国内生产总值", "pinyin": "guó nèi shēng chǎn zǒng zhí", "tones": "2-4-1-3-3-2", "ru": "Валовой внутренний продукт (ВВП)", "example_cn": "去年国内生产总值增长了5%", "example_ru": "В прошлом году ВВП вырос на 5%."},
    3: {"chinese": "通货紧缩", "pinyin": "tōng huò jǐn suō", "tones": "1-4-3-1", "ru": "Дефляция", "example_cn": "通货紧缩会导致消费需求下降", "example_ru": "Дефляция ведёт к снижению потребительского спроса."},
    4: {"chinese": "边际效应", "pinyin": "biān jì xiào yìng", "tones": "1-4-4-4", "ru": "Предельная полезность", "example_cn": "经济学家研究消费的边际效应", "example_ru": "Экономисты изучают предельную полезность потребления."},
    5: {"chinese": "机会成本", "pinyin": "jī huì chéng běn", "tones": "1-4-2-3", "ru": "Альтернативные издержки", "example_cn": "选择上大学的机会成本是放弃的工作收入", "example_ru": "Альтернативные издержки поступления в университет — потерянный заработок."},
    6: {"chinese": "供需关系", "pinyin": "gōng xū guān xì", "tones": "1-1-1-4", "ru": "Спрос и предложение", "example_cn": "价格由供需关系决定", "example_ru": "Цена определяется спросом и предложением."},
    7: {"chinese": "基尼系数", "pinyin": "jī ní xì shù", "tones": "1-2-4-4", "ru": "Коэффициент Джини", "example_cn": "基尼系数衡量收入不平等", "example_ru": "Коэффициент Джини измеряет неравенство доходов."},
    8: {"chinese": "恩格尔系数", "pinyin": "ēn gé ěr xì shù", "tones": "1-2-3-4-4", "ru": "Коэффициент Энгеля", "example_cn": "恩格尔系数越高，生活水平越低", "example_ru": "Чем выше коэффициент Энгеля, тем ниже уровень жизни."},
    9: {"chinese": "货币政策", "pinyin": "huò bì zhèng cè", "tones": "4-4-4-4", "ru": "Денежно-кредитная политика", "example_cn": "央行实施宽松的货币政策", "example_ru": "Центробанк проводит мягкую денежно-кредитную политику."},
    10: {"chinese": "财政政策", "pinyin": "cái zhèng zhèng cè", "tones": "2-4-4-4", "ru": "Фискальная политика", "example_cn": "政府通过财政政策刺激经济", "example_ru": "Правительство стимулирует экономику через фискальную политику."},
    11: {"chinese": "量化宽松", "pinyin": "liàng huà kuān sōng", "tones": "4-4-1-1", "ru": "Количественное смягчение (QE)", "example_cn": "美联储推出量化宽松政策", "example_ru": "ФРС запускает программу количественного смягчения."},
    12: {"chinese": "垄断", "pinyin": "lǒng duàn", "tones": "3-4", "ru": "Монополия", "example_cn": "反垄断法禁止市场垄断", "example_ru": "Антимонопольное законодательство запрещает монополизацию рынка."},
    13: {"chinese": "完全竞争", "pinyin": "wán quán jìng zhēng", "tones": "2-2-4-1", "ru": "Совершенная конкуренция", "example_cn": "完全竞争是理想市场模型", "example_ru": "Совершенная конкуренция — идеальная модель рынка."},
    14: {"chinese": "市场失灵", "pinyin": "shì chǎng shī líng", "tones": "4-3-1-2", "ru": "Фиаско рынка", "example_cn": "外部性会导致市场失灵", "example_ru": "Экстерналии ведут к фиаско рынка."},
    15: {"chinese": "国民收入", "pinyin": "guó mín shōu rù", "tones": "2-2-1-4", "ru": "Национальный доход", "example_cn": "国民收入反映经济整体状况", "example_ru": "Национальный доход отражает общее состояние экономики."},
    16: {"chinese": "流动性陷阱", "pinyin": "liú dòng xìng xiàn jǐng", "tones": "2-4-4-4-3", "ru": "Ликвидная ловушка", "example_cn": "利率接近于零时出现流动性陷阱", "example_ru": "При околонулевых ставках возникает ликвидная ловушка."},
    17: {"chinese": "比较优势", "pinyin": "bǐ jiào yōu shì", "tones": "3-4-1-4", "ru": "Сравнительное преимущество", "example_cn": "国际贸易基于比较优势", "example_ru": "Международная торговля основана на сравнительных преимуществах."},
    18: {"chinese": "贸易顺差", "pinyin": "mào yì shùn chā", "tones": "4-4-4-1", "ru": "Положительное сальдо торгового баланса", "example_cn": "中国长期保持贸易顺差", "example_ru": "Китай долгое время сохраняет положительное торговое сальдо."},
    19: {"chinese": "贸易逆差", "pinyin": "mào yì nì chā", "tones": "4-4-4-1", "ru": "Дефицит торгового баланса", "example_cn": "进口大于出口造成贸易逆差", "example_ru": "Импорт, превышающий экспорт, создаёт торговый дефицит."},
    20: {"chinese": "购买力平价", "pinyin": "gòu mǎi lì píng jià", "tones": "4-3-4-2-4", "ru": "Паритет покупательной способности (ППС)", "example_cn": "购买力平价比较各国实际生活水平", "example_ru": "Паритет покупательной способности сравнивает реальный уровень жизни в разных странах."},
    21: {"chinese": "经济", "pinyin": "jīng jì", "tones": "1-4", "ru": "Экономика", "example_cn": "中国经济快速增长", "example_ru": "Экономика Китая быстро растёт."},
    22: {"chinese": "通货膨胀", "pinyin": "tōng huò péng zhàng", "tones": "1-4-2-4", "ru": "Инфляция", "example_cn": "通货膨胀降低货币购买力", "example_ru": "Инфляция снижает покупательную способность денег."},
    23: {"chinese": "利率", "pinyin": "lì lǜ", "tones": "4-4", "ru": "Процентная ставка", "example_cn": "央行提高利率抑制通胀", "example_ru": "Центробанк повышает ставку, чтобы сдержать инфляцию."},
    24: {"chinese": "汇率", "pinyin": "huì lǜ", "tones": "4-4", "ru": "Валютный курс", "example_cn": "人民币汇率近期走强", "example_ru": "Курс юаня в последнее время укрепляется."},
    25: {"chinese": "股票", "pinyin": "gǔ piào", "tones": "3-4", "ru": "Акция", "example_cn": "他投资股票市场", "example_ru": "Он инвестирует в фондовый рынок."},
    26: {"chinese": "债券", "pinyin": "zhài quàn", "tones": "4-4", "ru": "Облигация", "example_cn": "政府发行国债筹集资金", "example_ru": "Правительство выпускает государственные облигации."},
    27: {"chinese": "基金", "pinyin": "jī jīn", "tones": "1-1", "ru": "Инвестиционный фонд", "example_cn": "她买了指数基金", "example_ru": "Она купила индексный фонд."},
    28: {"chinese": "保险", "pinyin": "bǎo xiǎn", "tones": "3-3", "ru": "Страхование", "example_cn": "医疗保险很重要", "example_ru": "Медицинская страховка очень важна."},
    29: {"chinese": "税收", "pinyin": "shuì shōu", "tones": "4-1", "ru": "Налог", "example_cn": "税收是国家主要收入来源", "example_ru": "Налоги — основной источник доходов государства."},
    30: {"chinese": "预算", "pinyin": "yù suàn", "tones": "4-4", "ru": "Бюджет", "example_cn": "公司年度预算已经批准", "example_ru": "Годовой бюджет компании утверждён."},
    31: {"chinese": "赤字", "pinyin": "chì zì", "tones": "4-4", "ru": "Дефицит", "example_cn": "财政赤字需要弥补", "example_ru": "Бюджетный дефицит необходимо покрыть."},
    32: {"chinese": "盈余", "pinyin": "yíng yú", "tones": "2-2", "ru": "Профицит", "example_cn": "预算盈余是好事吗？", "example_ru": "Бюджетный профицит — это хорошо?"},
    33: {"chinese": "债务", "pinyin": "zhài wù", "tones": "4-4", "ru": "Долг", "example_cn": "国家债务水平很高", "example_ru": "Уровень государственного долга очень высок."},
    34: {"chinese": "资产", "pinyin": "zī chǎn", "tones": "1-3", "ru": "Актив", "example_cn": "他的资产包括房产和股票", "example_ru": "Его активы включают недвижимость и акции."},
    35: {"chinese": "负债", "pinyin": "fù zhài", "tones": "4-4", "ru": "Пассив", "example_cn": "公司负债累累", "example_ru": "У компании огромные долги."},
    36: {"chinese": "净值", "pinyin": "jìng zhí", "tones": "4-2", "ru": "Чистая стоимость", "example_cn": "家庭净值逐年增长", "example_ru": "Чистая стоимость домохозяйства растёт год от года."},
    37: {"chinese": "收入", "pinyin": "shōu rù", "tones": "1-4", "ru": "Доход", "example_cn": "她的月收入提高了", "example_ru": "Её ежемесячный доход вырос."},
    38: {"chinese": "支出", "pinyin": "zhī chū", "tones": "1-1", "ru": "Расход", "example_cn": "控制支出有助于储蓄", "example_ru": "Контроль расходов помогает сберегать."},
    39: {"chinese": "储蓄", "pinyin": "chǔ xù", "tones": "3-4", "ru": "Сбережения", "example_cn": "银行存款是主要的储蓄方式", "example_ru": "Банковские депозиты — основной способ сбережений."},
    40: {"chinese": "投资", "pinyin": "tóu zī", "tones": "2-1", "ru": "Инвестиции", "example_cn": "投资有风险", "example_ru": "Инвестиции сопряжены с риском."},
    41: {"chinese": "消费", "pinyin": "xiāo fèi", "tones": "1-4", "ru": "Потребление", "example_cn": "消费拉动经济增长", "example_ru": "Потребление стимулирует экономический рост."},
    42: {"chinese": "生产", "pinyin": "shēng chǎn", "tones": "1-3", "ru": "Производство", "example_cn": "生产成本不断上升", "example_ru": "Себестоимость производства постоянно растёт."},
    43: {"chinese": "供给", "pinyin": "gōng jǐ", "tones": "1-3", "ru": "Предложение", "example_cn": "供给大于需求导致价格下跌", "example_ru": "Превышение предложения над спросом ведёт к падению цен."},
    44: {"chinese": "需求", "pinyin": "xū qiú", "tones": "1-2", "ru": "Спрос", "example_cn": "市场需求旺盛", "example_ru": "Рыночный спрос высок."},
    45: {"chinese": "价格", "pinyin": "jià gé", "tones": "4-2", "ru": "Цена", "example_cn": "汽油价格又涨了", "example_ru": "Цены на бензин снова выросли."},
    46: {"chinese": "成本", "pinyin": "chéng běn", "tones": "2-3", "ru": "Себестоимость", "example_cn": "降低成本提高利润", "example_ru": "Снижение издержек повышает прибыль."},
    47: {"chinese": "利润", "pinyin": "lì rùn", "tones": "4-4", "ru": "Прибыль", "example_cn": "公司利润同比增长10%", "example_ru": "Прибыль компании выросла на 10%."},
    48: {"chinese": "亏损", "pinyin": "kuī sǔn", "tones": "1-3", "ru": "Убыток", "example_cn": "疫情期间许多企业亏损", "example_ru": "Во время пандемии многие предприятия понесли убытки."},
    49: {"chinese": "市场", "pinyin": "shì chǎng", "tones": "4-3", "ru": "Рынок", "example_cn": "房地产市场降温", "example_ru": "Рынок недвижимости остывает."},
    50: {"chinese": "资本", "pinyin": "zī běn", "tones": "1-3", "ru": "Капитал", "example_cn": "人力资本同样重要", "example_ru": "Человеческий капитал не менее важен."},
    51: {"chinese": "经济周期", "pinyin": "jīng jì zhōu qī", "tones": "1-4-1-1", "ru": "Экономический цикл", "example_cn": "经济周期包括繁荣和衰退", "example_ru": "Экономический цикл включает подъём и спад."}
}

# ============================================================
# ФУНКЦИИ ПОИСКА
# ============================================================
def find_term(text):
    text = text.strip()
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 51:
            return num, term_data[num]
    for num, data in term_data.items():
        if data["chinese"] == text:
            return num, data
    for num, data in term_data.items():
        if text.lower() in data["ru"].lower():
            return num, data
    return None, None

def get_user_id(update):
    if update.effective_user:
        return update.effective_user.id
    if update.callback_query and update.callback_query.from_user:
        return update.callback_query.from_user.id
    if update.message and update.message.from_user:
        return update.message.from_user.id
    return 0

# ============================================================
# КОМАНДЫ БОТА
# ============================================================
async def start(update, context):
    user_id = str(get_user_id(update))
    if user_id not in favorites_db:
        favorites_db[user_id] = []
        save_favorites(favorites_db)
    
    keyboard = [
        [InlineKeyboardButton("🔍 Найти термин", callback_data="find")],
        [InlineKeyboardButton("📚 Моё избранное", callback_data="favorites")],
        [InlineKeyboardButton("📋 Список 1-51", callback_data="list_all")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    text = "🇨🇳 **ChinaEconomicsBot**\n\nБот для изучения китайских экономических терминов.\n\n**Что вводить:**\n• Номер от 1 до 51\n• Китайские иероглифы\n• Русское слово\n\nПример: `21`, `经济`, `экономика`"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_term(update, context, num, data, is_callback=True):
    user_id = str(get_user_id(update))
    favs = favorites_db.get(user_id, [])
    is_favorite = data["chinese"] in favs
    
    text = f"📌 **{num}. {data['chinese']}**\n\n🎵 {data['pinyin']} (тоны: {data['tones']})\n\n🇷🇺 {data['ru']}\n\n📖 **Пример:**\n“{data['example_cn']}”\n→ {data['example_ru']}"
    
    # Кнопка добавления/удаления из избранного
    fav_button_text = "❤️ Удалить из избранного" if is_favorite else "💾 Добавить в избранное"
    
    keyboard = [
        [InlineKeyboardButton(fav_button_text, callback_data=f"fav_{num}_{data['chinese']}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"prev_{num}"), InlineKeyboardButton("Вперед ➡️", callback_data=f"next_{num}")],
        [InlineKeyboardButton("🔍 Новый поиск", callback_data="find")],
        [InlineKeyboardButton("🔙 Меню", callback_data="menu")]
    ]
    
    if is_callback and update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_message(update, context):
    num, data = find_term(update.message.text)
    if data:
        await show_term(update, context, num, data, False)
    else:
        await update.message.reply_text("❌ Термин не найден. Попробуйте номер (1-51), иероглифы или русское слово.")

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(get_user_id(update))
    
    if data == "menu":
        await start(update, context)
    elif data == "find":
        await query.edit_message_text("🔍 **Введите номер, иероглифы или русское слово**", parse_mode="Markdown")
    elif data == "favorites":
        favs = favorites_db.get(user_id, [])
        if favs:
            text = "📚 **Ваше избранное:**\n\n"
            for i, term in enumerate(favs, 1):
                for num, td in term_data.items():
                    if td["chinese"] == term:
                        text += f"{i}. {term} — {td['ru']}\n"
                        break
            text += "\n🗑️ Чтобы удалить термин, нажмите /delete"
        else:
            text = "📚 У вас пока нет сохранённых терминов.\n\nЧтобы добавить — найдите термин и нажмите «Добавить в избранное»."
        await query.edit_message_text(text, parse_mode="Markdown")
    elif data == "list_all":
        text = "📋 **Список терминов (1-51):**\n\n"
        for i in range(1, 52):
            text += f"{i}. {term_data[i]['chinese']} — {term_data[i]['ru']}\n"
        await query.edit_message_text(text, parse_mode="Markdown")
    elif data == "help":
        text = "❓ **Помощь**\n\n/start - Главное меню\n/delete - Удалить последний термин из избранного\n\n**Что можно делать:**\n• Ввести номер (1-51)\n• Ввести иероглифы\n• Ввести русское слово\n• Сохранять термины в избранное"
        await query.edit_message_text(text, parse_mode="Markdown")
    
    elif data.startswith("fav_"):
        # Формат: fav_номер_термин
        parts = data.split("_", 2)
        if len(parts) >= 3:
            num = int(parts[1])
            term = parts[2]
            favs = favorites_db.get(user_id, [])
            
            if term in favs:
                favs.remove(term)
                await query.edit_message_text(f"🗑️ Термин «{term}» удалён из избранного.")
            else:
                favs.append(term)
                await query.edit_message_text(f"✅ Термин «{term}» добавлен в избранное!")
            
            favorites_db[user_id] = favs
            save_favorites(favorites_db)
            
            # Через секунду показываем обновлённый термин
            await show_term(update, context, num, term_data[num], True)
    
    elif data.startswith("next_"):
        num = int(data[5:])
        next_num = num + 1 if num < 51 else 1
        await show_term(update, context, next_num, term_data[next_num], True)
    elif data.startswith("prev_"):
        num = int(data[5:])
        prev_num = num - 1 if num > 1 else 51
        await show_term(update, context, prev_num, term_data[prev_num], True)

async def delete_command(update, context):
    user_id = str(get_user_id(update))
    favs = favorites_db.get(user_id, [])
    if favs:
        removed = favs.pop()
        favorites_db[user_id] = favs
        save_favorites(favorites_db)
        await update.message.reply_text(f"🗑️ Термин «{removed}» удалён из избранного.")
    else:
        await update.message.reply_text("📚 Ваше избранное пусто.")

# ============================================================
# ЗАПУСК
# ============================================================
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Бот запущен! Все 51 термин загружены.")
    print("📚 Функция избранного работает и сохраняется в файл.")
    app.run_polling()

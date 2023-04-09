import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from Configs.BotSettings import config

# Создаем экземпляр бота и настраиваем Intents
intents = discord.Intents(messages=True, message_content=True, members = True)

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Создаем словарь с рангами и соответствующими им ролями
ranks = {
    'Новичок': {
        'role_name': 'Новичок',
        'max_exp': 100
    },
    'Продвинутый': {
        'role_name': 'Продвинутый',
        'max_exp': 500
    },
    'Опытный': {
        'role_name': 'Опытный',
        'max_exp': 1000
    }
}

# Создаем словарь с опытом пользователей
user_exp = {}

# Обработчик события загрузки бота
@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов к работе')
    
async def on_member_join(member):
    # Получаем канал, в котором будет происходить приветствие
    welcome_channel = client.get_channel(1081953009317203979)  # Замените на ID канала, где будете делать приветствие

    # Создаем embed с приветствием
    embed = discord.Embed(title=f'Добро пожаловать на сервер {member.guild.name}!', description=f'Привет, {member.mention}! Добро пожаловать на наш сервер!', color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='Правила сервера', value='Пожалуйста, ознакомьтесь с правилами нашего сервера.', inline=False)
    embed.set_footer(text='Спасибо, что присоединились к нам!')

    # Отправляем embed в канал
    await welcome_channel.send(embed=embed)
   
async def on_member_remove(member):
    # Получаем канал, в котором будет происходить прощание
    goodbye_channel = client.get_channel(1081953382945796137)  # Замените на ID канала, где будете делать прощание

    # Создаем embed с прощанием
    embed = discord.Embed(title='До свидания!', description=f'{member.name}#{member.discriminator} покинул(а) сервер {member.guild.name}.', color=discord.Color.red())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Надеемся увидеть вас снова!')

    # Отправляем embed в канал
    await goodbye_channel.send(embed=embed)
    
# Функция для обновления ролей пользователя на основе его опыта
async def update_user_rank(user):
    # Получаем текущий опыт пользователя
    exp = user_exp.get(user.id, 0)

    # Проверяем, соответствует ли опыт рангам
    for rank_name, rank_data in ranks.items():
        max_exp = rank_data['max_exp']
        if exp >= max_exp:
            # Удаляем все роли пользователя
            await user.roles.clear()
            # Получаем роль, соответствующую рангу
            rank_role = discord.utils.get(user.guild.roles, name=rank_data['role_name'])
            if rank_role:
                # Добавляем роль, соответствующую рангу
                await user.add_roles(rank_role)
                await user.send(f'Поздравляю! Вы достигли ранга "{rank_name}".')
            break
 
# Обработчик событий на сообщения
@bot.event
async def on_message(message):
    # Игнорируем сообщения бота
    if message.author.bot:
        return

    # Получаем пользователя и его опыт
    user = message.author
    exp = user_exp.get(user.id, 0)

    # Увеличиваем опыт пользователя на основе количества слов в сообщении
    exp += len(message.content.split())

    # Обновляем опыт пользователя и роли на основе его опыта
    user_exp[user.id] = exp
    await update_user_rank(user)

    # Продолжаем обработку других команд и событий
    await bot.process_commands(message)    
    
# Команда, которая добавляет текст на изображение
@bot.command()
async def ранг(ctx):
    try:
        user = ctx.author  # Получаем пользователя, вызвавшего команду
        
        # Проверяем, есть ли пользователь в словаре опыта, если нет, то добавляем его
        if user.id not in user_exp:
            user_exp[user.id] = 0

        # Получаем текущий опыт пользователя
        exp = user_exp[user.id]
        
        current_rank = None
        next_rank = None
        for rank_name, rank_data in ranks.items():
            max_exp = rank_data['max_exp']
            if exp >= max_exp:
                current_rank = rank_name
                if rank_name == 'Опытный':
                    exp = max_exp
                next_rank_data = ranks.get(list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1])
                if next_rank_data:
                    next_rank = list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1]
                break  # Перемещаем оператор break внутрь цикла

        
        avatar_url = user.avatar.url  # Получаем URL аватарки пользователя
        response = requests.get(avatar_url)  # Загружаем аватарку по URL
        avatar = Image.open(BytesIO(response.content))  # Открываем аватарку как изображение
        avatar = avatar.resize((256, 256))  # Масштабируем аватарку до 128x128 пикселей

        # Создаем маску с закругленными углами
        mask = Image.new('L', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((20, 20, avatar.size[0], avatar.size[1]), fill=255)

        # Применяем маску к аватарке
        avatar.putalpha(mask)
        
        # Загружаем изображение с рамкой
        frame_url = 'https://www.onlygfx.com/wp-content/uploads/2017/11/grunge-circle-frame-2.png'  # Замените ссылку на URL изображения с рамкой
        frame_response = requests.get(frame_url)
        frame = Image.open(BytesIO(frame_response.content))
        frame = frame.resize((256,256))

        image = Image.new('RGB', (1200, 400), (255, 255, 255))  # Создаем новое изображение размером 600x200 с белым фоном
        draw = ImageDraw.Draw(image)
        
        font_name = ImageFont.truetype('arial.ttf', 50)  # Выбираем шрифт и размер текста
        font_exp = ImageFont.truetype('arial.ttf', 48)  # Выбираем шрифт и размер текста
        
        draw.text((430, 20), user.name, fill='black', font=font_name)  # Добавляем текст на изображение с черным цветом
        
        draw.text((300, 200), f'Опыт: {exp}/{max_exp}', fill='black', font=font_exp)  # Добавляем текст на изображение с черным цветом
        
        image.paste(avatar, (20, 70), mask=avatar)  # Добавляем аватарку на изображение с использованием маски
        image.paste(frame, (30, 75), mask=frame)
        image.save('output.png')  # Сохраняем изображение в формате PNG
        await ctx.reply(file=discord.File('output.png'))  # Отправляем изображение на сервер
    except Exception as e:
        await ctx.reply(f'Произошла ошибка: {e}')
#---End Command---#
        

@bot.command()
async def ранг(ctx):
@bot.command()
async def ранг(ctx):
    try:
        user = ctx.author  # Получаем пользователя, вызвавшего команду
        
        # Проверяем, есть ли пользователь в словаре опыта, если нет, то добавляем его
        if user.id not in user_exp:
            user_exp[user.id] = 0

        # Получаем текущий опыт пользователя
        exp = user_exp[user.id]
        
        current_rank = None
        next_rank = None
        for rank_name, rank_data in ranks.items():
            max_exp = rank_data['max_exp']
            if exp >= max_exp:
                current_rank = rank_name
                if rank_name == 'Опытный':
                    exp = max_exp
                next_rank_data = ranks.get(list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1])
                if next_rank_data:
                    next_rank = list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1]
                break  # Перемещаем оператор break внутрь цикла

        
        avatar_url = user.avatar.url  # Получаем URL аватарки пользователя
        response = requests.get(avatar_url)  # Загружаем аватарку по URL
        avatar = Image.open(BytesIO(response.content))  # Открываем аватарку как изображение
        avatar = avatar.resize((256, 256))  # Масштабируем аватарку до 128x128 пикселей

        # Создаем маску с закругленными углами
        mask = Image.new('L', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((20, 20, avatar.size[0], avatar.size[1]), fill=255)

        # Применяем маску к аватарке
        avatar.putalpha(mask)
        
        # Загружаем изображение с рамкой
        frame_url = 'https://www.onlygfx.com/wp-content/uploads/2017/11/grunge-circle-frame-2.png'  # Замените ссылку на URL изображения с рамкой
        frame_response = requests.get(frame_url)
        frame = Image.open(BytesIO(frame_response.content))
        frame = frame.resize((256,256))

        image = Image.new('RGB', (1200, 400), (255, 255, 255))  # Создаем новое изображение размером 600x200 с белым фоном
        draw = ImageDraw.Draw(image)
        
        font_name = ImageFont.truetype('arial.ttf', 50)  # Выбираем шрифт и размер текста
        font_exp = ImageFont.truetype('arial.ttf', 48)  # Выбираем шрифт и размер текста
        
        draw.text((430, 20), user.name, fill='black', font=font_name)  # Добавляем текст на изображение с черным цветом
        
        draw.text((300, 200), f'Опыт: {exp}/{max_exp}', fill='black', font=font_exp)  # Добавляем текст на изображение с черным цветом
        
        image.paste(avatar, (20, 70), mask=avatar)  # Добавляем аватарку на изображение с использованием маски
        image.paste(frame, (30, 75), mask=frame)
        image.save('output.png')  # Сохраняем изображение в формате PNG
        await ctx.reply(file=discord.File('output.png'))  # Отправляем изображение на сервер
    except Exception as e:
        await ctx.reply(f'Произошла ошибка: {e}')

    #---End Command---#


@bot.command()
async def ранг(ctx):
@bot.command()
async def ранг(ctx):
    try:
        user = ctx.author  # Получаем пользователя, вызвавшего команду
        
        # Проверяем, есть ли пользователь в словаре опыта, если нет, то добавляем его
        if user.id not in user_exp:
            user_exp[user.id] = 0

        # Получаем текущий опыт пользователя
        exp = user_exp[user.id]
        
        current_rank = None
        next_rank = None
        for rank_name, rank_data in ranks.items():
            max_exp = rank_data['max_exp']
            if exp >= max_exp:
                current_rank = rank_name
                if rank_name == 'Опытный':
                    exp = max_exp
                next_rank_data = ranks.get(list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1])
                if next_rank_data:
                    next_rank = list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1]
                break  # Перемещаем оператор break внутрь цикла

        
        avatar_url = user.avatar.url  # Получаем URL аватарки пользователя
        response = requests.get(avatar_url)  # Загружаем аватарку по URL
        avatar = Image.open(BytesIO(response.content))  # Открываем аватарку как изображение
        avatar = avatar.resize((256, 256))  # Масштабируем аватарку до 128x128 пикселей

        # Создаем маску с закругленными углами
        mask = Image.new('L', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((20, 20, avatar.size[0], avatar.size[1]), fill=255)

        # Применяем маску к аватарке
        avatar.putalpha(mask)
        
        # Загружаем изображение с рамкой
        frame_url = 'https://www.onlygfx.com/wp-content/uploads/2017/11/grunge-circle-frame-2.png'  # Замените ссылку на URL изображения с рамкой
        frame_response = requests.get(frame_url)
        frame = Image.open(BytesIO(frame_response.content))
        frame = frame.resize((256,256))

        image = Image.new('RGB', (1200, 400), (255, 255, 255))  # Создаем новое изображение размером 600x200 с белым фоном
        draw = ImageDraw.Draw(image)
        
        font_name = ImageFont.truetype('arial.ttf', 50)  # Выбираем шрифт и размер текста
        font_exp = ImageFont.truetype('arial.ttf', 48)  # Выбираем шрифт и размер текста
        
        draw.text((430, 20), user.name, fill='black', font=font_name)  # Добавляем текст на изображение с черным цветом
        
        draw.text((300, 200), f'Опыт: {exp}/{max_exp}', fill='black', font=font_exp)  # Добавляем текст на изображение с черным цветом
        
        image.paste(avatar, (20, 70), mask=avatar)  # Добавляем аватарку на изображение с использованием маски
        image.paste(frame, (30, 75), mask=frame)
        image.save('output.png')  # Сохраняем изображение в формате PNG
        await ctx.reply(file=discord.File('output.png'))  # Отправляем изображение на сервер
    except Exception as e:
        await ctx.reply(f'Произошла ошибка: {e}')

    #---End Command---#



@bot.command()
async def ранг(ctx):
@bot.command()
async def ранг(ctx):
    try:
        user = ctx.author  # Получаем пользователя, вызвавшего команду
        
        # Проверяем, есть ли пользователь в словаре опыта, если нет, то добавляем его
        if user.id not in user_exp:
            user_exp[user.id] = 0

        # Получаем текущий опыт пользователя
        exp = user_exp[user.id]
        
        current_rank = None
        next_rank = None
        for rank_name, rank_data in ranks.items():
            max_exp = rank_data['max_exp']
            if exp >= max_exp:
                current_rank = rank_name
                if rank_name == 'Опытный':
                    exp = max_exp
                next_rank_data = ranks.get(list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1])
                if next_rank_data:
                    next_rank = list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1]
                break  # Перемещаем оператор break внутрь цикла

        
        avatar_url = user.avatar.url  # Получаем URL аватарки пользователя
        response = requests.get(avatar_url)  # Загружаем аватарку по URL
        avatar = Image.open(BytesIO(response.content))  # Открываем аватарку как изображение
        avatar = avatar.resize((256, 256))  # Масштабируем аватарку до 128x128 пикселей

        # Создаем маску с закругленными углами
        mask = Image.new('L', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((20, 20, avatar.size[0], avatar.size[1]), fill=255)

        # Применяем маску к аватарке
        avatar.putalpha(mask)
        
        # Загружаем изображение с рамкой
        frame_url = 'https://www.onlygfx.com/wp-content/uploads/2017/11/grunge-circle-frame-2.png'  # Замените ссылку на URL изображения с рамкой
        frame_response = requests.get(frame_url)
        frame = Image.open(BytesIO(frame_response.content))
        frame = frame.resize((256,256))

        image = Image.new('RGB', (1200, 400), (255, 255, 255))  # Создаем новое изображение размером 600x200 с белым фоном
        draw = ImageDraw.Draw(image)
        
        font_name = ImageFont.truetype('arial.ttf', 50)  # Выбираем шрифт и размер текста
        font_exp = ImageFont.truetype('arial.ttf', 48)  # Выбираем шрифт и размер текста
        
        draw.text((430, 20), user.name, fill='black', font=font_name)  # Добавляем текст на изображение с черным цветом
        
        draw.text((300, 200), f'Опыт: {exp}/{max_exp}', fill='black', font=font_exp)  # Добавляем текст на изображение с черным цветом
        
        image.paste(avatar, (20, 70), mask=avatar)  # Добавляем аватарку на изображение с использованием маски
        image.paste(frame, (30, 75), mask=frame)
        image.save('output.png')  # Сохраняем изображение в формате PNG
        await ctx.reply(file=discord.File('output.png'))  # Отправляем изображение на сервер
    except Exception as e:
        await ctx.reply(f'Произошла ошибка: {e}')

    #---End Command---#


bot.run(config['token'])
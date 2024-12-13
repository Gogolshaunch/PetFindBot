import asyncio
import logging
import sys
from aiogram.methods.send_photo import SendPhoto
from aiogram import Bot, Dispatcher
from aiogram.types import *
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dataclasses import dataclass
import os
from edu import selection2
from dbase import new_human, count_person, del_person 

person = {} 

@dataclass  
class Person:     
    status: int
    name: str = None      
    phonenumber: str = None  
    city: str = None     
    tg_user: str = None  
    type_pet: str = None      
    name_pet: str = None  
    sex_pet: int = 0      
    breed_pet: str = None  
    describe: str = None      
    photo: str = None  


TOKEN = os.getenv("7820363449:AAFeXrpI9CBY1kG7EIFMYlWw4wS-ydA1x_s")
dp = Dispatcher()


class SG(StatesGroup):   
    status = State()      
    name = State()  
    phonenumber = State()      
    city = State() 
    type_pet = State()      
    name_pet = State()  
    sex_pet = State()      
    breed_pet = State()  
    describe = State()   


@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext):
    await msg.answer('Здравствуйте. Мне жаль, что вам пришлось обратиться ко мне, но я помогу решить вашу проблему. /nДля начала заполним анкету, пожалуйста отвечайте на вопросы без лишней информации и прямо, чтобы мне было легче помочь вам, если вы не знаете, что ответить, то пишите "не знаю". Если остались вопросы по заполнению - /info. /nИтак, вы владелец питомца или нашедший?')  
    if msg.chat.id in person:
        if count_person(person.status) != 0:
            out = selection2(person)
            if len(out) == 0: 
                await msg.answer('Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, обратитесь попозже')
            else:
                await msg.answer(f'Я нашел подходящие анкеты. Количество: {len(out)}. Вот:')
                for i in out:
                    await msg.send_photo(msg.chat.id, photo=i.photo, caption=f'Имя пользователя:{i.name}/nНомер телефона:{i.phonenumber}/nТелеграм юзер:{i.tg_user}/nГород:{i.city}/nЖивотное:{i.type_pet}/nИмя питомца:{i.name_pet}/nОписание:{i.decribe}')
                    await msg.answer(msg.chat.id, 'Надеюсь я смог вам помочь! Если вы смогли вернуть питомца домой, то удалите свое объявление /del. Если же нет, то попробуйте чуть-чуть попозже, вдруг человек еще не выложил объявление!')  
        else:
            await msg.answer(msg.chat.id, 'Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, обратитесь попозже')   
    else:    
        person[msg.chat.id] = Person(tg_user=msg.from_user.username)  
        await SG.status.set()    

@dp.message(commands=['info'])  
async def info(msg: Message):  
    await msg.answer(f'Пример ожидаемых ответов:/nСтатус: Владелец/nИмя и фамилия: Иванов Артем/nНомер телефона:89324445555/nГород:Сургут/nЖивотное: Собака/nИмя питомца: Дружок/nПол: Мужской/nПорода: Овчарка/nОписание: 3 декабря убежал со двора, не агрессивный и пугливый. Белые лапки и грудка, довольно крупный. Был в ошейнике')   

@dp.message(commands=['del'])  
async def delete(msg: Message):  
    if msg.chat.id in person:
        del_person(person[msg.chat.id], msg.chat.id)
        await msg.answer('Отлично, ваше объявление удалено!')
    else:
        await msg.answer('Для начала заполните анкету!')

@dp.message(state=SG.status)   
async def status(msg: Message, state: FSMContext):   
    if ('шел' in msg.lower() or 'шёл' in msg.lower() or 'второе' in msg.lower()) and len(msg) != 0:           
        person[msg.chat.id].status = 1  
    else:          
        person[msg.chat.id].status = 0  
    await state.finish()      
    await msg.answer('Ваше имя и фамилия:')  
    await SG.name.set()    

@dp.message(state=SG.name)   
async def name(msg: Message, state: FSMContext):   
    if len(msg) != 0:           
        person[msg.chat.id].name = msg  
    await state.finish()      
    await msg.answer('Ваш актуальный номер телефона:')  
    await SG.phonenumber.set()
    if len(msg) == 11:           
        person[msg.chat.id].phonenumber = msg  
        await state.finish()          
        await msg.answer('В каком вы городе?')  
        await SG.city.set()      
    else: 
        await msg.answer('Некорректный номер телефона')   

@dp.message(state=SG.city)   
async def city(msg: Message, state: FSMContext):   
    if len(msg) != 0:           
        person[msg.chat.id].city = msg  
    await state.finish()      
    await msg.answer('Какое животное вы нашли/потеряли?')  
    await SG.type_pet.set()   

@dp.message(state=SG.type_pet)   
async def type_pet(msg: Message, state: FSMContext):   
    if ('не знаю' not in msg.lower() or 'извест' not in msg.lower()) and len(msg) != 0:           
        person[msg.chat.id].type_pet = msg  
    await state.finish()      
    await msg.answer('Как зовут питомца?')  
    await SG.name_pet.set()    

@dp.message(state=SG.name_pet)   
async def name_pet(msg: Message, state: FSMContext):   
    if ('не знаю' not in msg.lower() or 'извест' not in msg.lower()) and len(msg) != 0:           
        person[msg.chat.id].name_pet = msg
    await state.finish()      
    await msg.answer('Пол питомца?')  
    await SG.sex_pet.set()   

@dp.message(state=SG.sex_pet)   
async def sex_pet(msg: Message, state: FSMContext):   
    if msg[0].lower() == 'ж' and len(msg) != 0:           
        person[msg.chat.id].sex_pet = 1  
    await state.finish()      
    await msg.answer('Порода питомца?')  
    await SG.breed_pet.set()    

@dp.message(state=SG.breed_pet)   
async def breed_pet(msg: Message, state: FSMContext):   
    if ('не знаю' not in msg.lower() or 'извест' not in msg.lower()) and len(msg) != 0:           
        person[msg.chat.id].breed_pet = msg  
    await state.finish()      
    await msg.answer('Поделитесь подробности (где, когда и во сколько вы нашли\потеряли питомца, особенности и отличительные черты питомцы и тд)')  
    await SG.describe.set()    

@dp.message(state=SG.describe)   
async def describe(msg: Message, state: FSMContext):   
    if len(msg) != 0:          
        person[msg.chat.id].describe = msg  
    await state.finish()      
    await msg.answer('Мы почти закончили. Отправьте фотографию питомца')  

@dp.message(content_types=['photo'])  
async def process_photo(msg: Message, state: FSMContext):          
    photo = msg.photo 
    if len(photo) != 1:
        photo = photo[0]             
    photo_file = await dp.get_file(photo.file_id) 

    if not os.path.exists('d_photo'):                 
        os.makedirs('d_photo') 

    photo_path = os.path.join('d_photo', f'{msg.message_id}.jpg')             
    person[msg.chat.id].photo = photo_path 
    await photo_file.download (photo_path)         
    await msg.answer('Все! Не беспокойтесь, уже ищу подходящие анкеты! Подождите пожалуйста!') 
    new_human(person[msg.chat.id], msg.chat.id) 
    if count_person(person.status) != 0:
        out = selection2(person)
        if len(out) == 0: 
            await msg.answer('Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, обратитесь попозже')
        else:
            await msg.answer(f'Я нашел подходящие анкеты. Количество: {len(out)}. Вот:')
            for i in out:
                await msg.send_photo(msg.chat.id, photo=i.photo, caption=f'Имя пользователя:{i.name}/nНомер телефона:{i.phonenumber}/nТелеграм юзер:{i.tg_user}/nГород:{i.city}/nЖивотное:{i.type_pet}/nИмя питомца:{i.name_pet}/nОписание:{i.decribe}')
                await msg.answer('Надеюсь я смог вам помочь! Если вы смогли вернуть питомца домой, то удалите свое объявление /del. Если же нет, то попробуйте чуть-чуть попозже, вдруг человек еще не выложил объявление!')  

    else:
        await msg.answer('Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, обратитесь попозже')    

@dp.message(content_types=['text'])  
async def get_text_messages(msg: Message):  
   await msg.answer('Не понимаю вас, ожидайте ответа')  

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
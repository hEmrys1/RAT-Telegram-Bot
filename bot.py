# coding=<utf-8>
import config
import telebot
from telebot import types
import requests
import os
import time
import pyautogui as pag
import platform as pf
import clr

my_id = config.user_id
bot = telebot.TeleBot(config.TOKEN)

openhardwaremonitor_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster',
                               'HDD']
openhardwaremonitor_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level',
                                   'Factor', 'Power', 'Data', 'SmallData']

commands_msg = '''
Вот мой список команд:

⚠️*Питание*
/shut - меню выключения
/restart - меню перезагрузки

🌡*Мониторинг ресурсов*
/temperature - меню температур

📌*Другое*
/spec - информация о пк и пользователе
/screenshot - сделать скриншот экрана (low quality)

🛠*Настройка*
/help - настройка бота
'''

help_msg = '''
Инструкция по настройке бота.

1. Перейдем в телеграм, в поиске найдем @BotFather. Командой /newbot создадим бота, указав сначала имя бота, затем его логин.
2. BotFather выдаст API нашего бота (Пример: 1769225647:ABHQQeGpHrg5ehKg12dUi7Ieg-8U93GqAUp), его нужно сохранить.
3. В поиске найдем еще одного бота @ShowJsonBot. Напишем ему любое сообщение, он отправит нам данные. Нужно найти и скопировать значение поля id (message : from : id).
4. В файл config.py поместим полученные данные (API бота и ваш id) и сохраним изменения.
5. С сайта OpenHardwareMonitor скачиваем утилиту [ТЫК](https://openhardwaremonitor.org/downloads/). Из всех файлов нам нужен *ТОЛЬКО* OpenHardwareMonitorLib.dll. Перекидываем его в папку с ботом.
6. Теперь создадим .exe файл нашего бота. Для этого понадобится Python [ТЫК](https://www.python.org/downloads/). Скачиваем и устанавливаем. Очень важно поставить галочку *add python to path*.
7. Открываем cmd, переходим в директорию с ботом и выполняем _pyinstaller -w -F bot.py_. Должен создаться .exe файл нашего бота в папке dist.
8. Перекидываем его из dist в корневую папку с ботом. Затем создаем ярлык .exe файла и помещаем в папку автозагрузки (C:\\Users\\ИмяПользователя\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup).
'''

# MARKUPS
back_btn = types.KeyboardButton("⏪Назад")

# main menu
rmk_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
menu_cmds = types.KeyboardButton("⚙️Список команд")
menu_help = types.KeyboardButton("🆘Помощь")
menu_power = types.KeyboardButton("⚠️Управление питанием")
menu_temperature = types.KeyboardButton("🌡Мониторинг ресурсов")
menu_addl = types.KeyboardButton("📌Другое")
rmk_menu.row(menu_cmds, menu_help)
rmk_menu.row(menu_power, menu_temperature)
rmk_menu.row(menu_addl)

# additional menu
rmk_addl = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
info_btn = types.KeyboardButton("🔎Информация")
screen_btn = types.KeyboardButton("📷Сделать скриншот")
rmk_addl.row(info_btn, screen_btn)
rmk_addl.row(back_btn)

# power
rkm_power = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
custom_btn = types.KeyboardButton("🕹Своя команда")
shut_btn = types.KeyboardButton("🔴Выключение")
rs_btn = types.KeyboardButton("♻️Перезагрузка")
rkm_power.row(custom_btn)
rkm_power.row(shut_btn, rs_btn)
rkm_power.row(back_btn)

# shut
rmk_shut = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
shut_now = types.KeyboardButton("shut now")
shut_cancel = types.KeyboardButton("shut cancel")
shut_5 = types.KeyboardButton("shut5")
shut_10 = types.KeyboardButton("shut10")
rmk_shut.row(shut_now, shut_cancel)
rmk_shut.row(shut_5, shut_10)
rmk_shut.row(back_btn)

# restart
rmk_restart = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
rs_now = types.KeyboardButton("restart now")
rs_cancel = types.KeyboardButton("restart cancel")
rs_5 = types.KeyboardButton("restart5")
rs_10 = types.KeyboardButton("restart10")
rmk_restart.row(rs_now, rs_cancel)
rmk_restart.row(rs_5, rs_10)
rmk_restart.row(back_btn)

# temperatures
rmk_temp = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
temp_all = types.KeyboardButton("🔑Показать все")
temp_gpu = types.KeyboardButton("🌡Видеокарта")
temp_cpu = types.KeyboardButton("🌡Процессор")
rmk_temp.row(temp_all)
rmk_temp.row(temp_gpu, temp_cpu)
rmk_temp.row(back_btn)

# при подключении бота, он напишет сообщение "Online, время запуска"
seconds = time.time()
time_now = time.ctime(seconds)
online_post_message = f"Online\n{time_now}"
bot.send_message(my_id, online_post_message, reply_markup=rmk_menu)


# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    hello_msg = "👋 Я помогу в управлении твоим компьютером.\nПеред началом использования убедись, что все условия выполнены."
    bot.send_message(message.chat.id, hello_msg, reply_markup=rmk_menu)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, help_msg, parse_mode="markdown")


@bot.message_handler(commands=['spec'])
def spec(message):
    pc_name = pf.node()
    req = requests.get('https://ip.42.pl/raw')
    ip = req.text
    uname = os.getlogin()
    bot.send_message(message.chat.id, f"*Пользователь:* {uname}\n*PC Name:* {pc_name}\n*IP:* {ip}\n",
                     parse_mode="markdown")


@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    pag.screenshot("000.jpg")
    with open("000.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['shut'])
def shut_main(message):
    bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=rmk_shut)
    bot.register_next_step_handler(message, shut_action)


@bot.message_handler(commands=['restart'])
def restart_main(message):
    bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=rmk_restart)
    bot.register_next_step_handler(message, restart_action)


@bot.message_handler(commands=['temperature'])
def restart_main(message):
    bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=rmk_temp)
    bot.register_next_step_handler(message, temperature_action)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.from_user.id == my_id:
        if message.text == "⚙️Список команд":
            bot.send_message(message.chat.id, commands_msg, parse_mode="markdown")

        elif message.text == "🆘Помощь":
            bot.send_message(message.chat.id, help_msg, parse_mode="markdown")

        elif message.text == "⚠️Управление питанием":
            bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=rkm_power)
            bot.register_next_step_handler(message, power_action)

        elif message.text == "🌡Мониторинг ресурсов":
            bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=rmk_temp)
            bot.register_next_step_handler(message, temperature_action)

        elif message.text == "📌Другое":
            bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=rmk_addl)
            bot.register_next_step_handler(message, addl_action)


def power_action(message):
    if message.from_user.id == my_id:
        if message.text == "🔴Выключение":
            bot.send_message(message.chat.id, "Выключение", reply_markup=rmk_shut)
            bot.register_next_step_handler(message, shut_action)

        elif message.text == "♻️Перезагрузка":
            bot.send_message(message.chat.id, "Перезагрузка", reply_markup=rmk_restart)
            bot.register_next_step_handler(message, restart_action)

        elif message.text == "🕹Своя команда":
            bot.send_message(message.chat.id, "Пожалуйста, введите команду...")
            bot.register_next_step_handler(message, custom_action)

        elif message.text == "⏪Назад":
            bot.send_message(message.chat.id, "Главное меню.", reply_markup=rmk_menu)
            bot.register_next_step_handler(message, text_handler)

        else:
            bot.send_message(message.chat.id,
                             "❗️Не является внутренней командой. Пожалуйста, выберите одну из предложенных.")
            bot.register_next_step_handler(message, power_action)
    else:
        error_rights(message)


def shut_action(message):
    if message.from_user.id == my_id:
        if message.text == "shut cancel":
            bot.send_message(message.chat.id, "Выключение отменено.")
            os.system('shutdown -a')
            bot.register_next_step_handler(message, shut_action)

        elif message.text == "shut now":
            bot.send_message(message.chat.id, "Выполняется выключение.")
            os.system('shutdown -s -t 0 -f')         
            bot.register_next_step_handler(message, shut_action)

        elif message.text == "shut5":
            bot.send_message(message.chat.id, "Выключение будет выполнено через 5 минут.")
            os.system('shutdown -s -t 300')
            bot.register_next_step_handler(message, shut_action)

        elif message.text == "shut10":
            bot.send_message(message.chat.id, "Выключение будет выполнено через 10 минут.")
            os.system('shutdown -s -t 600')
            bot.register_next_step_handler(message, shut_action)

        elif message.text == "⏪Назад":
            bot.send_message(message.chat.id, "Главное меню.", reply_markup=rmk_menu)
            bot.register_next_step_handler(message, text_handler)

        else:
            bot.send_message(message.chat.id,
                             "❗️Не является внутренней командой. Пожалуйста, выберите одну из предложенных.")
            bot.register_next_step_handler(message, shut_action)
    else:
        error_rights(message)


def restart_action(message):
    if message.from_user.id == my_id:
        if message.text == "restart cancel":
            bot.send_message(message.chat.id, "Перезагрузка отменена.")
            os.system('shutdown -a')
            bot.register_next_step_handler(message, restart_action)

        elif message.text == "restart now":
            bot.send_message(message.chat.id, "Выполняется перезагрузка.")
            os.system('shutdown -r -t 0 -f')
            bot.register_next_step_handler(message, restart_action)

        elif message.text == "restart5":
            bot.send_message(message.chat.id, "Перезагрузка будет выполнена через 5 минут.")
            os.system('shutdown -r -t 300')
            bot.register_next_step_handler(message, restart_action)

        elif message.text == "restart10":
            bot.send_message(message.chat.id, "Перезагрузка будет выполнена через 10 минут.")
            os.system('shutdown -r -t 600')
            bot.register_next_step_handler(message, restart_action)

        elif message.text == "⏪Назад":
            bot.send_message(message.chat.id, "Главное меню.", reply_markup=rmk_menu)
            bot.register_next_step_handler(message, text_handler)

        else:
            bot.send_message(message.chat.id,
                             "❗️Не является внутренней командой. Пожалуйста, выберите одну из предложенных.")
            bot.register_next_step_handler(message, restart_action)
    else:
        error_rights(message)


def custom_action(message):
    if message.from_user.id == my_id:
        try:
            os.system(message.text)
            bot.send_message(message.chat.id, "Успех!")
            bot.register_next_step_handler(message, power_action)
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так...")
    else:
        error_rights(message)


def temperature_action(message):
    if message.from_user.id == my_id:
        if message.text == "🔑Показать все":
            bot.send_message(message.chat.id, "Пожалуйста, подождите...")
            fetch_stats(HardwareHandle)
            for msg in output_list:
                bot.send_message(message.chat.id, msg)
            output_list.clear()
            bot.register_next_step_handler(message, temperature_action)

        elif message.text == "🌡Видеокарта":
            bot.send_message(message.chat.id, "Пожалуйста, подождите...")
            fetch_stats_gpu(HardwareHandle)
            for msg in output_list_gpu:
                bot.send_message(message.chat.id, msg)
            output_list_gpu.clear()
            bot.register_next_step_handler(message, temperature_action)

        elif message.text == "🌡Процессор":
            bot.send_message(message.chat.id, "Пожалуйста, подождите...")
            fetch_stats_cpu(HardwareHandle)
            for msg in output_list_cpu:
                bot.send_message(message.chat.id, msg)
            output_list_cpu.clear()
            bot.register_next_step_handler(message, temperature_action)

        elif message.text == "⏪Назад":
            bot.send_message(message.chat.id, "Главное меню.", reply_markup=rmk_menu)
            bot.register_next_step_handler(message, text_handler)

        else:
            bot.send_message(message.chat.id,
                             "❗️Не является внутренней командой. Пожалуйста, выберите одну из предложенных.")
            bot.register_next_step_handler(message, temperature_action)
    else:
        error_rights(message)


def addl_action(message):
    if message.from_user.id == my_id:
        if message.text == "🔎Информация":
            pc_name = pf.node()
            req = requests.get('https://ip.42.pl/raw')
            ip = req.text
            uname = os.getlogin()
            bot.send_message(message.chat.id, f"*Пользователь:* {uname}\n*PC Name:* {pc_name}\n*IP:* {ip}\n",
                             parse_mode="markdown")
            bot.register_next_step_handler(message, addl_action)

        elif message.text == "📷Сделать скриншот":
            pag.screenshot("000.jpg")

            with open("000.jpg", "rb") as img:
                bot.send_photo(message.chat.id, img)

            bot.register_next_step_handler(message, addl_action)

        elif message.text == "⏪Назад":
            bot.send_message(message.chat.id, "Главное меню.", reply_markup=rmk_menu)
            bot.register_next_step_handler(message, text_handler)

        else:
            bot.send_message(message.chat.id,
                             "❗️Не является внутренней командой. Пожалуйста, выберите одну из предложенных.")
            bot.register_next_step_handler(message, temperature_action)
    else:
        error_rights(message)


output_list = []
output_list_cpu = []
output_list_gpu = []


def initialize_openhardwaremonitor():
    file = 'OpenHardwareMonitorLib'
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)


def fetch_stats_cpu(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor_cpu(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor_cpu(subsensor)


def fetch_stats_gpu(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor_gpu(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor_gpu(subsensor)


def parse_sensor(sensor):
    if sensor.Value is not None:
        if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
            sensortypes = openhardwaremonitor_sensortypes
            hardwaretypes = openhardwaremonitor_hwtypes
        else:
            return

        if sensor.SensorType == sensortypes.index('Temperature'):
            output_str = u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (
            hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value)
            output_list.append(output_str)


def parse_sensor_cpu(sensor):
    if sensor.Value is not None:
        if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
            sensortypes = openhardwaremonitor_sensortypes
            hardwaretypes = openhardwaremonitor_hwtypes
        else:
            return

        if sensor.SensorType == sensortypes.index('Temperature') and sensor.Name[:8] == "CPU Core":
            output_str = u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (
            hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value)
            output_list_cpu.append(output_str)


def parse_sensor_gpu(sensor):
    if sensor.Value is not None:
        if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
            sensortypes = openhardwaremonitor_sensortypes
            hardwaretypes = openhardwaremonitor_hwtypes
        else:
            return

        if sensor.SensorType == sensortypes.index('Temperature') and sensor.Name[:8] == "GPU Core":
            output_str = u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (
            hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value)
            output_list_gpu.append(output_str)


def error_rights(message):
    bot.send_message(message.chat.id, "Не достаточно прав для выполнения команды: " + message)


if __name__ == "__main__":
    HardwareHandle = initialize_openhardwaremonitor()
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        pass

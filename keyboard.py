from telebot import types
main_board = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
carcase1 = types.KeyboardButton('1 корпус')
carcase2 = types.KeyboardButton('2 корпус')
main_board.add(carcase1, carcase2)
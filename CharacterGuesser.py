import imageZoom,os,telebot,random,bingScraper
from dotenv import load_dotenv
import json
import time

img_path = "C:/Users/gabri/Downloads/CharacterGuesserBing/img/"
json_path = "C:/Users/gabri/Downloads/CharacterGuesserBing/characters.json"

load_dotenv()
TELE_TOKEN = os.getenv("TELE_TOKEN")

banned = ['of', 'the', 'jr', 'jr.']
difficulty_list = ['easy', 'medium', 'hard']
mode_list = ['none', 'blur', 'shuffle', 'grayscale', 'disappearing']

ORI_NAME = 'ori.jpg'
RES_NAME = 'res.jpg'

with open(json_path, 'r') as json_file:
    characters = json.load(json_file)
category_list = list(characters.keys())
print(category_list)

modes = {}
difficulties = {}
categories = {}
phases = {}
answers = {}
scores = {}
bot = telebot.TeleBot(TELE_TOKEN)

def delete_message(chat_id, message_id):
    time.sleep(0.3)
    bot.delete_message(chat_id=chat_id, message_id=message_id)

def check(guess, answer):
    for g in guess[:3]:
        if g not in banned and g in answer:
            return True
    return False
    
def generate(change = True, chat_id = "", category = "", difficulty = "medium", modes = []):
    num = random.randint(0,len(characters[category])-1)
    if change:
        answers[chat_id] = characters[category][num].lower()
        print(answers[chat_id])  
        urls = bingScraper.img_search(answers[chat_id])
        #+ " " + category
        bingScraper.create_img(urls)     
    imageZoom.create_zoomed_image(difficulty, modes)
    return open(img_path + RES_NAME, 'rb'), answers[chat_id]
    
def sendphoto(change = True, chat_id = "", difficulty = "medium", modes = []):
    img_f, answer = generate(change, chat_id, categories[chat_id], difficulty, modes)
    answers[chat_id] = answer
    photo = bot.send_photo(chat_id, img_f)
    img_f.close()
    if 'disappearing' in modes:
        delete_message(chat_id, photo.message_id)

@bot.message_handler(commands=['play'])
def play(message):
    chat_id = message.chat.id
    if chat_id not in phases:
        phases[chat_id] = 'play'
    if phases[chat_id] != 'play':
        bot.send_message(chat_id,"Game is currenly in play right now, try another command")
    else:
        new_message = "Let's play \"Guess the Character\".\nPlease choose the category using the command /choose category_number:\n"
        for i in range(len(category_list)):
            new_message += (str(i+1) + ". " + category_list[i] + '\n')
        bot.send_message(chat_id, new_message)
        phases[chat_id] = 'category'

@bot.message_handler(commands=['choose'])
def choose(message):
    chat_id = message.chat.id
    words = message.text.strip().split()
    if phases[chat_id] == 'play':
        bot.send_message(chat_id,'Game has not started, please use the /play command')
    elif phases[chat_id] not in ['category', 'difficulty', 'mode']:
        bot.send_message(chat_id,'Choice has already been made')
    else:
        choice = int(words[-1])-1
        if not words[-1].isnumeric():
            bot.send_message(chat_id,'Please enter a number as the choice')
        elif phases[chat_id] == 'category':
            if choice < 0 or choice >= len(category_list) or len(words) > 2:
                bot.send_message(chat_id,'Invalid choice, make another choice')
            else:
                categories[chat_id] = category_list[choice]
                phases[chat_id] = 'difficulty'
                new_message = "Choose the difficulty using /choose:\n"
                for i in range(len(difficulty_list)):
                    new_message += str(i+1) + "." + difficulty_list[i] + '\n'
                bot.send_message(chat_id, new_message)
        elif phases[chat_id] == 'difficulty': 
            if choice < 0 or choice >= len(difficulty_list) or len(words) > 2:
                bot.send_message(chat_id,'Invalid choice, make another choice')
            else:
                phases[chat_id] = 'mode'
                difficulties[chat_id] = difficulty_list[choice]
                new_message = "Choose the mode using /choose followed by the mode numbers separated by spaces:\n"
                for i in range(len(mode_list)):
                    new_message += str(i+1) + "." + mode_list[i] + '\n'
                bot.send_message(chat_id, new_message)
        else:
            choices = words[1:]
            modes_chosen = []
            for i in range(len(choices)):
                if not choices[i].isnumeric():
                    bot.send_message(chat_id,'Please enter a number as the choice')
                    return
                modes_chosen.append(mode_list[int(choices[i])-1])
            if 'none' in modes_chosen:
                modes_chosen = []
            modes[chat_id] = modes_chosen
            phases[chat_id] = "guess"
            sendphoto(chat_id=chat_id, difficulty=difficulties[chat_id], modes=modes[chat_id])


            

@bot.message_handler(commands=['guess'])
def guess(message):
    chat_id = message.chat.id
    if phases[chat_id] == 'guess':
        player_guess = message.text.lower().strip().split()[1:]
        print(player_guess)
        if check(player_guess, answers[chat_id]):
            bot.send_message(chat_id, message.from_user.first_name + " has won the game!")
            ori = open(img_path + ORI_NAME, 'rb')
            bot.send_photo(chat_id=chat_id, photo=ori, caption="The answer was " + ' '.join(answers[chat_id]))
            ori.close()
            sendphoto(chat_id=chat_id, difficulty=difficulties[chat_id], modes=modes[chat_id])
        else:
            bot.send_message(chat_id, "Wrong! Try again")
    elif phases[chat_id] in ['category', 'difficulty', 'mode']:
        bot.send_message(chat_id, "Please make a choice first")
    else:
        bot.send_message(chat_id,'Game has not started, please use the /play command')

@bot.message_handler(commands=['change', 'skip'])
def change(message):    
    chat_id = message.chat.id
    sendphoto(chat_id=chat_id, difficulty=difficulties[chat_id], modes=modes[chat_id])

@bot.message_handler(commands=['move', 'shuffle'])
def move(message):
    chat_id = message.chat.id
    sendphoto(False, chat_id, difficulties[chat_id], modes=modes[chat_id])

@bot.message_handler(commands=['quit', 'exit'])
def quit(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "The game has ended")

@bot.message_handler(func = lambda message: message.text.startswith('dumbass bot'))
def ip_dox(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "IP: 192.134.155.62")

@bot.message_handler(func = lambda message: message.text.startswith('yo wtf'))
def ip_dox(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "CVV: 254")

bot.infinity_polling()


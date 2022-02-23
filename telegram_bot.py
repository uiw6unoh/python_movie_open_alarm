import telegram

# bot 선언, token 넣기
bot = telegram.Bot(token = '5173563474:AAFj62H4OoH4sLyIOqXP-k7dLzpMaJUrCRY')

## bot에 대한 업데이트 내용 가져오기
#for i in bot.getUpdates():
#    print(i.message)

bot.sendMessage(chat_id = '1767897517', text = "테스트입니다.")
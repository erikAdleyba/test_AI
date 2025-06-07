from core.bot import ChatBot

def main():
    bot = ChatBot()
    
    print("🚗 Добро пожаловать в автосалон Premium Motors!")
    name = input("Ваше полное имя: ")
    query = input("Ваш запрос: ")
    
    response = bot.process_request(name, query)
    print("\n🤖 Ответ бота:")
    print(response)

if __name__ == "__main__":
    main()
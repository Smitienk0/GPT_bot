import openai

import config

conf = config.conf()                                        # тут есть переменные из config.json
def error_print(e):
    if(conf.print_DataUsers_errors):
                print("Произошла ошибка: ", e)
class ai:
    openai.api_key = conf.OpenAi_TOKEN
        
    def __init__(self,obj):
        self.comp = obj  

    def generate_response(self, prompt):                    # принимает историю сообщений для того чтобы сеть понимала контекст 
                                                            #  она выглядит так
                                                            #  [{"role": "user", "content": mass},      - сообщение пользователя
                                                            #   {"role": "assistant", "content": ret}]  - ответ сети

                                                            #
                                                            #
        try:                                                # создаеться запрос, в нем указывается подель и история сообщений 
            completion = self.comp.create(
            model="gpt-3.5-turbo", messages= prompt )
       
            return completion.choices[0].message.content    # возвращаем ответ сети
        
        except openai.error.InvalidRequestError as e:       # эта ошибка возникает если prompt больше 4000 токенов, нужно удалить из него первые сообщения 
            error_print(e)
            return 1
        except ValueError as e:                             # другие ошибки
            error_print(e)
            return 2
        except openai.error.OpenAIError as e:
            error_print(e)
            return 3
        except openai.error.AuthenticationError as e:
            error_print(e)
            return 4
        except Exception as e:
            error_print(e)
            return 5
   
    
class user_:                                                # тут есть имя - это айди чата по сути и история сообщений 

    def __init__(self) :
        self.name = ""
        self.storeg = []


class users_:
    
    def __init__(self) :
        try:
            self.musers = []                                # создаем массив в которм будут пользователи - users_()
            self.AI = ai(openai.ChatCompletion)
        except Exception as e:
            error_print(e)   

    def add_user(self,name):                                # если пользователя с таким именем нет созадаем его.
        try:
            i = 0
            for x in self.musers:
                if name == x.name:
                    
                    return 1
                i+=1
            
            us = user_()
        
            us.name = name
            
            self.musers.append(us)

            if(conf.print_messages):   
                        print( 'add user - '+str(name) )
        except Exception as e:
            error_print(e)
            
    def del_storeg(self,name):
        try:
            for x in self.musers:
                if name == x.name:
                    x.storeg = []
                    if(conf.print_messages):   
                        print( '/del '+str(name) )

                
        except Exception as e:
            error_print(e)
        
    def del_n_stor(self, stor):                             # удаляет около 20% символов из начала истории сообщений, если по одному их удалять то ответ сети прерываться будет
        
        l = 0
        lx = 0
        for x in stor:
            l+=len(x["content"])

        i = 0
        for x in stor:
            i+=1
            lx+=len(x["content"])
            if(lx >= l/5) :
                break        
        
        return stor[i:]
    

    def generate_response_user(self, name, mass):         
        i = 0
        for x in self.musers:                               # ищем пользователся по имени 
                                                            
            if name == x.name:
                req = {"role": "user", "content": mass}     # создаем запрос 

                self.musers[i].storeg.append(req)           # добавляем в историю сообщений 
                
                while 1:
                    ret = self.AI.generate_response(self.musers[i].storeg)   # передаем историю сообщений в сеть, если ошибка из за числа токенов то удаляем чать сообщений и пробуем заново.
                    if ret == 1:
                        try:
                            self.musers[i].storeg = self.del_n_stor( self.musers[i].storeg)  # удаляем часть сообщений 
                        except Exception as e:
                            error_print(e)
                            break

                    elif ret == 2 or ret == 3 or ret == 4 or ret == 5  :
                        return "неизвесная ошибка запроса, повторите попытку"
                    else:
                       
                        
                        ans = {"role": "assistant", "content": ret}     # если ошибок нет то добавляем ответ в историю сообщений 
                        self.musers[i].storeg.append(ans)
                        break
                
               
                return ret  
            i+=1
        
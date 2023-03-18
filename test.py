import openai
import config

class ai:
    openai.api_key = "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"
    comp = 0
    max_tokens = 1024
    n=1
    stop = None
    temperature = 0.5
    
    def __init__(self,obj):
        self.comp = obj  
        print('new')
    def generate_response(self, prompt):
        
        try:
            completion = self.comp.create(
            model="gpt-3.5-turbo", messages= prompt )
       
            return completion.choices[0].message.content
        except openai.error.InvalidRequestError as e:
            print("Произошла ошибка: ", e)
            return 1
        except ValueError as e:
            print("Произошла ошибка: ", e)
            return 2
        except openai.error.OpenAIError as e:
            print("Произошла ошибка: ", e)
            return 3
        except openai.error.AuthenticationError as e:
            print("Произошла ошибка: ", e)
            return 4
        except Exception as e:
            print("Произошла ошибка: ", e)
            return 5
   
        
class user_:
    bd = 0
    name = ""
    stor = []
    chat = 0
    def __init__(self) :
        self.name = ""
        self.stor = []

    def set_chat(self, chat):
        self.chat = chat

class users_:
   
    musers = []
    userneme = []

   

    def add_user(self,name):
       
        i = 0
        for x in self.userneme:
            if name == x:
                
                return 1
            i+=1./s
       
        
        print("add  "+str(name))
        usx = user_()
         
        usx.name = name
        usx.stor = []
        usx.chat = ai(openai.ChatCompletion)
        self.userneme.append(name)
        self.musers.append(usx)
           
    def del_n_stor(self, stor):
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

        print(str(l),"  ",str(lx),"  ",str(i),"  ")
        return stor[i:]
    

    def generate_response_user(self, name, mass):
        i = 0
        for x in self.userneme:
            
            if name == x:
                zz = {"role": "user", "content": mass}

                self.musers[i].stor.append(zz)
                
                while 1 == 1:
                    ret = self.musers[i].chat.generate_response(self.musers[i].stor)
                    if ret == 1:
                        
                        self.musers[i].stor = self.del_n_stor( self.musers[i].stor)

                    elif ret == 2 or ret == 3 or ret == 4 or ret == 5  :
                        return "неизвесная ошибка запроса, повторите попытку"
                    else:
                       
                        
                        zz = {"role": "assistant", "content": ret}
                        self.musers[i].stor.append(zz)
                        break
                
               
                return ret
            i+=1
            



us = users_()


us.add_user(111)

while 1==1:
    mass = input(" >> ")
    if mass[0] == '/':
        if mass == '/stop':
            input()
            break 
        if mass == '/stor':
            print(us.musers[0].stor)
        if mass == '/min':
            us.del_n_stor(us.musers[0].stor)
    else:       
        xx = us.generate_response_user(111,str(mass))
        print(" << " + str(xx))
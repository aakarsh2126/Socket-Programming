from Tkinter import *
import pickle
import random
from simple_aes_cipher import AESCipher,generate_secret_key
from socket import *
from threading import *
from ScrolledText import*
class AES:
    pass_phrase=""
    i=0
    while i<32:
        if i%2==0:        
            pass_phrase+="1"
        else:
            pass_phrase+="0"
        i+=1;
    secret_key=generate_secret_key(pass_phrase)
    cipher=AESCipher(secret_key)
    raw_text=""
    encrypt_text=""
class Receive():
  def __init__(self,server,gettext):
    #Thread.__init__(self)
    self.server=server
    self.gettext=gettext
    while 1:
      try:
        text=self.server.recv(1024)
        data_variable=pickle.loads(text)
#        if not data_variable.encrypt_text: break
        self.gettext.configure(state=NORMAL)
        decrypted_text=data_variable.cipher.decrypt(data_variable.encrypt_text)
        self.gettext.insert(END,'client >> %s\n'%decrypted_text)
        self.gettext.configure(state=DISABLED)
        self.gettext.see(END)
      except:
        break
class App(Thread):
  server=socket()
  server.bind(('localhost',input("Port : ")))
  server.listen(5)
  client,addr=server.accept()
  def __init__(self,master):
    Thread.__init__(self)
    frame=Frame(master)
    frame.pack()
    self.gettext=ScrolledText(frame,height=10,width=100,state=NORMAL)
    self.gettext.pack()
    sframe=Frame(frame)
    sframe.pack(anchor='w')
    self.pro=Label(sframe,text="Server>>");
    self.sendtext=Entry(sframe,width=80)
    self.sendtext.focus_set()
    self.sendtext.bind(sequence="<Return>",func=self.Send)
    self.pro.pack(side=LEFT)
    self.sendtext.pack(side=LEFT)
    self.gettext.insert(END,'Welcome to Chat\n')
    self.gettext.configure(state=DISABLED)
  def Send(self, args):
    self.gettext.configure(state=NORMAL)
    text=self.sendtext.get()
    if text=="": text=" "
    self.gettext.insert(END,'Me >> %s \n'%text)
    self.sendtext.delete(0,END)
    pass_phrase=""
    i=0
    while i<32:
      a=random.randint(0,1)
      pass_phrase+=str(a)
      i+=1
    variable=AES()
    variable.pass_phrase=pass_phrase
    variable.secret_key=generate_secret_key(pass_phrase)
    variable.cipher=AESCipher(variable.secret_key)
    variable.encrypt_text=variable.cipher.encrypt(text)
    data_string=pickle.dumps(variable)
    self.client.send(data_string)
    self.sendtext.focus_set()
    self.gettext.configure(state=DISABLED)
    self.gettext.see(END)
  def run(self):
    Receive(self.client, self.gettext)
root=Tk()
root.title('Server Chat Side')
app=App(root).start()
root.mainloop()

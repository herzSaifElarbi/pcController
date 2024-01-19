import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import paramiko
client = paramiko.SSHClient()

kivy.require("1.9.0")
#kv = Builder.load_file("my.kv")
class ControlScreen(Screen):
    def on_enter(self):
        # This method will be called when the user presses Enter in the TextInput
        text = self.my_text_input.text
        self.my_text_input.text = ""
        if text == "exit" or text == "^C":
            client.close()
            self.manager.current = 'Connection'
        else:
            stdin, stdout, stderr = client.exec_command(text)
            if(stdout):
                message = stdout.read().decode()
                err_message = stderr.read().decode()

            cmd = "$> " + text + "\n" + message + "\n" + err_message + "\n"
            self.my_text_output.text += cmd
            

class ConnectionScreen(Screen):
    def connect(self, hostname_connect, port_connect, user_connect, passwd_connect):
        try:
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            client.connect(hostname_connect, port_connect, user_connect, passwd_connect)
            self.manager.current = 'Control'
        except Exception as e:
            self.info.text = str(e)
            
    hostname = ObjectProperty(None)
    port = ObjectProperty(None)
    user = ObjectProperty(None)
    passwd = ObjectProperty(None)
    info = ObjectProperty(None)
    
    def pressed(self):
        if(self.hostname.text  and self.port.text and self.user.text  and self.passwd.text):    
            
            hostname_text = self.hostname.text
            port_text = self.port.text
            user_text = self.user.text
            passwd_text = self.passwd.text
            
            self.hostname.text = ""
            self.port.text = ""
            self.user.text = ""
            self.passwd.text = ""
            self.connect(hostname_text, port_text, user_text, passwd_text)
            
        else:
            self.info.text = "please enter all values"

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ConnectionScreen(name='Connection'))
        sm.add_widget(ControlScreen(name='Control'))
        return sm

if __name__ == "__main__":
    MyApp().run()
    
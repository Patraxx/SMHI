
from tabulate import tabulate
import os
import serial
import keyboard
import time

serialcom = serial.Serial('com10', baudrate=2400, timeout=1)

hex_string = '9A 00 01 00 0A CC C7'
hex_string2= '9A 00 01 00 0A DD D6'
hex_string3= '9A 00 01 00 0A EE E5'

bytes1 = bytes.fromhex(hex_string)
bytes2 = bytes.fromhex(hex_string2)
bytes3 = bytes.fromhex(hex_string3)

string1 = "Stopp"
string2 = "Upp från stopp"
string3 = "Ner från stopp"

hex_meaning_dict = {
    bytes1: string1,
    bytes2: string2,
    bytes3: string3
}

def commandSwitch(command):
    if command == 1:
        return bytes1
    elif command == 2:
        return bytes2
    elif command == 3:
        return bytes3
    elif command == 4:
        return None
    else:
        print("Invalid command")
        return None
    
def display_menu():
    menu = [
        ["1", "Stopp"],
        ["2", "Upp från stopp"],
        ["3", "Ner från stopp"],
        ["4", "Exit"]
    ]
    print("\n" + "="*30)
    print("Select a command:")
    print(tabulate(menu, headers=["Option", "Command"], tablefmt="pretty"))
    print("="*30 + "\n")

currentCommand = 0

def run_menu():
    try:
        while (True):     
            os.system('cls'if os.name == 'nt' else 'clear')
            display_menu()
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                command = None
                if event.name == '1':
                    command = 1
                elif event.name == '2':
                    command = 2
                elif event.name == '3':
                    command = 3
                elif event.name == '4':
                    command = 4
                else:
                    time.sleep(0.5)
                    continue
                  
            if  command is not None:
                byte_command = commandSwitch(command)
                if byte_command is None:
                    if command == 4:
                        print("Exiting program")
                        break
                    continue  
                else:
                    serialcom.write(byte_command)
                    print(f"Sent command: {hex_meaning_dict[byte_command]}")
                    time.sleep(1)
                        
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        serialcom.close()

    


if __name__ == '__main__':
   
















""" Stopp: 		    0x9a 0x00 0x01 0x00 0X0a 0xcc 0xc7
    Upp från stopp: 0x9a 0x00 0x01 0x00 0x0a 0xdd 0xd6
    Ner från stopp:	0x9a 0x00 0x01 0x00 0x0a 0xee 0xe5 """

import serial as serial
import tabulate as tabulate
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

if __name__ == '__main__':


    while True:
        data = serialcom.read(7)
        print(hex_meaning_dict.get(data, "Unknown data"))
        print(data)

    serialcom.close()















""" Stopp: 		    0x9a 0x00 0x01 0x00 0X0a 0xcc 0xc7
    Upp från stopp: 0x9a 0x00 0x01 0x00 0x0a 0xdd 0xd6
    Ner från stopp:	0x9a 0x00 0x01 0x00 0x0a 0xee 0xe5 """
from asyncore import write
import xlsxwriter

current_char_index = 0

char_list = ['#','(',',',')',':', '\'','-','+','*','/','"','=',
'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
'q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F',
'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
'W','X','Y','Z','1','2','3','4','5','6','7','8','9','0', ' ','\n','.', '_', '?']

row_list = [0,2,3,4,6,7,8,9,11,12,13,14,15,16,17,18,19,20,22,
23,25,26,28,29,30,31,32,33,35,36,37,38,39,41,42,43,44,45,47,
48,49,50,51,52,53,54,55,56,57,58,59,60,61,-1]

def scanner():
    global current_char_index
    global transtable
    global char_list
    global row_list

    state = 0
    token = ""
    while (True):
        if (len(lines) < current_char_index+1):
            return -1
        ch = nextChar()
        token = token + ch
        state = int(transtable[row_list.index(state)][char_list.index(ch)])
        if (state == 3):
            return [token.lstrip()[:-1:] , 'comment']        
        if (state == 9 or state == 17 or state == 33 or state == 39 or state == 43 or
         state == 45 or state == 51 or state == 54):
            return [token.lstrip()[:-1:] , 'keyword']       
        if (state == 18):
            return [token.lstrip() , 'delimiter']
        if (state == 56):
            if (ch == '(' or ch == ')' or ch == ',' or ch == ':' or ch == '+' or ch == '-' or ch == '*' or ch == '/'):
                current_char_index = current_char_index - 1
            return [token.lstrip()[:-1:] , 'id']   
        if (state == 58):
            if (ch == '(' or ch == ')' or ch == ',' or ch == ':' or ch == '+' or ch == '-' or ch == '*' or ch == '/'):
                current_char_index = current_char_index - 1
            return [token.lstrip()[:-1:] , 'number literal']    
        if (state == 23 or state == 26):
            return [token.lstrip() , 'string literal']       
        if (state == 20):
            return [token.lstrip() , 'operator']        
        if (state == -1):
            return [token.lstrip()[:-1:] , 'error']

def nextChar():
    global current_char_index
    char = lines[current_char_index]
    current_char_index += 1
    return char

lines = ""
with open('input.txt') as f:
    lines = f.read()

transtable = []
with open('transtable.txt') as f:
    for line in f.readlines():
        transtable.append(line.split('	'))

workbook = xlsxwriter.Workbook('output.csv')
worksheet = workbook.add_worksheet()
worksheet.write(0,0, 'Token')
worksheet.write(0,1, 'Token Type')

i = 1
with open ('output.txt', 'w') as f:
    while True:
        out = scanner()
        if (out == -1):
            break
        print(out)
        f.write(str(out)+"\n")
        worksheet.write(i ,0 ,out[0])
        worksheet.write(i ,1 ,out[1])
        i = i + 1

workbook.close()

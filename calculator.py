from tkinter import *

first_number = second_number = operator = None
percent_pressed = False  

def get_digit(digit):
    curr = label['text']
    new = curr + str(digit)
    label.config(text=new)

def clear():
    label.config(text='')

# Single digit removal
def backspace():
    curr = label['text']
    if curr:
        label.config(text=curr[:-1])

def get_operator(op):
    global first_number, operator, percent_pressed
    curr = label['text']
    if not curr:
        return  
    try:
        # if there's already an operator and a second number, compute intermediate result first
        if operator and operator in curr:
            idx = curr.find(operator)
            second_str = curr[idx+1:]
            if second_str != '':
                second_number = float(second_str)
                # compute intermediate result
                if operator == '+':
                    result = first_number + second_number
                elif operator == '-':
                    result = first_number - second_number
                elif operator == 'x':
                    result = first_number * second_number
                elif operator == '/':
                    if second_number == 0:
                        label.config(text='Error')
                        operator = None
                        return
                    result = first_number / second_number
                else:
                    result = None

                if result is not None:
                    first_number = result
                    operator = op
                    percent_pressed = False
                    label.config(text=format_result(result) + op)
                    return
            else:
                # user just changed operator
                label.config(text=curr[:-1] + op)
                operator = op
                percent_pressed = False
                return

        # normal case: no operator yet
        first_number = float(curr)
        operator = op
        percent_pressed = False
        label.config(text=format_result(first_number) + op)
    except ValueError:
        label.config(text='Error')
        operator = None

def format_result(value, force_float=False):
    # Format result: integer if whole number, else float.
    try:
        v = float(value)
    except:
        return 'Error'
    if force_float:
        s = str(round(v, 6))
        if '.' not in s:
            s += '.0'
        return s
    return str(int(v)) if v.is_integer() else str(round(v, 6))

def get_result():
    global first_number, second_number, operator, percent_pressed
    try:
        curr = label['text']
        if not operator:
            return
        if operator not in curr:
            return
        idx = curr.find(operator)
        second_str = curr[idx+1:]
        if second_str == '':
            label.config(text=format_result(first_number))
            operator = None
            return
        second_number = float(second_str)

        if operator == '+':
            result = first_number + second_number
        elif operator == '-':
            result = first_number - second_number
        elif operator == 'x':
            result = first_number * second_number
        elif operator == '/':
            if second_number == 0:
                label.config(text='Error')
                operator = None
                return
            result = first_number / second_number
        else:
            result = None

        if result is not None:
            if percent_pressed:
                label.config(text=format_result(result, force_float=True))
            else:
                label.config(text=format_result(result))
            first_number = result
            operator = None
            percent_pressed = False
        else:
            label.config(text='Error')
            operator = None
    except:
        label.config(text='Error')
        operator = None

def add_dot():
    curr = label['text']
    if operator and operator in curr:
        idx = curr.find(operator)
        after = curr[idx+1:]
        if '.' not in after:
            label.config(text=curr + '.')
    else:
        if '.' not in curr:
            label.config(text=curr + '.')

def percentage():
    global percent_pressed, first_number, operator
    curr = label['text']
    try:
        if operator and operator in curr:
            idx = curr.find(operator)
            second_str = curr[idx+1:]
            if second_str == '':
                # no second number: convert the first number to percentage and replace display
                value = float(first_number) / 100
                label.config(text=format_result(value, force_float=True))
                first_number = value
                operator = None
                percent_pressed = True
            else:
                sec_val = float(second_str) / 100
                label.config(text=curr[:idx+1] + format_result(sec_val, force_float=True))
                percent_pressed = True
        else:
            # no operator: convert whole displayed number
            if curr == '':
                return
            val = float(curr) / 100
            label.config(text=format_result(val, force_float=True))
            percent_pressed = True
    except:
        label.config(text='Error')

root = Tk()
root.title('Calculator')
root.geometry('280x442')
root.resizable(0, 0)
root.configure(background='black')

label = Label(root, text='', bg='black', fg='white')
label.grid(row=0, column=0, columnspan=5, pady=(50, 25), sticky='E')
label.config(font=('verdana', 30, 'bold'))

# First row
btn_all_clr = Button(root, text='AC', bg='#636363', fg='white', width=5, height=2, command=clear)
btn_all_clr.grid(row=1, column=0)
btn_all_clr.config(font=('verdana', 14))

btn_back_space = Button(root, text='⌫', bg='#636363', fg='white', width=5, height=2, command=backspace)
btn_back_space.grid(row=1, column=1)
btn_back_space.config(font=('verdana', 14))

btn_pntg = Button(root, text='%', bg='#636363', fg='white', width=5, height=2, command=percentage)
btn_pntg.grid(row=1, column=2)
btn_pntg.config(font=('verdana', 14))

btn_div = Button(root, text='/', bg='#C76E00', fg='white', width=5, height=2, command=lambda: get_operator('/'))
btn_div.grid(row=1, column=3)
btn_div.config(font=('verdana', 14))


# Second row
btn7 = Button(root, text='7', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(7))
btn7.grid(row=2, column=0)
btn7.config(font=('verdana', 14))

btn8 = Button(root, text='8', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(8))
btn8.grid(row=2, column=1)
btn8.config(font=('verdana', 14))

btn9 = Button(root, text='9', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(9))
btn9.grid(row=2, column=2)
btn9.config(font=('verdana', 14))

btn_mul = Button(root, text='x', bg='#C76E00', fg='white', width=5, height=2, command=lambda: get_operator('x'))
btn_mul.grid(row=2, column=3)
btn_mul.config(font=('verdana', 14))


# 3rd row
btn4 = Button(root, text='4', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(4))
btn4.grid(row=3, column=0)
btn4.config(font=('verdana', 14))

btn5 = Button(root, text='5', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(5))
btn5.grid(row=3, column=1)
btn5.config(font=('verdana', 14))

btn6 = Button(root, text='6', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(6))
btn6.grid(row=3, column=2)
btn6.config(font=('verdana', 14))

btn_sub = Button(root, text='-', bg='#C76E00', fg='white', width=5, height=2, command=lambda: get_operator('-'))
btn_sub.grid(row=3, column=3)
btn_sub.config(font=('verdana', 14))


# 4th row
btn1 = Button(root, text='1', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(1))
btn1.grid(row=4, column=0)
btn1.config(font=('verdana', 14))

btn2 = Button(root, text='2', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(2))
btn2.grid(row=4, column=1)
btn2.config(font=('verdana', 14))

btn3 = Button(root, text='3', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(3))
btn3.grid(row=4, column=2)
btn3.config(font=('verdana', 14))

btn_add = Button(root, text='+', bg='#C76E00', fg='white', width=5, height=2, command=lambda: get_operator('+'))
btn_add.grid(row=4, column=3)
btn_add.config(font=('verdana', 14))


# 5th row
btn_exp = Button(root, text='e', bg='#494848', fg='white', width=5, height=2)
btn_exp.grid(row=5, column=0)
btn_exp.config(font=('verdana', 14))

btn0 = Button(root, text='0', bg='#494848', fg='white', width=5, height=2, command=lambda: get_digit(0))
btn0.grid(row=5, column=1)
btn0.config(font=('verdana', 14))

btn_dot = Button(root, text='.', bg='#494848', fg='white', width=5, height=2, command=add_dot)
btn_dot.grid(row=5, column=2)
btn_dot.config(font=('verdana', 14))

btn_eql = Button(root, text='=', bg='#C76E00', fg='white', width=5, height=2, command=get_result)
btn_eql.grid(row=5, column=3)
btn_eql.config(font=('verdana', 14))

root.mainloop()

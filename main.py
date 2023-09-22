import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import psycopg2
import hashlib

conn = None
cur = None

window = tk.Tk()
window.title("Архив")

def dbaEnter(self):
    inp = dbaInput.get()
    resultOutput.config(state='normal')
    resultOutput.delete(1.0,tk.END)
    resultOutput.insert(tk.INSERT,'> ' + dbaInput.get() + '\n')
    if inp:
        if 'drop' in inp.lower():
            resultOutput.insert(tk.INSERT,'no drop is allowed here')
        else:
            cur.execute(dbaInput.get());
            results = cur.fetchall()
            conn.commit()
            resultOutput.insert(tk.INSERT,results)
    else:
        resultOutput.insert(tk.INSERT,'need input')
    resultOutput.config(state='disabled')
    dbaInput.delete(0,tk.END)

def probit(self):
    inp = inpSelect.get()
    resultOutput.config(state='normal')
    resultOutput.delete(1.0,tk.END)
    if inp:
        if cur:
            try:
                cur.execute('SELECT * FROM cases WHERE num = {0}'.format(int(inp)))
                results = cur.fetchall()
                if results:
                    conn.commit()
                    for val in results:
                        resultOutput.insert(tk.INSERT, 'Номер: {0}\n'.format(val[0]))
                        resultOutput.insert(tk.INSERT, 'Дата заведения: {0}\n'.format(val[1]))
                        resultOutput.insert(tk.INSERT, 'Состояние: {0}\n'.format(val[2]))
                        resultOutput.insert(tk.INSERT, 'Таб. номер. секретаря: {0}\n'.format(val[3]))
                        resultOutput.insert(tk.INSERT, 'Решение суда: {0}\n'.format(val[4]))
                        resultOutput.insert(tk.INSERT, 'Код суда: {0}\n'.format(val[5]))
                else:
                    resultOutput.insert(tk.INSERT,'Ничего не найдено')
            except:
                resultOutput.insert(tk.INSERT,'Ошибка в запросе!')
        else:
            resultOutput.insert(tk.INSERT,'sorry, some error with cur')
    else:
        resultOutput.insert(tk.INSERT,'need input')
    resultOutput.config(state='disabled')

def findAccused(self):
    inp = inpSearch.get()
    resultOutput.config(state='normal')
    resultOutput.delete(1.0,tk.END)
    if inp:
        inp = inp.replace('\'', '\'\'')
        if cur:
            try:
                cur.execute("SELECT * FROM accused WHERE last_name ILIKE '%{0}%'".format(inp))
                results = cur.fetchall()
                if results:
                    conn.commit()
                    for val in results:
                        resultOutput.insert(tk.INSERT, 'Паспорт: {0}\n'.format(val[0]))
                        resultOutput.insert(tk.INSERT, 'Фамилия: {0}\n'.format(val[1]))
                        resultOutput.insert(tk.INSERT, 'Имя: {0}\n'.format(val[2]))
                        resultOutput.insert(tk.INSERT, 'Отчество: {0}\n'.format(val[3]))
                else:
                    resultOutput.insert(tk.INSERT,'Ничего не найдено')
            except:
                resultOutput.insert(tk.INSERT,'Ошибка в запросе!')
        else:
            resultOutput.insert(tk.INSERT,'sorry, some error with cur')
    else:
        resultOutput.insert(tk.INSERT,'need input')
    resultOutput.config(state='disabled')
    
def login(self):
    global conn
    global cur
    try:
        log = inpLogin.get()
        pas = hashlib.sha256(inpPassword.get().encode('utf-8')).hexdigest()
        conn = psycopg2.connect(host="localhost",database="arhiv", user=log, password=pas)
        if conn:
            cur = conn.cursor()
            lblOutput.configure(text='Вход выполнен.')
            inpSelect.focus()
            
            inpSelect.config(state='normal')
            inpSearch.config(state='normal')

            if inpLogin.get() == 'vasya':
                dbaInput.config(state='normal')
            else:
                dbaInput.config(state='disabled')

    except:
        lblOutput.configure(text='Ошибка!!')


lblLogin = tk.Label(window, text="Логин:")
lblPassword = tk.Label(window, text="Пароль:")
inpLogin = tk.Entry(window, width=20)
inpPassword = tk.Entry(window, width=20, show="*")
lblLogin.grid(row=0, column=0, padx=10, pady=10)
lblPassword.grid(row=1, column=0)
inpLogin.grid(row=0, column=1)
inpPassword.grid(row=1, column=1)
inpLogin.focus()
inpLogin.bind('<Return>', lambda event: inpPassword.focus())
inpPassword.bind('<Return>', login)

lblOutput = tk.Label(window, width=30)
lblOutput.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
lblOutput.configure(text='Нажмите Enter для входа.')

lblSelect = tk.Label(window, text="Найти дело по номеру:")
inpSelect = tk.Entry(window, width=40, state='disabled')
lblSelect.grid(row=0, column=2)
inpSelect.grid(row=1, column=2)
inpSelect.bind('<Return>', probit)

lblSearch = tk.Label(window, text="Найти обвиняемого по фамилии:")
inpSearch = tk.Entry(window, width=40, state='disabled')
lblSearch.grid(row=2, column=2)
inpSearch.grid(row=3, column=2)
inpSearch.bind('<Return>', findAccused)

resultOutput = ScrolledText(window,width=80,height=10,state='disabled')
resultOutput.grid(row=5, column=0, columnspan=8, padx=10, pady=10)

dbaInput = tk.Entry(window, width=80, state='disabled')
dbaInput.bind('<Return>', dbaEnter)
dbaInput.grid(row=6, column=0, columnspan=8, padx=10, pady=10)


def on_closing():
    if conn:
        conn.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
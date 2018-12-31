import requests
import json
from tkinter import *
from tkinter import messagebox


def change_frame(f):
    f.tkraise()


root = Tk()
root.title("calculate time order")
root.geometry('1000x600')

f1 = Frame(root , bg ="black")
f2 = Frame(root)
f3 = Frame(root)

for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')

Button(f1, text=' Calculation ', bg="white", fg="red", command=lambda: change_frame(f2)).place(x=450, y=250)


def hf3():
    root.geometry('1000x720')
    change_frame(f3)


Button(f1, text='Comparison', bg="white", fg="red", command=hf3).place(x=450, y=350)


f2entry = Text(f2, bg="red", fg="white", height=30, width=110)
f2entry.place(x=85, y=30)
f2entry.insert(END, """//type here
int main()
{	
	
return 0;
}""")


def compiler(inpt):
    url = "https://api.jdoodle.com/v1/execute"
    headers = {'Content-type': 'application/json'}
    payload = {"clientId": "fdd703fe8c319389ca26ed052413ae87",
               "clientSecret": "51133fcab2c301dc71e99ee905643c23bb5a6ff7cdb2b85a4849c1083e362360",
               "script": """{}""".format(inpt),
               "language": "c",
               "versionIndex": "0",
               }
    response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    response_parsed = response.json()
    return response_parsed['output']


def lagrange_api(points):
    url = "https://www.dcode.fr/api/"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    payload = {"tool": "lagrange-interpolating-polynomial",
               "points": f"{points}"
               }

    response = requests.post(url=url, data=payload, headers=headers)
    output = response.json()
    return output


def point(source, N):
    final_source = "\n#include<stdio.h>" + "\n" + "#define n {}\n".format(N) + source
    output = compiler(final_source)
    tup = (N, len(output))
    return tup


def equation(usr_src):
    points = ""
    for n in range(0, 5, 2):
        points += str(point(usr_src, n))

    print("final points are: {}".format(points))
    dcode_response = lagrange_api(points)
    equation = dcode_response['results']
    print(f"Equation: {equation.strip('$$')}")
    final_equation = equation.strip('$$')
    return final_equation


def calc_handle():
    user_input = f2entry.get("1.0", "end-1c")
    complexity = equation(user_input)
    messagebox.showwarning("", f"{complexity} \n")


btn = Button(f2, text="Calculate", bg="white", fg="red", command=calc_handle).place(x=730, y=550)

Label(f3).place(x=0, y=0, relwidth=1, relheight=1)
f3entry = Text(f3, bg="red", fg="white", height=40, width=55)
f3entry.insert(END, "//your code ")
f3entry.grid(column=1, row=1)

lbl = Label(f3, bg="red", fg="white", text="  ")
lbl.grid(column=2, row=1)

f3entry2 = Text(f3, bg="red", fg="white", height=40, width=55)
f3entry2.insert(END, "//your code ")
f3entry2.grid(column=3, row=1)


def compare_handle():
    c1 = equation(f3entry.get("1.0", "end-1c"))
    c2 = equation(f3entry2.get("1.0", "end-1c"))
    if c1 > c2:
        messagebox.showinfo("", f"left={c1} is better")
    elif c2 < c1:
        messagebox.showinfo("", f"right={c2} is better")
    else:
        messagebox.showinfo("", f"left = right = {c1}")


compare_btn = Button(f3,
                     text="Compare",
                     bg="white", fg="red", command=compare_handle)
compare_btn.grid(row=1, column=5)

change_frame(f1)
root.mainloop()

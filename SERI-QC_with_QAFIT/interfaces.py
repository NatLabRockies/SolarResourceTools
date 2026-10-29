
import tkinter as tk
import tkinter.scrolledtext as tkst


def listPoints():
    def save():
        pass

    listPage = tk.Tk()
    menuBar = tk.Menu(listPage)
    file = tk.Menu(menuBar, tearoff=0)
    file.add_command(label="Save", command=save)
    file.add_command(label="Close", command=listPage.quit)

    listPage.wm_geometry("600x400+500+250")
    listPage.title("QCFIT - List")
    listFrame = tk.Frame(listPage, bd=1)
    listFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
    # text=tk.Text(listFrame, state='disabled')
    # text.place(relx=0,rely=0, relwidth=1, relheight=0.98)
    # sclbar = tk.Scrollbar(text)
    # sclbar.pack(side=tk.RIGHT, fill=tk.Y)
    sclbar = tk.Scrollbar(listFrame)
    sclbar.pack(side=tk.RIGHT, fill=tk.Y)

    # listText = tkst.ScrolledText(listFrame, state='disabled')
    # listText.place(relx=0, rely=0, relwidth=1, relheight=1)
    # text.config(state="normal")
    # text.insert(tk.END, "Text goes here")
    # text.config(state="disabled")
    for i in range(0, 100):
        label = "label" + str(i)
        label = tk.Label(listFrame, text="pointasdsfeafv rv evf  " + str(i))
        label.place(x=1, y=1 + i, relwidth=1, relheight=1)
        print(i)

    listPage.mainloop()
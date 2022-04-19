from tkinter import Tk, StringVar, Label, Entry, Text, Button, Frame, filedialog, Toplevel, messagebox, Menu
from tkinter.messagebox import askyesno
import skpy
from skpy import SkypeAuthException, SkypeApiException
import pathlib
import re


# Splash Login
def splash_login():
    global username
    global password
    global splash_window
    # make it show in the center of the screen
    splash_window = Tk()
    splash_window.title("Login Screen")
    screen_width = splash_window.winfo_screenwidth()
    screen_height = splash_window.winfo_screenheight()
    login_width = 300
    login_height = 200
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')
    splash_label = Label(
        splash_window, text="Login to Skype API to continue").place(x=50, y=5)

    # username label and text entry box
    username_label = Label(splash_window, text="Username").place(x=50, y=30)
    username = StringVar()
    username_entry = Entry(
        splash_window, textvariable=username).place(x=50, y=50)

    # password label and password entry box
    password_label = Label(splash_window, text="Password").place(x=50, y=80)
    password = StringVar()
    password_entry = Entry(
        splash_window, textvariable=password, show='*').place(x=50, y=100)

    login_button = Button(splash_window, padx=6, text="Get Login Token",
                          command=login_trigger).place(x=70, y=150)

    splash_window.mainloop()


# main window
def main_window():
    global textBox
    global tkWindow
    global entry_var
    global entry_var2
    # show in the center of the screen
    tkWindow = Tk()
    app_width = 800
    app_height = 600
    screen_width = tkWindow.winfo_screenwidth()
    screen_height = tkWindow.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    # main window start in the center of the screen
    tkWindow.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    tkWindow.title('Skype Broadcast App --Version 3.6')
    direct_by = Label(tkWindow, text='by Chris').pack(
        side='left', anchor='sw')

    # frame surrounding login form
    fr1 = Frame(tkWindow, highlightbackground="black", highlightthickness=1)
    fr1.place(x=0, y=0)
    fr2 = Frame(tkWindow)
    fr2.place(x=300, y=10)
    fr3 = Frame(tkWindow, highlightbackground="black", highlightthickness=1)
    fr3.place(x=80, y=100)
    fr4 = Frame(tkWindow, highlightbackground="black", highlightthickness=1)
    fr4.place(x=80, y=490)

    # text message box
    textBox = Text(fr3)

    textBox.insert('1.0', '# Instructions: \n'
                          '1. Type your message in this box.\n'
                          '2. Send message to operator group by choosing a button above.\n'
                          '3. You can add files as well.\n'
                          '#NOTE!!!\n'
                          '1. Don\'t spam the button, it will crash the program.\n')

    textBox.grid(row=0, column=0)

    # Used for files functions
    entry_var = StringVar()
    entry_var2 = StringVar()
    file_label = None

    # Menu
    my_menu = Menu(tkWindow)
    tkWindow.config(menu=my_menu)

    # Menu Items
    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="File", menu=file_menu)
    changes = (
        "1. Login Screen!\n"
        "2. Added confirmation before sending\n"
        "3. Pictures can send thumbnails now\n"
        "4. Can unsend messages\n"
        "###UPCOMING###\n"
        "1. Send multiple files\n"
        "2. Dark Mode\n")

    file_menu.add_command(label="Change Log",
                          command=lambda: popup_window(changes))

    # Buttons on main window
    get_id_button = Button(tkWindow, padx=14, text="Get IDs",
                           command=get_ids).place(x=80, y=10)
    open_file_button = Button(
        tkWindow, padx=20, text="Open file..", command=open_file).place(x=80, y=500)
    clear_file_button = Button(
        tkWindow, padx=20, text="Clear file", command=clear_file).place(x=220, y=500)

    # Operator buttons on main window
    test_button = Button(tkWindow, padx=30, text="Preview",
                         command=command_factory("test")).place(x=80, y=40)
    unsend_button = Button(tkWindow, padx=30, text="Unsend",
                           command=unsend_msg).place(x=80, y=70)
    test2_button = Button(fr2, padx=20, text="test2",
                        command=command_factory("test2")).grid(row=0, column=0)

    tkWindow.mainloop()


# Conversations by group
conversations_test = {
    "19:954ea465b3cf42079987e9e11c76eba2@thread.skype": "Test Group 1",
}

conversations_test2 = {
    "19:8de3edf08d2d485a8b1168fee2738491@thread.skype": "Test Group 2",
}


# Add a file to send
def open_file():
    global open_file_label

    entry_var.set("")
    filenames = filedialog.askopenfilename(title='Open file', filetypes=[
        ('All Files', '*')])
    entry_var.set(filenames)
    open_file_label = Label(tkWindow, text=filenames, textvariable=entry_var)
    open_file_label.place(x=80, y=550)


# send a file
def send_file(ops):
    global entry_var

    file_to_send = entry_var.get().rsplit('/', 1)
    with open(entry_var.get(), "rb") as file:  # Selects the file you choose
        file_extension = pathlib.Path(
            entry_var.get()).suffix  # check the file extension
        image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]
        if file_extension in image_extensions:
            # send thumbnail if it's a picture
            ops.sendFile(file, file_to_send[1], image=True)
        else:
            ops.sendFile(file, file_to_send[1])


# Clear the file
def clear_file():
    entry_var.set("")


# Popup window for when errors show
def popup_window(text):
    window = Toplevel()

    label = Label(window, text=text)
    label.pack(fill='x', padx=50, pady=5)

    button_close = Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')


# Trigger skype_login function
def login_trigger():
    if username.get() != '':
        if password.get() != '':
            try:
                skype_login(username, password)
                splash_window.destroy()
                main_window()
            except SkypeAuthException:
                messagebox.showerror(
                    'Login Failed!!', 'Please confirm your email and password.')
            except SkypeApiException as error:
                popup_window(error)
        elif password.get() == '':
            messagebox.showerror('PASSWORD please!', 'The PASSWORD is empty!')
    else:
        messagebox.showerror('USERNAME please!', 'The USERNAME is empty!')


# Login to Skype API "Get Token" Button
def skype_login(email, pswd):
    global sk
    sk = skpy.Skype(email.get(), pswd.get())
    return sk


# Grab the Skype Chat IDs
def get_ids():
    chat_values = []
    try:
        with open('GetID.txt', 'w') as f:
            for keys, values in sk.chats.recent().items():
                chat_values.append(values)
            f.write(str(chat_values[0:1]) + "\n")
        popup_window(chat_values[0:1])
    except SkypeApiException as error:
        popup_window(error)
        pass
    except SkypeAuthException as error:
        popup_window(error)
        pass
    except NameError:
        messagebox.showerror(
            'Not logged in.', 'Please confirm your email or password.')
        pass


# Asks for confirmation before sending.
def confirm():
    answer = askyesno(title='Confirm', message='Are you sure?')
    if answer:
        return True


# Starts the Tkinter button commands and chooses an operator group.
def command_factory(text):
    def operator_chooser():
        if text == "test":
            global conversations_test
            skype_blast(conversations_test)
        elif text == "test2":
            global conversations_test2
            if confirm():
                skype_blast(conversations_test2)
    return operator_chooser


sent_msgs = []

# Strips the messages for the ID numbers and deletes them


def unsend_msg():
    if len(sent_msgs) == 0:
        messagebox.showerror('Error!', 'Nothing to unsend!')
    else:
        answer = askyesno(title='Confirm', message='Are you sure? This will unsend ALL messages sent with this tool from ALL operators. '
                                                   'Messages directly sent on Skype will not be affected.')
        if answer:
            for x in sent_msgs:
                x = re.split("\s", x, 1)
                y = x[1]
                z = re.split("\s", y, 2)
                a = z[1]
                for id in sk.chats:
                    try:
                        id.deleteRaw(a)
                    except:
                        pass
    sent_msgs.clear()

# Sends message to operators


def skype_blast(operator):
    message = textBox.get("1.0", "end-1c")
    for contact_id in operator:
        try:
            operator = sk.chats.chat(contact_id)
            sent_msgs.append(str(operator.sendMsg(message)))
            if entry_var.get() != "":
                answer = askyesno(
                    title='Confirm', message='Are you sure you want to send a file? You CANNOT unsend files.')
                if answer:
                    send_file(operator)
            else:
                pass
        except SkypeAuthException as error:
            print(error)
        except SkypeApiException as error:
            print(error)
            pass
        except FileNotFoundError as error:
            print(error)
            pass
        except NameError as error:
            print(error)
            pass
        except ConnectionError as error:
            print(error)
            pass


# Launches login splash screen
splash_login()

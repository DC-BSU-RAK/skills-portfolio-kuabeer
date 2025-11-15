from tkinter import *
from PIL import ImageTk, Image
import random

# Global variables
jokes_list = []
current_setup = ""
current_punchline = ""

root = Tk()
root.title("Alexa tell me a Joke") # window name 
root.geometry("1920x1080") # laptop screen size 

def show_frame(frame):
    frame.tkraise()

def click_me():
    show_frame(frame2) # to click here screen 

def back_to_home():
    show_frame(frame1) # to the home screen 

def start_tell_joke():
    show_frame(frame3) # to joke screen 
    next_joke()  # Show a joke immediately when entering the screen 

def openFile(): # load jokes from text file 
    global jokes_list 
    with open("randomJokes.txt","r") as file_handler:
        jokes_list = [line.strip() for line in file_handler]
    print(f"Loaded {len(jokes_list)} jokes from file") 

def random_jokes():
    global current_punchline, current_setup

    if jokes_list:
        joke_text = random.choice(jokes_list)
        
        # Split the joke into setup and punchline
        if "?" in joke_text:
            parts = joke_text.split("?", 1)
            current_setup = parts[0].strip() + "?"
            current_punchline = parts[1].strip()
        else:
            # If no question mark, use the whole line as setup
            current_setup = joke_text
            current_punchline = "No punchline found!"
        
        return current_setup
    else:
        return "No jokes available!"
        

def show_punchline(): #Display the punchline of the current joke
    punchline_label.config(text=current_punchline)

def next_joke(): #Display a new random joke
    setup = random_jokes()
    joke_label.config(text=setup)
    punchline_label.config(text="")  # Clear previous punchline

def quit_application():
    root.quit() #stop the main loop
    root.destroy # destroy all and close window

openFile()

# load background image 
home_img = ImageTk.PhotoImage(Image.open("4.png"))
start_img = ImageTk.PhotoImage(Image.open("5.png"))
joke_img = ImageTk.PhotoImage(Image.open("6.png"))

# frame 1 - Home screen 
frame1 = Frame(root)
bg_screen = Label(frame1,
                  image=home_img)
bg_screen.place(relx=0, rely=0, relwidth=1, relheight=1)

text = Label(frame1, 
             text="Alexa's Joke!", 
             font=("Comic Sans MS",55,"bold"), 
             justify=CENTER,
             fg="Black", 
             bg="#ffb902") # to match color from background
text.place(relx=0.5, rely=0.45, anchor=CENTER) # position of text 

start = Button(frame1, 
               text="Let's Start", 
               font=("Comic Sans MS",20), 
               fg="white", 
               bg="black", 
               relief="raised",
               command=click_me) # Navigates to click here screen
start.place(relx=0.5, rely=0.6, width=250, anchor=CENTER)

frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

#frame 2 - start joke screen 
frame2 = Frame(root)
bg_screen = Label(frame2,
                  image=start_img)
bg_screen.place(relx=0, rely=0, relwidth=1, relheight=1)

click_here_text = Label(frame2, 
                        text="Click Here!", 
                        font=("Comic Sans MS",25,"bold"), 
                        justify=CENTER,
                        fg="Black", 
                        bg="#ffb902") # to match color from background
click_here_text.place(relx=0.5, rely=0.45, anchor=CENTER) # position of text 

start1 = Button(frame2, 
                text="Alexa tell me a Joke", 
                font=("Comic Sans MS",30), 
                fg="white", 
                bg="black", 
                relief="raised",
                command=start_tell_joke) # Navigates to joke screen + shows joke
start1.place(relx=0.5, rely=0.6, anchor=CENTER)

back_btn = Button(frame2, 
                   text="back", 
                   font=("Comic Sans MS",20), 
                   fg="black", 
                   bg="#ffb902", 
                   relief="raised",
                   command=back_to_home) # Navigates back to home screen
back_btn.place(relx=0.2, rely=0.2,width=180, anchor=CENTER)

frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

#frame 3 - joke telling screen
frame3 = Frame(root)
bg_screen = Label(frame3,
                  image=joke_img)
bg_screen.place(relx=0, rely=0, relwidth=1, relheight=1)

quit_btn = Button(frame3, 
                  text="Quit", 
                  font=("Comic Sans MS",20), 
                  fg="black", 
                  bg="#ffb902", 
                  relief="raised",
                  command=quit_application) # Navigates back to home screen
quit_btn.place(relx=0.2, rely=0.15,width=180, anchor=CENTER)

joke_label = Label(frame3,
                    text="",
                    font=("Comic Sans MS",20,"bold"), 
                    fg="black", 
                    bg="#ffb902")
joke_label.place(relx=0.5,rely=0.35,anchor=CENTER)

punchline_label = Label(frame3,
                        text="",
                        font=("Comic Sans MS", 20, "italic"),
                        fg="white",
                        bg="#ffb902",
                        justify=CENTER)
punchline_label.place(relx=0.5, rely=0.55, anchor=CENTER)

next_joke_btn = Button(frame3, 
                       text="Next Joke", 
                       font=("Comic Sans MS",20), 
                       fg="black", 
                       bg="#ffb902", 
                       relief="raised",
                       command=next_joke)
next_joke_btn.place(relx=0.6, rely=0.85, anchor=CENTER)

show_punchline_btn = Button(frame3, 
                            text="Show Punchline", 
                            font=("Comic Sans MS",20), 
                            fg="black", 
                            bg="#ffb902", 
                            relief="raised",
                            command=show_punchline)
show_punchline_btn.place(relx=0.4, rely=0.85, anchor=CENTER)

frame3.place(relx=0, rely=0, relwidth=1, relheight=1)

# Start with home screen
show_frame(frame1)

root.mainloop()

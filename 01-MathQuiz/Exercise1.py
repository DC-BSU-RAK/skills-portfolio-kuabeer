from tkinter import *
from PIL import ImageTk, Image
import random

root = Tk()
root.title("Math Quiz") # window name 
root.geometry("1920x1080") # laptop screen size 

# global variables 
current_difficulty = ""   
score = 0                 
current_question = 0      
total_questions = 10
first_attempt = True
num1 = 0
num2 = 0
operation = ""
correct_answer = 0

def show_frame(frame):
    frame.tkraise()  

def go_to_instructions():
    show_frame(frame2) # move to instruction screen 

def go_to_difficulty():
    show_frame(frame3) # move to difficulty level screen

def back_to_home():
    show_frame(frame1) # back to home screen 

def back_to_instructions():
    show_frame(frame2) # back to instruction screen

def play_again():
    show_frame(frame3) # back to difficulty level to start play again 

def randomInt(difficulty): # generate random number based on difficulty level 
    if difficulty == "Easy":
        return random.randint(0, 9)
    elif difficulty == "Moderate":
        return random.randint(10, 99)
    else:  # Advanced
        return random.randint(1000, 9999)

def decideOperation(): # decide problem is whether addition or subtraction 
    return random.choice(['+', '-'])

def calculateAnswer(num1, num2, operation): # to calculate correct answer 
    if operation == "+":
       return num1 + num2 
    else: # subtraction -
        # Ensure result is never negative by swapping numbers 
        if num1 < num2:
            num1, num2 = num2, num1
        return num1 - num2

def displayProblem(num1, num2, operation): # display math problem
    problem.config(text=f"{num1} {operation} {num2} = ?")

def isCorrect(user_answer, correct_answer): # check answer is correct or not
    return user_answer == correct_answer

def displayResults(): # show results with feedback
    global score
    show_frame(frame5)
    
    # Calculate grade
    if score >= 90:
        grade = "A+"
        message = "Excellent!"
    elif score >= 80:
        grade = "A"
        message = "Great job!"
    elif score >= 70:
        grade = "B"
        message = "Good work!"
    elif score >= 60:
        grade = "C"
        message = "Not bad!"
    elif score >= 50:
        grade = "D"
        message = "Keep practicing!"
    else:
        grade = "F"
        message = "Try again!"
    
    result_text.config(text=f"Final Score: {score}/100")
    grade_label.config(text=f"Grade: {grade}")
    message_label.config(text=message)

def start_quiz(difficulty): # start quiz with selected difficulty level
    global current_difficulty, score, current_question, first_attempt
    current_difficulty = difficulty
    score = 0
    current_question = 0
    first_attempt = True
    show_frame(frame4)
    feedback.config(text="")
    next_question()

def next_question(): # show next question if answer is correct 
    global num1, num2, operation, correct_answer, current_question, first_attempt

    if current_question >= total_questions:
        displayResults() # if all question is done then show results screen 
        return # exit the question screen 
    
    # create new question  
    num1 = randomInt(current_difficulty)
    num2 = randomInt(current_difficulty)
    operation = decideOperation()

    correct_answer = calculateAnswer(num1, num2, operation) 

    # update question screen using displayProblem function
    question_text.config(text=f"Question {current_question + 1}/{total_questions}")
    displayProblem(num1, num2, operation)
    answer_entry.delete(0, END)
    score_label.config(text=f"Score: {score}")
    first_attempt = True
    submit.config(text="Submit Answer")
    feedback.config(text="")

def check_answer():
    global score, first_attempt, current_question

    try:
        user_answer = int(answer_entry.get())  # get user answer and convert it to integer
    except ValueError:
        feedback.config(text="Please enter a valid number!", fg="red") # if user enter letter or nothing 
        return
    
    if isCorrect(user_answer, correct_answer):
        if first_attempt: 
            score += 10 # first try 
            feedback.config(text="Correct! +10 points", fg="white")
        else:
            score += 5 # Second try
            feedback.config(text="Correct! +5 points", fg="white")
        
        current_question += 1 # move to next question 
        score_label.config(text=f"Score: {score}") # update score 

        # Only delay for correct answers
        root.after(1000, check_quiz_completion)
        
    else: #  user answered incorrect
        if first_attempt: # give second chance if answer is wrong 
            first_attempt = False
            feedback.config(text="Incorrect! Try again", fg="red")
            submit.config(text="Try Again")
        else: # if answer is wrong = show correct answer and move to next question 
            feedback.config(text=f"Incorrect! Answer: {correct_answer}", fg="red")
            current_question += 1
            # Delay only when moving to next question after second wrong attempt
            root.after(1000, check_quiz_completion)

def check_quiz_completion(): # check if quiz is done after delay
    if current_question >= total_questions:
        displayResults()  # Go to results screen
    else:
        next_question()  # Show next question

# All image 
home_img = ImageTk.PhotoImage(Image.open("1.png")) # home background / result background 
background_img =ImageTk.PhotoImage(Image.open("2.png")) # instruction / difficulty background
broad_img = ImageTk.PhotoImage(Image.open("3.png")) # question broad background

# frame 1 - Home screen 
frame1 = Frame(root)
bg_screen = Label(frame1,
                  image=home_img)
bg_screen.place(relx=0, rely=0, relwidth=1, relheight=1)

text = Label(frame1, 
             text="Math Quiz", 
             font=("Comic Sans MS",80,"bold"), 
             fg="white", 
             bg="#c21110") 
text.place(relx=0.5, rely=0.4,width=600, anchor=CENTER) # position of text 

start = Button(frame1, 
               text="Start", 
               font=("Comic Sans MS",20), 
               fg="white", 
               bg="#ffb902", 
               relief="raised", # to make button look 3d 
               command=go_to_instructions) # move to instruction / frame 2
start.place(relx=0.5, rely=0.6, width=250, anchor=CENTER) # position of start button 

frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

# frame 2 - Instruction screen
frame2 = Frame(root)

bg_screen2 = Label(frame2,
                  image=background_img)
bg_screen2.place(relx=0, rely=0, relwidth=1, relheight=1)

text2 = Label(frame2,
              text="Instructions:",
              font=("Comic Sans MS",30,"bold"),
              fg="white",
              bg="#c21110")
text2.place(relx=0.5, rely=0.3, anchor=CENTER)

text3 = Label(frame2, # instructions list 
              text="- You have to choose difficulty level\n" +
                   "- There will be 10 questions\n" +
                   "- 10 points for first try but 5 points for 2nd try!\n" +
                   "- Total marks: 100 points" ,
              font=("Comic Sans MS", 20),
              fg="white",
              bg="#c21110",
              justify=CENTER, # text align 
              width=50,
              height=5)
text3.place(relx=0.5, rely=0.5, anchor=CENTER)

start2 = Button(frame2,
                text="Begin Quiz",
                font=("Comic Sans MS", 20),
                fg="white",
                bg="#ffb902",
                relief="raised",
                command=go_to_difficulty) # move to diificulty level / frame 3
start2.place(relx=0.5, rely=0.7, width=200, anchor=CENTER)

back = Button(frame2,
              text="Back",
              font=("Comic Sans MS", 15),
              fg="white",
              bg="#1e74bd",
              relief="raised",
              command=back_to_home)
back.place(relx=0.2, rely=0.25, width=150, anchor=CENTER)

frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

# frame 3 - Difficulty level 
frame3 = Frame(root)

bg_screen3 = Label(frame3,
                  image=background_img)
bg_screen3.place(relx=0, rely=0, relwidth=1, relheight=1)


level_text = Label(frame3,
               text="Choose the Difficulty Level:",
               font=("Comic Sans MS",30,"bold"),
               fg="white",
               bg="#c21110")
level_text.place(relx=0.5, rely=0.4, anchor=CENTER) # position of text 

button1 = Button(frame3,
                 text="Easy",
                 font=("Comic Sans MS",20),
                 fg="white",
                 bg="#ffb902",
                 relief="raised",
                 command=lambda: start_quiz("Easy")) # move to easy question screen 
button1.place(relx=0.3, rely=0.5, width=250, anchor=CENTER)

button2 = Button(frame3,
                 text="Moderate",
                 font=("Comic Sans MS",20),
                 fg="white",
                 bg="#ffb902",
                 relief="raised",
                 command=lambda: start_quiz("Moderate")) # move to moderate question screen 
button2.place(relx=0.5, rely=0.5, width=250, anchor=CENTER)

button3 = Button(frame3,
                 text="Advanced",
                 font=("Comic Sans MS",20),
                 fg="white",
                 bg="#ffb902",
                 relief="raised",
                 command=lambda: start_quiz("Advanced")) # move to advanced question screen 
button3.place(relx=0.7, rely=0.5, width=250, anchor=CENTER)

back2 = Button(frame3,
                 text="Back",
                 font=("Comic Sans MS",15),
                 fg="white",
                 bg="#1e74bd",
                 relief="raised",
                 command=back_to_instructions) # move to instruction / frame 2 
back2.place(relx=0.2, rely=0.25, width=150, anchor=CENTER)

frame3.place(relx=0, rely=0, relwidth=1, relheight=1)

# frame 4 - question screen 
frame4 = Frame(root)

bg_screen4 = Label(frame4,
                  image=broad_img)
bg_screen4.place(relx=0, rely=0, relwidth=1, relheight=1)

question_text = Label(frame4,
                      text="Question 1/10",
                      font=("Comic Sans MS",30,"bold"),
                      fg="white",
                      bg="#3f9c43")
question_text.place(relx=0.5, rely=0.25, anchor=CENTER)

problem = Label(frame4, 
                text=" ", 
                font=("Comic Sans MS", 50, "bold"),
                fg="white", 
                bg="#3f9c43")
problem.place(relx=0.5, rely=0.45, anchor=CENTER)

answer_entry = Entry(frame4,
                      text=" ",
                      font=("Comic Sans MS",30,"bold"),
                      fg="white",
                      bg="#3b7c76",
                      width=20)
answer_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
answer_entry.bind('<Return>', lambda event: check_answer())  

back3 = Button(frame4,
              text="Quit Quiz",
              font=("Comic Sans MS", 15),
              fg="white",
              bg="#1e74bd",
              relief="raised",
              command=back_to_instructions) # move to instruction / frame 2
back3.place(relx=0.2, rely=0.2, width=150, anchor=CENTER)

submit = Button(frame4,
              text="Submit",
              font=("Comic Sans MS", 20),
              fg="white",
              bg="#ffb902",
              relief="raised",
              command=check_answer) 
submit.place(relx=0.5, rely=0.7, width=220, anchor=CENTER)

score_label = Label(frame4, 
                    text="Score: 0", 
                    font=("Comic Sans MS", 25),
                    fg="white", 
                    bg="#3f9c43")
score_label.place(relx=0.8, rely=0.2, anchor=CENTER)

feedback = Label(frame4,
                      text="",
                      font=("Comic Sans MS", 20),
                      fg="white",
                      bg="#3f9c43")
feedback.place(relx=0.5, rely=0.35, anchor=CENTER)

frame4.place(relx=0, rely=0, relwidth=1, relheight=1)

# frame 5 - result screen 
frame5 = Frame(root)

bg_screen5 = Label(frame5,
                  image=home_img)
bg_screen5.place(relx=0, rely=0, relwidth=1, relheight=1)

result_text = Label(frame5,
                    text="Results:", 
                    font=("Comic Sans MS",40,"bold"), 
                    fg="white", 
                    bg="#c21110")
result_text.place(relx=0.5, rely=0.3, anchor=CENTER)

grade_label = Label(frame5,
                    text=" ",
                    font=("Comic Sans MS", 35),
                    fg="white", 
                    bg="#c21110")
grade_label.place(relx=0.5, rely=0.4, anchor=CENTER)

message_label = Label(frame5,
                      text=" ",
                      font=("Comic Sans MS", 35),
                      fg="white", 
                      bg="#c21110")
message_label.place(relx=0.5, rely=0.5, anchor=CENTER)

back4 = Button(frame5,
                 text="Play Again",
                 font=("Comic Sans MS",20),
                 fg="white",
                 bg="#1e74bd",
                 relief="raised",
                 command=play_again) # move to difficulty level / frame 3 to start again 
back4.place(relx=0.4, rely=0.7, width=200, anchor=CENTER)

start3 = Button(frame5,
                 text="Back to home",
                 font=("Comic Sans MS",20),
                 fg="white",
                 bg="#1e74bd",
                 relief="raised",
                 command=back_to_home) # move to home screen  / frame 1
start3.place(relx=0.6, rely=0.7, width=200, anchor=CENTER)

frame5.place(relx=0, rely=0, relwidth=1, relheight=1)

show_frame(frame1)

root.mainloop()
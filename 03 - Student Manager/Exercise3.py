from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.title("Student Manager") # window name 
root.geometry("1024x500") # screen size 
root.resizable(0,0) # fixed size 

def openFile():
    students = [] # empty list to store data from file 
    try:
        with open ("studentMarks.txt", "r") as file_handler:
            lines = file_handler.readlines()

            for line in lines[1:]: # skip the first line which is the neumber of students 
                data = line.strip().split(",") # Split line by commas
                if len(data) == 6:
                    student_id, name, mark1, mark2, mark3, exam = data
                    coursework_total = int(mark1) + int(mark2) + int(mark3) # to calculate the total maek of coursework 
                    total_marks = coursework_total + int(exam)
                    percentage = (total_marks/ 160) * 100 
                    grade = studentGrade(percentage)

                    students.append({ # studnet dictionary with all information
                        'id': student_id,
                        'name': name,
                        'marks': [int(mark1), int(mark2), int(mark3)],
                        'coursework_total': coursework_total,
                        'exam': int(exam),
                        'total_marks': total_marks,
                        'percentage': percentage,
                        'grade': grade
                    })
            return students   # return the complete list
        
    except Exception as e: # error message if file reading fails
        messagebox.showerror("Error", f"Error reading file: {e}")
        return []    # retuen the empty list  
                    

def studentGrade(percentage):
     if percentage >= 70:
        grade = "A"
     elif percentage >= 60:
        grade = "B"
     elif percentage >= 50:
        grade = "C"
     elif percentage >= 40:
        grade = "D"
     else:
        grade = "F"
     return grade

def all_student_records(): # display all student information in table 
   textarea.delete(1.0, END)

   textarea.tag_configure("center", justify='center')  # Center alignment 

   if not students_data: # check if student data is available or not 
        textarea.insert(END, "No student data loaded!\n")
        return
    
   # Create headers with better spacing
   header1 = f"{'ID':<6} {'NAME':<13} {'COURSEWORK':<12} {'EXAM':<8} {'TOTAL':<8} {'%':<6} {'GRADE':<6}\n"
   header2 = f"{'':<6} {'':<16} {'TOTAL':<12} {'':<6} {'':<7} {'':<8} {'':<6}\n"
   separator = "-" * 64 + "\n"
    
   textarea.insert(END, "ALL STUDENT RECORDS\n", "center")
   textarea.insert(END, separator)
   textarea.insert(END, header1)
   textarea.insert(END, header2)
   textarea.insert(END, separator)

   # display each student's data 
   total_percentage = 0
   for student in students_data:
        row = f"{student['id']:<6} {student['name']:<18} {student['coursework_total']:<8} {student['exam']:<8} {student['total_marks']:<8} {student['percentage']:<8.1f} {student['grade']:<6}\n"
        textarea.insert(END, row)
        total_percentage += student['percentage']
    
   # display summary
   avg_percentage = total_percentage / len(students_data)
   textarea.insert(END, separator)
   textarea.insert(END, f"\nSUMMARY: Students: {len(students_data)}, Average: {avg_percentage:.1f}%\n","center")

def individual_student_record():
    if not students_data:
        messagebox.showwarning("Warning", "No student data loaded!") # messagebox if there is no student data 
        return
    
    # Create a new window for student selection
    select_window = Toplevel(root)
    select_window.title("Select Student")
    select_window.geometry("400x300")  
    
    # instruction Label
    label = Label(select_window, text="Select a student:", font=("Arial", 12, "bold"))
    label.place(x=20, y=20, width=360, height=30)
    
    # display student list 
    student_listbox = Listbox(select_window, font=("Arial", 10))
    student_listbox.place(x=20, y=60, width=360, height=180)  
    
    
    for student in students_data:
        student_listbox.insert(END, f"{student['id']} - {student['name']}")
    
    # Select button
    def on_select():
        selection = student_listbox.curselection()
        if selection:
            index = selection[0]
            show_individual_student(students_data[index])
            select_window.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a student!")
    
    select_btn = Button(select_window, text="Select Student", command=on_select, 
                       font=("Arial", 10, "bold"), bg="#1957D2", fg="white")
    select_btn.place(x=120, y=250, width=160, height=35)  
    


def show_individual_student(student):
    textarea.delete(1.0, END)
    textarea.tag_configure("center", justify='center')
   
    header1 = f"{'ID':<6} {'NAME':<13} {'COURSEWORK':<12} {'EXAM':<8} {'TOTAL':<8} {'%':<6} {'GRADE':<6}\n"
    header2 = f"{'':<6} {'':<16} {'TOTAL':<12} {'':<6} {'':<7} {'':<8} {'':<6}\n"
    separator = "-" * 64 + "\n"
    
    textarea.insert(END, "INDIVIDUAL STUDENT RECORD\n", "center")
    textarea.insert(END, separator)
    textarea.insert(END, header1)
    textarea.insert(END, header2)
    textarea.insert(END, separator)
    
    # Show the individual student 
    row = f"{student['id']:<6} {student['name']:<18} {student['coursework_total']:<8} {student['exam']:<8} {student['total_marks']:<8} {student['percentage']:<8.1f} {student['grade']:<6}\n"
    textarea.insert(END, row)
   
def highest_score(): # display the highest scoring student 
    textarea.delete(1.0, END)
    textarea.tag_configure("center", justify='center')

    if not students_data: # if student data is not load
        textarea.insert(END, "No student data loaded!\n")
        return
    
    # Find the highest scoring student
    highest_student = max(students_data, key=lambda x: x['total_marks'])

    
    header1 = f"{'ID':<6} {'NAME':<13} {'COURSEWORK':<12} {'EXAM':<8} {'TOTAL':<8} {'%':<6} {'GRADE':<6}\n"
    header2 = f"{'':<6} {'':<16} {'TOTAL':<12} {'':<6} {'':<7} {'':<8} {'':<6}\n"
    separator = "-" * 64 + "\n"
    
    textarea.insert(END, "HIGHEST SCORING STUDENT\n", "center")
    textarea.insert(END, separator)
    textarea.insert(END, header1)
    textarea.insert(END, header2)
    textarea.insert(END, separator)
    
   
    row = f"{highest_student['id']:<6} {highest_student['name']:<18} {highest_student['coursework_total']:<8} {highest_student['exam']:<8} {highest_student['total_marks']:<8} {highest_student['percentage']:<8.1f} {highest_student['grade']:<6}\n"
    textarea.insert(END, row)
    
    textarea.insert(END, separator)
    textarea.insert(END, f"\nThis student has the highest total score: {highest_student['total_marks']}/160\n", "center")

def lowest_score(): # display the lowest scroing student 
    textarea.delete(1.0, END)
    textarea.tag_configure("center", justify='center')

    if not students_data:
        textarea.insert(END, "No student data loaded!\n")
        return
    
    # Find the lowest scoring student
    lowest_student = min(students_data, key=lambda x: x['total_marks'])

   
    header1 = f"{'ID':<6} {'NAME':<13} {'COURSEWORK':<12} {'EXAM':<8} {'TOTAL':<8} {'%':<6} {'GRADE':<6}\n"
    header2 = f"{'':<6} {'':<16} {'TOTAL':<12} {'':<6} {'':<7} {'':<8} {'':<6}\n"
    separator = "-" * 64 + "\n"
    
    textarea.insert(END, "LOWEST SCORING STUDENT\n", "center")
    textarea.insert(END, separator)
    textarea.insert(END, header1)
    textarea.insert(END, header2)
    textarea.insert(END, separator)
    
    
    row = f"{lowest_student['id']:<6} {lowest_student['name']:<18} {lowest_student['coursework_total']:<8} {lowest_student['exam']:<8} {lowest_student['total_marks']:<8} {lowest_student['percentage']:<8.1f} {lowest_student['grade']:<6}\n"
    textarea.insert(END, row)
    
    textarea.insert(END, separator)
    textarea.insert(END, f"\nThis student has the lowest total score: {lowest_student['total_marks']}/160\n", "center")

def empty_it(): # empty the text area 
    textarea.delete(1.0, END)

      
students_data = openFile() # load student data from file 

#load background image 
home_img = ImageTk.PhotoImage(Image.open("7.png"))

# main home screen 
main_frame = Frame(root)
bg_screen = Label(main_frame,
                  image=home_img)
bg_screen.place(relx=0, rely=0, relwidth=1, relheight=1)
main_frame.place(relx=0, rely=0, relwidth=1, relheight=1) 

# title label 
label = Label(main_frame,
              text="Student\n Manager\n System",
              font=("Arial",30,"bold"),
              fg="white",
              bg="#1800ad",
              justify="center")
label.place(relx=0.03, rely=0.1)

textarea = Text(main_frame,
                width=40,
                height=10)
textarea.place(x=230, y=40, height=420, width=520)

# Vertical scrollbar to view all information 
vscroll = Scrollbar(root, orient="vertical")
vscroll.place(x=750, y=40, height=420)

vscroll.config(command=textarea.yview) # scrollbar controls the text view
textarea.config(yscrollcommand=vscroll.set) # text widget controls the scroolbar 

# clear textarea button 
empty_btn = Button(main_frame,
                   text="Empty",
                   font=("Arial",12,"bold"),
                   fg="white",
                   bg="#1957D2",
                   relief="raised",
                   command=empty_it)
empty_btn.place(relx=0.82, rely=0.05, width=120)

# Button 1: Display all student records
all_btn = Button(main_frame,
                 text="All Student Records",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=all_student_records)
all_btn.place(relx=0.78, rely=0.15, width=200)

# Button 2: Search for individual student 
individual_btn = Button(main_frame,
                 text="Individual\n Student Record",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=individual_student_record)
individual_btn.place(relx=0.78, rely=0.25, width=200)

# Button 3: Display highest score student 
highest_btn = Button(main_frame,
                 text="Highest Total Score",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=highest_score)
highest_btn.place(relx=0.78, rely=0.40, width=200)

# Button 4: Display lowest score student 
lowest_btn = Button(main_frame,
                 text="Lowest Total Score",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=lowest_score)
lowest_btn.place(relx=0.78, rely=0.50, width=200)

root.mainloop()
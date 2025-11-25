from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.title("Student Manager") # Window Title 
root.geometry("1024x500") # screen size 
root.resizable(0,0) # fixed window size 

def openFile():
    students = [] # empty list to store data from file 
    try:
        with open ("studentMarks.txt", "r") as file_handler:
            lines = file_handler.readlines()

            for line in lines[1:]: # skip the first line ( number of students ) 
                data = line.strip().split(",") # Split line by commas
                if len(data) == 6:
                    student_id, name, mark1, mark2, mark3, exam = data
                    coursework_total = int(mark1) + int(mark2) + int(mark3) # to calculate the total mark of coursework 
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
        return []    # return the empty list  
                    

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

def lowest_score(): # display the lowest scoring student 
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

def sort_students_data():
    if not students_data:   # if student data is not load
        messagebox.showwarning("Warning", "No student data loaded!")
        return
    
    # create new window for sort studnets 
    sort_window = Toplevel(root)
    sort_window.title("Sort Students")
    sort_window.geometry("300x200")

    # instruction label 
    Label(sort_window, text="Sort by:", font=("Arial", 12, "bold")).place(x=20, y=10)
    
    sort_option = StringVar()
    sort_option.set("name_asc") 
    
    # Sort option radiobuttons 
    Radiobutton(sort_window, text="Name (A-Z)", variable=sort_option, value="name_asc").place(x=70,y=40)
    Radiobutton(sort_window, text="Name (Z-A)", variable=sort_option, value="name_desc").place(x=70,y=60)
    Radiobutton(sort_window, text="Total Score (High-Low)", variable=sort_option, value="score_desc").place(x=70, y=80)
    Radiobutton(sort_window, text="Total Score (Low-High)", variable=sort_option, value="score_asc").place(x=70, y=100)
    
    def perform_sort():
        option = sort_option.get()
        sorted_students = students_data.copy() # create copy to avoid modifying original 
        
        # selected options 
        if option == "name_asc":
            sorted_students.sort(key=lambda x: x['name'].lower())
        elif option == "name_desc":
            sorted_students.sort(key=lambda x: x['name'].lower(), reverse=True)
        elif option == "score_desc":
            sorted_students.sort(key=lambda x: x['total_marks'], reverse=True)
        elif option == "score_asc":
            sorted_students.sort(key=lambda x: x['total_marks'])
        
        sort_window.destroy()
        textarea.delete(1.0, END)
        display_students_table(sorted_students, "SORTED STUDENT RECORDS")  
    
    Button(sort_window, text="Sort", command=perform_sort, font=("Arial", 10, "bold"), 
           bg="#1957D2", fg="white").place(x=130, y=130)

def display_students_table(students, title):

    textarea.tag_configure("center", justify='center')
    
    header1 = f"{'ID':<6} {'NAME':<13} {'COURSEWORK':<12} {'EXAM':<8} {'TOTAL':<8} {'%':<6} {'GRADE':<6}\n"
    header2 = f"{'':<6} {'':<16} {'TOTAL':<12} {'':<6} {'':<7} {'':<8} {'':<6}\n"
    separator = "-" * 64 + "\n"
    
    textarea.insert(END, f"{title}\n", "center")
    textarea.insert(END, separator)
    textarea.insert(END, header1)
    textarea.insert(END, header2)
    textarea.insert(END, separator)
    
    #display student data
    total_percentage = 0
    for student in students:
        row = f"{student['id']:<6} {student['name']:<18} {student['coursework_total']:<8} {student['exam']:<8} {student['total_marks']:<8} {student['percentage']:<8.1f} {student['grade']:<6}\n"
        textarea.insert(END, row)
        total_percentage += student['percentage']
    
    if len(students) > 0:
        avg_percentage = total_percentage / len(students)
        textarea.insert(END, separator)
        textarea.insert(END, f"\nSUMMARY: Students: {len(students)}, Average: {avg_percentage:.1f}%\n", "center")

def add_students_data():
    # create new window for add new student data 
    add_window = Toplevel(root)
    add_window.title("New Student Record")
    add_window.geometry("400x300")

    Label(add_window,text=" New Student Record", font=("Arial", 12, "bold")).place(x=110, y=10)

    # Input fields 
    labels = ["Student ID:", "Name:", "Mark 1 (0-20):", "Mark 2 (0-20):", "Mark 3 (0-20):", "Exam Mark (0-100):"]
    entries = []

    for i, label_text in enumerate(labels):
        Label(add_window, text=label_text, anchor="w").place(x=50, y=50 + i*30)
        entry = Entry(add_window, width=20)
        entry.place(x=150, y=50 + i*30)
        entries.append(entry)

    def save_new_student():
        try:
            # get and validate input data
            id = entries[0].get().strip()
            name = entries[1].get().strip()
            mark1 = int(entries[2].get())
            mark2 = int(entries[3].get())
            mark3 = int(entries[4].get())
            exam = int(entries[5].get())
            
            if not id or not name: # if id or name is empty 
                messagebox.showerror("Error", "ID and Name are required!")
                return
            # check if there is same id 
            if any(s['id'] == id for s in students_data):
                messagebox.showerror("Error", "Student ID already exists!")
                return
            
            # Validate mark ranges
            if not (0 <= mark1 <= 20) or not (0 <= mark2 <= 20) or not (0 <= mark3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0-20!")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0-100!")
                return
            
            # Calculate derived values
            coursework_total = mark1 + mark2 + mark3
            total_marks = coursework_total + exam
            percentage = (total_marks / 160) * 100
            grade = studentGrade(percentage)
            
            # Add to students data
            new_student = {
                'id': id, 'name': name, 'marks': [mark1, mark2, mark3],
                'coursework_total': coursework_total, 'exam': exam, 'total_marks': total_marks,
                'percentage': percentage, 'grade': grade
            }
            students_data.append(new_student)
            
            # Save to file
            if saveToFile(students_data):
                messagebox.showinfo("Success", "Student added successfully!")
                add_window.destroy()
                all_student_records() # display the updated studnet data after save it 
            else:
                students_data.pop()  # Remove if save failed
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks!")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding student: {e}")

    
    Button(add_window, text="Save Student", command=save_new_student, font=("Arial", 10, "bold"), bg="#1957D2", fg="white").place(x=150, y=250)
    
def saveToFile(students):
    try:
        with open("studentMarks.txt", "w") as file_handler:
            file_handler.write(f"{len(students)}\n")  # Write number of students first
            for student in students:
                line = f"{student['id']},{student['name']},{student['marks'][0]},{student['marks'][1]},{student['marks'][2]},{student['exam']}\n"
                file_handler.write(line)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")
        return False 

def delete_student():
    if not students_data: # messagebox if there is no student data 
        messagebox.showwarning("Warning", "No student data loaded!")
        return
    
    # new window for delete 
    delete_window = Toplevel(root)
    delete_window.title("Delete Student")
    delete_window.geometry("400x300")
    
    Label(delete_window, text="Select student to delete:", font=("Arial", 12, "bold")).place(x=20, y=20)
    
    #student list 
    student_listbox = Listbox(delete_window, font=("Arial", 10))
    student_listbox.place(x=20, y=60, width=360, height=180)
    
    for student in students_data:  
        student_listbox.insert(END, f"{student['id']} - {student['name']}")
    
    def perform_delete():
        selection = student_listbox.curselection()
        if not selection: # if student is not select to delete
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
        
        index = selection[0]
        student = students_data[index]
        
        # messagebox to make sure if user want to delete or not 
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete {student['name']} ({student['id']})?")
        if confirm:
            students_data.pop(index)
            if saveToFile(students_data):
                messagebox.showinfo("Success", "Student deleted successfully!")
                delete_window.destroy()
                all_student_records() 
            else:
                students_data.insert(index, student)
    
    Button(delete_window, text="Delete", command=perform_delete, font=("Arial", 10, "bold"), bg="red", fg="white").place(x=150, y=250)



def update_students_data():
    if not students_data:
        messagebox.showwarning("Warning", "No student data loaded!") # messagebox if there is no student data 
        return
    
    # new window for student selction 
    update_window = Toplevel(root)
    update_window.title("Update Student")
    update_window.geometry("400x300")  
    
    # instruction Label
    label = Label(update_window, text="Select student to update:", font=("Arial", 12, "bold"))
    label.place(x=20, y=20, width=360, height=30)
    
    # display student list 
    student_listbox = Listbox(update_window, font=("Arial", 10))
    student_listbox.place(x=20, y=60, width=360, height=180)  
    
    
    for student in students_data:
        student_listbox.insert(END, f"{student['id']} - {student['name']}")

    def perform_update():
        selection = student_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to update!")
            return
        
        index = selection[0]
        student = students_data[index]
        update_window.destroy()
        show_update_fields(student, index)

    Button(update_window, text="Update Selected", command=perform_update,
           font=("Arial", 10, "bold"), bg="#1957D2", fg="white").place(x= 150, y=250)

def show_update_fields(student, index):
    update_window = Toplevel(root)
    update_window.title(f"Update {student['name']}")
    update_window.geometry("400x400")
    
    Label(update_window, text=f"Update {student['name']}", font=("Arial", 14, "bold")).place(x=120, y=10)
    
    
    Label(update_window, text=f"Student ID: {student['id']}", anchor="w").place(x=50, y=50)
    
    labels = ["Name:", "Mark 1 (0-20):", "Mark 2 (0-20):", "Mark 3 (0-20):", "Exam Mark (0-100):"]
    entries = []
    
    for i, label_text in enumerate(labels):
        Label(update_window, text=label_text, anchor="w").place(x=50, y=80 + i*30)
        entry = Entry(update_window, width=20)
        entry.place(x=150, y=80 + i*30)
        entries.append(entry)
    
    # Set current values
    entries[0].insert(0, student['name'])
    entries[1].insert(0, student['marks'][0])
    entries[2].insert(0, student['marks'][1])
    entries[3].insert(0, student['marks'][2])
    entries[4].insert(0, student['exam'])
    
    def save_updated_student():
        try:
            name = entries[0].get().strip()
            mark1 = int(entries[1].get())
            mark2 = int(entries[2].get())
            mark3 = int(entries[3].get())
            exam = int(entries[4].get())
            
            if not name:
                messagebox.showerror("Error", "Name is required!")
                return
            
            # Validate mark ranges
            if not (0 <= mark1 <= 20) or not (0 <= mark2 <= 20) or not (0 <= mark3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0-20!")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0-100!")
                return
            
            # Calculate derived values
            coursework_total = mark1 + mark2 + mark3
            total_marks = coursework_total + exam
            percentage = (total_marks / 160) * 100
            grade = studentGrade(percentage)
            
            # Update student data
            students_data[index].update({
                'name': name, 'marks': [mark1, mark2, mark3],
                'coursework_total': coursework_total, 'exam': exam, 'total_marks': total_marks,
                'percentage': percentage, 'grade': grade
            })
            
            # Save to file
            if saveToFile(students_data):
                messagebox.showinfo("Success", "Student updated successfully!")
                update_window.destroy()
                all_student_records()  # Refresh display
            else:
                # Restore original data if save failed by reloading from file
                restored_data = openFile()  # Use a different variable name
                students_data.clear()
                students_data.extend(restored_data)
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks!")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating student: {e}")
    
    # Add the Save button here
    Button(update_window, text="Save Changes", command=save_updated_student, 
           font=("Arial", 10, "bold"), bg="#1957D2", fg="white").place(x=150, y=250)
    
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
empty_btn.place(relx=0.82, rely=0.03, width=120)

# Button 1: Display all student records
all_btn = Button(main_frame,
                 text="All Student Records",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=all_student_records)
all_btn.place(relx=0.78, rely=0.13, width=200)

# Button 2: Search for individual student 
individual_btn = Button(main_frame,
                 text="Individual\n Student Record",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=individual_student_record)
individual_btn.place(relx=0.78, rely=0.23, width=200)

# Button 3: Display highest score student 
highest_btn = Button(main_frame,
                 text="Highest Total Score",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=highest_score)
highest_btn.place(relx=0.78, rely=0.37, width=200)

# Button 4: Display lowest score student 
lowest_btn = Button(main_frame,
                 text="Lowest Total Score",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=lowest_score)
lowest_btn.place(relx=0.78, rely=0.47, width=200)

# Button 5: Sort the Student Records
sort_btn = Button(main_frame,
                 text="Sort Student Records",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=sort_students_data)
sort_btn.place(relx=0.78, rely=0.57, width=200)

# Button 6:  New Student Records
add_btn = Button(main_frame,
                 text="Add Student Record",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=add_students_data)
add_btn.place(relx=0.78, rely=0.67, width=200)

# Button 7: delete Student Records
delete_btn = Button(main_frame,
                 text="Delete\n Student Record",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=delete_student)
delete_btn.place(relx=0.78, rely=0.77, width=200)

# Button 8: Update Student Records
update_btn = Button(main_frame,
                 text="Update Student Record",
                 font=("Arial",12,"bold"),
                 fg="white",
                 bg="#1957D2",
                 relief="raised",
                 command=update_students_data)
update_btn.place(relx=0.78, rely=0.9, width=200)

root.mainloop()
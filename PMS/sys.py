from tkinter import *
import sqlite3 as sql
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps  # type: ignore
import random
import os
import win32api
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import bcrypt


app=Tk()
app.geometry("550x600")
app.resizable(False, False)
app.title("Student Profile Management System (SPMS)")
logo = PhotoImage(file='assets/account-management.png')
app.iconphoto(False, logo)

bg_color = '#06202B' #Background Color

#ICONS
icon1 = Image.open("assets/personal-information.png")
icon1 = icon1.resize((60, 60), Image.Resampling.LANCZOS) 
login_std_img = ImageTk.PhotoImage(icon1)

icon2 = Image.open("assets/admin.png")
icon2 = icon2.resize((60, 60), Image.Resampling.LANCZOS)
login_admin_img = ImageTk.PhotoImage(icon2)

icon3 = Image.open("assets/add-user.png")
icon3 = icon3.resize((60, 60), Image.Resampling.LANCZOS)
login_addu_img = ImageTk.PhotoImage(icon3)

##

icon_std = Image.open("assets/personal-information.png")
icon_std= icon_std.resize((90, 90), Image.Resampling.LANCZOS) 
login_std_img1 = ImageTk.PhotoImage(icon_std)

icon2 = Image.open("assets/admin.png")
icon2 = icon2.resize((90, 90), Image.Resampling.LANCZOS)
login_admin_img1 = ImageTk.PhotoImage(icon2)

#USER Icon
user_icon = Image.open("assets/user.png")
user_icon = user_icon.resize((120, 120), Image.Resampling.LANCZOS)
id_img = ImageTk.PhotoImage(user_icon)

#Padlock ICON
close_eye = PhotoImage(file="assets/close_eye.png")
open_eye = PhotoImage(file="assets/open_eye.png")



#Database
def init_database():
    # Create database and table if they don't exist
    conn = sql.connect("students_acc.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        idnum text PRIMARY KEY,
        password blob,
        name text, 
        age text,                           
        gender text,
        contact_num text,
        yr_lvl text,
        blk text,
        email text,
        image blob
    )
    """)
    conn.commit()
    conn.close()
    
    # Check if table exists and has data
    conn = sql.connect("students_acc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    print(cursor.fetchall())
    conn.close()

#Add Data
def add_data(idnum, password, name, age, gender, contact_num, yr_lvl, blk, email, image):
    #password hashing
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = sql.connect("students_acc.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO students (idnum, password, name, age, gender, contact_num, yr_lvl, blk, email, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (idnum, hashed_pass, name, age, gender, contact_num, yr_lvl, blk, email, image))
        conn.commit()
        messagebox.showinfo("Success", "Profile added successfully!\nID Number: {}\nName: {}".format(idnum, name))
    except sql.IntegrityError:
        messagebox.showerror("Error", "ID number already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        conn.close()


#Draw std card
def draw_std_card(pic, std_data):
    labels = """
ID number:
Name:
Gender:
Age:
Year Level:
Block:
Contact:
Email:
"""

    std_card = Image.open('assets/student_card_frame.png')
    pic = Image.open(pic)

    box_size = (123, 120)
    pic_resized = ImageOps.fit(pic, box_size, method=Image.LANCZOS, centering=(0.5, 0.5))
    
    # Paste resized picture into frame
    std_card.paste(pic_resized, (15, 20))

    #
    draw = ImageDraw.Draw(std_card)
    heading_font = ImageFont.truetype('bahnschrift', 18)
    labels_font = ImageFont.truetype('arialbd', 14)
    data_font = ImageFont.truetype('arial', 13)

    
    draw.text(xy=(150,50),font=heading_font, text='Student Card', fill=(0,0,0))
    draw.multiline_text(xy=(20,130),text=labels, fill=(0,0,0),font=labels_font, spacing=5)
    draw.multiline_text(xy=(150,130),text=std_data, fill=(0,0,0),font=data_font, spacing=6)

    return std_card
#Student card page
def student_card_page(std_card_obj):

    std_card_img = ImageTk.PhotoImage(std_card_obj)

    student_card_page_fm = Frame(app, highlightbackground=bg_color, 
                highlightthickness=3)

    student_card_page_fm.pack(pady=50)
    student_card_page_fm.pack_propagate(False)
    student_card_page_fm.configure(width=450,height=520)

    header_lb = Label(student_card_page_fm, text='Student Card', bg=bg_color, fg='white', font=('Arial Bold', 20))
    header_lb.place(x=0,y=0,width=450) 

    #Close Button
    close_btn = Button(student_card_page_fm, text='X', bg=bg_color, fg='white', font=('Arial Bold', 10), bd=0, command = lambda: student_card_page_fm.destroy() )
    close_btn.place(x=423,y=0)

    # Save function
    def save_card():
        file_path = asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png')], title='Save Student Card As')    
        if file_path:
            std_card_obj.save(file_path)
    #Print function
    def print_card():
        file_path = asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png')], title='Save Student Card As')    
        if file_path:
            std_card_obj.save(file_path)
         # Print the saved image using its path
            win32api.ShellExecute(0, 'print', file_path, None, '.', 0)


    #Student Card Save button
    std_save_card_btn = Button(student_card_page_fm, text='Save Student Card', bg=bg_color, fg='white', font=('Arial Bold', 12), command=save_card)
    std_save_card_btn.place(x=100, y=425, width=200)
    #Download button
    std_card_print_btn = Button(student_card_page_fm, text='  🖨️', bg=bg_color, fg='white', font=('Arial Bold', 12), command=print_card)
    std_card_print_btn.place(x=305, y=425, width=50)
    
    #Display generated std. Card
    std_card_lb = Label(student_card_page_fm, image = std_card_img)
    std_card_lb.pack(pady=75)
    std_card_lb.image = std_card_img

#Welcome Page
def welcome_page():

    #Show info
    def info():
        info_msg = messagebox.showinfo("Info", """This application was inspired from Tkinter Hub
(https://www.youtube.com/@tkinterhub)

𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚍 𝚊𝚗𝚍 𝚖𝚘𝚍𝚒𝚏𝚒𝚎𝚍 𝚋𝚢 𝙺𝚎𝚟𝚒𝚗 𝙱. 𝙱𝚞𝚎𝚗𝚘.
                                       
Icons Credits:
Info icon by Vectoricons - https://www.flaticon.com/free-icons/info
Add & Admin icons by Freepik - https://www.flaticon.com/free-icons/add
Eye icon by Gregor Cresnar - https://www.flaticon.com/free-icons/eye
Hide icon by The Icon Tree - https://www.flaticon.com/free-icons/hide
User icon by kmg design - https://www.flaticon.com/free-icons/user
Account management icon by Dewi Sari - https://www.flaticon.com/free-icons/account-management
                                       """)

 
    ##Link to other pages
    def link_to_std_login_pg():
        wc_page.destroy()
        app.update()
        student_login_page()
    def link_to_adm_login_pg():
        wc_page.destroy()
        app.update()
        admin_login_page()
    def link_to_addprofile_pg():
        wc_page.destroy()
        app.update()
        add_profile_page()


  
    #FRAME
    wc_page=Frame(app, highlightbackground=bg_color, 
                highlightthickness=3)

    wc_page.pack(pady=80)
    wc_page.pack_propagate(False)
    wc_page.configure(width=400,height=420)

    #HEADING
    heading= Label(wc_page,
                    text="Welcome to Student Profile \nManagement System", bg=bg_color, fg='white', font=('Arial Bold', 15))
    heading.place(x=0, y=0, width=400)

    #Info
    info_btn = Button(app, text='ℹ️', font=('Arial Bold', 15),bd=0, command=info)
    info_btn.place(x=12, y=555)

    #BUTTONS
    login_std_button = Button(wc_page, text='Login as Student', bg=bg_color, fg='white', font=('Arial Bold', 15), command=link_to_std_login_pg)
    login_std_button.place(x=120, y=125, width=200)

    login_admin_button = Button(wc_page, text='Login as Admin', bg=bg_color, fg='white', font=('Arial Bold', 15),command=link_to_adm_login_pg)
    login_admin_button.place(x=120, y=220, width=200)

    login_addu_button = Button(wc_page, text='Add Profile', bg=bg_color, fg='white', font=('Arial Bold', 15),command=link_to_addprofile_pg)
    login_addu_button .place(x=120, y=315, width=200)


    login_std_icon = Button(wc_page, image=login_std_img, bd=0)
    login_std_icon.place(x=45, y=110)

    login_admin_icon = Button(wc_page, image=login_admin_img, bd=0)
    login_admin_icon .place(x=45, y=210)

    login_addu_icon = Button(wc_page, image=login_addu_img, bd=0)
    login_addu_icon .place(x=45, y=310)





# Forget Password Page
def forget_pass_page():
    def recover_pass():
        idnum = std_id_ent.get().strip()

        if not idnum:
            messagebox.showwarning("Input Error", "Please enter your ID number.")
            return

        if check_idnum_exist(idnum=idnum):
            try:
                con = sql.connect('students_acc.db')
                cursor = con.cursor()

                # Fetch email
                cursor.execute("SELECT email FROM students WHERE idnum = ?", (idnum,))
                result = cursor.fetchone()
                if not result:
                    con.close()
                    messagebox.showerror('Error', 'ID number found but no email associated.')
                    return
                student_email = result[0]

                confirm = messagebox.askyesno("Confirmation",
                    f"We will send a temporary password to:\n{student_email}\n\nDo you want to continue?")
                if not confirm:
                    con.close()
                    return

                # Generate a secure temporary password
                temp_pass = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789', k=10))
                hashed_temp_pass = bcrypt.hashpw(temp_pass.encode('utf-8'), bcrypt.gensalt())

                # Update password in DB
                cursor.execute("UPDATE students SET password=? WHERE idnum=?", (hashed_temp_pass, idnum))
                con.commit()
                con.close()

                # Load environment variables
                load_dotenv()
                sender_email = os.getenv('EMAIL_ADDRESS')
                sender_pass = os.getenv('EMAIL_PASSWORD')

                if not sender_email or not sender_pass:
                    messagebox.showerror("Error", "Email credentials are not set in environment variables.")
                    return

                # Compose email
                msg = EmailMessage()
                msg['Subject'] = 'Password Recovery - SPMS'
                msg['From'] = sender_email
                msg['To'] = student_email
                msg.set_content(f"""
Hello {student_email},

You requested a password recovery from SPMS.

Your Temporary Password: {temp_pass}

Please log in using this temporary password, then change your password from your dashboard.

SPMS Admin
----------------------------------------------------------------------------
This is a computer generated email, please do not reply.
                """.strip())

                # Send email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender_email, sender_pass)
                    smtp.send_message(msg)

                messagebox.showinfo("Success", f"Temporary password sent successfully to {student_email}!")

            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send email.\n\nDetails: {e}")
        else:
            messagebox.showerror('Try again', 'Invalid ID number!')
    # UI elements should be placed here (like std_id_ent)


    forget_pass_fm = Frame(app, highlightbackground=bg_color, highlightthickness=3)
    forget_pass_fm.place(x=100, y=140, width=350, height=250)

    heading_forgot_pass = Label(forget_pass_fm, text='⚠️Recover Forgotten Password', bg=bg_color, font=('Arial Bodl', 13), fg='white', width=40)
    heading_forgot_pass.place(x=0,y=0)

    close_btn = Button(forget_pass_fm, text='✖️', font=('Bold', 9), bg=bg_color, fg='white', bd=0, command=lambda: forget_pass_fm.destroy())
    close_btn.place(x=320, y=0)

    std_id_lb = Label(forget_pass_fm, text='Enter Student ID number', font=('Calibri Bold', 13), fg=bg_color)
    std_id_lb.place(x=80, y=50)

    std_id_ent = Entry(forget_pass_fm,  font=('Calibri', 11), width=40, justify=CENTER, 
                       highlightbackground='grey',highlightcolor=bg_color, highlightthickness=2)
    std_id_ent.place(x=30, y=75)

    note_lb = Label(forget_pass_fm, text='Via Email Address\nWe will send to you\nyour forgotten passsword.', font=('Arial Italic', 8), fg=bg_color, justify=CENTER)
    note_lb.place(x=107, y= 120)

    next_btn = Button(forget_pass_fm, text='Next', font=('Calibri Bold', 12), fg='white', bg=bg_color, bd=0, width=20, command=recover_pass)
    next_btn.place(x=90, y=180)

#Student Dashboard
def std_dashboard():

    def switch(indicator, page):
        home_ind.config(bg="#153C50")
        std_card_ind.config(bg="#153C50")
        sec_ind.config(bg="#153C50")
        edit_data_btn_ind.config(bg="#153C50")
        del_acc_btn_ind.config(bg="#153C50")
        change_pass_ind.config(bg="#153C50")

        indicator.config(bg="#c3c3c3")

        for widgets in pages_fm.winfo_children():
            widgets.destroy()
            app.update()

        page()

#Dashboard
    dashboard_fm = Frame(app, highlightbackground=bg_color, highlightthickness=3)
    dashboard_fm.pack(padx=3, pady=3)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=550, height=600)

#Side Bar
    side_bar = Frame(dashboard_fm, bg="#153C50", width=150, height=599, highlightbackground=bg_color, highlightthickness=3)
    side_bar.place(x=0, y=0)
#Options
    home_btn = Button(side_bar, text="Home", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0, command=lambda: switch(indicator=home_ind, page=home_page))
    home_btn.place(x=20, y=50)

    home_ind = Label(side_bar, bg="#c3c3c3"
                     )
    home_ind.place(x=10, y=47, width=3, height=37)

    std_card_btn = Button(side_bar, text="Student Card", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0, command=lambda: switch(indicator=std_card_ind, page=std_card_page))
    std_card_btn.place(x=20, y=100)

    std_card_ind = Label(side_bar, bg="#153C50")
    std_card_ind.place(x=10, y=97, width=3, height=37)

    sec_btn = Button(side_bar, text="Security", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0,command=lambda: switch(indicator=sec_ind, page=sec_page))
    sec_btn.place(x=20, y=150)

    sec_ind = Label(side_bar, bg="#153C50")
    sec_ind.place(x=10, y=147, width=3, height=37)

    edit_data_btn = Button(side_bar, text="Edit Data", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0, command=lambda: switch(indicator=edit_data_btn_ind, page=edit_page))
    edit_data_btn.place(x=20, y=200)

    edit_data_btn_ind = Label(side_bar, bg="#153C50")
    edit_data_btn_ind.place(x=10, y=197, width=3, height=37)

    del_acc_btn = Button(side_bar, text="Delete Account", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0, command=lambda: switch(indicator=del_acc_btn_ind, page=del_acc_page))
    del_acc_btn.place(x=20, y=250)

    del_acc_btn_ind = Label(side_bar, bg="#153C50")
    del_acc_btn_ind.place(x=10, y=247, width=3, height=37)

    change_pass_btn = Button(side_bar, text="Change Password", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0, command=lambda: switch(indicator=change_pass_ind, page=change_pass_page))
    change_pass_btn.place(x=20, y=300)
    change_pass_ind = Label(side_bar, bg="#153C50")
    change_pass_ind.place(x=10, y=297, width=3, height=37)

    logout_btn = Button(side_bar, text="Logout", fg='#c3c3c3', font=("Calibri", 13), bg="#153C50",bd=0)
    logout_btn.place(x=20, y=350)
#Pages Frame

    def home_page():
        home_page_fm = Frame(pages_fm)
        home_page_fm.pack(fill=BOTH, expand=True)

        home_page_lb = Label(home_page_fm, text='Home Page', font=('Arial Bold', 15))
        home_page_lb.place(x=100, y=100)

    def std_card_page():
        std_card_page_fm = Frame(pages_fm)
        std_card_page_fm.pack(fill=BOTH, expand=True)

        std_card_page_lb = Label(std_card_page_fm, text='Student Card Page', font=('Arial Bold', 15))
        std_card_page_lb.place(x=100, y=100)

    def sec_page():
        sec_page_fm = Frame(pages_fm)
        sec_page_fm.pack(fill=BOTH, expand=True)

        sec_page_lb = Label(sec_page_fm, text='Security Page', font=('Arial Bold', 15))
        sec_page_lb.place(x=100, y=100)
    
    def edit_page():
        edit_page_fm = Frame(pages_fm)
        edit_page_fm.pack(fill=BOTH, expand=True)

        edit_page_lb = Label(edit_page_fm, text='Edit Data Page', font=('Arial Bold', 15))
        edit_page_lb.place(x=100, y=100)

    def del_acc_page():
        del_acc_page_fm = Frame(pages_fm)
        del_acc_page_fm.pack(fill=BOTH, expand=True)
        del_acc_page_lb = Label(del_acc_page_fm, text='Delete Account Page', font=('Arial Bold', 15))
        del_acc_page_lb.place(x=100, y=100)

    def change_pass_page():
        change_pass_fm = Frame(pages_fm)
        change_pass_fm.pack(fill=BOTH, expand=True)
        change_pass_fm.configure(bg=bg_color)

        Label(change_pass_fm, text="Change Password", font=("Arial Bold", 16), bg=bg_color, fg="white").pack(pady=10)

        # Current Password
        Label(change_pass_fm, text="Current Password:", font=("Calibri", 13), bg=bg_color, fg="white").place(x=30, y=15)
        current_pass_ent = Entry(change_pass_fm, show="*", font=("Calibri", 12), width=30)
        current_pass_ent.place(x=30, y=45)
        def toggle_current_pass():
            if current_pass_ent['show'] == '*':
                current_pass_ent.config(show='')
                show_current_icon.config(image=open_eye)
            else:
                current_pass_ent.config(show='*')
                show_current_icon.config(image=close_eye)
        show_current_icon = Button(change_pass_fm, image=close_eye, border=0, command=toggle_current_pass)
        show_current_icon.place(x=320, y=45, width=28, height=28)

        # New Password
        Label(change_pass_fm, text="New Password:", font=("Calibri", 13), bg=bg_color, fg="white").place(x=30, y=75)
        new_pass_ent = Entry(change_pass_fm, show="*", font=("Calibri", 12), width=30)
        new_pass_ent.place(x=30, y=105)
        def toggle_new_pass():
            if new_pass_ent['show'] == '*':
                new_pass_ent.config(show='')
                show_new_icon.config(image=open_eye)
            else:
                new_pass_ent.config(show='*')
                show_new_icon.config(image=close_eye)
        show_new_icon = Button(change_pass_fm, image=close_eye, border=0, command=toggle_new_pass)
        show_new_icon.place(x=320, y=105, width=28, height=28)

        # Confirm New Password
        Label(change_pass_fm, text="Confirm New Password:", font=("Calibri", 13), bg=bg_color, fg="white").place(x=30, y=135)
        confirm_pass_ent = Entry(change_pass_fm, show="*", font=("Calibri", 12), width=30)
        confirm_pass_ent.place(x=30, y=165)
        def toggle_confirm_pass():
            if confirm_pass_ent['show'] == '*':
                confirm_pass_ent.config(show='')
                show_confirm_icon.config(image=open_eye)
            else:
                confirm_pass_ent.config(show='*')
                show_confirm_icon.config(image=close_eye)
        show_confirm_icon = Button(change_pass_fm, image=close_eye, border=0, command=toggle_confirm_pass)
        show_confirm_icon.place(x=320, y=165, width=28, height=28)

        def update_password():
            current_pass = current_pass_ent.get()
            new_pass = new_pass_ent.get()
            confirm_pass = confirm_pass_ent.get()

            # Get logged-in user ID (assume stored in app.user_id)
            user_id = getattr(app, 'user_id', None)
            if not user_id:
                messagebox.showerror("Error", "User ID not found. Please log in again.")
                return

            if not current_pass or not new_pass or not confirm_pass:
                messagebox.showwarning("Input Error", "Please fill out all fields.")
                return
            if new_pass != confirm_pass:
                messagebox.showerror("Error", "New passwords do not match.")
                return
            if len(new_pass) < 6:
                messagebox.showerror("Error", "New password must be at least 6 characters.")
                return

            # Fetch current hashed password from DB
            conn = sql.connect("students_acc.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM students WHERE idnum=?", (user_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                messagebox.showerror("Error", "User not found.")
                return
            hashed = result[0]
            # bcrypt expects bytes
            if isinstance(hashed, str):
                hashed = hashed.encode('utf-8')
            if not bcrypt.checkpw(current_pass.encode('utf-8'), hashed):
                conn.close()
                messagebox.showerror("Error", "Current password is incorrect.")
                return

            # Hash new password and update
            new_hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE students SET password=? WHERE idnum=?", (new_hashed, user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password updated successfully!")
            current_pass_ent.delete(0, END)
            new_pass_ent.delete(0, END)
            confirm_pass_ent.delete(0, END)

        Button(change_pass_fm, text="Update Password", font=("Calibri Bold", 13), bg="#153C50", fg="white", command=update_password).place(x=30, y=205, width=200, height=35)

    pages_fm = Frame(dashboard_fm)
    pages_fm.place(x=155, y=2, width=380, height=580)
    
   






#Student Login
def student_login_page():

    #Back button
    def back_arrow():
        std_login_page_fm.destroy()
        app.update()
        welcome_page()



    def show_hidden_pass():
        if std_pass_ent['show'] == "*":
            std_pass_ent.config(show='')
            show_icon_pass.config(image=open_eye)
        else:
            std_pass_ent.config(show='*')
            show_icon_pass.config(image=close_eye)

    #Login Account\
    def login_acc():
        verifu_idnum = check_idnum_exist(idnum= std_id_ent.get())
        if verifu_idnum:
            print('ID # is correct')

            verify_pass = check_valid_pass(idnum=std_id_ent.get(), password=std_pass_ent.get())
            if verify_pass:
                print("Password is correct")
                # Store user ID for session
                app.user_id = std_id_ent.get()
                std_login_page_fm.destroy()
                app.update()
                std_dashboard()
            else:
                print("Password is incorrect")
                messagebox.showerror('Invalid Password', 'Please input  a valid password.')
        else:
            print("ID is incorrect")
            messagebox.showerror('Invalid', 'Please input  a valid ID number.')



    #Login page
    #frame
    std_login_page_fm = Frame(app, highlightbackground=bg_color, 
                highlightthickness=3)

    std_login_page_fm.pack(pady=50)

    std_login_page_fm.pack_propagate(False)
    std_login_page_fm.configure(width=450,height=520)

    header_lb = Label(std_login_page_fm, text='Student Login Page', bg=bg_color, fg='white', font=('Arial Bold', 20))
    header_lb.place(x=0,y=0,width=450)

    #ICON
    login_std_icon = Button(std_login_page_fm, image=login_std_img1, bd=0)
    login_std_icon.place(x=170, y=55)



    #Label ID
    std_id_lb = Label(std_login_page_fm, text="Enter Student ID number:",font=("Calibri", 14), fg=bg_color)
    std_id_lb.place(x=125, y=175)
    #Entry_ID
    std_id_ent = Entry(std_login_page_fm, width=37, font=("Calibri", 12), justify=CENTER, highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    std_id_ent.place(x=70, y=225)

    #Label - password
    std_pass_lb = Label(std_login_page_fm, text="Enter Student Password:",font=("Calibri", 14), fg=bg_color)
    std_pass_lb.place(x=125, y=275)

    #Entry_Password
    std_pass_ent = Entry(std_login_page_fm, width=37, font=("Calibri", 12), show="*", justify=CENTER,  highlightcolor=bg_color,
                           highlightbackground='grey', highlightthickness=2) 
    std_pass_ent.place(x=70, y=325)

    #Show Password ICON
    show_icon_pass = Button(std_login_page_fm, image=close_eye, border=0, command=show_hidden_pass)
    show_icon_pass.place(x=350, y=330)

    #Login Button
    login_but = Button(std_login_page_fm, text='Login', font=('Calibri Bold', 13),bg=bg_color, fg='white', width=20, command=login_acc)
    login_but.place(x=125, y=375)

    #FOrgot Password
    fgt_pass = Button(std_login_page_fm, text="⚠\nForgot Password", font=('Calibri', 8), fg=bg_color, border=0, command=forget_pass_page)
    fgt_pass.place(x=175, y=440)

      #Back Button
    back = Button(std_login_page_fm, text="⬅", font=('Calibri', 15), border=0, command=back_arrow)
    back.place(x=3, y=40)


def admin_login_page():

    #back arrow
    def back_arrow():
        adm_login_page_fm.destroy()
        app.update()
        welcome_page()

    def show_hidden_pass():
        if adm_pass_ent['show'] == "*":
            adm_pass_ent.config(show='')
            show_icon_pass.config(image=open_eye)
        else:
            adm_pass_ent.config(show='*')
            show_icon_pass.config(image=close_eye)

    #Login page
    #frame
    adm_login_page_fm = Frame(app, highlightbackground=bg_color, 
            highlightthickness=3)

    adm_login_page_fm.pack(pady=50)

    adm_login_page_fm.pack_propagate(False)
    adm_login_page_fm.configure(width=450,height=520)

    header_lb = Label(adm_login_page_fm, text='Admin Login Page', bg=bg_color, fg='white', font=('Arial Bold', 20))
    header_lb.place(x=0,y=0,width=450)

    #ICON
    adm_std_icon = Button(adm_login_page_fm, image=login_admin_img1, bd=0)
    adm_std_icon.place(x=170, y=55)



    #Label ID
    adm_id_lb = Label(adm_login_page_fm, text="Enter Admin ID number:",font=("Calibri", 14), fg=bg_color)
    adm_id_lb.place(x=125, y=175)
    #Entry_ID
    adm_id_ent = Entry(adm_login_page_fm, width=37, font=("Calibri", 12), justify=CENTER, highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    adm_id_ent.place(x=70, y=225)

    #Label - password
    adm_pass_lb = Label(adm_login_page_fm, text="Enter Admin Password:",font=("Calibri", 14), fg=bg_color)
    adm_pass_lb.place(x=125, y=275)

    #Entry_Password
    adm_pass_ent = Entry(adm_login_page_fm, width=37, font=("Calibri", 12), show="*", justify=CENTER,  highlightcolor=bg_color,  highlightbackground='grey', highlightthickness=2) 
    adm_pass_ent.place(x=70, y=325)

    #Show Password ICON
    show_icon_pass = Button(adm_login_page_fm, image=close_eye, border=0, command=show_hidden_pass)
    show_icon_pass.place(x=350, y=330)



    #Login Button
    login_but = Button(adm_login_page_fm, text='Login', font=('Calibri Bold', 13),bg=bg_color, fg='white', width=20)
    login_but.place(x=125, y=375)

    #FOrgot Password
    fgt_pass = Button(adm_login_page_fm, text="⚠\nForgot Password", font=('Calibri', 8), fg=bg_color, border=0)
    fgt_pass.place(x=175, y=440)

     #Back Button
    back = Button(adm_login_page_fm, text="⬅", font=('Calibri', 15), border=0, command=back_arrow)
    back.place(x=3, y=40)


def check_idnum_exist(idnum):
    conn = sql.connect("students_acc.db")
    cursor = conn.cursor()

    cursor.execute("SELECT idnum FROM students WHERE idnum=?",(idnum,))
    result = cursor.fetchone()

    cursor.close()

    if result:
        return True
    else:
        return False

def check_valid_pass(idnum, password):
    conn = sql.connect("students_acc.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM students WHERE idnum=?", (idnum,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        hashed = result[0]
        # bcrypt expects bytes
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed):
            return True
        else:
            return False
    else:
        return False


def add_profile_page():

    #Pic 
    pic_path = StringVar()

    pic_path.set('')

    def open_pic():
        path = askopenfilename()

        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((118,120)))
            pic_path.set(path)

            add_pic_btn.config(image=img)
            add_pic_btn.image = img
        


    #link to home
    def home():
        add_profile_fm.destroy()
        app.update()
        welcome_page()

    def show_hidden_pass():
        if std_pass_ent['show'] == "*":
            std_pass_ent.config(show='')
            show_icon_pass.config(image=open_eye)
        else:
            std_pass_ent.config(show='*')
            show_icon_pass.config(image=close_eye)

    #Message Box
    def popup():
        mssgbox = messagebox.askyesno("Confirmation", "Are you sure you want to go home?")
        if mssgbox:
            add_profile_fm.destroy()
            app.update()
            home()
        else:
            pass
    def clear_data_in_form():
                        # Clear all input fields after successful submission
            std_name_ent.delete(0, END)
            std_age_ent.delete(0, END)
            std_contact_ent.delete(0, END)
            std_yr_ent.set('')  # Clear combobox
            std_blk_ent.set('')  # Clear combobox
            std_email_ent.delete(0, END)
            std_pass_ent.delete(0, END)
            std_gender.set('male')  # Reset gender to default
            pic_path.set('')  # Clear picture path
            add_pic_btn.config(image=id_img)  # Reset picture button
            gen_id()  # Generate new ID number

    def open_student_card_page(card_obj):
        student_card_page(std_card_obj=card_obj)

            

    #Empty Error Mssg
    def  validation():

        if std_name_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out student's name field.")
        elif std_age_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out student's age field.")
        elif std_contact_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out student's contact number field.")
        elif std_yr_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out student's year level field.")
        elif std_blk_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out student's block field.")
        elif std_email_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out email field.")
        elif std_pass_ent.get() == '':
            errmsg = messagebox.showwarning("Input required", "Please fill out 'Create Account Password' field")                        
        else:

            image = b''
            if pic_path.get() != "":
                resizepic = Image.open(pic_path.get()).resize((118,120))
                resizepic.save('temp_pic.png')

                read_data = open('temp_pic.png', 'rb')

                image = read_data.read()
                read_data.close()
            
            else:
                default_user_icon_path = "assets/user.png"
                read_data = open(default_user_icon_path, 'rb')
                image = read_data.read()
                read_data.close()
                pic_path.set(default_user_icon_path)


            confirm = messagebox.askyesno("Confirmation","Are you sure you want to submit data?")
            if confirm:
                add_data(idnum=std_idnum_ent.get(),
                password=std_pass_ent.get(),
                name=std_name_ent.get(),
                age=std_age_ent.get(),
                gender=std_gender.get(),
                contact_num=std_contact_ent.get(),
                yr_lvl=std_yr_ent.get(),
                blk=std_blk_ent.get(),
                email=std_email_ent.get(),
                image=image)

                #Std Data
            data = f"""
{std_idnum_ent.get()}
{std_name_ent.get()}
{std_gender.get()}
{std_age_ent.get()}
{std_yr_ent.get()}
{std_blk_ent.get()}
{std_contact_ent.get()}
{std_email_ent.get()}
"""
            #Draw student card func
            get_std_card = draw_std_card(pic_path.get(), data)

            open_student_card_page(get_std_card)#Redirect to Save Card Page
            
            clear_data_in_form()#Clear form

            

    #Generate ID num
    def gen_id():
        gen_id = ''
        
        for r in range (5):
            gen_id += str(random.randint(0,9))
        
        print(f"ID num: {gen_id}")

        std_idnum_ent.config(state=NORMAL)
        std_idnum_ent.delete(0, END)
        std_idnum_ent.insert(END, gen_id)
        std_idnum_ent.config(state='readonly')

    #Std Gender
    std_gender = StringVar()
    #Year Level Lists
    yrlvl = ['1st Year','2nd Year', '3rd Year', '4th Year']
    blk = ['A', 'B', 'C', 'D']

    #Add Profile Frame
    add_profile_fm = Frame(app, highlightbackground=bg_color, 
            highlightthickness=3)

    add_profile_fm.pack(pady=8)
    add_profile_fm.pack_propagate(False)
    add_profile_fm.configure(width=530,height=700)

    #Pic
    add_pic_fm = Frame(add_profile_fm, highlightbackground=bg_color, 
            highlightthickness=2)

    add_pic_fm.place(x=10, y=10, height=125, width=125)
    add_pic_btn = Button(add_pic_fm, image=id_img, bd=0, command=open_pic)
    add_pic_btn.pack()
   

    #Student Name Label
    std_name_lb = Label(add_profile_fm, text='Student Name:', font=('Calibri', 15), fg=bg_color)
    std_name_lb.place(x=10, y=150)

    #Student Name Entry
    std_name_ent = Entry(add_profile_fm, width=22, font=("Calibri", 12),
                        highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    std_name_ent.place(x=10, y=180)

    #Gender Label
    std_gender_lb = Label(add_profile_fm, text='Select Gender:', font=('Calibri', 15), fg=bg_color)
    std_gender_lb.place(x=10, y=230)

    #Radio Button
    male_radio_btn = Radiobutton(add_profile_fm, text='Male', font=('Calibri', 15), fg=bg_color, variable=std_gender, value='male')
    male_radio_btn.place(x=10, y=260)

    female_radio_btn = Radiobutton(add_profile_fm, text='Female', font=('Calibri', 15), fg=bg_color, variable=std_gender, value='female')
    female_radio_btn.place(x=90, y=260)

    std_gender.set('male') 

    #Std Age
    std_age_lb = Label(add_profile_fm, text='Student Age:', font=('Calibri', 15), fg=bg_color)
    std_age_lb.place(x=10, y=310)

    std_age_ent = Entry(add_profile_fm, width=22, font=("Calibri", 12),
                        highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    std_age_ent.place(x=10, y=340)

    #Contact #
    std_contact_lb = Label(add_profile_fm, text='Contact Number:', font=('Calibri', 15), fg=bg_color)
    std_contact_lb.place(x=10, y=390)

    std_contact_ent = Entry(add_profile_fm, width=22, font=("Calibri", 12),
                        highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    std_contact_ent.place(x=10, y=420)


    #Year/
    std_yr_lb = Label(add_profile_fm, text='Year Level|', font=('Calibri', 15), fg=bg_color)
    std_yr_lb.place(x=10, y=470)

    std_yr_ent = ttk.Combobox(add_profile_fm, font=("Calibri", 12), values=yrlvl) 
    std_yr_ent.current(0)
    std_yr_ent.place(x=10, y=500, width= 90, height= 30)

    #/Block
    std_blk_lb = Label(add_profile_fm, text='Block:', font=('Calibri', 15), fg=bg_color)
    std_blk_lb.place(x=110, y=470)

    std_blk_ent = ttk.Combobox(add_profile_fm, font=("Calibri", 12), values=blk) 
    std_blk_ent.current(0)
    std_blk_ent.place(x=100, y=500, width= 90, height= 30)

    #Student ID#

    std_idnum = Label(add_profile_fm, text='Student ID Number:', font=('Times New Roman', 15), fg=bg_color)
    std_idnum.place(x=260, y=20)

    std_idnum_ent = Entry(add_profile_fm, font=('Times New Roman', 18), fg=bg_color, bd=0)
    std_idnum_ent.place(x=420, y=20, width=90)

    std_idnum_ent.config(state='readonly')
    gen_id()

    #Note
    std_idnum_note = Label(add_profile_fm, text='*Automatically Generated ID Number\n Remember using this ID number\n When Logging in to account. ',
                            font=('Calibri Italic', 11), fg='grey', anchor='w', justify='left')
    std_idnum_note.place(x=260, y=50)

    #Student Email Label
    std_email_lb = Label(add_profile_fm, text='Student Email Address:', font=('Calibri', 15), fg=bg_color)
    std_email_lb.place(x=260, y=150)

    #Student Email Entry
    std_email_ent = Entry(add_profile_fm, width=22, font=("Calibri", 12),
                        highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    std_email_ent.place(x=260, y=180)
    #Note
    std_email_note = Label(add_profile_fm, text='*Via Email Address student\n can receive account\n in case forgetting password and also\n student will get future notifications. ',
                            font=('Calibri Italic', 11), fg='grey', anchor='w', justify='left')
    std_email_note.place(x=260, y=220)


    #Student Password Label
    std_pass_lb = Label(add_profile_fm, text='Create Account Password:', font=('Calibri', 15), fg=bg_color)
    std_pass_lb.place(x=260, y=310)

    #Student password Entry
    std_pass_ent = Entry(add_profile_fm, width=22, font=("Calibri", 12),
                        highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2) 
    std_pass_ent.place(x=260, y=340)
    #Note
    std_pass_note = Label(add_profile_fm, text='*Via Email Address student\n can receive account\n in case forgetting password and also\n student will get future notifications. ',
                            font=('Calibri Italic', 11), fg='grey', anchor='w', justify='left')
    std_pass_note.place(x=260, y=380)


    #Show Password ICON
    show_icon_pass = Button(add_profile_fm, image=close_eye, border=0, command=show_hidden_pass)
    show_icon_pass.place(x=450, y=350)
    
    #Home Button
    home_btn = Button(add_profile_fm, text='Home', fg='white', bg='grey', font=('Bold', 12), command=popup)
    home_btn.place(x=260, y=500)

    submit_btn = Button(add_profile_fm, text='Submit', fg='white', bg=bg_color, font=('Bold', 12), command=validation)
    submit_btn.place(x=380, y=500)

    divider = Frame(add_profile_fm, bg='grey', height=550)
    divider.place(x=220, y=20, width=2)



# forget_pass_page()
# std_dashboard()
welcome_page()
app.mainloop()

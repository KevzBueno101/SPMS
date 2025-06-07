from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # type: ignore
import sqlite3 as sql

# -----Credit Section----#
    #<a href="https://www.flaticon.com/free-icons/info" title="info icons">Info icons created by Vectoricons - Flaticon</a>
    #<a href="https://www.flaticon.com/free-icons/add" title="add icons">Add icons created by Freepik - Flaticon</a>
    #<a href="https://www.flaticon.com/free-icons/admin" title="admin icons">Admin icons created by Freepik - Flaticon</a>
    #<a href="https://www.flaticon.com/free-icons/eye" title="eye icons">Eye icons created by Gregor Cresnar - Flaticon</a>
    #<a href="https://www.flaticon.com/free-icons/hide" title="hide icons">Hide icons created by The Icon Tree - Flaticon</a>
    #<a href="https://www.flaticon.com/free-icons/user" title="user icons">User icons created by kmg design - Flaticon</a>
#System Inspired by Tkinterhub
#-----------------------#

app=Tk()
app.geometry("550x600")
app.resizable(False, False)
app.title("Profile Management System (PMS)")


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





def welcome_page():

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
    login_but = Button(std_login_page_fm, text='Login', font=('Calibri Bold', 13),bg=bg_color, fg='white', width=20)
    login_but.place(x=125, y=375)

    #FOrgot Password
    fgt_pass = Button(std_login_page_fm, text="⚠\nForgot Password", font=('Calibri', 8), fg=bg_color, border=0)
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




def add_profile_page():

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
            welcome_page()
        else:
            pass


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
    add_pic_btn = Button(add_pic_fm, image=id_img, bd=0)
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
    std_yr_lb = Label(add_profile_fm, text='Year Level/', font=('Calibri', 15), fg=bg_color)
    std_yr_lb.place(x=10, y=470)

    std_yr_ent = ttk.Combobox(add_profile_fm, font=("Calibri", 12), values=yrlvl) 
    std_yr_ent.place(x=10, y=500, width= 90, height= 30)

    #/Block
    std_blk_lb = Label(add_profile_fm, text='Block:', font=('Calibri', 15), fg=bg_color)
    std_blk_lb.place(x=110, y=470)

    std_blk_ent = ttk.Combobox(add_profile_fm, font=("Calibri", 12), values=blk) 
    std_blk_ent.place(x=100, y=500, width= 90, height= 30)

    #Student ID#

    std_idnum = Label(add_profile_fm, text='Student ID Number:', font=('Times New Roman', 15), fg=bg_color)
    std_idnum.place(x=260, y=20)

    std_idnum_ent = Entry(add_profile_fm, font=('Times New Roman', 18), fg=bg_color, bd=0)
    std_idnum_ent.place(x=420, y=20, width=90)

    std_idnum_ent.insert(END, '12345')
    std_idnum_ent.config(state='readonly')


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

    home_btn = Button(add_profile_fm, text='Submit', fg='white', bg=bg_color, font=('Bold', 12))
    home_btn.place(x=380, y=500)

welcome_page()

app.mainloop()

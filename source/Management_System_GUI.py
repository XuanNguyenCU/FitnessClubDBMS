# Xuan Nguyen 101228417
# COMP 3005 - Health and Fitness Management System

import psycopg2
import tkinter as tk
from tkinter import messagebox, simpledialog

def change_on_hover(button, colorOnHover, colorOnLeave):
    # Adjusting the background of the button on hover
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))

    # Adjusting the background of the button when it is not hovered over
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))
    

def login_page():
    window = tk.Tk()
    window.title("Health and Fitness Management System Login")
    window.geometry("700x500")

    main_frame = tk.Frame(window)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Username
    username_label = tk.Label(main_frame, text="Username", font=("Arial", 12))
    username_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
    
    username_entry = tk.Entry(main_frame, font=("Arial", 12))
    username_entry.grid(row=0, column=1, pady=(0, 10), padx=(5, 0))

    # Password
    password_label = tk.Label(main_frame, text="Password", font=("Arial", 12))
    password_label.grid(row=1, column=0, pady=(0, 10), sticky="w")
    
    password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
    password_entry.grid(row=1, column=1, pady=(0, 10), padx=(5, 0))

    # Login Button
    login_button = tk.Button(main_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), window))
    # Adjusting the button to be directly under the password box
    login_button.grid(row=2, column=1, pady=(10, 0))
    login_button.config(font=("Arial", 12), bg="#4CAF50", fg="white", padx=40, pady=5)

    # Centering the main_frame
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    window.mainloop()


def login(username, password, window):
    global login_result

    conn = psycopg2.connect(**db_config)

    cur = conn.cursor()
    cur.execute("SELECT * FROM \"Users\" WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    if result is not None:
        login_result = result
        window.destroy()
    else:
        messagebox.showerror("Error", "Invalid username or password")
    cur.close()
    conn.close()


def admin_page():
    window = tk.Tk()
    window.title("Admin Page")
    window.geometry("950x650")

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    global rooms_listbox
    global equipment_status_entry
    global room
    global events_listbox
    global event_name_entry
    global event_date_entry
    global event_description_entry
    global event_trainer_entry
    global event_room_entry

    # Using Frames to organize the layout
    events_frame = tk.Frame(window)
    rooms_frame = tk.Frame(window)
    equipment_frame = tk.Frame(window)
    logout_frame = tk.Frame(window)

    # Grid layout for frames
    events_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    rooms_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    equipment_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    logout_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

    # Ensure that frames expand correctly
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    # Widgets for events_frame using grid
    events_label = tk.Label(events_frame, text="Scheduled Events")
    events_label.grid(row=0, column=0, sticky="ew")

    events_listbox = tk.Listbox(events_frame, width=60, height=10)
    events_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    # Widgets for rooms_frame using grid
    rooms_label = tk.Label(rooms_frame, text="Rooms")
    rooms_label.grid(row=0, column=0, sticky="ew")

    rooms_listbox = tk.Listbox(rooms_frame, width=40, height=10)
    rooms_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    # Widgets for equipment_frame using grid
    equipment_status_label = tk.Label(equipment_frame, text="Enter in the textbox to set new status for the selected room.")
    equipment_status_label.grid(row=0, column=0, sticky="ew")

    equipment_status_entry = tk.Entry(equipment_frame)
    equipment_status_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    # Ensure events_frame and rooms_frame columns expand and fill
    events_frame.columnconfigure(0, weight=1)
    rooms_frame.columnconfigure(0, weight=1)
    equipment_frame.columnconfigure(0, weight=1)

    # Event Form Setup in the rooms_frame for better layout integration
    event_form = tk.LabelFrame(rooms_frame, text="Create Event")
    event_form.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    # Event Form Widgets
    tk.Label(event_form, text="Event Name").grid(row=0, column=0, sticky="w")
    event_name_entry = tk.Entry(event_form)
    event_name_entry.grid(row=0, column=1, sticky="ew")

    tk.Label(event_form, text="Event Date").grid(row=1, column=0, sticky="w")
    event_date_entry = tk.Entry(event_form)
    event_date_entry.grid(row=1, column=1, sticky="ew")

    tk.Label(event_form, text="Event Description").grid(row=2, column=0, sticky="w")
    event_description_entry = tk.Entry(event_form)
    event_description_entry.grid(row=2, column=1, sticky="ew")

    tk.Label(event_form, text="Trainer ID").grid(row=3, column=0, sticky="w")
    event_trainer_entry = tk.Entry(event_form)
    event_trainer_entry.grid(row=3, column=1, sticky="ew")

    tk.Label(event_form, text="Room ID").grid(row=4, column=0, sticky="w")
    event_room_entry = tk.Entry(event_form)
    event_room_entry.grid(row=4, column=1, sticky="ew")

        # Stylish Set Status Button
    set_status_button = tk.Button(equipment_frame, text="Set Equipment Status", command=lambda: set_status(),
                                  font=('Helvetica', 12, 'bold'), bg='#007bff', fg='white', padx=10, pady=5)
    set_status_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    # Adding hover effect to Set Status Button
    change_on_hover(set_status_button, '#0056b3', '#007bff')

    # Stylish Logout Button
    logout_button = tk.Button(logout_frame, text="Logout", command=window.destroy,
                              font=('Helvetica', 12, 'bold'), bg='#f44336', fg='white', padx=10, pady=5)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Adding hover effect to Logout Button
    change_on_hover(logout_button, '#d32f2f', '#f44336')

    # Stylish Create Event Button
    create_event_button = tk.Button(event_form, text="Create Event", command=lambda: create_event(),
                                    font=('Helvetica', 12, 'bold'), bg='#4CAF50', fg='white', padx=10, pady=5)
    create_event_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    # Adding hover effect to Create Event Button
    change_on_hover(create_event_button, '#45a049', '#4CAF50')

    # Stylish Delete Event Button
    delete_event_button = tk.Button(event_form, text="Delete Event", command=lambda: delete_event(),
                                    font=('Helvetica', 12, 'bold'), bg='#ff5722', fg='white', padx=10, pady=5)
    delete_event_button.grid(row=6, column=0, columnspan=2, pady=(5, 10))

    # Adding hover effect to Delete Event Button
    change_on_hover(delete_event_button, '#e64a19', '#ff5722')

    # Populate events listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    for event in events:
        
        # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    # Populate rooms listbox
    cur.execute("SELECT * FROM \"Rooms\"")
    rooms = cur.fetchall()
    for room in rooms:
       rooms_listbox.insert(tk.END, f"{room[0]}: {room[1]}, Status: {room[2]}")

    cur.close()
    conn.close()
    window.mainloop()


# Create an event in the admin page
def create_event():

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    event_name = event_name_entry.get()
    event_date = event_date_entry.get()
    event_description = event_description_entry.get()
    event_trainer = event_trainer_entry.get()
    event_room = event_room_entry.get()

    cur.execute("INSERT INTO \"GroupEvents\" (event_name, event_date, event_description, trainer_id, room_id) VALUES (%s, %s, %s, %s, %s)",
                (event_name, event_date, event_description, event_trainer, event_room))

    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox.delete(0, tk.END)
    for event in events:
       # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]
        
        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()


# Delete an event in the admin page
def delete_event():

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    selected_event_index = events_listbox.curselection()
    if len(selected_event_index) == 0:
        messagebox.showerror("Error", "No event selected")
        return

    # Get the selected event
    selected_event_id = events_listbox.get(selected_event_index)[0]

    # Delete the selected event from the database
    cur.execute("DELETE FROM \"GroupEvents\" WHERE event_id = %s", (selected_event_id,))

    # Commit the changes
    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox.delete(0, tk.END)
    for event in events:
       # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()


# Set status in the admin page
def set_status():
    # Get the selected room ID
    selected_room_index = rooms_listbox.curselection()
    if len(selected_room_index) == 0:
        messagebox.showerror("Error", "No room selected")
        return
    selected_room_id = rooms_listbox.get(selected_room_index)[0] # Extract the room ID from the string

    # Get the new status
    new_status = equipment_status_entry.get()

    # Update the status of the selected room in the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("UPDATE \"Rooms\" SET equipment_status = %s WHERE room_id = %s", (new_status, selected_room_id))
    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"Rooms\"")
    rooms = cur.fetchall()
    rooms_listbox.delete(0, tk.END)
    for room in rooms:
        rooms_listbox.insert(tk.END, f"{room[0]}: {room[1]}, Status: {room[2]}")
    cur.close()
    conn.close()


def member_page(user_id):
    global events_listbox_member
    global details_listbox
    global fitness_goal_entry
    conn = psycopg2.connect(**db_config)

    cur = conn.cursor()
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]
    cur.execute("SELECT * FROM \"MemberDetails\" WHERE member_id = %s", (member_id,))
    member_details = cur.fetchone()
    cur.execute("SELECT s.session_id, s.trainer_id, d.session_date, d.session_time, d.session_status, u.username FROM \"Session\" s JOIN \"SessionDetails\" d ON s.session_id = d.session_id JOIN \"Users\" u ON s.trainer_id = u.user_id WHERE s.member_id = %s", (member_id,))
    sessions = cur.fetchall()
    sessions_listbox_items = [f"Date: {session[2]}, Time: {session[3]}, Trainer: {session[5]}, Status: {session[4]}" for session in sessions]

    # Fetching necessary data
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]
    cur.execute("SELECT * FROM \"MemberDetails\" WHERE member_id = %s", (member_id,))
    member_details = cur.fetchone()
    cur.execute("""
        SELECT s.session_id, s.trainer_id, d.session_date, d.session_time, d.session_status, u.username
        FROM \"Session\" s
        JOIN \"SessionDetails\" d ON s.session_id = d.session_id
        JOIN \"Users\" u ON s.trainer_id = u.user_id
        WHERE s.member_id = %s
    """, (member_id,))
    sessions = cur.fetchall()
    sessions_listbox_items = [f"Date: {session[2]}, Time: {session[3]}, Trainer: {session[5]}, Status: {session[4]}" for session in sessions]

    window = tk.Tk()
    window.title("Member Page")
    window.geometry("800x700")

    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Member details section using a Listbox for selectable items
    details_frame = tk.LabelFrame(main_frame, text="Member Details", padx=10, pady=10)
    details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    # Member details section
    details_listbox = tk.Listbox(details_frame, height=8)
    details_listbox.pack(fill=tk.BOTH, expand=True)

    member_details = [
        f"Member ID: {member_details[0]}",
        f"First Name: {member_details[1]}",
        f"Last Name: {member_details[2]}",
        f"Fitness Goals: {member_details[3]}",
        f"Health Metrics: {member_details[4]}",
        f"Exercise Routine: {member_details[5]}",
        f"Fitness Achievements: {member_details[6]}",
        f"Billing Info: {member_details[7]}",
        f"Loyalty Points: {member_details[8]}"
    ]
    
    for detail in member_details:
        details_listbox.insert(tk.END, detail)

    # Sessions section
    sessions_frame = tk.LabelFrame(main_frame, text="Your Sessions", padx=10, pady=10)
    sessions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    sessions_listbox = tk.Listbox(sessions_frame, height=5)
    for item in sessions_listbox_items:
        sessions_listbox.insert(tk.END, item)
    sessions_listbox.pack(fill=tk.BOTH, expand=True)

    # Events section
    events_frame = tk.LabelFrame(main_frame, text="Upcoming Events", padx=10, pady=10)
    events_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    events_listbox_member = tk.Listbox(events_frame, height=5)
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    for event in events:  # Assume sessions variable holds events for this example
        # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox_member.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    events_listbox_member.pack(fill=tk.BOTH, expand=True)
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(fill=tk.X, pady=10)

    fitness_goal_label = tk.Label(details_frame, text="Enter new value:")
    fitness_goal_label.pack(side=tk.TOP, fill=tk.X)

    fitness_goal_entry = tk.Entry(details_frame)
    fitness_goal_entry.pack(side=tk.TOP, fill=tk.X)

    set_goal_button = tk.Button(details_frame, text="Update Personal Info", command=lambda: update_personal(user_id))
    set_goal_button.pack(pady=10)

    # Register and Logout buttons

    register_button = tk.Button(buttons_frame, text="Register for Event", 
                                command=lambda: register_for_event(member_id, events_listbox_member.get(tk.ACTIVE)[0]),
                                font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', padx=10, pady=5)
    register_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

    logout_button = tk.Button(buttons_frame, text="Logout", 
                              command=window.destroy,
                              font=('Arial', 12, 'bold'), bg='#f44336', fg='white', padx=10, pady=5)
    logout_button.pack(side=tk.RIGHT, padx=10, pady=10, expand=True)

    change_on_hover(register_button, '#45a049', '#4CAF50')
    change_on_hover(logout_button, '#d32f2f', '#f44336')

    cur.close()
    conn.close()
    window.mainloop()

def update_personal(user_id):

    conn = psycopg2.connect(**db_config)

    details_index = details_listbox.curselection()
    if len(details_index ) == 0:
        messagebox.showerror("Error", "No room selected")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]

    new_status = fitness_goal_entry.get()

    # Update the status of the selected room in the database
    cur = conn.cursor()
    cur.execute("UPDATE \"MemberDetails\" SET fitness_goals = %s WHERE member_id = %s", (new_status, member_id))
    conn.commit()

    cur.execute("SELECT * FROM \"MemberDetails\" WHERE member_id = %s", (member_id,))
    member_details = cur.fetchone()

    member_details = [
        f"Member ID: {member_details[0]}",
        f"First Name: {member_details[1]}",
        f"Last Name: {member_details[2]}",
        f"Fitness Goals: {member_details[3]}",
        f"Health Metrics: {member_details[4]}",
        f"Exercise Routine: {member_details[5]}",
        f"Fitness Achievements: {member_details[6]}",
        f"Billing Info: {member_details[7]}",
        f"Loyalty Points: {member_details[8]}"
    ]
    
    # Update the status in the listbox
    details_listbox.delete(0, tk.END)
    for detail in member_details:
        details_listbox.insert(tk.END, detail)
        print(detail)
    cur.close()
    conn.close()
    

# Register for event in member page
def register_for_event(member_id, event_id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO \"MemberGroupEvent\" (member_id, event_id) VALUES (%s, %s)", (member_id, event_id))
    conn.commit()

    #Update list by reloading contents
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox_member.delete(0, tk.END)
    for event in events:
        # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox_member.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()


def set_trainer_availability(conn, trainer_id):
    new_availability = simpledialog.askstring("Availability", "Enter your available times (e.g., 'Monday 10-12'): ")
    if new_availability:
        with conn.cursor() as cur:
            cur.execute("UPDATE \"TrainerDetails\" SET training_schedule = %s WHERE trainer_id = %s", (new_availability, trainer_id))
            conn.commit()
        messagebox.showinfo("Success", "Your availability has been updated.")

def view_member_profile(conn):
    member_name = simpledialog.askstring("Member Search", "Enter the member's first name to search: ")
    if member_name:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT md.* 
            FROM \"MemberDetails\" md
            JOIN \"Members\" m ON md.member_id = m.member_id
            WHERE md.first_name ILIKE %s
            """, (f'%{member_name}%',))
            member_details = cur.fetchall()
        print(member_details)
            
        if member_details:
            details_str = "\n\n".join([
                f"Member ID: {detail[0]}\n"
                f"First Name: {detail[1]}\n"
                f"Last Name: {detail[2]}\n"
                f"Fitness Goals: {detail[3]}\n"
                f"Health Metrics: {detail[4]}\n"
                f"Exercise Routine: {detail[5]}\n"
                f"Fitness Achievements: {detail[6]}\n"
                f"Billing Info: {detail[7]}" 
                for detail in member_details])
            messagebox.showinfo("Member Profile", details_str)

        else:
            messagebox.showinfo("Member Profile", "No member found with that name.")


def get_trainer_id(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT trainer_id FROM \"Trainers\" WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        return result[0] if result else None

def trainer_page(user_id):
    conn = psycopg2.connect(**db_config)
    trainer_id = get_trainer_id(conn, user_id)

    if trainer_id is None:
        messagebox.showerror("Error", "Trainer ID not found for the given User ID.")
        conn.close()
        return

    window = tk.Tk()
    window.title("Trainer Page")
    window.geometry("600x400")

    # Schedule Management
    schedule_frame = tk.LabelFrame(window, text="Schedule Management")
    schedule_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    set_availability_button = tk.Button(schedule_frame, text="Set Availability",
                                        command=lambda: set_trainer_availability(conn, trainer_id),
                                        font=('Arial', 12, 'bold'), # Setting the font style, size, and weight
                                        bg='#4CAF50', # Background color
                                        fg='white', # Font color
                                        padx=10, # Horizontal padding
                                        pady=5) # Vertical padding
    set_availability_button.pack(pady=10) # Adding some padding around the button for better spacing

    # Member Profile Viewing
    profile_frame = tk.LabelFrame(window, text="Member Profile Viewing")
    profile_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    view_profile_button = tk.Button(profile_frame, text="View Member Profile",
                                    command=lambda: view_member_profile(conn),
                                    font=('Arial', 12, 'bold'), # Font styling
                                    bg='#007BFF', # Background color, using a blue shade
                                    fg='white', # Font color
                                    padx=10, # Horizontal padding
                                    pady=5) # Vertical padding
    view_profile_button.pack(pady=10) # Adding some vertical padding

    window.mainloop()
    conn.close()


# Setting up the database
def setupDB():

    # Connect to the default postgres database
    conn = psycopg2.connect(**db_config)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the SQL file
    with open('DDL.sql', 'r') as f:
        sql_file = f.read()

    # Execute the SQL file
    cur.execute(sql_file)

    # Commit and close
    cur.close()
    conn.commit()
    conn.close()


# Populating the database
def populateDB():

    conn = psycopg2.connect(**db_config)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the SQL file
    with open('DML.sql', 'r') as f:
        sql_file = f.read()

    # Execute the SQL file
    cur.execute(sql_file)

    # Close communication with the default postgres database
    cur.close()
    conn.commit()
    conn.close()

db_config = {}
def main():

    global db_config
    login_successful = False
    while not login_successful:
        db_config = {
            'database': input("Enter the database name: "),
            'user': input("Enter your pgadmin 4 username: "),
            'password': input("Enter your pgadmin 4 password: "),
        }
        try:
            setupDB()
            populateDB()
            print("Database setup and population successful.")
            login_successful = True 

        except Exception as e:
            print("Failed to set up database or log in: " + str(e))
            continue  # Prompt again for database details

    while (True):
        login_page()
        user_id = login_result[0]
        user_type = login_result[4]
    
        if (user_type == "admin"):
            print("Admin Login")
            admin_page()

        elif (user_type == "trainer"):
            print("Trainer login")
            trainer_page(user_id)

        elif (user_type == "member"):
            print("Member login")
            member_page(user_id)


# main guard
if __name__ == "__main__":
   main()

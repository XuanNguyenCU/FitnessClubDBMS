import psycopg2, datetime
from decimal import Decimal
import tkinter as tk
from tkinter import messagebox, simpledialog

def change_on_hover(button, colorOnHover, colorOnLeave):
    # Adjusting the background of the button on hover
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))

    # Adjusting the background of the button when it is not hovered over
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

def registration_page():
    registration_window = tk.Toplevel()
    registration_window.title("Registration")
    registration_window.geometry("600x500")

    tk.Label(registration_window, text="Username:").pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    tk.Label(registration_window, text="Password:").pack()
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack()

    tk.Label(registration_window, text="Email:").pack()
    email_entry = tk.Entry(registration_window)
    email_entry.pack()

    tk.Label(registration_window, text="First Name:").pack()
    first_name_entry = tk.Entry(registration_window)
    first_name_entry.pack()

    tk.Label(registration_window, text="Last Name:").pack()
    last_name_entry = tk.Entry(registration_window)
    last_name_entry.pack()

    tk.Label(registration_window, text="Fitness Goals:").pack()
    fitness_goals_entry = tk.Entry(registration_window)
    fitness_goals_entry.pack()

    tk.Label(registration_window, text="Exercise Routine:").pack()
    exercise_routine_entry = tk.Entry(registration_window)
    exercise_routine_entry.pack()

    tk.Label(registration_window, text="Blood Pressure:").pack()
    blood_pressure_entry = tk.Entry(registration_window)
    blood_pressure_entry.pack()

    tk.Label(registration_window, text="Weight (kg):").pack()
    weight_entry = tk.Entry(registration_window)
    weight_entry.pack()

    tk.Label(registration_window, text="Height (cm):").pack()
    height_entry = tk.Entry(registration_window)
    height_entry.pack()

    submit_button = tk.Button(registration_window, text="Submit", command=lambda: register_user(
        username_entry.get(),
        password_entry.get(),
        email_entry.get(),
        first_name_entry.get(),
        last_name_entry.get(),
        fitness_goals_entry.get(),
        exercise_routine_entry.get(),
        blood_pressure_entry.get(),
        weight_entry.get(),
        height_entry.get(),
        registration_window))
    submit_button.pack(pady=10)  # Adding some padding around the button
    submit_button.config(font=("Arial", 12, 'bold'), bg="#4CAF50", fg="white", padx=16, pady=8)
    change_on_hover(submit_button, '#45a049', '#4CAF50')


def register_user(username, password, email, first_name, last_name, fitness_goals, exercise_routine, blood_pressure, weight, height, window):
    try:
        conn = psycopg2.connect(**db_config)
        with conn.cursor() as cur:
            # Insert into Users table
            cur.execute("""
                INSERT INTO "Users" (username, password, email, user_type) 
                VALUES (%s, %s, %s, 'member') RETURNING user_id
            """, (username, password, email))
            user_id = cur.fetchone()[0]

            # Insert into Members table
            cur.execute("""
                INSERT INTO "Members" (user_id, first_name, last_name, fitness_goals, exercise_routine, billing_info, loyalty_points) 
                VALUES (%s, %s, %s, %s, %s, 10.00, 1)
            """, (user_id, first_name, last_name, fitness_goals, exercise_routine))

            # Insert into HealthMetrics table
            cur.execute("""
                INSERT INTO "HealthMetrics" (blood_pressure, weight, height) 
                VALUES (%s, %s, %s)
            """, (blood_pressure, weight, height))
            conn.commit()
        window.destroy()

        messagebox.showinfo("Registration Success", "You have successfully registered!")
    except Exception as e:
        messagebox.showerror("Error", "Registration failed: " + str(e))
        window.destroy()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


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
    login_button.grid(row=2, column=1, pady=(10, 0))
    login_button.config(font=("Arial", 12, 'bold'), bg="#4CAF50", fg="white", padx=40, pady=5)
    change_on_hover(login_button, '#45a049', '#4CAF50')

    # Centering the main_frame
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    registration_button = tk.Button(window, text="Register", command=lambda: registration_page(), bg='#007bff', fg='white', font=('Arial', 12, 'bold'))
    registration_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)  # Aligns to top left corner
    change_on_hover(registration_button, '#0056b3', '#007bff')

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
    global event_time_entry
    global event_description_entry
    global event_trainer_entry
    global event_room_entry

    events_frame = tk.Frame(window)
    rooms_frame = tk.Frame(window)
    equipment_frame = tk.Frame(window)
    logout_frame = tk.Frame(window)

    # Layout frames
    events_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)  # Allow rowspan for events_frame to occupy two rows
    rooms_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    equipment_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    logout_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

    # Configure window grid
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    # Scheduled Events Listbox
    events_label = tk.Label(events_frame, text="Scheduled Group Events")
    events_label.pack(fill=tk.X)

    events_listbox = tk.Listbox(events_frame, width=60, height=10)
    events_listbox.pack(fill=tk.BOTH, expand=True)

    # Billing Information Listbox
    billing_info_label = tk.Label(events_frame, text="Billing Information from All Members")
    billing_info_label.pack(fill=tk.X)

    billing_info_listbox = tk.Listbox(events_frame, width=60, height=8)
    billing_info_listbox.pack(fill=tk.BOTH, expand=True)

    # Query database for billing_info from all members
    cur.execute("""
    SELECT m.first_name || ' ' || m.last_name || ': ' || m.billing_info AS billing_info
    FROM "Members" m
    """)
    billing_infos = cur.fetchall()

    # Populate the billing_info_listbox
    for billing_info in billing_infos:
        billing_info_listbox.insert(tk.END, billing_info[0])

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

    tk.Label(event_form, text="Event Description").grid(row=3, column=0, sticky="w")
    event_description_entry = tk.Entry(event_form)
    event_description_entry.grid(row=3, column=1, sticky="ew")

    tk.Label(event_form, text="Trainer ID").grid(row=4, column=0, sticky="w")
    event_trainer_entry = tk.Entry(event_form)
    event_trainer_entry.grid(row=4, column=1, sticky="ew")

    tk.Label(event_form, text="Room ID").grid(row=5, column=0, sticky="w")
    event_room_entry = tk.Entry(event_form)
    event_room_entry.grid(row=5, column=1, sticky="ew")

    set_status_button = tk.Button(equipment_frame, text="Set Equipment Status", command=lambda: set_status(),
                                  font=('Arial', 12, 'bold'), bg='#007bff', fg='white', padx=10, pady=5)
    set_status_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    # Adding hover effect to Set Status Button
    change_on_hover(set_status_button, '#0056b3', '#007bff')

    logout_button = tk.Button(logout_frame, text="Logout", command=window.destroy,
                              font=('Arial', 12, 'bold'), bg='#f44336', fg='white', padx=10, pady=5)
    logout_button.pack(side=tk.RIGHT, padx=10)
    change_on_hover(logout_button, '#d32f2f', '#f44336')

    # Stylish Create Event Button
    create_event_button = tk.Button(event_form, text="Create Event", command=lambda: create_event(),
                                    font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', padx=10, pady=5)
    create_event_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    change_on_hover(create_event_button, '#45a049', '#4CAF50')

    # Stylish Delete Event Button
    delete_event_button = tk.Button(event_form, text="Delete Event", command=lambda: delete_event(),
                                    font=('Arial', 12, 'bold'), bg='#ff5722', fg='white', padx=10, pady=5)
    delete_event_button.grid(row=7, column=0, columnspan=2, pady=(5, 10))
    change_on_hover(delete_event_button, '#e64a19', '#ff5722')

    # Populate events listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    for event in events:
        
        # Fetch the trainer name and room using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[5],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT room_type FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in the {room_name}. Date: {event[2]}. Details: {event[3]}. {member_count} member(s) attending.")

    # Populate rooms listbox
    cur.execute("SELECT * FROM \"Rooms\"")
    rooms = cur.fetchall()
    for room in rooms:
       rooms_listbox.insert(tk.END, f"{room[0]}: {room[1]}, Status: {room[2]}")

    cur.close()
    conn.close()
    window.mainloop()


# Create a group event as an admin
def create_event():

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    try:
        # Get the event details from user inputs
        event_name = event_name_entry.get()
        event_date = event_date_entry.get() # Adjust the format as necessary
        event_description = event_description_entry.get()
        trainer_id = int(event_trainer_entry.get())
        room_id = int(event_room_entry.get())

        # Start a transaction
        cur.execute("BEGIN;")

        # Check for trainer availability on the given date
        cur.execute("""
            SELECT date_id FROM "Dates"
            WHERE trainer_id = %s AND availability = %s
        """, (trainer_id, event_date))
        availability = cur.fetchone()

        if availability is None:
            messagebox.showerror("Error", "Trainer is not available on this date.")
            cur.execute("ROLLBACK;")
            return
        
        else:
            date_id = availability[0]

            # Insert the new group event
            cur.execute("""
                INSERT INTO "GroupEvents"
                (event_name, event_date, event_description, trainer_id, room_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (event_name, event_date, event_description, trainer_id, room_id))

            # Delete the matched availability
            cur.execute("""
                DELETE FROM "Dates"
                WHERE date_id = %s
            """, (date_id,))

            # Commit the transaction
            cur.execute("COMMIT;")
            messagebox.showinfo("Success", "Event created and trainer availability updated.")
    
    except Exception as e:
        cur.execute("ROLLBACK;")
        messagebox.showerror("Error", f"Failed to create event: {e}")

    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox.delete(0, tk.END)
    for event in events:
        # Fetch the trainer name and room using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[5],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT room_type FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in the {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()


# Delete a group event as an admin
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
    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox.delete(0, tk.END)
    for event in events:
       # Fetch the trainer name and room using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[5],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT room_type FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in the {room_name}. Date: {event[2]}. Details: {event[3]}. {member_count} member(s) attending.")

    cur.close()
    conn.close()


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


def update_member_details_display(member_id, details_listbox):
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM \"Members\" WHERE member_id = %s", (member_id,))
        member_details = cur.fetchone()

        if member_details:
            details_list = [
                f"Member ID: {member_details[1]}",
                f"First Name: {member_details[2]}",
                f"Last Name: {member_details[3]}",
                f"Fitness Goals: {member_details[4]}",
                f"Exercise Routine: {member_details[5]}",
                f"Fitness Achievements: {member_details[6]}",
                f"Outstanding Fees: ${member_details[7]}",
                f"Loyalty Points: {member_details[8]}"
            ]
            
            details_listbox.delete(0, tk.END)
            for detail in details_list:
                details_listbox.insert(tk.END, detail)
        else:
            messagebox.showerror("Error", "Member not found.")
    conn.close()


def member_page(user_id):
    global events_listbox_member
    global details_listbox
    global sessions_listbox
    global health_metrics_listbox
    global fitness_goal_entry, blood_pressure_entry, weight_entry, height_entry
    conn = psycopg2.connect(**db_config)

    cur = conn.cursor()
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]
    
    cur.execute("""
    SELECT s.session_id, s.trainer_id, s.session_date, s.session_notes, u.username, r.room_type as room_name
    FROM "Sessions" s
    JOIN "Trainers" t ON s.trainer_id = t.trainer_id
    JOIN "Users" u ON t.user_id = u.user_id
    JOIN "Rooms" r ON s.room_id = r.room_id
    WHERE s.member_id = %s
    """, (member_id,))
    sessions = cur.fetchall()
    sessions_listbox_items = [
        f"Date: {session[2]}, Trainer: {session[4]}, Room: {session[5]}, Notes: {session[3]}" 
        for session in sessions
    ]

    window = tk.Tk()
    window.title("Member Page")
    window.geometry("800x650")

    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Member details section using a Listbox for selectable items
    details_frame = tk.LabelFrame(main_frame, text="Member Details", padx=10, pady=10)
    details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    # Member details section
    details_listbox = tk.Listbox(details_frame, height=8)
    details_listbox.pack(fill=tk.BOTH, expand=True)

    update_member_details_display(member_id, details_listbox)

    # Health Metrics section
    cur.execute("SELECT * FROM \"HealthMetrics\" WHERE member_id = %s", (member_id,))
    health_metrics = cur.fetchall()
    health_metrics_frame = tk.LabelFrame(main_frame, text="Health Metrics", padx=10, pady=10)
    health_metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    health_metrics_listbox = tk.Listbox(health_metrics_frame, height=3)
    for metric in health_metrics:
        health_metrics_listbox.insert(tk.END, f"Blood Pressure: {metric[2]}")
        health_metrics_listbox.insert(tk.END, f"Weight: {metric[3]} kg")
        health_metrics_listbox.insert(tk.END, f"Height: {metric[4]} cm") 
    health_metrics_listbox.pack(fill=tk.BOTH, expand=True)

    # Sessions section
    sessions_frame = tk.LabelFrame(main_frame, text="Your Training Sessions", padx=10, pady=10)
    sessions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    sessions_listbox = tk.Listbox(sessions_frame, height=3)
    for item in sessions_listbox_items:
        sessions_listbox.insert(tk.END, item)
    sessions_listbox.pack(fill=tk.BOTH, expand=True)

    # Events section
    events_frame = tk.LabelFrame(main_frame, text="Upcoming Events", padx=10, pady=10)
    events_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    events_listbox_member = tk.Listbox(events_frame, height=2)
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    for event in events:
        # Fetch the trainer name and room using the trainer ID and room ID
        cur.execute("""
        SELECT u.username 
        FROM "Users" u
        JOIN "Trainers" t ON u.user_id = t.user_id
        WHERE t.trainer_id = %s
        """, (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT room_type FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox_member.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in the {room_name}. Date: {event[2]}. Details: {event[3]}. {member_count} member(s) attending.")

    events_listbox_member.pack(fill=tk.BOTH, expand=True)
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(fill=tk.X, pady=10)

    fitness_goal_entry = tk.Entry(details_frame)
    fitness_goal_entry.pack(side=tk.TOP, fill=tk.X)

    # Create a subframe for a more compact layout using grid
    entries_frame = tk.Frame(health_metrics_frame)
    entries_frame.pack(pady=10)

    # Blood Pressure Entry
    tk.Label(entries_frame, text="New Blood Pressure:").grid(row=0, column=0, sticky="w")
    blood_pressure_entry = tk.Entry(entries_frame)
    blood_pressure_entry.grid(row=0, column=1, sticky="ew")

    # Weight Entry
    tk.Label(entries_frame, text="New Weight (kg):").grid(row=1, column=0, sticky="w")
    weight_entry = tk.Entry(entries_frame)
    weight_entry.grid(row=1, column=1, sticky="ew")

    # Height Entry
    tk.Label(entries_frame, text="New Height (cm):").grid(row=2, column=0, sticky="w")
    height_entry = tk.Entry(entries_frame)
    height_entry.grid(row=2, column=1, sticky="ew")

    # Ensure the entries_frame column 1 (where entries are) expands to fill the space
    entries_frame.columnconfigure(1, weight=1)
    update_metrics_button = tk.Button(health_metrics_frame, text="Update Metrics",
                                      command=lambda: update_health_metrics(user_id), font=('Arial', 10, 'bold'),
                                    bg='#dda0dd',
                                    fg='white',
                                    padx=8,
                                    pady=4)
    update_metrics_button.pack(pady=10)

    set_goal_button = tk.Button(details_frame, text="Update Personal Info", command=lambda: update_personal(user_id), font=('Arial', 10, 'bold'),
                                    bg='#dda0dd',
                                    fg='white',
                                    padx=8, # Horizontal padding
                                    pady=4) # Vertical padding
    set_goal_button.pack(pady=8)

    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)
    buttons_frame.grid_columnconfigure(3, weight=1)

    # Pay Bills Button
    pay_bills_button = tk.Button(buttons_frame, text="Pay Bills", command=lambda: pay_bills(member_id),
                                 font=('Arial', 12, 'bold'), bg='#CB09F6', fg='white')
    pay_bills_button.grid(row=0, column=0, padx=5, pady=10, sticky='ew')  # Expanded to fill the grid cell

    # Registration Button
    register_button = tk.Button(buttons_frame, text="Register for Event", 
                                command=lambda: register_for_event(member_id, events_listbox_member.get(tk.ACTIVE)[0]),
                                font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    register_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')  # Expanded to fill the grid cell

    # Schedule Session Button
    schedule_session_button = tk.Button(buttons_frame, text="Schedule Session", 
                                        command=lambda: schedule_page(member_id),
                                        font=('Arial', 12, 'bold'), bg='#007bff', fg='white')
    schedule_session_button.grid(row=0, column=2, padx=10, pady=10, sticky='ew')  # Expanded to fill the grid cell

    # Logout Button
    logout_button = tk.Button(buttons_frame, text="Logout", 
                              command=window.destroy,
                              font=('Arial', 12, 'bold'), bg='#f44336', fg='white')
    logout_button.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

    change_on_hover(register_button, '#45a049', '#4CAF50')
    change_on_hover(schedule_session_button, '#0056b3', '#007bff')
    change_on_hover(logout_button, '#d32f2f', '#f44336')
    change_on_hover(pay_bills_button, '#B307D9', '#CB09F6')

    cur.close()
    conn.close()
    window.mainloop()

def schedule_page(member_id):
    schedule_window = tk.Toplevel()
    schedule_window.title("Schedule a Session")
    schedule_window.geometry("600x400")

    listbox = tk.Listbox(schedule_window, height=15, width=50)
    listbox.pack(pady=20)

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT date_id, availability, trainer_id FROM \"Dates\" ORDER BY availability")
    dates = cur.fetchall()
    for date in dates:
        listbox.insert(tk.END, f"{date[0]}, Date: {date[1]}")

    submit_button = tk.Button(schedule_window, text="Register for Event", 
                                command=lambda: schedule_session(member_id, listbox.get(tk.ACTIVE)[0], schedule_window),
                                font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    submit_button.pack(pady=10)

    cur.close()
    conn.close()

def schedule_session(member_id, date_id, schedule_window):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute("SELECT trainer_id, availability FROM \"Dates\" WHERE date_id = %s", date_id)
    schedule_details = cur.fetchall() # a tuple (availability, trainer_id)
    print(schedule_details)
    trainer_id, trainer_availability = schedule_details[0]

    # Formatting the availability as a string in the 'YYYY-MM-DD HH:MM:SS' format
    trainer_availability = trainer_availability.strftime('%Y-%m-%d %H:%M:%S')
    

    cur.execute("INSERT INTO \"Sessions\" (member_id, trainer_id, room_id, session_date) VALUES (%s, %s, %s, %s)",
                            (member_id, trainer_id, 1, trainer_availability))
    conn.commit()
    messagebox.showinfo("Success", "Session Scheduled Successfully")

    cur.execute("SELECT billing_info FROM \"Members\" WHERE member_id = %s", (member_id,))
    current_billing = cur.fetchone()[0] or Decimal('0.00')  # Default to Decimal('0.00') if None
    # Update billing_info with an additional $15.99
    new_billing = current_billing + Decimal('15.99')
    cur.execute("UPDATE \"Members\" SET billing_info = %s WHERE member_id = %s", (new_billing, member_id))
    conn.commit()
    update_member_details_display(member_id, details_listbox)

    cur.execute("""
    SELECT s.session_id, s.trainer_id, s.session_date, s.session_notes, u.username, r.room_type as room_name
    FROM "Sessions" s
    JOIN "Trainers" t ON s.trainer_id = t.trainer_id
    JOIN "Users" u ON t.user_id = u.user_id
    JOIN "Rooms" r ON s.room_id = r.room_id
    WHERE s.member_id = %s
    """, (member_id,))
    sessions = cur.fetchall()
    sessions_listbox_items = [
        f"Date: {session[2]}, Trainer: {session[4]}, Room: {session[5]}, Notes: {session[3]}" 
        for session in sessions
    ]
    sessions_listbox.delete(0, tk.END)
    for item in sessions_listbox_items:
        sessions_listbox.insert(tk.END, item)
    sessions_listbox.pack(fill=tk.BOTH, expand=True)

    cur.execute("""
        DELETE FROM "Dates"
        WHERE date_id = %s
    """, (date_id,))
    conn.commit()
    schedule_window.destroy()
    cur.close()
    conn.close()


def pay_bills(member_id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Update the billing_info for the current member to $0.00
    cur.execute("UPDATE \"Members\" SET billing_info = 0.00 WHERE member_id = %s", (member_id,))
    conn.commit()

    messagebox.showinfo("Payment Successful", "Your bills have been paid in full.")
    update_member_details_display(member_id, details_listbox)
    cur.close()
    conn.close()


def update_personal(user_id):
    conn = psycopg2.connect(**db_config)
    details_index = details_listbox.curselection()
    if len(details_index ) == 0:
        messagebox.showerror("Error", "No personal info selected")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]

    new_status = fitness_goal_entry.get()

    # Update the status of the selected room in the database
    cur = conn.cursor()
    cur.execute("UPDATE \"Members\" SET fitness_goals = %s WHERE member_id = %s", (new_status, member_id))
    conn.commit()

    update_member_details_display(member_id, details_listbox)
    cur.close()
    conn.close()


def update_health_metrics(user_id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]

    new_blood_pressure = blood_pressure_entry.get()
    new_weight = weight_entry.get()
    new_height = height_entry.get()

    try:
        # Update HealthMetrics in the database for the member
        cur.execute("""
            UPDATE "HealthMetrics" 
            SET blood_pressure = %s, weight = %s, height = %s 
            WHERE member_id = %s
        """, (new_blood_pressure, new_weight, new_height, member_id))
        conn.commit()

        cur.execute("SELECT * FROM \"HealthMetrics\" WHERE member_id = %s", (member_id,))
        updated_metrics = cur.fetchone()

        health_metrics_listbox.delete(0, tk.END)
        health_metrics_listbox.insert(tk.END, f"Blood Pressure: {updated_metrics[2]}")
        health_metrics_listbox.insert(tk.END, f"Weight: {updated_metrics[3]} kg")
        health_metrics_listbox.insert(tk.END, f"Height: {updated_metrics[4]} cm")

    except Exception as e:
        print("Failed to update your health metrics: " + str(e))

    cur.close()
    conn.close()
    

def register_for_event(member_id, event_id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO \"MemberGroupEvent\" (member_id, event_id) VALUES (%s, %s)", (member_id, event_id))

    cur.execute("SELECT billing_info FROM \"Members\" WHERE member_id = %s", (member_id,))
    current_billing = cur.fetchone()[0] or Decimal('0.00')  # Default to Decimal('0.00') if None
    # Update billing_info with an additional $20.99
    new_billing = current_billing + Decimal('20.99')
    cur.execute("UPDATE \"Members\" SET billing_info = %s WHERE member_id = %s", (new_billing, member_id))
    conn.commit()

    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()                     # Update events list by reloading contents
    events_listbox_member.delete(0, tk.END)
    for event in events:
        # Fetch the trainer name and room using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[5],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT room_type FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox_member.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in the {room_name}. Date: {event[2]}. Details: {event[3]}. {member_count} member(s) attending.")

    update_member_details_display(member_id, details_listbox)
    
    cur.close()
    conn.close()


def set_trainer_availability(conn, trainer_id):
    new_date = simpledialog.askstring("Availability", "Enter your available date and time (e.g., '2024-04-30 15:30:05'): ")
    if new_date:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO "Dates" (trainer_id, availability) 
                    VALUES (%s, %s)
                """, (trainer_id, new_date))
                conn.commit()
            messagebox.showinfo("Success", f"Your availability date has been added: {new_date}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use 'YYYY-MM-DD HH:MM' format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update availability: {e}")

def view_member_profile(conn):
    member_name = simpledialog.askstring("Member Search", "Enter the member's first name to search: ")
    if member_name:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT m.* 
            FROM "Members" m
            WHERE m.first_name = %s
            """, (f'{member_name}',))
            member_details = cur.fetchall()
        print(member_details)
            
        if member_details:
            details_str = "\n\n".join([
                f"Member ID: {detail[1]}\n"
                f"First Name: {detail[2]}\n"
                f"Last Name: {detail[3]}\n"
                f"Fitness Goals: {detail[4]}\n"
                f"Exercise Routine: {detail[5]}\n"
                f"Fitness Achievements: {detail[6]}\n"
                f"Outstanding Fees: ${detail[7]}" 
                for detail in member_details])
            messagebox.showinfo("Member Profile", details_str)

        else:
            messagebox.showinfo("Member Profile", "No member found with that first name.")

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
    change_on_hover(set_availability_button, '#45a049', '#4CAF50')

    # Member Profile Viewing
    profile_frame = tk.LabelFrame(window, text="Member Profile Viewing")
    profile_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    view_profile_button = tk.Button(profile_frame, text="View Member Profile",
                                    command=lambda: view_member_profile(conn),
                                    font=('Arial', 12, 'bold'),
                                    bg='#007BFF',
                                    fg='white',
                                    padx=10, # Horizontal padding
                                    pady=5) # Vertical padding
    view_profile_button.pack(pady=10)
    change_on_hover(view_profile_button, '#0056b3', '#007bff')

    logout_frame = tk.Frame(window)
    logout_frame.pack(pady=8, fill=tk.X)
    logout_button = tk.Button(logout_frame, text="Logout", command=window.destroy,
                              font=('Arial', 12, 'bold'), bg='#f44336', fg='white', padx=8, pady=5)
    logout_button.pack(side=tk.RIGHT, padx=10)
    change_on_hover(logout_button, '#d32f2f', '#f44336')

    window.mainloop()
    conn.close()


# Setting up the database by creating tables from the DDL.sql file
def setupDB():
    conn = psycopg2.connect(**db_config)
    # cursor to perform database operations
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


# Populating sample data from DML.sql
def populateDB():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    with open('DML.sql', 'r') as f:
        sql_file = f.read()

    cur.execute(sql_file)
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
        try:
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
        except Exception as e:
            print("Failed to set up database or log in: " + str(e))
            continue

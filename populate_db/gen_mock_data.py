import faker
import numpy as np
import pandas as pd
import uuid
import random
import string
import time
from datetime import datetime, timedelta, time

def get_photos():
    """
    get list of mock student photos from base64 encoded text file
    """
    photos = []
    with open("./photos.txt") as file:
        for line in file:
            line.strip()
            photos.append(line.rstrip('\n'))
    return photos

def dob_generator():
    """
    randomly generate a date of birth

    Return:
       dob in the form "mm/dd/yyyy"
    """
    month = random.randint(1, 12)
    year = random.randint(2012, 2024)
    if (month == 2):
        if (year % 4 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)        
    elif (month == 4 or month == 6 or month == 9 or month == 11):
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    
    return(str(month)+"/"+str(day)+"/"+str(year))

def get_unique_student_list(users_df: pd.DataFrame, num_students) :
    """
    generate a list of students (with unique emails) for a class
    
    Parameters:
        user_df: the user table
        num_students: the number of students to enroll in the class
    
    Return: 
        a list of student emails (all unique) from the user table
    """
    student_list = []
    while (len(student_list) <= num_students):
        index = random.randint(0, len(users_df.index)-1)
        if (users_df.iloc[index]['role'] == "student") and (users_df.iloc[index]['email_address'] not in student_list):
            student_list += [users_df.iloc[index]['email_address']]
       
    return(student_list)

def get_teacher_email(users_df: pd.DataFrame) :
    '''
    grab a teacher id for a class
    
    Parameters:
        user_df: the user database
    
    Return:
        a teacher id for the class (id is from the users table)
    '''
    index = random.randint(0, len(users_df.index)-1)
    while users_df.iloc[index]['role'] != "teacher":
        index = random.randint(0, len(users_df.index)-1)
    
    return(users_df.iloc[index]['email_address'])

def generate_users_table(n: int) -> pd.DataFrame:
    """
    Generate users table (using randomly generated data).
    
    Parameters:
        n: number of users
    
    Return: 
        .csv file with mock data
    """
    photos = get_photos()
    fake_person = faker.Faker()
    df_dict = {
        "first_name": [
            fake_person.first_name() for _ in range(n)
        ],

        "last_name": [
            fake_person.unique.last_name() for _ in range(n)
        ],
        "preferred_name": [
            fake_person.unique.first_name() for _ in range(n)
        ],
        "password": [
            fake_person.unique.password() for _ in range(n)
        ],
        "physical_id_num": [str(uuid.uuid4()) for _ in range(n)],
        "dob": [dob_generator() for _ in range(n)],
        "role" : [random.choice(["teacher", "student"]) for _ in range(n)],
        "photo" : [photos[random.randint(0, len(photos))-1] for _ in range(n)]
    }
    
    df_dict["email_address"] = [
        f"{first_name}.{last_name}@schoolmail.com"
        for first_name, last_name in zip(df_dict["first_name"], df_dict["last_name"])
    ]
    
    df_dict["is_staff"] = [
        True if role == "teacher" else False for role in df_dict["role"]
    ]
    
    df_dict["is_superuser"] = [
        True if staff is True else False for staff in df_dict["is_staff"]
    ]
    
    df = pd.DataFrame(df_dict)
    df.to_csv("users_table.csv", index=False)
    return(df)

def generate_events_table(n: int) -> pd.DataFrame:
    """
    Generate events table (using randomly generated data).
    
    Parameters:
        n: number of events
    
    Return: 
        .csv file with mock data
    """
    
    df_dict = {
        "event_id": [i for i in range(1,n+1)],
        "event_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 10))) for _ in range(n)
        ],
        "meeting_link": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for _ in range(n)
        ],
        "super_link": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for _ in range(n)
        ],
        "year": [str(random.randint(2020, 2022)) for _ in range(n)],
        "section": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for _ in range(n)
        ]
    }
    
    df_dict["meeting_link"] = [
        f"https://{event_name}.com"
        for event_name in df_dict["event_name"]
    ]
    df_dict["super_link"] = [
        f"https://{event_name}_super.com"
        for event_name in df_dict["event_name"]
    ]
    
    df = pd.DataFrame(df_dict)
    df.to_csv("events_table.csv", index=False)
    return df

def generate_event_enrollment_table(users_df: pd.DataFrame, events_df: pd.DataFrame, roster_df: pd.DataFrame) -> None:
    '''
    Generate event enrollment table (using randomly generated data).
    
    Parameters:
        user_df: the user table
        events_df: the events table
        roster_df, the event roster table
    
    Return: None
    '''
    entries: dict = {
        "enrollment_id": [],
        "event_id": [],
        "roster_id": []
    }  
    
    j = 1
    for idx, row in events_df.iterrows():
        num_students = random.randint(12, 25)
        
        i = 0
        while (i <= num_students):
            entries["enrollment_id"] += [j]
            entries["event_id"] += [row["event_id"]]
            index = random.randint(0,roster_df.shape[0] - 1)
            entries["roster_id"] += [roster_df.iloc[index]['roster_id']]
            i += 1
            j += 1
    
    df = pd.DataFrame(entries)
    df.to_csv("event_enrollment_table.csv", index=False)

def generate_event_schedule_table(events_df: pd.DataFrame, n: int) -> None:
    '''
    Generate event schedule table.
    
    Parameters:
        events_df: the events table
        n, the number of events
    
    Return: None
    '''
    entries: dict = {
        "schedule_id": [],
        "event_id": [],
        "weekday": [],
        "start_time": [],
        "end_time": [],
    }  
    
    for idx, row in events_df.iterrows():
        start_time = random.randint(9, 15)
        entries["schedule_id"] = [i for i in range(1,n+1)]
        entries["event_id"] += row["event_id"],
        entries["weekday"] += random.randint(0, 4), # 0 = Monday, 4 = Friday
        entries["start_time"] += time(hour=start_time),
        entries["end_time"] += time(hour=start_time+1),
    
    df = pd.DataFrame(entries)
    df.to_csv("event_schedule_table.csv", index=False)

def generate_assignments_table(events_df: pd.DataFrame) -> None:
    '''
    Generate assignment table.
    
    Parameters:
        events_df: the events table
    
    Return: None
    '''
    entries: dict = {
        "assignment_id": [],
        "name": [],
        "description": [],
        "assigned_date": [],
        "due_date": [],
        "event_id": [],
    }

    for idx, row in events_df.iterrows():        
        entries["assignment_id"] += random.randint(0, 10000),
        entries["name"] += ["".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 10)))]
        entries["description"] += ["".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 100)))]
        entries["assigned_date"] += dob_generator(), # may want to revisit
        entries["due_date"] += dob_generator(), # may want to revisit
        entries["event_id"] += [events_df.iloc[random.randint(0, len(events_df.index)-1)]['event_id']]
    
    df = pd.DataFrame(entries)
    df.to_csv("assignments_table.csv", index=False)

def generate_event_roster_table() -> None:
    '''
    Generate event roster table.
    The roster id is unique to itself. Each roster will have at least 1 (possibly more) teachers and some number of students (see participants table).
    Multiple events, such as science, math and english, could all use the same roster id (this is typical in early education)
    
    Parameters:
        n: the number of roster ids to generate
    
    Return: the event roster table
    '''    
    entries: dict = {
        "roster_id": [],
        "roster_name": []
    }
    
    entries["roster_id"] = 1,
    entries["roster_name"] = "roster"
    
    df = pd.DataFrame(entries)
    df.to_csv("event_roster_table.csv", index=False)
    return df
    
def generate_event_roster_participant_table(users_df: pd.DataFrame, roster_df: pd.DataFrame) -> None:
    '''
    Generate class roster participant table.
    
    Parameters:
        user_df, the users table
        roster_df: the event roster table
    
    Return: None
    '''    
    entries: dict = {
        "roster_id": [],
        "participant_id": [],
        "email_address": []
    }
    
    for idx, row in roster_df.iterrows():
        # add teacher to a class
        entries["email_address"] += [get_teacher_email(users_df=users_df)]
        entries["participant_id"] += [1]
        entries["roster_id"] += [row["roster_id"]]
        # populate class roster with students
        num_students = random.randint(12, 25)
        entries["email_address"] += get_unique_student_list(users_df=users_df, num_students=num_students-1)
        for i in range(0, num_students):
            entries["participant_id"] += [(i+2)]
            entries["roster_id"] += [row["roster_id"]]
    
    df = pd.DataFrame(entries)
    df.to_csv("event_roster_participant_table.csv", index=False)

if __name__ == "__main__":

    df_users = generate_users_table(n=100)
    df_events = generate_events_table(n=30)
    df_roster = generate_event_roster_table() # chose half the number of events 
    
    generate_event_enrollment_table(users_df=df_users, events_df=df_events, roster_df=df_roster)
    generate_event_schedule_table(events_df=df_events, n=30)
    generate_assignments_table(events_df=df_events)
    generate_event_roster_participant_table(users_df=df_users, roster_df=df_roster)
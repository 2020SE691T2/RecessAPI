import pandas as pd
import uuid
import random
import string
import numpy as np

def dob_generator():
    '''
    randomly generate a date of birth

    Return:
       dob in the form "mm/dd/yyyy"
    '''
    month = random.randint(1, 12)
    year = random.randint(1960, 2020)
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
    '''
    generate a list of students (with unique emails) for a class
    
    Parameters:
        user_df: the user table
        num_students: the number of students to enroll in the class
    
    Return: 
        a list of student emails (all unique) from the user table
    '''
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
    
    df_dict = {
        "first_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 10))) for i in range(n)
        ],
        "last_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for i in range(n)
        ],
        "preferred_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for i in range(n)
        ],
        "password": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for i in range(n)
        ],
        "physical_id_num": [str(uuid.uuid4()) for i in range(n)],
        "dob": [dob_generator() for i in range(n)],
        "role" : [random.choice(["teacher", "student"]) for i in range(n)]
    }
    
    df_dict["email_address"] = [
        f"{first_name}.{last_name}@schoolmail.com"
        for first_name, last_name in zip(df_dict["first_name"], df_dict["last_name"])
    ]
    
    df = pd.DataFrame(df_dict)
    df.to_csv("users_table.csv", index=False)
    return(df)

def generate_classes_table(n: int) -> pd.DataFrame:
    """
    Generate classes table (using randomly generated data).
    
    Parameters:
        n: number of classes
    
    Return: 
        .csv file with mock data
    """
    
    df_dict = {
        "class_id": [i for i in range(1,n+1)],
        "class_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 10))) for i in range(n)
        ],
        "meeting_link": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for i in range(n)
        ],
        "year": [str(random.randint(1960, 2020)) for i in range(n)],
        "section": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for i in range(n)
        ]
    }
    
    df_dict["meeting_link"] = [
        f"https://{class_name}.com"
        for class_name in df_dict["class_name"]
    ]
    
    df = pd.DataFrame(df_dict)
    df.to_csv("classes_table.csv", index=False)
    return df

def generate_class_enrollment_table(users_df: pd.DataFrame, classes_df: pd.DataFrame) -> None:
    '''
    Generate classes table (using randomly generated data).
    
    Parameters:
        user_df: the user table
        classes_df: the classes table
    
    Return: None
    '''
    entries: dict = {
        "class_id": [],
        "teacher_email": [],
        "student_email": [],
    }  
    
    for idx, row in classes_df.iterrows():
        num_students = random.randint(12, 25)
        teacher_id = get_teacher_email(users_df=users_df)
        entries["student_email"] += get_unique_student_list(users_df=users_df, num_students=num_students)
        i = 0
        while (i <= num_students):
            entries["class_id"] += [row["class_id"]]
            entries["teacher_email"] += [teacher_id]
            i += 1
                
    df = pd.DataFrame(entries)
    df.to_csv("class_enrollment_table.csv", index=False)

def generate_class_schedule_table(classes_df: pd.DataFrame) -> None:
    '''
    Generate class schedule table.
    
    Parameters:
        classes_df: the classes table
    
    Return: None
    '''
    entries: dict = {
        "class_id": [],
        "date": [],
        "start_time": [],
        "end_time": [],
    }  
    
    for idx, row in classes_df.iterrows():
        start_time = random.randint(9, 15)
        entries["class_id"] += row["class_id"],
        entries["date"] += dob_generator(), # may want to revisit
        entries["start_time"] += start_time,
        entries["end_time"] += start_time+1,
    
    df = pd.DataFrame(entries)
    df.to_csv("class_schedule_table.csv", index=False)

def generate_assignments_table(classes_df: pd.DataFrame) -> None:
    '''
    Generate assignment table.
    
    Parameters:
        classes_df: the classes table
    
    Return: None
    '''
    entries: dict = {
        "assignment_id": [],
        "name": [],
        "description": [],
        "assigned_date": [],
        "due_date": [],
        "class_id": [],
    }

    for idx, row in classes_df.iterrows():        
        entries["assignment_id"] += random.randint(0, 10000),
        entries["name"] += ["".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 10)))]
        entries["description"] += ["".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 100)))]
        entries["assigned_date"] += dob_generator(), # may want to revisit
        entries["due_date"] += dob_generator(), # may want to revisit
        entries["class_id"] += [classes_df.iloc[random.randint(0, len(classes_df.index)-1)]['class_id']]
    
    df = pd.DataFrame(entries)
    df.to_csv("assignments_table.csv", index=False)

if __name__ == "__main__":
    df_users = generate_users_table(n=100)
    df_classes = generate_classes_table(n=30)
    generate_class_enrollment_table(users_df=df_users, classes_df=df_classes)
    generate_class_schedule_table(classes_df=df_classes)
    generate_assignments_table(classes_df=df_classes)
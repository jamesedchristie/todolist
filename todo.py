from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
 
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()
 
class ToDoList(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())
 
    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

while True:
    today = datetime.today()
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    command = input()
    print()
    if command == '0':
        print('Bye!')
        break
    if command == '1':
        # Print today's tasks
        rows = session.query(ToDoList).all()
        todays_tasks = [row.task for row in rows if row.deadline == today.date()]
        if len(todays_tasks) == 0:
            print('Nothing to do!')
        else:
            for i in range(len(todays_tasks)):
                print(f'{i + 1}. {todays_tasks[i]}')
                print(rows[0].deadline)
        print()
    elif command == '2':
        # Print the week's tasks
        rows = session.query(ToDoList).all()
        for i in range(7):
            day = today + timedelta(days=(i%7))
            print(f"{weekdays[day.weekday()]} {day.day} {day.strftime('%b')}:")
            days_tasks = [row.task for row in rows if row.deadline == day.date()]
            if len(days_tasks) == 0:
                print('Nothing to do!')
            else:
                for j in range(len(days_tasks)):
                    print(f'{j + 1}. {days_tasks[j]}')
            print()
    elif command == '3':
        rows = session.query(ToDoList).all()
        rows = sorted(rows, key=lambda d: d.deadline)
        print('All tasks:')
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
        print()
    elif command == '4':
        # Display tasks with expired deadlines
        print('Missed tasks:')
        rows = session.query(ToDoList).all()
        missed_tasks = [row for row in rows if row.deadline < today.date()]
        missed_tasks = sorted(missed_tasks, key=lambda d: d.deadline)
        if len(missed_tasks) == 0:
            print('Nothing is missed!')
        else:
            for i in range(len(missed_tasks)):
                print(f'{i + 1}. {missed_tasks[i].task} {missed_tasks[i].deadline.day} {missed_tasks[i].deadline.strftime("%b")}')
        print()
    elif command == '5':
        print('Enter task')
        new_task = input()
        print('Enter deadline')
        new_deadline = input()
        new_row = ToDoList(task=new_task, deadline=datetime.strptime(new_deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print('The task has been added!')    
        print()
    elif command == '6':
        # Delete tasks
        print('Choose the number of the task you want to delete')
        rows = session.query(ToDoList).all()
        tasks = sorted(rows, key=lambda d: d.deadline)
        for task in tasks:
            print(f'{tasks.index(task) + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
        task_index = int(input()) - 1
        to_delete = tasks[task_index]
        session.delete(to_delete)
        session.commit()
        print('The task has been deleted!')
        print()


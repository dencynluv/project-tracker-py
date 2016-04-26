"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    #Writing out query for db.session.execute to execute
    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = :github
        """
    #Execute query and bind result to db_cursor
    db_cursor = db.session.execute(QUERY, {'github': github})
    #Return a tuple of query result db_cursor and bind it to identifier row
    row = db_cursor.fetchone() 
    #Index tuple and print statement
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    #Writing out query to insert data into database
    QUERY = """
        INSERT INTO Students
        VALUES (:first_name, :last_name, :github)
        """
    #executing query and binding results to db_cursor
    db_cursor = db.session.execute(QUERY, {'first_name': first_name, 
                                            'last_name': last_name, 
                                            'github': github})
    # In order to commit changes to database must call commit() function
    db.session.commit()

    # confirming that changes were made to database
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT description
        FROM projects
        WHERE title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    row = db_cursor.fetchone()

    print "Project description: %s" % (row[0])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """
        SELECT grade
        FROM grades
        WHERE student_github = :github
        AND project_title = :title
        """

    # executing query and binding results to db_cursor
    # order of parameters matter. Should match parameters from above.
    db_cursor = db.session.execute(QUERY, {'github': github,
                                            'title': title})

    row = db_cursor.fetchone()
    
    print "Student grade: %s" % (row[0])

def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    pass


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")  #input by user
        tokens = input_string.split() #takin input and returning a list of strings binding it to tokens
        command = tokens[0] #binding command to first item of tokens list 
        args = tokens[1:] #binding args to all the items after and including the first index

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        #if the command entered is equal to 'project_description'
        elif command == "project_description": 
            # parameter title equals to the word after our command
            title = args[0]
            # calling function 
            get_project_by_title(title)

        elif command == 'student grade':
            github, title = args
            get_grade_by_github_title(github, title)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    db.session.close()

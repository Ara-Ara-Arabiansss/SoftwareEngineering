import click, pytest, sys
from flask import Flask
from datetime import datetime

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *



# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()    
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(username, password):
#     create_user(username, password)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("competition", help = 'Testing Competition commands')
@click.argument("type", default="all")
def competition_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CompUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CompIntegrationTests"]))
    else:
        print("deafult input, no test ran")

app.cli.add_command(test)


'''
Competition Commands
'''

competition_cli = AppGroup('competition', help = 'Competition object commands')   

@competition_cli.command("create", help = 'Creates new competition')
@click.argument("id", default = "1")
@click.argument("name", default ="Run Time")
@click.argument("location", default ="Chaguanas")
def create_competition_command(id,name,location):
    competition = create_competition(id,name,location)
    if competition:
        print("Competition Created Successfully")
    else:
        print("Competition not created")

@competition_cli.command("Get", help = " Get competition")
def get_competition_by_id_command(id):
    competition = get_competition_by_id(id)
    if competition :
        print(competition)
    else: 
        print("No competition Found")


@competition_cli.command("List", help = "Lists all competitions")
def list_competitions_command():
    competitions = get_all_competitions_json()
    print(competitions)

@competition_cli.command("Add", help = "Add results to competition")
def add_results_command(user_id, comp_id, rank):
    competition = add_results(user_id, comp_id, rank)
    if competition :
        print(competition)
    else:
        print("No compettion Found")


#@competition_cli.command("add_user")
#@click.argument("user_id")
#@click.argument("comp_id")
# @click.argument("rank")
# def add_to_comp(user_id, comp_id, rank):
#     add_user_to_comp(user_id, comp_id, rank)
#     print("Done!")


# @comps.command("getUserComps")
# @click.argument("user_id")
# def getUserCompetitions(user_id):
#     competitions = get_user_competitions(user_id)
#     print("these are the competitions")
#     # print(competitions)

# @comps.command("findcompuser")
# @click.argument("user_id")
# @click.argument("comp_id")
# def find_comp_user(user_id, comp_id):
#     findCompUser(user_id, comp_id)

# @comps.command("getCompUsers")
# @click.argument("comp_id")
# def get_comp_users(comp_id):
#     get_competition_users(comp_id)




app.cli.add_command(competition_cli)


'''
Competitor commands
'''

competitor = AppGroup('competitor', help = 'commands for competitor')

@competitor.command("create", help = 'create new competitor')
@click.argument("username", default = "rick")
@click.argument("password", default = "sanchez")
def create_competitor_command(username, password):
    competitor = create_competitor(username, password)
    if competitor:
        print("Competitor Created Successfully")
    else:
        print("Error adding competitor")

@competitor.command("list", help = 'list all competitors')
def list_competitors_command():
    competitors = get_all_competitors()
    if competitors:
        print(competitors)
    else:
        print("Error getting competitors")

@competitor.command("get_competitor", help = 'get competitor by id')
def get_competitor_command():
    id  = click.prompt("Enter id", type=str)
    competitor = get_competitor_by_id(id)
    if competitor:
        print(competitor)
    else:
        print("Error getting competitor")

@competitor.command("get_competitor_json", help = 'get competitor by id')
def get_competitor_json_command():
    id = click.prompt("Enter id", type=str)
    competitor = get_competitor_by_id(id)
    if competitor:
        print(competitor.get_json())
    else:
        print("Error getting competitor")

@competitor.command("get_competitor_by_username", help = 'get competitor by username')
def get_competitor_by_username_command():
    username = click.prompt("Enter username", type=str)
    competitor = get_competitor_by_username(username)
    if competitor:
        print(competitor)
    else:
        print("Error getting competitor")

app.cli.add_command(competitor)

'''
Rank commands
''' 

rank = AppGroup('rank', help = 'commands for rank')

@rank.command("create", help = 'create new rank')
def create_rank_command():
    competitor_id = click.prompt("Enter Competitor ID")
    ranking = click.prompt("Enter Ranking")
    rank = create_rank(competitor_id, ranking)
    if rank:
        print("Rank Created Successfully")
    else:
        print("Error adding rank")

@rank.command("update_rank", help = 'update rank')
def update_rank_command():
    competitor_id = click.prompt("Enter Competitor ID")
    ranking = click.prompt("Enter Ranking", type = int)
    rank = update_rank(competitor_id, ranking)
    if rank:
        print("Rank Updated Successfully")
    else:
        print("Error updating rank")

@rank.command("update_points", help = 'update points')
def update_rank_points_command():
    competitor_id = click.prompt("Enter Competitor ID")
    points = click.prompt("Enter Points", type = int)
    rank = update_rank_points(competitor_id, points)
    if rank:
        print("Rank Updated Successfully")
    else:
        print("Error updating points")


@rank.command("list", help = 'list all ranks')
def list_ranks_command():
    ranks = get_all_ranks_json()
    if ranks:
        print(ranks)
    else:
        print("Error getting ranks")
    
@rank.command("get_rank_by_competitor_id", help = 'get rank by competitor id')
def get_rank_command():
    competitor_id = click.prompt("Enter Competitor ID")
    rank = get_rank_by_competitor_id(competitor_id)
    if rank:
        print(rank)
    else:
        print("Error getting rank")


app.cli.add_command(rank)



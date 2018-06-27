# Dev: Michael G
# Date: 3/29/2018 
# Build with: python, django, html, css
# Description:  coding dojo's official ping pong application
# allows registered users to initiate games, keeps scores, records and statistics

#------------------------------------- IMPORTS --------------------------------------
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import Admin, Player, Record, Game, Message, Comment, League
import bcrypt
from django.contrib import messages
import itertools
#------------------------------------------------------------------------------------


# function that renders the login page
def renderMain(request):
    if "user_id" not in request.session:
        request.session['user_id'] = False

    context = {
        "leagues": League.objects.all(),
    }

    # for n in messages:
    # print "n in messages is: {}".format(n)
    # print "message error is ", messages.error
    
    return render(request, 'dojoPong/main.html', context)



# # function that takes user form input from a POST request and creates a new user in db
def register(request):
    errors = Admin.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
        return redirect('/main')
    else:
        name = request.POST["name"]
        moniker = request.POST["moniker"]
        league_name = request.POST['league_name']
        league_city = request.POST["league_city"]
        password = request.POST["password"]
        hp = bcrypt.hashpw( password.encode(), bcrypt.gensalt() )
        # creating a new league
        League.objects.create(name=league_name, city=league_city)
        league = League.objects.filter(name=league_name, city=league_city)[0]
        print(league)
        
        # creating a new league administrator
        Admin.objects.create(name=name, moniker=moniker, password_hash=hp, organization=league)
        user = Admin.objects.filter(moniker=moniker, password_hash=hp)[0]

        # saving sessions information
        request.session['league_id'] = league.id
        request.session['user_id'] = user.id

    # return render(request, "dojoPong/league.html", context)
    return redirect('/league')



# function that renders the league.html page
def renderLeague(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    
    admin = Admin.objects.get(id = request.session['user_id'])
    league = League.objects.get(id = request.session['league_id'])
    top_three = get_top_three(league)
    top_three_players = []
    for n in top_three:
        p = Player.objects.get(id=n[0])
        top_three_players.append(p)
    # print(top_three)
    context={
        "u": admin,
        "league": league,
        "players": league.players.all(),
        "top_three": top_three_players
    }
    return render(request, 'dojoPong/league.html', context)



# calculates and returns the top three players with best winning percentage
# where winning percentage = wins/totalnumber of games * 100%
def get_top_three(league):
    players_win_percentage = []
    top_three = []
    for player in league.players.all():
        if (player.record.wins > 0 or player.record.losses > 0):
            win_percentage = (player.record.wins/float(player.record.wins+player.record.losses))*100
            players_win_percentage.append( (player.id, win_percentage) )

    sorted_list = sorted(players_win_percentage, key=lambda x: x[1])
    for n in range(0,3):
        if(len(sorted_list) > 0):
            top_three.append(sorted_list.pop(len(sorted_list)-1))
    return top_three


# function that renders the player.html page,  sends the player and all games player
# was part of
def render_player_edit(request, id):
    if "user_id" not in request.session:
        return redirect('/main')
    
    # if "game"
    # get all games that have player id either as winner or loser
    games = Game.objects.filter(league=request.session['league_id'], winner=id) | Game.objects.filter(league=request.session['league_id'], loser=id)
    league = League.objects.get(id=request.session['league_id'])
    # gamesLost = Game.objects.filter(league=request.session['league_id'], loser=id)
    # games = gamesWon+gamesLost
    context={
        "player": Player.objects.get(id=id),
        "games": games,
        "players": league.players.all,
    }
    return render(request, 'dojoPong/player_edit.html', context)



# takes in the admin moniker and password and logs admin into system
def login(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    moniker = request.POST["moniker"]
    password = request.POST['password']
    hp = bcrypt.hashpw( password.encode(), bcrypt.gensalt() )
    # check if username/email and password exist in system
    temp_users = Admin.objects.filter(moniker = moniker)
    if len(temp_users) > 0:
        for n in temp_users:
            if (bcrypt.checkpw(password.encode(), n.password_hash.encode())):
                request.session['user_id'] = n.id
                request.session['league_id'] = n.organization_id
                return redirect('/league') 
    else:
        # print 'inside else'
        messages.add_message(request, messages.INFO, 'Incorrect moniker and or password')
        return redirect('/main')



# function that adds a player to the current league in session
def add_player(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')

    errors = Player.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
        return redirect('/main')
    else:
        # creating an empty record and a new league player
        new_record = Record.objects.create(wins=0, losses=0, draws=0)
        name = request.POST["name"]
        moniker = request.POST["moniker"]
        league = League.objects.get(id=request.session['league_id'])
        Player.objects.create(name=name, moniker=moniker, league=league, record=new_record)
        return redirect('/league')



# renders the league_edit.html page to administrate league changes
def render_admin_view(request):
    if "user_id" not in request.session:
        return redirect('/main')

    admin = Admin.objects.get(id = request.session['user_id'])
    league = League.objects.get(id = request.session['league_id'])
    context = {
        "admin": admin,
        "league": league,
        "players": league.players.all()
    }
    return render(request, 'dojoPong/league_edit.html', context)



def update_league(request):
    if request.method == 'POST':
        errors = League.objects.basic_validator(request.POST)
        if len(errors):
            # for tag, error in errors.iteritems():
                # messages.error(request, error, extra_tags=tag)
            return redirect( '/league')
        else:
            name = request.POST["name"]
            city = request.POST["city"]
            state = request.POST["state"]
            location = request.POST["location"]
            rules = request.POST['rules']
            league = League.objects.get(id=request.session['league_id'])
            league.name = name
            league.city = city
            league.state = state
            league.location = location
            league.rules = rules
            league.save()
            return redirect('/league')
                


# updates the players an scores of a game
# def update_game(request, game_id):
#     if "user_id" not in  request.session:
#         return redirect('/main')
#     # need to find a way to update previous game players wins and losses
    

#     game = Game.objects.get(id=game_id)
#     game.winner = request.POST['winner']
#     game.loser = request.POST['loser']
#     game.winner_points = request.POST['winner_points']
#     game.loser_points = request.POST['loser_points']
#     game.save()
#     return redirect('/league/edit')    


# deletes a player from the league and database
def delete_player(request, id):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    # delete the player record, then the player
    league = League.objects.get(id=request.session['league_id'])
    player = Player.objects.get(id=id)
    record = Record.objects.get(id=player.record.id)
    record.delete()
    league.players.remove(player)
    player.delete()
    return redirect('/league/edit')



def render_scoreboard(request, id):
    if "user_id" not in request.session:
        return redirect('/main')
    league = League.objects.get(id=id)   

    top_three = get_top_three(league)
    top_three_players = []
    for n in top_three:
        p = Player.objects.get(id=n[0])
        top_three_players.append(p)
    context={
        "u": league.admin,
        "league": league,
        "players": league.players.all(),
        "top_three": top_three_players
    }
    return render(request, 'dojoPong/scoreboard.html', context)


def log_game(request):
    if "user_id" not in request.session:
        return redirect('/main')
    player_1_points = int(request.POST['player_1_points'])
    player_2_points = int(request.POST['player_2_points'])
    player_1_id = request.POST['p1']
    player_2_id = request.POST['p2']
    # print('player 1 id is {}, player 2 id is {}'.format(player_1_id, player_2_id))
    player1 = Player.objects.filter(id=player_1_id, league_id=request.session['league_id'])
    player2 = Player.objects.filter(id=player_2_id, league_id=request.session['league_id'])
    # print('player 1 is {}, points: {}'.format(player1, player_1_points))
    # print('player 2 is {}, points: {}'.format(player2, player_2_points))
    
    if( player_1_points < 0 or player_2_points < 0 or player_1_id == 'Player 1' or player_2_id =='Player 2'):
        return redirect('/main')

    # if player 1 and player 2 where found by their id then run the following
    if( len(player1) > 0 and len(player2) > 0 ):
        player1 = player1[0]
        player2 = player2[0]
        notes = request.POST['notes']
        if( player1 is not player2 ):
            league = League.objects.get(id=request.session['league_id'])
            # case where player 1 is winner of game
            if(player_1_points > player_2_points):
                game =  Game.objects.create(winner=player1, loser=player2, winner_points=player_1_points, loser_points=player_2_points, notes=notes, league=league)
                player1.record.wins += 1
                player2.record.losses += 1
                player1.record.save()
                player2.record.save()
            # case where player 2 is winner of game
            elif(player_2_points > player_1_points):
                game =  Game.objects.create(winner=player2, loser=player1, winner_points=player_2_points, loser_points=player_1_points, notes=notes, league=league)
                player2.record.wins += 1
                player1.record.losses += 1
                player1.record.save()
                player2.record.save()
            # case where there is a draw, very unlikely?
            else:
                game =  Game.objects.create(winner=player1, loser=player2, winner_points=player_1_points, loser_points=player_2_points, notes=notes, league=league)
                player1.record.draws += 1
                player2.record.draws += 1
                player1.record.save()
                player2.record.save()
    return redirect('/league')



# # function that logs out a user
def logout(request):
    del request.session['user_id']
    if 'league_id' in request.session:
        del request.session['league_id']
    return redirect('/main')




# JavaScript functionality for toggleing the game edit form into view
# function needs to  be called within the <td> tag with
# onclick="toggle_form( '{{game.id}}' )


# <script>
#         $(document).ready(function(){
            

#         })
        

#         function toggle_form(game) {
#             console.log('clicked');
#             var x = document.getElementById(game)
#             if (x.style.display === "none") {
#                 x.style.display = "block";
#             }
#             else {
#                 x.style.display = "none";
#             }
#         }

#     </script>


# form rendered into view

# <form action='/update_game/{{game.id}}' style="display: block" method='post'>
#     {% csrf_token %}
#     <table class='table'>
#         <tr>
#             <td><p>Winner:</p></td>
#             <td>
#                 <select class="form-control" name='winner'>
#                     <option><p>{{game.winner.moniker}}</p></option>
#                     {% for player in players %}
#                         <option value="{{player.id}}"><p>{{player.moniker}}</p></option>
#                     {% endfor %}
#                 </select>
#             </td>
#             <td size='5'><p>Score:</p></td>
#             <td><p><input type='text' name='winner_points' size='5' value={{game.winner_points}}></p></td>
#         </tr>
#         <tr>
#             <td><p>Loser:</p></td>
#             <td>
#                 <select class="form-control" name='loser'>
#                     <option><p>{{game.loser.moniker}}</p></option>
#                     {% for player in players %}
#                         <option value="{{player.id}}"><p>{{player.moniker}}</p></option>
#                     {% endfor %}
#                 </select>
#             </td>
#             <td size='5'><p>Score:</p></td>
#             <td><p><input type='text' name='loser_points' size='5' value={{game.loser_points}}></p></td>
#         </tr>
#         <tr>
#             <td></td>
#             <td></td>
#             <td colspan="2"><p><input class="btn btn-primary btn-sm" type='submit' id='submit' value='Update Game' class='buttons'></p></td>
#         </tr>
#     </table>
# </form>
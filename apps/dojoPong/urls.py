from django.conf.urls import url
from . import views

urlpatterns = [
    # route to render main.html page
    url(r'^main$',  views.renderMain),

    # route to register a new user     
    url(r'^register$',  views.register),

    # route to render league.html page
    url(r'^league$', views.renderLeague),

    # route to login a user    
    url(r'^login$',  views.login),

    # route to logout a user && del any sessions
    url(r'^logout$', views.logout),

    # route to add a player to a league
    url(r'^add_player$', views.add_player),

    # route to render the admin view to edit a league
    url(r'^league/edit$', views.render_admin_view),

    # route to update the current league
    url(r'^league/update$', views.update_league),

    # route to delete a player from current league
    url(r'^remove/(?P<id>\d+)$',  views.delete_player),
    
    # route to log a new game and its scores to players
    url(r'^log_game$',  views.log_game),

    # route to render the player page for edit
    url(r'^league/player/(?P<id>\d+)$',  views.render_player_edit),
    
    # route to render the league score board without login
    url(r'^league/scoreboard/(?P<id>\d+)$',  views.render_scoreboard),
        
]
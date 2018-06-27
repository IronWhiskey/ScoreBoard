# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import datetime


class AdminManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # today = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        
        if len(postData['name']) < 2 or len(postData['name']) > 255:
            errors["name"] = "name field should not be empty or greater than 255 characters"

        # if len(postData['lastName']) < 2 or len(postData['lastName']) > 255:
        #     errors["lastName"] = "last name field should not be empty"

        if hasNum(postData['name']):
            errors['name'] = "first name can not have a number"
            
        # if hasNum(postData['lastName']):
        #     errors['lastName'] = "last name can not have a number"

        if len(postData['moniker']) < 3:
            errors['moniker'] = "moniker must be greater than 2 characters"

        # if matchEmail(postData['email']) == False:
        #     errors['email'] = "email field is not the correct format" 

        if postData['password'] != postData['confirmPass']:
            errors['password'] = "passwords do not match"

        if len(postData['password']) < 8:
            errors['password'] = "password must be greater than 8 characters"
        # if(postData['password']):
        #     if postData['password'] != postData['confirmPass']:
        #         errors['password'] = "passwords do not match"

        #     if len(postData['password']) < 8:
        #         errors['password'] = "password must be greater than 8 characters"

        # if matchEmail(postData['email']) == False:
        #     errors['email'] =  "email is not correct format"

        return errors


class PlayerManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or len(postData['name']) > 255:
            errors["name"] = "name field should not be empty or greater than 255 characters"

        if hasNum(postData['name']):
            errors['name'] = "first name can not have a number"

        if len(postData['moniker']) < 3:
            errors['moniker'] = "moniker must be greater than 2 characters"

        return errors


# class GameManager(models.Manager):
#     def basic_validator(self, postData):
#         errors = {}
#         if ( postData['player_points'] < 7 and postData['opponent_points'] < 7 ):
#             errors["quote"] = "One player must win by at least 7 points"
#         return errors   



class MessageManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if ( postData['message'] < 1):
            errors["message"] = "The message field must not be empty"
        return errors



class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if ( postData['comment'] < 1):
            errors["comment"] = "the comment field must not be empty"
        return errors


class LeagueManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['league_name'] = "the league name must not be empty"
        if len(postData['city']) < 1:
            errors['league_city'] = "the league city must not be empty"
        # if len(postData['state']) < 1:
        #     errors['league_state'] = "the league state must not be empty"
        return errors 


class Record(models.Model):
    wins = models.IntegerField()
    losses = models.IntegerField()
    draws = models.IntegerField(null=True)
    notes = models.TextField(default='Enter league rules here...')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)



class League(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=32)
    location = models.CharField(max_length=255, default='Enter location or address info...')
    state = models.CharField(max_length=32, null=True)
    rules = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = LeagueManager()



class Admin(models.Model):
    name = models.CharField(max_length=255)
    moniker = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    organization = models.OneToOneField(League, related_name='admin', null=True)
    # record = models.OneToOneField(Record, null=True)
    # opponent_records = models.ForeignKey(Record, related_name="opponent", null=True)
    # league = models.ForeignKey(League, related_name='players', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AdminManager()



class Player(models.Model):
    name = models.CharField(max_length=255)
    moniker = models.CharField(max_length=255)
    record = models.OneToOneField(Record, null=True)
    opponent_records = models.ForeignKey(Record, related_name="opponent", null=True)
    league = models.ForeignKey(League, related_name='players', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PlayerManager()
    def __str__(self):
        return "<Player object: {} {}>".format(self.name, self.moniker)



class Game(models.Model):
    winner = models.ForeignKey(Player, related_name='win')
    loser = models.ForeignKey(Player, related_name='defeat')
    winner_points = models.IntegerField()
    loser_points = models.IntegerField()
    league = models.ForeignKey(League, related_name='games', null=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # objects = GameManager()



class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # user = models.ForeignKey(User, related_name="messages")
    player = models.ForeignKey(Player, related_name="messages")
    objects = MessageManager()



class Comment(models.Model):
    comment = models.TextField()
    # user = models.ForeignKey(User, related_name="comments")
    player = models.ForeignKey(Player, related_name="comments")
    message = models.ForeignKey(Message, related_name='comments')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()



def matchEmail(e):
    return bool(re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', e))


def hasNum(someStr):
    return any(char.isdigit() for char in someStr)
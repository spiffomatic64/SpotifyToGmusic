#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import *  # noqa
from getpass import getpass
from gmusicapi import Mobileclient
from random import shuffle

def get_searches(fname):

    searches = [] 
    with open(fname,encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split("\t")
        search = "%s %s" % (parts[1],parts[2])
        searches.append(search)
        
    return searches
 
 
def ask_for_credentials():
    """Make an instance of the api and attempts to login with it.
    Return the authenticated api.
    """
 
    # We're not going to upload anything, so the Mobileclient is what we want.
    api = Mobileclient()
 
    logged_in = False
    attempts = 0
 
    while not logged_in and attempts < 3:
        # If you use two-factor (which you should)
        # https://support.google.com/accounts/answer/6010255?hl=en
        email = "gmail address"
        password = "gmail password"
 
        logged_in = api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)
        attempts += 1
 
    return api
 
 
def get_playlist_by_name(name):
 
    playlist_id = None
    playlists = api.get_all_playlists()
    for playlist in playlists:
        print(playlist["name"])
        if playlist["name"] == name:
            playlist_id = playlist["id"]
            return playlist_id
    
    return None
        
def get_songid(search):
    
    results = api.search(search)
    songid = None
    try:
        songid = results["song_hits"][0]["track"]["storeId"]
    except Exception as e:
        print("Exception! %s" % e)
        
    return songid
    
 
if __name__ == '__main__':
    api = ask_for_credentials()
 
    if not api.is_authenticated():
        print("Sorry, those credentials weren't accepted.")
    else:
        print('Successfully logged in.')
        print()
        
        #playlist_id = get_playlist_by_name("delete me")
        # assumes you have already run spotify_tracks.py (but this can be added inline as well meh)
        searches = get_searches("out.txt")
        
        # Added shuffle because gmusic has a limit of 1000 songs per playlist, and I wanted variety
        # Sound of everything playlist is sorted by genre alphebetically
        shuffle(searches)
        
        playlist_name = "EveryNoise"
        playlist_id = None
        playlist_num = 1
        counter = 1
        
        for search in searches:
            print("Count: %d, Playlist Num: %d, Total: %s" % (counter, playlist_num, len(searches)))
            if counter == 1:
                #Create a new playlist for every 1000 songs
                playlist_name = "%s %d" % (playlist_name, playlist_num)
                playlist_id = api.create_playlist(playlist_name)
                print("Created playlist: %s" % playlist_name)
            try:
                # Added this as a hack because the whole python3 utf thing doesnt make sense to me sometimes lol
                print("Looking for: %s" % search)
            except Exception as e:
                print("Exception! %s" % e)
            try:
                # had to hack gmusicapi to avoid more utf issues
                # Lib\site-packages\gmusicapi\utils\utils.py
                # Line: 330
                # add encoding = "UTF-8" (will add patch to repo as well)
                song_id = get_songid(search)
                if song_id:
                    print("Got songid: %s" % song_id)
                    api.add_songs_to_playlist(playlist_id, song_id)
                    counter += 1
                    if counter > 1000:
                        counter = 1
                        playlist_num += 1
            except Exception as e:
                print("Exception! %s" % e)
    

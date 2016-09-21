#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
from itertools import izip, tee

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) AS num FROM players")
    result = cursor.fetchone()[0]
    conn.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    if name:
        conn = connect()
        content_valid = bleach.clean(name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (name) VALUES (%s)",(name,))
        conn.commit()
        conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    query = """
            SELECT players.keyid,
                players.name,
                count(CASE WHEN players.keyid = matches.winner THEN 1 ELSE null END) as wins,
                count(CASE WHEN players.keyid = matches.loser or
                    players.keyid = matches.winner THEN 1 ELSE null END) as matches
                FROM players LEFT JOIN matches ON players.keyid = matches.winner OR
                    players.keyid = matches.loser
                GROUP BY players.keyid ORDER BY wins DESC;
            """
    cursor.execute(query)
    outputlist = cursor.fetchall()
    conn.close()
    return outputlist

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if winner and loser:
        winner_clean = bleach.clean(winner)
        loser_clean = bleach.clean(loser)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s,%s)" % (winner_clean, loser_clean))
        conn.commit()
        conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    query = """
            SELECT players.keyid,
                players.name,
                count(CASE WHEN players.keyid = matches.winner THEN 1 ELSE null END) as wins
                FROM players LEFT JOIN matches ON players.keyid = matches.winner
                GROUP BY players.keyid ORDER BY wins DESC;
            """
    cursor.execute(query)
    outputlist = []
    pairings = pairwise(cursor.fetchall())
    for row1,row2 in pairings:
        tup = (row1[0], row1[1], row2[0], row2[1]);
        outputlist.append(tup)
        next(pairings,None)
    conn.close()
    return outputlist

def pairwise(iterable):
    """
    Returns a string of pairs from a single list

    Assume that iterable is a list such as [a,b,c,d...] this function returns a list [(a,b),(b,c),(c,d),...]
    """
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

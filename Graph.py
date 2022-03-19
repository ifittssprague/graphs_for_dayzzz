"""
Isaac Fitts-Sprague
29312728
ECE-241 Data Structures

FILE DESCRIPTION
This file contains the Graph and Vertex classes that are used by the ArtistConnections class.
The Vertex class is called only by the Graph class and is used to initiate vertices. The Graph
class calls the Vertex class and is called by the ArtistConnections class. It is used to connect
the vertices.
"""


class Vertex:
    def __init__(self, artist):
        self.id = artist
        self.songs = []
        self.coArtists = {}

    def addNeighbor(self, nbr, weight=0):
        self.coArtists[nbr] = weight

    def addSongs(self, songLst):
        self.songs.append(songLst)

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.coArtists])


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t].id, cost)

    def addSongs(self, key, temp_song_list):
        self.vertList[key].addSongs(temp_song_list)

    def __iter__(self):
        return iter(self.vertList.values())

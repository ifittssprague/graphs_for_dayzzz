"""
Isaac Fitts-Sprague
29312728
ECE-241 Data Structures

FILE DESCRIPTION
This file contains the ArtistConnections class which calls the Graph and SongLibrary classes.
It is used to build a graph and collect, organize, and search through data from the graph.
"""

from SongLibrary import SongLibrary
from Graph import Graph


class ArtistConnections:

    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    """
    FUNCTION DESCRIPTION
This function is used to create a graph from the song library data passed to it. It creates a vertex
dictionary for each artist, with the key being the artists name and storing other information such as 
the names of songs the artist has written, and other artists they have worked with. 

    """

    def load_graph(self, songLibaray):
        self.song_lib_obj = SongLibrary()
        self.song_lib_obj.loadLibrary(songLibaray)  # creates a song lib obj then loads the song array

        self.graph_obj = Graph()  # Creates a graph object

        # create a vertex for each unique artist by iterating over the artist list and iterating over each
        # artist's coartist list if the artist of the current iteration already has a vertex it writes over it
        for i in range(len(self.song_lib_obj.songArray)):
            cur_song = self.song_lib_obj.songArray[i]
            self.graph_obj.addVertex(cur_song.artist)

            # this for loop makes a vertex for every one of the artists co artist
            for cur_coartist in cur_song.collaborators:
                self.graph_obj.addVertex(cur_coartist)

        self.numVertices = len(self.graph_obj.vertList)

        # add in the songs that each artist writes and adds them to a list within each artist's vertex
        for i in range(len(self.song_lib_obj.songArray)):
            cur_song = self.song_lib_obj.songArray[i]
            self.graph_obj.addSongs(cur_song.artist, cur_song.title)

        # this adds the amount of times the artist has worked with each of its colaborators to a coloborators
        # dictionary stored with in each vertex
        for i in range(len(self.song_lib_obj.songArray)):
            cur_song = self.song_lib_obj.songArray[i]

            # for each co artist
            for cur_coartist in cur_song.collaborators:

                # incase the artist is in the co artist list this prevents it from connecting an artist to itself
                if cur_song.artist not in cur_coartist:

                    # if there are coartists are listed already then the cost just increases by 1
                    if cur_coartist in self.graph_obj.vertList[cur_song.artist].coArtists:
                        count = self.graph_obj.vertList[cur_song.artist].coArtists[cur_coartist] + 1
                    else:
                        count = 1

                    # calls the Graph class to add the weight to the connection between the artists
                    self.graph_obj.addEdge(cur_song.artist, cur_coartist, count)
                    self.graph_obj.addEdge(cur_coartist, cur_song.artist, count)

        self.vertList = self.graph_obj.vertList
        self.numVertices = len(self.graph_obj.vertList)
        return self.numVertices

    """
    Return song libary information
    """

    def graph_info(self):
        return "Vertex Size: " + str(self.numVertices)

    """
    FUNCTION DESCRIPTION
    This function searches  the information of an artist based on the artist name and returns
    a tuple: (the number of songs he/she wrote, the collaborative artist list)
    """

    def search_artist(self, artist_name):

        tempLst = list(self.graph_obj.vertList[artist_name].coArtists.keys())
        numSongs = len(self.graph_obj.vertList[artist_name].songs)

        tup1 = numSongs, tempLst

        return tup1

    """
    FUNCTION DESCRIPTION
    This function calculates then returns a list of collaborators that are two connections 
    away from the current artist.
    """

    def find_new_friends(self, artist_name):
        two_hop_friends = []

        # creates a list of the artists the given artists has colabed with
        temp_colab_artists = list(self.graph_obj.vertList[artist_name].coArtists.keys())
        temp_colab_artists.append(artist_name)

        # creates a list of all the two hop artists
        for temp_artist in temp_colab_artists:
            two_hop_friends += (list(self.graph_obj.vertList[temp_artist].coArtists.keys()))

        # remove the artists in the  colab from the two hop
        colabartists = list(set(two_hop_friends) - set(temp_colab_artists))

        return colabartists

    """
    FUNCTION DESCRIPTION
    This function analyzes the list of two hop artists and returns the artist that has written
    the most songs with their collaborative artists.
    """

    def recommend_new_collaborator(self, artist_name):

        two_hop_cost = {}  # initiates a dictionary
        one_hop_artists = list(self.graph_obj.vertList[artist_name].coArtists.keys())

        # iterates over the one co artists for the artists passed in the function call
        for temp_one_hop_artist in one_hop_artists:

            # iterates over the co artists of the coartists of the artists passed in the function call
            for temp_two_hop_artist in self.graph_obj.vertList[temp_one_hop_artist].coArtists:
                # adds to the dictionay for the cost to go from ne artist to the next
                two_hop_cost[temp_two_hop_artist] = self.graph_obj.vertList[temp_one_hop_artist].coArtists[
                    temp_two_hop_artist]

        artist = max(two_hop_cost, key=two_hop_cost.get)
        numSongs = two_hop_cost[artist]

        return artist, numSongs

    """
    FUNCTION DESCRIPTION
    This function finds the least number of connections between the artist it is passed and all other artists. 
    It returns a library with the keys being the name of the other artists and the values being the number of 
    connections away the artists are.
    """

    def shortest_path(self, initial_vert):
        cur_vert = initial_vert  # current vertex

        unvisited_vertexs = set(self.vertList.keys())

        # keeps track of the vertexs that have and have not been visited. 0 means not 1 means visited
        visited = dict.fromkeys(unvisited_vertexs, 0)

        # initializes the necessary dictionaries needed for the search algorithm
        hops_dict = dict.fromkeys(unvisited_vertexs, float("inf"))
        hops_count_dict = dict.fromkeys(unvisited_vertexs, 0)
        hops_search_dict = dict(hops_dict)
        hops_dict[cur_vert] = 0

        # while there are still
        while len(unvisited_vertexs) > 0:
            # for each of the curent verts neighbors
            for neighbor in self.vertList[cur_vert].coArtists:
                if visited[neighbor] == 0:
                    # calculates the weight of hopping directly to the neighbor
                    tentative_hop_weight = hops_count_dict[cur_vert] + 1

                    if tentative_hop_weight < hops_dict[neighbor]:
                        hops_count_dict[neighbor] = tentative_hop_weight
                        hops_dict[neighbor] = tentative_hop_weight
                        hops_search_dict[neighbor] = tentative_hop_weight

            # marks the curent vertex visited
            visited[cur_vert] = 1

            del hops_search_dict[cur_vert]
            unvisited_vertexs.remove(cur_vert)

            # finds the next vertex to visit based on what is the least hops away
            if len(unvisited_vertexs) > 0:
                cur_min_hop_vert = min(hops_search_dict, key=hops_search_dict.get)
                cur_vert = cur_min_hop_vert

        return hops_count_dict

    """
    FUNCTION DESCRIPTION
    This function uses Dijkstra's algorithm to find the shortest path from the passed artist to all other
    artists. It returns a dictionary where the keys are the artists names and the values are the number of 
    songs between the passed artist and the key artist.
"""
    def Dijkstra_shortest_path(self, initial_vert):
        cur_vert = initial_vert  # current vertex

        unvisited_vertexs = set(self.vertList.keys())

        # keeps track of the vertexs that have and have not been visited. 0 means not 1 means visited
        visited = dict.fromkeys(unvisited_vertexs, 0)

        # initializes the necessary dictionaries needed for the search algorithm
        vert_dist = dict.fromkeys(unvisited_vertexs, float("inf"))
        search_dict = dict(vert_dist)
        vert_dist[cur_vert] = 0

        while len(unvisited_vertexs) > 0:
            # for each of the curent verts neighbors
            for neighbor in self.vertList[cur_vert].coArtists:
                if visited[neighbor] == 0:
                    tenative_weight = vert_dist[cur_vert] + self.vertList[cur_vert].coArtists[neighbor]

                    # if the new calculated weight is less than the one previously calculated
                    if tenative_weight < vert_dist[neighbor]:
                        vert_dist[neighbor] = tenative_weight
                        search_dict[neighbor] = tenative_weight

            # marks the curent vertex visited
            visited[cur_vert] = 1
            del search_dict[cur_vert]
            unvisited_vertexs.remove(cur_vert)

            # finds the next vertex to visit

            if len(unvisited_vertexs) > 0:
                cur_vert = min(search_dict, key=search_dict.get)

        return vert_dist


# WRITE YOUR OWN TEST UNDER THAT IF YOU NEED
if __name__ == '__main__':
    artistGraph = ArtistConnections()

    artistGraph.load_graph("TenKsongs_proj2.csv")
    artistGraph.search_artist("Mariah Carey")
    artistGraph.find_new_friends("Mariah Carey")
    artistGraph.recommend_new_collaborator("Mariah Carey")
    print(artistGraph.shortest_path("Mariah Carey"))
    print(artistGraph.Dijkstra_shortest_path("Mariah Carey"))

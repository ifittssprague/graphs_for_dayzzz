"""
Isaac Fitts-Sprague
29312728
ECE-241 Data Structures

FILE DESCRIPTION
The file contains the Song and SongLibrary classes that are used by the ArtistConnections class.
The Song class is used to instantiate song objects and is called only by the SongLibrary class.
The SongLibrary class is called by the ArtistConnections class and is used to read in a CSV file
and instantiate Song objects.
"""


class Song:

    def __init__(self, songRecord):

        tokens = songRecord.split(',')
        if len(tokens) != 6:
            print("incorrect song record")
        else:
            self.title = tokens[1]
            self.artist = tokens[2]
            self.duration = tokens[3]
            self.trackID = tokens[4]
            teststr = tokens[5]
            teststr = teststr[:len(teststr) - 1].split(';')
            self.collaborators = teststr

    def toString(self):
        return "Title: " + self.title + ";  Artist: " + self.artist


class SongLibrary:

    def __init__(self):
        self.songArray = list()
        self.isSorted = False
        self.size = 0

    def loadLibrary(self, inputFilename):
        with open(inputFilename, 'r') as file:
            lines = file.readlines()
            # CHANGED FOR DEBUGGING
            # lines=lines[0:10]

            for line in lines:
                song = Song(line)
                self.songArray.append(song)
                self.size += 1

        file.close()

    """
    Return song libary information
    """

    def libraryInfo(self):
        return "Size: " + str(self.size) + ";  isSorted: " + str(self.isSorted)

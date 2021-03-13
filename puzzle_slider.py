from tkinter import*
from tkinter.ttk import Entry,Button,OptionMenu
from PIL import Image,ImageTk
import random
import tkinter.filedialog
import os

# creating tiles class
class Tiles():
    def __init__(self,grid):
        self.tiles = []
        self.grid = grid
        self.gap = None
        self.moves = 0
    # creating an add member fuction for adding all the tiles
    def add(self,tile):
        self.tiles.append(tile)

    # changing tile's position
    def getTile(self,*pos):
        for tile in self.tiles:
            if tile.pos == pos:
                return tile

    # moving tiles
    def getTileAroundGap(self):
        gRow, gCol = self.gap.pos
        return self.getTile(gRow,gCol-1),self.getTile(gRow-1,gCol),self.getTile(gRow,gCol+1),self.getTile(gRow+1,gCol)

    # moving the empty tile
    def changeGap(self,tile):
        try:
            gPos = self.gap.pos
            self.gap.pos = tile.pos
            tile.pos = gPos
            self.moves += 1
        except :
            pass
    # changing the gap using arrow keys
    def slide(self,key):
        left,top,right,down = self.getTileAroundGap()
        if key == 'Up':
            self.changeGap(down)
        if key == 'Down':
            self.changeGap(top)
        if key == 'Left':
            self.changeGap(right)
        if key == 'Right':
            self.changeGap(left)
        self.show()

    # fuction for shuffling the image tiles
    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0
        for row in range(self.grid):
            for col in range(self.grid):
                self.tiles[i].pos = (row,col)
                i+=1

    def show(self):
        for tile in self.tiles:
            if self.gap != tile:
                tile.show()
    # deleting a tile
    def setGap(self,index):
        self.gap = self.tiles[index]

    def isCorrect(self):
        for tile in self.tiles:
            if not tile.isCorrectPos():
                return False
        return True

class Tile(Label):
    def __init__(self,parent,image,pos):
        Label.__init__(self,parent,image = image)

        self.image = image
        self.pos = pos
        self.curPos = pos

    def show(self):
        self.grid(row = self.pos[0],column = self.pos[1])

    def isCorrectPos(self):
        return self.pos == self.curPos

# creating game board class
class  Board(Frame):
    MAX_BOARD_SIZE = 500
    # declaring class members and member functions
    def __init__(self,parent,image,grid,win,*args,**kwargs):
        Frame.__init__(self,parent,*args,**kwargs)

        self.parent = parent
        self.grid = grid
        self.win = win
        self.image = self.openImage(image)
        self.tileSize = self.image.size[0]/self.grid
        self.tiles = self.createTiles()
        self.tiles.shuffle()
        self.tiles.show()
        self.bindKeys()
    # defining openImage fuction for resizing or croping image to match board size
    def openImage(self,image):
        image = Image.open(image)
        if min(image.size) > self.MAX_BOARD_SIZE:
            image = image.resize((self.MAX_BOARD_SIZE,self.MAX_BOARD_SIZE),Image.ANTIALIAS)
        if image.size[0] == image.size[1]:
            image = image.crop((0,0,image.size[0],image.size[0]))
        return image
    # creating tiles of that image
    def createTiles(self):
        tiles = Tiles(self.grid)
        for row in range(self.grid):
            for col in range(self.grid):
                x0 = col*self.tileSize
                y0 = row*self.tileSize
                x1 = x0 + self.tileSize
                y1 = y0 + self.tileSize
                tileImage = ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                tile = Tile(self,tileImage,(row,col))
                tiles.add(tile)
        tiles.setGap(-1)
        return tiles

    # binding keys to move tiles
    def bindKeys(self):
        self.bind_all('<Key-Up>',self.slide)
        self.bind_all('<Key-Down>',self.slide)
        self.bind_all('<Key-Right>',self.slide)
        self.bind_all('<Key-Left>',self.slide)

    # checking if tiles are in current position
    def slide(self,event):
        self.tiles.slide(event.keysym)
        if self.tiles.isCorrect():
            self.win(self.tiles.moves)
# declaring Main class
class Main():
    # declaring class members and fuctions
    def __init__(self,parent):
        self.parent = parent

        self.image = StringVar()
        self.winTex = StringVar()
        self.grid = IntVar()
        self.createWidgets()

    # creating main frame of the game
    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame,text = "Puzzle Slider",font =('',50)).pack(padx=10,pady=10)
        frame = Frame(self.mainFrame)
        Label(frame,text='Image').grid(sticky = W)
        Entry(frame,textvariable = self.image, width =50).grid(row=0,column=1,padx=10,pady=10)
        Button(frame,text ='Browse',command = self.browse).grid(row=0,column=2,pady=10)
        Label(frame,text='Grid').grid(sticky = W)
        OptionMenu(frame,self.grid,*[3,4,5,6,7,8,9,10]).grid(row=1,column=1,padx=10,pady=10, sticky=W)
        frame.pack(padx=1,pady=10)
        Button(self.mainFrame, text = "Start", command =self.start).pack(padx=10,pady=10)
        self.mainFrame.pack()
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)
        Label(self.winFrame,textvariable = self.winTex,font = ('',50)).pack(padx=10,pady=10)
        Button(self.winFrame,text = 'Play Again',command = self.playAgain).pack(padx=10,pady=10)
    # creating start fuction
    def start(self):
        image = self.image.get()
        grid = self.grid.get()
        if os.path.exists(image):
            # declaring Game Board
            self.board = Board(self.parent,image,grid,self.win)
            # hiding main frame
            self.mainFrame.pack_forget()
            # visibolizing board
            self.board.pack()
    # defining browse func for browing images with jpg and png formats only
    def browse(self):
        self.image.set(filedialog.askopenfilename(title="Select Image",filetype= (("jpg File","*.jpg"),("png File","*.png"))))

    # win memeber fuction
    def win(self,moves):
        self.board.pack_forget()
        self.winTex.set('You Won!!! (with {0} moves)'.format(moves))
        self.winFrame.pack()
    # play again memeber fuction
    def playAgain(self):
        self.winFrame.pack_forget()
        self.mainFrame.pack()

# declaring main program
if __name__ == "__main__":
    root = Tk()
    Main(root)
    root.mainloop()

import sys
import os
import pyglet
import cocos
from cocos.director import director
from cocos.sprite import Sprite

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class Trajectory():
    def __init__(Self):
        print("log")

    def start():
        print("log")

    def stop():
        print("log")


class Enemy(cocos.layer.Layer):
    def __init__(self):
        super( Enemy, self ).__init__()

        self.ww = director.window.width
        self.wh = director.window.height

        sprite = Sprite('images/spaceship.gif')
        sprite.position = 320,240
        self.add( sprite, z=1 )


class Paddle(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, fixedY):
        super(Paddle, self).__init__()

        self.y = fixedY
        self.offsetX = 76;
        self.width = 159

        self.sprite = Sprite("images/paddle.png")
        self.add( self.sprite)
        self.sprite.position = 0, 0

    def setX(self, x):
        self.position = x, self.y

    def on_mouse_motion (self, x, y, dx, dy):
        x = x-self.width/2
        if x < self.width/2:
            x = self.width/2
        elif x > 616-self.width/2:
            x = 616-self.width/2
        self.position = x, self.y


class GameScene(cocos.layer.Layer):
    def __init__(self):
        super(GameScene, self).__init__()


        self.dimension = 616
        self.position = 76, 348

        track_sprite = Sprite('images/track.png')
        track_sprite.position = self.dimension/2, 27
        self.add( track_sprite, z=1 )

        self.paddle = Paddle(27)
        self.paddle.setX(self.dimension/2)
        self.add( self.paddle, z=2)



class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super( BackgroundLayer, self ).__init__()

        board_bg = Sprite('images/boardbg.png')
        board_bg.position = director.window.width/2,director.window.height*0.611
        self.add( board_bg, z=0 )


class ForegroundLayer(cocos.layer.Layer):
    def __init__(self):
        super( ForegroundLayer, self ).__init__()

        board = Sprite('images/board.png')
        board.position = director.window.width/2,director.window.height/2
        self.add( board, z=1 )


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    director.init( width=768, height=1024, caption="Pong Attack" )

    # And now, start the application, starting with main_scene
    director.run (cocos.scene.Scene (BackgroundLayer(), GameScene(), ForegroundLayer()))

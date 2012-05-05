import sys
import os
import math
import pyglet
import cocos

from cocos.director import director
from cocos.sprite import Sprite

import cocos.euclid as eu
import cocos.collision_model as cm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class CollidableRectSprite(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y):
        super(CollidableRectSprite, self).__init__(image)
        self.position = (center_x, center_y)
        self.vector2 = eu.Vector2(center_x, center_y)
        self.cshape = cm.AARectShape(self.vector2, self.width/2, self.height/2)
        print(self.width, self.height, self.cshape, self.vector2)

# Movements
class BounceBoundedMove(cocos.actions.move_actions.Move):
    def __init__(self, width, height, offsetY):
        super(BounceBoundedMove, self).__init__()
        self.width = width
        self.height = height
        self.offsetY = offsetY

    def start(self):
        self.target.position = self.width/2, self.height/2
        self.half_width = self.target.width/2
        self.half_height = self.target.height/2

    def step(self, dt):
        pos = self.target.position
        vel = self.target.velocity

        if pos[0] < self.half_width and vel[0] < 0:
            vel = math.fabs(vel[0]), vel[1]
            if "collide_left" in vars(self): self.collide_left()
        elif pos[0] > self.width - self.half_width and vel[0] > 0:
            vel = -math.fabs(vel[0]), vel[1]
            if "collide_right" in vars(self): self.collide_right()

        if pos[1] < self.offsetY + self.half_height and vel[1] < 0:
            vel = vel[0], math.fabs(vel[1])
            if "collide_bottom" in vars(self): self.collide_bottom()
        elif pos[1] > self.height - self.half_height and vel[1] > 0:
            vel = vel[0], -math.fabs(vel[1])
            if "collide_top" in vars(self): self.collide_top()

        self.target.velocity = vel
        self.target.position = pos[0] + vel[0]*dt, pos[1] + vel[1]*dt



class Monster(cocos.layer.Layer):
    def __init__(self):
        super( Monster, self ).__init__()

        self.ww = director.window.width
        self.wh = director.window.height

        sprite = Sprite('images/spaceship.gif')
        sprite.position = 320,240
        self.add( sprite, z=1 )


class Paddle(object):
    def __init__(self, fixedY):
        super(Paddle, self).__init__()

        self.y = fixedY
        self.offsetX = 76;

        self.sprite = CollidableRectSprite("images/paddle.png", 100, 400)

    def setPosition(self, x, scene_width):
        width = self.sprite.width
        if x < width: x = width
        elif x > scene_width: x = scene_width
        self.sprite.position = x-width/2, self.y


class GameScene(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(GameScene, self).__init__()


        self.dimension = 616
        self.position = 76, 348


        track_sprite = Sprite('images/track.png')
        track_sprite.position = self.dimension/2, 27
        self.add( track_sprite, z=1 )

        # ball and movement
        ball_movement = BounceBoundedMove(self.dimension, self.dimension, 10)
        ball_movement.collide_bottom = self.ball_collide_bottom
        self.ball = CollidableRectSprite("images/ball.png", 100, 400)
        self.add(self.ball, z=10)
        self.ball.velocity = (200, 136)
        self.ball.do(ball_movement)


        # paddle
        self.paddle = Paddle(27)
        self.paddle.setPosition(self.dimension/2, self.dimension)
        self.add( self.paddle.sprite, z=2)


        collision = cm.CollisionManager();
        collision.clear()
        collision.add(self.paddle.sprite)
        collision.add(self.ball)
        print(collision.known_objs(), collision.any_near(100, 400))

    def ball_collide_bottom(self):
        print ("hit bottom")
        #print(self.collision.known_objs(), self.collision.they_collide(self.ball, self.paddle.sprite))

    def on_mouse_motion (self, x, y, dx, dy):
        self.paddle.setPosition(x, self.dimension)







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

    game_scene = GameScene()
    # And now, start the application, starting with main_scene
    director.run (cocos.scene.Scene (BackgroundLayer(), game_scene, ForegroundLayer()))


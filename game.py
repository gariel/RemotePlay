

import pygame
import zmq
from threading import Thread

class Receive(Thread):
    def __init__(self, game):
        Thread.__init__(self)
        self.game = game

    def run(self):
        try:
            context = zmq.Context()
            sock = context.socket(zmq.REP)
            sock.connect('tcp://localhost:8888')
            print("aaaaaaa")
            while True:
                msg = str(sock.recv())
                sock.send_string("ok")
                print(msg)
                a = msg.split("'")
                print(a)
                b = a[1]
                p, d = b.split('_')
                print(p, d)
                self.game.button(int(p), d)
        except Exception as e:
            print(e)
        finally:
            context.term()

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Game:
    def __init__(self):
        self.ps = [Player(30, 30, (0, 128, 255)), Player(130, 30, (0, 255, 128))]

    def button(self, p, button):
        if(button == "left"):
            self.ps[p-1].x -= 10
        if(button == "right"):
            self.ps[p-1].x += 10
        if(button == "up"):
            self.ps[p-1].y -= 10
        if(button == "down"):
            self.ps[p-1].y += 10

    def run(self):

        pygame.init()
        screen = pygame.display.set_mode((800, 600))#pygame.FULLSCREEN)

        ship_filename = 'ship.png'
        ship = pygame.image.load(ship_filename).convert_alpha()
        
        done = False
        is_blue = True
        while not done:
            screen.fill((0, 0, 0))
            for p in self.ps:
                screen.blit(ship, (p.x, p.y))
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    rec = Receive(game)
    rec.daemon = True
    rec.start()
    game.run()
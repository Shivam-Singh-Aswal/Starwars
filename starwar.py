''' starwars '''

#using pygame module 1.9.6

#import the module
import pygame, random, time

#initialise the module
pygame.init ()

#creating the window class
class window :
    def __init__ (self) :
        pass

    def load (self) :
        #declaring the size of the displaying surface
        self.width = 1200
        self.height = 600
        
        #declaring the main window and its other parameters
        self.window = pygame.display.set_mode ((self.width, self.height))
        pygame.display.set_caption ('Star Wars')
        self.bg_img = pygame.image.load ('space.jpg')
        self.window.blit (self.bg_img, (0, 0))
        pygame.display.update ()

        
#creating the classes
class game (window) :
    def __init__ (self) :
        self.load ()
        
        #clock variable and the frame rate
        self.clock = pygame.time.Clock ()
        self.frame_rate = 30

        #the battle ship instance
        self.fighter = ship (self)

        #the meteor counter
        self.ismeteor = 50
        self.meteor_list = []

        # bullet variable
        self.isbullet = True
        self.bullet_count = 0

        #score calc and timing and level
        self.level = 1
        self.time = 30
        self.timer = 0
        self.score = 0
        self.vel_list = [2, 4, 6]
        return

    def play (self) :
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        #the main game variable
        self.run = True

        while self.run :
            #arrest the speed
            self.clock.tick (self.frame_rate)
            self.timer += 1

            #check for the events by traversing through the event list
            for event in pygame.event.get() :
                #quit program on the quit event
                if event.type == pygame.QUIT :
                    self.run = False
                #event to fire the bullets
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_p :
                        self._pause ()
                    if event.key == pygame.K_SPACE and self.isbullet :
                        self.isbullet = False
                        self.bullet_count = 0
                        my_bullet = bullet (self, self.fighter)
                        self.fighter.bullet_list.append (my_bullet)

            #keys that are pressed continuously
            keys_pressed = pygame.key.get_pressed ()

            #move the starship
            if keys_pressed [pygame.K_LEFT] :
                self.fighter.velbox [0] = -self.fighter.vel
            elif keys_pressed [pygame.K_RIGHT] :
                self.fighter.velbox [0] = self.fighter.vel
            else :
                self.fighter.velbox [0] = 0
            if keys_pressed [pygame.K_UP] :
                self.fighter.velbox [1] = -self.fighter.vel
            elif keys_pressed [pygame.K_DOWN] :
                self.fighter.velbox [1] = self.fighter.vel
            else :
                self.fighter.velbox [1] = 0
            
            #create the meteors
            if self.ismeteor == 50 :
                a = meteor (self)
                self.meteor_list.append (a)

            #update the screen
            self.refresh ()

        #quit the game
        pygame.quit ()
        return

    def bullet_hit (self) :
        hit_list = []
        for bullet in self.fighter.bullet_list :
            if bullet.y < 0 :
                hit_list.append (bullet)
            else :
                for stone in self.meteor_list :
                    if bullet.hit_box.colliderect (stone.hit_box) :
                        self.score += 5
                        hit_list.append (bullet)
                        self.meteor_list.remove (stone)
                        break
        if hit_list :
            for element in hit_list :
                self.fighter.bullet_list.remove (element)
        return
    
    def meteor_hit (self) :
        for asteroid in self.meteor_list :
            if asteroid.hit_box.colliderect (self.fighter.hit_box) :
                self.run = False
                self.message ('GAME OVER !!!')
        return
    
    def _pause (self) :
        paused = True
        while paused :
            for event in pygame.event.get () :
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p :
                    paused = False
        return

    def scorecard_time (self) :
        #scorecard and other stuffs
        font = pygame.font.SysFont ('Century', 26, True)
        font_ = pygame.font.SysFont ('Century', 24, False)
        subsurf1 = font.render ('Score : ' + str (self.score), 1, (255, 255, 255))
        subsurf2 = font_.render ('Time left : ' + str (self.time), 1, (255, 255, 255))
        subsurf3 = font_.render ('Level : ' + str (self.level), 1, (255, 255, 255))
        
        self.window.blit (subsurf1, (self.width - 200, 20))
        self.window.blit (subsurf3, (10, 20))
        self.window.blit (subsurf2, (10, 50))        
        return
    
    def message (self, msg) :
        font = pygame.font.SysFont ('Century', 24, True)
        subsurf = font.render (msg, 1, (0, 0, 255))
        subsurf_ = font.render ('FINAL SCORE : ' + str (self.score), 1, (0, 0, 255))
        self.window.fill ((255, 255, 255))
        self.window.blit (subsurf, (self.width //2 - 30, self.height // 2 - 48))
        self.window.blit (subsurf_, (self.width //2 - 30, self.height // 2 - 16))
        pygame.display.update ()
        time.sleep (3)
        
        return
    
    def refresh (self) :
        self.window.blit (self.bg_img, (0, 0))
        #draw the fighter plane onto the main surface
        self.fighter.draw ()
        #draw the bullets onto the surface
        if self.fighter.bullet_list :
            self.bullet_hit ()
            for bullet in self.fighter.bullet_list :
                bullet.draw ()

        #draw the meteors
        for enemy in self.meteor_list : enemy.draw ()

        #meteor delay
        if self.ismeteor == 50 : self.ismeteor = 0
        else : self.ismeteor += 1
        
        #bullet delay
        if self.bullet_count == 5 :
            self.bullet_count = 0
            self.isbullet = True
        else : self.bullet_count += 1

        #increment in the score and others
        if self.timer == 30 :
            self.timer = 0
            self.time -= 1
        if self.time == 0 :
            self.time = 30
            self.level += 1
        self.scorecard_time ()
        
        #checking for the meteor hit
        self.meteor_hit ()
        if self.level == 4 :
            self.run = False
            self.message ('YOU WIN !!!')
        
        #display the changes
        pygame.display.update ()
        


class game_object :
    def __init__ (self) :
        pass
    
    def load_object (self, path = None, para = ()) :
        if path :
            self.object = 'image'
            self.image = pygame.image.load (path [0])
            # Transform the image to the required scale
            try :
                self.width = path [1][0]
                self.height = path [1][1]
            except :
                self.width = self.image.get_width ()
                self.height = self.image.get_height ()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else :
            self.parameters = para
            self.object = 'shape'
            self.radius = self.parameters [0]
        return

    def box (self) :
        if self.object == 'image' :
            self.hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
        elif self.object == 'shape' :
            self.hit_box = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        return

    def move (self) :
        self.x += self.velbox [0]
        self.y += self.velbox [1]
        self.hit_box [0] += self.velbox [0]
        self.hit_box [1] += self.velbox [1]
        return
        
    def draw (self) :
        self.move ()
        if self.object == 'image':
            self.game.window.blit (self.image, (self.x, self.y))
        elif self.object == 'shape' :
            pygame.draw.circle (self.game.window, self.parameters [1], (self.x, self.y), self.radius, 2)
        return
    
        
class ship (game_object) :
    def __init__ (self, game) :
        self.game = game
        self.load_object (path = ['fighter.png'])
        self.x = self.game.width // 2
        self.y = self.game.height - self.height
        self.box ()
        self.vel = 8
        self.velbox = [0, 0]
        self.bullet_list = []
        return
        

class bullet (game_object) :
    def __init__ (self, game, ship) :
        self.game = game
        self.ship = ship
        self.load_object (para = (5, (0, 255, 0)))
        self.x = self.ship.x + self.ship.width // 2
        self.y = self.ship.y
        self.box ()
        self.velbox = [0, -13]
        return
    

class meteor (game_object) :
    def __init__ (self, game) :
        self.game = game
        self.load_object (path = ['meteor1.png', (60, 60)])
        self.x = random.randint (0, self.game.width - self.width)
        self.y = -self.height
        self.box ()
        self.velbox = [0, self.game.vel_list [self.game.level - 1]]
        return


#the calling statement
if __name__ == '__main__' : 
    my_game = game ()
    my_game.play ()

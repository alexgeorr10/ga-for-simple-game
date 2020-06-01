import random
import pygame


screen_width, screen_height = 800, 800
win = pygame.display.set_mode((screen_width, screen_height))
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]
k_buttons = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]


class Agent:
    def __init__(self, x=10, y=10, r=10, vel=10, color=(0, 0, 255), brain=None):
        self.x = x
        self.y = y
        self.r = r
        self.vel = vel
        self.color = color
        self.mind = brain

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

    def move(self, direction):
        self.x += direction[0]*self.vel
        self.y += direction[1]*self.vel

    def enters(self, x, y, w, h):
        return x < self.x+self.r and self.x-self.r < x+w and y < self.y+self.r and self.y-self.r < y+h

    def get_fitness(self, goal):
        return 100.0/((self.x-goal.x)**2+(self.y-goal.y)**2+1)

    def buttons_pressed(self, stp, eve):
        self.mind[stp] = eve

    def plays_a_move(self, who=True, hkeys=None, cnew_event=None):
        """If who is True, a human plays with the keyboard. Otherwise, the agents are played by the computer"""
        if who:
            if hkeys[pygame.K_LEFT]:
                condition = False
                for o in obstacles:
                    roo = self.enters(o.x+o.w, o.y, self.vel, o.h)
                    condition = condition or roo
                if self.x-self.r-self.vel >= 0 and not condition:
                    self.move((-1, 0))
            if hkeys[pygame.K_RIGHT]:
                condition = False
                for o in obstacles:
                    loo = self.enters(o.x-self.vel, o.y, self.vel, o.h)
                    condition = condition or loo
                if self.x+self.r+self.vel <= screen_width and not condition:
                    self.move((1, 0))
            if hkeys[pygame.K_UP]:
                condition = False
                for o in obstacles:
                    bo = self.enters(o.x, o.y+o.h, o.w, self.vel)
                    condition = condition or bo
                if self.y-self.r-self.vel >= 0 and not condition:
                    self.move((0, -1))
            if hkeys[pygame.K_DOWN]:
                condition = False
                for o in obstacles:
                    ao = self.enters(o.x, o.y-self.vel, o.w, self.vel)
                    condition = condition or ao
                if self.y+self.r+self.vel <= screen_height and not condition:
                    self.move((0, 1))
            if hkeys[pygame.K_SPACE]:
                self.x = screen_width-self.x
                self.y = screen_height-self.y
            if hkeys[pygame.K_c]:
                self.color = random.choice(
                    [c for c in colors if c != self.color])
        else:
            if cnew_event.key == 276:
                condition = False
                for o in obstacles:
                    roo = self.enters(o.x+o.w, o.y, self.vel, o.h)
                    condition = condition or roo
                if self.x-self.r-self.vel >= 0 and not condition:
                    self.move((-1, 0))
            if cnew_event.key == 275:
                condition = False
                for o in obstacles:
                    loo = self.enters(o.x-self.vel, o.y, self.vel, o.h)
                    condition = condition or loo
                if self.x+self.r+self.vel <= screen_width and not condition:
                    self.move((1, 0))
            if cnew_event.key == 273:
                condition = False
                for o in obstacles:
                    bo = self.enters(o.x, o.y+o.h, o.w, self.vel)
                    condition = condition or bo
                if self.y-self.r-self.vel >= 0 and not condition:
                    self.move((0, -1))
            if cnew_event.key == 274:
                condition = False
                for o in obstacles:
                    ao = self.enters(o.x, o.y-self.vel, o.w, self.vel)
                    condition = condition or ao
                if self.y+self.r+self.vel <= screen_height and not condition:
                    self.move((0, 1))


class Obstacle:
    def __init__(self, x=0, y=screen_width//2, w=500, h=100, color=(200, 140, 98)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))


class Goal:
    def __init__(self, x=screen_width-30, y=screen_height-30, r=10, color=(150, 0, 0)):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def set_color(self, color):
        self.color = color

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)


def mutated_brain(brain, steps_changed=30):
    """Mutates the brain of an agent. Either generally or at the beginning, middle, or late in the game."""
    how = random.randint(0, 3)
    if how == 0:
        for _ in range(2*steps_changed):
            new_event = pygame.event.Event(
                pygame.KEYDOWN, key=random.choice(k_buttons))
            # pygame.event.post(new_event)
            brain[random.randint(0, game_steps)] = new_event
        return brain
    if how == 1:
        for _ in range(steps_changed):
            new_event = pygame.event.Event(
                pygame.KEYDOWN, key=random.choice(k_buttons))
            # pygame.event.post(new_event)
            brain[random.randint(0, int(game_steps/3))] = new_event
        return brain
    if how == 2:
        for _ in range(steps_changed):
            new_event = pygame.event.Event(
                pygame.KEYDOWN, key=random.choice(k_buttons))
            # pygame.event.post(new_event)
            brain[random.randint(int(game_steps/3), 2 *
                                 int(game_steps/3))] = new_event
        return brain
    if how == 3:
        for _ in range(steps_changed):
            new_event = pygame.event.Event(
                pygame.KEYDOWN, key=random.choice(k_buttons))
            # pygame.event.post(new_event)
            brain[random.randint(2*int(game_steps/3), game_steps)] = new_event
        return brain


def main_loop(agnts, gen, player=False):
    """Main loop of the game"""
    pygame.init()
    pygame.display.set_caption('Generation: {}'.format(gen))
    run = True
    step = 0
    while run and step <= game_steps:
        pygame.time.delay(20)

        if player:
            keys = pygame.key.get_pressed()
            agnts[0].plays_a_move(True, hkeys=keys)
        else:
            for j in range(number):
                new_event = pygame.event.Event(
                    pygame.KEYDOWN, key=random.choice(k_buttons))
                pygame.event.post(new_event)
                # agnts[j].plays_a_move(False, cnew_event=new_event)
                # agnts[j].buttons_pressed(step, new_event)

                if step not in agnts[j].mind.keys():
                    agnts[j].plays_a_move(False, cnew_event=new_event)
                    agnts[j].buttons_pressed(step, new_event)
                else:
                    agnts[j].plays_a_move(
                        False, cnew_event=agnts[j].mind[step])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if player:
            if (agnts[0].x-g.x)**2+(agnts[0].y-g.y)**2 < (g.r+agnts[0].r)**2:
                g.set_color((0, 150, 0))
        else:
            for j in range(number):
                if (agnts[j].x-g.x)**2+(agnts[j].y-g.y)**2 < (g.r+agnts[j].r)**2:
                    g.set_color((0, 150, 0))

        # Draw
        win.fill((210, 230, 220))
        for obst in obstacles:
            obst.draw()
        if player:
            agnts[0].draw()
        else:
            for j in range(number):
                agnts[j].draw()

        g.draw()
        pygame.display.update()
        step += 1


def next_gen_agents(agnts, steps_changed):
    """Updates the agents. It keeps the number*percent_to_keep best and the rest are
    mutations of the best."""
    best_agents_fitness = sorted([(i, -agnts[i].get_fitness(
        g)) for i in range(number)], key=lambda t: t[1])[: int(number*percent_to_keep)]
    best_agents_index = [t[0] for t in best_agents_fitness]
    best_agents_brain = [agnts[i].mind for i in best_agents_index]
    best_agents = [Agent(10, 10, 10, 10, (0, 0, 255), best_agents_brain[i])
                   for i in range(int(number*percent_to_keep))]
    agnts = best_agents
    times = int(1/percent_to_keep)-1
    for _ in range(times):
        agnts = [Agent(10, 10, 10, 10, (135, 206, int(
            255-255*(i/number))), mutated_brain(best_agents_brain[i].copy(), steps_changed)) for i in range(int(number*percent_to_keep))]+agnts
    return agnts


# Goal----------------------------------------------------------------------------------
g = Goal()

# Obstacles-----------------------------------------------------------------------------
o1 = Obstacle(0,   100, 500, 40, (200, 140, 98))
o2 = Obstacle(300, 200, 500, 20, (200, 140, 98))
o3 = Obstacle(0,   300, 100, 40, (200, 140, 98))
o4 = Obstacle(200,   300, 420, 20, (200, 140, 98))
o5 = Obstacle(600, 450, 200, 20, (200, 140, 98))
o6 = Obstacle(0, 550, 600, 20, (200, 140, 98))
o7 = Obstacle(400, 600, 400, 20, (200, 140, 98))

obstacles = [o4, o5, o6]

# Hyperparameters-----------------------------------------------------------------------
number = 100
percent_to_keep = 0.1   # 1/percent_to_keep must be integer
game_steps = 300        # 500 
steps_to_change = 20

def ga(human):
    """Genetic algorithm to win the game. You may play the game by passing True for the boolean variable human."""

    # Initialize the agents---------------------------------------------------------------------
    agents = []
    for i in range(number):
        agents.append(
            Agent(10, 10, 10, 10, (135, 206, 255-255*(i/number*percent_to_keep)), brain={}))

    # Generations loop----------------------------------------------------------------------
    generation = 0
    while g.color != (0, 150, 0):
        generation += 1
        main_loop(agents, generation, human)
        agents = next_gen_agents(agents, steps_to_change)

    print('It took {} generations to win!'.format(generation))


# Pass true to play the game with the keyboard arrows.
ga(False)

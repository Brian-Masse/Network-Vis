import pygame
import pandas as pd
import random

pygame.init()


screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode(( screen_width, screen_height), pygame.RESIZABLE)

running = True
clock = pygame.time.Clock()



xls = pd.ExcelFile(
    "./indpendent-work2/data/result.xlsx"
)
data = pd.read_excel( xls, "result")

class node:
    def __init__(self, id):
        self.id = id
        self.followers = []
        self.following = []
        
        self.x =  random.randint( 0, screen_width )
        self.y = random.randint( 0, screen_height )

        self.is_rendered = False
        self.is_random = False

    def add_following(self, person):
        self.following.append( person )

    def follower_names(self):
        rows=   data["name"]==self.id
        columns="username"
        return data.loc[ rows, columns ]    

    def render(self, callers, bypass):

        if not self.is_rendered:
            un_rendered_heads = self.check_render_status()

            if len(un_rendered_heads) == 0 or bypass:
                self.find_pos()
                # self.draw()

                self.is_rendered = True
                for follower in self.followers:
                    if follower not in callers:
                        follower.render(callers, False)

            else:
                all_heads_are_callers = True

                for head in un_rendered_heads:
                    if not head in callers:
                        all_heads_are_callers = False

                        temp = callers
                        temp.append(self)
                        head.render( temp, False )

                if all_heads_are_callers:
                    self.render(callers, True)
                else:
                    self.render(callers, False)
            
    def draw(self):
        if self.is_random:
            # pass
            self.draw_point(( 255, 0, 255 ))
            self.draw_line(( 255, 0, 255 ))
        else:
            self.draw_point(( 255, 0, 0 ))
            self.draw_line(( 255, 0, 0 ))
        
    def draw_point(self, color):
        pygame.draw.circle(screen, color, ( self.x, self.y ), 1)


    def draw_line(self, color):
        for followee in self.followers:
            if not followee.is_random:
                pygame.draw.line( screen, color, ( self.x, self.y ), ( followee.x, followee.y ) )

    # makes sure that all heads are rendered, and if not, handles it
    def check_render_status(self):
        returning = []
        for head in self.following:
            if not head.is_rendered and not self.id == "brian_masse":
                returning.append( head )
        return returning

    def find_pos(self):
        results = self.find_percent_similarity()
        x = 0
        y = 0
        perc_sum = 0

        for head_result in results:
            x += ( head_result[0] * head_result[1] ) 
            y += ( head_result[0] * head_result[2] ) 
            perc_sum += head_result[0]

        if perc_sum > 0.1:
            self.x = x / ( perc_sum )
            self.y = y / ( perc_sum  )
        else:
            self.is_random = True

            x = random.randint( 10, screen_width - 10 )
            y = random.randint( 10, screen_height - 10 )
            
            while (x > screen_width / 5 and x < screen_width - (screen_width / 5)) and (y > screen_height / 5 and y < screen_height - (screen_height / 5)):
               x = random.randint( 10, screen_width - 10 ) 
               y = random.randint( 10, screen_height - 10 )  
               
            self.x=x
            self.y=y
            
        
    
    def find_percent_similarity(self):
        returning = []

        for head in self.following:
            matched = 0
            copy_followers = head.following 

            for head2 in self.following:
                if head2 in copy_followers:
                    matched += 1
    
            percent = (matched / max( len(self.following), len(head.following))) * 100 
            x       = head.x
            y       = head.y
            returning.append( (percent, x, y) )
        
        return returning


    
people = {
}

def create_person(name):
    if not name in people:
        new_node = node(name) #me 
        
        people[ name ] = new_node

        # create all followers, and assign them to follow me
        for follower in new_node.follower_names():
            create_person(follower)
            people[ name ].followers.append( people[follower] )
            people[follower].following.append( new_node )

people["brian_masse"] = node("brian_masse")

for name in data["name"]:
    create_person(name)
    people["brian_masse"].followers.append( people[name] )
    
people["brian_masse"].render([people["brian_masse"]], False)

for person in people:
    people[person].draw()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # screen.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()


from operator import mul
from turtle import distance
from numpy import diagonal, matrix
import pygame
import pandas as pd
import random
import numpy as np
import math


pygame.init()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode(( screen_width, screen_height), pygame.RESIZABLE)

running = True
clock = pygame.time.Clock()


xls = pd.ExcelFile(
    "independent_work/Network-Vis/data/followersList.xlsx"
)
data = pd.read_excel( xls, "result (1)")

# matrix_data = pd.ExcelFile(
#     "independent_work/Network-Vis/data/matrix.xlsx"
# )
# matrix = pd.read_excel(matrix_data, "matrix")

class node:
    def __init__(self, name):
        self.name = name
        self.followers = []
        self.following = []

        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

        self.similarity_to_center = 0

    def follower_names(self):
        rows=   data["name"]==self.name
        columns="username"
        return data.loc[ rows, columns ][:20]

    # def render(self):
    #     self.x = float(x_matrix[self.row])
    #     self.y = float(y_matrix[self.row])
    #     pygame.draw.circle( screen, (255, 0, 0), (self.x, self.y), 2 )

    def percent_similarity(self, other):
        matched = 0

        for head in self.following:
            if head in other.following:
                matched += 1

        percent = (matched / max( len(self.following), len(other.following), 1)) * 100     
        return percent

def create_person(name):
    if not name in people:
        new_node = node(name) #me 
        people[ name ] = new_node

        # create all followers, and assign them to follow me
        for follower in new_node.follower_names():
            create_person(follower)
            people[ name ].followers.append( people[follower] )
            people[follower].following.append( new_node )

# create all the people, so they know their followers, and who follows them
people = {}

def create_people():
    create_person("brian_masse")
    for name in data["name"]:
        create_person(name)
        people["brian_masse"].followers.append( people[name] )

create_people()


def create_matrix():
    distance_matrix = []
    names = []
    for person in people:
        row = []
        names.append(people[person].name)
        for person2 in people:
            percent = people[person].percent_similarity( people[person2] )
            row.append(100 - percent)
        distance_matrix.append( row )
    return distance_matrix, names

matrix, names = create_matrix()
# df = pd.DataFrame(matrix, names, names)
# df.to_csv("/Users/brianmasse/Desktop/matrix.csv")
screen.fill( (30, 30, 30) )

def render_people(index, size, pos, main, main_c, c, matrix):
    positions = matrix[index]

    for i in range(0, len(positions)):
        if main:
            print(i)
        
        theta = random.uniform( 0, 2 * math.pi )
        x = math.cos(theta) * ((1 - positions[i]) * size) / 100
        y = math.sin(theta) * ((1 - positions[i]) * size) / 100

        x += pos[0]
        y = screen_height - (y + pos[1])


        pygame.draw.circle(screen, c, (x, y), 2)
        if main:
            render_people( i, 100, ( x, y ), False, c, ( 115, 119, 244 ), matrix )

    pygame.draw.circle(screen, main_c, (pos[0], screen_height - pos[1]), 4)


center = ( screen_width / 2, screen_height / 2 )

print("launch")
render_people( 0, 100, center, False, (255, 0, 0), (255, 255, 255), matrix )

# for person in people:
#     people[person].render()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    pygame.display.flip()

pygame.quit()

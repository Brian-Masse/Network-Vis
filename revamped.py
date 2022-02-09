from operator import mul
from turtle import distance
from numpy import diagonal, matrix
import pygame
import pandas as pd
import random
import numpy as np


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

matrix_data = pd.ExcelFile(
    "independent_work/Network-Vis/data/matrixSmall.xlsx"
)
matrix = pd.read_excel(matrix_data, "matrix")

class node:
    def __init__(self, name):
        self.name = name
        self.followers = []
        self.following = []

        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

        self.row = node.get_row(name)
    
    def get_row(name):
        row = matrix["name"]==name
        row_number = matrix.index[ row ].tolist()
        if len(row_number) > 0:
            return row_number[0]
        return 0

    def follower_names(self):
        rows=   data["name"]==self.name
        columns="username"
        return data.loc[ rows, columns ][:20]   

    def render(self):
        self.x = float(x_matrix[self.row])
        self.y = float(y_matrix[self.row])
        pygame.draw.circle( screen, (255, 0, 0), (self.x, self.y), 2 )

    def percent_similarity(self, other):
        matched = 0

        for head in self.following:
            if head in other.following:
                matched += 1

        percent = (matched / max( len(self.following), len(other.following), 1)) * 100     
        return percent

    def recalculate_pos(self):
        x = 0
        y = 0

        row = matrix["name"]==self.name
        
        row_number = matrix.index[ row ].tolist()
        if len(row_number) > 0:

            for person in people:
                if people[person].name != self.name:
                    percent = matrix.iat[row_number[0], 1]
                    x += (percent / 100) * people[person].x
                    y += (percent / 100) * people[person].y
            
            x /= len(people) - 2
            y /= len(people) - 2

            if abs(self.x - x)  < 1 and abs(self.y - y):
                rendered.append(self)
            else:
                if self in rendered:
                    rendered.remove( self )


def create_person(name):
    if not name in people:
        new_node = node(name) #me 
        people[ name ] = new_node

        xs.append( [new_node.y] )
        ys.append( [new_node.y] )

        # create all followers, and assign them to follow me
        for follower in new_node.follower_names():
            create_person(follower)
            people[ name ].followers.append( people[follower] )
            people[follower].following.append( new_node )

def interpret_matrix():
    stripped_matrix = matrix.drop(
        labels = ["name"],
        axis = 1,
        inplace = False
    )
    
    distance_matrix = stripped_matrix.to_numpy()
    distance_matrix = np.clip(distance_matrix, 0.1, 100)
    distance_matrix = np.nan_to_num( distance_matrix )
    return np.divide( distance_matrix, 100 )

def calculate_divisors(matrix):
    ones = np.full(( len(matrix), 1), 1, dtype=int)
    sums = np.matmul( matrix, ones )
    inverse = 1 / sums
    transpose = inverse.transpose()
    return transpose

# create all the people, so they know their followers, and who follows them

people = {}

# position is the 1 X n matrix of every person's position, they contian a row number to access theier pos for rendering
xs = []
ys = []
# This is all of their distances to each other, it must be normalized to [0, 1] first
distance_matrix = interpret_matrix()
rendered = []

def create_people():
    create_person("brian_masse")
    for name in data["name"]:
        create_person(name)
        people["brian_masse"].followers.append( people[name] )

create_people()
x_matrix = np.asarray( xs)
y_matrix = np.asarray( ys)

divisors = calculate_divisors(distance_matrix)

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

# matrix, names = create_matrix()
# df = pd.DataFrame(matrix, names, names)
# df.to_csv("/Users/brianmasse/Desktop/matrix.csv")

def recalculate_positions():
    # multiplied_x = np.matmul( distance_matrix, x_matrix )
    # multiplied_y = np.matmul( distance_matrix, y_matrix )

    multiplied_x = procedure( x_matrix )
    multiplied_y = procedure( y_matrix )

    return multiplied_x, multiplied_y

def procedure(matrix):
    sums = np.matmul( distance_matrix, matrix )
    total = np.matmul( sums, divisors)

    diagonal = np.asarray([ np.diagonal( total ) ])
    return np.transpose(diagonal)
    




distance_matrix = np.asarray( [[100, 20, 30],
                                [20, 100, 70],
                                [30, 70, 100]])
distance_matrix = np.divide(distance_matrix, 100)


divisors = calculate_divisors(distance_matrix)

x_matrix = np.asarray( [[2],
                        [4],
                        [1]] )


y_matrix = x_matrix            

iteration = 0

# print(divisors)
# x_matrix = procedure(x_matrix)
# print(x_matrix)
# print(procedure(x_matrix))

# while len( rendered ) < len(people) and iteration < 1000:
#     x_matrix, y_matrix = recalculate_positions()        
#     iteration += 1

#     # print(x_matrix[0][0])
#     # print( iteration )


def test(values):
    print(distance_matrix[0][0])
    value1 = (values[0] * distance_matrix[0][0]) + (values[1] * distance_matrix[0][1])  + (values[2] * distance_matrix[0][2] )
    value2 = (values[0] * distance_matrix[1][0]) + (values[1] * distance_matrix[1][1])  + (values[2] * distance_matrix[1][2] )
    value3 = (values[0] * distance_matrix[2][0]) + (values[1] * distance_matrix[2][1])  + (values[2] * distance_matrix[2][2] )

    value1 /= (distance_matrix[0][0] + distance_matrix[0][1] + distance_matrix[0][2])
    value2 /= (distance_matrix[1][0] + distance_matrix[1][1] + distance_matrix[1][2])
    value3 /= (distance_matrix[2][0] + distance_matrix[2][1] + distance_matrix[2][2])

    return value1, value2, value3

values = test( (20, 400, 890) )
print(values)
for i in range(0, 10):
    values = test(values)
    print(values)


# print(x_matrix)

# for person in people:
#     people[person].render()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    pygame.display.flip()

pygame.quit()

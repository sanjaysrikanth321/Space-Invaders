import turtle
import os
import math
import random
import re

# To make the code and the game my own i need to add a level system and make the bullet balance off of the walls atleast 3 times
player = "player.gif"
invader = "invader.gif"
# bg = "space_invaders_background.gif"

# Render sceen
sc = turtle.Screen()
sc.bgcolor("black")


# score
score = 0
score_creater = turtle.Turtle()
score_creater.speed(0)
score_creater.color("white")
score_creater.penup()
score_creater.setposition(-180, 180)
scoreDisplay = "Score: %s" % score
score_creater.write(scoreDisplay, align="left")
score_creater.hideturtle()

# player code
sc.addshape(player)
pc = turtle.Turtle()
pc.shape(player)
pc.setheading(90)
pc.setposition(0,-175)
pc.speed(0)
playerspeed=15

# move player left or right
def left():
    x = pc.xcor()
    x -= playerspeed
    if x < -175:
        x = -175
    pc.setx(x)

def right():
    x = pc.xcor()
    x += playerspeed
    if x > 175:
        x = 175
    pc.setx(x)
    
# sc.onkey(left, "Left")
# sc.onkey(right, "Right")
# sc.listen()

# # bullet = turtle.Turtle()
# # bullet.color('yellow')
# # bullet.setheading(90)
# # bullet.penup()
# # bullet.speed
# # bullet.hideturtle()
# # bulletspeed = 20

# # bullet = turtle.Turtle()
# # bullet.color("yellow")
# # bullet.shape("triangle")
# # bullet.penup()
# # bullet.speed(0)
# # bullet.setheading(90)
# # bullet.hideturtle()

# # bulletspeed = 20


class Enemy(turtle.Turtle):
  # (self, name, x, y)
  def __init__(self, name, x, y):
    self.name
    turtle.Turtle.__init__(self)
    self.penup()
    sc.addshape(invader)
    self.shape(invader)
    self.speed(0)
    self.setheading(90)
    self.setposition(x, y)
    




# row1 = Enemy()
# row1.setposition(-125, 150)

# row2 = Enemy()
# row2.setposition(-100, 150)

# row3 = Enemy()
# row3.setposition(-75, 150)

# row4 = Enemy()
# row4.setposition(-50, 150)

# row5 = Enemy()
# row5.setposition(-25,150)

# row6 = Enemy()
# row6.setposition(0, 150)

# row7 = Enemy()
# row7.setposition(25, 150)

# row8 = Enemy()
# row8.setposition(50, 150)

# row9 = Enemy()
# row9.setposition(75, 150)

# row01 = Enemy()
# row01.setposition(100,150)



# # row 2
# row21 = Enemy()
# row21.setposition(-125, 125)

# row22 = Enemy()
# row22.setposition(-100, 125)

# row23 = Enemy()
# row23.setposition(-75, 125)

# row24 = Enemy()
# row24.setposition(-50, 125)

# row25 = Enemy()
# row25.setposition(-25,125)

# row26 = Enemy()
# row26.setposition(0, 125)

# row27 = Enemy()
# row27.setposition(25, 125)

# row28 = Enemy()
# row28.setposition(50, 125)

# row29 = Enemy()
# row29.setposition(75, 125)

# row02 = Enemy()
# row02.setposition(100,125)


# # row 3
# row31 = Enemy()
# row31.setposition(-125, 100)

# row32 = Enemy()
# row32.setposition(-100, 100)

# row33 = Enemy()
# row33.setposition(-75, 100)

# row34 = Enemy()
# row34.setposition(-50, 100)

# row35 = Enemy()
# row35.setposition(-25,100)

# row36 = Enemy()
# row36.setposition(0, 100)

# row37 = Enemy()
# row37.setposition(25, 100)

# row38 = Enemy()
# row38.setposition(50, 100)

# row39 = Enemy()
# row39.setposition(75, 100)

# row03 = Enemy()
# row03.setposition(100,100)


# # row 4 
# row41 = Enemy()
# row41.setposition(-125, 75)

# row42 = Enemy()
# row42.setposition(-100, 75)

# row43 = Enemy()
# row43.setposition(-75, 75)

# row44 = Enemy()
# row44.setposition(-50, 75)

# row45 = Enemy()
# row45.setposition(-25,75)

# row46 = Enemy()
# row46.setposition(0, 75)

# row47 = Enemy()
# row47.setposition(25, 75)

# row48 = Enemy()
# row48.setposition(50, 75)

# row49 = Enemy()
# row49.setposition(75, 75)

# row04 = Enemy()
# row04.setposition(100,75)

# throws all into arrays by rows
first_row = ['row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row01']
second_row = ['row21', 'row22', 'row23', 'row24', 'row25', 'row26', 'row27', 'row28', 'row29', 'row02']
third_row = ['row31', 'row32', 'row33', 'row34', 'row35', 'row36', 'row37', 'row38', 'row39', 'row03']
fourth_row =['row41', 'row42', 'row43', 'row44', 'row45', 'row46', 'row47', 'row48', 'row49', 'row04']

# allows me to refer to each variable when calling a dictionary by name
arrayDict1 = [Enemy(name=name, x=0, y=150) for name in first_row]
arrayDict2 = [Enemy(name=name, x=0, y=125) for name in second_row]
arrayDict3 = [Enemy(name=name, x=0, y=100) for name in third_row]
arrayDict4 = [Enemy(name=name, x=0, y=75) for name in fourth_row]
rowList = [arrayDict1, arrayDict2, arrayDict3, arrayDict4]


# supposed to allow me to loop through the entire collection and assign positions accordingly. 
# needs work

for position in range(4):
  
  x=-125
  
  for index in rowList[position]:
    number =+ 1
    y=150 - (position * 25)
    index.setposition(x, y)
    
  # return x+=25
    


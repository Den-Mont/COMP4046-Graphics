import graphics as gp

win = gp.GraphWin("Ejemplo sistema gráfico", width = 500, height=500, autoflush=False)

p1 = gp.Point(100,100)
circle1 = gp.Circle(p1, 40)

circle1.setFill("red")
circle1.draw(win)

for i in range(20):
    circle1.move(i,i)
    gp.update(30)

button = gp.Text(gp.Point(250, 490), "Click to quit" )

# wait for click or enter to quit
#input("Presione <Enter> para salir")
button.draw(win)
win.getMouse()

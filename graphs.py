import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

plt.style.use('ggplot')
emot = []
mag = []
month = []
day = []
year = []

with open('C:/Users/Bert/workspace/HackCWRU/RESTful API/flask_minimal/api/tab.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            month.append(row[0])
            day.append(row[1])
            year.append(row[2])
            emot.append(row[3])
            mag.append(row[4])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

counter = 0
initY = [int(emot[0]) * int(mag[0])]
initX = ["%s/%s/%s" % (month[0],day[0],year[0])]

def animate(i):
    global initX, counter
    x=initX
    y=initY
    counter+=1
    x.append("%s/%s/%s" % (month[counter],day[counter],year[counter]))
    y.append(int(emot[counter]) * int(mag[counter]))
    ax.clear()
    plt.plot(x,y,color="blue")
def main():
    fig.suptitle('Mood Tracker', fontsize=20)
    ani = animation.FuncAnimation(fig, animate, interval=600)
    plt.show()
    ani.save('Track.gif',dpi=60,writer='imagemagick')

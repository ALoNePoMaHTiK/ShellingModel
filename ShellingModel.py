from random import randint
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2
import os
import time

class ShellingModel:
    def __init__(self,size):
        self.imgs = []
        self.size = size
        self.turn = 0
        self.model = [[''] * self.size for i in range(self.size)] # Создание матрицы

    # Заполнение модели
    def fillModel(self):
        redCount = int(self.size ** 2 * 0.4)    #Кол-во красных
        blueCount = int(self.size ** 2 * 0.4)   #Кол-во синих
        while redCount > 0:
            x, y = self.getRandCellCoord()
            self.model[x][y] = 'R'
            redCount -= 1
        while blueCount > 0:
            x, y = self.getRandCellCoord()
            if self.model[x][y] == '':
                self.model[x][y] = 'B'
                blueCount -= 1

    # Координаты случайной точки
    def getRandCellCoord(self):
        return (randint(0, self.size - 1), randint(0, self.size - 1))

    # Определение счатливости клетки
    def isHappy(self, x, y, count_for_happy = 3):
        color = self.model[x][y]
        count = 0
        neighbors_offsets = [(-1, 0), (-1, -1), (-1, 1),
                             (1, -1), (1, 0), (1, 1),
                             (0, 1), (0, -1)]
        for i in neighbors_offsets:
            if (x + i[0]) >= 0 and (x + i[0]) < self.size and (y + i[1]) >= 0 and (y + i[1]) < self.size:
                count += (self.model[x + i[0]][y + i[1]] == color)
        return count >= count_for_happy  # Количество соседей для счастья

    # Получение всех несчастливых и свободных
    def getAllUnhappyAndFree(self):
        unhappy = []
        free = []
        for i in range(self.size):
            for j in range(self.size):
                if not self.isHappy(i, j) and self.model[i][j] != '':
                    unhappy.append((i, j))
                elif self.model[i][j] == '':
                    free.append((i, j))
        return unhappy,free

    # Отрисовка и сохранение модели
    def draw(self,name):
        fig, ax = plt.subplots()
        ax.plot()
        ax.set_axis_off()
        for i in range(self.size):
            for j in range(self.size):
                color = ''
                if self.model[i][j] == 'R':
                    color = 'red'
                elif self.model[i][j] == 'B':
                    color = 'blue'
                else:
                    color = 'white'
                ax.add_patch(Rectangle((1 + i * 2, 1 + j * 2), 2, 2, edgecolor='black', lw=1, facecolor=color))
        file_name = f'images/{name}_model.png'
        self.imgs.append(file_name)
        plt.savefig(file_name, dpi=300)
        ax.clear()
        plt.close()

    # Перемещение случайного несчастливого на случайную свободную позицию
    def moveRandUnhappy(self):
        unhappy,free = self.getAllUnhappyAndFree()
        if len(unhappy) == 0:
            self.draw(f'{self.size}_{self.turn}')
            return False
        old_x, old_y = unhappy[randint(0, len(unhappy) - 1)]
        new_x, new_y = free[randint(0, len(free) - 1)]
        self.model[new_x][new_y] = self.model[old_x][old_y]
        self.model[old_x][old_y] = ''
        self.turn +=1
        return True

    def getResultImg(self):
        imgs = []
        for i in self.imgs:
            imgs.append(cv2.imread(i))
        rows = []
        for i in range(0, len(imgs), len(imgs)//4):
            rows.append(cv2.hconcat(imgs[i:i + len(imgs)//4]))
        cv2.imwrite(f'images/{self.size}_{self.turn}_result.png', cv2.vconcat(rows))

def out(message,level = 1):
    print('\t'*(level-1)+time.strftime('[%X] ', time.localtime())+str(message))

#Очищение папки и изображениями
def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

delete_files_in_directory('./images')
model = ShellingModel(size=100)
model.fillModel()
model.draw('begin')

while model.moveRandUnhappy():
    if model.turn % 500 == 0:
        out(model.turn)
        model.draw(model.turn)
model.getResultImg()
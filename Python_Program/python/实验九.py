from random import randrange
def init():
    result={i:'goat'for i in range(3)}
    r=randrange(3)
    result[r]='car'
    return result

def startGame():
    doors= init()
    while Ture:
        try:
            firstDoorNum=int(input('Choose a door to open:'))
            break
        except:
            print('tiehanhan')

            for door in doors.keys()-{firstDoorNum}:
                if(doors[door])=='goat':
                    print('"goat"behind the door',door)
                    thirDoor=(doors.keys()-{door,firstDoorNum}).pop()
                    change=input('Swith to {}?(y/n)'.format(thirDoor))
                    finalDoorNum=thirDoor if change=='y'else firstDoorNum
                    if door[finalDoorNum]=='goat':
                        return 'SB'
                    else:
                        return 'ershazi'

                    while Ture:
                        print('='*30)
                        print((startGame()))
                        break;
"""
File: penaltygame.py
-------------------
Mouse kontrolü ile rastgele hareket eden kaleciye penaltı atma üzerine kurgulanmış bir oyun.
-------------------
Creators: Arjen GÖKDEMİR, Azad AVŞAR, Efe KURNAZ, Eray ÇİRKİN
"""
from graphics import Canvas
import time
import random
import operator

# Canvasın genişlik ve yükseklik ayarlarını ekliyoruz.
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 750

# İntro fonksiyonu kullanıcıya bir giriş ekranı ve iki aşamalı bir seçim imkanı sunar.
def intro(canvas):
    """

    Parameters
    ----------
    canvas

    Returns
    -------
    shots : int
    team : str

    """
    canvas.create_image(0, 0, "bgintro.png")
    canvas.create_image(300,250, "leveltext.png")
    canvas.create_image(300,400, "level1.png")
    canvas.create_image(450,400, "level2.png")
    canvas.create_image(600,400, "level3.png")
    selector = 0
    shots = 0
    team = ''
    while selector<1:
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            if 300 < click.x < 400 and 400 < click.y < 500:
                shots = 5
                selector += 1
                canvas.delete_all()
            if 450 < click.x < 550 and 400 < click.y < 500:
                shots = 10
                selector += 1
                canvas.delete_all()
            if 600 < click.x < 700 and 400 < click.y < 500:
                shots = 15
                selector += 1
                canvas.delete_all()
        canvas.update()
    canvas.create_image(0, 0, "bgintro.png")
    canvas.create_image(300,250, "teamtext.png")
    canvas.create_image(300,400, "fb.png")
    canvas.create_image(450,400, "gs.png")
    canvas.create_image(600,400, "bjk.png")
    while selector<2:
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            if 300 < click.x < 400 and 400 < click.y < 500:
                team = 'navy blue'
                selector += 1
                canvas.delete_all()
            if 450 < click.x < 550 and 400 < click.y < 500:
                team = 'red'
                selector += 1
                canvas.delete_all()
            if 600 < click.x < 700 and 400 < click.y < 500:
                team = 'black'
                selector += 1
                canvas.delete_all()
        canvas.update()
    return shots, team

# Tıklanılan bölgenin kalenin içerisinde olması halinde toplu tıklanılan kordinata yönlendirir.
def takeashot(canvas, ball):
    """

    Parameters
    ----------
    canvas
    ball : Canvas object

    Returns
    -------
    ball : Canvas object

    """
    clicks = canvas.get_new_mouse_clicks()
    for click in clicks:
        if 207 < click.x < 791 and 43 < click.y < 312:
            canvas.move_to(ball, click.x-23, click.y-23)
    canvas.update()
    return ball

# Elde edilen rastgele değere göre kalecinin hareketini sağlar.
def randomgoalkeeper(canvas, goalkeeper):
    """

    Parameters
    ----------
    canvas
    goalkeeper : Canvas object

    Returns
    -------
    goalkeeper : Canvas object

    """
    x_index = random.randint(-300, 300)
    if 207-50 < x_index + canvas.get_left_x(goalkeeper) < 791-50:
        canvas.move(goalkeeper, x_index, 0)
        time.sleep(0.5)
        canvas.update()
    return goalkeeper

# Kalecinin ve topun üst üste gelme durumunu denetler ve uygun koşullarda skora etki eder.
def control(canvas, ball, goalkeeper, score):
    """

    Parameters
    ----------
    canvas
    ball : Canvas object
    goalkeeper : Canvas object
    score : Canvas object

    Returns
    -------
    ball : Canvas object
    goalkeeper : Canvas object
    score : int

    """
    gx1 = canvas.get_left_x(goalkeeper)
    gx2 = canvas.get_left_x(goalkeeper) + 100
    gy1 = canvas.get_top_y(goalkeeper)
    gy2 = canvas.get_top_y(goalkeeper) + 286
    bx1 = canvas.get_left_x(ball)
    bx2 = canvas.get_left_x(ball) + 47
    by1 = canvas.get_top_y(ball)
    by2 = canvas.get_top_y(ball) + 47
    if (gx1 < bx1 < gx2 or gx1 < bx2 < gx2) and (gy1 < by1 < gy2 or gy1 < by2 < gy2):
        canvas.delete(ball)
        ball = canvas.create_image(479, 654, "ball.png")
        time.sleep(0.5)
        canvas.update()
    elif canvas.get_left_x(ball) != 479 and canvas.get_top_y(ball) != 654:
        canvas.delete(ball)
        score -= 1
        ball = canvas.create_image(479, 654, "ball.png")
        time.sleep(0.5)
        goal = canvas.create_image(300, 300, "goaltext.png")
        canvas.update()
        time.sleep(1)
        canvas.delete(goal)
        canvas.update()
    return ball, goalkeeper, score

# Elde edilen end ve start değerleri ile kullanıcının skorunu hesaplar ve kullanıcı için iki adet aksiyon sunar.
def outro(canvas, start, end):
    """

    Parameters
    ----------
    canvas
    start : float
    end : float

    Returns
    -------
    None.

    """
    canvas.delete_all()
    canvas.create_image(0, 0, "bgoutro.png")
    canvas.create_image(75, 250, "scorarea.png")
    outro_text = canvas.create_text(500, 330, end-start)
    canvas.set_color(outro_text, "white")
    canvas.set_font(outro_text, "Arial", 35)
    canvas.create_image(75, 500, "viewscore.png")
    canvas.create_image(525, 500, "addscore.png")
    selector = 0
    while selector<1:
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            if 75 < click.x < 475 and 500 < click.y < 580:
                selector += 1
                canvas.delete_all()
                viewlist(canvas)
            if 525 < click.x < 925 and 500 < click.y < 580:
                selector += 1
                canvas.delete_all()
                addscore(canvas, start, end)
                time.sleep(2)
                canvas.delete_all()
                viewlist(canvas)
        canvas.update()

# Listeye yazılmış skorları sırasıyla ekrana yazdırır.
def viewlist(canvas):
    """

    Parameters
    ----------
    canvas

    Returns
    -------
    None.

    """
    canvas.create_image(0, 0, "bgoutro.png")
    scores = {}
    with open("scoretable.txt") as f:
        for lines in f:
            line = lines.strip().split(",")
            scores[line[0]] = float(line[1])
    # Kütüphane içine yazılan skor ve isim çiftlerini küçükten büyüğe sıralayarak listeye ekler.
    sortedscores = sorted(scores.items(), key=operator.itemgetter(1))
    for count, i in enumerate(sortedscores):
        text = i[0] + " -> " + str(i[1])
        y = 200 + 35*count 
        text = canvas.create_text(500, y, text)
        canvas.set_color(text, "white")
        canvas.set_font(text, "Arial", 20)
        time.sleep(0.5)
        canvas.update()

# Verilen skoru listeye ekler.
def addscore(canvas, start, end):
    """

    Parameters
    ----------
    canvas
    start : float
    end : float

    Returns
    -------
    None.

    """
    canvas.create_image(0, 0, "bgoutro.png")
    canvas.create_image(300, 300, "addscoretext.png")
    canvas.update()
    name = str(input("Please Enter Your Name: "))
    score = str(end-start)
    with open("scoretable.txt", "a") as f:
        text = name +','+score+'\n'
        f.write(text)

def main():
    canvas = Canvas()
    # Verilen boyutlarda canvası oluşturur.
    canvas.set_canvas_size(CANVAS_WIDTH, CANVAS_HEIGHT)
    # Canvasın ismini oluşturur.
    canvas.set_canvas_title("Penalty")
    # Canvasın araka plan rengini atar.
    canvas.set_canvas_background_color("green")
    # Giriş fonksiyonunu çağırır.
    score, team = intro(canvas)
    # Seçilen takıma göre arkaplan görselini oluşturur.
    if team == 'navy blue':
        canvas.create_image(0, 0, "fbfield.png")
    elif team == 'red':
        canvas.create_image(0, 0, "gsfield.png")
    elif team == 'black':
        canvas.create_image(0, 0, "bjkfield.png")
    # Kaleciyi verilen kordinatlarda oluştuyor.
    goalkeeper = canvas.create_image(450, 45, "goalkeeper.png")
    # Topu verilen kordinatlarda oluşturuyor.
    ball = canvas.create_image(479, 654, "ball.png")
    # Oyunun başlangıcında süreyi başlatıyor.
    start = time.time()
    # Seçilen zorluk seviyesine göre skor 0 olana kadar kodu çalıştırıyor.
    while score != 0:
        # Toplu yönlendirmek için mouse tıklaması alır ve topu o noktaya yönlendirir.
        ball = takeashot(canvas, ball)
        # Rastgele değerlerle kaleciyi sağa veya sola hareket ettirir.
        goalkeeper = randomgoalkeeper(canvas, goalkeeper)
        # Kaleci ve topun üst üste gelme durumunu denetleyip sonucu skora yansıtır.
        ball, goalkeeper, score = control(canvas, ball, goalkeeper, score)
    # Oyunun birişinde süreyi durduruyor.
    end = time.time()
    # Çıkış fonksiyonunu çağırır.
    outro(canvas, start, end)
    canvas.mainloop()   
    
if __name__ == "__main__":
    main()
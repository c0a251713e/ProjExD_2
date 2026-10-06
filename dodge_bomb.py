import os
import pygame as pg
import random
import sys
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
         pg.K_DOWN:(0,5),
         pg.K_LEFT:(-5,0),
         pg.K_RIGHT:(5,0)
        }

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.Surface) -> None:
    """
    引数：screenのSurface
    戻り値：なし
    文字と画像を表示
    """
    black_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_img, (0, 0, 0), (0, 0, 10000, 10000), width=0)
    black_img.set_alpha(200)
    screen.blit(black_img, [0, 0])

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [500, 250])

    shock_img = pg.image.load("fig/8.png")
    screen.blit(shock_img, [0, 300])
    screen.blit(shock_img, [500, 300])
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：タプル(爆弾の大きさSurfaceリスト, 加速度intリスト)
    """    
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    
    return (bb_imgs, bb_accs)


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル（横方向判定結果,縦方向判定結果）
    画面内ならTrue,画面外ならFalese
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = (random.randint(0,WIDTH),random.randint(0,HEIGHT))
    vx, vy = 5, 5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs = init_bb_imgs()[0]
    bb_accs = init_bb_imgs()[1]
    avx = vx*bb_accs[min(tmr//500, 9)]
    avy = avx
    bb_img = bb_imgs[min(tmr//500, 9)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): # kkとbbのrectが重なっていたら
            print("game over")
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5

        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] # 縦方向移動
                sum_mv[1] += tpl[1] # 横方向移動
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # どこかしらはみ出ている
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # その動きをキャンセル
        screen.blit(kk_img, kk_rct)

        if tmr == 100:
            avx = bb_accs[9]
            avy = avx
        elif tmr == 90:
            avx = bb_accs[8]
            avy = avx
        elif tmr == 80:
            avx = bb_accs[7]
            avy = avx
        elif tmr == 70:
            avx = bb_accs[6]
            avy = avx
        elif tmr == 60:
            avx = bb_accs[5]
            avy = avx
        elif tmr == 50:
            avx = bb_accs[4]
            avy = avx
        elif tmr == 40:
            avx = bb_accs[3]
            avy = avx
        elif tmr == 30:
            avx = bb_accs[2]
            avy = avx
        elif tmr == 20:
            avx = bb_accs[1]
            avy = avx
        elif tmr == 10:
            avx = bb_accs[0]
            avy = avx

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            avx *= -1
        if not tate:
            avy *= -1
        screen.blit(bb_img, bb_rct)
            
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

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
    black_img = pg.Surface((WIDTH, HEIGHT))  # Surfaceの生成
    pg.draw.rect(black_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT), width=0)  # 黒画像の描画
    black_img.set_alpha(200)  # 透明度の調整
    screen.blit(black_img, [0, 0])  # 画面の更新

    fonto = pg.font.Font(None, 80)  # フォントの設定
    txt = fonto.render("Game Over", True, (255, 255, 255))  # 文字の決定
    screen.blit(txt, [400, 300])  # 画面の更新

    shock_img = pg.image.load("fig/8.png")  # 画像の読み込み
    screen.blit(shock_img, [300, 300])  # 1枚目の描画
    screen.blit(shock_img, [800, 300])  # 2枚目の描画
    pg.display.update()  #画面の更新
    time.sleep(5)  # 5秒待機


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：タプル(爆弾の大きさSurfaceリスト, 加速度intリスト)
    """    
    bb_imgs = []
    for r in range(1, 11):  # 大きさのSurfaceリスト作成
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]  # 加速度のintリスト
    
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
    bb_img.set_colorkey((0,0,0))

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

        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] # 縦方向移動
                sum_mv[1] += tpl[1] # 横方向移動
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True): # どこかしらはみ出ている
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # その動きをキャンセル
        screen.blit(kk_img, kk_rct)

        if tmr == 100:  # 時間経過による速度変更
            bb_img = bb_imgs[9]
            avx = bb_accs[9]
            avy = avx
        elif tmr == 90:
            bb_img = bb_imgs[8]
            avx = bb_accs[8]
            avy = avx
        elif tmr == 80:
            bb_img = bb_imgs[7]
            avx = bb_accs[7]
            avy = avx
        elif tmr == 70:
            bb_img = bb_imgs[6]
            avx = bb_accs[6]
            avy = avx
        elif tmr == 60:
            bb_img = bb_imgs[5]
            avx = bb_accs[5]
            avy = avx
        elif tmr == 50:
            bb_img = bb_imgs[4]
            avx = bb_accs[4]
            avy = avx
        elif tmr == 40:
            bb_img = bb_imgs[3]
            avx = bb_accs[3]
            avy = avx
        elif tmr == 30:
            bb_img = bb_imgs[2]
            avx = bb_accs[2]
            avy = avx
        elif tmr == 20:
            bb_img = bb_imgs[1]
            avx = bb_accs[1]
            avy = avx
        elif tmr == 10:
            bb_img = bb_imgs[0]
            avx = bb_accs[0]
            avy = avx
        bb_rct.width = bb_img.get_rect().width

        bb_rct.move_ip(avx, avy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)  # 壁にぶつかったら折り返す
        if not yoko:
            avx *= -1
        if not tate:
            avy *= -1
        screen.blit(bb_img, bb_rct)
        bb_img.set_colorkey((0,0,0))
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

from ursina import *
from player import Player
from spring import Spring
from map_bp import *
from fade import Fade
from ursina.shaders import lit_with_shadows_shader
from saveload import *
from menu import PauseMenu

app = Ursina(development_mode=True, title='Lucid Dreams')
window.borderless = False
window.icon = 'imp/assets/gr8logo.ico'
shader = lit_with_shadows_shader
Text.default_font='imp/assets/font.tff'
ambient = AmbientLight(color=Vec4(0.5, 0.55, 0.66, 0) * 1.3)
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, rotation=(45, -45, 45), shadows=True)



player = Player()
player.cursor.color = color.white66
player.y = 10

spring = Spring()
fade = Fade()

hand = Entity(
    model='hand.obj',
    texture='hand_texture.png',
    scale=.5,
    double_sided=True,
    parent=camera
)

pausemenu=PauseMenu(player,app)

player_pos_txt = Text(f"x:{int(player.x)},y:{int(player.y)},z:{int(player.z)}", position=window.top_left)


duration = 1
timer = 0

def complete_level():
    global timer
    timer += time.dt
    if timer >= duration:
        timer -= duration
        if player.y <= -10:
            player.y = 5
        if map.finished==True and check_level()==map.level:
            save_level(map.level+1)
            fade.fade_in()
            invoke(load_level,delay=1)

def load_level():
    global map
    current_level = check_level()
    if current_level == 1:

        map = Map1(player)

    elif current_level == 2:
        try:
            destroy(map)
        except:
            print('level_loaded!')

        map = Map2(player)
    # Add more level loading logic for additional levels

load_level()

def input(key):
    if key=='escape':
        a=pausemenu.toggle()



def update():
    global duration ,timer
    complete_level()
    player_pos_txt.text = f"x:{int(player.x)},y:{int(player.y)},z:{int(player.z)}"
    movement = spring.update(time.dt)
    spring.shove(Vec3(mouse.y, mouse.x, 0))
    hand.position = (movement.y * -1, movement.x * -1, movement.z * -1) + (0.65, -0.5, 0.9)

app.render.setShaderAuto()

app.run()

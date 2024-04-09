from ursina import *
from maze_generator import *
from saveload import *

class Map1(Entity):
    def __init__(self,player):
        super().__init__(

        )
        self.player=player
        self.level=1  
        scene.fog_density=0.4
        scene.fog_color=color.black
        self.sky= Sky(color=color.black)
        self.box=Entity(model='lv_1',texture='doodle1',scale=25,double_sided=True,texture_scale=(10,10),collider='mesh',parent=self)
        self.textures = ['doodle1','doodle2','doodle3','doodle4']
        self.current_texture_index = 0
        self.duration = 1
        self.timer = 0
        if check_level() == 1:
            self.finished=False
            print('false f map1')
        else:
            self.finished=True
            print('true f map1')



    def on_destroy(self):
        scene.fog_density=0
        destroy(self.sky)
        del self

    def update(self):
        if self.finished==False and int(self.player.z)>= 38:
            print('true f map2')
            self.finished=True
        self.timer += time.dt
        if self.timer >= self.duration:
            self.timer -= self.duration
            self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
            self.box.texture = self.textures[self.current_texture_index]

class Map2(Entity):
    def __init__(self, player):
        super().__init__()

        self.player = player
        self.level=2
        self.collider = 'mesh'
        self.maze = self.optimize_map_generation()
        if check_level() == 2:
            self.finished=False
            print('false f map2')
        else:
            self.finished=True
            print('true f map2')

    def optimize_map_generation(self):
        self.walls_parent = Entity(parent=self)  # Create a parent entity for all walls
        self.exit_door = None  # Variable to hold the exit door entity
        for i in range(len(MAP)):
            for j in range(len(MAP[0])):
                if MAP[i][j]:
                    if MAP[i][j] == 'p':
                        self.p_pos=Vec3(BLOCKSIZE * i, 3, BLOCKSIZE * j)
                        self.player.position = self.p_pos
                        continue
                    elif MAP[i][j] == 'e':  # If 'e' is encountered, create an exit door
                        
                        self.exit_door = Entity(
                            model='door.obj',
                            texture='door_texture',
                            collider='box',
                            scale=2,
                            position=BLOCKPOSITION * Vec3(i, .33, j),
                            parent=self.walls_parent,
                            rotation_y=-90
                        )
                    else:
                        self.wall = Entity(
                            model='cube',
                            texture='brick',
                            collider='box',
                            scale=BLOCKSCALE,
                            position=BLOCKPOSITION * Vec3(i, 1, j),
                            parent=self.walls_parent
                        )
        self.ground = Entity(model='plane',
                        double_sided=True,
                        position=((WIDTH // 2) - 2, 1, (HEIGHT // 2) - 2),
                        scale=(WIDTH, 1, HEIGHT),
                        texture='tiles',
                        collider='mesh',
                        parent=self)
        self.ground.texture_scale = (25, 25)
        self.ceiling = Entity(model='plane',
                        double_sided=True,
                        position=((WIDTH // 2) - 2, 5, (HEIGHT // 2) - 2),
                        scale=(WIDTH, 1, HEIGHT),
                        texture='brick',
                        collider='mesh',
                        color=color.rgb(155, 155, 200),
                        parent=self)
        self.ceiling.texture_scale = (25, 25)

    
    def update(self):
        if self.finished==False and self.player.position== self.exit_door.position:
            print('Finished!!!!')
            self.finished=True

class Map3(Entity):
    def __init__(self, player):
        super().__init__()
        self.player=player
        if check_level() == 3:
            self.finished=False
            print('false f map1')
        else:
            self.finished=True
            print('true f map2')
                
    
 

if __name__ == "__main__":
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina(borderless=True)
    camer = EditorCamera()
    Map2(camer)
    player_pos_txt = Text(f"x:{int(camer.x)},y:{int(camer.y)},z:{int(camer.z)}", position=window.top_left)
    def update():
        player_pos_txt.text=f"x:{int(camer.x)},y:{int(camer.y)},z:{int(camer.z)}"
        if camer.y<=-10:
            camer.y=5
        
            
    app.run()
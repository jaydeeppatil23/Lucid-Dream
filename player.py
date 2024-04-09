# (This is a litreal shit. This does not work properly. Remake is necessary.)
from ursina import *
from ursina.prefabs.health_bar import HealthBar
from particles import Particles


class Player(Entity):
    def __init__(self, **kwargs):
       
        self.speedbar = HealthBar(100, bar_color=color.hex("#50acff"), roundness=0,
                                  position=window.bottom_left + (0.12, 0.05), scale_y=0.01, scale_x=0.2)
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)

        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        
        self.speedbar.text_entity.disable()
        self.speedbar.animation_duration = 0

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0


        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]
        self.on_destroy = self.on_disable



        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y


    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        khopdi_ray = raycast(self.position + Vec3(0, self.height - 0.1, 0), self.up,traverse_target=self.traverse_target, distance=.5,ignore=self.ignore_list, debug=False)
        if held_keys["left shift"] and held_keys["w"]:
            bitch_ray = raycast(self.world_position+(0,self.height,0), self.down,traverse_target=self.traverse_target,ignore=self.ignore_list)
            if self.speedbar.value > 0 and not feet_ray.hit and not head_ray.hit:
                self.speedbar.value = self.speedbar.value-0.3
                self.speed = 10
                if bitch_ray.hit and bitch_ray.entity:
                    surface_texture = bitch_ray.entity.texture
                    surface_texture.texture_scale=(-1,-1)
                    running_particles = Particles(self.position,texture=surface_texture, direction=Vec3(
                    random.random(), random.randrange(-10, 10, 1) / 10, random.random()), spray_amount=5, scale=0.05)
                    
                if camera.fov <= 90 + 20:
                    camera.fov = camera.fov + 1
                

            else:
                if camera.fov >= 90:
                    camera.fov -= 1
                self.speed = 5
        else:
            if camera.fov >= 90:
                    camera.fov -= 1
            if self.speedbar.value < 100:
                self.speedbar.value = self.speedbar.value+0.1
            self.speed = 5

        if held_keys["left mouse"]:
            if self.cursor.scale > 0.01:
                self.cursor.scale -= (0.001, 0.001, 0.001)
                self.cursor.rotation -= (0, 0, 45)

        if not held_keys["left mouse"]:
            if self.cursor.scale < 0.015:
                self.cursor.scale += (0.001, 0.001, 0.001)
                self.cursor.rotation += (0, 0, 45)
        
        if khopdi_ray.hit:
            self.start_fall()
            self.y-=.1

        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=self.ignore_list)

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity



    def input(self, key):
        if key == 'space':
            self.jump()


    def jump(self):
        if not self.grounded:
            return

        # Check head collision before jumping
        khopdi_ray = raycast(self.position + Vec3(0, self.height - 0.1, 0), self.up, distance=.5,ignore=self.ignore_list, debug=True)
        if khopdi_ray.hit:
            return

        self.grounded = False
        self.animate_y(self.y + self.jump_height, self.jump_up_duration, resolution=int(1 // time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)
        self.jumping = True

    def on_enable(self):
        self.speedbar.enabled=True
        mouse.locked = True
        self.cursor.enabled = True


    def on_disable(self):
        self.speedbar.enabled=False
        mouse.locked = False
        self.cursor.enabled = False

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True




if __name__ == "__main__":
    app=Ursina()
    ground = Entity(scale=(100, 1, 100), collider='mesh', model='plane',
                texture="grass", double_sided=True)
    ground2 = Entity(scale=(100,1, 100), collider='mesh', model='cube',
                texture="white_cube", double_sided=True,y=4)
    player = Player()
    app.run()
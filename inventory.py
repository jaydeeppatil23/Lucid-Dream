from ursina import *

class Inventory(Entity):
    def __init__(self, **kwargs):
         super().__init__(**kwargs)
         self.selected=1

         self.select_slot(1)
         self.slotone=Entity(parent = camera.ui,
              model = Quad(radius=.015),
              texture = 'white_cube',
           texture_scale = (1, 1),
           scale = (1*.05, 1*.05
                    ),
           origin = (0,0),
           position = (-.1,-.45),
           color = color.clear)
         self.slottwo=Entity(parent = camera.ui,
           model = Quad(radius=.015),
           texture = 'white_cube',
           texture_scale = (1, 1),
           scale = (1*.05, 1*.05),
           origin = (0,0),
           position = (0,-.45),
           color = color.clear)
         self.slotthree=Entity(parent = camera.ui,
           model = Quad(radius=.015),
           texture = 'white_cube', 
           texture_scale = (1, 1),
           scale = (1*.05, 1*.05),
           origin = (0,0),
           position = (.1,-.45),
           color = color.clear)
    def select_slot(self,number):
        if self.selected<1 or self.selected>3:
            return
        self.selected=number
    
    def selected_slot(self):
        if self.selected<1 or self.selected>3:
            return
        elif self.selected==1:
            return self.slotone
        elif self.selected==2:
            return self.slottwo
        elif self.selected==3:
            return self.slotthree
        
    def fade_in(self):
        self.selected_slot().animate_color(color.black33, duration=.5, curve=curve.linear)
        invoke(self.fade_out, delay=2)  # Schedule the fade_out() method after the duration

    def fade_out(self):
        self.selected_slot().animate_color(color.clear, duration=1, curve=curve.linear)
        self.select_slot()
    def update(self):
             
        
if __name__ == '__main__':
    app = Ursina()
    Inventory()
    app.run()
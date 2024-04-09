from ursina import *
from direct.filter.CommonFilters import CommonFilters
from ursina.prefabs.button_list import ButtonList


class PauseMenu(Entity):
    def __init__(self, player, app, **kwargs):
        self.filter = CommonFilters(app.win, app.cam)
        self.filter.setBlurSharpen(1)
        self.quitbutton = Button(text="Exit the Game", scale=(
            0.5, 0.05), highlight_color=color.rgba(200, 0, 0, 150), position=(0, -0.2, 0))
        self.resumebutton = Button(text="Back to the Game", scale=(
            0.5, 0.05), highlight_color=color.white10, position=(0, 0.1, 0))
        self.buttonlist = [self.resumebutton, self.quitbutton]
        
        
        super().__init__(parent=camera.ui, ignore_paused=True, enabled=False, **kwargs)
        self.ignore_paused = True
        self.player = player
        
        for button in self.buttonlist:
            button.parent = self
            button.color = color.black33
            button.ignore_paused = True
            button.z=-10
        
        self.resumebutton.on_click = self.resumeButtonFunc
        self.quitbutton.on_click = self.quitButtonFunc

    def quitButtonFunc(self):
        if self.quitbutton.disabled:
            pass
        else:
            application.quit()
            os._exit(0)

    def resumeButtonFunc(self):
        self.toggle()

    def come_in(self, obj=Entity, delay=0):
        obj.scale = (0.5, 0.05)
        obj.x = 2.5
        obj.animate_x(value=0, delay=delay*.1,
                       curve=curve.out_expo, duration=0.5)


    def go_out(self, obj=Entity, delay=0):
        obj.scale = (0.5, 0.05)
        obj.x = 0
        obj.animate_x(value=-2.5, delay=delay*.1,
                       curve=curve.in_expo, duration=0.5)

    def on_enable(self):
        for i in self.buttonlist:
            self.come_in(i, self.buttonlist.index(i))
        print('pmnu:Enabled')
        @after(0.5) 
        def func():
            application.pause()

    def on_disable(self):
        print('pmenu:Disable')
        



    def toggle(self):
        print(self.resumebutton.position)
        if self.enabled:
            application.resume()
            for i in self.buttonlist:
                self.go_out(i, self.buttonlist.index(i))
            @after(delay=len(self.buttonlist)*.1+.3)
            def func():
                self.disable()
                self.filter.setBlurSharpen(1)
            mouse.locked = True
            
            print('app running True')
        else:
            mouse.locked = False
            self.filter.setBlurSharpen(0)
            self.enable()
            print('app running False')



        


if __name__ == "__main__":
    from player import *
    app = Ursina()
    sky=Sky()
    player = Player()
    cube = Entity(model="cube", texture="white_cube")
    pmenu = PauseMenu(player, app)
    pmenu.ignore_paused = True
    def input(key):
        if key == 'escape':
            pmenu.toggle()
    app.run()

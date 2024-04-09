from ursina import *

class Fade(Entity):
    def __init__(self, duration=.5,text='Please Wait'):
        super().__init__(
            model='quad',
            color=color.clear,
            scale=100,
            eternal=True,
            text='Please wait',
            parent=camera.ui,
            z=-10  # Render above everything
        )
        self.duration = duration
        self.txt=Text(text,parent=camera.ui,color=color.clear,font='.imp/assets/font.tff',scale=2,origin=(0,0),z=-11)
        
    

    def fade_in(self):
        self.txt.animate_color(color.white, duration=self.duration, curve=curve.linear)
        self.animate_color(color.black, duration=self.duration, curve=curve.linear)
        invoke(self.fade_out, delay=5)  # Schedule the fade_out() method after the duration

    def fade_out(self):
        self.txt.animate_color(color.clear, duration=self.duration, curve=curve.linear)
        self.animate_color(color.clear, duration=self.duration, curve=curve.linear)

if __name__ == '__main__':
    app = Ursina()
    """duration=1
    def dest():
        destroy(fade)
        print('destroyed')
    def input(key):
        global fade
        if key=='space':
            fade =Entity(model='quad',
            color=color.clear,
            scale=100,
            eternal=True,
            z=10  # Render above everything
            )
            
            fade.animate_color(color.black, duration=duration, curve=curve.linear)
            
        if key=='escape':
            
            fade.animate_color(color.clear, duration=duration, curve=curve.linear)
            invoke(dest,delay=duration)"""
    a=Fade()
    def input(key):
        if key=='space':
            a.fade_in()
    app.run()

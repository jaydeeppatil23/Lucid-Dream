from ursina import *

class ActionBar(Text):
    def __init__(self,text_='[Your Text Goes Here]',color_=color.white,**kwargs):
        super().__init__(
            text=text_,
            color=color.clear,
            origin=(0,0),
            y=-.35,
            **kwargs)
        self.color_=color_
        self.create_background(self.size*1.5)
        self.background.color=color.clear

        self.fade_in()

        for key, value in kwargs.items():
            setattr(self, key, value)


    def fade_in(self):
        self.animate_color(self.color_, duration=.5, curve=curve.linear)
        self.background.animate_color(color.black33, duration=.5, curve=curve.linear)
        invoke(self.fade_out, delay=2)  # Schedule the fade_out() method after the duration

    def fade_out(self):
        self.animate_color(color.clear, duration=1, curve=curve.linear)
        self.background.animate_color(color.clear, duration=1, curve=curve.linear)
        destroy(self,1)

    def destroy(self, delay=1):
        destroy(self, delay)
        del self

if __name__ == '__main__':
    app= Ursina()
    def input(key):
        if key=='space':
            ab=ActionBar('Tatti = 100 rs.',color.gold)
    app.run()
class Settings():
    """存储2048游戏的设置"""
    def __init__(self):
        #屏幕设置
        self.screen_width=530
        self.screen_height=600
        self.bg_color=(230,230,230)

        #方格设置
        self.square_width=120
        self.margin=10
        self.sq_color=(255,255,255)
        self.text_size=64
        self.color_dict={
            '2':(200,200,200),
            '4':(150,150,150),
            '8':(255,255,102),
            '16':(255,153,51),
            '32':(255,51,51),
            '64':(255,0,127),
            '128':(255,0,255),
            '256':(178,102,255),
            '512':(102,102,255),
            '1024':(102,178,255),
            '2048':(0,255,255),
        }

        #计数板设置
        self.b_color=(0,0,0)
        self.board_size=32
        self.borad_pos=(20,20)
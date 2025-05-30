from openai import OpenAI

def llm(grids):
    client = OpenAI(api_key="sk-080ef8fec79e40f392b15579358ba8d1", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个2048游戏专家"},
            {"role": "user", "content": str(grids)+"""2048是这样一个游戏:在4*4的方格中进行,选择一个方向后所有有数字的格子向这个方向移动,2个相同的格子相加,3个相
同的只能合并靠近边缘的两个,4个相同的全部相加。每选择一次方向,4x4格子中空白格子处随机生成一个2或4,合成2048为成功,无处生成2、4则失败.游戏采用计分制,每有两个格子相加,增加的的得分为这两个格子的和.
现在你接收一个4*4矩阵,在提示词最开始已经给出,解析之后它是一个二维列表的形式,其中每个一维列表是一行,四个一维列表按顺序堆叠形成4*4矩阵.根据规则选择上下左右四个方向中的一个,使得这次移动增加的得分最高,如果有不止一个方向移动后的得分最高,则随机选择其中一个.
             选择向上移动,返回U,
             选择向下移动,返回D,
             选择向左移动,返回L,
             选择向右移动,返回R, 
    """},
        ],
        stream=False
    )

    return response.choices[0].message.content[-1]
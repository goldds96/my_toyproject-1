##############################################################################################################
#                                                                                                            #
#               이 프로젝트는 Ursina를 개인적으로 공부하기 위해 만든 toy project입니다.                          #
#                                                                                                            #
#   File name : my_project.py                                                                                #
#                                                                                                            #
#   Reference : Official Ursina -> https://github.com/pokepetter/ursina/blob/master/samples                  #
#                                                                                                            #
#   Assets : https://www.cgtrader.com/3d-models/textures/architectural-textures/minecraft-all-about-blocks   #
#          : https://freesound.org/people/kretopi/sounds/406464/                                             #
#          : https://www.deviantart.com/darth-biomech/art/MilkyWay-galaxy-sphere-map-8k-746133328            #
#          : https://github.com/kairess                                                                      #
#                                                                                                            #
#                                           Made by Kim Dong Soo                                             #
#                                                                                                            #
##############################################################################################################

from ast import Pass
from cgitb import handler
from re import L
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.fps_counter.enabled = True
window.exit_button.visible = True

hit = Audio("assets/punch", autoplay=False)

blocks = [
    load_texture("assets/grass.png"),
    load_texture("assets/stone.png"),
    load_texture("assets/gold.png"),
    load_texture("assets/lava.png"),
    Pass,  # 더 많은 텍스쳐를 추가하고 싶으면 이곳에 추가하기
]

block_id = 1


def input(key: int) -> None:
    """
    사용자에게 키보드 입력을 받아 블록의 텍스쳐를 바꿔주는 함수입니다.
    1번 -> grass, 2번 -> stone, 3번 -> gold, 4번 -> lava이며 더 많은 텍스쳐를 원할 경우 위의 blocks에 추가하여 사용 가능합니다.

    Args:
        key (int) : 사용자의 키보드 입력
    Return:
        None
    """
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id - 1]


def update() -> Vec2:
    """
    사용자의 키보드 입력을 계속 update 해주는 함수입니다.
    마우스 왼쪽키나 마우스 오른쪽키를 누르면 그에 맞는 동작을 수행합니다.

    Args:
        None

    Return:
        Vec2 (Vec2) : 동작을 수행할 위치인 Vec2(x,y) 값을 return 합니다.
    """
    if held_keys["left mouse"] or held_keys["right mouse"]:
        hit.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)


# 게임의 배경 설정
background = Entity(
    parent=scene,
    model="sphere",
    texture=load_texture("assets/space_sky-min.png"),
    scale=500,
    double_sided=True,
)

# 플레이어의 손 설정
hand = Entity(
    parent=camera.ui,
    model="assets/block",
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6),
)

# 이곳에 게임에 사용될 block을 정의합니다.
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="assets/grass.png"):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5,
        )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                Voxel(
                    position=self.position + mouse.normal, texture=blocks[block_id - 1]
                )
            elif key == "right mouse down":
                destroy(self)


# 초기 위치 타일의 크기
for z in range(30):
    for x in range(30):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()

app.run()

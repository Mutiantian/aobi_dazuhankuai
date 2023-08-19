import sys
import time
from aobi_decete import emu_point_new
from aobi_decete import screen_and_predictor
from aobi_decete import grad_list
import ctypes

# 定义Windows API函数
mouse_event = ctypes.windll.user32.mouse_event
SetCursorPos = ctypes.windll.user32.SetCursorPos

import time
import ctypes

# 定义鼠标事件常量
MOUSE_EVENT_LEFT_DOWN = 0x0002
MOUSE_EVENT_LEFT_UP = 0x0004


# 定义鼠标输入结构体
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


# 定义输入结构体
class Input(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MouseInput)]

    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.c_ulong),
                ("_input", _INPUT)]


# 定义SendInput函数的参数类型
SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = (ctypes.c_uint, ctypes.POINTER(Input), ctypes.c_int)
SendInput.restype = ctypes.c_uint


# 定义鼠标点击函数
def click_mouse(count: int = 1, interval=0.02):
    """模拟鼠标点击事件"""

    for i in range(count):
        # 创建一个鼠标左键按下事件
        mouse_down = Input()
        mouse_down.type = 0
        mouse_down.mi.dwFlags = MOUSE_EVENT_LEFT_DOWN

        # 创建一个鼠标左键释放事件
        mouse_up = Input()
        mouse_up.type = 0
        mouse_up.mi.dwFlags = MOUSE_EVENT_LEFT_UP

        # 将事件打包为输入结构体数组
        events = (Input * 2)()
        events[0] = mouse_down
        events[1] = mouse_up

        # 发送输入事件
        SendInput(2, events, ctypes.sizeof(Input))
        # 暂停一下
        time.sleep(interval)


class crood:
    left_botton = (228, 873)
    right_botton = (1688, 884)


class ADBMETHODS:

    def click(self, x, y, clicks=1, interval=0.08):
        # 移动鼠标到指定坐标
        SetCursorPos(x, y)
        # 模拟鼠标左键按下和抬起事件
        click_mouse(clicks, interval=interval)


if __name__ == '__main__':
    # 创建模拟器对象
    dev_obj = ADBMETHODS()

    # 创建yolo对象
    yolo_obj = screen_and_predictor()

    last_click = crood.left_botton
    grad_obj = grad_list()
    yolo_obj.run_cv(grad_obj)
    # 敲掉一个进入循环
    dev_obj.click(crood.left_botton[0], crood.left_botton[1])
    del grad_obj.grads[0]
    time.sleep(0.5)

    # 大于650分的时候开始换挡，二档会比较容易失败
    gear = [[0.023, 0.08], [0.018, 0.075]]
    turn = 1

    while True:
        # time_start_run = time.time()
        count_click = 2

        # 分数大于600分的时候适当提升下速度，牺牲稳定性来冲分
        if turn < 300:
            while count_click > 0:
                grad = grad_obj.grads[0]

                if grad == emu_point_new.left:
                    dev_obj.click(crood.right_botton[0], crood.right_botton[1], interval=gear[0][0])
                    last_click = crood.right_botton
                elif grad == emu_point_new.right:
                    dev_obj.click(crood.left_botton[0], crood.left_botton[1], interval=gear[0][0])
                    last_click = crood.left_botton
                else:
                    dev_obj.click(last_click[0], last_click[1], interval=gear[0][0])
                count_click -= 1
                del grad_obj.grads[0]
            time.sleep(gear[0][1])
            # print(f"本次敲击用时{time.time() - time_start_run}")
        else:
            while count_click > 0:
                grad = grad_obj.grads[0]

                if grad == emu_point_new.left:
                    dev_obj.click(crood.right_botton[0], crood.right_botton[1], interval=gear[1][0])
                    last_click = crood.right_botton
                elif grad == emu_point_new.right:
                    dev_obj.click(crood.left_botton[0], crood.left_botton[1], interval=gear[1][0])
                    last_click = crood.left_botton
                else:
                    dev_obj.click(last_click[0], last_click[1], interval=gear[1][0])
                count_click -= 1
                del grad_obj.grads[0]
            time.sleep(gear[1][1])

        yolo_obj.run_cv(grad_obj)
        turn += 1
        if yolo_obj.failed_record >= 20:
            sys.exit(0)

import os
import mss.tools
import os.path
import pyautogui as pag


class IMAGEMETHOD:
    def __init__(self):
        pass

    @staticmethod
    def get_coordinate(small_image, big_image, confidence=0.7):
        file_not_exist = 0
        if os.path.exists(small_image) is False:
            print(f"small_image: [{small_image}] is not exists")
            file_not_exist += 1
        if os.path.exists(big_image) is False:
            print(f"big_image: [{big_image}] is not exists")
            file_not_exist += 1
        if file_not_exist != 0:
            print("待匹配的图片不存在，请排查:small_image:[{}]; big_image:[{}]".format(small_image, big_image))
            return False
        imgCoordinate = pag.locate(small_image, big_image, confidence=confidence)
        if imgCoordinate is None:
            print(f"未从大图:[{big_image}]中匹配到小图[{small_image}]")
            return False
        return True


class emu_point:
    empty_left = 0
    empty_right = 1
    stock_left = 2
    stock_right = 3


class image_crod:
    def __init__(self, y, x, w, h):
        self.cord = [y, x, w, h]


class emu_point_new:
    right = 0
    left = 1
    empty = 2


class grad_list:
    def __init__(self):
        self.grads = [0]


class screen_and_predictor:
    def __init__(self):
        self.png = "aobi_test.png"
        self.img_obj = IMAGEMETHOD()
        # 1920*1080的模拟器屏幕
        self.first_img = image_crod(355, 397, 936, 230)
        self.second_img = image_crod(283, 717, 157, 84)
        self.third_img = image_crod(44, 706, 157, 84)
        self.click_cache = emu_point_new
        self.cont = 0
        self.failed_record = 0

    def run_cv(self, grad_list: grad_list):
        # 每次识别都会识别两张图
        # time_start = time.time()
        self.__take_screen(*self.second_img.cord, output=f"{self.cont}aobi_test0.png")
        detect = self.__take_predictor_cv()
        if detect == emu_point_new.right:
            if self.click_cache == emu_point_new.left:
                grad_list.grads.append(emu_point_new.empty)
                self.click_cache = emu_point_new.empty
            else:
                grad_list.grads.append(detect)
                self.click_cache = emu_point_new.right
            self.failed_record += 1
        else:
            grad_list.grads.append(detect)
            self.click_cache = emu_point_new.left
            self.failed_record = 0

        self.__take_screen(*self.third_img.cord, output=f"{self.cont}aobi_test0.png")
        detect = self.__take_third_predictor_cv()
        if detect == emu_point_new.right:
            if self.click_cache == emu_point_new.left:
                grad_list.grads.append(emu_point_new.empty)
                self.click_cache = emu_point_new.empty
            else:
                grad_list.grads.append(detect)
                self.click_cache = emu_point_new.right
        else:
            grad_list.grads.append(detect)
            self.click_cache = emu_point_new.left

    def __take_screen(self, top=66, left=204, width=1700, height=700, output="0aobi_test.png"):
        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": width, "height": height}

            # Grab the data
            sct_img = sct.grab(monitor)

            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    def __take_predictor_cv(self):
        images = ["images/right.png", "images/left.png"]
        if self.img_obj.get_coordinate(images[1], f"{self.cont}aobi_test0.png", confidence=0.85) is not False:
            print(f"匹配到了左边")
            return emu_point_new.left
        print(f"未匹配到左边")
        return emu_point_new.right

    def __take_third_predictor_cv(self):
        images = ["images/o_left.png"]
        if self.img_obj.get_coordinate(images[0], f"{self.cont}aobi_test0.png", confidence=0.85) is not False:
            print(f"匹配到了左边")
            return emu_point_new.left
        else:
            print(f"未匹配到左边")
            return emu_point_new.right

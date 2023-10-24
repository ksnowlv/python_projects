# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import cv2


def main():
    # Use a breakpoint in the code line below to debug your script.
    print(cv2.__version__)

    image = cv2.imread('images/1.webp')

    # 缩放图片
    scale_percent = 50  # 缩放比例
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # 在窗口中显示图片
    cv2.imshow('Image', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

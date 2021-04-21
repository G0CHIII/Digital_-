import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
import cv2
from kivy.utils import platform
from pyzbar.pyzbar import decode, ZBarSymbol
import numpy as np

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

class MyCamera(Camera, FloatLayout):
    symbol = StringProperty()
    def __init__(self, **kwargs):
        self._request_android_permissions()
        super(MyCamera, self).__init__(**kwargs)

    @staticmethod
    def is_android():
        return platform == 'android'

    def _request_android_permissions(self):
        """
        Requests CAMERA permission on Android.
        """
        print("_request")

        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)

    def _camera_loaded(self, *largs):
        if kivy.platform == 'android':
            self.texture = Texture.create(size=self.resolution, colorfmt='rgb')
            self.texture_size = list(self.texture.size)
        else:
            self.texture = self._camera.texture
            self.texture_size = list(self.texture.size)
        self.btn_qr = ToggleButton(group='fun', allow_no_selection = False, state='down',
                                   pos_hint = {'center_x': .4, 'y': 1}, size_hint=[None, None], size=[100, 100],
                                   background_normal  = 'qr.png', background_down  = 'qr_dark.png'
                                   )
        self.btn_ar = ToggleButton(group='fun', allow_no_selection = False,
                                   pos_hint = {'center_x': .6, 'y': 1}, size_hint=[None, None], size=[100, 100],
                                   background_normal  = 'ar.png', background_down  = 'ar_dark.png'
                                   )
        self.add_widget(self.btn_qr)
        self.add_widget(self.btn_ar)
        self.frameCounter = 0

    def on_tex(self, *l):
        if kivy.platform == 'android':
            buf = self._camera.grab_frame()
            if buf is None:
                return
            frame = self._camera.decode_frame(buf)
        else:
            ret, frame = self._camera._device.read()
        if frame is None:
            print("No")
        # print('btn_qr:', self.btn_qr.state, 'btn_ar:', self.btn_ar.state)
        if self.btn_qr.state == 'down':
            buf = self.process_frame_qr(frame)
        elif self.btn_ar.state == 'down':
            buf = self.process_frame(frame)
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        if kivy.platform == 'android':
            self.texture.flip_vertical()
        if kivy.platform != 'android':
            self.texture.flip_horizontal()
        super(MyCamera, self).on_tex(*l)

    def process_frame_qr(self, frame):
        codes = decode(frame, symbols=[ZBarSymbol.QRCODE])
        # print('Decoded:', codes)
        if len(codes) == 1:
            self.symbol = codes[0].data.decode("utf-8")
        else:
            self.symbol = ''
        for code in codes:
            self.data = code.data.decode('ascii')
            x, y, w, h = code.rect.left, code.rect.top, \
                         code.rect.width, code.rect.height
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 8)
            cv2.rectangle(frame, code.polygon[0], code.polygon[1], (0, 255, 0), 4)
        if kivy.platform == 'android':
            frame = rotate_image(frame, 90)
            frame = cv2.flip(frame, 1)
        if kivy.platform != 'android':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame.tostring()

    def process_frame(self, frame):
        mv_0 = cv2.imread("mv_0.png")
        vs_0 = cv2.imread("mv_0.png")
        imgTarget_list = [mv_0, vs_0]
        images_list = ['vsadnik', 'vishnya']
        mv_1 = cv2.imread("mv_1.png")
        mv_2 = cv2.imread("mv_2.png")
        mv_3 = cv2.imread("mv_3.png")
        mv_4 = cv2.imread("mv_4.png")
        mv_5 = cv2.imread("mv_5.png")
        mv_list = [mv_1, mv_2, mv_3, mv_4, mv_5]
        vs_list = [mv_1, mv_2, mv_3, mv_4, mv_5]
        anim_list = [mv_list, vs_list]

        orb = cv2.ORB_create()
        imgAug = frame.copy()
        kp2, des2 = orb.detectAndCompute(frame, None)
        imgAug = cv2.drawKeypoints(imgAug, kp2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        kp_mv, des_mv = orb.detectAndCompute(mv_0, None)
        matches = bf.match(des_mv, des2)
        good_matches_mv = sorted(matches, key=lambda x: x.distance)

        kp_vs, des_vs = orb.detectAndCompute(vs_0, None)
        matches = bf.match(des_vs, des2)
        good_matches_vs = sorted(matches, key=lambda x: x.distance)

        imgMatches = [good_matches_mv, good_matches_vs]
        imgMatchesLen = [len(good_matches_mv), len(good_matches_vs)]
        kps = [kp_mv, kp_vs]

        print('imgMatchesLen', imgMatchesLen)

        imgTarget = imgTarget_list[np.argmax(imgMatchesLen)]
        good = imgMatches[np.argmax(imgMatchesLen)]
        kp1 = kps[np.argmax(imgMatchesLen)]
        anim = anim_list[np.argmax(imgMatchesLen)]
        print('Selected image:', images_list[np.argmax(imgMatchesLen)])
        print('len', len(good))

        if len(good) > 50:
            hT, wT, cT = imgTarget.shape
            srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)
            if matrix is not None:
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)

                print('frameCounter', self.frameCounter)
                if self.frameCounter == len(anim):
                    imgVideo = mv_0
                    self.frameCounter = 0
                else:
                    imgVideo = anim[self.frameCounter]

                imgVideo = cv2.resize(imgVideo, (wT, hT))

                imgWarp = cv2.warpPerspective(imgVideo, matrix, (frame.shape[1], frame.shape[0]))
                maskNew = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255, 0))
                maskInv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
                frame =  imgAug
                self.frameCounter += 1
        else:
            print('reset video counter')
            self.frameCounter = 0
        if kivy.platform == 'android':
            frame = rotate_image(frame, 90)
            frame = cv2.flip(frame, 1)
        if kivy.platform != 'android':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame.tostring()

# class CameraClick(BoxLayout):
#     def __init__(self, **kwargs):
#         print("__init__")
#
#         self._request_android_permissions()
#         super(CameraClick, self).__init__(**kwargs)
#
#     @staticmethod
#     def is_android():
#         return platform == 'android'
#
#     def _request_android_permissions(self):
#         """
#         Requests CAMERA permission on Android.
#         """
#         print("_request")
#
#         if not self.is_android():
#             return
#         from android.permissions import request_permission, Permission
#         request_permission(Permission.CAMERA)
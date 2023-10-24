import cv2
import numpy as np

from overrides import overrides

from camera_fusion.camera_fusion.capture import CameraCapture


class UnsupportedMode(RuntimeError): pass
class InvalidFPS(RuntimeError): pass


class ThermoCam160B(CameraCapture):
    """ ThermoEye Infrared Thermal Camera
    
    capture_modes = {0: CaptureMode(160, 120, 9)}
    """

    MIN_TEMP = -10  # temperature
    MAX_TEMP = 140

    @staticmethod

    @overrides
    def connect(self, cap_source:str) -> None:
        super().connect(cap_source)
        self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
        self.cap.set(cv2.CAP_PROP_FOURCC,
                     cv2.VideoWriter.fourcc('Y', '1', '6', ' '))

    @overrides
    def preprocess(self, frame:np.ndarray) -> np.ndarray:
        frame = frame / 65535.0  # rescale 0~65535(16bit img) to 0~1
        frame = frame * (self.max_temp - self.min_temp)
        frame = (frame - np.min(frame)) / (np.max(frame) - np.min(frame))
        frame = cm.plasma(frame)
        frame = frame[:, :, :3]
        frame = frame[:, :, ::-1]
        frame = (frame * 255).astype(np.uint8)  # rescale to 0~255(8bit img)
        frame = cv2.resize(frame, (self.dst_width, self.dst_height))
        return frame
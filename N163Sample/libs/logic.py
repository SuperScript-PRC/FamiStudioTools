import numpy as np
from numpy.typing import NDArray
from scipy import signal
from scipy.io import wavfile
from typing import IO


def resample_audio(input_file: IO[bytes], target_rate=14400):
    """
    将音频文件重采样到目标采样率

    Args:
        input_file: 输入音频文件路径
        target_rate: 目标采样率 (Hz)
    """
    # 读取原始音频文件
    original_rate, data = wavfile.read(input_file)

    # 计算重采样比例
    ratio = target_rate / original_rate

    # 如果是立体声（多声道），需要分别处理每个声道
    if len(data.shape) > 1:
        # 处理多声道
        data = data[:, 0]
    # 单声道处理
    target_length = int(len(data) * ratio)
    resampled_data = signal.resample(data, target_length)

    # # 转换数据类型以保持原始格式
    # if data.dtype == np.int16:
    #     resampled_data = np.clip(resampled_data, -32768, 32767).astype(np.int16)
    # elif data.dtype == np.int32:
    #     resampled_data = np.clip(resampled_data, -2147483648, 2147483647).astype(
    #         np.int32
    #     )
    # elif data.dtype == np.uint8:
    #     resampled_data = np.clip(resampled_data, 0, 255).astype(np.uint8)

    # 保存重采样后的音频
    return np.clip(resampled_data, -2147483648, 2147483647).astype(np.int32)

    # print(f"原始采样率: {original_rate} Hz")
    # print(f"目标采样率: {target_rate} Hz")
    # print(f"原始长度: {len(data)} 采样点")
    # print(f"重采样后长度: {len(resampled_data)} 采样点")


def normalize_to_height_16(samples: NDArray[np.int32]):
    """
    将采样数据归一化到高度范围 [0, 15] (总共16个级别)

    Args:
        samples: 原始采样数据列表

    Returns:
        归一化后的采样数据列表
    """
    # if not samples:
    #     return samples.astype(np.uint8)

    # 转换为numpy数组以便处理
    samples_array = np.array(samples)

    # 找到原始数据的最小值和最大值
    min_val = np.min(samples_array)
    max_val = np.max(samples_array)

    # 如果所有值都相同，返回中间值
    if min_val == max_val:
        raise ValueError("All values are the same")

    # 线性映射到 [0, 15] 范围
    # 目标范围是32个级别 (0 到 15)
    target_min, target_max = 0, 15

    # 执行线性变换: y = (x - min) / (max - min) * (target_max - target_min) + target_min
    normalized = (samples_array - min_val) / (max_val - min_val) * (
        target_max - target_min
    ) + target_min

    # 转换为整数并返回列表
    return normalized.astype(np.uint8)


def to_n163_waves(samples_normalized: NDArray[np.uint8], total_wavelength: int):
    indices = np.arange(total_wavelength, len(samples_normalized), total_wavelength)
    return np.array_split(samples_normalized, indices)

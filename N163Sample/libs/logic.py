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


def normalize_to_height_and_get_volume(
    samples: NDArray[np.int32],
    single_wave_length: int,
    wave_height: int,
    volume_max: int,
    *,
    volume_fix_value: float = 1.1,
    silent_threshold: int = 20,
) -> tuple[NDArray[np.uint8], list[NDArray]]:
    samples_array = np.array(samples)

    min_val = np.min(samples_array)
    max_val = np.max(samples_array)

    if min_val == max_val:
        raise ValueError("All values are the same ..That means no sound!")

    sample_blocks = np.array_split(
        samples_array,
        np.arange(single_wave_length, len(samples_array), single_wave_length),
    )
    target_min, target_max = 0, wave_height
    sample_blocks_normalized = []
    volumes = np.zeros(len(sample_blocks), np.uint8)
    max_vol = 0
    for i, block in enumerate(sample_blocks):
        local_min_val = np.min(block)
        local_max_val = np.max(block)
        local_volume_delta = local_max_val - local_min_val
        if local_volume_delta > silent_threshold:
            volume = max(
                1,
                min(
                    volume_max,
                    round(
                        (local_max_val - local_min_val)
                        / (max_val - min_val)
                        * volume_max
                        * volume_fix_value
                    ),
                ),
            )
        else:
            volume = 0
        normalized = (block - local_min_val) / (local_max_val - local_min_val) * (
            target_max - target_min
        ) + target_min
        sample_blocks_normalized.append(normalized.astype(np.uint8))
        volumes[i] = volume
        if volume > max_vol:
            max_vol = volume

    # print(f"Max vol={max_vol}")

    return volumes, sample_blocks_normalized

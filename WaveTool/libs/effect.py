Wave = list[int]


def chord(wave: Wave, wave_count_avali: int):
    wave_size = len(wave)
    step = wave_size // wave_count_avali
    new_wave: Wave = []
    for i in range(wave_count_avali):
        s = i * step
        wave_add = [wave[(i + s) % wave_size] for i in range(wave_size)]
        for i in range(wave_size):
            new_wave.append(round((wave[i] + wave_add[i]) / 2))
    return new_wave


def pwm(wave: Wave, wave_count_avali: int):
    wave_size = len(wave)
    new_wave: Wave = []
    pwm_value = 0
    step = wave_size // wave_count_avali
    for i in range(wave_count_avali):
        pwm_value += step
        pwm_wave = [15 if j <= i else 0 for j in range(wave_count_avali)]
        if all(pwm_wave):
            pwm_wave[-1] = 0
        new_wave.extend(pwm_wave)
    return new_wave


def averange(wave: Wave, wave_count_avali: int):
    wave_size = len(wave)
    new_wave: Wave = []
    wave_before: Wave = wave.copy()
    # for _ in range(wave_count_avali):
    #     for i, curr in enumerate(wave_before):
    #         left = wave_before[(i + 1) % wave_size]
    #         right = wave_before[(i - 1) % wave_size]
    #         wave[i] = (left + curr + right) // 3
    #     new_wave.extend(wave)
    #     wave_before = wave.copy()
    for _ in range(wave_count_avali):
        for i in range(wave_size):
            curr = wave[i]
            left = wave[(i + 1) % wave_size]
            right = wave[(i - 1) % wave_size]
            wave[i] = (left + curr + right) // 3
        new_wave.extend(wave)
    return new_wave
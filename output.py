import time


def slayer_event_logs(driver, dic):
    driver.slayer_battle_logs.add(time.time(), dic)


def boss_counter(driver):

    if 'Speed Demon' in driver.boss_name:
        driver.demon_count.append(time.time())
    elif 'Red Oni' in driver.boss_name:
        driver.oni_count.append(time.time())
    elif 'Yatsu' in driver.boss_name:
        driver.yatsu_count.append(time.time())
    elif 'Fulst' in driver.boss_name:
        driver.fulst_count.append(time.time())
    elif 'XPS' in driver.boss_name:
        driver.bone_count.append(time.time())
    elif 'Beast' in driver.boss_name:
        driver.beast_count.append(time.time())

    print(f"\n\n{time.strftime('%m/%d %H:%M:%S')}\n{driver.boss_name}:"
          f"\n\n\tSpeed Demon: {rate(driver.demon_count)}"
          f"\n\tRed Oni: {rate(driver.oni_count)}"
          f"\n\tDark Beast: {rate(driver.beast_count)}"
          f"\n\tFulst: {rate(driver.fulst_count)}"
          f"\n\tYatsu: {rate(driver.yatsu_count)}"
          f"\n\tXPS-11A: {rate(driver.bone_count)}\n")


def rate(encounters):
    from statistics import mean
    diff_list = []

    if encounters.__len__() > 1:
        for i in range(1, encounters.__len__()):
            diff_list.append(encounters[i] - encounters[i - 1])
        diff_list.append(time.time() - encounters[-1])
        avg_diff = int(mean(diff_list))
        e = encounters.__len__() - 1
        return f"{e} (every {int(avg_diff/60)} min)"
    else:
        return 0

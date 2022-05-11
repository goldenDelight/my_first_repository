import time


def slayer_event_logs(driver, dic):
    driver.bot.slayer_battle_logs.add(time.time(), dic)


def boss_counter(driver):

    if 'Speed Demon' in driver.bot.boss_name:
        driver.bot.demon_count.append(time.time())
    elif 'Red Oni' in driver.bot.boss_name:
        driver.bot.oni_count.append(time.time())
    elif 'Yatsu' in driver.bot.boss_name:
        driver.bot.yatsu_count.append(time.time())
    elif 'Fulst' in driver.bot.boss_name:
        driver.bot.fulst_count.append(time.time())
    elif 'XPS' in driver.bot.boss_name:
        driver.bot.bone_count.append(time.time())
    elif 'Beast' in driver.bot.boss_name:
        driver.bot.beast_count.append(time.time())

    print(f"\n\n{time.strftime('%m/%d %H:%M:%S')}\n{driver.bot.boss_name}:"
          f"\n\n\tSpeed Demon: {rate(driver.bot.demon_count)}"
          f"\n\tRed Oni: {rate(driver.bot.oni_count)} (1 : {ratio(driver)})"
          f"\n\tDark Beast: {rate(driver.bot.beast_count)}"
          f"\n\tFulst: {rate(driver.bot.fulst_count)}"
          f"\n\tYatsu: {rate(driver.bot.yatsu_count)}"
          f"\n\tXPS-11A: {rate(driver.bot.bone_count)}\n")


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


def ratio(driver):

    encounter_count = driver.bot.demon_count.__len__() + \
                      driver.bot.beast_count.__len__() + \
                      driver.bot.fulst_count.__len__() + \
                      driver.bot.yatsu_count.__len__() + \
                      driver.bot.oni_count.__len__()

    oni_ratio = "{:.2f}".format(encounter_count / driver.bot.oni_count.__len__())
    return oni_ratio

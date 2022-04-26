import json


def track_slayer_battle(driver):
    stats = driver.execute_script("return app.boss.data")

    skills_used = skill_tracker(driver)

    print(f"skills used: {skills_used}/5\n"
          f"player attack: {stats.get('player_attack'):,}\n"
          f"player defense: {stats.get('player_defense'):,}\n"
          f"player hp: {stats.get('player_hp'):,}\n")

    if stats.get('player_hp') != stats.get('player_hp_last'):
        print(f"  hp left: {stats.get('player_hp_last'):,}\n")

    with open("battle_log.txt", 'a') as f:
        json.dump(stats, f)
        f.write("\n")


def skill_tracker(driver):
    data = driver.execute_script("return app")
    deck_dic = data.get('boss').get('data').get('cards')
    active_skills = 0

    for dd in deck_dic:
        if dd.get('activate'):
            active_skills += 1

    return active_skills


def arena_result(driver):
    data = driver.execute_script("return app.arena2.data")
    atk = data.get("attack")

    defense = driver.execute_script(
        "return document.querySelector('div[class^=result_defense_frame]');")

    defense = int(defense.text)

    print(f"\nplayer attack: {atk:,}\n"
          f"opponent defense: {defense:,}\n")

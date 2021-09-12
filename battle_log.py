import json
import io


def track_battle(driver):
    stats = driver.execute_script("return app.boss.data")

    print(f"\nplayer attack: {stats.get('player_attack')}\n"
          f"player defense: {stats.get('player_defense')}\n"
          f"player hp: {stats.get('player_hp')}\n"
          f"  hp left: {stats.get('player_hp_last')}\n")

    with open("battle_log.txt", 'a') as f:
        json.dump(stats, f)
        f.write("\n")

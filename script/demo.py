from user_agent import generate_user_agent


def main(**kwargs):
    for x in range(30):
        print(generate_user_agent())

from user_agent import generate_user_agent


def setup_arg_parser(parser):
    parser.add_argument('-p', '--platform')
    parser.add_argument('-n', '--navigator')


def main(platform, navigator, **kwargs):
    for x in range(30):
        print(generate_user_agent(platform=platform, navigator=navigator))

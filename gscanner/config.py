import logging
from typing import Any

import configargparse

config = None


def get_config() -> Any:
    global log
    parser = configargparse.get_argument_parser(
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c", "--config", required=False, is_config_file=True, help="config file path"
    )
    parser.add_argument(
        "--local", required=False, is_config_file=True, help="local config file path"
    )
    parser.add_argument(
        "--config-save",
        required=False,
        is_write_out_config_file_arg=True,
        help="config file path",
    )

    parser.add_argument("--debug", action="store_true", default=False, help="debug")
    parser.add_argument("--image", default="", help="open image instead of webcam")

    parser.add_argument(
        "--height",
        type=int,
        default=500,
        help="image height for image processing",
    )
    config, _ = parser.parse_known_args()

    if config.debug:
        import jurigged

        logging.getLogger("watchdog").setLevel(logging.INFO)
        jurigged.watch(pattern="*mev_query*.py")

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level=logging.DEBUG if config.debug else logging.INFO,
    )


    return config

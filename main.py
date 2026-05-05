import os
from pprint import pprint
from typing import cast

import dotenv

from pricelab_retriever.adapter.outbound.configuration.load_configuration import LoadConfiguration


def main():
    dotenv.load_dotenv()
    app_configuration = LoadConfiguration(
        cast(str, os.getenv("CONFIGURATION_FILE_PATH"))
    ).load()
    pprint(app_configuration)

if __name__ == "__main__":
    main()
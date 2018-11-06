# -*- coding: utf-8 -*-
import re
import sys
from package import Package
from exception import APIException

__author__ = "Asim Krticic"

class Parser():

    @staticmethod
    def parse_file_content(content):
        """This method is parsing a content of a file that was passed as a console argument.

            Constraints:
            1. Max weight that a package can take is ≤ 100
            2. Package can take max 15 items
            3. Max weight and cost of an item is ≤ 100

            :param content: content of the file
            :type content: string
            :returns: list of packages
            :rtype: list
            :raises: APIException

        """

        packages = []

        for x in content:

            i = Package()
            i.package_limit = int(x.strip().split(":")[0])

            try:
                if i.package_limit > 100:
                    sys.excepthook = APIException.exception_handler
                    raise APIException(
                        'Max weight that a package can take is <= 100!')
            except APIException:
                raise

            # parse items in the package and check for constraints
            for y in x.strip().split(":")[1].strip().split():

                item_properties = y.replace("(", "").replace(
                    ")", "").strip().split(",")
                index = int(item_properties[0])
                weight = float(item_properties[1])
                cost = int(re.sub('[^0-9]', '', item_properties[2]))
                i.add_item(index, weight, cost)

                try:
                    if len(i.items) > 15:
                        sys.excepthook = APIException.exception_handler
                        raise APIException(
                            'Package can take max 15 items!'
                        )
                except APIException:
                    raise

                try:
                    if weight > 100 or cost > 100:
                        sys.excepthook = APIException.exception_handler
                        raise APIException(
                            'Max weight and cost of an item need to be ≤ 100!')
                except APIException:
                    raise

            packages.append(i)

        return packages

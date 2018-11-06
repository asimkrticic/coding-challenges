# -*- coding: utf-8 -*-
import io
import os
import sys
from exception import APIException
from package import Package
from parser import Parser

__author__ = "Asim Krticic"

class Packer:

    global_list = []

    @staticmethod
    def pack(file_path):
        """
            Accepts only absolute path to a file.
            Opens a file and sends the file content to parse_file_content function.

            :param file_path: an absolute path to a file
            :type file_path: string
            :returns: final results of packing
            :rtype: string
            :raises: APIException
            :raises: IOError

        """

        try:
            if file_path is None:
                sys.excepthook = APIException.exception_handler
                raise APIException(
                    'A valid file path expected as an argument!')
        except APIException:
            raise

        try:
            if not os.path.isabs(file_path):
                sys.excepthook = APIException.exception_handler
                raise APIException(
                    'You need to provide an absolute path to a file!')
        except APIException:
            raise

        try:
            if not os.path.exists(file_path):
                sys.excepthook = APIException.exception_handler
                raise APIException('File does not exist!')
        except APIException:
            raise

        try:
            f = io.open(file_path, encoding="utf-8", errors='ignore')
            content = f.readlines()
        except IOError:
            sys.excepthook = APIException.exception_handler
            content = ""
            raise



        # parse file content
        packages = Parser.parse_file_content(content)
        # pack items into packages
        results = Packer.__pack_items(packages)

        return results

    @classmethod
    def __get_item_combinations(cls, package, list_index, item_indexes,
                                total_weight, total_cost):
        """Recursive combination algorithm

            Start from first list_index in package.items[] and find all possible combinations
            with the remaining items in the package. Recur the same procedure for remaining indexes.

            :param package: instance of the class Package
            :type package: Package
            :param list_index: list index of the item in package.items[]
            :type list_index: int
            :param item_indexes:
            :type item_indexes: int
            :param total_weight: accumulated weight of a package
            :type total_weight: int
            :param total_cost: accumulated cost of a package
            :type total_cost: int
            :returns:
            :rtype:

        """
        # iterate through items list starting from last item from previous recursive call
        for value in package.items[list_index:]:
            # skip item if its equal to the last item from previous recursive call
            if package.items[list_index].index == value.index:
                continue

            total_cost_new = total_cost + value.cost
            total_weight_new = total_weight + value.weight
            item_indexes_new = item_indexes[:]
            # check if total weight of current combination of items is less or equal to the package max weight limit
            if total_weight_new < package.package_limit and value.index not in item_indexes:
                item_indexes_new.append(value.index)
                possible_item_combinations = {
                    "item_combinations": ','.join(str(x) for x in item_indexes_new),
                    "total_weight": total_weight_new,
                    "total_cost": total_cost_new
                }
                Packer.global_list.append(possible_item_combinations)
            # find more combinations based on curent combination
            Packer.__get_item_combinations(package, package.items.index(value),
                                           item_indexes_new, total_weight_new,
                                           total_cost_new)

    @classmethod
    def __pack_items(cls, packages):
        """Return combination of items for which the total weight is less
            than or equal to the package limit and the total cost is as large as possible.
            If there are more than one item combinations with the same total_price,
            choose the one with the lowest weight.

            Combinations that are retrieved from __get_item_combinations method and appended to
            global_list are sorted by largest total_cost and lowest total_weight.
            First combination of items from global_list are then put into the __results_string.

            __result_string is delimited by newline


            :param packages: list of packages from file
            :type packages: list
            :returns: results of packing
            :rtype: string

        """

        __result_string = ""

        # get number of packages in the list
        packages_count = len(packages)

        for package_index, package in enumerate(packages):
            Packer.global_list = []

            for counter, value in enumerate(package.items):
                # check if current item's weight is less or equal to the package max weight limit
                if value.weight <= package.package_limit:
                    total_cost = value.cost
                    total_weight = value.weight
                    # create dict object for the first combination of current item, which is current item index
                    possible_item_combinations = {
                        "item_combinations": str(value.index),
                        "total_weight": total_weight,
                        "total_cost": total_cost
                    }
                    Packer.global_list.append(possible_item_combinations)
                    Packer.__get_item_combinations(package, counter,
                                                   [value.index], total_weight,
                                                   total_cost)
            # sort global list of dict object by total_price in descending order and by total_weight in ascending order
            Packer.global_list.sort(
                key=lambda x: (x['total_cost'], -x['total_weight']),
                reverse=True)

            # check if combination complies with the terms and create the string accordingly
            if len(Packer.global_list) == 0:
                __result_string = __result_string + "-" + \
                    ('\n' if packages_count > package_index + 1 else "")
            else:
                __result_string = __result_string + Packer.global_list[0]["item_combinations"] + (
                    '\n' if packages_count > package_index + 1 else "")

        return __result_string

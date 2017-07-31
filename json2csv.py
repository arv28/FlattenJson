# json2csv.py
#
# Description:
#       Convert an array of flat non-hierarchial json objects to a csv file.

## Assumptions ###
# 1. This program requires a input file containing valid json data.
# 2. The argument for the output file is optional. If the output file is not specified,
#    then a default file name of "result.csv" will be created in the same directory where
#    the script is located.
# 3. The input file can contain comma and new line as part of characters in the string. I have
#    not considered any other special characters.
# 4. If the input file is empty, then an output file will not be created and instead a message will
#    be logged on the terminal.
# 5. I have used the json library in python to parse the json data file.

## Usage ##
# python json2csv.py --help
# usage: json2csv.py [-h] -i INPUT_FILE [-o OUTPUT_FILE]

# convert JSON file to CSV

# optional arguments:
#  -h, --help            show this help message and exit
#  -i INPUT_FILE, --input-file INPUT_FILE
#                        Source json file
#  -o OUTPUT_FILE, --output-file OUTPUT_FILE
#                        Destination csv file

## Testing ##
# 1. Tested with a simple valid json file
# 2. Tested with an empty json file
# 3. Tested with a complex json file containing the assumed special characters.
#
# All the 3 test files are included along with the code.



import os
import json
import argparse
import logging

logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)


SPECIAL_CHARS = (',', '\n')

class MyCSV(object):
    """custom class to read and write csv.
    """
    def __init__(self, csv_file):
        self.fp = csv_file   # should be a file like object

    def writeRow(self, values):
        """Takes a list object and writes to the file.
        """
        if not isinstance(values, list):
            raise TypeError("Invalid type %s" % type(values))
        self.fp.write(','.join(map(str, values)))
        self.fp.write('\n')
        return

    def readRow(self):
        raise NotImplementedError("Method of function hasn't been implemented yet.")
        return


def parse_json_to_csv(in_file, out_file):
    """parse json to csv
    """
    data = None
    header = []
    with open(in_file) as json_file:
        data = json.loads(json_file.read())
    if not data:
        print "json data is empty."
        return

    # get list of columns from json data
    for obj in data:
        for key in obj.keys():
            if key not in header:
                header.append(key.encode('utf-8'))
    #print 'Header is %s' % header

    with open(out_file, 'wb') as csv_file:
        mycsv = MyCSV(csv_file)
        # first write the header to the csv file
        mycsv.writeRow(header)
        # read each json object and write to csv
        for item in data:
            item_values = []
            for key in header:
                value = item.get(key, '')
                # if the value of a json key object contains a comma or new line
                # then escape the string with a double quote.
                if isinstance(value, basestring) and any(c in value for c in SPECIAL_CHARS):
                    value = '"' + repr(value) + '"'
                item_values.append(value)
            mycsv.writeRow(item_values)

    return 


def main():

    parser = argparse.ArgumentParser(
        description='convert JSON file to CSV'
    )

    parser.add_argument(
        '-i',
        '--input-file',
        dest='input_file',
        default=None,
        required=True,
        help='Source json file'
    )

    parser.add_argument(
        '-o',
        '--output-file',
        dest='output_file',
        default=None,
        required=False,
        help='Destination csv file'
    )

    args = parser.parse_args()
    # expand if paths contain ~ or %USERPROFILE%
    input_file = os.path.expanduser(args.input_file)
    
    # validate input file
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        raise RuntimeError("Invalid input file %s" % input_file)

    # validate output file
    if not args.output_file:
        # default csv file in current working directory
        output_file = 'result.csv'
    else:
        output_file = os.path.expanduser(args.output_file)

    try:    
        parse_json_to_csv(input_file, output_file)
    except Exception, ex:
        logging.exception(str(ex))
        


if __name__ == '__main__':
    main()

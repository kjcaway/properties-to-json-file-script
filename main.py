"""
This can convert properties file(*.properties) used in message source
to json file(*.json)

usage: python main.py [file path]
"""
import sys
import logging
import re
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s ### %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def main(args):
	try:
		f = args[0]
		logger.info('Target file: ' + str(f))
		data = {}

		for i, line in enumerate(open(f, 'r', encoding='utf', errors='ignore')):
			res = re.match(r'([(A-Z\d_)])+(.*?)+', line) # formatted message line matcher
			if(res is not None):
				field = line.split('=')[0]
				split_idx = line.find('=')
				value = line[(split_idx + 1):]
				value = ''.join(value.rsplit('\n', 1)) # last \n character remove
				value = value.replace('\\n', '\n')

				data[field] = value
		
		file_name = f.split(os.path.sep)[-1] # path separator (windows: \\ , linux: /)
		json_file_name = file_name.split('.')[0] + '.json'

		with open(json_file_name, 'w', encoding='UTF-8-sig') as json_file:
			json_file.write(json.dumps(data, ensure_ascii=False))

	except Exception as e:
		logger.exception(e)


if __name__ == '__main__':
	argument = sys.argv
	del argument[0]
	main(argument)
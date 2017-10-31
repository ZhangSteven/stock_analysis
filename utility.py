# coding=utf-8
# 
# from config_logging package, provides a config object (from config file)
# and a logger object (logging to a file).
# 

import configparser, os



def get_current_directory():
	"""
	Get the absolute path to the directory where this module is in.

	This piece of code comes from:

	http://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python
	"""
	return os.path.dirname(os.path.abspath(__file__))



def _load_config(filename='analysis.config'):
	"""
	Read the config file, convert it to a config object. The config file is 
	supposed to be located in the same directory as the py files, and the
	default name is "config".

	Caution: uncaught exceptions will happen if the config files are missing
	or named incorrectly.
	"""
	cfg = configparser.ConfigParser()
	cfg.read(os.path.join(get_current_directory(), filename))
	return cfg



# initialized only once when this module is first imported by others
if not 'config' in globals():
	config = _load_config()



def get_output_directory():
	global config
	d = config['directory']['output']
	if d == '':
		return get_current_directory()
	else:
		return d
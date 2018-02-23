# coding: utf8

import sys
import logging

class abstract_writer:
	'''Abstract class for DiTTo writers.

author: Nicolas Gensollen. October 2017.

'''

	def __init__(self,**kwargs):
		'''Abstract class CONSTRUCTOR.

'''
		if kwargs.has_key('log_file'):
			log_file=kwargs['log_file']
		else:
			log_file='writer.log'

		if kwargs.has_key('output_path'):
			self.output_path=kwargs['output_path']
		else:
			self.output_path='./'

		# create logger 
		self.logger=logging.getLogger('writer')
		self.logger.setLevel(logging.INFO)

		# create file handler which logs everything
		self.fh=logging.FileHandler(log_file)
		self.fh.setLevel(logging.INFO)

		# create console handler with WARNING log level
		self.ch=logging.StreamHandler()
		self.ch.setLevel(logging.WARNING)

		# create formatter and add it to the handlers
		formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.fh.setFormatter(formatter)
		self.ch.setFormatter(formatter)

		# add the handlers to the logger
		self.logger.addHandler(self.fh)
		self.logger.addHandler(self.ch)


	#@abstractmethod
	def write(self, model, **kwargs):
		'''Write abstract method.

.. note:: To be implemented in subclasses.

'''
		pass




	def convert_from_meters(self, quantity, unit, **kwargs):
		'''Converts a distance in meters to a distance in given unit.

:param quantity: Distance in meter to convert
:type quantity: float
:param unit: The unit to convert to
:type unit: str (see below the units supported)
:param inverse: Use inverse ration (see below)
:type inverse: bool
:returns: The distance in the requested unit
:rtype: float

**Units supported:**

The units supported are the OpenDSS available units:

        - miles ('mi')
        - kilometers ('km')
        - kilofeet ('kft')
        - meters ('m')
        - feet ('ft')
        - inches ('in')
        - centimeters ('cm')


**Ratios:**

The ratios used are the ones provided by Google. The following table summerize the multipliers to obtain the unit:

+--------+------------+
|  Unit  | Multiplier |
+========+============+
|   mi   | 0.000621371|
+--------+------------+
|   km   |    0.001   |
+--------+------------+
|   kft  | 0.00328084 |
+--------+------------+
|    m   |     1      |
+--------+------------+
|   ft   |   3.28084  |
+--------+------------+
|   in   |   39.3701  |
+--------+------------+
|   cm   |     100    |
+--------+------------+
            
.. note:: If the unit is not one of these, the function returns None

.. warning:: This function is a duplicate (also exists for the OpenDSS reader). Reproduce here for convenience.

.. seealso:: convert_to_meters, unit_conversion
        
'''
		if kwargs.has_key('inverse') and isinstance(kwargs['inverse'], bool):
			inverse=kwargs['inverse']
		else:
			inverse=False

		if unit is None:
			return None

		if not isinstance(unit, unicode):
			self.logger.warning('convert_from_meters() expects a unit in string format')
			return None

		if quantity is None:
			return None

		if unit.lower()=='mi':
			if inverse:
				return quantity/0.000621371
			else:
				return 0.000621371*quantity
                
		elif unit.lower()=='km':
			if inverse:
				return quantity/10**-3
			else:
				return 10**-3*quantity
                
		elif unit.lower()=='kft':
			if inverse:
				return quantity/0.00328084
			else:
				return 0.00328084*quantity

		elif unit.lower()=='m':
			return quantity

		elif unit.lower()=='ft':
			if inverse:
				return quantity/3.28084
			else:
				return 3.28084*quantity

		elif unit.lower()=='in':
			if inverse:
				return quantity/39.3701
			else:
				return 39.3701*quantity

		elif unit.lower()=='cm':
			if inverse:
				return quantity/100
			else:
				return 100*quantity

		else:
			return None


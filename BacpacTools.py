from lxml import etree as ET
from pathlib import Path
import hashlib

class BacpacContentTool():
	def __init__(self, dir_path):
		self.dir_path = dir_path
		self.model_path = Path(dir_path) / 'model.xml'
		self.origin_path = Path(dir_path) / 'Origin.xml'

		self.model_xml = ET.parse(str(self.model_path))
		self.model_root = self.model_xml.getroot()
		self.origin_xml = ET.parse(str(self.origin_path))
		self.origin_root = self.origin_xml.getroot()

	def __enter__(self):
		return self

	def remove_external_tables(self):
		removed = self.remove_elements_with_type(self.model_root, 'SqlExternalTable')
		print(f'Removed {removed} external tables')
		
	def remove_external_data_sources(self):
		removed = self.remove_elements_with_type(self.model_root, 'SqlExternalDataSource')
		print(f'Removed {removed} external data sources')

	def remove_elements_with_type(self, root, type):
		elements = root.xpath(f"//*[@Type='{type}']")
		num_elements = len(elements)
		for element in elements:
			element.getparent().remove(element)
		return num_elements

	def recalculate_hash(self):
		element = self.origin_root.xpath("//*[@Uri='/model.xml']")[0]
		with open(self.model_path, "rb") as model_file:
			sha256_hash = hashlib.sha256(model_file.read())
			sha256_hashed = sha256_hash.hexdigest()
		element.text = sha256_hashed
		print(f'Rehashed file with SHA256')
		print(sha256_hashed)
	
	def rewrite_file(self, path, root):
		with open(str(path), 'w') as output:
			output.write(ET.tostring(root, pretty_print=True, xml_declaration=True).decode('utf-8'))

	def close(self):
		print(f'Finished with file, destructing')
		self.rewrite_file(self.model_path, self.model_root)
		self.recalculate_hash()
		self.rewrite_file(self.origin_path, self.origin_root)

	def __exit__(self, *args):
		self.close()
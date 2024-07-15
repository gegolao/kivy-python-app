import json
import requests

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory



class OrgButton(ListItemButton):
	pass

class GetOrg(BoxLayout):
	
	search_results = ObjectProperty()
	
	def get_org(self):
		org_file = {}
		url = "https://dashboard.meraki.com/api/v0/organizations"

		headers = {
    		'content-type': "application/json",
    		'x-cisco-meraki-api-key': "XXX", # <--- YOUR API KEY
    		'cache-control': "no-cache",
    		}

		search_response = requests.request("GET", url, headers=headers)
		request = self.found_org(search_response, org_file)
		
	def found_org(self, search_response, org_file):
		org_file = search_response.json()
		print (org_file)
		output_org = ['Organization:  {}   ID:  {}' .format(d['name'], d['id']) for d in org_file]
		#self.search_results.item_strings = org_file
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(output_org)
		self.search_results._trigger_reset_populate()
		

class ProvisionRoot(BoxLayout):
	
	def show_current_org(self, org):
		org_id=org.split(':  ')[-1]
		url = "https://dashboard.meraki.com/api/v0/organizations/" +str(org_id) +"/inventory"
		print (url)
		headers = {
    		'content-type': "application/json",
    		'x-cisco-meraki-api-key': "XXX",   # <---- YOUR API Key
    		'cache-control': "no-cache",
    		}
		print (headers)
		search_response = requests.request("GET", url, headers=headers)
		inventory_file = search_response.json()
		print (inventory_file)
		output_inventory = ['Model: {}  Mac_Addr: {} Serial: {}' .format(d['model'], d['mac'], d['serial'])for d in inventory_file]
		print (output_inventory)
		self.clear_widgets()
		current_inventory = Factory.show_current_org()
		current_inventory.inventory = output_inventory
		current_inventory.org_id = org_id
		self.add_widget(current_inventory)
		#url = "https://dashboard.meraki.com/api/v0/organizations/" +str(org_id) +" /inventory"
		#headers = {
    	#'content-type': "application/json",
    	#'x-cisco-meraki-api-key': "XXX",
    	#'cache-control': "no-cache",
    	#}
		#inventory_search = requests.request("GET", url, headers=headers)
		#request=self.found_inventory(inventory_search, inventory_file)
		
	def claimDev(self, serial, org_id):
		url = "https://dashboard.meraki.com/api/v0/organizations/" +str(org_id) + "/claim"
		device = {}
		headers = {'content-type': "application/json",'x-cisco-meraki-api-key': "XXX",'cache-control': "no-cache"} # <--- YOUR API KEY
		device['serial'] = format(str(serial))
		print (device)
		sepp=json.dumps(device)
		newdevice=requests.post(url, data = sepp, headers=headers)
		print (newdevice)
		
	def show_GetOrg(self):
		self.clear_widgets()
		self.add_widget(GetOrg())
		
	pass

class Provision(App):
	pass

if __name__ == '__main__':
	Provision() .run()

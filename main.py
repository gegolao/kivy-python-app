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
    		'x-cisco-meraki-api-key': "YOUR API KEY",
    		'cache-control': "no-cache",
    		}

		search_response = requests.request("GET", url, headers=headers)
		request = self.found_org(search_response, org_file)
		
	def found_org(self, search_response, org_file):
		org_file = search_response.json()
		output_org = ['Organization:  {}   ID:  {}' .format(d['name'], d['id']) for d in org_file]
		self.search_results.item_strings = org_file
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(output_org)
		self.search_results._trigger_reset_populate()
		
#class Current_Org(BoxLayout):

class ProvisionRoot(BoxLayout):
	
	inventory = ObjectProperty()

	def show_current_org(self, org):
		self.clear_widgets()
		current_org = Factory.show_current_org()
		current_org.org = org
		self.add_widget(current_org)
		org_id= current_org.org
		org_id=org_id.split(':  ')
		org_id2=org_id[-1]
		request = self.get_inventory(org_id2)
		
	
	def get_inventory(self, org_id2):
		inventory_file={}
		url = "https://dashboard.meraki.com/api/v0/organizations/" +str(org_id2) +" /inventory"
		headers = {
    	'content-type': "application/json",
    	'x-cisco-meraki-api-key': "YOUR API KEY",
    	'cache-control': "no-cache",
    	}
		inventory_search = requests.request("GET", url, headers=headers)
		#request=self.found_inventory(inventory_search, inventory_file)
		
	#def found_inventory(self, inventory_search, inventory_file):
		inventory_file = inventory_search.json()
		inventory_output = ['Model: {}  Mac_Addr: {} Serial: {}' .format(d['model'], d['mac'], d['serial'])for d in inventory_file]
		#self.inventory.item_strings = org_id2
		print(inventory_output)
		
	
	def show_GetOrg(self):
		self.clear_widgets()
		self.add_widget(GetOrg())
		
	pass

class Provision(App):
	pass

if __name__ == '__main__':
	Provision() .run()


 
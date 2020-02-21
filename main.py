from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
import json
from kivy.uix.listview import ListItemButton

class CurrentWeather(BoxLayout):
	location = ListProperty(["New York", "US"])
	conditions = StringProperty()
	temp = NumericProperty()
	temp_min = NumericProperty()
	temp_max = NumericProperty()
	
	def update_weather(self):
		weather_template='https://api.openweathermap.org/data/2.5/weather?q={},{}&appid=b6a9148b158f51b7d6dee8424e8fafea&units=imperial'
		weather_url = weather_template.format(*self.location)
		request = UrlRequest(weather_url, self.weather_retrieved)
		
	def weather_retrieved(self, request, data):
		data = json.loads(data.decode()) if not isinstance(data, dict) else data
		self.conditions = data['weather'][0]['description']
		self.temp = data['main']['temp']
		self.temp_min = data['main']['temp_min']
		self.temp_max = data['main']['temp_max']

class LocationButton(ListItemButton):
	location = ListProperty()

class WeatherRoot(BoxLayout):
	current_weather = ObjectProperty()
	def show_current_weather(self, location=None):
		self.clear_widgets()
		if self.current_weather is None:
			self.current_weather = CurrentWeather()
		if location is not None:
			self.current_weather.location = location
			self.current_weather.update_weather()
			self.add_widget(self.current_weather)

	def show_add_location_form(self):
		self.clear_widgets()
		self.add_widget(AddLocationForm())	
		
class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()
	search_result = ObjectProperty()
	
	def args_converter(self, index, data_item):
		city, country = data_item
		return {'location': (city, country)}
	
	def search_location(self):
		try:
			search_template = 'https://api.openweathermap.org/data/2.5/find?q={}&type=like&appid=b6a9148b158f51b7d6dee8424e8fafea'
			search_url = search_template.format(self.search_input.text)
			request = UrlRequest(search_url, self.found_location)
		except Exception as e:
			self.search_results.item_strings = e
			
	def found_location(self, request, data):
		try:
			data = json.loads(data.decode()) if not isinstance(data, dict) else data
			cities = [(d['name'], d['sys']['country']) for d in data['list']]
			'''cities = ["{} ({}) {} temp: {}\xb0F humidity: {}".format(d['name'], 
				d['sys']['country'], 
				d['weather'][0]['description'], 
				round(9/5 * (d['main']['temp'] - 273) + 32), 
				d['main']['humidity']) for d in data['list']]'''
			self.search_results.item_strings = cities
			self.search_results.adapter.data.clear()
			self.search_results.adapter.data.extend(cities)
			self.search_results._trigger_reset_populate()
		except Exception as e:
			self.search_results.item_strings = e
			

			
class WeatherApp(App):
	pass
if __name__=='__main__': WeatherApp().run()

'''
Simple output from weather api
{
{"message":"like",
"cod":"200",
"count":5,
"list":[
		{"id":2643743,"name":"London","coord":{"lat":51.5073,"lon":-0.1277},"main":{"temp":288.82,"pressure":1020,"humidity":72,"temp_min":288.15,"temp_max":290.15},"dt":1534560600,"wind":{"speed":4.6,"deg":240},"sys":{"country":"GB"},"rain":null,"snow":null,"clouds":{"all":75},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}]},
		{"id":6058560,"name":"London","coord":{"lat":42.9886,"lon":-81.2467},"main":{"temp":295.15,"pressure":1013,"humidity":94,"temp_min":295.15,"temp_max":295.15},"dt":1534561200,"wind":{"speed":2.6,"deg":120},"sys":{"country":"CA"},"rain":null,"snow":null,"clouds":{"all":90},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},
		{"id":4298960,"name":"London","coord":{"lat":37.129,"lon":-84.0833},"main":{"temp":297.15,"pressure":1018,"humidity":100,"temp_min":295.15,"temp_max":299.15},"dt":1534559700,"wind":{"speed":1.5,"deg":240},"sys":{"country":"US"},"rain":null,"snow":null,"clouds":{"all":1},"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"01n"}]},
		{"id":4517009,"name":"London","coord":{"lat":39.8864,"lon":-83.4483},"main":{"temp":295.61,"pressure":1016,"humidity":94,"temp_min":295.15,"temp_max":297.15},"dt":1534561020,"wind":{"speed":1.5,"deg":260},"sys":{"country":"US"},"rain":null,"snow":null,"clouds":{"all":1},"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"01n"}]},
		{"id":5016884,"name":"London","coord":{"lat":43.5261,"lon":-93.0627},"main":{"temp":292.31,"pressure":1019,"humidity":100,"temp_min":292.15,"temp_max":293.15},"dt":1534562100,"wind":{"speed":1.5,"deg":10},"sys":{"country":"US"},"rain":null,"snow":null,"clouds":{"all":1},"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"01n"}]}
		]
}
'''

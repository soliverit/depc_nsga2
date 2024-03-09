##
# Why do I exist? It's memory efficient to have a single option
# shared by many than a string description for each Retrofit.
##

class RetrofitOption():
	def __init__(self, description):
		self.description	= description
		self.costKey		= description + "-Cost"
		self.efficiencyKey	= description + "-Eff"
		
RetrofitOption.ENVELOPES_HOTWATER_ROOF_WINDOWS 	= RetrofitOption("envelopes_hotwater_roof_windows")
RetrofitOption.HOTWATER_ROOF_WINDOWS 			= RetrofitOption("hotwater_roof_windows")
RetrofitOption.HOTWATER_ROOF 					= RetrofitOption("hotwater_roof")
RetrofitOption.ROOF 							= RetrofitOption("roof")
RetrofitOption.HOTWATER 						= RetrofitOption("hotwater")
RetrofitOption.ROOF_WINDOWS 					= RetrofitOption("roof_windows")
RetrofitOption.WINDOWS 							= RetrofitOption("windows")
RetrofitOption.HOTWATER_WINDOWS 				= RetrofitOption("hotwater_windows")
RetrofitOption.ENVELOPES_HOTWATER_ROOF 			= RetrofitOption("envelopes_hotwater_roof")
RetrofitOption.ENVELOPES_ROOF 					= RetrofitOption("envelopes_roof")
RetrofitOption.ENVELOPES 						= RetrofitOption("envelopes")
RetrofitOption.ENVELOPES_HOTWATER 				= RetrofitOption("envelopes_hotwater")
RetrofitOption.ENVELOPES_ROOF_WINDOWS 			= RetrofitOption("envelopes_roof_windows")
RetrofitOption.ENVELOPES_WINDOWS 				= RetrofitOption("envelopes_windows")
RetrofitOption.ENVELOPES_HOTWATER_WINDOWS 		= RetrofitOption("envelopes_hotwater_windows")
RetrofitOption.AS_BUILT							= RetrofitOption("as_built")
RetrofitOption.RETROFIT_OPTION_DICTIONARY	= {
	"envelopes_hotwater_roof_windows": 	RetrofitOption.ENVELOPES_HOTWATER_ROOF_WINDOWS, 
	"hotwater_roof_windows": 			RetrofitOption.HOTWATER_ROOF_WINDOWS, 
	"hotwater_roof": 					RetrofitOption.HOTWATER_ROOF, 
	"roof": 							RetrofitOption.ROOF, 
	"hotwater": 						RetrofitOption.HOTWATER, 
	"roof_windows": 					RetrofitOption.ROOF_WINDOWS, 
	"windows": 							RetrofitOption.WINDOWS, 
	"hotwater_windows": 				RetrofitOption.HOTWATER_WINDOWS, 
	"envelopes_hotwater_roof":			RetrofitOption.ENVELOPES_HOTWATER_ROOF, 
	"envelopes_roof": 					RetrofitOption.ENVELOPES_ROOF, 
	"envelopes": 						RetrofitOption.ENVELOPES, 
	"envelopes_hotwater": 				RetrofitOption.ENVELOPES_HOTWATER, 
	"envelopes_roof_windows": 			RetrofitOption.ENVELOPES_ROOF_WINDOWS, 
	"envelopes_windows": 				RetrofitOption.ENVELOPES_WINDOWS, 
	"envelopes_hotwater_windows": 		RetrofitOption.ENVELOPES_HOTWATER_WINDOWS,
	"as_built":							RetrofitOption.AS_BUILT
}
RetrofitOption.RETROFIT_OPTION_KEYS			= [
	"envelopes_hotwater_roof_windows",
	"hotwater_roof_windows",
	"hotwater_roof",
	"roof",
	"hotwater",
	"roof_windows",
	"windows",
	"hotwater_windows",
	"envelopes_hotwater_roof",
	"envelopes_roof",
	"envelopes",
	"envelopes_hotwater",
	"envelopes_roof_windows",
	"envelopes_windows",
	"envelopes_hotwater_windows"
]
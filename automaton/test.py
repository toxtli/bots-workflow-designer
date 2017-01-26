from modules.UserRequesterModule import UserRequesterModule
from modules.BotsCreatorModule import BotsCreatorModule
from modules.ConnectionRequesterModule import ConnectionRequesterModule
from modules.MessengerModule import MessengerModule
from modules.ProfilesExtractorModule import ProfilesExtractorModule
from modules.ProfilesFinderModule import ProfilesFinderModule
from modules.ProfilesGeneratorModule import ProfilesGeneratorModule

user = UserRequesterModule()
creator = BotsCreatorModule()
connection = ConnectionRequesterModule()
messenger = MessengerModule()
extractor = ProfilesExtractorModule()
finder = ProfilesFinderModule()
generator = ProfilesGeneratorModule()

user.add_node({'type':'in','name':'platforms','source':'User'})
user.add_node({'type':'in','name':'expertise','source':'User'})
user.add_node({'type':'in','name':'feedback','source':'Linked'})
user.add_node({'type':'out','name':'results','source':'Table'})

generator.add_node({'type':'in','name':'platforms','source':'Linked'})
generator.add_node({'type':'in','name':'expertise','source':'Linked'})
generator.add_node({'type':'in','name':'gender','source':'User'})
generator.add_node({'type':'in','name':'feedback','source':'Linked'})
generator.add_node({'type':'out','name':'profiles','source':'Linked'})

creator.add_node({'type':'in','name':'platforms','source':'Linked'})
creator.add_node({'type':'in','name':'profiles','source':'Linked'})
creator.add_node({'type':'out','name':'bots','source':'Linked'})

finder.add_node({'type':'in','name':'bots','source':'Linked'})
finder.add_node({'type':'in','name':'platforms','source':'Linked'})
finder.add_node({'type':'in','name':'expertise','source':'Linked'})
finder.add_node({'type':'in','name':'location','source':'User'})
finder.add_node({'type':'out','name':'contacts','source':'Linked'})

connection.add_node({'type':'in','name':'bots','source':'Linked'})
connection.add_node({'type':'in','name':'contacts','source':'Linked'})
connection.add_node({'type':'in','name':'message','source':'User'})
connection.add_node({'type':'out','name':'accepted','source':'Linked'})

extractor.add_node({'type':'in','name':'bots','source':'Linked'})
extractor.add_node({'type':'in','name':'accepted','source':'Linked'})
extractor.add_node({'type':'out','name':'userdata','source':'Table'})

messenger.add_node({'type':'in','name':'bots','source':'Linked'})
messenger.add_node({'type':'in','name':'userdata','source':'Linked'})
messenger.add_node({'type':'in','name':'feedback','source':'Linked'})
messenger.add_node({'type':'in','name':'message','source':'User'})
messenger.add_node({'type':'out','name':'results','source':'Linked'})

user.connect({'name':'platforms', 'target':generator})
user.connect({'name':'expertise', 'target':generator})
user.connect({'name':'feedback', 'target':generator})

generator.connect({'name':'platforms', 'target':creator})
generator.connect({'name':'expertise', 'target':finder})
generator.connect({'name':'feedback', 'target':messenger})
generator.connect({'name':'profiles', 'target':creator})

creator.connect({'name':'platforms', 'target':finder})
creator.connect({'name':'bots', 'target':finder})

finder.connect({'name':'bots', 'target':connection})
finder.connect({'name':'contacts', 'target':connection})

connection.connect({'name':'bots', 'target':extractor})
connection.connect({'name':'accepted', 'target':extractor})

extractor.connect({'name':'bots', 'target':messenger})
extractor.connect({'name':'userdata', 'target':messenger})

messenger.connect({'name':'results', 'target':user})

connection.set_values({'message':'Please accept my request.'})
messenger.set_values({'message':'Hello friend'})
finder.set_values({'location':'United States'})

user.set_values({'platforms':'Linkedin'})
user.set_values({'expertise':'Software Engineering'})
user.set_values({'feedback':'Initial Advice'})

print('Done')
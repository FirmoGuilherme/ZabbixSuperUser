from src.Item import Item
from src.Utils import ZabbixAPI


item = Item(ZabbixAPI.item.get(itemids=129892)[0])
item.getHistory()
item.convertHistory()
#print(item.__dict__)
for key, value in item.__dict__.items():
	if key != "histRawValues" and key != "rawHistory":
		print(f"{key} - {value}")

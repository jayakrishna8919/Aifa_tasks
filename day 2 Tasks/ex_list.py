l={"fruits":["mango","banana","peer"],"vegetables":["potato","tomato","brinjal"]}

# for fruit in l["fruits"]:
#     for vegie in l["vegetables"]:
#         if vegie[0]==fruit[0]:
#                 print(vegie)
#                 print(fruit)



l=[(fruit,vegie) for fruit in l["fruits"] for vegie in l["vegetables"] if vegie[0]==fruit[0]]

for k,v in l:
    print(k,v)
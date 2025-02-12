class_all = {"person": {"outer": ["Coat", "jacket", "Jumper", "Padding"],
                         "middle": ["vest", "Cardigan"],
                         "inner": ["Blouse", "Top", "shirts"]}}

ids=[]
labels=[]
def make_idNum():
    m_id = 0
    if len(ids) == 0:
        ids.append(0)
    else:
        m_id = ids[-1]+1
        ids.append(m_id)
    return m_id

class LabelingClass:
    id=int
    name=str
    supercategory="none"

    def __init__(self, name, super):
        self.id = make_idNum()
        self.name=name
        self.supercategory=super

    def make_dic(self):
       dic = dict()
       dic["id"] = self.id
       dic["name"] = self.name
       dic["supercategory"]=self.supercategory
       return dic


# Level 1
person=LabelingClass(name="person",super="none")
labels.append(person.make_dic())
# Level 2
for key in class_all["person"].keys():
    k = LabelingClass(name=key, super="person")
    labels.append(k.make_dic())
    # Level 3
    for i in class_all["person"].get(key):
        val=LabelingClass(name=i, super=key)
        labels.append(val.make_dic())

print(labels)

# [{'id': 0, 'name': 'person', 'supercategory': 'none'},
# {'id': 1, 'name': 'outer', 'supercategory': 'person'},
# {'id': 2, 'name': 'Coat', 'supercategory': 'outer'},
# {'id': 3, 'name': 'jacket', 'supercategory': 'outer'},
# {'id': 4, 'name': 'Jumper', 'supercategory': 'outer'},
# {'id': 5, 'name': 'Padding', 'supercategory': 'outer'},
# {'id': 6, 'name': 'middle', 'supercategory': 'person'},
# {'id': 7, 'name': 'vest', 'supercategory': 'middle'},
# {'id': 8, 'name': 'Cardigan', 'supercategory': 'middle'},
# {'id': 9, 'name': 'inner', 'supercategory': 'person'},
# {'id': 10, 'name': 'Blouse', 'supercategory': 'inner'},
# {'id': 11, 'name': 'Top', 'supercategory': 'inner'},
# {'id': 12, 'name': 'shirts', 'supercategory': 'inner'}]
import bpy
import json
from bpy.types import Menu, Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

def osc_export_config(scene):
    config_table = {}
    for osc_item in scene.NodeOSC_keys:
        config_table[osc_item.osc_address] = {
            "data_path" : osc_item.data_path,
            "id" : osc_item.id,
            "osc_type" : osc_item.osc_type,
            "osc_index" : osc_item.osc_index,
            "osc_direction" : osc_item.osc_direction,
            "enabled" : osc_item.enabled,
        }

    return json.dumps(config_table)

def osc_import_config(scene, config_file):
    config_table = json.load(config_file)
    for address, values in config_table.items():
        print(address)
        print(values)
        item = scene.NodeOSC_keys.add()
        item.osc_address = address
        item.data_path = values["data_path"]
        item.id = values["id"]
        item.osc_type = values["osc_type"]
        item.osc_index = values["osc_index"]
        item.osc_direction = values["osc_direction"]
        item.enabled = values["enabled"]

def parse_ks(item):
    dp = item.data_path
    ID = repr(item.id)

    #custom prop:
    if dp[-1] == ']':
        #it's a simple datapath like ['plop']
        if dp[0] == '[' :
            full_p = ID + dp
            path = ID
            prop = dp
        #it's a composed datapath like foo.bones["bar"]['plop']
        else:
            full_p = ID + '.' + dp
            path = str(full_p.split('][')[0]) + ']'
            prop = '[' + str(full_p.split('][')[1])
    #normal prop:
    else:
        full_p = ID + '.' + dp
        path = '.'.join(full_p.split('.')[:-1])
        prop = full_p.split('.')[-1]

    return full_p, path, prop

#######################################
#  Force Update Sorcar Tree           #
#######################################

class OSC_OT_SorcarTreepdate(bpy.types.Operator):
    """Update sorcar tree"""
    bl_idname = "nodeosc.sorcar_tree_update"
    bl_label = "Create"

    def execute(self, context):
        bpy.context.scene.nodeosc_SORCAR_needsUpdate = True
        return {'FINISHED'}

#######################################
#  Create OSC Settings                #
#######################################

class OSC_OT_ItemCreate(bpy.types.Operator):
    """Create new message handler"""
    bl_idname = "nodeosc.createitem"
    bl_label = "Create"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    copy: bpy.props.IntProperty(default=0)

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        #file = open(self.filepath, 'w')
        #file.write(osc_export_config(context.scene))
        return {'FINISHED'}

    def invoke(self, context, event):
        keys = bpy.context.scene.NodeOSC_keys
        new_item = keys.add()
        if self.copy == -1:
            new_item.id = "location"
            new_item.data_path = "bpy.data.objects['Cube']"
            new_item.osc_address = "/cube/location"
            new_item.osc_index = "()"
        else:
            new_item.id = keys[self.copy].id
            new_item.data_path = keys[self.copy].data_path
            new_item.osc_address = keys[self.copy].osc_address
            new_item.osc_index = keys[self.copy].osc_index
            new_item.osc_direction = keys[self.copy].osc_direction

        #bpy.context.scene.NodeOSC_keys.remove(self.index)

        #for item in bpy.context.scene.NodeOSC_keys:
        #    if item.idx == self.index:
        #        print(bpy.context.scene.NodeOSC_keys.find(item))
        return {'RUNNING_MODAL'}

###########################################
#  Create OSC Settings via Context Menu   #
###########################################
# credits: JPfeP : http://www.jpfep.net/pages/addons/addroutes/
class WM_OT_button_context_addhandler(bpy.types.Operator):
    """Create a new message handler"""
    bl_idname = "nodeosc.button_context_createitem"
    bl_label = "Create a node osc handler"

    # @classmethod
    # def poll(cls, context):
    #      print (context.active_operator)
    #      return context.active_object is not None

    def execute(self, context):
        value1 = getattr(context, "button_pointer", None)
        if value1 is not None:
            id = value1.id_data

        value2 = getattr(context, "button_prop", None)
        if value2 is not None:
            prop = value2.identifier
            keys = bpy.context.scene.NodeOSC_keys
            my_item = keys.add()
            my_item.id = "location"
            my_item.data_path = "bpy.data.objects['Cube']"
            my_item.osc_address = "/context/menu"
            my_item.osc_index = "()"

            # Workaround for materials using nodes
            if id.name == 'Shader Nodetree':
                # Ugly way to guess the good id
                # For materials
                try:
                    id_type = 'materials'
                    id = bpy.context.object.active_material
                    path_from_id = value1.path_from_id(prop)
                    #remove the property from the datapath
                    data_path = 'node_tree.' + path_from_id[0:path_from_id.rindex('.')]

                    # this to raise an error, if needed
                    a = eval(repr(id)+'.'+data_path)

                    #my_item.id_type = id_type
                    #setattr(my_item.id, id_type, id)
                    path = path_from_id.replace(' ','_').replace('.','/').replace("[\"",'/').replace("\"]",'').replace("[",'/').replace("]",'')
                    my_item.osc_address = "/" + id_type + "/" + id.name + "/" + path
                    my_item.data_path = repr(id) + "." + data_path
                    my_item.id = prop
                except:
                    pass
                # For worlds
                try:
                    id_type = 'worlds'
                    id = bpy.context.scene.world
                    path_from_id = value1.path_from_id(prop)
                    #remove the property from the datapath
                    data_path = 'node_tree.' + path_from_id[0:path_from_id.rindex('.')]

                    # this to raise an error, if needed
                    a = eval(repr(id) + '.' + data_path)

                    #my_item.id_type = id_type
                    #setattr(my_item.id, id_type, id)
                    path = path_from_id.replace(' ','_').replace('.','/').replace("[\"",'/').replace("\"]",'').replace("[",'/').replace("]",'')
                    my_item.osc_address = "/" + id_type + "/" + id.name + "/" + path
                    my_item.data_path = repr(id) + "." + data_path
                    my_item.id = prop
                except:
                    pass

            else:
                try:
                    id_type = repr(id).split(".")[2].split('[')[0]
                    path_from_id = value1.path_from_id(prop)
                    data_path = ''
                    if path_from_id.find('.') != -1:
                        #remove the property from the datapath
                        data_path = '.' + path_from_id[0:path_from_id.rindex('.')]
                    
                    #my_item.id_type = id_type
                    #setattr(my_item.id, id_type, id)
                    path = path_from_id.replace(' ','_').replace('.','/').replace("[\"",'/').replace("\"]",'').replace("[",'/').replace("]",'')
                    my_item.osc_address = "/" + id_type + "/" + id.name + "/" + path
                    my_item.data_path = repr(id) + data_path
                    my_item.id = prop
                except Exception as err:
                    print (value1, value2, prop)
                    self.report({'INFO'}, "Error: {0}".format(err))

        return {'FINISHED'}  

#######################################
#  Delete OSC Settings                #
#######################################

class OSC_OT_ItemDelete(bpy.types.Operator):
    """Delete this message handle"""
    bl_idname = "nodeosc.deleteitem"
    bl_label = "Delete"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    index: bpy.props.IntProperty(default=0)

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        #file = open(self.filepath, 'w')
        #file.write(osc_export_config(context.scene))
        return {'FINISHED'}

    def invoke(self, context, event):
        bpy.context.scene.NodeOSC_keys.remove(self.index)

        #for item in bpy.context.scene.NodeOSC_keys:
        #    if item.idx == self.index:
        #        print(bpy.context.scene.NodeOSC_keys.find(item))
        return {'RUNNING_MODAL'}

#######################################
#  Export OSC Settings                #
#######################################

class OSC_Export(bpy.types.Operator):
    """Export the current OSC configuration to a file in JSON format"""
    bl_idname = "nodeosc.export"
    bl_label = "Export Config"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        file = open(self.filepath, 'w')
        file.write(osc_export_config(context.scene))
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


#######################################
#  Import OSC Settings                #
#######################################

class OSC_Import(bpy.types.Operator):
    """Import OSC configuration from a file in JSON format"""
    bl_idname = "nodeosc.import"
    bl_label = "Import Config"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        context.scene.NodeOSC_keys.clear()
        config_file = open(self.filepath, 'r')
        osc_import_config(context.scene, config_file)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class NodeOSC_ImportKS(Operator):
    bl_idname = "nodeosc.importks"
    bl_label = "Import a Keying Set"
    bl_options = {'UNDO'}
    bl_description ="Import the keys of the active Keying Set"

    def verifdefaddr(self,context):
        if context.scene.nodeosc_defaultaddr[0] != "/":
            context.scene.nodeosc_defaultaddr = "/"+context.scene.nodeosc_defaultaddr

    bpy.types.Scene.nodeosc_defaultaddr = bpy.props.StringProperty(default="/blender", description='Form new addresses based on this keyword',update=verifdefaddr)

    def execute(self, context):
        ks = bpy.context.scene.keying_sets.active
        t_arr = [] #temporary array for data_path,id
        id_n = -1

        if str(ks) != "None":
            for items in ks.paths:
                if str(items.id) != "None":     #workaround to avoid bad ID Block (Nodes)

                    tvar_ev,path,prop = parse_ks(items)

                    #Let's break tuple properties into several ones
                    if repr(type(eval(tvar_ev)))!="<class 'str'>":

                        try:
                            l=len(eval(tvar_ev))
                            if items.use_entire_array==True:
                                j = 0
                                k = l
                            else:
                                j = items.array_index
                                k = j+1
                            for i in range(j,k):
                                t_arr.append([prop + "[" + str(i) + "]",path])
                        except:
                            t_arr.append([prop,path])
                    else:
                        t_arr.append([prop,path])



                else:
                    self.report({'ERROR'}, "Missing ID block !")


            #what is the highest ID number ?
            for item in bpy.context.scene.NodeOSC_keys:
                split = item.osc_address.split('/')
                try:
                    if split[1] == bpy.context.scene.nodeosc_defaultaddr[1:]:
                        if int(split[-1]) > id_n:
                            id_n = int(split[-1])
                except:
                    pass


            #Transfer of tvar2 into the NodeOSC_keys_tmp property
            bpy.context.scene.NodeOSC_keys_tmp.clear()
            index = 0
            for i,j in t_arr:
                my_item = bpy.context.scene.NodeOSC_keys_tmp.add()
                my_item.id = i
                my_item.idx = index
                my_item.data_path = j
                #for custom prop
                if i[0:2] == '["' and i[-2:] == '"]':
                    t_eval = my_item.data_path + my_item.id
                #for the others
                else:
                    t_eval = my_item.data_path + "." + my_item.id

                my_item.osc_type = repr(type(eval(t_eval)))[8:-2]
                index = index + 1

            #Copy addresses from NodeOSC_keys if there are some
            for item_tmp in bpy.context.scene.NodeOSC_keys_tmp:
                for item in bpy.context.scene.NodeOSC_keys:
                    if item_tmp.id == item.id and item_tmp.data_path == item.data_path:
                        item_tmp.osc_address = item.osc_address
                        item_tmp.idx = item.idx
                if item_tmp.osc_address == "":
                    id_n += 1
                    item_tmp.osc_address = bpy.context.scene.nodeosc_defaultaddr + "/" + str(id_n)
                item_tmp.osc_index = "()"

            #Simple copy NodeOSC_keys_tmp toward NodeOSC_keys
            item = bpy.context.scene.NodeOSC_keys.clear()
            for tmp_item in bpy.context.scene.NodeOSC_keys_tmp:
                item = bpy.context.scene.NodeOSC_keys.add()
                item.data_path = tmp_item.data_path
                item.id = tmp_item.id
                item.osc_address = tmp_item.osc_address
                item.osc_type = tmp_item.osc_type
                item.osc_index = tmp_item.osc_index
                item.osc_direction = tmp_item.osc_direction
                item.enabled = tmp_item.enabled
                item.idx = tmp_item.idx

        else:
            self.report({'INFO'}, "None found !")

        return{'FINISHED'}

#######################################
#  Pick OSC Address                   #
#######################################

class PickOSCaddress(bpy.types.Operator):
    bl_idname = "nodeosc.pick"
    bl_label = "Pick the last event OSC address"
    bl_options = {'UNDO'}
    bl_description ="Pick the address of the last OSC message received"

    i_addr: bpy.props.StringProperty()

    def execute(self, context):
        last_event = bpy.context.scene.nodeosc_envars.lastaddr
        if len(last_event) > 1 and last_event[0] == "/":
            for item in bpy.context.scene.NodeOSC_keys:
                if item.osc_address == self.i_addr :
                    item.osc_address = last_event
        return{'FINISHED'}

# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(Menu):
    bl_label = "Unused.test"

    def draw(self, context):
        pass
 
def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(WM_OT_button_context_addhandler.bl_idname)

op_classes = (
    PickOSCaddress,
    OSC_Export,
    OSC_Import,
    NodeOSC_ImportKS,
    OSC_OT_ItemDelete,
    OSC_OT_ItemCreate,
    OSC_OT_SorcarTreepdate,
    WM_OT_button_context_addhandler,
    WM_MT_button_context,
)

def register():
    for cls in op_classes:
        bpy.utils.register_class(cls)
    bpy.types.WM_MT_button_context.append(menu_func)


def unregister():
    bpy.types.WM_MT_button_context.remove(menu_func)  # order is important
    for cls in reversed(op_classes):
        bpy.utils.unregister_class(cls)



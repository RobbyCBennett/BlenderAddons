import bpy
from bpy.types import BooleanModifier, Collection, Context, Object, Operator


bl_info = {
	'name': 'Union Selected',
	'version': (0, 0, 1),
	'blender': (3, 0, 0),
	'category': 'Object',
}


class UnionSelectedOperator(Operator):
	bl_idname = 'object.union_selected'
	bl_label = 'Union Selected'

	@classmethod
	def poll(cls, context: Context):
		return len(context.selected_objects) > 1 and context.active_object in context.selected_objects

	def execute(self, context: Context):
		# Make a collection of the other selected objects
		other_objects: Collection = bpy.data.collections.new('tmp')
		for obj in context.selected_objects:
			if obj != context.active_object:
				other_objects.objects.link(obj)

		# Add and apply an exact collection boolean union
		modifier: BooleanModifier = context.active_object.modifiers.new('tmp', 'BOOLEAN')
		modifier.operation = 'UNION'
		modifier.operand_type = 'COLLECTION'
		modifier.collection = other_objects
		bpy.ops.object.modifier_apply(modifier=modifier.name)

		# Deselect the first selected object
		context.active_object.select_set(False)

		# Delete the other objects
		bpy.ops.object.delete(confirm=False)

		return {'FINISHED'}


def menu_func(self, context: Context):
	self.layout.operator(UnionSelectedOperator.bl_idname, text=UnionSelectedOperator.bl_label)


def register():
	bpy.utils.register_class(UnionSelectedOperator)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.utils.unregister_class(UnionSelectedOperator)
	bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == '__main__':
	register()

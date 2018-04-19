

def reference_generator(instance, new_refence=None):
    type = instance.type.code
    sphere = instance.sphere_text
    cylindre = instance.cylindre_text
    axis = instance.axis
    addition = instance.add_text
    reference = "{type}{sphere}{cylindre}{axis} {addition}".format(type=type, sphere=sphere, cylindre=cylindre, addition=addition, axis=axis)
    return reference

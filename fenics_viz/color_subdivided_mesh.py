def color_subdivided_mesh(context, obj, vals, min_val, max_val, col1=(0.5,0.75,1.0), col2=(1.0,0.0,0.0), alpha=0.1):

    # Select the object
    obj.select = True
    context.scene.objects.active = obj

    # Go through all materials
    mat_list = [item.material for item in context.object.material_slots]
    for mat in mat_list:

        # Get the vertex from the name
        i_vert = int(mat.name[-4:])

        # Get the value
        val = (vals[i_vert] - min_val) / (max_val - min_val)

        # Make the color
        mat.diffuse_color = (col1[0]+val*(col2[0]-col1[0]),col1[1]+val*(col2[1]-col1[1]),col1[2]+val*(col2[2]-col1[2]))
        mat.use_transparency = True
        mat.transparency_method = 'MASK'
        mat.alpha = alpha

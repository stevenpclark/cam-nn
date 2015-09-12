import os
from os import path
import bpy
import random
from random import uniform
from math import pi
import shutil


def render(obj_func, n, scale, name, range_list):
    #modifies range_list in place
    obj_func()
    obj = bpy.context.object
    obj.scale = [scale, scale, scale]
    sub_dir = path.join(output_dir, name)
    os.makedirs(sub_dir)
    for i in range(n):
        cam_dist = uniform(4.0, 30.0)
        range_list.append(cam_dist)
        obj_range = cam_dist/2.0 #with 45 FOV, should cover same pixel span of randomness
        cam.location = (0, 0, cam_dist)
        light.location = (uniform(-obj_range, obj_range), uniform(-obj_range, obj_range), 5.0)
        obj.location = (uniform(-obj_range/2, obj_range/2), uniform(-obj_range/2, obj_range/2), 0)
        obj.rotation_euler = (uniform(0,2*pi), uniform(0,2*pi), uniform(0,2*pi))
        scene.render.filepath = path.join(sub_dir, '%05d.png'%(i))
        bpy.ops.render.render(write_still=True)
    bpy.ops.object.delete()


if __name__ == '__main__':
    num_images_per_class = 4096
    render_size = 256

    output_dir = path.join(path.dirname(__file__), 'images')
    print('cleaning up old stuff')
    try:
        shutil.rmtree(output_dir)
    except OSError:
        pass
    os.makedirs(output_dir)

    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = render_size
    scene.render.resolution_y = render_size
    scene.render.resolution_percentage = 100

    cam = bpy.data.objects['Camera']
    light = bpy.data.objects['Lamp']

    range_list = []

    obj_func = bpy.ops.mesh.primitive_ico_sphere_add
    render(obj_func, num_images_per_class, 1.0, '0', range_list)
    render(obj_func, num_images_per_class, 0.7, '1', range_list)

    obj_func = bpy.ops.mesh.primitive_cube_add
    render(obj_func, num_images_per_class, 1.0, '2', range_list)
    render(obj_func, num_images_per_class, 0.7, '3', range_list)

    with open(path.join(output_dir, 'range_list.txt'), 'w') as f:
        f.write('\n'.join(['%.3f'%x for x in range_list]))


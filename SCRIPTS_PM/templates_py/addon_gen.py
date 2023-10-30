#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-10-18 09:47:59
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os
import bpy

# from icecream import ic

classes = ()


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

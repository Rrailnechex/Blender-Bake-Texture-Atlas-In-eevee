| Disclamer!!! This script was created to serve my pipline, which is about creating trim textures in blender and rendering tham to use in unity. btw ist free for everything lol. but now i dont recomend you to use it cz it change schene settings

# Setup
* Get master shader group (Baker.MainShader() currently not included)
* Create layered schene: camera, objects, BG plane with BG material (Baker.BGPlane() currently not included)

# Use
0. Enter Main Shader name, so script can svitch connection in it an render different passes
1. Select camera(s), so each of them will be rendered and saved to default folder
2. Set camera`s name to TA name, so each image will have base name + postfix
3. Bake
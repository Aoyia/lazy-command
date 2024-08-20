from PIL import Image, ImageDraw, ImageFilter

def create_shadow_layer(width, height, blur_radius, color):
    # 创建一个透明的图层
    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_layer)
    
    # 计算阴影的最大透明度
    max_opacity = color[3]
    
    # 为了创建透明度渐变，我们在边缘画多个矩形，透明度从0增加到最大值
    for i in range(blur_radius):
        opacity = int(max_opacity * (i / blur_radius))
        draw.rectangle([i, i, width-i-1, height-i-1], outline=(color[0], color[1], color[2], opacity))
    
    # 使用高斯模糊滤镜来模糊边缘，实现渐变效果
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    return shadow_layer

def add_background_to_screenshot(screenshot_path, background_path, output_path, margin=90, radius=60, shadow_offset=(5, 10), shadow_blur_radius=50, shadow_color=(0, 0, 0, 128)):
    screenshot = Image.open(screenshot_path).convert("RGBA")
    background = Image.open(background_path).convert("RGBA")
    
    screenshot_width, screenshot_height = screenshot.size
    background_width, background_height = background.size
    
    new_width = screenshot_width + 2 * margin
    new_height = screenshot_height + 2 * margin
    
    scale_width = new_width / background_width
    scale_height = new_height / background_height
    scale = max(scale_width, scale_height)
    
    if scale > 1:
        new_background_size = (int(background_width * scale), int(background_height * scale))
        new_background = background.resize(new_background_size, Image.Resampling.LANCZOS)
    else:
        new_background = background
    
    # 创建阴影层，增加模糊半径和调整透明度
    shadow_layer = create_shadow_layer(screenshot_width + 2 * shadow_blur_radius, screenshot_height + 2 * shadow_blur_radius, shadow_blur_radius, shadow_color)
    
    # 创建圆角遮罩
    mask = Image.new('L', (screenshot_width, screenshot_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, screenshot_width, screenshot_height), radius=radius, fill=255)
    
    rounded_screenshot = Image.new('RGBA', screenshot.size)
    rounded_screenshot.paste(screenshot, (0, 0), mask)
    
    # 合并阴影层和背景，调整阴影位置
    left = (new_background.size[0] - screenshot_width) // 2 + shadow_offset[0]
    top = (new_background.size[1] - screenshot_height) // 2 + shadow_offset[1]
    new_background.paste(shadow_layer, (left - shadow_blur_radius, top - shadow_blur_radius), shadow_layer)
    
    # 将圆角截图粘贴到背景上
    new_background.paste(rounded_screenshot, (left, top), mask=mask)
    
    full_output_path = output_path + 'screenshot_with_background.png'
    new_background.save(full_output_path)
    print(f'图片已保存到 {full_output_path}')
    
# 使用示例
screenshot_path = '/Users/neoyuan/Desktop/Xnip2024-04-12_23-31-48.jpg'
background_path = '/Users/neoyuan/Desktop/背景1.png'
output_path = '/Users/neoyuan/Desktop/'

add_background_to_screenshot(screenshot_path, background_path, output_path)
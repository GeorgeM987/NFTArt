import random
from PIL import Image, ImageDraw, ImageChops, ImageFilter


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def random_elipse_points(img_size, padding):
    i_size = img_size[0] - (padding*4)
    size = random.randint(32, 128)
    rand_point_x = random.randint(padding, i_size)
    rand_point_y = random.randint(padding, i_size)
    pa = (rand_point_x - size, rand_point_y - size)
    pb = (pa[0] + size, pa[1] + size)
    return (pa, pb)


def interpolate(start, end, factor):
    recip = 1 - factor
    return (
        int((start[0] * recip) + (end[0] * factor)),
        int((start[1] * recip) + (end[1] * factor)),
        int((start[2] * recip) + (end[2] * factor)),
    )


def generate_art(path):
    target_size = 256
    scale_factor = 9
    image_size = ((target_size * scale_factor), (target_size * scale_factor))
    padding = 24 * scale_factor
    image_bg_color = (0, 0, 0)
    line_start_color = random_color()
    line_end_color = random_color()
    image = Image.new('RGB', image_size, image_bg_color)

    lines = 7
    points = []
    
    for _ in range(lines):
        random_point = (random.randint(padding, (image_size[0] - padding)),
                     random.randint(padding, (image_size[1] - padding)))
        points.append(random_point)
    
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    delta_x = min_x - (image_size[0] - max_x)
    delta_y = min_y - (image_size[0] - max_y)

    for i, point in enumerate(points):        
        points[i] = (point[0] -(delta_x / 2), point[1] - (delta_y / 2))

    sc = line_thickness = 1 * scale_factor
    total_points = len(points) - 1
    for i, point in enumerate(points):
        overlay_img = Image.new('RGB', image_size, image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_img)        

        p1 = point
        if i == total_points:
            p2 = points[0]
        else:
            p2 = points[i + 1]

        line_xy = (p1, p2)
        color_factor = i / total_points
        line_color = interpolate(line_start_color, line_end_color, color_factor)
        overlay_draw.ellipse(((p1[0]-sc), (p1[1]-sc), (p1[0]+sc), (p1[1]+sc)), line_color, line_color, line_thickness)
        overlay_draw.ellipse(((p2[0]-sc), (p2[1]-sc), (p2[0]+sc), (p2[1]+sc)), line_color, line_color, line_thickness)
        overlay_draw.line(line_xy, line_color, line_thickness)
        overlay_draw.ellipse(random_elipse_points(image_size, padding), line_color, line_color, line_thickness)
        if i < 3:
            overlay_draw.arc(line_xy, float(random.randint(-180, 0)), float(random.randint(0, 180)), line_color, line_thickness)
        image = ImageChops.add(image, overlay_img)
        line_thickness += int(scale_factor * 1.25)
        sc += scale_factor / 1.25



    image.filter(ImageFilter.SHARPEN())
    image.filter(ImageFilter.SMOOTH())
    image = image.resize((target_size, target_size), Image.ANTIALIAS)
    image.save(path)

    return image_size, padding


if __name__ == '__main__':
    for i in range(10):
        print(f'Generating NFT #{i+80}')
        generate_art(f'nft_img_#{i+80}.png')

from PIL import Image
import colorsys
import math
import argparse
import os


def save_color_wheel(radius, v, file_path, color_scheme):
    h = w = args.radius * 2
    im = Image.new("RGBA", (h, w), (0, 0, 0, 0))
    cx, cy = im.size[0] / 2, im.size[1] / 2
    pix = im.load()

    for x in range(im.width):
        for y in range(im.height):
            rx = x - cx
            ry = y - cy
            s = (rx**2.0 + ry**2.0) ** 0.5 / args.radius
            if s <= 1.0:
                h = (math.atan2(-rx, ry) + math.pi) / (math.pi * 2)
                if color_scheme == "hls":
                    rgb = colorsys.hls_to_rgb(h, v, s)
                else:
                    rgb = colorsys.hsv_to_rgb(h, s, v)
                pix[x, y] = tuple([int(round(c * 255.0)) for c in rgb])

    im.save(file_path, quality=95)


if __name__ == "__main__":
    DEFAULT_RADIUS = 365
    DEFAULT_VALUE_START = 0
    DEFAULT_VALUE_END = 1.0
    DEFAULT_VALUE_STEP = 0.1
    DEFAULT_APPEND_VALUES = []
    DEFAULT_FILE_PATTERN = "wheel_{:0.2f}.png"
    DEFAULT_OUTPUTDIR = "./imgs"
    DEFAULT_COLOR_SCHEME = "hls"
    parser = argparse.ArgumentParser(description="指定した明度(V)の範囲の色相環をまとめて作成する")
    # radius
    parser.add_argument(
        "-r", "--radius", type=int, metavar="RADIUS", default=DEFAULT_RADIUS, help=f"色相環の半径(default: {DEFAULT_RADIUS})"
    )
    # v_start
    parser.add_argument(
        "--start",
        type=float,
        metavar="START",
        default=DEFAULT_VALUE_START,
        help=f"作成対象の明度範囲の開始値(default: {DEFAULT_VALUE_START})",
    )
    # v_end
    parser.add_argument(
        "--end",
        type=float,
        metavar="END",
        default=DEFAULT_VALUE_END,
        help=f"作成対象の明度範囲の終了値(default: {DEFAULT_VALUE_END})",
    )
    # v_step
    parser.add_argument(
        "--step",
        type=float,
        metavar="STEP",
        default=DEFAULT_VALUE_STEP,
        help=f"作成対象の明度範囲の間隔(default: {DEFAULT_VALUE_STEP}, 小数点以下2桁まで指定可能)",
    )
    # v_additional_values
    parser.add_argument(
        "--append-values",
        type=float,
        metavar="values",
        default=DEFAULT_APPEND_VALUES,
        nargs="+",
        help=f"作成対象の明度範囲の間隔(default: {DEFAULT_APPEND_VALUES})",
    )
    # filename pattern
    parser.add_argument(
        "--filename",
        type=str,
        metavar="FILENAME",
        default=DEFAULT_FILE_PATTERN,
        help=f"作成する画像のファイル名。置換フィールドを指定可能(default: '{DEFAULT_FILE_PATTERN}')",
    )
    # output dir path
    parser.add_argument(
        "--outputdir",
        type=str,
        metavar="OUTPUTDIR",
        default=DEFAULT_OUTPUTDIR,
        help=f"作成する画像を保存するディレクトリ(default: '{DEFAULT_OUTPUTDIR}')",
    )
    # color scheme
    parser.add_argument(
        "--color",
        type=str,
        metavar="COLOR_SCHEME",
        default=DEFAULT_COLOR_SCHEME,
        help=f"カラーホイールのカラースキーム名(hls or hsv) (default: '{DEFAULT_COLOR_SCHEME}')",
    )

    args = parser.parse_args()

    output_dir = os.path.abspath(os.path.expanduser(args.outputdir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_pattern = os.path.join(output_dir, args.filename)
    values = []
    i = args.start
    while round(i, 2) < round(args.end + args.step, 2):
        values.append(round(i, 2))
        i = round(i + args.step, 2)

    values.extend(args.append_values)

    for v in values:
        save_color_wheel(args.radius, v, file_pattern.format(v), args.color)

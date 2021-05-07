from ..utils import BasicSegment
from ..color_tools import get_random_color_and_contrast
from ..colortrans import rgb2short
from socket import gethostname


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        if powerline.segment_conf("hostname", "colorize"):
            hostname = gethostname()

            # use the random color as the background and the contrasting color as the foreground
            background, foreground = get_random_color_and_contrast(hostname)

            foreground, background = (rgb2short(*color) for color in [foreground, background])
            host_prompt = " %s " % hostname.split(".")[0]
            powerline.append(host_prompt, foreground, background)
        else:
            if powerline.args.shell == "bash":
                host_prompt = r" \h "
            elif powerline.args.shell == "zsh":
                host_prompt = " %m "
            else:
                host_prompt = " %s " % gethostname().split(".")[0]
            powerline.append(host_prompt,
                             powerline.theme.HOSTNAME_FG,
                             powerline.theme.HOSTNAME_BG)

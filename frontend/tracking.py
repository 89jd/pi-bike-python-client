import os
import datetime

from types import SimpleNamespace
from PIL import ImageFont

from frontend import Canvas, Output
from client import SocketClient

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')

def create_font(size):
    return ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), size)

ORIGINAL_VALUE_FONT_SIZE = 60

TITLE_FONT = create_font(22)
VALUE_FONT = create_font(ORIGINAL_VALUE_FONT_SIZE)

class TrackingScreen(Canvas):
    def __init__(self, socket_client: SocketClient, output: Output) -> None:
        super().__init__(width=output.width, height=output.height, lock=output.lock)
        self.output = output
        self.output.clear()


        self.draw(lambda draw: draw.rectangle([(0,0), (self.width, self.height)], fill='#468a99'))
        self.reload_output()

        self.duration_in_secs = 0

        socket_client.on_duration_received = self.show_duration
        socket_client.on_exercise_data_received = self.show_exercise_data
        socket_client.on_idle_received = self.show_idle_state

    def reload_output(self):
        self.output.show(self.image)

    def show_exercise_data(self, data):
        set_item = self._set_item

        duration_in_secs = self.duration_in_secs
        
        self.output.switch_backlight(True)

        distance = data['distance']
        rpm = data['rpm']
        self._set_item('Distance', f'{distance:.2f}')
        time_delta_ = datetime.timedelta(seconds=duration_in_secs)
        set_item('Time', str(time_delta_) if time_delta_.seconds / 60 / 60 > 1 else str(time_delta_)[2:])
        set_item('Heartrate', data['heartrate'] if 'heartrate' in data else '-')
        set_item('RPM', f'{rpm:.2f}')

    def show_idle_state(self, is_idle):
        self.is_idle = is_idle
        if is_idle:
            self.output.switch_backlight(False)
        
    def show_duration(self, duration):
        self.duration_in_secs = duration
        time_delta_ = datetime.timedelta(seconds=self.duration_in_secs)
        self._set_item('Time', str(time_delta_) if time_delta_.seconds / 60 / 60 > 1 else str(time_delta_)[2:])
        self.reload_output()

    #Inverted for legacy code, where height and width were wrong way round from LCD
    @property
    def disp(self):
        return SimpleNamespace(**{
            "height": self.width,
            "width": self.height
        })

    def _set_item(self, title, value):
        disp = self.disp

        if title == 'RPM':
            self._draw_section(0, 0, title, value)
        elif title == 'Distance':
            self._draw_section(disp.height/2, disp.width/2, title, value)
        elif title == 'Time':
            self._draw_section(0, disp.width/2, title, value)
        elif title == 'Heartrate':
            self._draw_section(disp.height/2, 0, title, value)

    def _draw_section(self, x, y, title, value):
        disp = self.disp

        self.draw(lambda draw: draw.rectangle([(x, y), (x + disp.height/2, y + disp.width/2)], fill='#468a99'))
        self.draw(lambda draw: draw.rectangle([(x, y), (x + disp.height/2, y + disp.width/2)], outline = 'WHITE'))
        _value_font = VALUE_FONT
        measured_title = TITLE_FONT.getsize(str(title))
        measured_value = VALUE_FONT.getsize(str(value))

        new_value_font_size = ORIGINAL_VALUE_FONT_SIZE

        while measured_value[0] + 5 > disp.height / 2:
            new_value_font_size -= 1
            _value_font = create_font(new_value_font_size)
            measured_value = _value_font.getsize(str(value))

        self.draw(lambda draw: draw.text(((x + disp.height/4) - measured_title[0]/2, y + 10), str(title), font = TITLE_FONT, fill = "WHITE"))

        centre_value_y = (disp.width/2-10+measured_title[1])/2 - measured_value[1]/2
        self.draw(lambda draw: draw.text(((x + disp.height/4) - measured_value[0]/2, y + centre_value_y), str(value), font = _value_font, fill = "WHITE"))

# pi-bike-python-client

## Config File example

```json
{
    "server_address": "http://192.168.0.7:5000",
    "debug_image_location": "/home/pi",
    "remote": { 
        "device_id": "/dev/input/event0",
        "buttons": {
            "reset_button": 158,
            "pause_button": 164,
            "wake_button": 111
        }
    },
    "pi_gpio": {
        "buttons": {    
            "reset_button": {
                "pin": 4,
                "mode": "pull_up"
            }
        }
    },
    "output_type": "debug",
    "waveshare_lib_dir": "waveshare/lib/"
}
```


| Field      | Description |
| ----------- | ----------- |
| server_address      | string. Full address where the server is running  |
| debug_image_location   |if output_type is debug, this is where it will store the jpeg        |
| remote   | 
| pi_gpio   | 
| output_type   | Currently either debug (write to an image) or ST7889 (Waveshare LCD screen) |
| waveshare_lib_dir   | If using waveshare, point to the provided SDK |

| Field      | Description |
| ----------- | ----------- |
| device_id      | String. Input device if using some kind of input on your client  |
| buttons   | Map of button (reset_button, pause_button, wake_button) to the code from the device_id above   |


| Field      | Description |
| ----------- | ----------- |
| buttons   | Map of button (reset_button, pause_button, wake_button) to the corresponding GPIO pin and whether it is a pull up or pull down circuit|

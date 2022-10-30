import os
import configparser

DEFAULT = """
[ui]
main_window_maximized=False
main_window_x=
main_window_y=
main_window_width=
main_window_height=
sash_position=
tx_col0_width=40
tx_col1_width=110
tx_col2_width=180
rx_col0_width=40
rx_col1_width=110
rx_col2_width=180

[serial]
port=
baudrate=9600

[send]
group0_0=
group0_1=
group0_2=
group0_3=
group0_4=
is_hex=True
"""


class Config:

    def __init__(self):
        self._conf_path = os.path.expanduser("~/.config/sptk")
        self._conf_file_path = os.path.join(self._conf_path, "config")
        self._config = configparser.ConfigParser()
        self._config.read_string(DEFAULT)

    def load(self):
        if os.path.exists(self._conf_file_path):
            try:
                self._config.read(self._conf_file_path)
            except configparser.Error:
                pass  # use default settings

    def save(self):
        if not os.path.isdir(self._conf_path):
            os.makedirs(self._conf_path)
        with open(self._conf_file_path, "w") as f:
            self._config.write(f)

    @property
    def main_window_maximized(self):
        return self._config["ui"][f"main_window_maximized"] == "True"

    @main_window_maximized.setter
    def main_window_maximized(self, value):
        self._config["ui"][f"main_window_maximized"] = str(value)

    @property
    def ui_main_window_x(self):
        if self._config["ui"]["main_window_x"]:
            return int(self._config["ui"]["main_window_x"])

    @ui_main_window_x.setter
    def ui_main_window_x(self, value):
        self._config["ui"]["main_window_x"] = str(value)

    @property
    def ui_main_window_y(self):
        if self._config["ui"]["main_window_y"]:
            return int(self._config["ui"]["main_window_y"])

    @ui_main_window_y.setter
    def ui_main_window_y(self, value):
        self._config["ui"]["main_window_y"] = str(value)

    @property
    def ui_main_window_width(self):
        if self._config["ui"]["main_window_width"]:
            return int(self._config["ui"]["main_window_width"])

    @ui_main_window_width.setter
    def ui_main_window_width(self, value):
        self._config["ui"]["main_window_width"] = str(value)

    @property
    def ui_main_window_height(self):
        if self._config["ui"]["main_window_height"]:
            return int(self._config["ui"]["main_window_height"])

    @ui_main_window_height.setter
    def ui_main_window_height(self, value):
        self._config["ui"]["main_window_height"] = str(value)

    @property
    def ui_sash_position(self):
        if self._config["ui"]["sash_position"]:
            return int(self._config["ui"]["sash_position"])

    @ui_sash_position.setter
    def ui_sash_position(self, value):
        self._config["ui"]["sash_position"] = str(value)

    @property
    def ui_tx_cols_width(self):
        return (
            int(self._config["ui"]["tx_col0_width"]),
            int(self._config["ui"]["tx_col1_width"]),
            int(self._config["ui"]["tx_col2_width"]),
        )

    @ui_tx_cols_width.setter
    def ui_tx_cols_width(self, value):
        self._config["ui"]["tx_col0_width"] = str(value[0])
        self._config["ui"]["tx_col1_width"] = str(value[1])
        self._config["ui"]["tx_col2_width"] = str(value[2])

    @property
    def ui_rx_cols_width(self):
        return (
            int(self._config["ui"]["rx_col0_width"]),
            int(self._config["ui"]["rx_col1_width"]),
            int(self._config["ui"]["rx_col2_width"]),
        )

    @ui_rx_cols_width.setter
    def ui_rx_cols_width(self, value):
        self._config["ui"]["rx_col0_width"] = str(value[0])
        self._config["ui"]["rx_col1_width"] = str(value[1])
        self._config["ui"]["rx_col2_width"] = str(value[2])

    @property
    def serial_port(self):
        return self._config["serial"]["port"]

    @serial_port.setter
    def serial_port(self, value):
        self._config["serial"]["port"] = value

    @property
    def serial_baudrate(self):
        return int(self._config["serial"]["baudrate"])

    @serial_baudrate.setter
    def serial_baudrate(self, value):
        self._config["serial"]["baudrate"] = str(value)

    @property
    def send_group0(self):
        return [
            self._config["send"][f"group0_{i}"]
            for i in range(5)
            if self._config["send"][f"group0_{i}"]
        ]

    @send_group0.setter
    def send_group0(self, value):
        for i in range(min(len(value), 5)):
            self._config["send"][f"group0_{i}"] = value[i]

    @property
    def send_is_hex(self):
        return self._config["send"][f"is_hex"] == "True"

    @send_is_hex.setter
    def send_is_hex(self, value):
        self._config["send"][f"is_hex"] = str(value)

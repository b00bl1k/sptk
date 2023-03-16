import wx
import serial
from datetime import datetime as dt
from serial.tools import list_ports
from pubsub import pub

from sptk import config, port, ui, version


class WxListSerialLog(port.SerialLogView):

    def __init__(self, list_ctrl: wx.ListCtrl):
        self.list = list_ctrl

    @classmethod
    def to_hex(cls, data):
        return " ".join(f"{b:02x}" for b in data)

    def update_line(self, index, data):
        self.list.SetItem(index, 2, self.to_hex(data))

    def insert_line(self, index, tm, data):
        self.list.InsertItem(index, str(index + 1))
        self.list.SetItem(index, 1,
                          dt.fromtimestamp(tm).strftime("%H:%M:%S.%f")[:-3])
        self.list.SetItem(index, 2, self.to_hex(data))

    def clear_lines(self):
        self.list.DeleteAllItems()


class SerialPortDialog(ui.SerialPortDialog):
    BAUDRATES = [
        "300", "600", "1200", "2400", "4800", "9600",
        "19200", "38400", "57600", "115200",
    ]
    DATABITS = {
        "5": serial.FIVEBITS,
        "6": serial.SIXBITS,
        "7": serial.SEVENBITS,
        "8": serial.EIGHTBITS,
    }
    PARITY = {
        _("None"): serial.PARITY_NONE,
        _("Event"): serial.PARITY_EVEN,
        _("Odd"): serial.PARITY_EVEN,
        _("Mark"): serial.PARITY_MARK,
        _("Space"): serial.PARITY_SPACE,
    }
    STOPBITS = {
        "1": serial.STOPBITS_ONE,
        "1.5": serial.STOPBITS_ONE_POINT_FIVE,
        "2": serial.STOPBITS_TWO,
    }

    def __init__(self, parent, conf):
        super().__init__(parent)
        self.conf = conf
        self.ports = [port[0] for port in list_ports.comports()]

        def _populate_list(lst, choices, value):
            lst.SetItems(choices)
            try:
                lst.SetSelection(choices.index(value))
            except (ValueError, IndexError):
                pass

        def _key_by_value(d, value):
            for k, v in d.items():
                if v == value:
                    return k
            return ""

        _populate_list(self.list_port, self.ports, conf.serial_port)
        _populate_list(self.list_baud, self.BAUDRATES, str(conf.serial_baudrate))
        _populate_list(self.list_data, list(self.DATABITS.keys()),
                       _key_by_value(self.DATABITS, conf.serial_databits))
        _populate_list(self.list_stop, list(self.STOPBITS.keys()),
                       _key_by_value(self.STOPBITS, conf.serial_stopbits))
        _populate_list(self.list_parity, list(self.PARITY.keys()),
                       _key_by_value(self.PARITY, conf.serial_parity))

    def btn_ok_click(self, event):
        self.conf.serial_port = self.list_port.GetStringSelection()
        self.conf.serial_baudrate = int(self.list_baud.GetStringSelection())
        self.conf.serial_databits = self.DATABITS[self.list_data.GetStringSelection()]
        self.conf.serial_parity = self.PARITY[self.list_parity.GetStringSelection()]
        self.conf.serial_stopbits = self.STOPBITS[self.list_stop.GetStringSelection()]
        event.Skip()


class SendDialog(ui.SendDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        send_group0 = self.parent.conf.send_group0
        if send_group0:
            self.combo_send.SetItems(send_group0)
            self.combo_send.SetSelection(0)
        if self.parent.conf.send_is_hex:
            self.check_hex.Set3StateValue(wx.CHK_CHECKED)

    def btn_send_click(self, event):
        data = self.combo_send.GetValue()
        items = self.combo_send.GetItems()
        if data not in items:
            items.insert(0, data)
            self.combo_send.SetItems(items)
            self.combo_send.SetSelection(0)
            self.parent.conf.serial_send_group0 = items
        if self.check_hex.IsChecked():
            try:
                data_bytes = bytes.fromhex(data.replace(" ", ""))
            except ValueError as e:
                wx.MessageBox(str(e), _("Error"), wx.OK | wx.ICON_ERROR)
                return
        else:
            data_bytes = data.encode("utf-8")
        self.parent.serial_transmit(data_bytes)

    def btn_close_click(self, event):
        self.Hide()

    def check_hex_click(self, event):
        self.parent.conf.send_is_hex = self.check_hex.IsChecked()


class MainWindow(ui.MainWindow):

    TX_COLUMNS = ["#", _("Time"), _("Transmitted")]
    RX_COLUMNS = ["#", _("Time"), _("Received")]

    def __init__(self, parent):
        super().__init__(parent)

        for i, name in enumerate(self.TX_COLUMNS):
            self.tx_list.InsertColumn(i, name)
        for i, name in enumerate(self.RX_COLUMNS):
            self.rx_list.InsertColumn(i, name)

        self.conf = config.Config()
        self.ser = serial.Serial()
        self.ser_receiver = port.SerialReceiver()
        self.ser_worker = None
        self.rx_log_view = WxListSerialLog(self.rx_list)
        self.tx_log_view = WxListSerialLog(self.tx_list)
        self.rx_log = port.SerialLog(self.rx_log_view, 16, delim_time=0.1)
        self.tx_log = port.SerialLog(self.tx_log_view, 16)

        self.load_settings()
        self.splitter.SetSashGravity(0.5)

        self.send_dialog = SendDialog(self)

        pub.subscribe(self.rx_log.add_bytes, "serial.receive")
        pub.subscribe(self.serial_conn_lost, "serial.connection_lost")

        self.update_buttons_state()
        self.update_status_bar()

    def load_settings(self):
        self.conf.load()
        x = self.conf.ui_main_window_x
        y = self.conf.ui_main_window_y
        if x and y:
            self.Move(x, y)
        width = self.conf.ui_main_window_width
        height = self.conf.ui_main_window_height
        if width and height:
            self.SetSize(wx.Size(width, height))
        if self.conf.main_window_maximized:
            self.Maximize(True)
        if self.conf.ui_sash_position:
            self.splitter.SetSashPosition(self.conf.ui_sash_position, True)
        for i, width in enumerate(self.conf.ui_tx_cols_width):
            self.tx_list.SetColumnWidth(i, width)
        for i, width in enumerate(self.conf.ui_rx_cols_width):
            self.rx_list.SetColumnWidth(i, width)
        self.ser.port = self.conf.serial_port
        self.ser.baudrate = self.conf.serial_baudrate

    def save_settings(self):
        if self.IsMaximized():
            self.conf.main_window_maximized = True
        else:
            self.conf.main_window_maximized = False
            x, y = self.GetPosition()
            self.conf.ui_main_window_x = x
            self.conf.ui_main_window_y = y
            width, height = self.GetSize()
            self.conf.ui_main_window_width = width
            self.conf.ui_main_window_height = height
        self.conf.ui_sash_position = self.splitter.GetSashPosition()
        self.conf.ui_tx_cols_width = [
            self.tx_list.GetColumnWidth(i)
            for i, _ in enumerate(self.TX_COLUMNS)
        ]
        self.conf.ui_rx_cols_width = [
            self.rx_list.GetColumnWidth(i)
            for i, _ in enumerate(self.RX_COLUMNS)
        ]
        self.conf.serial_port = self.ser.port
        self.conf.serial_baudrate = self.ser.baudrate
        self.conf.save()

    def update_status_bar(self):
        self.statusbar.SetStatusText(self.ser.port, 1)
        port_conf = "{}-{}-{}-{}".format(
            self.ser.baudrate,
            self.ser.bytesize,
            self.ser.parity,
            self.ser.stopbits,
        )
        self.statusbar.SetStatusText(port_conf, 2)

    def update_buttons_state(self):
        state = self.ser.is_open
        self.toolbar.EnableTool(self.tool_open_port.Id, not state)
        self.toolbar.EnableTool(self.tool_close_port.Id, state)

    def tool_open_port_click(self, event):
        self.serial_open()
        self.update_buttons_state()

    def tool_close_port_click(self, event):
        self.serial_close()
        self.update_buttons_state()

    def tool_exit_click(self, event):
        self.Close()

    def mnu_send_click(self, event):
        self.send_dialog.Show()

    def mnu_ser_port_click(self, event):
        dlg = SerialPortDialog(self, self.conf)
        if dlg.ShowModal() == wx.ID_OK:
            if run := self.ser_worker is not None:
                self.serial_close()
            self.ser.port = self.conf.serial_port
            self.ser.baudrate = self.conf.serial_baudrate
            self.ser.bytesize = self.conf.serial_databits
            self.ser.parity = self.conf.serial_parity
            self.ser.stopbits = self.conf.serial_stopbits
            if run:
                self.serial_open()
            self.update_status_bar()

    def mnu_about_click(self, event):
        wx.MessageBox(f"Serial Port Toolkit v{version.__version__}", _("About"),
                      wx.OK | wx.CENTRE | wx.ICON_INFORMATION)

    def btn_tx_clear_click(self, event):
        self.tx_log.clear()

    def btn_rx_clear_click(self, event):
        self.rx_log.clear()

    def on_close(self, event):
        self.serial_close()
        self.save_settings()
        event.Skip()

    def serial_open(self):
        try:
            if not self.ser.is_open:
                self.ser.open()
            if not self.ser_worker:
                self.ser_worker = port.ReaderThread(self.ser, self.ser_receiver)
                self.ser_worker.start()
        except serial.SerialException as e:
            wx.MessageBox(str(e), _("Error"), wx.OK | wx.ICON_ERROR)

    def serial_close(self):
        if self.ser_worker:
            self.ser_worker.close()
            self.ser_worker = None
        if self.ser.is_open:
            self.ser.close()

    def serial_transmit(self, data):
        if self.ser_worker:
            self.ser_worker.write(data)
            self.tx_log.new_line()
            self.tx_log.add_bytes(data)

    def serial_receive(self, data):
        self.rx_log.add_bytes(data)

    def serial_conn_lost(self):
        self.ser_worker = None
        if self.ser.is_open:
            self.ser.close()
        self.update_buttons_state()


class SptkApplication(wx.App):

    def OnInit(self):
        wnd_main = MainWindow(None)
        wnd_main.Show(True)
        return True

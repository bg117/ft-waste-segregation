import time
import smbus

from ..CombinedSensor import CombinedSensor

class BMX055(object):
    
    GYROMETER_ADDRESS     = 0x68
    MAGNETOMETER_ADDRESS  = 0x10
    ACCELEROMETER_ADDRESS = 0x18

    X_LSB = 0x02
    X_MSB = 0x03
    Y_LSB = 0x04
    Y_MSB = 0x05
    Z_LSB = 0x06
    Z_MSB = 0x07
    
    MODE_REGISTER           = 0x11
    RANGE_REGISTER          = 0x0f
    FILTER_BW_REGISTER      = 0x10
    COMPENSATION_REGISTER_1 = 0x36
    COMPENSATION_REGISTER_2 = 0x37

    MAG_POWER_MODE = 0x4b
    MAG_OP_MODE    = 0x4c
    MAG_CONFIG     = 0x4e
    MAG_REP_XY     = 0x51
    MAG_REP_Z      = 0x52
    
    MAG_X_LSB = 0x42
    MAG_X_MSB = 0x43
    MAG_Y_LSB = 0x44
    MAG_Y_MSB = 0x45
    MAG_Z_LSB = 0x46
    MAG_Z_MSB = 0x47

class Txt4CombinedSensor(CombinedSensor):

    def __init__(self, controller, identifier):
        """
        Initializes the Txt2CombinedSensor.

        Parameters taken from superclass.

        @param controller the TXT controller. Needs to be supplied in order to be compatible with the superclass __init__ method, but will be discarded
        @param identifier The number of the input. Necessary to be compatible with the superclass. Must be supplied but is not used.

        Initializes the accelerometer, gyrometer and magnetometer.

        KNOWN BUG:
        Might fail when the magnetometer is not yet ready.
        """
        CombinedSensor.__init__(self, controller, identifier)
        self.__i2c = smbus.SMBus(3)
        self.__is_accelerometer_initialized = False
        self.__is_magnetometer_initialized = False
        self.__is_gyrometer_initialized = False

    def init_accelerometer(self, data_range = 2, data_bandwidth = 8, compensation = False):
        """
        Set acceleration range to +/- 2g.
        Set filter bandwidth to 7.81 Hz.
        Activate slow and fast compensation for the accelerometer.

        ranges = {2: 0x03, 4: 0x05, 8: 0x08, 16: 0x0c} in g
        filter_bandwidth = {8: 0x08, 16: 0x09, 31: 0x0a, 63: 0x0b1, 125: 0x0c, 250: 0x0d, 500: 0x0e, 1000: 0x0f} in Hz

        Fast compensation: The acceleration value is corrected by 1g after measuring the data.
        Slow compensation: The average acceleration is continuously corrected towards 0 to
        reduce noise.
        """

        ranges = {2: 0x03, 4: 0x05, 8: 0x08, 16: 0x0c}
        bandwidths = {8: 0x08, 16: 0x09, 31: 0x0a, 63: 0x0b1, 125: 0x0c, 250: 0x0d, 500: 0x0e, 1000: 0x0f}

        try:
            range_value = ranges[data_range]
        except:
            val_list = list(ranges.values())
            if data_range in val_list:
                range_value = data_range
                data_range = [k for k, v in ranges.items() if v == range_value][0]
            else:
                raise ValueError('invalid range, use 2, 4, 8 or 16')

        try:
            bandwidth_value = bandwidths[data_bandwidth]
        except:
            val_list = list(bandwidths.values())
            if data_bandwidth in val_list:
                bandwidth_value = data_bandwidth
            else:
               raise ValueError('invalid filter bandwidth, use 8, 16, 31, 63, 125, 250, 500 or 1000')

        # set bandwidth e.g. 7.81 Hz
        self.__i2c.write_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.FILTER_BW_REGISTER, bandwidth_value)
        time.sleep(0.1)
        
        self.__compensation(BMX055.ACCELEROMETER_ADDRESS, ranges[2], range_value, compensation)
        self.__acc_resolution = {2:0.98, 4:1.95, 8:3.91, 16:7.81}[data_range] / 1000
        self.__is_accelerometer_initialized = True

    def init_gyrometer(self, data_range = 125, data_bandwidth = 64, compensation = False):
        """
        ranges = {125: 4, 250: 3, 500: 2, 1000: 1, 2000: 0} in °/s
        filter_bandwidth = {12: 0x05, 23: 0x04, 32: 0x07, 47: 0x03, 64: 0x06, 116: 0x02, 230: 0x01, "unfiltered": 0x00} in Hz

        Sets the speed that the gyrometer is able to detect to a maximum of 125°/s to set the scale.
        Sets the filter bandwidth to 64 Hz.
        """

        ranges = {125: 0x04, 250: 0x03, 500: 0x02, 1000: 0x01, 2000: 0x00}
        bandwidths = {12: 0x05, 23: 0x04, 32: 0x07, 47: 0x03, 64: 0x06, 116: 0x02, 230: 0x01, "unfiltered": 0x00}

        try:
            range_value = ranges[data_range]
        except:
            val_list = list(ranges.values())
            if data_range in val_list:
                range_value = data_range
                data_range = [k for k, v in ranges.items() if v == range_value][0]
            else:
                raise ValueError('invalid range, use 125, 250, 500, 1000 or 2000')

        try:
            bandwidth_value = bandwidths[data_bandwidth]
        except:
            val_list = list(bandwidths.values())
            if data_bandwidth in val_list:
                bandwidth_value = data_bandwidth
            else:
                raise ValueError('invalid filter bandwidth, use 12, 23, 32, 47, 64, 116, 230 or "unfiltered"')
        
        # set bandwidth e.g. 125 Hz
        self.__i2c.write_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.FILTER_BW_REGISTER, bandwidth_value)
        time.sleep(0.1)
        
        self.__compensation(BMX055.GYROMETER_ADDRESS, ranges[125], range_value, compensation)
        self.__gyro_resolution = 2 * data_range / (2**16)
        self.__is_gyrometer_initialized = True

    def init_magnetometer(self, data_rate = 2):
        """
        Initialize the magnetometer.
        Sets the repetition of measurements to 9 repetitions for the X and Y axis and
        16 repetitions for the Z axis.

        rates = {2: 0x08, 6: 0x10, 8: 0x18, 10: 0x00, 15: 0x20, 20: 0x28, 25: 0x30, 30: 0x28} in Hz
        """

        rates = {2: 0x08, 6: 0x10, 8: 0x18, 10: 0x00, 15: 0x20, 20: 0x28, 25: 0x30, 30: 0x28}

        try:
            rate_value = rates[data_rate]
        except:
            val_list = list(rates.values())
            if data_rate in val_list:
                rate_value = data_rate
            else:
                raise ValueError('invalid rate, use 2, 6, 8, 10, 15, 20, 25 or 30')
                
        # switch to suspend mode for full reset (chapter 10.6, page 134)
        self.__i2c.write_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_POWER_MODE, 0x00)
        time.sleep(0.1)
        # switch to sleep mode
        self.__i2c.write_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_POWER_MODE, 0x01)
        time.sleep(0.1)
        # switch to normal mode by set a rate
        self.__i2c.write_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_OP_MODE, rate_value)
        time.sleep(0.1)
        # enable XYZ axis
        self.__i2c.write_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_CONFIG, 0x84)
        time.sleep(0.1)
        # number of repetitions for XY axis = 9 (chapter 10.8, page 138)
        self.__i2c.write_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_REP_XY, 0x04)
        time.sleep(0.1)
        # number of repetitions for Z axis = 16 (chapter 10.8, page 139)
        self.__i2c.write_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_REP_Z, 0x0F)
        time.sleep(0.1)

        self.__is_magnetometer_initialized = True
 
    def __compensation(self, address, default_range, range_value, active):
        """
        With no arguments passed, runs fast compensation.
        With boolean argument passe, activates or deactivates slow compensation.
        """

        # set default range 
        self.__i2c.write_byte_data(address, BMX055.RANGE_REGISTER, default_range)
        time.sleep(0.1)
        # settings x0y0z1 10Hz
        self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_2, 0x21)
        time.sleep(0.1)
        # reset
        self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x80)
        time.sleep(0.1)
        
        if active is None: # trigger fast comp 
            # deactivate slow comp
            self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x00)
            time.sleep(0.1)
            # fast compensation for x
            self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x20) 
            time.sleep(0.1)
            # fast compensation for y
            self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x40)
            time.sleep(0.1)
            # fast compensation for z
            self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x60)
            time.sleep(0.1)
        elif active: # activate slow comp
            self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x07)
            time.sleep(0.1)
        elif not active: # deactivate slow comp
            self.__i2c.write_byte_data(address, BMX055.COMPENSATION_REGISTER_1, 0x00)
            time.sleep(0.1)
        else:
            raise TypeError('pass a boolean or no argument') 
        
        # set range 
        self.__i2c.write_byte_data(address, BMX055.RANGE_REGISTER, range_value)
        time.sleep(0.1)

    def get_acceleration_x(self) -> float:
        """
        Returns the current acceleration in X direction in g. 1g = 9.81m/s^2.
        @returns {float} acceleration in X direction in g
        """
        if self.__is_accelerometer_initialized:
            register = self.__i2c.read_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.X_LSB)
            if register & 1:
                lsb = twos_complement(register >> 4, 4)
                msb = twos_complement(self.__i2c.read_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.X_MSB))
                return (lsb + (msb << 4)) * self.__acc_resolution
        return None
    
    def get_acceleration_y(self) -> float:
        """
        Returns the current acceleration in Y direction in g. 1g = 9.81m/s^2.
        @returns {float} acceleration in Y direction in g
        """
        if self.__is_accelerometer_initialized:
            register = self.__i2c.read_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.Y_LSB)
            if register & 1:
                lsb = twos_complement(register >> 4, 4)
                msb = twos_complement(self.__i2c.read_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.Y_MSB))
                return (lsb + (msb << 4)) * self.__acc_resolution
        return None
    
    def get_acceleration_z(self) -> float:
        """
        Returns the current acceleration in Z direction in g. 1g = 9.81m/s^2.
        @returns {float} acceleration in Z direction in g
        """
        if self.__is_accelerometer_initialized:
            register = self.__i2c.read_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.Z_LSB)
            if register & 1:
                lsb = twos_complement(register >> 4, 4)
                msb = twos_complement(self.__i2c.read_byte_data(BMX055.ACCELEROMETER_ADDRESS, BMX055.Z_MSB))
                return (lsb + (msb << 4)) * self.__acc_resolution
        return None

    def get_rotation_x(self) -> float:
        """
        Returns the rotation speed around the X axis in degrees per second.

        @returns {float} rotation speed around the X axis in degrees per second
        """
        if self.__is_gyrometer_initialized:
            lsb = twos_complement(self.__i2c.read_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.X_LSB))
            msb = twos_complement(self.__i2c.read_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.X_MSB))
            return (lsb + (msb << 4)) * self.__gyro_resolution
        return None

    def get_rotation_y(self) -> float:
        """
        Returns the rotation speed around the Y axis in degrees per second.

        @returns {float} rotation speed around the Y axis in degrees per second
        """
        if self.__is_gyrometer_initialized:
            lsb = twos_complement(self.__i2c.read_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.Y_LSB))
            msb = twos_complement(self.__i2c.read_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.Y_MSB))
            return (lsb + (msb << 4)) * self.__gyro_resolution
        return None

    def get_rotation_z(self) -> float:
        """
        Returns the rotation speed around the X axis in degrees per second.

        @returns {float} rotation speed around the X axis in degrees per second
        """
        if self.__is_gyrometer_initialized:
            lsb = twos_complement(self.__i2c.read_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.Z_LSB))
            msb = twos_complement(self.__i2c.read_byte_data(BMX055.GYROMETER_ADDRESS, BMX055.Z_MSB))
            return (lsb + (msb << 4)) * self.__gyro_resolution
        return None

    def get_magnetic_field_x(self) -> float:
        """
        Returns the current magnetic flux density in X direction in microtesla.
        (chapter 10.4, page 132)
        @returns {float} mangnetic flux density in X direction in microtesla
        """
        if self.__is_magnetometer_initialized:
            lsb = twos_complement(self.__i2c.read_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_X_LSB) & 0b11111000)
            msb = twos_complement(self.__i2c.read_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_X_MSB))
            return (lsb + (msb << 5)) / 16
        return None

    def get_magnetic_field_y(self) -> float:
        """
        Returns the current magnetic flux density in Y direction in microtesla.
        (chapter 10.4, page 133)
        @returns {float} mangnetic flux density in Y direction in microtesla
        """
        if self.__is_magnetometer_initialized:
            lsb = twos_complement(self.__i2c.read_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_Y_LSB) & 0b11111000)
            msb = twos_complement(self.__i2c.read_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_Y_MSB))
            return (lsb + (msb << 5)) / 16
        return None

    def get_magnetic_field_z(self) -> float:
        """
        Returns the current magnetic flux density in Z direction in microtesla.
        (chapter 10.4, page 133-134)
        @returns {float} mangnetic flux density in Z direction in microtesla
        """
        if self.__is_magnetometer_initialized:
            lsb = twos_complement(self.__i2c.read_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_Z_LSB) & 0b11111110)
            msb = twos_complement(self.__i2c.read_byte_data(BMX055.MAGNETOMETER_ADDRESS, BMX055.MAG_Z_MSB))
            return (lsb + (msb << 7)) / 16
        return None


# from stackoverflow J.F. Sebastian
def twos_complement(val, bits=8):
    """
    compute the 2's complement of int val with bits
    """
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is
